"""Run: python3 test_audio_tools.py (no venv or models needed)."""
from audio_tools import label_speakers, srt_time

assert srt_time(0) == "00:00:00,000"
assert srt_time(3661.5) == "01:01:01,500"
assert srt_time(59.9996) == "00:01:00,000"  # rounding carries into the next second

turns = [(0.0, 10.2, 0), (11.5, 18.7, 1), (18.7, 21.2, 0)]
segs = label_speakers([{"start": 0.2, "end": 9.9}, {"start": 11.0, "end": 18.0},
                       {"start": 18.0, "end": 21.0}, {"start": 30.0, "end": 31.0}], turns)
assert [s["speaker"] for s in segs] == [1, 2, 1, None], segs
print("ok")
