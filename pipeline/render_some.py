"""python3 ../../pipeline/render_some.py 2 9  -> renders scenes/mXX.mp4 for those scene indices (0-based)."""
import sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes as S
from epkit import render_scene_fast
os.makedirs("scenes", exist_ok=True)
for i in map(int, sys.argv[1:]):
    a, b = S.BOUNDS[i]; p = f"scenes/m{i+1:02d}.mp4"
    if os.path.exists(p): os.remove(p)
    render_scene_fast(S.SCENES[i], b - a, p); print("done", p, flush=True)
