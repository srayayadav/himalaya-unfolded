"""Transparent overlay for the graphics-upgrade sample: foreground ridge, shaded Gurkha walking in,
mist, god rays, snow. Rendered over any background (static / AI-motion / parallax)."""
import sys, os, math
sys.path.insert(0, "../../pipeline")
from hu import *
from characters import character, GURKHA
from painted import grass, ground_shadow, WARM_DEFS
from effects import *

W, H = 1920, 1080

def ridge(t):
    # dark foreground ridge drawn in code so the character stands on solid ground
    d = "M-20 1100 L-20 905 Q260 860 520 880 Q760 900 980 950 Q1300 1010 1940 985 L1940 1100Z"
    return (f'<path d="{d}" fill="#24303A"/>'
            f'<path d="M-20 905 Q260 860 520 880 Q760 900 980 950 Q1300 1010 1940 985" fill="none" stroke="#C9A97A" stroke-width="4" opacity="0.5"/>'
            + grass(-20, 1000, 884, 3, n=120, col="#24303A"))

def overlay(t, d, char=True, rays=True, snowfall=True, fog=True, shade=True):
    s = ""
    if rays: s += god_rays(1450, 140, t, op=0.9)
    if fog: s += mist(t, y=760, op=0.42, seed=3) + mist(t, y=560, op=0.22, seed=9, n=4, speed=8)
    if char:
        x = 260 + min(1, t / 3.2) * 300          # walks in from the left, then stops
        walking = t < 3.2
        y = 880 - 2 + (abs(math.sin(t * 6)) * 8 if walking else 0)
        g = character(0, 0, 1.0, GURKHA, t=t, talking=False, gesture=(min(1, max(0, (t - 4.0) / 0.8)) * 0.9 if t > 4 else 0))
        inner = shaded(g, box=(-200, -260, 420, 600)) if shade else g
        s += ridge(t) + ground_shadow(x, 893, 95)
        s += f'<g filter="url(#warm)"><g transform="translate({x:.0f} {y + 12 - 305:.0f}) scale(0.95)">{inner}</g></g>'
        lab = min(1, max(0, (t - 3.6) / 0.6))
        if lab > 0:
            s += card(x - 170, 935, 340, 58, lab) + text(x, 975, "A GURKHA SOLDIER", 28, WHITE, 700, op=lab)
    if snowfall: s += snow(t, n=110, op=0.75)
    return f'<defs>{FX_DEFS}{WARM_DEFS}</defs>' + s

def overlay_svg(t, d, **kw):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{overlay(t, d, **kw)}</svg>'

if __name__ == "__main__":
    import subprocess
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 5
    open("ov.svg", "w").write(overlay_svg(t, 8))
    subprocess.run(["rsvg-convert", "-o", "ov.png", "ov.svg"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "../003-gurkhas/bg/g_hook.jpg", "-i", "ov.png", "-filter_complex",
                    "[0]scale=1920:1080[b];[b][1]overlay", "-frames:v", "1", "test_c.jpg"], check=True)
