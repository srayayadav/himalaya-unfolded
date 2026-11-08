"""Narrate script.py BEATS -> voice.wav, times.json, beats.json [(start,end,[(a,b)...]) per beat]."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
from hu import narrate
from script import BEATS
lines = [l for b in BEATS for l in b]
times = narrate(lines)
out, i = [], 0
for b in BEATS:
    ts = times[i:i + len(b)]; i += len(b)
    out.append([ts[0][0], ts[-1][1], ts])
json.dump(out, open("beats.json", "w"))
print("total", times[-1][1])
