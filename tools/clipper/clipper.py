#!/usr/bin/env python3
"""Stream clipper: Twitch clip -> vertical 1080x1920 short with captions and a hook.

Subcommands
  find  CHANNEL [--range 24h|7d|30d] [--limit N] [--keyword gta]
        List the most-viewed viewer clips (the strongest "people want this" signal).
  prep  CLIP_URL [--streamer NAME]
        Download the clip and transcribe it (word timestamps). Prints the transcript
        so a hook can be written for it.
  make  CLIP_URL --hook "TEXT" [--streamer NAME] [--style split|full] [--out FILE]
        Render the vertical clip: face cam on top, game below, word-by-word captions,
        hook across the seam.

Work files live in --work (default: ./clipper-work), one folder per clip.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FONT = "Inter Black"
ACCENT = "&H0040E07A&"  # ASS is BGR: a green (#7AE040)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def load_streamers():
    with open(os.path.join(HERE, "streamers.json")) as f:
        return json.load(f)


def clip_dir(work, url):
    slug = url.rstrip("/").split("/")[-1].split("?")[0]
    slug = re.sub(r"[^A-Za-z0-9_-]", "", slug)[:60] or hashlib.md5(url.encode()).hexdigest()[:12]
    d = os.path.join(work, slug)
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------- find
def cmd_find(a):
    url = f"https://www.twitch.tv/{a.channel}/clips?filter=clips&range={a.range}"
    out = run(["yt-dlp", "--flat-playlist", "-I", f"1:{a.limit * 3 if a.keyword else a.limit}",
               "--print", "%(url)s\t%(title)s\t%(view_count)s", url]).stdout
    rows = []
    for line in out.strip().splitlines():
        u, title, views = (line.split("\t") + ["", "", "0"])[:3]
        if a.keyword and a.keyword.lower() not in title.lower():
            continue
        rows.append({"url": u, "title": title, "views": int(views or 0)})
    rows = rows[: a.limit]
    print(json.dumps(rows, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- prep
def download(d, url):
    src = os.path.join(d, "source.mp4")
    if not os.path.exists(src):
        run(["yt-dlp", "-q", "-f", "best[height<=1080]", "-o", src, url])
    return src


def transcribe(d, src, model_size="small"):
    tj = os.path.join(d, "transcript.json")
    if os.path.exists(tj):
        with open(tj) as f:
            return json.load(f)
    import numpy as np
    from faster_whisper import WhisperModel
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, language="en", word_timestamps=True, vad_filter=True)
    words = []
    for s in segs:
        for w in s.words or []:
            t = w.word.strip()
            if t:
                words.append({"w": t, "s": round(w.start, 2), "e": round(w.end, 2)})
    with open(tj, "w") as f:
        json.dump(words, f)
    return words


def cmd_prep(a):
    d = clip_dir(a.work, a.url)
    src = download(d, a.url)
    words = transcribe(d, src, a.model)
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", src]).stdout.strip())
    print(json.dumps({"dir": d, "duration": round(dur, 1),
                      "transcript": " ".join(w["w"] for w in words)}, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- make
def ass_time(t):
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def esc(t):
    return t.replace("\\", "").replace("{", "(").replace("}", ")")


def build_ass(words, hook, duration, hook_y, cap_y):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{FONT},64,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,18,0,5,60,60,0,1
Style: Cap,{FONT},86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    hook_txt = "\\N".join(textwrap.wrap(esc(hook.upper()), 24))
    ev.append(f"Dialogue: 2,{ass_time(0)},{ass_time(duration)},Hook,,0,0,0,,{{\\pos({W // 2},{hook_y})}}{hook_txt}")

    # word-by-word captions in chunks of up to 3 words; the spoken word is highlighted
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or w["s"] - cur[-1]["e"] > 0.6):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    for ci, ch in enumerate(chunks):
        chunk_end = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else ch[-1]["e"] + 0.4
        chunk_end = min(chunk_end, ch[-1]["e"] + 0.6)
        for wi, w in enumerate(ch):
            start = w["s"]
            end = ch[wi + 1]["s"] if wi + 1 < len(ch) else chunk_end
            parts = []
            for k, x in enumerate(ch):
                t = esc(x["w"].upper())
                parts.append(f"{{\\c{ACCENT}\\fscx108\\fscy108}}{t}{{\\c&H00FFFFFF&\\fscx100\\fscy100}}" if k == wi else t)
            ev.append(f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{{\\pos({W // 2},{cap_y})}}{' '.join(parts)}")
    return head + "\n".join(ev) + "\n"


def cmd_make(a):
    d = clip_dir(a.work, a.url)
    src = download(d, a.url)
    words = transcribe(d, src, a.model)
    probe = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "json", src]).stdout)
    sw, sh = probe["streams"][0]["width"], probe["streams"][0]["height"]
    duration = min(float(probe["format"]["duration"]), a.max_len)
    sx, sy = sw / 1920, sh / 1080  # layouts are stored in 1920x1080 pixels

    cfg = load_streamers().get((a.streamer or "").lower(), {})
    cam = cfg.get("facecam")
    style = a.style or ("split" if cam else "full")

    if style == "split" and cam:
        fx, fy, fw, fh = (int(cam[0] * sx), int(cam[1] * sy), int(cam[2] * sx), int(cam[3] * sy))
        top_h = int(round(W * fh / fw / 2) * 2)
        bot_h = H - top_h
        gw = int(round(sh * W / bot_h / 2) * 2)
        gx = max(0, min(sw - gw, (sw - gw) // 2 + int(cfg.get("game_offset_x", 0) * sx)))
        vf = (f"[0:v]crop={fw}:{fh}:{fx}:{fy},scale={W}:{top_h},setsar=1[top];"
              f"[0:v]crop={gw}:{sh}:{gx}:0,scale={W}:{bot_h},setsar=1[bot];"
              f"[top][bot]vstack=inputs=2[v]")
        hook_y, cap_y = top_h, top_h + int(bot_h * 0.62)
    else:  # full frame centred on a blurred fill
        fg_h = int(round(W * sh / sw / 2) * 2)
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2,eq=brightness=-0.15[bg];"
              f"[0:v]scale={W}:{fg_h}[fg];[bg][fg]overlay=0:(H-h)/2[v]")
        hook_y, cap_y = (H - fg_h) // 2 - 120, (H + fg_h) // 2 + 170

    ass_path = os.path.join(d, "subs.ass")
    with open(ass_path, "w") as f:
        f.write(build_ass(words, a.hook, duration, hook_y, cap_y))

    out = a.out or os.path.join(d, "final.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", f"{duration:.2f}",
         "-filter_complex", vf + f";[v]ass={ass_path}[out]",
         "-map", "[out]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    print(json.dumps({"out": out, "style": style, "duration": round(duration, 1)}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--work", default=os.path.join(os.getcwd(), "clipper-work"))
    p.add_argument("--model", default="small", help="faster-whisper model size")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find")
    f.add_argument("channel")
    f.add_argument("--range", default="24h", choices=["24h", "7d", "30d", "all"])
    f.add_argument("--limit", type=int, default=10)
    f.add_argument("--keyword")

    pr = sub.add_parser("prep")
    pr.add_argument("url")

    m = sub.add_parser("make")
    m.add_argument("url")
    m.add_argument("--hook", required=True)
    m.add_argument("--streamer")
    m.add_argument("--style", choices=["split", "full"])
    m.add_argument("--max-len", type=float, default=60.0)
    m.add_argument("--out")

    a = p.parse_args()
    {"find": cmd_find, "prep": cmd_prep, "make": cmd_make}[a.cmd](a)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr or str(e))
        sys.exit(1)
