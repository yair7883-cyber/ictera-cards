#!/usr/bin/env python3
"""Open-source replacement for vidIQ's "watch short-form content".

Give it a TikTok / Instagram / YouTube link (or a local video file) and it:
  1. downloads the video and its metadata with yt-dlp,
  2. extracts timestamped frames with ffmpeg and tiles them into contact sheets,
  3. transcribes the speech with faster-whisper (Hebrew-tuned ivrit-ai model by default),
  4. writes report.md with the caption, stats, timed transcript and frame list.

Usage:
  python3 tools/watch_video.py URL_OR_FILE [-o OUT_DIR] [--every 2.5] [--lang he]
                               [--model ivrit-ai/whisper-large-v3-turbo-ct2] [--no-transcript]

Requires: pip install yt-dlp faster-whisper ; ffmpeg on PATH.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_MODEL = "ivrit-ai/whisper-large-v3-turbo-ct2"


def run(cmd):
    subprocess.run(cmd, check=True)


def download(url, out):
    run(["yt-dlp", "--no-progress", "--no-playlist", "--write-info-json",
         "-f", "best[ext=mp4]/best", "-o", str(out / "video.%(ext)s"), url])
    video = next(p for p in out.glob("video.*") if p.suffix != ".json")
    info_path = out / "video.info.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {}
    return video, info


def extract_frames(video, out, every):
    frames = out / "frames"
    frames.mkdir(exist_ok=True)
    stamp = "drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-vf", f"fps=1/{every},scale=360:-2,{stamp}", str(frames / "f_%03d.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-pattern_type", "glob", "-i", str(frames / "f_*.jpg"),
         "-vf", "tile=3x3:padding=4", str(out / "sheet_%02d.jpg")])
    return sorted(frames.glob("f_*.jpg")), sorted(out.glob("sheet_*.jpg"))


def transcribe(video, model_name, lang):
    import numpy as np
    from faster_whisper import WhisperModel
    # Decode with the ffmpeg CLI (16 kHz mono float32) so we don't depend on PyAV's version.
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "f32le",
                          "-ac", "1", "-ar", "16000", "-"], check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, language=lang, vad_filter=True, beam_size=5)
    return [(s.start, s.end, s.text.strip()) for s in segments], info.language


def ts(sec):
    return f"{int(sec // 60):02d}:{sec % 60:04.1f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="video URL or local file")
    ap.add_argument("-o", "--out", default="watch_out", help="output directory")
    ap.add_argument("--every", type=float, default=2.5, help="seconds between frames")
    ap.add_argument("--lang", default="he", help="speech language (e.g. he, en); 'auto' to detect")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="faster-whisper model name or path")
    ap.add_argument("--no-transcript", action="store_true")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if Path(a.source).is_file():
        video, info = Path(a.source), {}
    else:
        video, info = download(a.source, out)

    frames, sheets = extract_frames(video, out, a.every)
    segs, lang = ([], None) if a.no_transcript else transcribe(
        video, a.model, None if a.lang == "auto" else a.lang)

    md = [f"# {info.get('channel') or info.get('uploader') or video.name}", ""]
    fields = [("Link", "webpage_url"), ("Creator", "uploader"), ("Uploaded", "upload_date"),
              ("Duration (s)", "duration"), ("Views", "view_count"), ("Likes", "like_count"),
              ("Comments", "comment_count"), ("Shares", "repost_count"), ("Sound", "track")]
    md += [f"- **{label}:** {info[k]}" for label, k in fields if info.get(k) is not None]
    if info.get("description"):
        md += ["", "## Caption", "", info["description"]]
    if segs:
        md += ["", f"## Transcript ({lang})", ""]
        md += [f"- `{ts(s)}–{ts(e)}` {t}" for s, e, t in segs]
    md += ["", "## Frames", "", f"{len(frames)} frames, one every {a.every}s, in `frames/`.",
           "Contact sheets (3x3, timestamped): " + ", ".join(f"`{p.name}`" for p in sheets)]
    (out / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Done: {out / 'report.md'}")


if __name__ == "__main__":
    sys.exit(main())
