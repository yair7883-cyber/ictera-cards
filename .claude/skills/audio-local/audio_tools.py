#!/usr/bin/env python3
"""Local audio toolkit: transcribe, stems, denoise, speakers, midi.

Run with any python3; it installs its venv on first use (setup.sh) and re-runs itself there.
Input is a local file or an http(s) URL. Outputs go to --out (default ./audio-out).
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

HOME = Path(os.environ.get("AUDIO_TOOLS_HOME", Path.home() / ".local/share/audio-tools"))
MODELS = HOME / "models"
HEBREW_MODEL = "ivrit-ai/whisper-large-v3-turbo-ct2"


def pcm(path, sr=16000):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def srt_time(t):
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def label_speakers(segs, turns):
    """Give each transcript segment the speaker (1-based) whose turns overlap it most."""
    for seg in segs:
        overlap = {}
        for start, end, spk in turns:
            overlap[spk] = overlap.get(spk, 0) + max(0.0, min(end, seg["end"]) - max(start, seg["start"]))
        best = max(overlap, key=overlap.get, default=None)
        seg["speaker"] = best + 1 if best is not None and overlap[best] > 0 else None
    return segs


def diarize(path, num_speakers=None):
    import sherpa_onnx as so
    cfg = so.OfflineSpeakerDiarizationConfig(
        segmentation=so.OfflineSpeakerSegmentationModelConfig(
            pyannote=so.OfflineSpeakerSegmentationPyannoteModelConfig(model=str(MODELS / "segmentation.onnx"))),
        embedding=so.SpeakerEmbeddingExtractorConfig(model=str(MODELS / "embedding.onnx")),
        clustering=so.FastClusteringConfig(num_clusters=num_speakers or -1, threshold=0.5),
        min_duration_on=0.3, min_duration_off=0.5)
    if not cfg.validate():
        sys.exit("speaker models missing: run setup.sh")
    sd = so.OfflineSpeakerDiarization(cfg)
    return [(r.start, r.end, r.speaker) for r in sd.process(pcm(path, sd.sample_rate)).sort_by_start_time()]


def transcribe(a):
    from faster_whisper import WhisperModel
    audio = pcm(a.input)
    model = a.model or (HEBREW_MODEL if a.lang == "he" else "turbo")
    segs, info = WhisperModel(model, device="cpu", compute_type="int8").transcribe(audio, language=a.lang, vad_filter=True)
    if not a.model and info.language == "he" and model != HEBREW_MODEL:  # detected Hebrew: the ivrit-ai model is far more accurate
        segs, info = WhisperModel(HEBREW_MODEL, device="cpu", compute_type="int8").transcribe(audio, language="he", vad_filter=True)
    segs = [{"start": s.start, "end": s.end, "text": s.text.strip().strip("‪‫‬‎‏")} for s in segs]
    if a.speakers:
        label_speakers(segs, diarize(a.input, a.num_speakers))
    who = lambda s: f"[Speaker {s['speaker']}] " if s.get("speaker") else ""
    base = a.out / a.input.stem
    base.with_suffix(".txt").write_text("\n".join(who(s) + s["text"] for s in segs) + "\n", encoding="utf-8")
    base.with_suffix(".srt").write_text("".join(
        f"{i}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n{who(s)}{s['text']}\n\n" for i, s in enumerate(segs, 1)), encoding="utf-8")
    base.with_suffix(".json").write_text(json.dumps({"language": info.language, "segments": segs}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"language={info.language}; wrote {base}.txt .srt .json")


def stems(a):
    cmd = [sys.executable, "-m", "demucs", "-n", "htdemucs", "-o", str(a.out)]
    if a.two:
        cmd += ["--two-stems", a.two]
    subprocess.run(cmd + (["--mp3"] if a.mp3 else []) + [str(a.input)], check=True)
    print(f"wrote {a.out / 'htdemucs' / a.input.stem}/")


def denoise(a):
    dest = a.out / f"{a.input.stem}_clean.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(a.input), "-vn", "-af", f"arnndn=m={MODELS / 'sh.rnnn'}", str(dest)], check=True)
    print(f"wrote {dest}")


def speakers(a):
    import numpy as np, soundfile as sf
    turns = diarize(a.input, a.num_speakers)
    sr = 44100
    audio = pcm(a.input, sr)
    for spk in sorted({t[2] for t in turns}):
        track = np.zeros_like(audio)
        for start, end, k in turns:
            if k == spk:
                track[int(start * sr):int(end * sr)] = audio[int(start * sr):int(end * sr)]
        sf.write(a.out / f"{a.input.stem}_speaker{spk + 1}.wav", track, sr)
    (a.out / f"{a.input.stem}_speakers.json").write_text(json.dumps(
        [{"start": round(s, 2), "end": round(e, 2), "speaker": k + 1} for s, e, k in turns], indent=1))
    print(f"{len({t[2] for t in turns})} speakers; wrote {a.out}/{a.input.stem}_speaker*.wav and _speakers.json")


def midi(a):
    from basic_pitch import FilenameSuffix, build_icassp_2022_model_path
    from basic_pitch.inference import predict
    with tempfile.TemporaryDirectory() as tmp:  # decode anything ffmpeg reads (mp3, m4a, video) to wav first
        wav = Path(tmp) / "in.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(a.input), "-vn", "-ac", "1", "-ar", "22050", str(wav)], check=True)
        _, mid, notes = predict(str(wav), build_icassp_2022_model_path(FilenameSuffix.onnx))
    dest = a.out / f"{a.input.stem}.mid"
    mid.write(str(dest))
    print(f"{len(notes)} notes; wrote {dest}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in [("transcribe", transcribe), ("stems", stems), ("denoise", denoise), ("speakers", speakers), ("midi", midi)]:
        s = sub.add_parser(name)
        s.add_argument("input")
        s.add_argument("--out", type=Path, default=Path("audio-out"))
        s.set_defaults(fn=fn)
        if name == "transcribe":
            s.add_argument("--lang", help="language code, e.g. he or en (default: detect)")
            s.add_argument("--model", help=f"faster-whisper model (default: turbo; {HEBREW_MODEL} for Hebrew)")
            s.add_argument("--speakers", action="store_true", help="label who speaks each line")
        if name in ("transcribe", "speakers"):
            s.add_argument("--num-speakers", type=int, help="exact speaker count, if known")
        if name == "stems":
            s.add_argument("--two", metavar="STEM", help="split into STEM and no_STEM only (vocals, drums, bass, other)")
            s.add_argument("--mp3", action="store_true")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.input.startswith(("http://", "https://")):
        dest = a.out / (Path(a.input.split("?")[0]).name or "input")
        subprocess.run(["curl", "-fsSL", "--retry", "3", "-o", str(dest), a.input], check=True)
        a.input = dest
    a.input = Path(a.input)
    if not a.input.is_file():
        sys.exit(f"not found: {a.input}")
    a.fn(a)


if __name__ == "__main__":
    if Path(sys.prefix).resolve() != HOME.resolve():  # not in the toolkit venv yet: install if needed, then re-run there
        if not (HOME / ".ready-1").exists():
            subprocess.run(["bash", str(Path(__file__).with_name("setup.sh"))], check=True)
        os.execv(HOME / "bin/python", [str(HOME / "bin/python"), __file__, *sys.argv[1:]])
    main()
