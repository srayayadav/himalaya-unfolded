"""Code-drawn map and runway diagram for ep 005 (real Natural Earth borders; facts from the script)."""
import sys, subprocess; sys.path.insert(0, "../../pipeline")
from hu import svg, text, card, projector, country_path, GOLD, WHITE, CREAM
W, H = 1920, 1080

def png(body, out):
    open("/tmp/g.svg", "w").write(svg(body, W, H)); subprocess.run(["rsvg-convert", "-o", out, "/tmp/g.svg"], check=True)

def nepal_map():
    p = projector(79.5, 25.8, 89.8, 31.2, 140, 120, 1780, 980)
    b = '<rect width="1920" height="1080" fill="#0E2A33"/>'
    for c, f in (("China", "#1D3B45"), ("India", "#1D3B45"), ("Bhutan", "#1D3B45"), ("Bangladesh", "#1D3B45")):
        try: b += country_path(c, p, f, 1, "#2E5560", 2)
        except KeyError: pass
    b += country_path("Nepal", p, "#3F6B58", 1, GOLD, 3)
    kx, ky = p(85.324, 27.717); lx, ly = p(86.731, 27.687)
    b += f'<path d="M{kx:.0f} {ky:.0f} Q{(kx+lx)/2:.0f} {ky-120:.0f} {lx:.0f} {ly:.0f}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="14 12"/>'
    for x, y, n, dy in ((kx, ky, "KATHMANDU", 70), (lx, ly, "LUKLA", -40)):
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="{GOLD}" stroke="#0E2A33" stroke-width="4"/>' + text(x, y + dy, n, 46, WHITE, 800)
    b += text(960, 1020, "NEPAL · borders: Natural Earth", 30, CREAM, 600, op=0.8)
    png(b, "img/g_map.png")

def runway():
    b = '<rect width="1920" height="1080" fill="#0E2A33"/>' + text(960, 120, "TENZING-HILLARY AIRPORT, LUKLA", 56, WHITE, 800)
    # top view
    b += f'<rect x="260" y="230" width="1400" height="110" rx="6" fill="#3A3F44" stroke="{CREAM}" stroke-width="3"/>'
    b += "".join(f'<rect x="{x}" y="281" width="60" height="8" fill="{WHITE}" opacity="0.8"/>' for x in range(330, 1600, 130))
    b += f'<path d="M260 390 L1660 390" stroke="{GOLD}" stroke-width="4"/><path d="M260 375 L260 405 M1660 375 L1660 405" stroke="{GOLD}" stroke-width="4"/>' + text(960, 450, "527 m long", 54, GOLD, 800)
    b += f'<path d="M1720 230 L1720 340" stroke="{GOLD}" stroke-width="4"/>' + text(1790, 300, "20 m", 40, GOLD, 800)
    # side profile: uphill toward the 24 end (exaggerated for clarity)
    b += f'<path d="M260 900 L1660 700 L1660 940 L260 940Z" fill="#3F6B58"/><path d="M260 900 L1660 700" stroke="{CREAM}" stroke-width="10"/>'
    b += text(960, 990, "Side view: about 11.75% uphill (slope exaggerated)", 38, CREAM, 600)
    b += text(520, 700, "LAND on 06 → uphill", 44, WHITE, 800) + text(1380, 610, "← TAKE OFF from 24, downhill", 44, WHITE, 800)
    png(b, "img/g_runway.png")

nepal_map(); runway(); print("ok")
