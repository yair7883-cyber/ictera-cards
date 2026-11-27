---
name: audio-local
description: Process audio locally in the container, with no account or API key - transcribe speech (Hebrew included) with speaker labels and SRT subtitles, split a song into stems (vocals, drums, bass, other), remove background noise, split a conversation into one track per speaker, convert a recording to MIDI, or convert formats. Use for any of these, and in place of AudioPod whenever AudioPod is not connected or has no valid key.
---

# Local audio tools

One script, `audio_tools.py` in this folder. Run it with plain `python3`. On first use it runs `setup.sh`: a Python 3.12 venv in `~/.local/share/audio-tools` plus models, each checked by SHA-256 (about 6 GB, a few minutes). Tell the user about that wait before the first run. Later runs start at once.

Input is a local file or an http(s) URL; anything ffmpeg reads works, video included. Pass `--out` to a folder the user can open (the working directory or the scratchpad); the default is `./audio-out`.

| Task | Command | Output |
|------|---------|--------|
| Transcribe | `python3 audio_tools.py transcribe IN [--lang he] [--speakers] [--num-speakers N]` | `.txt`, `.srt`, `.json` |
| Stems | `python3 audio_tools.py stems IN [--two vocals] [--mp3]` | `htdemucs/<name>/vocals.wav drums.wav bass.wav other.wav` |
| Remove noise | `python3 audio_tools.py denoise IN` | `<name>_clean.wav` |
| One track per speaker | `python3 audio_tools.py speakers IN [--num-speakers N]` | `<name>_speakerN.wav`, `<name>_speakers.json` |
| To MIDI | `python3 audio_tools.py midi IN` | `<name>.mid` |
| Convert format | `ffmpeg -i IN OUT.mp3` (or `.wav .flac .ogg .m4a`; `-vn` to drop video) | |

- **Transcribe:** Hebrew uses the ivrit-ai model, whether set with `--lang he` or detected. Other languages use Whisper large-v3 turbo. Pass `--num-speakers` when the count is known; the auto count can split one voice in two.
- **Speech over music or loud noise:** `stems IN --two vocals` isolates the voice better than `denoise`. `denoise` (RNNoise) is for steady background noise: hiss, hum, room tone, fans.
- **Speed on this CPU:** stems run at about real time, so a 4-minute song takes about 4 minutes. Transcription is faster than real time. Run long files in the background.
- Send results to the user with SendUserFile.

Tests: `python3 test_audio_tools.py`.
