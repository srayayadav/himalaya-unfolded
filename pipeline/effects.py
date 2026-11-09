"""Atmosphere + character shading for the painted look (graphics upgrade, Nov 2026).
All functions return SVG snippets; times in seconds. Put FX_DEFS inside <defs>.

  shaded(svg)            wrap a code character so it gets soft 3D lighting, a warm rim light and an outline
  mist(t, y, op, seed)   slow drifting fog bands (good over valleys)
  god_rays(cx, cy, t)    soft light shafts from a sun position
  snow(t, n, seed)       falling snow with depth (big/near flakes faster)
  embers(t, x, y)        rising sparks for fires / battle smoke
"""
import math, random

FX_DEFS = '''
<filter id="shade3d" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b"/>
  <feDiffuseLighting in="b" surfaceScale="6" diffuseConstant="1.25" lighting-color="#FFF4E4" result="lit">
    <feDistantLight azimuth="225" elevation="42"/>
  </feDiffuseLighting>
  <feBlend in="SourceGraphic" in2="lit" mode="multiply" result="sh0"/>
  <feComposite in="sh0" in2="SourceAlpha" operator="in" result="shaded"/>
  <feMorphology in="SourceAlpha" operator="dilate" radius="2" result="fat"/>
  <feFlood flood-color="#160C0B" flood-opacity="0.9"/><feComposite in2="fat" operator="in" result="outline"/>
  <feOffset in="SourceAlpha" dx="-4" dy="-3" result="off"/>
  <feComposite in="SourceAlpha" in2="off" operator="out" result="rimmask"/>
  <feFlood flood-color="#FFD98A" flood-opacity="0.75"/><feComposite in2="rimmask" operator="in" result="rim"/>
  <feMerge><feMergeNode in="outline"/><feMergeNode in="shaded"/></feMerge>
</filter>
<filter id="whiteout"><feFlood flood-color="#FFFFFF"/><feComposite in2="SourceAlpha" operator="in"/></filter>
<linearGradient id="sideshade" x1="0" y1="0" x2="1" y2="1"><stop offset="0.35" stop-color="#0B0710" stop-opacity="0"/><stop offset="1" stop-color="#0B0710" stop-opacity="0.55"/></linearGradient>
<filter id="fog" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="38"/></filter>
<filter id="soft6"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="soft2"><feGaussianBlur stdDeviation="1.6"/></filter>
<radialGradient id="sunglowfx"><stop offset="0" stop-color="#FFE7B0" stop-opacity="0.85"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>
<linearGradient id="rayfx" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9B8" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE9B8" stop-opacity="0"/></linearGradient>
'''

_n = [0]
def shaded(body, box=(-200, -420, 400, 760)):
    """Lit, outlined character plus a soft dark side (bottom-right) clipped to its silhouette.
    `box` = x, y, w, h of the area the side shade covers, in the body's own coordinates."""
    _n[0] += 1; m = f"cm{_n[0]}"; x, y, w, h = box
    return (f'<mask id="{m}"><g filter="url(#whiteout)">{body}</g></mask>'
            f'<g filter="url(#shade3d)">{body}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sideshade)" mask="url(#{m})"/>')

def mist(t, y=700, op=0.35, seed=3, n=5, col="#F3E6D6", speed=14):
    r = random.Random(seed); s = ""
    for i in range(n):
        w = r.uniform(700, 1300); h = r.uniform(60, 130); sp = speed * r.uniform(0.6, 1.4) * (1 if i % 2 else -1)
        x = (r.uniform(-300, 1900) + sp * t) % 2600 - 350
        yy = y + r.uniform(-80, 80) + 8 * math.sin(t * 0.3 + i)
        s += f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{w/2:.0f}" ry="{h/2:.0f}" fill="{col}" opacity="{op * r.uniform(0.5, 1):.3f}" filter="url(#fog)"/>'
    return s

def god_rays(cx, cy, t, n=7, length=1300, op=1.0, seed=4):
    r = random.Random(seed); s = f'<circle cx="{cx}" cy="{cy}" r="260" fill="url(#sunglowfx)" opacity="{0.8*op:.3f}"/>'
    for i in range(n):
        a = math.radians(55 + i * 70 / n + 3 * math.sin(t * 0.25 + i)); w = r.uniform(18, 60)
        x1, y1 = cx + length * math.cos(a), cy + length * math.sin(a)
        px, py = -math.sin(a) * w, math.cos(a) * w
        o = op * (0.35 + 0.25 * math.sin(t * 0.6 + i * 1.7))
        s += (f'<path d="M{cx} {cy} L{x1+px:.0f} {y1+py:.0f} L{x1-px:.0f} {y1-py:.0f}Z" fill="#FFE9B8" '
              f'opacity="{max(0, o) * 0.35:.3f}" filter="url(#soft6)"/>')
    return s

def snow(t, n=140, seed=8, W=1920, H=1080, op=0.9):
    r = random.Random(seed); s = ""
    for _ in range(n):
        z = r.random(); size = 1.5 + 5 * z; v = 40 + 130 * z
        x0 = r.uniform(0, W); y0 = r.uniform(0, H)
        y = (y0 + v * t) % (H + 40) - 20
        x = (x0 + 25 * math.sin(t * (0.6 + z) + x0) + 20 * t * z) % W
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{size:.1f}" fill="#FFFFFF" opacity="{op*(0.35+0.6*z):.2f}"{" filter=\"url(#soft2)\"" if z > 0.75 else ""}/>'
    return s

def embers(t, x, y, n=40, seed=5, spread=160, height=420):
    r = random.Random(seed); s = ""
    for _ in range(n):
        ph = r.random(); life = 2.5 + 2 * r.random(); k = ((t / life) + ph) % 1
        ex = x + r.uniform(-spread, spread) + 30 * math.sin(t * 2 + ph * 9) * k
        ey = y - height * k
        s += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{2 + 2*r.random():.1f}" fill="#FFB347" opacity="{(1-k)*0.9:.2f}"/>'
    return s
