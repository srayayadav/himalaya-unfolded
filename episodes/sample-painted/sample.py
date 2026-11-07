import sys, base64, math, random, json, subprocess, os
sys.path.insert(0, "../../pipeline")
from hu import *
from characters import character, GURKHA, BRITISH_OFFICER
from style2 import TEXTURE_DEFS, smoke, stone_fort, lower_third

W, H = 1920, 1080
BG = "data:image/jpeg;base64," + base64.b64encode(open("bg_nalapani.jpg", "rb").read()).decode()
K = 1920 / 1344
WARM = '''<filter id="warm"><feColorMatrix type="matrix" values="0.84 0.03 0.01 0 0.08  0.02 0.80 0.02 0 0.04  0.01 0.02 0.76 0 0.02  0 0 0 1 0"/></filter>
<filter id="flash"><feGaussianBlur stdDeviation="10"/></filter>'''

def grass(x0, x1, y, seed):
    r = random.Random(seed); s = ""
    for _ in range(170):
        x = r.uniform(x0, x1); yy = y + r.uniform(0, 18); h = r.uniform(10, 34)
        s += f'<path d="M{x:.0f} {yy:.0f} q{r.uniform(-4,4):.0f} {-h/2:.0f} {r.uniform(-7,7):.0f} {-h:.0f}" stroke="#5E3A34" stroke-width="2.4" fill="none" opacity="0.95"/>'
    return s

def frame(t, d, W, H):
    b = TEXTURE_DEFS.replace("<defs>", "<defs>" + WARM)
    b += f'<image href="{BG}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
    fx, fy, fw, fh = 300, 360, 430, 140
    base_y = fy + fh
    b += f'<ellipse cx="{fx+fw/2:.0f}" cy="{base_y+6}" rx="{fw*0.62:.0f}" ry="22" fill="#1A0D0D" opacity="0.45" filter="url(#flash)"/>'
    g = f'<g filter="url(#warm)">'
    for i, x in enumerate(range(fx + 50, fx + fw - 30, 62)):
        talk = (i == 2 and 1.0 < t < 8.5)
        gest = 0.5 + 0.5 * math.sin(t * 1.3) if i == 2 else (0.3 if i % 2 else 0)
        g += character(x, fy - 12, 0.24, GURKHA, t + i * 0.9, talking=talk, gesture=gest)
    g += stone_fort(fx, fy, fw, fh, t)
    # Company troops advancing slowly up the slope
    for i in range(9):
        x = 1180 + i * 62 - 9 * t; y = 900 + (i % 3) * 26 + 3 * math.sin(t * 5 + i)
        g += character(x, y, 0.27, BRITISH_OFFICER, t * 1.1 + i * 0.4, flip=True)
    g += '</g>'
    b += g + grass(fx - 40, fx + fw + 40, base_y - 6, 3)
    # musket flashes from the fort walls + drifting powder smoke
    r = random.Random(int(t * 3))
    if r.random() < 0.35:
        mx = fx + r.uniform(20, fw - 20)
        b += f'<circle cx="{mx:.0f}" cy="{fy - 6}" r="26" fill="#FFD27A" opacity="0.85" filter="url(#flash)"/>'
    b += smoke(fx + fw - 30, fy, t, 4, 0.55) + smoke(fx + 40, fy, t + 1.4, 5, 0.45) + smoke(1220 - 9 * t, 820, t + 0.6, 6, 0.4)
    b += lower_third(W, H, "NALAPANI, 1814", "~600 Gorkha defenders · ~3,500 Company troops", prog(t, 0.8, 1.6))
    return fade(b, t, d, W, H, fin=0.5, fout=0.6)

if __name__ == "__main__":
    lines = ["At a small hill fort called Nalapani, about six hundred Gorkha soldiers held out against some three thousand five hundred Company troops.",
             "For a whole month, they refused to surrender."]
    times = narrate(lines)
    d = times[-1][1] + 1.2
    if sys.argv[1:] == ["preview"]:
        preview(frame, 4.0, d, W, H, "p_sample.png")
    else:
        os.makedirs("scenes", exist_ok=True)
        render_scene(frame, d, W, H, "scenes/m01.mp4")
        finish(["scenes/m01.mp4"], "voice.wav", "nalapani_painted_sample.mp4", bed_db=-15, srt_lines=lines, srt_times=times)
