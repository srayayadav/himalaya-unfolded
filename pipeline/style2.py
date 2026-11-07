"""Richer illustration helpers ("painted documentary" look), all free and code-drawn.
- natural ridgelines (fractal noise, smooth curves) instead of straight triangles
- atmospheric haze between layers, soft clouds, smoke, pine trees, stone walls
- paper/grain texture and warm light overlays
Use with hu.svg(): put TEXTURE_DEFS inside the body once, then call the helpers.
"""
import math, random

TEXTURE_DEFS = '''<defs>
<filter id="paper" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 0.10 0"/>
</filter>
<filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="soft2"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="10"/></filter>
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2A4A"/><stop offset="0.45" stop-color="#5B4A6E"/><stop offset="0.75" stop-color="#C9785A"/><stop offset="1" stop-color="#F2B36B"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#FFE7B0" stop-opacity="0.9"/><stop offset="1" stop-color="#FFB86B" stop-opacity="0"/></radialGradient>
<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2C9A0" stop-opacity="0"/><stop offset="1" stop-color="#F2C9A0" stop-opacity="0.55"/></linearGradient>
</defs>'''

def ridge_path(W, H, base, amp, seed, rough=1.0, steps=90):
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in range(5)]
    pts = []
    for i in range(steps + 1):
        x = W * i / steps; u = x / W
        y = base - amp * (0.55 * math.sin(u * 3.1 + ph[0]) + 0.3 * math.sin(u * 7.3 + ph[1])
                          + rough * 0.15 * math.sin(u * 17 + ph[2]) + rough * 0.06 * math.sin(u * 41 + ph[3]))
        pts.append((x, y))
    d = f"M0 {H} L" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f" L{W} {H}Z"
    return d, pts

def layer(W, H, base, amp, seed, fill, haze_op=0.0, rough=1.0, snow_above=None):
    d, pts = ridge_path(W, H, base, amp, seed, rough)
    s = f'<path d="{d}" fill="{fill}"/>'
    if snow_above is not None:  # snow on the highest parts
        s += f'<clipPath id="sc{seed}"><path d="{d}"/></clipPath><rect x="0" y="0" width="{W}" height="{snow_above}" fill="#F4F1EC" opacity="0.92" clip-path="url(#sc{seed})"/>'
    if haze_op: s += f'<rect x="0" y="{base - amp:.0f}" width="{W}" height="{H - base + amp:.0f}" fill="url(#haze)" opacity="{haze_op}"/>'
    return s

def clouds(W, y, n, seed, op=0.35, col="#F6D9C0", drift=0):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = (r.uniform(-200, W + 200) + drift) % (W + 400) - 200; yy = y + r.uniform(-60, 60); w = r.uniform(180, 420)
        s += f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{w:.0f}" ry="{w*0.16:.0f}" fill="{col}" opacity="{op}" filter="url(#soft)"/>'
    return s

def pines(W, y0, n, seed, col="#0C1420", scale=1.0):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(0, W); h = r.uniform(60, 140) * scale; w = h * 0.35; y = y0 + r.uniform(-10, 30)
        s += f'<path d="M{x:.0f} {y-h:.0f} L{x+w:.0f} {y:.0f} L{x-w:.0f} {y:.0f}Z" fill="{col}"/>'
    return s

def smoke(x, y, t, seed, op=0.5):
    r = random.Random(seed); s = ""
    for i in range(7):
        k = (t * 0.25 + i / 7) % 1
        s += f'<circle cx="{x + 40*k + r.uniform(-8,8):.0f}" cy="{y - 260*k:.0f}" r="{18 + 70*k:.0f}" fill="#B8B0A8" opacity="{op*(1-k):.2f}" filter="url(#soft2)"/>'
    return s

def stone_fort(x, y, w, h, t=0):
    s = f'<g filter="url(#rough)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#5A5248"/>'
    for i in range(0, w, 40):
        s += f'<rect x="{x+i}" y="{y-24}" width="26" height="26" fill="#5A5248"/>'
    for j in range(0, h, 22):
        for i in range((j // 22) % 2 * 20, w, 40):
            s += f'<rect x="{x+i}" y="{y+j}" width="38" height="20" fill="none" stroke="#3E3830" stroke-width="2"/>'
    s += '</g>'
    fl = 8 * math.sin(t * 4)
    s += f'<rect x="{x+w//2}" y="{y-150}" width="5" height="130" fill="#D8D2C8"/><path d="M{x+w//2+5} {y-148} Q{x+w//2+40} {y-138+fl:.0f} {x+w//2+80} {y-136} L{x+w//2+5} {y-110}Z" fill="#B3261E"/>'
    return s

def paper_overlay(W, H, op=1):
    return f'<rect width="{W}" height="{H}" filter="url(#paper)" opacity="{op}"/><rect width="{W}" height="{H}" fill="#3A2410" opacity="0.06"/>'

def lower_third(W, H, title, sub, op=1, gold="#FFD98A"):
    return (f'<g opacity="{op:.2f}"><rect x="70" y="{H-200}" width="10" height="120" fill="{gold}"/>'
            f'<text x="104" y="{H-140}" font-family="Inter" font-weight="900" font-size="64" fill="#FFFFFF" letter-spacing="4">{title}</text>'
            f'<text x="106" y="{H-92}" font-family="Inter" font-weight="500" font-size="34" fill="#F3DCC0">{sub}</text></g>')
