"""2.5D camera move on a painting using its depth map (graphics upgrade, Nov 2026).

render_parallax(img_path, depth_path, out_mp4, dur=8, move="push", amp=40)
  depth map: white = near (Depth Anything V2 output). Near pixels shift more than far ones, so the
  ridges slide past each other like a real camera move. Output 1920x1080, 30 fps, H.264.
moves: "push" (slow dolly in), "pan" (sideways truck), "rise" (camera rises)
"""
import subprocess, numpy as np, cv2

W, H, FPS = 1920, 1080, 30

def _ease(x):
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(x, 0, 1))

def frames(img_path, depth_path, dur=8, move="push", amp=40):
    img = cv2.resize(cv2.imread(img_path), (W, H), interpolation=cv2.INTER_CUBIC)
    d = cv2.resize(cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE), (W, H)).astype(np.float32) / 255.0
    d = cv2.GaussianBlur(d, (0, 0), 3)               # soften depth edges -> fewer tearing artefacts
    d = (d - d.min()) / max(1e-6, d.max() - d.min())
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H * 0.55
    n = int(dur * FPS)
    for k in range(n):
        p = _ease(k / (n - 1)) * 2 - 1                # -1 .. 1 over the shot
        if move == "pan":
            dx, dy, z = amp * p, 0.0, 0.0
        elif move == "rise":
            dx, dy, z = 0.0, -amp * 0.6 * p, 0.0
        else:  # push
            dx, dy, z = amp * 0.25 * p, 0.0, 0.05 * (p + 1) / 2
        # zoom grows with nearness (near layers scale more), plus depth-weighted translation
        s = 1.0 + z * (0.4 + 0.6 * d)
        mapx = cx + (xs - cx) / s - dx * d
        mapy = cy + (ys - cy) / s - dy * d
        # overscan 4% so the frame edges never show empty space
        mapx = (mapx - cx) * 0.96 + cx
        mapy = (mapy - cy) * 0.96 + cy
        yield cv2.remap(img, mapx.astype(np.float32), mapy.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def render_parallax(img_path, depth_path, out_mp4, dur=8, move="push", amp=40):
    tmp = out_mp4[:-4] + ".tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                           "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in frames(img_path, depth_path, dur, move, amp):
        ff.stdin.write(f.tobytes())
    ff.stdin.close()
    if ff.wait() == 0:
        import os; os.replace(tmp, out_mp4)
    return out_mp4
