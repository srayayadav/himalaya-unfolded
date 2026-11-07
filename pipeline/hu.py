"""Himalaya Unfolded video toolkit.

Usage in an episode folder:
    from hu import *          # (sys.path.insert(0, "../../pipeline"))
    lines = [...]              # narration, one sentence per line
    times = narrate(lines)     # -> voice.wav, times.json, list of (start, end)
    scenes = [(fn, start, end), ...]   # fn(t, d, W, H) -> SVG body string
    render_all(scenes, W=1920, H=1080, out="main.mp4")   # or W=1080, H=1920 for a Short

Every scene function draws ONE frame as an SVG body; helpers below keep the brand look.
"""
import json, math, os, subprocess, random

FPS = 30
GOLD, CREAM, WHITE, SNOW = "#FFD98A", "#F3DCC0", "#FFFFFF", "#F7F4EF"
FLAG = ["#2F6FD6", "#F4F1E8", "#D9343A", "#2E9E5B", "#F2C230"]
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "models")

# ---------- voice ----------
def ensure_models():
    os.makedirs(MODELS, exist_ok=True)
    base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
    for f, name in [("kokoro.onnx", "kokoro-v1.0.onnx"), ("voices.bin", "voices-v1.0.bin")]:
        p = os.path.join(MODELS, f)
        if not os.path.exists(p):
            subprocess.run(["curl", "-sSL", "-o", p, base + name], check=True)

def narrate(lines, voice="bm_george", speed=1.0, gap=0.45, out="voice.wav"):
    """Kokoro TTS (Apache-2.0, free for commercial use). Returns [(start, end)] per line."""
    ensure_models()
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELS, "kokoro.onnx"), os.path.join(MODELS, "voices.bin"))
    chunks, times, t, sr = [], [], 0.0, 24000
    for line in lines:
        a, sr = k.create(line, voice=voice, speed=speed, lang="en-gb")
        times.append((round(t, 2), round(t + len(a) / sr, 2)))
        pad = np.zeros(int(sr * gap), dtype=a.dtype)
        chunks += [a, pad]; t += (len(a) + len(pad)) / sr
    sf.write(out, np.concatenate(chunks), sr)
    json.dump(times, open("times.json", "w"))
    return times

# ---------- drawing ----------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, a, b): return ease((t - a) / (b - a))

def defs():
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06142B"/><stop offset="0.45" stop-color="#0F3550"/><stop offset="0.7" stop-color="#2F6A7A"/><stop offset="0.86" stop-color="#E7A26A"/><stop offset="1" stop-color="#F6C97A"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06142B"/><stop offset="1" stop-color="#123049"/></linearGradient>
<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E2236"/><stop offset="1" stop-color="#050B16"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.6"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<filter id="ts" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#04101F" flood-opacity="0.7"/></filter>
</defs>'''

def svg(body, W, H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}{body}</svg>'

def bg(W, H, kind="night", stars=40, seed=1):
    r = random.Random(seed)
    s = f'<rect width="{W}" height="{H}" fill="url(#{kind})"/>'
    s += "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H*0.45):.0f}" r="{r.uniform(1,2.5):.1f}" fill="#fff" opacity="{r.uniform(.3,.8):.2f}"/>' for _ in range(stars))
    return s

def text(x, y, s, size, fill=WHITE, weight=700, anchor="middle", op=1, ls=0, shadow=True):
    f = ' filter="url(#ts)"' if shadow else ""
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="Inter" font-weight="{weight}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" opacity="{op:.3f}"{f}>{s}</text>'

def poly(pts, fill, op=1):
    return '<path d="M' + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f'Z" fill="{fill}" opacity="{op}"/>'

def peak(cx, top, base_y, wl, wr, lit="#2D5873", shade="#163448", snow=0.25, seed=0):
    """Two-tone mountain with a jagged snow cap (the channel's signature shape)."""
    r = random.Random(seed or int(cx + top))
    L, R, P, mid = (cx - wl, base_y), (cx + wr, base_y), (cx, top), (cx + wr * 0.12, base_y)
    s = poly([L, P, mid], lit) + poly([P, R, mid], shade)
    h = (base_y - top) * snow; lx, rx, y = cx - wl * snow, cx + wr * snow, top + h
    pts = [P, (rx, y)]
    for i in range(1, 6):
        pts.append((rx - (rx - lx) * i / 6, y + (r.uniform(10, h * 0.45) if i % 2 else r.uniform(-6, 8))))
    pts.append((lx, y))
    return s + poly(pts, SNOW) + poly([P, (rx, y), (cx + wr * 0.03, y + h * 0.25)], "#C9CFE6", 0.85)

def flags(x0, y0, x1, y1, sag, size, count, seed=2):
    r = random.Random(seed); my = max(y0, y1) + sag
    s = f'<path d="M{x0} {y0} Q{(x0+x1)/2} {my} {x1} {y1}" stroke="#E8D9C0" stroke-width="{max(1.5,size/14):.1f}" fill="none" opacity="0.8"/>'
    for i in range(count):
        t = (i + 0.5) / count
        x = (1-t)**2*x0 + 2*(1-t)*t*(x0+x1)/2 + t*t*x1; y = (1-t)**2*y0 + 2*(1-t)*t*my + t*t*y1
        w, sk = size * 0.8, r.uniform(-0.15, 0.15) * size
        s += poly([(x-w/2, y), (x+w/2, y), (x+w/2+sk, y+size), (x-w/2+sk, y+size)], FLAG[i % 5], 0.95)
    return s

def card(x, y, w, h, op=1, fill="#0B1E33"):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="22" fill="{fill}" opacity="{0.82*op:.3f}" stroke="{GOLD}" stroke-opacity="{0.35*op:.3f}" stroke-width="2"/>'

def caption(s, W, H, op=1):
    """Big lower-third caption, readable on phones."""
    return card(W*0.08, H*0.80, W*0.84, H*0.11, op) + text(W/2, H*0.80 + H*0.075, s, int(min(W, H)*0.05), WHITE, 700, op=op)

def fade(body, t, d, W, H, fin=0.3, fout=0.3):
    o = min(clamp(t / fin) if fin else 1, clamp((d - t) / fout) if fout else 1)
    return body + f'<rect width="{W}" height="{H}" fill="#050B16" opacity="{1 - o:.3f}"/>'

# ---------- rendering ----------
def frame_png(body, W, H):
    return subprocess.run(["rsvg-convert", "-f", "png"], input=svg(body, W, H).encode(), capture_output=True, check=True).stdout

def preview(fn, t, d, W, H, path):
    open(path, "wb").write(frame_png(fn(t, d, W, H), W, H))

def render_scene(fn, d, W, H, path):
    n = round(d * FPS); tmp = path[:-4] + ".tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
        "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(frame_png(fn(f / FPS, d, W, H), W, H))
    ff.stdin.close()
    if ff.wait() == 0: os.replace(tmp, path)

def render_all(scenes, W, H, out, audio="voice.wav", music=None, music_vol=0.12, tag="m"):
    """scenes: list of (fn, start, end). Renders each scene file, joins, adds narration (+ optional music)."""
    os.makedirs("scenes", exist_ok=True)
    files = []
    for i, (fn, a, b) in enumerate(scenes):
        p = f"scenes/{tag}{i+1:02d}.mp4"
        if not os.path.exists(p): render_scene(fn, b - a, W, H, p)
        files.append(p); print("scene", i + 1, "done", flush=True)
    open(f"{tag}_list.txt", "w").write("".join(f"file '{p}'\n" for p in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{tag}_list.txt", "-c", "copy", f"{tag}_video.mp4"], check=True)
    if music:
        af = f"[2:a]volume={music_vol},afade=t=in:d=2[m];[1:a][m]amix=inputs=2:duration=first,apad[a]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tag}_video.mp4", "-i", audio, "-stream_loop", "-1", "-i", music,
               "-filter_complex", af, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tag}_video.mp4", "-i", audio, "-map", "0:v", "-map", "1:a",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out]
    subprocess.run(cmd, check=True)
    return out

def contact_sheet(paths, out, cols=2, w=640):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = int(ims[0].height * w / ims[0].width); rows = (len(ims) + cols - 1) // cols
    g = Image.new("RGB", (cols * w, rows * h))
    for i, im in enumerate(ims): g.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    g.save(out)
