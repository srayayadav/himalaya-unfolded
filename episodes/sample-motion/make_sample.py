"""Graphics-upgrade sample for Santosh (9 Nov 2026): one scene, four versions, 8 s each.
1 AI motion (SVD) · 2 depth parallax · 3 new character + effects · 4 everything together.
Needs kaggle/g_hook_depth.png and kaggle/g_hook_svd*_NN.jpg from the Kaggle job."""
import sys, os, glob, subprocess
sys.path.insert(0, "../../pipeline")
from parallax import render_parallax
from fx_overlay import overlay_svg
from hu import text, card, WHITE

PAINT = "../003-gurkhas/bg/g_hook.jpg"
DEPTH = "kaggle/g_hook_depth.png"
D, FPS, W, H = 8, 30, 1920, 1080

def svd_bg(mb, out):
    fr = sorted(glob.glob(f"kaggle/g_hook_svd{mb}_*.jpg"))
    # 25 generated frames -> forward then backward (seamless), stretched to 8 s with motion interpolation
    os.makedirs("pp", exist_ok=True)
    seq = fr + fr[-2:0:-1]
    for i, f in enumerate(seq):
        subprocess.run(["cp", f, f"pp/{i:03d}.jpg"])
    src_fps = len(seq) / D
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", f"{src_fps:.4f}", "-i", "pp/%03d.jpg",
                    "-vf", f"scale={W}:{H}:flags=lanczos,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,format=yuv420p",
                    "-t", str(D), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True)
    subprocess.run("rm -rf pp", shell=True)

def static_bg(out):
    # what we do today: still painting with a slow push-in
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", PAINT, "-vf",
                    f"scale=2400:-2,zoompan=z='1+0.0004*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={D*FPS}:s={W}x{H}:fps={FPS},format=yuv420p",
                    "-frames:v", str(D * FPS), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True)

def tag_svg(label):
    return card(40, 40, 30 + 19 * len(label), 64, 0.9) + text(60 + 9.5 * len(label), 84, label, 30, WHITE, 700)

def compose(bg, out, label, **kw):
    """Background video + per-frame transparent overlay (character/effects/label)."""
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", bg, "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]",
                           "-frames:v", str(D * FPS), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out],
                          stdin=subprocess.PIPE)
    for k in range(D * FPS):
        t = k / FPS
        s = overlay_svg(t, D, **kw).replace("</svg>", tag_svg(label) + "</svg>")
        ff.stdin.write(subprocess.run(["rsvg-convert", "-f", "png"], input=s.encode(), capture_output=True).stdout)
    ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    none = dict(char=False, rays=False, snowfall=False, fog=False)
    static_bg("out/bg_static.mp4")
    render_parallax(PAINT, DEPTH, "out/bg_parallax.mp4", dur=D, move="push", amp=60)
    mb = 90 if glob.glob("kaggle/g_hook_svd90_*.jpg") else 40
    svd_bg(mb, "out/bg_svd.mp4")
    compose("out/bg_static.mp4", "out/v0.mp4", "AHILE KO", char=True, rays=False, snowfall=False, fog=False, shade=False)
    compose("out/bg_svd.mp4", "out/v1.mp4", "1  CHALNE PAINTING (AI)", **none)
    compose("out/bg_parallax.mp4", "out/v2.mp4", "2  3D GAHIRAI", **none)
    compose("out/bg_static.mp4", "out/v3.mp4", "3  NAYA CHARACTER + EFFECTS")
    compose("out/bg_parallax.mp4", "out/v4.mp4", "4  SABAI EKAI THAU")
    open("out/list.txt", "w").write("".join(f"file 'v{i}.mp4'\n" for i in range(5)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/list.txt", "-c", "copy",
                    "graphics_sample.mp4"], check=True)
    print("done")
