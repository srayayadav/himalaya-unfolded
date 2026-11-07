"""Himalaya Unfolded video toolkit.

Usage in an episode folder:
    from hu import *          # (sys.path.insert(0, "../../pipeline"))
    lines = [...]              # narration, one sentence per line
    times = narrate(lines)     # -> voice.wav, times.json, list of (start, end)
    scenes = [(fn, start, end), ...]   # fn(t, d, W, H) -> SVG body string
    render_all(scenes, W=1920, H=1080, out="main.mp4")   # or W=1080, H=1920 for a Short

Every scene function draws ONE frame as an SVG body; helpers below keep the brand look.
"""
import json, math, os, re, subprocess, random

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
    s = re.sub(r"&(?![a-zA-Z]+;|#\d+;)", "&amp;", str(s)).replace("<", "&lt;")
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

def make_short(main, start, end, title, title2="", footer="Full story on the channel", out="short.mp4"):
    """Clip [start, end] seconds of a 16:9 main video into a 9:16 Short (max 60 s):
    blurred copy fills the frame, the clip sits in the middle, title on top, footer at the bottom."""
    W, H = 1080, 1920
    assert end - start <= 60, "Shorts must be 60 s or less"
    over = f'<rect x="60" y="250" width="960" height="{300 if title2 else 190}" rx="28" fill="#06142B" opacity="0.82" stroke="{GOLD}" stroke-opacity="0.4" stroke-width="3"/>'
    over += text(540, 375, title, 76, WHITE, 900)
    if title2: over += text(540, 485, title2, 76, GOLD, 900)
    over += f'<rect x="140" y="1480" width="800" height="110" rx="55" fill="#06142B" opacity="0.82"/>' + text(540, 1552, footer, 42, CREAM, 700)
    over += text(540, 1720, "HIMALAYA UNFOLDED", 40, GOLD, 800, ls=8)
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{defs()}{over}</svg>'
    open("_short_overlay.svg", "w").write(s)
    subprocess.run(["rsvg-convert", "_short_overlay.svg", "-o", "_short_overlay.png"], check=True)
    d = end - start
    fc = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=30:2,eq=brightness=-0.12[bg];"
          f"[b]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[v1];[v1][1:v]overlay=0:0,"
          f"fade=t=in:d=0.3,fade=t=out:st={d-0.5:.2f}:d=0.5[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", f"{d:.2f}", "-i", main, "-i", "_short_overlay.png",
                    "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-af", f"afade=t=out:st={d-0.6:.2f}:d=0.6",
                    "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", out], check=True)
    return out

# ---------- "documentary feel" finishing ----------
def ambient_bed(duration, cuts=(), out="bed.wav", seed=5):
    """Original, royalty-free sound bed made from scratch: a warm drone, soft singing-bowl strikes,
    and a gentle whoosh at every scene cut. Nothing sampled, so no copyright issues."""
    import numpy as np, soundfile as sf
    sr = 44100; n = int(duration * sr); t = np.arange(n) / sr; r = np.random.default_rng(seed)
    bed = np.zeros(n)
    for f, a in [(55, .5), (82.4, .35), (110, .3), (164.8, .15), (220, .08)]:   # A / E drone
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.03 + r.random() * 0.04) * t + r.random() * 6)
        bed += a * lfo * np.sin(2 * np.pi * f * t + r.random() * 6)
    bed *= 0.10
    bowl_f = 392.0; parts = [(1, 1), (2.71, .5), (5.12, .25), (8.3, .1)]
    for st in np.arange(4.0, duration - 6, 13.0):                                 # singing bowl strikes
        i0 = int(st * sr); m = min(n - i0, int(9 * sr)); tt = np.arange(m) / sr
        hit = sum(a * np.sin(2 * np.pi * bowl_f * k * tt) * np.exp(-tt * (0.6 + k * 0.35)) for k, a in parts)
        bed[i0:i0 + m] += 0.05 * hit * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * tt))
    for c in cuts:                                                                 # whoosh at cuts
        i0 = int(max(0, c - 0.35) * sr); m = min(n - i0, int(0.9 * sr))
        if m <= 0: continue
        noise = r.standard_normal(m); k = np.ones(40) / 40; noise = np.convolve(noise, k, "same")
        env = np.sin(np.pi * np.arange(m) / m) ** 2
        bed[i0:i0 + m] += 0.12 * noise * env
    fade = np.minimum(1, np.minimum(t / 3, (duration - t) / 3)); bed *= fade
    sf.write(out, np.stack([bed, bed * 0.97], 1).astype("float32"), sr)
    return out

def finish(scene_files, voice, out, bed_db=-17, srt_lines=None, srt_times=None):
    """Turn rendered scene files into a less 'synthetic-looking' film:
    slow camera drift on every scene (alternating push-in and pan), film grain, soft vignette,
    an original ambient sound bed under the narration, and an .srt caption file."""
    os.makedirs("finished", exist_ok=True); done = []; cuts = []; t = 0
    for i, f in enumerate(scene_files):
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
        n = max(1, round(d * FPS)); dx = (1 if i % 2 else -1) * 30
        z = f"1.0+0.045*on/{n}" if i % 3 != 2 else f"1.045-0.045*on/{n}"
        vf = (f"scale=2112:1188,zoompan=z='{z}':x='iw/2-(iw/zoom/2)+{dx}*on/{n}':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS},"
              f"noise=alls=7:allf=t+u,vignette=angle=PI/5")
        p = f"finished/{os.path.basename(f)}"; tmp = p[:-4] + ".tmp.mp4"
        if not os.path.exists(p):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-vf", vf, "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], check=True)
            os.replace(tmp, p)
        done.append(p); t += d; cuts.append(t)
    open("finished/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in done))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "finished/list.txt", "-c", "copy", "finished/video.mp4"], check=True)
    ambient_bed(t, cuts[:-1], "finished/bed.wav")
    af = f"[2:a]volume={bed_db}dB[b];[1:a]aresample=44100,apad[v];[v][b]amix=inputs=2:duration=longest:normalize=0[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "finished/video.mp4", "-i", voice, "-i", "finished/bed.wav",
                    "-filter_complex", af, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
    if srt_lines and srt_times:
        def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x*1000%1000):03d}"
        open(out[:-4] + ".srt", "w").write("".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{line}\n\n" for i, (line, (a, b)) in enumerate(zip(srt_lines, srt_times))))
    return out

# ---------- real maps (Natural Earth 1:50m, public domain) ----------
_GEO = None
def countries():
    """{ADMIN name: [ring, ...]} from Natural Earth admin-0 (data/ne_50m_countries.geojson).
    Borders are Natural Earth's de-facto lines; tell the owner before showing any disputed area."""
    global _GEO
    if _GEO is None:
        p = os.path.join(HERE, "data", "ne_50m_countries.geojson")
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            subprocess.run(["curl", "-sSL", "-o", p, "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"], check=True)
        _GEO = {}
        for f in json.load(open(p))["features"]:
            g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            _GEO[f["properties"]["ADMIN"]] = [ring for poly_ in polys for ring in poly_[:1]]
    return _GEO

def projector(lon0, lat0, lon1, lat1, x0, y0, x1, y1):
    """Equirectangular projection of a lon/lat box onto a pixel box, keeping the shape true at mid-latitude."""
    k = math.cos(math.radians((lat0 + lat1) / 2))
    sx = (x1 - x0) / ((lon1 - lon0) * k); sy = (y1 - y0) / (lat1 - lat0); s = min(sx, sy)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; mlon, mlat = (lon0 + lon1) / 2, (lat0 + lat1) / 2
    return lambda lon, lat: (cx + (lon - mlon) * k * s, cy - (lat - mlat) * s)

def country_path(name, proj, fill, op=1, stroke="#0A1A2C", sw=2, extra=""):
    d = ""
    for ring in countries()[name]:
        d += "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (proj(lo, la) for lo, la in ring)) + "Z"
    return f'<path d="{d}" fill="{fill}" opacity="{op:.3f}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'

def contact_sheet(paths, out, cols=2, w=640):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = int(ims[0].height * w / ims[0].width); rows = (len(ims) + cols - 1) // cols
    g = Image.new("RGB", (cols * w, rows * h))
    for i, im in enumerate(ims): g.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    g.save(out)
