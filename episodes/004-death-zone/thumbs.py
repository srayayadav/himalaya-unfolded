"""Three Test & Compare thumbnails (1280x720): A diagram-led, B scene-led, C big question. No bodies shown."""
import sys, subprocess
sys.path.insert(0, "../../pipeline")
from epkit import *
import scenes as S

def big(x, y, s, size, col=WHITE, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="900" font-size="{size}" fill="{col}" '
            f'stroke="#06142B" stroke-width="{size*0.09:.0f}" paint-order="stroke" letter-spacing="2">{s}</text>')

def save(body, out):
    open("thumb.svg", "w").write(svg(body, 1920, 1080))
    subprocess.run(["rsvg-convert", "-w", "1280", "-h", "720", "thumb.svg", "-o", out], check=True)

# A: diagram-led (death zone band over the summit)
a = DEFS + PAINT("d_title") + dim(0.1)
a += f'<rect x="0" y="0" width="1920" height="430" fill="{S.ORED}" opacity="0.35"/><path d="M0 430 L1920 430" stroke="{S.ORED}" stroke-width="10" stroke-dasharray="40 20"/>'
a += big(960, 300, "DEATH ZONE", 200, WHITE) + big(960, 560, "8,000 m+", 120, GOLD)
save(a, "thumb_a.png")
# B: scene-led (night queue of headlamps on the ridge)
b = DEFS + PAINT("d_hook") + dim(0.3) + S.queue(3.0, S.RIDGE, 16, 1.4, 0, True)
b += big(1880, 820, "WHY THEY NEVER", 130, WHITE, "end") + big(1880, 990, "CAME DOWN", 150, GOLD, "end")
save(b, "thumb_b.png")
# C: big question
c = DEFS + PAINT("d_northridge") + dim(0.35)
c += big(960, 420, "BODIES LEFT ON", 150, WHITE) + big(960, 680, "EVEREST?", 250, GOLD)
save(c, "thumb_c.png")
print("ok")
