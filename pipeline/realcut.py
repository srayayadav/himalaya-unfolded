"""Realistic documentary cut (Santosh, 9 Nov 2026: "realistic like The Blueprint", free tools).
Photoreal stills (Ken Burns) + AI motion clips, cuts on narration lines, flash/fade transitions,
bold word-group captions burned in (like the reference channel), film grain, vignette, ambient bed.

    from realcut import Shot, build
    shots = [Shot("kaggle/h1.jpg", 0.0), Shot("kaggle/h2_wan.mp4", 5.06, move="clip"), ...]
    build(shots, lines, times, "voice.wav", "out.mp4", titles=[(24.3, 27.9, "THE GURKHAS")],
          labels=[(28.3, 32.7, "GORKHA, NEPAL")])

A Shot starts at a narration time and lasts until the next shot starts (the last one until end).
move: "in", "out", "left", "right", "up" for stills; "clip" for a video file.
"""
import os, subprocess, json, math, shutil
from dataclasses import dataclass

W, H, FPS, T = 1920, 1080, 30, 0.45      # T = transition length (s)

@dataclass
class Shot:
    src: str
    start: float
    move: str = "in"
    flash: bool = False          # light flash into this shot instead of a plain fade

def _run(cmd):
    subprocess.run(cmd, check=True)

def _dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)

def _still(src, d, move, out):
    n = max(2, round(d * FPS))
    z = {"in": ("1.0+0.10*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
         "out": ("1.10-0.10*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
         "left": ("1.08", "(iw-iw/zoom)*(1-on/{n})", "ih/2-ih/zoom/2"),
         "right": ("1.08", "(iw-iw/zoom)*on/{n}", "ih/2-ih/zoom/2"),
         "up": ("1.08", "iw/2-iw/zoom/2", "(ih-ih/zoom)*(1-on/{n})")}[move]
    zz, xx, yy = (s.format(n=n) for s in z)
    _run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf",
          f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
          f"zoompan=z='{zz}':x='{xx}':y='{yy}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
          "-frames:v", str(n), "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out])

def _clip(src, d, out):
    """Fit a generated clip to the shot: slow it down (with motion interpolation) or trim it."""
    cd = _dur(src)
    k = max(1.0, d / cd)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setpts={k:.4f}*PTS,"
          f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,format=yuv420p")
    _run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-t", f"{d:.3f}", "-an",
          "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out])

def _frames_clip(folder, d, out):
    """A folder of frames (e.g. SVD output): play forward then backward, stretched to d."""
    fr = sorted(f for f in os.listdir(folder) if f.endswith(".jpg"))
    seq = fr + fr[-2:0:-1]
    tmp = out + "_seq"; os.makedirs(tmp, exist_ok=True)
    for i, f in enumerate(seq): shutil.copy(os.path.join(folder, f), f"{tmp}/{i:03d}.jpg")
    _run(["ffmpeg", "-v", "error", "-y", "-framerate", f"{len(seq)/d:.4f}", "-i", f"{tmp}/%03d.jpg", "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,format=yuv420p",
          "-t", f"{d:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out])
    shutil.rmtree(tmp)

def _ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def captions_ass(lines, times, path, titles=(), labels=(), words=3):
    """Bold yellow word-group captions (3 words at a time), big titles and place labels."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display,84,&H004DE1FF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,2,80,80,110,1
Style: Title,Inter Display,150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,6,0,1,8,4,5,80,80,0,1
Style: Label,Inter Display,46,&H008AD9FF,&H00FFFFFF,&H00101010,&H96000000,-1,0,0,0,100,100,3,0,3,10,0,7,70,70,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for line, (a, b) in zip(lines, times):
        ws = line.replace("’", "'").split()
        groups = [" ".join(ws[i:i + words]) for i in range(0, len(ws), words)]
        tot = sum(len(g) + 2 for g in groups); t = a
        for g in groups:
            dt = (b - a) * (len(g) + 2) / tot
            ev.append(f"Dialogue: 0,{_ass_time(t)},{_ass_time(t + dt)},Cap,,0,0,0,,{{\\fad(60,0)}}{g.upper()}")
            t += dt
    for a, b, s in titles:
        ev.append(f"Dialogue: 1,{_ass_time(a)},{_ass_time(b)},Title,,0,0,0,,{{\\fad(300,300)}}{s}")
    for a, b, s in labels:
        ev.append(f"Dialogue: 1,{_ass_time(a)},{_ass_time(b)},Label,,0,0,0,,{{\\fad(300,300)}}{s}")
    open(path, "w").write(head + "\n".join(ev) + "\n")

def build(shots, lines, times, voice, out, titles=(), labels=(), tail=2.0, workdir="cut", bed=True):
    os.makedirs(workdir, exist_ok=True)
    end = times[-1][1] + tail
    starts = [s.start for s in shots] + [end]
    segs = []
    for i, s in enumerate(shots):
        d = starts[i + 1] - s.start + (T if i < len(shots) - 1 else 0)
        p = f"{workdir}/seg{i:02d}.mp4"
        if os.path.isdir(s.src): _frames_clip(s.src, d, p)
        elif s.move == "clip": _clip(s.src, d, p)
        else: _still(s.src, d, s.move, p)
        segs.append(p)
    # chain with xfade: plain fade, or a warm light flash (fadewhite) where flash=True
    inputs = sum((["-i", p] for p in segs), [])
    fc, last = [], "[0:v]"
    for i in range(1, len(segs)):
        kind = "fadewhite" if shots[i].flash else "fade"
        o = f"[x{i}]"
        fc.append(f"{last}[{i}:v]xfade=transition={kind}:duration={T}:offset={starts[i]:.3f}{o}")
        last = o
    ass = f"{workdir}/cap.ass"
    captions_ass(lines, times, ass, titles, labels)
    fc.append(f"{last}eq=saturation=0.92:contrast=1.04,noise=alls=7:allf=t,vignette=PI/5,"
              f"subtitles={ass},format=yuv420p[v]")
    # sound: narration + ambient bed with soft hits at cuts
    aud = ["-i", voice]
    amap = f"[{len(segs)}:a]"
    if bed:
        import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from hu import ambient_bed
        ambient_bed(end, cuts=starts[1:-1], out=f"{workdir}/bed.wav")
        aud += ["-i", f"{workdir}/bed.wav"]
        fc.append(f"[{len(segs)}:a]apad[va];[{len(segs)+1}:a]volume=-17dB[ba];[va][ba]amix=inputs=2:duration=longest:normalize=0,"
                  f"atrim=0:{end:.3f},loudnorm=I=-14:TP=-1.5[a]")
        amap = "[a]"
    _run(["ffmpeg", "-v", "error", "-y", *inputs, *aud, "-filter_complex", ";".join(fc),
          "-map", "[v]", "-map", amap, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
          "-c:a", "aac", "-b:a", "192k", "-t", f"{end:.3f}", out])
    return out
