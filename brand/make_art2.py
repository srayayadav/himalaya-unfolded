import subprocess, math, random
random.seed(7)
FLAG = ["#2F6FD6", "#F4F1E8", "#D9343A", "#2E9E5B", "#F2C230"]

def poly(pts, fill, op=1):
    return '<path d="M' + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f'Z" fill="{fill}" opacity="{op}"/>'

def peak(cx, top, base_y, wl, wr, lit, shade, snow=0.22, jag=True):
    """Two-tone mountain: lit left face, shadowed right face, jagged snow cap."""
    L, R, P = (cx - wl, base_y), (cx + wr, base_y), (cx, top)
    mid = (cx + wr * 0.12, base_y)
    s = poly([L, P, mid], lit) + poly([P, R, mid], shade)
    # snow cap
    h = (base_y - top) * snow
    lx, rx = cx - wl * snow, cx + wr * snow
    y = top + h
    pts = [P, (rx, y)]
    n = 6
    for i in range(1, n):
        x = rx - (rx - lx) * i / n
        pts.append((x, y + (random.uniform(10, h * 0.45) if i % 2 else random.uniform(-6, 8))))
    pts.append((lx, y))
    s += poly(pts, "#F7F4EF")
    # shadow on right part of snow
    s += poly([P, (rx, y), (cx + wr * 0.12 * snow, y + h * 0.25)], "#C9CFE6", 0.85)
    return s

def flags(x0, y0, x1, y1, sag, size, count):
    s = f'<path d="M{x0} {y0} Q{(x0+x1)/2} {max(y0,y1)+sag} {x1} {y1}" stroke="#E8D9C0" stroke-width="{max(1.5,size/14):.1f}" fill="none" opacity="0.8"/>'
    for i in range(count):
        t = (i + 0.5) / count
        x = (1-t)**2*x0 + 2*(1-t)*t*(x0+x1)/2 + t*t*x1
        y = (1-t)**2*y0 + 2*(1-t)*t*(max(y0,y1)+sag) + t*t*y1
        c = FLAG[i % 5]
        w, h = size*0.8, size
        sk = random.uniform(-0.15, 0.15)*w
        s += poly([(x-w/2, y), (x+w/2, y), (x+w/2+sk, y+h), (x-w/2+sk, y+h)], c, 0.95)
    return s

def mist(y, h, op):
    return f'<rect x="0" y="{y}" width="2560" height="{h}" fill="url(#mist)" opacity="{op}"/>'

# ---------------- BANNER ----------------
W, H = 2560, 1440
stars = "".join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,420):.0f}" r="{random.uniform(1,2.6):.1f}" fill="#fff" opacity="{random.uniform(.3,.8):.2f}"/>' for _ in range(70))
b = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#06142B"/><stop offset="0.32" stop-color="#0F3550"/><stop offset="0.52" stop-color="#2F6A7A"/>
<stop offset="0.64" stop-color="#E7A26A"/><stop offset="0.72" stop-color="#F6C97A"/><stop offset="1" stop-color="#F6C97A"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF4D6"/><stop offset="0.25" stop-color="#FFD98A" stop-opacity="0.9"/><stop offset="1" stop-color="#FFB25C" stop-opacity="0"/></radialGradient>
<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FCE3C0" stop-opacity="0"/><stop offset="0.5" stop-color="#FCE3C0" stop-opacity="0.55"/><stop offset="1" stop-color="#FCE3C0" stop-opacity="0"/></linearGradient>
<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E2236"/><stop offset="1" stop-color="#050B16"/></linearGradient>
<filter id="ts" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#04101F" flood-opacity="0.75"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}
<circle cx="1280" cy="930" r="520" fill="url(#sun)"/>
'''
# far range (hazy, blue)
for cx, top, wl, wr in [(180,740,420,380),(600,700,380,400),(1050,975,300,320),(1520,975,320,300),(1960,700,400,380),(2400,740,400,420)]:
    b += peak(cx, top, 1010, wl, wr, "#5E8FA6", "#3F6F88", 0.2)
b += mist(860, 200, 0.7)
# mid range: big peaks on sides, lower in centre so the title sits on open sky
for cx, top, wl, wr in [(330,600,520,470),(860,980,380,360),(1280,1010,360,360),(1700,980,360,380),(2240,590,480,540)]:
    b += peak(cx, top, 1130, wl, wr, "#2D5873", "#163448", 0.26)
b += mist(1000, 180, 0.5)
# foreground ridge
fg = [(0,1150),(180,1090),(360,1130),(560,1060),(760,1120),(980,1080),(1200,1140),(1420,1090),(1640,1135),(1860,1070),(2080,1125),(2300,1080),(2560,1120),(2560,1440),(0,1440)]
b += poly(fg, "url(#fg)")
# prayer flags (inside the always-visible strip, kept to the sides)
b += flags(-20, 560, 760, 640, 70, 34, 16)
b += flags(1800, 640, 2580, 560, 70, 34, 16)
# title block
b += f'''<g filter="url(#ts)">
<text x="1280" y="700" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" letter-spacing="10" fill="#FFFFFF">HIMALAYA</text>
<text x="1280" y="800" text-anchor="middle" font-family="Inter" font-weight="300" font-size="86" letter-spacing="46" fill="#FFD98A">UNFOLDED</text>
</g>
<rect x="1060" y="836" width="440" height="4" rx="2" fill="#FFD98A" opacity="0.9"/>
<text x="1280" y="896" text-anchor="middle" font-family="Inter" font-weight="600" font-size="38" letter-spacing="6" fill="#FFFFFF" filter="url(#ts)">STORIES FROM THE ROOF OF THE WORLD</text>
</svg>'''
open("banner2.svg", "w").write(b)

# ---------------- LOGO ----------------
S = 800
random.seed(3)
l = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B2A44"/><stop offset="0.5" stop-color="#1F5B6E"/><stop offset="0.72" stop-color="#F0A764"/><stop offset="1" stop-color="#F6C97A"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF4D6"/><stop offset="0.35" stop-color="#FFD98A"/><stop offset="1" stop-color="#FFB25C" stop-opacity="0"/></radialGradient>
<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E2236"/><stop offset="1" stop-color="#050B16"/></linearGradient>
<clipPath id="c"><circle cx="400" cy="400" r="330"/></clipPath>
</defs>
<rect width="{S}" height="{S}" fill="#06142B"/>
<circle cx="400" cy="400" r="372" fill="none" stroke="#FFD98A" stroke-width="14"/>
<circle cx="400" cy="400" r="346" fill="none" stroke="#FFD98A" stroke-width="3" opacity="0.6"/>
<g clip-path="url(#c)">
<rect width="{S}" height="{S}" fill="url(#bg)"/>
<circle cx="400" cy="470" r="230" fill="url(#sun)"/>
{peak(170, 400, 620, 260, 230, "#5E8FA6", "#3F6F88", 0.22)}
{peak(640, 420, 620, 230, 260, "#5E8FA6", "#3F6F88", 0.22)}
{peak(400, 170, 690, 300, 300, "#2D5873", "#163448", 0.27)}
{poly([(0,640),(140,590),(300,640),(470,595),(640,645),(800,600),(800,800),(0,800)], "url(#fg)")}
{flags(40, 430, 360, 470, 40, 20, 9)}
</g>
</svg>'''
open("logo2.svg", "w").write(l)
subprocess.run(["rsvg-convert", "banner2.svg", "-o", "banner2.png"], check=True)
subprocess.run(["rsvg-convert", "logo2.svg", "-o", "logo2.png"], check=True)
