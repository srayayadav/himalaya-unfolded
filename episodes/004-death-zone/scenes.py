"""Episode 004 — The Death Zone: Why Bodies Stay on Everest. Painted backgrounds + code overlays.
Look for this episode: cold blues and whites, oxygen-red warnings, gold only for key numbers.
Respect rule: no bodies are ever drawn. Climbers appear only as small living silhouettes with headlamps."""
import sys, os
sys.path.insert(0, "../../pipeline")
from epkit import *

ICE = "#BFE3F2"; ORED = "#E0533D"; NEP = "#2F6A7A"
PZ = projector(84.6, 26.4, 89.2, 29.6, 60, 150, 1860, 1050)
EV = PZ(86.925, 27.988)

def climber(x, y, s=1.0, t=0, lamp=True, op=1):
    """Tiny living climber silhouette with pack (and headlamp)."""
    st = math.sin(t * 6) * 6
    g = (f'<g opacity="{op:.2f}" transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
         f'<path d="M-8 -40 L8 -40 L10 -8 L-10 -8Z" fill="#20160F"/><rect x="-14" y="-38" width="10" height="26" rx="3" fill="#C8553D"/>'
         f'<circle cx="2" cy="-48" r="8" fill="#20160F"/>'
         f'<path d="M-6 -8 L{-8+st:.0f} 14 M6 -8 L{8-st:.0f} 14" stroke="#20160F" stroke-width="5"/>'
         f'<path d="M10 -32 L22 6" stroke="#5A4A3A" stroke-width="3"/>')
    if lamp:
        g += '<circle cx="9" cy="-49" r="3.5" fill="#FFF6D0"/><circle cx="9" cy="-49" r="12" fill="#FFF6D0" opacity="0.35"/>'
    return g + '</g>'

def queue(t, pts, n, s=0.8, speed=0.02, lamp=True, op=1):
    """n climbers spaced along a polyline, creeping forward slowly."""
    segs = list(zip(pts, pts[1:])); lens = [math.dist(a, b) for a, b in segs]; tot = sum(lens)
    out = ""
    for i in range(n):
        u = ((i / n) + t * speed) % 1 * tot
        for (a, b), l in zip(segs, lens):
            if u <= l:
                k = u / l; out += climber(a[0] + (b[0]-a[0])*k, a[1] + (b[1]-a[1])*k, s, t + i, lamp, op); break
            u -= l
    return out

def wind(t, op=0.5, seed=3, y0=200, y1=700):
    r = random.Random(seed); s = ""
    for i in range(26):
        y = r.uniform(y0, y1); sp = r.uniform(500, 900); L_ = r.uniform(120, 320)
        x = (r.uniform(0, 2400) + t * sp) % 2400 - 300
        s += f'<path d="M{x:.0f} {y:.0f} l{L_:.0f} {-L_*0.08:.0f}" stroke="#FFFFFF" stroke-width="{r.uniform(1.5,3):.1f}" opacity="{op*r.uniform(0.3,0.8):.2f}" stroke-linecap="round"/>'
    return s

def snow(t, op=0.7, n=70, seed=8):
    r = random.Random(seed); s = ""
    for i in range(n):
        x = (r.uniform(0, 1920) + t * r.uniform(150, 420)) % 1920; y = (r.uniform(0, 1080) + t * r.uniform(40, 120)) % 1080
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,3.5):.1f}" fill="#fff" opacity="{op*r.uniform(0.3,0.9):.2f}"/>'
    return s

def bar(x, y, w, h, frac, col, op=1, bgc="#0B1E33"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{bgc}" opacity="{0.7*op:.2f}"/>'
            f'<rect x="{x}" y="{y}" width="{max(h, w*frac):.0f}" height="{h}" rx="{h/2:.0f}" fill="{col}" opacity="{op:.2f}"/>')

# ---------------- scenes ----------------
RIDGE = [(-60, 760), (300, 700), (620, 640), (900, 560), (1180, 470), (1450, 380)]
def s0(t, d, W, H):  # hook
    b = DEFS + PAINT("d_hook") + shade(0.35) + wind(t, 0.45)
    b += queue(t, RIDGE, 7, 0.9, 0.006, True, prog(t, 0.3, 1.5))
    o1 = inout(t, L(0, 0) + 1.5, L(0, 1) - 0.3)
    # the landmark is shown only as a small marker, never as a person
    mx, my = 1180, 520
    b += f'<circle cx="{mx}" cy="{my}" r="{24 + 6*math.sin(t*3):.0f}" fill="none" stroke="#3FBF6A" stroke-width="5" opacity="{o1:.2f}"/>'
    b += chip(mx, my - 70, "“GREEN BOOTS”", o1, 40, "#8FE0A8")
    o2 = inout(t, L(0, 1), L(0, 2) - 0.3)
    b += chip(960, 200, "1996 → still on the mountain for decades", o2, 42)
    o3 = prog(t, L(0, 2), L(0, 2) + 0.7)
    b += dim(0.35 * o3) + text(960, 300, "HE IS NOT ALONE", 110, WHITE, 900, op=o3, ls=6)
    return fade(b, t, d, W, H, fin=0.8)

def s1(t, d, W, H):  # title
    b = DEFS + PAINT("d_title") + shade(0.55) + wind(t, 0.35, 5, 100, 500)
    b += text(960, 330, "THE DEATH ZONE", 150, WHITE, 900, op=prog(t, 0, 0.7), ls=8)
    b += text(960, 430, "WHY BODIES STAY ON EVEREST", 58, ICE, 800, op=prog(t, 0.5, 1.2), ls=8)
    b += f'<rect x="760" y="470" width="400" height="6" fill="{ORED}" opacity="{prog(t, 1, 1.8):.2f}"/>'
    return fade(b, t, d, W, H)

def s2(t, d, W, H):  # map + height + names
    om = prog(t, 0, 0.8)
    b = '<rect width="1920" height="1080" fill="#0E2A40"/>'
    for c in ("India", "Bhutan", "Bangladesh"): b += country_path(c, PZ, "#2B2A3F", om)
    b += country_path("China", PZ, "#24324A", om) + country_path("Nepal", PZ, NEP, om, "#E8F1F5", 2.5)
    b += text(400, 560, "NEPAL", 60, WHITE, 900, op=om, ls=8) + text(1400, 300, "CHINA (TIBET)", 46, "#9FB3C8", 800, op=om, ls=8)
    ex, ey = EV
    o1 = prog(t, 0.8, 1.6)
    b += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{36 + 10*math.sin(t*3):.0f}" fill="none" stroke="{GOLD}" stroke-width="4" opacity="{o1*0.8:.2f}"/>'
    b += peak(ex, ey - 120 * o1, ey + 8, 70, 70, "#9FC3D6", "#5E8AA2", 0.45, 7) if o1 > 0 else ""
    b += text(ex, ey + 70, "MOUNT EVEREST", 40, WHITE, 900, op=o1)
    o2 = prog(t, L(2, 1), L(2, 1) + 0.6) * (1 - prog(t, L(2, 2), L(2, 2) + 0.4))
    h = 8848.86 * prog(t, L(2, 1) + 0.5, L(2, 1) + 4)
    b += card(1150, 560, 640, 220, o2) + text(1470, 680, f"{h:,.2f} m", 92, GOLD, 900, op=o2) + text(1470, 740, "official height · Nepal & China, 2020", 30, CREAM, 600, op=o2)
    o3 = prog(t, L(2, 2), L(2, 2) + 0.6)
    b += card(1150, 520, 640, 300, o3) + text(1470, 610, "SAGARMATHA", 66, GOLD, 900, op=o3) + text(1470, 655, "Nepali", 28, CREAM, 600, op=o3)
    o4 = prog(t, L(2, 2) + 2.2, L(2, 2) + 2.8)
    b += text(1470, 740, "CHOMOLUNGMA", 60, ICE, 900, op=o4) + text(1470, 785, "Tibetan · “Goddess Mother of the World”", 28, CREAM, 600, op=o4)
    return fade(b, t, d, W, H)

def s3(t, d, W, H):  # the death zone line + oxygen
    b = DEFS + PAINT("d_deathzone") + dim(0.35) + wind(t, 0.3)
    # altitude axis on the left
    oa = prog(t, 0.2, 1.0)
    y_of = lambda m: 1000 - m / 9000 * 860
    b += f'<path d="M180 {y_of(0):.0f} L180 {y_of(9000):.0f}" stroke="#FFFFFF" stroke-width="4" opacity="{oa:.2f}"/>'
    for m in range(0, 9001, 2000):
        b += f'<path d="M168 {y_of(m):.0f} L192 {y_of(m):.0f}" stroke="#fff" stroke-width="3" opacity="{oa:.2f}"/>' + text(150, y_of(m) + 10, f"{m:,} m", 26, WHITE, 600, "end", oa)
    oz = prog(t, L(3, 0), L(3, 0) + 1.0)
    b += f'<rect x="180" y="{y_of(9000):.0f}" width="1740" height="{y_of(8000)-y_of(9000):.0f}" fill="{ORED}" opacity="{0.28*oz:.2f}"/>'
    b += f'<path d="M180 {y_of(8000):.0f} L1920 {y_of(8000):.0f}" stroke="{ORED}" stroke-width="5" stroke-dasharray="20 12" opacity="{oz:.2f}"/>'
    b += text(1000, y_of(8000) - 40, "THE DEATH ZONE · above ~8,000 m", 54, WHITE, 900, op=oz)
    o1 = inout(t, L(3, 1), L(3, 2) - 0.2)
    b += card(560, 420, 900, 230, o1) + text(1010, 520, "Dr Edouard Wyss-Dunant · 1953", 48, GOLD, 800, op=o1) + text(1010, 590, "wrote of a “lethal zone”", 38, CREAM, 600, op=o1)
    o2 = prog(t, L(3, 2), L(3, 2) + 0.6)
    k = prog(t, L(3, 2) + 0.8, L(3, 2) + 3)
    b += text(540, 520, "SEA LEVEL", 36, WHITE, 800, "start", o2) + bar(540, 540, 1100, 56, 1.0, ICE, o2)
    b += text(540, 680, "SUMMIT", 36, WHITE, 800, "start", o2) + bar(540, 700, 1100, 56, 1 - (1 - 0.31) * k, ORED, o2)
    b += text(1660, 745, "less than ⅓", 40, ORED, 900, "start", o2 * prog(t, L(3, 2) + 3, L(3, 2) + 3.6))
    b += text(1090, 860, "oxygen pressure in each breath", 32, CREAM, 600, op=o2)
    o3 = prog(t, L(3, 3), L(3, 3) + 0.6)
    b += chip(1090, 960, "The body cannot adapt up here", o3, 40, GOLD)
    return fade(b, t, d, W, H)

def body_outline(x, y, s, op, hl_lung=0, hl_brain=0, hl_hands=0):
    g = f'<g opacity="{op:.2f}" transform="translate({x} {y}) scale({s})" fill="none" stroke="{ICE}" stroke-width="5">'
    g += '<circle cx="0" cy="-260" r="62"/><path d="M-40 -195 L-110 -170 L-150 40 M40 -195 L110 -170 L150 40 M-90 -170 L-80 120 L-60 330 M90 -170 L80 120 L60 330 M-80 120 L80 120"/>'
    g += '</g>'
    g += f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<ellipse cx="-38" cy="-80" rx="34" ry="70" fill="{ORED}" opacity="{0.75*hl_lung:.2f}"/><ellipse cx="38" cy="-80" rx="34" ry="70" fill="{ORED}" opacity="{0.75*hl_lung:.2f}"/>'
    g += f'<circle cx="0" cy="-262" r="44" fill="{ORED}" opacity="{0.75*hl_brain:.2f}"/>'
    g += f'<circle cx="-150" cy="48" r="20" fill="{ICE}" opacity="{hl_hands:.2f}"/><circle cx="150" cy="48" r="20" fill="{ICE}" opacity="{hl_hands:.2f}"/>'
    g += f'<circle cx="-60" cy="340" r="20" fill="{ICE}" opacity="{hl_hands:.2f}"/><circle cx="60" cy="340" r="20" fill="{ICE}" opacity="{hl_hands:.2f}"/></g>'
    return g

def gauge(cx, cy, r, frac, op, lab):
    a0, a1 = math.pi, 2 * math.pi
    def P(a, rr): return cx + rr * math.cos(a), cy + rr * math.sin(a)
    s = f'<g opacity="{op:.2f}">'
    for k, col in enumerate(["#7A1F2B", ORED, "#E7A26A", "#7FBF8F"]):
        x0, y0 = P(a0 + (a1 - a0) * k / 4, r); x1, y1 = P(a0 + (a1 - a0) * (k + 1) / 4, r)
        s += f'<path d="M{x0:.0f} {y0:.0f} A{r} {r} 0 0 1 {x1:.0f} {y1:.0f}" stroke="{col}" stroke-width="34" fill="none"/>'
    a = a0 + (a1 - a0) * frac; nx, ny = P(a, r - 40)
    s += f'<path d="M{cx} {cy} L{nx:.0f} {ny:.0f}" stroke="#fff" stroke-width="8" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="16" fill="#fff"/>'
    return s + text(cx, cy + 70, lab, 32, CREAM, 600) + '</g>'

def s4(t, d, W, H):  # what happens to the body
    b = DEFS + PAINT("d_deathzone") + dim(0.55) + snow(t, 0.5)
    o0 = prog(t, 0.2, 1.0)
    b += chip(960, 130, "BLOOD SAMPLES AT ~8,400 m · study published 2009", o0 * (1 - prog(t, L(4, 2), L(4, 2) + 0.5)), 36)
    k = prog(t, L(4, 0) + 2, L(4, 1) + 2)
    frac = 0.92 - (0.92 - 0.12) * k
    b += gauge(1380, 560, 260, frac, inout(t, L(4, 0) + 1, L(4, 2)), "blood oxygen")
    b += text(1120, 640, "normal", 28, "#7FBF8F", 700, op=inout(t, L(4, 0) + 1, L(4, 2)))
    o1 = inout(t, L(4, 1), L(4, 2))
    b += chip(1380, 780, "levels seen in patients close to death", o1, 34, ORED)
    o2 = prog(t, L(4, 2), L(4, 2) + 0.6)
    b += body_outline(560, 560, 1.0, o2, prog(t, L(4, 2) + 1.5, L(4, 2) + 2.2), prog(t, L(4, 2) + 2.5, L(4, 2) + 3.2), prog(t, L(4, 2) + 5.5, L(4, 2) + 6.2))
    for k_, (s_, yy, a) in enumerate([("fluid in the lungs", 470, 1.5), ("fluid on the brain", 300, 2.5), ("judgement fails", 380, 4.0), ("frozen fingers & toes", 620, 5.5)]):
        b += chip(1260, yy + 80, s_, o2 * prog(t, L(4, 2) + a, L(4, 2) + a + 0.5) * (1 - prog(t, L(4, 3), L(4, 3) + 0.4)), 36, WHITE, 520)
    o3 = prog(t, L(4, 3), L(4, 3) + 0.6)
    # oxygen bottle
    b += f'<g opacity="{o3:.2f}" transform="translate(1380 520)"><rect x="-60" y="-200" width="120" height="380" rx="56" fill="{ORED}"/><rect x="-24" y="-250" width="48" height="56" fill="#C9CFD6"/><rect x="-60" y="-80" width="120" height="40" fill="#F3DCC0" opacity="0.8"/></g>'
    b += chip(1380, 820, "every hour counts", o3, 44, GOLD)
    return fade(b, t, d, W, H)

def s5(t, d, W, H):  # the numbers
    b = DEFS + PAINT("d_basecamp") + dim(0.68)
    o1 = prog(t, 0.2, 1.0)
    b += counter_text(520, 300, countup(t, 0.3, 3.0, 339), "deaths on Everest, to 2025", o1, 140, ORED)
    o2 = prog(t, L(5, 1), L(5, 1) + 0.6)
    b += counter_text(1400, 300, countup(t, L(5, 1), L(5, 1) + 3, 13700) + "+", "summits", o2, 140, GOLD)
    o2b = inout(t, L(5, 2), L(5, 3) - 0.2)
    b += chip(520, 470, "229 Nepal side · 110 Tibet side", o2b, 34)
    o3 = inout(t, L(5, 3), L(5, 4) - 0.2)
    b += chip(960, 520, "≈ 1 death per 100 summits", o3, 50, WHITE)
    for i in range(100):
        x = 560 + (i % 25) * 32; y = 640 + (i // 25) * 44
        b += f'<circle cx="{x}" cy="{y}" r="11" fill="{ORED if i == 37 else ICE}" opacity="{o3*(0.95 if i==37 else 0.55):.2f}"/>'
    o4 = prog(t, L(5, 4), L(5, 4) + 0.6)
    causes = [("Avalanches", 1.0), ("Falls", 0.99), ("Altitude sickness", 0.61), ("Exhaustion", 0.41), ("Cold & exposure", 0.33)]
    for k, (nm, f) in enumerate(causes):
        ok = o4 * prog(t, L(5, 4) + k * 0.5, L(5, 4) + k * 0.5 + 0.5)
        b += text(760, 560 + k * 90, nm, 36, WHITE, 700, "end", ok) + bar(790, 530 + k * 90, 820, 40, f, ORED if k < 2 else "#E7A26A", ok)
    b += text(1200, 1030, "main causes of death (Himalayan Database, approximate share)", 26, CREAM, 500, op=o4 * 0.85)
    return fade(b, t, d, W, H)

def icon(kind, x, y, op, t):
    s = f'<g opacity="{op:.2f}" transform="translate({x} {y})">'
    if kind == "weight":
        s += '<path d="M-70 40 L70 40 L50 -40 L-50 -40Z" fill="#C9CFD6"/><circle cy="-56" r="18" fill="none" stroke="#C9CFD6" stroke-width="8"/>' + text(0, 22, "100+ kg", 30, "#0B1E33", 900, shadow=False)
    elif kind == "ice":
        s += '<path d="M-60 -50 L60 -50 L70 50 L-70 50Z" fill="#9FD3EA" opacity="0.9"/><path d="M-40 -30 L20 -40 M-30 10 L40 0" stroke="#fff" stroke-width="5"/>'
    elif kind == "time":
        s += '<circle r="60" fill="none" stroke="#fff" stroke-width="8"/>' + f'<path d="M0 0 L0 -44" stroke="#fff" stroke-width="7" transform="rotate({t*90:.0f})"/><path d="M0 0 L30 0" stroke="{GOLD}" stroke-width="7"/>'
    elif kind == "weather":
        s += '<ellipse cx="-10" cy="-10" rx="60" ry="34" fill="#C9CFD6"/>' + "".join(f'<path d="M{-40+i*25} 30 l-10 26" stroke="#fff" stroke-width="5"/>' for i in range(4))
    elif kind == "cost":
        s += f'<rect x="-34" y="-70" width="68" height="140" rx="30" fill="{ORED}"/>' + text(0, 20, "$", 60, "#fff", 900, shadow=False)
    elif kind == "danger":
        s += f'<path d="M0 -66 L66 54 L-66 54Z" fill="none" stroke="{GOLD}" stroke-width="9"/>' + text(0, 40, "!", 70, GOLD, 900, shadow=False)
    return s + '</g>'

def s6(t, d, W, H):  # why bodies stay: six reasons
    b = DEFS + PAINT("d_icefall") + dim(0.5) + snow(t, 0.4)
    o0 = inout(t, 0.2, L(6, 1) + 0.5)
    b += text(960, 520, "Why aren't they brought down?", 80, WHITE, 900, op=o0)
    items = [("weight", "WEIGHT", "100+ kg · carry limit up here ~25 kg"),
             ("ice", "ICE", "11 hours to free one body"),
             ("time", "TIME", "24 hours to move one body 3.5 km"),
             ("weather", "WEATHER", "good windows: ~2 weeks a year"),
             ("cost", "COST", "~$20,000 of oxygen for one recovery"),
             ("danger", "DANGER", "1984: two men died trying")]
    for k, (ic, nm, sub) in enumerate(items):
        a = L(6, k + 1)
        ok = prog(t, a, a + 0.6)
        col, row = k % 3, k // 3
        x = 330 + col * 630; y = 230 + row * 420
        active = a <= t < (L(6, k + 2) if k < 5 else d)
        hl = 1.0 if active else 0.55
        b += card(x - 290, y - 120, 580, 360, ok * hl) + icon(ic, x, y, ok * hl, t)
        b += text(x, y + 120, nm, 50, GOLD if active else WHITE, 900, op=ok * hl)
        b += text(x, y + 175, sub, 25 if len(sub) > 36 else 28, CREAM, 600, op=ok * hl)
    return fade(b, t, d, W, H)

def s7(t, d, W, H):  # Green Boots — marker only, never the body
    b = DEFS + PAINT("d_northridge") + shade(0.4) + wind(t, 0.3)
    b += queue(t, [(-60, 900), (500, 760), (900, 640), (1300, 520), (1700, 380)], 6, 0.8, 0.005, True, prog(t, 0.2, 1.2) * (1 - prog(t, L(7, 3), L(7, 3) + 1)))
    mx, my = 1080, 600
    o1 = prog(t, L(7, 1), L(7, 1) + 0.6)
    b += f'<circle cx="{mx}" cy="{my}" r="{30 + 8*math.sin(t*3):.0f}" fill="none" stroke="#3FBF6A" stroke-width="5" opacity="{o1:.2f}"/>'
    b += chip(mx, my - 80, "rock alcove · ~8,500 m", o1 * (1 - prog(t, L(7, 4), L(7, 4) + 0.5)), 36)
    b += chip(420, 160, "NORTHEAST RIDGE", prog(t, 0.3, 1.0), 40)
    o2 = inout(t, L(7, 2), L(7, 3))
    b += chip(960, 960, "used by climbers as a marker", o2, 38)
    o3 = prog(t, L(7, 3), L(7, 3) + 0.6)
    b += chip(1500, 300, "2014: reportedly moved out of view", o3 * (1 - prog(t, L(7, 4), L(7, 4) + 0.5)), 36)
    o4 = prog(t, L(7, 4), L(7, 4) + 0.8)
    b += dim(0.45 * o4) + card(360, 330, 1200, 380, o4)
    b += text(960, 420, "2026 · DNA TEST", 40, CREAM, 800, op=o4, ls=6) + text(960, 520, "Lance Naik Dorje Morup", 78, GOLD, 900, op=o4)
    b += text(960, 600, "Indo-Tibetan Border Police · 1996 expedition", 36, WHITE, 600, op=o4)
    o5 = prog(t, L(7, 5), L(7, 5) + 0.6)
    b += text(960, 670, "India plans to bring him home", 40, ICE, 800, op=o5)
    return fade(b, t, d, W, H)

def s8(t, d, W, H):  # Mallory & Irvine 1924
    b = DEFS + PAINT("d_rongbuk") + shade(0.45)
    o1 = prog(t, L(8, 1), L(8, 1) + 0.8)
    climb = prog(t, L(8, 1), L(8, 1) + 7)
    fadeup = 1 - prog(t, L(8, 1) + 5, L(8, 1) + 7.5)
    for k, (nm, xo) in enumerate([("George Mallory", 0), ("Andrew Irvine", -150)]):
        x = 700 + 600 * climb + xo; y = 900 - 380 * climb + (40 if k else 0)
        b += warm(character(x, y + bob(t + k, 0 < climb < 1, 4), 0.38 - 0.12 * climb, MOUNTAINEER_1924, t + k, op=o1 * fadeup))
        b += label(x, y + 70, nm, o1 * fadeup * (1 - prog(t, L(8, 1) + 3, L(8, 1) + 4)), 380, 28)
    b += clouds(1920, 360, 6, 4, 0.5 * prog(t, L(8, 1) + 4, L(8, 1) + 7), "#E8EEF2", t * 30)
    b += chip(960, 140, "JUNE 1924", prog(t, L(8, 1), L(8, 1) + 0.6), 50, GOLD)
    o2 = prog(t, L(8, 2), L(8, 2) + 0.6)
    b += chip(460, 360, "1999: Mallory found", o2, 40)
    o3 = prog(t, L(8, 3), L(8, 3) + 0.6)
    b += chip(460, 480, "2024: a boot on the glacier", o3, 40)
    # sock label card (just text, no remains drawn)
    o3b = prog(t, L(8, 3) + 3, L(8, 3) + 3.6)
    b += f'<g opacity="{o3b:.2f}" transform="translate(1420 560) rotate(-4)"><rect x="-220" y="-70" width="440" height="140" rx="8" fill="#F3EBDD" stroke="#B59B72" stroke-width="4"/>' + text(0, 22, "A.C. IRVINE", 64, "#7A1F2B", 900, shadow=False) + '</g>'
    o4 = prog(t, L(8, 4), L(8, 4) + 0.6)
    b += dim(0.75 * o4) + text(960, 560, "?", 340, GOLD, 900, op=o4) + text(960, 700, "Did they reach the top in 1924?", 56, WHITE, 800, op=o4)
    return fade(b, t, d, W, H)

def s9(t, d, W, H):  # clean-up campaigns
    b = DEFS + PAINT("d_southcol") + shade(0.5)
    rows = [("2019", "4 bodies", "11 tonnes of rubbish", 1), ("2024", "4 bodies + 1 skeleton", "~11 tonnes of waste", 2)]
    for k, (yr, a_, b_, li) in enumerate(rows):
        ok = prog(t, L(9, li), L(9, li) + 0.6)
        y = 260 + k * 230
        b += card(260, y - 90, 1400, 190, ok) + text(400, y + 30, yr, 80, GOLD, 900, op=ok) + text(1000, y, a_, 50, WHITE, 800, op=ok) + text(1000, y + 60, b_, 38, CREAM, 600, op=ok)
    o3 = prog(t, L(9, 3), L(9, 3) + 0.6)
    b += chip(960, 760, "melting ice is exposing more · Khumbu Icefall · South Col", o3 * (1 - prog(t, L(9, 4), L(9, 4) + 0.5)), 34)
    o4 = prog(t, L(9, 4), L(9, 4) + 0.6)
    b += card(360, 690, 1200, 200, o4) + text(960, 780, "2019 – 2024 · four campaigns", 40, CREAM, 700, op=o4) + text(960, 850, "12 bodies · ~180 tonnes of rubbish", 56, GOLD, 900, op=o4)
    return fade(b, t, d, W, H)

def s10(t, d, W, H):  # crowds
    b = DEFS + PAINT("d_hook") + shade(0.3) + wind(t, 0.25)
    n = 12 + int(18 * prog(t, 0, L(10, 2)))
    b += queue(t, RIDGE, n, 0.75, 0.003, True, prog(t, 0.2, 1.0))
    o1 = prog(t, L(10, 1), L(10, 1) + 0.6) * (1 - prog(t, L(10, 2), L(10, 2) + 0.4))
    b += card(1150, 560, 640, 240, o1) + text(1470, 680, countup(t, L(10, 1) + 0.5, L(10, 1) + 3, 1008), 120, GOLD, 900, op=o1) + text(1470, 750, "summits · spring 2026 (record)", 32, CREAM, 600, op=o1)
    o2 = prog(t, L(10, 2), L(10, 2) + 0.6) * (1 - prog(t, L(10, 3), L(10, 3) + 0.4))
    b += chip(1470, 680, "May 2019 · the queue photo · 11 deaths", o2, 34)
    o3 = prog(t, L(10, 3), L(10, 3) + 0.6)
    b += chip(1400, 680, "waiting in the death zone", o3, 44, ORED)
    return fade(b, t, d, W, H)

def s11(t, d, W, H):  # puja + ending
    first = DEFS + PAINT("d_basecamp") + shade(0.3)
    first += flags(-20, 380, 1940, 330, 120, 40, 34, 5) + flags(200, 520, 1700, 470, 80, 30, 26, 6)
    first += smoke(980, 840, t, 3, 0.55) + smoke(1010, 850, t + 1.7, 4, 0.45)
    first += f'<rect x="900" y="820" width="180" height="70" rx="8" fill="#7A6A55"/>'
    first += chip(960, 160, "PUJA AT BASE CAMP", prog(t, 0.3, 1.0), 46, GOLD)
    second = DEFS + PAINT("d_end") + shade(0.7)
    b = crossfade(t, L(11, 1) + 2.5, 1.5, first, second)
    o1 = inout(t, L(11, 2), L(11, 3) - 0.2)
    b += text(960, 260, "The hardest part of Everest", 70, WHITE, 900, op=o1) + text(960, 360, "is getting back down.", 70, GOLD, 900, op=o1 * prog(t, L(11, 2) + 3, L(11, 2) + 3.6))
    o2 = inout(t, L(11, 3), L(11, 4) - 0.2)
    b += card(470, 210, 980, 130, o2) + text(960, 295, "Would you climb into the death zone? ↓", 46, WHITE, 800, op=o2)
    o3 = inout(t, L(11, 4), L(11, 5) - 0.2)
    b += text(960, 220, "NEXT EPISODE", 40, CREAM, 700, op=o3, ls=8) + text(960, 320, "Lukla: The World's Most Dangerous Airport?", 62, WHITE, 900, op=o3)
    o4 = prog(t, L(11, 5), L(11, 5) + 0.6)
    b += text(960, 300, "HIMALAYA", 120, WHITE, 900, op=o4, ls=10) + text(960, 390, "UNFOLDED", 64, GOLD, 300, op=o4, ls=34)
    return fade(b, t, d, W, H, fout=1.2)

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]

if __name__ == "__main__":
    main(SCENES, "death_zone")
