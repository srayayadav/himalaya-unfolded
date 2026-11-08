"""Shared helpers for painted-documentary episodes (from ep 003 on).
In an episode folder:  from epkit import *   then define scene functions and SCENES = [fn, ...] (one per beat),
and end the file with  main(SCENES, "slug").
Commands:  python3 scenes.py preview [i ...]   -> pp_XX.png + pp_sheet.png (busiest moment of each scene)
           python3 scenes.py render            -> scenes/mXX.mp4 (2 workers) + finish() -> <slug>_main.mp4 + .srt
"""
import sys, os, json, math, random, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hu import *
from characters import *
from style2 import TEXTURE_DEFS, smoke, stone_fort, lower_third, clouds
from painted import bg_image, WARM_DEFS, grass, ground_shadow

DEFS = TEXTURE_DEFS.replace("<defs>", "<defs>" + WARM_DEFS)
BEATS = json.load(open("beats.json"))
END = BEATS[-1][1] + 3.0
STARTS = [b[0] for b in BEATS]
BOUNDS = list(zip(STARTS, STARTS[1:] + [END]))

def L(i, k):
    """Local start time (s) of line k of beat i, relative to the beat's start."""
    return BEATS[i][2][k][0] - STARTS[i]

def LE(i, k):
    return BEATS[i][2][k][1] - STARTS[i]

def speaking(t, i, k0, k1=None):
    """True while lines k0..k1 of beat i are being narrated (for talking mouths)."""
    k1 = k0 if k1 is None else k1
    return L(i, k0) <= t <= LE(i, k1)

FAST = {"on": False}

def _paint_path(name):
    for p in (f"bg/{name}.jpg", f"../sample-painted/{name}.jpg"):
        if os.path.exists(p): return p

@functools.lru_cache(None)
def PAINT(name, op=1.0):
    if FAST["on"] and op == 1.0 and _paint_path(name):
        return f"<!--BG:{name}-->"
    for p in (f"bg/{name}.jpg", f"../sample-painted/{name}.jpg"):
        if os.path.exists(p): return bg_image(p, 1920, 1080, op)
    # placeholder until the painting exists (only used for previews)
    return '<rect width="1920" height="1080" fill="url(#dusk)"/>' + text(960, 540, f"[{name}]", 40, WHITE, 400, op=0.4)

def shade(op=0.45, top=True, uid=""):
    a, b = ("0", "0.5") if top else ("0.5", "1")
    o1, o2 = (op, 0) if top else (0, op)
    g = f"sh{int(top)}{uid}"
    return (f'<linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="{a}" stop-color="#06142B" stop-opacity="{o1}"/>'
            f'<stop offset="{b}" stop-color="#06142B" stop-opacity="{o2}"/></linearGradient><rect width="1920" height="1080" fill="url(#{g})"/>')

def dim(op):
    return f'<rect width="1920" height="1080" fill="#06142B" opacity="{op:.3f}"/>'

def label(x, y, name, op=1, w=440, size=30):
    return card(x - w/2, y, w, 58, op) + text(x, y + 40, name, size, WHITE, 700, op=op)

def walk_x(t, start, x0, x1, dur=2.0):
    return x0 + (x1 - x0) * prog(t, start, start + dur)

def bob(t, walking, amp=6):
    return -abs(math.sin(t * 7)) * amp if walking else 0

def inout(t, a, b, fi=0.6, fo=0.5):
    """Opacity that fades in at a and out at b (local seconds)."""
    return prog(t, a, a + fi) * (1 - prog(t, b, b + fo))

def chip(x, y, s, op=1, size=40, col=CREAM, w=None):
    w = w or max(160, len(s) * size * 0.58 + 60)
    return card(x - w/2, y - size*1.25, w, size*1.9, op) + text(x, y + size*0.1, s, size, col, 800, op=op)

def counter_text(x, y, val, label_, op, size=120, col=GOLD, lsize=36):
    return text(x, y, val, size, col, 900, op=op) + text(x, y + 30 + lsize, label_, lsize, CREAM, 600, op=op)

def countup(t, a, b, n, fmt="{:,.0f}"):
    return fmt.format(n * prog(t, a, b))

def medal(x, y, s=1.0, op=1, ribbon="#7A1F2B", metal="#C9A04A", cross=True):
    """Generic bravery medal (stylised, not a copy of any real design)."""
    r = 44 * s
    g = (f'<g opacity="{op:.2f}" transform="translate({x:.0f} {y:.0f})">'
         f'<path d="M{-30*s:.0f} {-130*s:.0f} L{30*s:.0f} {-130*s:.0f} L{22*s:.0f} {-44*s:.0f} L{-22*s:.0f} {-44*s:.0f}Z" fill="{ribbon}"/>'
         f'<circle r="{r:.0f}" fill="{metal}" stroke="#7A5A1A" stroke-width="{4*s:.1f}"/>')
    if cross:
        k = r * 0.62
        g += f'<path d="M0 {-k:.0f} L{k*0.3:.0f} {-k*0.3:.0f} L{k:.0f} 0 L{k*0.3:.0f} {k*0.3:.0f} L0 {k:.0f} L{-k*0.3:.0f} {k*0.3:.0f} L{-k:.0f} 0 L{-k*0.3:.0f} {-k*0.3:.0f}Z" fill="#8C6A24"/>'
    return g + '</g>'

def warm(s):
    return f'<g filter="url(#warm)">{s}</g>'

def crossfade(t, at, dur, a_body, b_body):
    o = prog(t, at, at + dur)
    return a_body + f'<g opacity="{o:.3f}">{b_body}</g>'

# ---------- running ----------
def render_scene_fast(fn, d, path):
    """Faster render: the painting is composited by ffmpeg under a transparent rsvg overlay
    (PNG-encoding a full painting every frame was the slow part). Scenes whose painting changes
    mid-scene (crossfades) fall back to the normal renderer."""
    import re, subprocess
    FAST["on"] = True; PAINT.cache_clear()
    n = round(d * FPS)
    names = set()
    for k in (0, n // 2, n - 1):
        names |= set(re.findall(r"<!--BG:(\w+)-->", fn(k / FPS, d, 1920, 1080)))
    if len(names) != 1:
        FAST["on"] = False; PAINT.cache_clear()
        return render_scene(fn, d, 1920, 1080, path)
    bgp = _paint_path(names.pop()); tmp = path[:-4] + ".tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", bgp,
        "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
        "-filter_complex", "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgba[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
        "-map", "[v]", "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(frame_png(fn(f / FPS, d, 1920, 1080), 1920, 1080))
    ff.stdin.close()
    if ff.wait() == 0: os.replace(tmp, path)
    FAST["on"] = False; PAINT.cache_clear()

def _render_one(args):
    fn_name, i, a, b, mod = args
    import importlib
    m = importlib.import_module(mod)
    fn = m.SCENES[i]
    p = f"scenes/m{i+1:02d}.mp4"
    if not os.path.exists(p):
        render_scene_fast(fn, b - a, p)
    return p

def busiest(i):
    """A good preview time for scene i: a bit after its last line starts."""
    a, b = BOUNDS[i]
    return min(b - a - 0.8, max(BEATS[i][2][-1][0] - a + 1.2, 2.5))

def main(SCENES, slug, mod="scenes"):
    assert len(SCENES) == len(BEATS), (len(SCENES), len(BEATS))
    cmd = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if cmd == "preview":
        idx = [int(x) for x in sys.argv[2:]] or range(len(SCENES))
        paths = []
        for i in idx:
            a, b = BOUNDS[i]
            for j, ft in enumerate([busiest(i)] if len(sys.argv) <= 2 else [busiest(i), (b - a) * 0.35]):
                p = f"pp_{i:02d}_{j}.png"; preview(SCENES[i], ft, b - a, 1920, 1080, p); paths.append(p)
        contact_sheet(paths, "pp_sheet.png", cols=3, w=640)
        print("pp_sheet.png", len(paths))
    elif cmd == "frame":   # python3 scenes.py frame i t
        i, ft = int(sys.argv[2]), float(sys.argv[3]); a, b = BOUNDS[i]
        preview(SCENES[i], ft, b - a, 1920, 1080, f"pp_f{i:02d}.png"); print(f"pp_f{i:02d}.png")
    elif cmd == "render":
        from multiprocessing import Pool
        os.makedirs("scenes", exist_ok=True)
        jobs = sorted(((None, i, a, b, mod) for i, (a, b) in enumerate(BOUNDS)), key=lambda j: -(j[3] - j[2]))
        with Pool(int(os.environ.get("WORKERS", 2))) as pool:
            for p in pool.imap_unordered(_render_one, jobs): print("done", p, flush=True)
        sys.path.insert(0, os.getcwd())
        from script import BEATS as SB
        lines = [l for bt in SB for l in bt]; times = json.load(open("times.json"))
        files = [f"scenes/m{i+1:02d}.mp4" for i in range(len(SCENES))]
        finish(files, "voice.wav", f"{slug}_main.mp4", srt_lines=lines, srt_times=times)
        print("FINISHED", f"{slug}_main.mp4", flush=True)
