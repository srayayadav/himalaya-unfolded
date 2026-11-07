import sys, json, math, random
sys.path.insert(0, "../../pipeline")
from hu import *

BEATS = json.load(open("beats.json"))
END = BEATS[-1][1] + 2.8
STARTS = [b[0] for b in BEATS]
BOUNDS = list(zip(STARTS, STARTS[1:] + [END]))
def L(i, k):  # local start time of line k in beat i
    return BEATS[i][2][k][0] - STARTS[i]

RED = "#C8553D"; TEAL = "#3E8C8C"; NEP = "#2F6A7A"; LAND = "#1C3B52"

# ---------- real map (Natural Earth, public domain) ----------
PZ = projector(76.8, 25.0, 89.6, 31.9, 40, 170, 1880, 1070)      # Nepal close-up
PW = projector(58, -6, 112, 40, 0, 40, 1920, 1080)               # South & Southeast Asia
def P(lon, lat): return PZ(lon, lat)
def mp(pts): return [P(*p) for p in pts]
NEPAL = [(80.06,28.84),(80.5,29.7),(81.1,30.2),(81.5,30.4),(82.2,30.1),(83.3,29.5),(84.1,29.2),(84.7,28.6),(85.4,28.3),(86.0,27.9),(86.8,28.0),(87.5,27.9),(88.1,27.9),(88.2,27.3),(88.0,26.6),(87.3,26.4),(86.0,26.6),(85.2,26.8),(84.6,27.3),(83.4,27.5),(82.7,27.5),(81.9,27.9),(81.0,28.4)]
# historical areas (approximate, drawn by hand): Kumaon & Garhwal, western Terai, land east of the Mechi
WEST = [(80.06,28.84),(80.5,29.7),(81.1,30.2),(80.2,30.9),(79.2,31.2),(78.3,31.2),(77.8,30.6),(78.1,30.0),(79.0,29.4),(79.6,28.9)]
TERAI = [(80.06,28.6),(81.0,28.1),(81.9,27.7),(82.7,27.3),(83.4,27.35),(84.2,27.25),(84.2,26.95),(83.4,27.05),(82.6,27.0),(81.8,27.3),(80.9,27.75),(80.0,28.25)]
EAST = [(88.15,27.4),(88.15,27.9),(88.8,27.9),(88.9,26.7),(88.05,26.5)]
KTM, GORKHA, NALAPANI = P(85.32,27.7), P(84.63,28.0), P(78.05,30.33)

def nepal(fill, op=1, proj=None, sw=2):
    return country_path("Nepal", proj or PZ, fill, op, "#E8F1F5" if op > 0.5 else "#0A1A2C", sw)
def region_bg(W, H, op=1, india_label=True, china_label=True):
    s = f'<rect width="{W}" height="{H}" fill="#0E2A40"/>'
    s += country_path("China", PZ, "#24324A", 0.95*op) + country_path("India", PZ, "#2B2A3F", 0.95*op)
    s += country_path("Bhutan", PZ, "#2A3A4A", 0.95*op) + country_path("Bangladesh", PZ, "#2B2A3F", 0.95*op)
    if china_label: s += text(1650, 330, "QING CHINA", 40, "#9FB3C8", 800, op=0.7*op, ls=8, shadow=False)
    if india_label: s += text(420, 1040, "BRITISH INDIA", 40, "#C9A9A0", 800, op=0.7*op, ls=8, shadow=False)
    return s

BRITISH = ["India", "Pakistan", "Bangladesh", "Sri Lanka", "Myanmar", "Malaysia"]
FRENCH_DUTCH = ["Vietnam", "Laos", "Cambodia", "Indonesia"]
OTHERS = ["China", "Afghanistan", "Iran", "Thailand", "Bhutan", "Mongolia", "Tajikistan", "Turkmenistan", "Uzbekistan", "Kyrgyzstan", "Oman", "Philippines", "Brunei", "Singapore", "Timor-Leste", "North Korea", "South Korea", "Taiwan", "Kazakhstan"]
def asia(p_brit, p_fd, nepal_fill=NEP, nepal_op=1):
    s = f'<rect width="1920" height="1080" fill="#0E2A40"/>'
    for c in OTHERS:
        if c in countries(): s += country_path(c, PW, "#24324A", 1, "#0E2A40", 1.5)
    for c in BRITISH: s += country_path(c, PW, "#2B2A3F", 1, "#0E2A40", 1.5) + country_path(c, PW, RED, 0.85*p_brit, "#0E2A40", 1.5)
    for c in FRENCH_DUTCH: s += country_path(c, PW, "#2B2A3F", 1, "#0E2A40", 1.5) + country_path(c, PW, "#7B5EA7", 0.85*p_fd, "#0E2A40", 1.5)
    return s + nepal(nepal_fill, nepal_op, PW, 2.5)

def dot(x, y, label, op=1, r=12, dy=-26, size=34, col=GOLD):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{op:.2f}"/>' + text(x, y + dy, label, size, WHITE, 700, op=op)

def counter(x, y, val, label, op, size=120, col=GOLD):
    return text(x, y, val, size, col, 900, op=op) + text(x, y + 56, label, 36, CREAM, 600, op=op)

def soldiers(x0, y0, n, cols, op, col, scale=1.0, seed=1):
    r = random.Random(seed); s = ""
    for i in range(n):
        x = x0 + (i % cols) * 26 * scale + r.uniform(-3, 3); y = y0 + (i // cols) * 34 * scale
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7*scale:.1f}" fill="{col}" opacity="{op:.2f}"/>'
        s += f'<rect x="{x-6*scale:.0f}" y="{y+8*scale:.0f}" width="{12*scale:.0f}" height="{16*scale:.0f}" rx="4" fill="{col}" opacity="{op:.2f}"/>'
    return s

def gurkha(x, y, s, op=1, col="#0F2438"):
    """Simple soldier silhouette with a slouch hat."""
    return f'''<g transform="translate({x:.0f} {y:.0f}) scale({s:.3f})" opacity="{op:.2f}">
<ellipse cx="0" cy="-118" rx="34" ry="8" fill="{col}"/><path d="M-18 -120 Q0 -150 18 -120Z" fill="{col}"/>
<circle cx="0" cy="-100" r="15" fill="{col}"/><path d="M-26 -84 L26 -84 L22 -20 L-22 -20Z" fill="{col}"/>
<path d="M-20 -20 L-24 40 L-10 40 L0 -5 L10 40 L24 40 L20 -20Z" fill="{col}"/>
<path d="M26 -80 L44 -40 L36 -36 L22 -64Z" fill="{col}"/><path d="M-26 -80 L-40 -36 L-32 -34 L-22 -60Z" fill="{col}"/>
<path d="M40 -44 Q66 -60 70 -30 Q58 -44 44 -38Z" fill="{col}"/></g>'''

# ---------- scenes ----------
def s0(t, d, W, H):  # empires swallow South Asia
    pb, pf = prog(t, 1.0, L(0,1)+2.5), prog(t, L(0,2), L(0,2)+1.5)
    b = asia(pb, pf)
    for i, (lab, lon, lat) in enumerate([("INDIA", 79, 22), ("BURMA", 96, 21), ("CEYLON", 80.7, 7.8)]):
        x, y = PW(lon, lat); o = prog(t, L(0,1) + i*0.8, L(0,1) + i*0.8 + 0.5)
        b += card(x - 120, y - 52, 240, 74, o) + text(x, y, lab, 40, WHITE, 800, op=o)
    x, y = PW(104, 14); b += text(x, y, "FRENCH", 36, WHITE, 800, op=pf)
    x, y = PW(110, -2.5); b += text(x - 40, y, "DUTCH", 36, WHITE, 800, op=pf)
    b += text(960, 120, "1800s: EMPIRES IN ASIA", 64, WHITE, 900, op=prog(t, 0.2, 1.0), ls=4)
    b += f'<rect x="60" y="960" width="34" height="34" rx="6" fill="{RED}" opacity="{pb:.2f}"/>' + text(110, 990, "British rule", 32, WHITE, 600, "start", pb)
    b += f'<rect x="60" y="1010" width="34" height="34" rx="6" fill="#7B5EA7" opacity="{pf:.2f}"/>' + text(110, 1040, "French &amp; Dutch rule", 32, WHITE, 600, "start", pf)
    return fade(b, t, d, W, H, fin=0.6)

def s1(t, d, W, H):  # but Nepal survived
    g = prog(t, 0.5, 2.0)
    b = asia(1, 1, GOLD, 1)
    x, y = PW(84, 28.4)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{60 + 200*(1-g):.0f}" fill="none" stroke="{GOLD}" stroke-width="5" opacity="{g:.2f}"/>'
    o = prog(t, L(1,1), L(1,1)+0.6)
    b += card(x + 160, y - 90, 560, 170, o) + text(x + 440, y - 15, "NEPAL", 80, WHITE, 900, op=o, ls=10) + text(x + 440, y + 50, "never colonized", 44, GOLD, 600, op=o)
    return fade(b, t, d, W, H)

def s2(t, d, W, H):  # title card
    b = bg(W, H, "sky", 50, 3) + f'<circle cx="960" cy="760" r="420" fill="url(#glow)"/>'
    b += peak(330, 560, 1150, 520, 470) + peak(1590, 600, 1150, 470, 520) + peak(960, 760, 1150, 400, 400)
    b += flags(-20, 420, 700, 470, 60, 30, 14) + flags(1220, 470, 1940, 420, 60, 30, 14)
    b += text(960, 300, "WHY NEPAL WAS", 110, WHITE, 900, op=prog(t, 0, 0.6), ls=6)
    b += text(960, 420, "NEVER COLONIZED", 120, GOLD, 900, op=prog(t, 0.3, 0.9), ls=6)
    for i, w in enumerate(["A KING'S WARNING", "A BRUTAL WAR", "A DEAL"]):
        o = prog(t, 1.0 + i*1.1, 1.6 + i*1.1)
        b += card(260 + i*500, 860, 420, 90, o) + text(470 + i*500, 920, w, 38, CREAM, 800, op=o, ls=3)
    return fade(b, t, d, W, H)

def s3(t, d, W, H):  # unification
    b = region_bg(W, H, 0.6)
    r = random.Random(4); u = prog(t, L(3,1)+1, L(3,4)+2)
    nep = mp(NEPAL); xs = [p[0] for p in nep]; ys = [p[1] for p in nep]
    b += poly(nep, NEP, 0.25 + 0.75*u)
    def inside(x, y):
        c = False
        for (x1, y1), (x2, y2) in zip(nep, nep[1:] + nep[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
        return c
    pts = []
    while len(pts) < 34:
        x, y = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        if inside(x, y): pts.append((x, y))
    for i, (x, y) in enumerate(pts):  # rival hill states as dots that merge
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{10*(1-u)+2:.1f}" fill="{FLAG[i%5]}" opacity="{0.9*(1-u)+0.1:.2f}"/>'
    b += dot(*GORKHA, "Gorkha", prog(t, 0.6, 1.4), 16)
    yr = int(1743 + 26 * prog(t, L(3,1), L(3,4)+1.5))
    b += counter(1560, 520, str(yr), "Prithvi Narayan Shah's campaigns", prog(t, L(3,1), L(3,1)+0.6))
    k = prog(t, L(3,4), L(3,4)+1)
    b += f'<circle cx="{KTM[0]:.0f}" cy="{KTM[1]:.0f}" r="{18+30*(1-k):.0f}" fill="none" stroke="{GOLD}" stroke-width="4" opacity="{k:.2f}"/>'
    b += dot(*KTM, "Kathmandu — new capital", k, 14, dy=52)
    b += text(960, 110, "ONE COUNTRY FROM MANY HILL STATES", 54, WHITE, 900, op=prog(t, L(3,1), L(3,1)+0.8), ls=3)
    return fade(b, t, d, W, H)

def boulder(cx, cy, rx, ry, col, op=1):
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op:.2f}"/><ellipse cx="{cx-rx*0.25:.0f}" cy="{cy-ry*0.35:.0f}" rx="{rx*0.45}" ry="{ry*0.25}" fill="#FFFFFF" opacity="{0.08*op:.2f}"/>'

def s4(t, d, W, H):  # yam between two boulders
    b = bg(W, H, "night", 40, 5)
    squeeze = 40 * math.sin(clamp((t - L(4,3)) / 3) * math.pi)
    lb, rb = prog(t, L(4,2), L(4,2)+1), prog(t, L(4,2)+2.5, L(4,2)+3.5)
    b += boulder(560 + squeeze, 600, 360, 300, "#5A6577", lb) + text(560 + squeeze, 610, "QING CHINA", 52, WHITE, 900, op=lb)
    b += boulder(1360 - squeeze, 600, 360, 300, "#6E4B46", rb) + text(1360 - squeeze, 590, "EAST INDIA", 52, WHITE, 900, op=rb) + text(1360 - squeeze, 650, "COMPANY", 52, WHITE, 900, op=rb)
    y = prog(t, L(4,1), L(4,1)+0.8)
    b += f'<g transform="translate(960 600) rotate(-20) scale({0.6+0.4*y:.2f})" opacity="{y:.2f}"><ellipse rx="70" ry="120" fill="#A4673A"/><ellipse rx="70" ry="120" fill="none" stroke="#6B3F22" stroke-width="5"/><path d="M-20 -110 Q0 -170 25 -112" stroke="#2E9E5B" stroke-width="12" fill="none"/></g>'
    b += text(960, 800, "NEPAL", 44, GOLD, 900, op=y, ls=8)
    q = prog(t, L(4,1), L(4,1)+0.8)
    b += card(360, 90, 1200, 130, q) + text(960, 175, "“A yam between two boulders”", 64, WHITE, 800, op=q)
    b += text(960, 1000, "— Prithvi Narayan Shah", 40, CREAM, 500, op=q)
    b += text(960, 930, "Still quoted by Nepali leaders today", 40, GOLD, 600, op=prog(t, L(4,4), L(4,4)+0.6))
    return fade(b, t, d, W, H)

def s5(t, d, W, H):  # expansion -> collision
    b = region_bg(W, H)
    b += nepal(NEP)
    w, te = prog(t, L(5,1), L(5,1)+2), prog(t, L(5,1)+3, L(5,1)+5)
    b += poly(mp(WEST), TEAL, 0.9*w) + poly(mp(TERAI), TEAL, 0.9*te) + poly(mp(EAST), TEAL, 0.9*te)
    b += text(*P(78.9, 30.4), "Kumaon &amp; Garhwal", 34, WHITE, 700, op=w) if False else text(P(79.2,30.3)[0], P(79.2,30.3)[1], "Kumaon &amp; Garhwal", 34, WHITE, 700, op=w)
    b += text(P(82,27.4)[0], P(82,27.4)[1] + 60, "Terai plains", 34, WHITE, 700, op=te)
    c = prog(t, L(5,2), L(5,2)+1.5)
    line = mp([(80.0,28.35),(80.9,27.9),(81.8,27.4),(82.6,27.1),(83.4,27.1),(84.2,27.0),(85.2,26.8),(86.0,26.6),(87.3,26.4),(88.0,26.6)])
    b += '<path d="M' + " L".join(f"{x:.0f} {y:.0f}" for x, y in line) + f'" stroke="{RED}" stroke-width="8" fill="none" stroke-dasharray="{2000*c:.0f} 2000"/>'
    war = prog(t, L(5,3), L(5,3)+0.6)
    b += card(1260, 900, 520, 150, war, "#3A1410") + text(1520, 1000, "WAR · 1814", 80, "#FFB4A2", 900, op=war, ls=4)
    b += text(960, 110, "EXPANSION", 60, WHITE, 900, op=prog(t, 0.3, 1), ls=8)
    return fade(b, t, d, W, H)

def fort_hill(W, H):
    s = poly([(0,H),(0,820),(500,640),(800,470),(1000,440),(1150,480),(1450,660),(W,760),(W,H)], "#1B3A50")
    s += poly([(860,470),(860,400),(900,400),(900,380),(940,400),(990,400),(990,370),(1030,400),(1090,400),(1090,470)], "#3B4F5E")
    s += f'<rect x="965" y="320" width="4" height="90" fill="#C9D3DA"/>' + poly([(969,322),(1010,336),(969,350)], "#D9343A")
    return s

def s6(t, d, W, H):  # Nalapani
    b = bg(W, H, "night", 50, 7) + fort_hill(W, H)
    o1 = prog(t, L(6,1), L(6,1)+0.8)
    b += soldiers(890, 500, 24, 8, o1, GOLD, 0.9)
    b += soldiers(160, 760, 140, 20, prog(t, L(6,1)+2, L(6,1)+3), "#E07A5F", 0.9, 9)
    b += soldiers(1360, 760, 120, 20, prog(t, L(6,1)+2.4, L(6,1)+3.4), "#E07A5F", 0.9, 10)
    b += counter(960, 180, "~600", "Gorkha defenders · Capt. Balbhadra Kunwar", o1)
    b += counter(1560, 420, "~3,500", "Company troops", prog(t, L(6,1)+2, L(6,1)+3), 90, "#FFB4A2")
    g = prog(t, L(6,2), L(6,2)+0.6)
    b += card(200, 330, 620, 140, g, "#3A1410") + text(510, 390, "Day 1: Maj. Gen. Gillespie", 38, WHITE, 800, op=g) + text(510, 440, "shot and killed", 38, "#FFB4A2", 700, op=g)
    m = prog(t, L(6,3), L(6,3)+0.6)
    b += text(960, 1040, "31 Oct – 30 Nov 1814 · one month under siege", 40, CREAM, 600, op=m)
    b += text(160, 120, "NALAPANI", 60, WHITE, 900, "start", prog(t, 0.2, 0.8), 8)
    return fade(b, t, d, W, H)

def s7(t, d, W, H):  # Sugauli
    b = region_bg(W, H, india_label=False)
    lost = prog(t, L(7,1), L(7,1)+2)
    drop = 60 * prog(t, L(7,1)+2.5, L(7,1)+4)
    b += nepal(NEP)
    for reg in (WEST, TERAI, EAST):
        pts = [(x, y + drop) for x, y in mp(reg)]
        b += poly(pts, TEAL if lost < 0.5 else RED, 0.85 - 0.45*clamp(drop/60))
    b += text(1560, 980, "≈ 1/3", 110, "#FFB4A2", 900, op=lost) + text(1560, 1040, "of Nepal's territory lost", 36, CREAM, 600, op=lost)
    back = prog(t, L(7,4), L(7,4)+1)
    b += poly(mp([(84.2,27.35),(83.4,27.5),(82.7,27.5),(82.7,27.25),(83.4,27.2),(84.2,27.1)]), TEAL, back)
    b += text(1300, 250, "Part of the Terai handed back, Dec 1816", 32, GOLD, 600, op=back)
    doc = prog(t, 0.3, 1.0)
    b += card(140, 80, 760, 130, doc, "#2A2218") + text(520, 140, "TREATY OF SUGAULI", 52, GOLD, 900, op=doc, ls=4) + text(520, 190, "agreed Dec 1815 · ratified 1816", 32, CREAM, 500, op=doc)
    b += text(520, 290, "+ British resident in Kathmandu", 34, WHITE, 600, op=prog(t, L(7,3), L(7,3)+0.6))
    for i, w in enumerate(["KING ✓", "CAPITAL ✓", "INDEPENDENCE ✓"]):
        o = prog(t, L(7,5) + 1.6 + i*0.9, L(7,5) + 2.2 + i*0.9)
        b += text(560 + i*0, 960 + i*0, "", 10) + text(300 + i*400, 1000, w, 46, GOLD if i == 2 else WHITE, 900, op=o)
    return fade(b, t, d, W, H)

def s8(t, d, W, H):  # three reasons
    b = bg(W, H, "night", 40, 11)
    b += text(960, 160, "WHY NOT TAKE THE REST?", 80, WHITE, 900, op=prog(t, 0, 0.7), ls=4)
    items = [("1", "THE MOUNTAINS", "slow, costly, deadly", L(8,1)), ("2", "GOAL ACHIEVED", "lowlands + fixed border", L(8,2)), ("3", "RESPECT", "for the men who fought them", L(8,3))]
    for i, (n, h, s, at) in enumerate(items):
        o = prog(t, at, at + 0.7); x = 210 + i*520; y = 320 + 40*(1-o)
        b += card(x, y, 460, 520, o)
        b += f'<circle cx="{x+230}" cy="{y+120}" r="64" fill="{GOLD}" opacity="{o:.2f}"/>' + text(x+230, y+145, n, 70, "#0B1E33", 900, op=o, shadow=False)
        if i == 0: b += f'<g opacity="{o:.2f}">' + peak(x+230, y+230, y+420, 170, 170) + '</g>'
        if i == 1: b += f'<path d="M{x+60} {y+330} L{x+400} {y+330}" stroke="{RED}" stroke-width="10" stroke-dasharray="26 16" opacity="{o:.2f}"/>' + text(x+230, y+300, "✓", 110, GOLD, 900, op=o)
        if i == 2: b += gurkha(x+230, y+400, 1.25, o, "#9FB3C8")
        b += text(x+230, y+450, h, 42, WHITE, 900, op=o) + text(x+230, y+500, s, 30, CREAM, 500, op=o)
    return fade(b, t, d, W, H)

def s9(t, d, W, H):  # Gurkhas
    b = bg(W, H, "sky", 40, 13) + f'<circle cx="960" cy="820" r="300" fill="url(#glow)"/>'
    b += peak(300, 560, 1000, 480, 420) + peak(1620, 600, 1000, 420, 480)
    b += f'<rect x="0" y="900" width="{W}" height="{H-900}" fill="url(#fg)"/>'
    n = int(1 + 9 * prog(t, 0.5, 6))
    for i in range(n):
        b += gurkha(260 + i*160, 930, 1.3, prog(t, 0.5 + i*0.55, 1.0 + i*0.55))
    g = prog(t, L(9,1), L(9,1)+0.8)
    b += text(960, 300, "GURKHAS", 170, GOLD, 900, op=g, ls=20)
    b += text(960, 390, "recruited by Britain after the war", 46, WHITE, 600, op=g)
    return fade(b, t, d, W, H)

def s10(t, d, W, H):  # Ranas timeline
    b = bg(W, H, "night", 40, 17)
    y = 560; p = prog(t, 0.3, L(10,3)+2)
    b += f'<line x1="180" y1="{y}" x2="1740" y2="{y}" stroke="{CREAM}" stroke-width="4" opacity="0.3"/>'
    b += f'<line x1="180" y1="{y}" x2="{180+1560*p:.0f}" y2="{y}" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    ev = [(330, "1846", "Rana prime ministers take power", L(10,0)), (900, "1857", "Nepal sends troops; Gurkhas at Lucknow", L(10,2)), (1500, "1914–18", "90,000+ Gurkhas in WWI", L(10,3))]
    for i, (x, yr, s, at) in enumerate(ev):
        o = prog(t, at, at + 0.7); up = i % 2 == 0
        b += f'<circle cx="{x}" cy="{y}" r="20" fill="{GOLD}" opacity="{o:.2f}"/>'
        yy = y - 160 if up else y + 120
        b += card(x - 290, yy - 70, 580, 150, o) + text(x, yy, yr, 60, GOLD, 900, op=o) + text(x, yy + 55, s, 30, WHITE, 600, op=o)
    b += text(960, 1000, "20,000+ killed, wounded or missing", 44, "#FFB4A2", 700, op=prog(t, L(10,4), L(10,4)+0.6))
    b += text(960, 130, "FRIENDSHIP WITH BRITAIN", 64, WHITE, 900, op=prog(t, L(10,1), L(10,1)+0.7), ls=4)
    return fade(b, t, d, W, H)

def s11(t, d, W, H):  # 1923 treaty
    b = bg(W, H, "night", 30, 19)
    o = prog(t, L(11,1), L(11,1)+0.8)
    b += f'<g opacity="{o:.2f}"><rect x="560" y="{150+40*(1-o):.0f}" width="800" height="760" rx="14" fill="#EFE3C8"/>'
    for i in range(9):
        b += f'<rect x="640" y="{430+i*40}" width="{640 - (i%3)*90}" height="10" rx="5" fill="#B9A882"/>'
    b += '</g>' + text(960, 250, "TREATY OF FRIENDSHIP", 50, "#3A2A14", 900, op=o, ls=3, shadow=False)
    b += text(960, 320, "21 December 1923 · Singha Durbar", 36, "#5A4526", 600, op=o, shadow=False)
    b += text(960, 380, "O'Connor (Britain) · Chandra Shumsher Rana (Nepal)", 28, "#5A4526", 600, op=prog(t, L(11,1)+3, L(11,1)+4), shadow=False)
    s = prog(t, L(11,2), L(11,2)+0.4); sc = 1.6 - 0.6*s
    b += f'<g transform="translate(1180 800) rotate(-12) scale({sc:.2f})" opacity="{s:.2f}"><circle r="120" fill="none" stroke="#B3261E" stroke-width="10"/><circle r="100" fill="none" stroke="#B3261E" stroke-width="3"/></g>'
    b += f'<g transform="translate(1180 800) rotate(-12)" opacity="{s:.2f}">' + text(0, -10, "SOVEREIGN", 34, "#B3261E", 900, shadow=False) + text(0, 30, "INDEPENDENT", 30, "#B3261E", 900, shadow=False) + '</g>'
    b += text(960, 1010, "Celebrated with a two-day national holiday", 40, GOLD, 600, op=prog(t, L(11,3), L(11,3)+0.6))
    b += text(960, 110, "RECOGNITION", 64, WHITE, 900, op=prog(t, 0.2, 0.9), ls=8)
    return fade(b, t, d, W, H)

def s12(t, d, W, H):  # shadow of empire
    b = region_bg(W, H, india_label=False, china_label=False)
    sh = prog(t, L(12,1), L(12,1)+2)
    b += nepal(NEP)
    b += f'<ellipse cx="{1000}" cy="{900-200*sh:.0f}" rx="{1100}" ry="{520}" fill="#000" opacity="{0.55*sh:.2f}"/>'
    b += text(960, 130, "TRULY FREE?", 80, WHITE, 900, op=prog(t, 0, 0.6), ls=6)
    for i, (s, at) in enumerate([("Foreign relations: under British influence", L(12,1)), ("Weapons: limited by Britain", L(12,1)+3), ("“A glorified member of the protectorate”", L(12,2)), ("Independence paid for with soldiers?", L(12,3))]):
        o = prog(t, at, at + 0.6)
        b += card(1040, 330 + i*120, 820, 92, o) + text(1450, 390 + i*120, s, 32, WHITE if i != 2 else GOLD, 700, op=o)
    e = prog(t, L(12,4), L(12,4)+0.8)
    b += text(560, 1000, "Never a colony — but in an empire's shadow", 44, GOLD, 800, op=e)
    return fade(b, t, d, W, H)

def s13(t, d, W, H):  # ending
    b = bg(W, H, "sky", 60, 23)
    sun = prog(t, 0, 6)
    b += f'<circle cx="960" cy="{820-160*sun:.0f}" r="300" fill="url(#glow)"/><circle cx="960" cy="{820-160*sun:.0f}" r="90" fill="{GOLD}"/>'
    b += peak(320, 520, 1130, 520, 470) + peak(1600, 560, 1130, 470, 520) + peak(960, 820, 1130, 380, 380)
    b += flags(-20, 380, 720, 440, 60, 30, 14) + flags(1200, 440, 1940, 380, 60, 30, 14)
    for i, w in enumerate(["HARD MOUNTAINS", "HARD FIGHTERS", "CAREFUL DEALS"]):
        o = prog(t, 0.8 + i*0.9, 1.4 + i*0.9) * (1 - prog(t, L(13,1), L(13,1)+0.5))
        b += text(960, 200 + i*80, w, 60, WHITE if i < 2 else GOLD, 900, op=o, ls=4)
    o2 = prog(t, L(13,1), L(13,1)+0.6) * (1 - prog(t, L(13,3), L(13,3)+0.5))
    b += text(960, 260, "The yam was never crushed.", 76, GOLD, 900, op=o2)
    o3 = prog(t, L(13,3), L(13,3)+0.6) * (1 - prog(t, L(13,4), L(13,4)+0.5))
    b += card(560, 190, 800, 120, o3) + text(960, 268, "Which mattered most? Comment ↓", 46, WHITE, 800, op=o3)
    o4 = prog(t, L(13,4), L(13,4)+0.6) * (1 - prog(t, L(13,5), L(13,5)+0.5))
    b += text(960, 220, "NEXT EPISODE", 40, CREAM, 700, op=o4, ls=8) + text(960, 310, "The Gurkhas: Why Armies Feared Them", 66, WHITE, 900, op=o4)
    o5 = prog(t, L(13,5), L(13,5)+0.6)
    b += text(960, 260, "HIMALAYA", 120, WHITE, 900, op=o5, ls=10) + text(960, 350, "UNFOLDED", 64, GOLD, 300, op=o5, ls=34)
    return fade(b, t, d, W, H, fout=1.2)

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13]
LIST = [(fn, a, b) for fn, (a, b) in zip(SCENES, BOUNDS)]

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "preview":
        paths = []
        for i, (fn, a, b) in enumerate(LIST):
            ft = min(b - a - 0.5, max(BEATS[i][2][-1][0] - a + 1.5, 2))
            p = f"preview_{i:02d}.png"; preview(fn, ft, b - a, 1920, 1080, p); paths.append(p)
        contact_sheet(paths, "preview_sheet.png", cols=3, w=640)
    else:
        render_all(LIST, 1920, 1080, "main.mp4")
