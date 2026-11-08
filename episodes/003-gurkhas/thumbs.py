"""Three Test & Compare thumbnails (1280x720): A map-led, B character-led, C big question."""
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

# A: map-led
a = S.nepal_map(1) + dim(0.15)
G = S.PZ(84.63, 28.0)
a += f'<circle cx="{G[0]:.0f}" cy="{G[1]:.0f}" r="60" fill="none" stroke="{GOLD}" stroke-width="10"/>' + big(G[0], G[1] - 90, "GORKHA", 70, GOLD)
a += S.khukuri(1100, 760, 2.0, -12)
a += big(60, 190, "WHY ARMIES", 150, WHITE, "start") + big(60, 340, "FEARED THEM", 150, GOLD, "start")
save(DEFS + a, "thumb_a.png")
# B: character-led
b = DEFS + PAINT("g_end") + shade(0.5)
b += warm(character(1350, 960, 1.35, GURKHA, 0.5, gesture=0.9)) + S.khukuri(1530, 300, 1.2, -40)
b += big(80, 300, "THE", 120, WHITE, "start") + big(80, 470, "GURKHAS", 190, GOLD, "start")
save(b, "thumb_b.png")
# C: big question
c = DEFS + PAINT("g_burma") + dim(0.35)
for i in range(7): c += medal(260 + i * 230, 860, 1.3)
c += big(960, 330, "WHO ARE THE", 140, WHITE) + big(960, 520, "GURKHAS?", 210, GOLD)
save(c, "thumb_c.png")
print("ok")
