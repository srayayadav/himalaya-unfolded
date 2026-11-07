import subprocess, sys
sys.path.insert(0, "../../pipeline")
from scenes import *
from characters import character, PRITHVI_NARAYAN
W, H = 1280, 720

# B: squeezed between two empires
b = bg(W, H, "night", 30, 4) + '<circle cx="640" cy="420" r="300" fill="url(#glow)"/>'
b += boulder(220, 470, 300, 260, "#5A6577") + text(220, 490, "CHINA", 54, WHITE, 900)
b += boulder(1060, 470, 300, 260, "#7A3A30") + text(1060, 470, "BRITISH", 50, WHITE, 900) + text(1060, 525, "INDIA", 50, WHITE, 900)
PB = projector(79.6, 26.0, 88.6, 30.8, 470, 360, 810, 560)
b += '<g filter="url(#ts)">' + country_path("Nepal", PB, GOLD, 1, GOLD, 1) + '</g>'
b += text(640, 130, "SQUEEZED.", 112, WHITE, 900, ls=4) + text(640, 250, "NEVER CRUSHED.", 104, GOLD, 900, ls=4)
open("thumb_b.svg", "w").write(svg(b, W, H))

# C: the king who saw it coming
c = bg(W, H, "sky", 30, 6) + '<circle cx="980" cy="560" r="320" fill="url(#glow)"/>'
c += peak(1000, 380, 760, 330, 330) + peak(1240, 440, 760, 260, 260)
c += character(330, 470, 1.25, PRITHVI_NARAYAN, 1.0, gesture=0.8)
c += text(860, 140, "HOW NEPAL", 104, WHITE, 900, ls=4) + text(860, 260, "STAYED FREE", 104, GOLD, 900, ls=4)
c += f'<rect x="640" y="600" width="520" height="80" rx="16" fill="#C8553D"/>' + text(900, 655, "1814 – 1923", 50, WHITE, 900, shadow=False)
open("thumb_c.svg", "w").write(svg(c, W, H))
for n in "bc":
    subprocess.run(["rsvg-convert", f"thumb_{n}.svg", "-o", f"thumb_{n}.png"], check=True)
