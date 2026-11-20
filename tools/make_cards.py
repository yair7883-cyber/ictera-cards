"""Build one or many ICTera cards in a single call ("code mode" for the card pipeline).

Instead of several separate steps per card (write the spec JSON, write the caption TXT,
run build_card_hq.py, check the PNG), pass everything at once:

    python3 -I tools/make_cards.py batch.json [--out cards]

batch.json is a list (or a single object) of:
    {
      "date": "20261121",              # -> cards/ictera-card-20261121.{json,txt,png}
      "sentence": ["line 1", "line 2"],
      "explain":  ["l1", "l2", "l3"],
      "caption":  "full post text",    # written to the .txt
      "style": "A"                     # optional, "A" = no candle backdrop
    }

Rendering is delegated to build_card_hq.py unchanged, so output is pixel-identical to
building each card by hand. Every card is validated and built before the next one starts;
a bad card is reported and the rest still run. Exit code is 1 if any card failed.
"""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
BUILDER = HERE / "build_card_hq.py"
LOGO = HERE / "logo.png"


def validate(item):
    if not re.fullmatch(r"\d{8}(-[\w-]+)?", str(item.get("date", ""))):
        raise ValueError("date must look like 20261121 (optionally -suffix)")
    for key, n in (("sentence", 2), ("explain", 3)):
        v = item.get(key)
        if not (isinstance(v, list) and len(v) == n and all(isinstance(x, str) and x.strip() for x in v)):
            raise ValueError(f"{key} must be a list of {n} non-empty strings")
    if not str(item.get("caption", "")).strip():
        raise ValueError("caption is required")


def build(item, out_dir):
    validate(item)
    stem = out_dir / f"ictera-card-{item['date']}"
    spec = {"sentence": item["sentence"], "explain": item["explain"]}
    if item.get("style"):
        spec["style"] = item["style"]
    stem.with_suffix(".json").write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    stem.with_suffix(".txt").write_text(item["caption"].rstrip() + "\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-I", str(BUILDER), str(LOGO), str(stem.with_suffix(".json")), str(stem.with_suffix(".png"))],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip())
    return r.stdout.strip()


def main():
    args = sys.argv[1:]
    out_dir = ROOT / "cards"
    if "--out" in args:
        i = args.index("--out")
        out_dir = pathlib.Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    items = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = [items]
    out_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for item in items:
        name = item.get("date", "?") if isinstance(item, dict) else "?"
        try:
            print(f"OK   {name}: {build(item, out_dir)}")
        except Exception as e:  # report and continue with the remaining cards
            failed += 1
            print(f"FAIL {name}: {e}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
