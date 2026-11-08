"""Episode 003 — The Gurkhas: Why Armies Feared Them. Painted backgrounds + animated code characters.
Look for this episode: green-and-khaki palette, gold accents, low warm sun; maps in deep teal."""
import sys, os
sys.path.insert(0, "../../pipeline")
from epkit import *

KHAKI = "#B9A576"; RED = "#C8553D"; NEP = "#2F6A7A"
PZ = projector(79.5, 25.6, 89.0, 31.2, 60, 150, 1860, 1050)

def khukuri(x, y, s=1.0, rot=-20, op=1, sheath=False):
    """Khukuri (checked against a real photo, 9 Nov 2026): blade bends DOWN at an 'elbow', spine is the
    outer convex curve, edge is the inner side with a wide belly near the tip, cho notch at the base of
    the edge, brass bolster, wooden handle with rings and a flared butt."""
    blade = ('<path d="M0 0 C70 -12 140 -12 190 14 C250 44 305 100 352 168 C320 188 268 208 222 186 '
             'C182 162 148 96 100 64 C80 54 60 50 40 48 L34 40 L30 47 L25 38 L20 47 L16 40 L0 36Z" '
             'fill="#D9DEE3" stroke="#6C7680" stroke-width="3" stroke-linejoin="round"/>'
             '<path d="M18 10 C80 2 140 4 186 30" stroke="#5F6973" stroke-width="5" fill="none" stroke-linecap="round"/>'
             '<path d="M200 44 C245 76 290 120 334 166" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.7"/>')
    handle = ('<path d="M-4 -2 L-34 -6 L-34 42 L-4 38Z" fill="#C9A04A" stroke="#7A5A1A" stroke-width="3"/>'
              '<path d="M-34 -4 C-80 -8 -120 -4 -150 -16 L-176 -26 L-182 62 L-150 54 '
              'C-120 44 -80 46 -34 40Z" fill="#6B3420" stroke="#3E1E12" stroke-width="3"/>'
              '<path d="M-150 -16 L-150 54 M-140 -12 L-140 50 M-60 -4 L-60 42" stroke="#3E1E12" stroke-width="4"/>'
              '<path d="M-60 2 C-90 -2 -120 0 -145 -8" stroke="#9A5634" stroke-width="5" fill="none" opacity="0.6"/>')
    return f'<g opacity="{op:.2f}" transform="translate({x:.0f} {y:.0f}) rotate({rot}) scale({s:.3f})">{handle}{blade}</g>'

def nepal_map(op=1):
    s = '<rect width="1920" height="1080" fill="#0E2A40"/>'
    for c in ("China", "India", "Bhutan", "Bangladesh"):
        s += country_path(c, PZ, "#24324A" if c == "China" else "#2B2A3F", 0.95 * op)
    s += country_path("Nepal", PZ, NEP, op, "#E8F1F5", 2.5)
    s += text(1600, 300, "CHINA (TIBET)", 38, "#9FB3C8", 800, op=0.6 * op, ls=8, shadow=False)
    s += text(560, 1000, "INDIA", 38, "#C9A9A0", 800, op=0.6 * op, ls=8, shadow=False)
    return s

def dot(xy, name, op, dy=-30, size=36, col=GOLD):
    x, y = xy
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{col}" opacity="{op:.2f}"/>' + text(x, y + dy, name, size, WHITE, 800, op=op)

# ---------------- scenes ----------------
def s0(t, d, W, H):  # hook: the quote on a misty ridge
    b = DEFS + PAINT("g_hook") + shade(0.55)
    x = walk_x(t, 0.3, 2100, 1450, 3.5)
    b += ground_shadow(x, 905, 70) + warm(character(x, 880, 0.55, GURKHA, t, flip=True, gesture=0.0) )
    q1 = inout(t, 0.2, L(0, 2) - 0.4)
    b += text(860, 330, "“If a man says he is not afraid of dying,", 58, WHITE, 700, op=prog(t, L(0, 1), L(0, 1) + 0.6) * q1)
    b += text(860, 420, "he is either lying, or he is a Gurkha.”", 58, GOLD, 800, op=prog(t, L(0, 1) + 2.4, L(0, 1) + 3.0) * q1)
    b += text(860, 500, "— often attributed to Field Marshal Sam Manekshaw", 30, CREAM, 500, op=q1 * prog(t, L(0, 1) + 3, L(0, 1) + 4))
    o2 = prog(t, L(0, 2), L(0, 2) + 0.6)
    b += text(760, 330, "200+ YEARS", 120, GOLD, 900, op=o2 * (1 - prog(t, L(0, 3), L(0, 3) + 0.4))) + text(760, 400, "in Britain's wars", 44, CREAM, 600, op=o2 * (1 - prog(t, L(0, 3), L(0, 3) + 0.4)))
    o3 = prog(t, L(0, 3), L(0, 3) + 0.6)
    for i in range(13):
        mx = 330 + (i % 7) * 140 + (70 if i >= 7 else 0); my = 330 + (i // 7) * 200
        b += medal(mx, my, 0.7, o3 * prog(t, L(0, 3) + i * 0.18, L(0, 3) + i * 0.18 + 0.3))
    b += text(760, 760, "13 VICTORIA CROSSES · NEPALI GURKHAS", 44, WHITE, 800, op=o3)
    return fade(b, t, d, W, H, fin=0.8)

def s1(t, d, W, H):  # title
    b = DEFS + PAINT("g_title") + shade(0.6)
    b += text(960, 360, "THE GURKHAS", 150, WHITE, 900, op=prog(t, 0, 0.7), ls=10)
    b += text(960, 470, "WHY ARMIES FEARED THEM", 60, GOLD, 800, op=prog(t, 0.5, 1.2), ls=10)
    b += khukuri(960 - 180, 600, 1.0, -8, prog(t, 1.0, 1.8))
    b += flags(200, 120, 1720, 140, 60, 34, 22) if t > 0 else ""
    return fade(b, t, d, W, H)

def s2(t, d, W, H):  # map: Gorkha, Kathmandu 1768, hill people, khukuri
    b = nepal_map(prog(t, 0, 0.8))
    G, K = PZ(84.63, 28.0), PZ(85.32, 27.7)
    og = prog(t, 0.5, 1.2)
    b += f'<circle cx="{G[0]:.0f}" cy="{G[1]:.0f}" r="{40 + 14*math.sin(t*3):.0f}" fill="none" stroke="{GOLD}" stroke-width="4" opacity="{og*0.7:.2f}"/>'
    b += dot(G, "GORKHA", og)
    ok = prog(t, L(2, 1) + 3, L(2, 1) + 4)
    gx, gy = G; kx, ky = K; k = prog(t, L(2, 1) + 3, L(2, 1) + 6)
    b += f'<path d="M{gx:.0f} {gy:.0f} Q{(gx+kx)/2:.0f} {gy-120:.0f} {gx + (kx-gx)*k:.0f} {gy + (ky-gy)*k - 120*4*k*(1-k)*0:.0f}" stroke="{RED}" stroke-width="7" fill="none" stroke-dasharray="18 12" opacity="{ok:.2f}"/>'
    b += dot(K, "KATHMANDU", prog(t, L(2, 1) + 5, L(2, 1) + 6), dy=60) + chip(kx + 220, ky + 10, "1768", prog(t, L(2, 1) + 6, L(2, 1) + 7), 44, GOLD)
    oc = prog(t, L(2, 1), L(2, 1) + 0.8)
    b += warm(character(260, 900, 0.5, PRITHVI_NARAYAN, t, talking=False, gesture=0.5 * oc, op=oc)) + label(260, 980, "Prithvi Narayan Shah", oc, 420, 28)
    oh = prog(t, L(2, 2), L(2, 2) + 0.8) * (1 - prog(t, L(2, 3) + 3, L(2, 3) + 4))
    for i in range(3):
        x = walk_x(t, L(2, 2) + i * 0.4, 1950 + i * 120, 1300 + i * 170, 3)
        b += warm(character(x, 880 + bob(t + i, True), 0.42, GURKHA, t + i, flip=True, op=oh))
    b += chip(1500, 620, "HILL FARMERS & HERDERS", oh * (1 - prog(t, L(2, 3), L(2, 3) + 0.4)), 34)
    okh = prog(t, L(2, 3), L(2, 3) + 0.8)
    b += khukuri(1250, 420, 1.1, -10 + 6 * math.sin(t), okh) + chip(1450, 620, "THE KHUKURI", okh, 40, GOLD)
    return fade(b, t, d, W, H)

def s3(t, d, W, H):  # Kalunga / Nalapani -> first battalions 1815
    b = DEFS + PAINT("bg_nalapani")
    fx, fy, fw, fh = 300, 360, 430, 140
    b += ground_shadow(fx + fw / 2, fy + fh + 6, fw * 0.62)
    g = ""
    for i, x in enumerate(range(fx + 50, fx + fw - 30, 62)):
        g += character(x, fy - 12, 0.24, GURKHA, t + i * 0.9, gesture=(0.5 + 0.5 * math.sin(t * 1.3 + i)) if i % 2 else 0)
    g += stone_fort(fx, fy, fw, fh, t)
    wave = (t - L(3, 1)) % 6 / 6 if t > L(3, 1) else 0
    adv = prog(t, L(3, 1), L(3, 1) + 3)
    for i in range(12):
        x = 2000 - (700 * adv) + i * 58 - 260 * math.sin(math.pi * wave) * (t < L(3, 3)); y = 880 + (i % 3) * 30 + 3 * math.sin(t * 5 + i)
        g += character(x, y, 0.26, BRITISH_OFFICER, t * 1.1 + i * 0.4, flip=True)
    b += warm(g) + grass(fx - 40, fx + fw + 40, fy + fh - 6, 3)
    r = random.Random(int(t * 3))
    if L(3, 1) + 1 < t < L(3, 3) and r.random() < 0.4:
        b += f'<circle cx="{r.uniform(fx, fx+fw):.0f}" cy="{fy + 20:.0f}" r="30" fill="#FFE7B0" opacity="0.7" filter="url(#flash)"/>'
    b += smoke(fx + fw - 60, fy, t, 2, 0.45)
    b += chip(1400, 170, "KALUNGA (NALAPANI) · 1814", prog(t, L(3, 1), L(3, 1) + 0.7) * (1 - prog(t, L(3, 4), L(3, 4) + 0.5)), 40)
    og = inout(t, L(3, 2), L(3, 3) + 1.5)
    b += chip(1400, 290, "General Gillespie killed", og, 36, GOLD)
    # 1815: two battalions
    o5 = prog(t, L(3, 4), L(3, 4) + 0.8)
    b += dim(0.55 * o5)
    for k, (nm, sub) in enumerate([("NASIRI", "battalion"), ("SIRMOOR", "battalion")]):
        ok = prog(t, L(3, 5) + k * 0.8, L(3, 5) + k * 0.8 + 0.6)
        x = 620 + k * 680
        b += card(x - 280, 330, 560, 330, ok) + text(x, 450, nm, 70, GOLD, 900, op=ok) + text(x, 520, sub, 40, CREAM, 600, op=ok)
        b += warm(character(x, 860, 0.45, GURKHA, t + k, op=ok))
    b += text(960, 240, "1815 · GURKHA SERVICE TO BRITAIN BEGINS", 50, WHITE, 900, op=o5)
    return fade(b, t, d, W, H)

def house(x, y, op=1):
    s = f'<g opacity="{op:.2f}" filter="url(#warm)"><rect x="{x}" y="{y}" width="360" height="170" fill="#D8C7A4"/>'
    s += f'<rect x="{x-10}" y="{y-16}" width="380" height="20" fill="#B8A684"/>'
    for i in range(5):
        s += f'<rect x="{x + 22 + i*68}" y="{y + 50}" width="34" height="60" rx="16" fill="#5A4636"/>'
    return s + '</g>'

def s4(t, d, W, H):  # 1857 Delhi Ridge, Hindu Rao's house
    b = DEFS + PAINT("g_delhi") + shade(0.35)
    hx, hy = 760, 470
    b += ground_shadow(hx + 180, hy + 176, 240) + house(hx, hy, prog(t, L(4, 1), L(4, 1) + 1))
    oc = prog(t, L(4, 1) + 1, L(4, 1) + 2)
    for i in range(7):
        x = hx - 120 + i * 95
        b += warm(character(x, hy + 300, 0.3, GURKHA, t + i * 0.7, gesture=(0.4 if (i + int(t)) % 3 == 0 else 0), op=oc))
    r = random.Random(int(t * 4))
    if L(4, 2) < t < L(4, 3) + 3 and r.random() < 0.5:
        b += f'<circle cx="{r.uniform(1300, 1800):.0f}" cy="{r.uniform(650, 850):.0f}" r="26" fill="#FFE7B0" opacity="0.8" filter="url(#flash)"/>'
        b += smoke(r.uniform(1300, 1800), 820, t, r.randint(0, 9), 0.4)
    b += chip(960, 150, "DELHI RIDGE · 1857", prog(t, 0.3, 1.0), 44)
    b += chip(hx + 180, hy - 70, "Hindu Rao's house", oc, 32, GOLD)
    o3 = prog(t, L(4, 3), L(4, 3) + 0.6) * (1 - prog(t, L(4, 4), L(4, 4) + 0.5))
    b += card(1250, 260, 560, 250, o3) + text(1530, 380, countup(t, L(4, 3), L(4, 3) + 2.5, 327), 110, GOLD, 900, op=o3) + text(1530, 460, "of ~490 killed or wounded", 34, CREAM, 600, op=o3)
    o4 = prog(t, L(4, 4), L(4, 4) + 0.7)
    tx = 1500
    b += f'<g opacity="{o4:.2f}" transform="translate({tx} 420) rotate({-8 + 3*math.sin(t*1.5):.1f})"><rect x="-12" y="-150" width="24" height="300" rx="10" fill="#C9A04A" stroke="#7A5A1A" stroke-width="3"/><circle cy="-170" r="34" fill="#C9A04A" stroke="#7A5A1A" stroke-width="4"/><circle cy="-170" r="14" fill="#7A1F2B"/></g>'
    b += chip(tx, 690, "THE QUEEN'S TRUNCHEON", o4, 38, GOLD)
    return fade(b, t, d, W, H)

def s5(t, d, W, H):  # the khukuri: tool, myth
    b = DEFS + PAINT("g_village2") + shade(0.5)
    a0 = prog(t, 0.2, 1.4)
    rot = -30 + 22 * a0 + 2 * math.sin(t * 1.2)
    b += dim(0.25) + khukuri(700, 520, 1.6, rot, a0)
    o1 = prog(t, L(5, 1), L(5, 1) + 0.6)
    b += f'<path d="M560 760 L1300 760" stroke="{GOLD}" stroke-width="4" opacity="{o1:.2f}"/><path d="M560 740 L560 780 M1300 740 L1300 780" stroke="{GOLD}" stroke-width="4" opacity="{o1:.2f}"/>'
    b += text(930, 830, "about 40–45 cm", 50, WHITE, 800, op=o1)
    o2 = inout(t, L(5, 2), L(5, 4) - 0.2)
    icons = ["CUTTING WOOD", "CLEARING PATHS", "CHOPPING FOOD"]
    for k, s_ in enumerate(icons):
        ok = o2 * prog(t, L(5, 2) + k * 1.2, L(5, 2) + k * 1.2 + 0.5)
        b += chip(1550, 300 + k * 150, s_, ok, 36)
    o3 = inout(t, L(5, 3), L(5, 4) - 0.2)
    for k, (nm, sub) in enumerate([("CHAKMAK", "strikes sparks"), ("KARDA", "small knife")]):
        ok = o3 * prog(t, L(5, 3) + k * 0.9, L(5, 3) + k * 0.9 + 0.5)
        b += card(1330, 280 + k * 220, 460, 180, ok) + text(1560, 360 + k * 220, nm, 50, GOLD, 900, op=ok) + text(1560, 420 + k * 220, sub, 32, CREAM, 600, op=ok)
    o4 = prog(t, L(5, 4), L(5, 4) + 0.6) * (1 - prog(t, L(5, 6), L(5, 6) + 0.5))
    b += text(960, 200, "“Once drawn, it must taste blood”", 60, WHITE, 800, op=o4)
    st = prog(t, L(5, 5), L(5, 5) + 0.35)
    if st > 0:
        sc = 1.6 - 0.6 * st
        b += f'<g opacity="{st*(1 - prog(t, L(5, 6), L(5, 6)+0.5)):.2f}" transform="translate(960 330) rotate(-8) scale({sc:.2f})"><rect x="-200" y="-60" width="400" height="120" rx="14" fill="none" stroke="{RED}" stroke-width="10"/>' + text(0, 30, "MYTH", 90, RED, 900, shadow=False) + '</g>'
    o6 = prog(t, L(5, 6), L(5, 6) + 0.6)
    b += warm(character(walk_x(t, L(5, 6), 2100, 1550, 2.5), 900 + bob(t, L(5, 6) < t < L(5, 6) + 2.5), 0.5, GURKHA, t, flip=True, op=o6))
    b += chip(1550, 200, "Issued to every British Army Gurkha", o6, 34, GOLD)
    return fade(b, t, d, W, H)

def s6(t, d, W, H):  # WWI France: Kulbir Thapa
    b = DEFS + PAINT("g_france") + shade(0.4)
    o0 = inout(t, 0.2, L(6, 2))
    b += chip(960, 150, "FRANCE · FIRST WORLD WAR", o0, 44)
    o1 = inout(t, L(6, 1), L(6, 2) - 0.2)
    b += medal(960, 520, 1.6, o1) + chip(960, 760, "VC open to Gurkhas only from 1911", o1, 38, GOLD)
    oc = prog(t, L(6, 2), L(6, 2) + 0.8)
    b += chip(960, 150, "NEUVE CHAPELLE · SEPT 1915", oc * (1 - prog(t, L(6, 5), L(6, 5) + 0.5)), 42)
    # Kulbir finds and guards the wounded soldier, then carries him back
    carry = prog(t, L(6, 4) + 3.5, L(6, 4) + 9.5)
    kx = 1150 - 700 * carry if t > L(6, 4) + 3.5 else walk_x(t, L(6, 2), -150, 1000, 4)
    walking = (L(6, 2) < t < L(6, 2) + 4) or (L(6, 4) + 3.5 < t < L(6, 4) + 9.5)
    if t < L(6, 4) + 3.5:   # wounded soldier lying down
        b += ground_shadow(1240, 930, 150, 0.35 * oc) + f'<g opacity="{oc:.2f}" transform="translate(1240 900) rotate(-85)">' + warm(character(0, 0, 0.42, TOMMY_WW1, t)) + '</g>'
        b += warm(character(kx, 880 + bob(t, walking), 0.5, GURKHA_WW1, t, op=oc, gesture=0.2 if t > L(6, 3) else 0))
    else:
        y = 880 + bob(t, walking)
        b += ground_shadow(kx, 930, 110) + warm(character(kx, y, 0.5, GURKHA_WW1, t, gesture=0.7))
        b += f'<g transform="translate({kx-10:.0f} {y-150:.0f}) rotate(-80)">' + warm(character(0, 0, 0.4, TOMMY_WW1, t)) + '</g>'
    ol = prog(t, L(6, 2) + 2, L(6, 2) + 3)
    b += label(kx, 1000, "Rifleman Kulbir Thapa", ol, 460, 30)
    if t > L(6, 3):
        dn = prog(t, L(6, 3) + 1.5, L(6, 4))
        b += dim(0.35 * dn * (1 - prog(t, L(6, 4) + 2, L(6, 4) + 4)))
        b += chip(1500, 300, "all day · all night", prog(t, L(6, 4), L(6, 4) + 0.6) * (1 - prog(t, L(6, 5), L(6, 5) + 0.4)), 40, GOLD)
    o5 = prog(t, L(6, 5), L(6, 5) + 0.6)
    b += medal(1500, 470, 1.2, o5) + chip(1500, 680, "FIRST GURKHA VC", o5, 44, GOLD)
    return fade(b, t, d, W, H)

def s7(t, d, W, H):  # WWII Burma: Lachhiman Gurung
    b = DEFS + PAINT("g_burma") + '<rect width="1920" height="1080" fill="#0A1A3A" opacity="0.45"/>' + shade(0.3)
    o0 = inout(t, 0.2, L(7, 1))
    b += counter_text(960, 420, "100,000+", "Gurkhas served in the Second World War", o0, 140)
    o1 = prog(t, L(7, 1), L(7, 1) + 0.8)
    b += chip(960, 140, "BURMA · MAY 1945", o1, 44)
    # trench
    b += f'<path d="M500 900 Q960 860 1420 900 L1420 1080 L500 1080Z" fill="#1C140F" opacity="{o1:.2f}"/>'
    b += f'<path d="M520 905 Q960 868 1400 905" stroke="#3A2A1E" stroke-width="20" fill="none" opacity="{o1:.2f}"/>'
    hurt = t > L(7, 2)
    look = dict(GURKHA_WW2)
    b += warm(character(900, 900, 0.5, look, t, op=o1, gesture=0.25 if not hurt else 0.05))
    if hurt:
        b += f'<rect x="860" y="790" width="180" height="16" rx="8" fill="#5A4A3A" opacity="0.9" transform="rotate(-8 900 800)"/>'
    b += label(900, 990, "Rifleman Lachhiman Gurung", prog(t, L(7, 1) + 2, L(7, 1) + 3), 520, 30)
    # attackers in the dark: muzzle flashes far away
    r = random.Random(int(t * 5))
    if t > L(7, 1) + 3:
        for _ in range(3):
            if r.random() < 0.5:
                b += f'<circle cx="{r.uniform(1250, 1850):.0f}" cy="{r.uniform(560, 760):.0f}" r="12" fill="#FFE7B0" opacity="0.9" filter="url(#flash)"/>'
        b += chip(1560, 320, "200+ attackers", inout(t, L(7, 1) + 4, L(7, 2) + 1), 36)
    if L(7, 2) - 0.3 < t < L(7, 2) + 0.6:   # grenade flash
        k = 1 - abs(t - L(7, 2) - 0.1) / 0.7
        b += f'<circle cx="960" cy="860" r="{120 + 200*k:.0f}" fill="#FFF1C9" opacity="{max(0,k)*0.8:.2f}" filter="url(#flash)"/>'
    if t > L(7, 3):   # his left-handed rifle fire
        if int(t * 6) % 3 == 0: b += '<circle cx="1050" cy="830" r="16" fill="#FFE7B0" opacity="0.9" filter="url(#flash)"/>'
        hrs = 4 * prog(t, L(7, 3), L(7, 4))
        b += chip(420, 300, f"{hrs:.1f} HOURS", inout(t, L(7, 3), L(7, 5)), 56, GOLD, 420)
    o4 = prog(t, L(7, 4), L(7, 4) + 0.8)
    b += dim(-0.0) + f'<rect width="1920" height="1080" fill="#F6C97A" opacity="{0.18*o4:.2f}"/>'
    b += chip(1500, 320, "31 enemy dead in front of his section", o4 * (1 - prog(t, L(7, 5), L(7, 5) + 0.4)), 34)
    o5 = prog(t, L(7, 5), L(7, 5) + 0.6)
    b += medal(1500, 500, 1.2, o5) + chip(1500, 720, "VICTORIA CROSS · lived to 92", o5, 36, GOLD)
    return fade(b, t, d, W, H)

def s8(t, d, W, H):  # the cost: 46,000 lights
    b = DEFS + PAINT("g_hook") + dim(0.72)
    n = int(460 * prog(t, 0.5, L(8, 1) + 3))
    r = random.Random(4)
    for i in range(460):
        x = 120 + (i % 46) * 37 + r.uniform(-6, 6); y = 420 + (i // 46) * 52 + r.uniform(-6, 6)
        if i < n:
            fl = 0.55 + 0.35 * math.sin(t * 3 + i)
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{GOLD}" opacity="{fl:.2f}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="18" fill="{GOLD}" opacity="{fl*0.18:.2f}"/>'
    o1 = prog(t, L(8, 1), L(8, 1) + 0.8)
    b += counter_text(960, 250, countup(t, L(8, 1), L(8, 1) + 2.5, 46000) + "+", "Gurkhas died serving the British Crown", o1, 130)
    b += text(960, 1020, "each light = 100 lives", 28, CREAM, 500, op=o1 * 0.8)
    return fade(b, t, d, W, H, fin=0.8)

PI_ = projector(66, 5, 99, 37, 40, 140, 1100, 1060)
PUK = projector(-10.8, 49.8, 2.0, 59.0, 1300, 330, 1840, 980)
def s9(t, d, W, H):  # 1947: 6 regiments to India, 4 to Britain
    om = prog(t, 0, 0.8)
    b = '<rect width="1920" height="1080" fill="#0E2A40"/>'
    for c in ("Pakistan", "China", "Nepal", "Bangladesh", "Myanmar", "Sri Lanka", "Afghanistan", "Bhutan"):
        b += country_path(c, PI_, "#24324A" if c != "Nepal" else NEP, om, "#0E2A40", 1.5)
    b += country_path("India", PI_, "#3A5A4A", om, "#E8F1F5", 2)
    b += country_path("United Kingdom", PUK, "#5A3A4A", om, "#E8F1F5", 2) + country_path("Ireland", PUK, "#24324A", om, "#0E2A40", 1.5)
    b += text(560, 760, "INDIA", 54, WHITE, 900, op=om, ls=6) + text(1570, 1030, "UNITED KINGDOM", 40, WHITE, 900, op=om, ls=6)
    b += chip(960, 120, "1947 · TEN GURKHA REGIMENTS SPLIT", prog(t, 0.2, 1.0), 44)
    split = prog(t, L(9, 1), L(9, 1) + 3)
    for i in range(10):
        sx, sy = 520 + i * 98, 230
        if i < 6: tx, ty = 330 + (i % 3) * 120, 500 + (i // 3) * 110
        else: tx, ty = 1460 + ((i - 6) % 2) * 120, 520 + ((i - 6) // 2) * 110
        x = sx + (tx - sx) * split; y = sy + (ty - sy) * split
        o = prog(t, 0.6 + i * 0.12, 0.9 + i * 0.12)
        b += f'<g opacity="{o:.2f}"><rect x="{x-3:.0f}" y="{y-40:.0f}" width="6" height="80" fill="#D8D2C8"/><path d="M{x+3:.0f} {y-40:.0f} l70 14 l-70 14Z" fill="{KHAKI if i<6 else RED}"/></g>'
    b += chip(470, 860, "6 → INDIAN ARMY", prog(t, L(9, 1) + 2, L(9, 1) + 3), 40, GOLD)
    b += chip(1560, 400, "4 → BRITISH ARMY", prog(t, L(9, 1) + 3, L(9, 1) + 4), 40, GOLD)
    o3 = prog(t, L(9, 2) + 3, L(9, 2) + 4)
    sg = PI_(103.8, 1.35)
    b += chip(1000, 980, "+ Singapore Police Gurkha Contingent · since 1949", o3, 34)
    return fade(b, t, d, W, H)

def doko(x, y, s=1.0):
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><path d="M-70 -150 L70 -150 L45 60 L-45 60Z" fill="#B9874A" stroke="#6B4A22" stroke-width="5"/>'
            + "".join(f'<path d="M{-66+i*2} {-150+i*42} L{66-i*6} {-150+i*42}" stroke="#6B4A22" stroke-width="4"/>' for i in range(5))
            + '<path d="M-60 -150 Q0 -200 60 -150" stroke="#E9DDBF" stroke-width="10" fill="#D8C49A"/></g>')

def s10(t, d, W, H):  # selection in Pokhara, doko race
    b = DEFS + PAINT("g_pokhara") + shade(0.45)
    o1 = inout(t, L(10, 1), L(10, 3) - 0.3)
    b += counter_text(620, 380, countup(t, L(10, 1), L(10, 1) + 3, 16000) + "+", "applicants", o1, 130)
    b += counter_text(1300, 380, "274", "places", o1 * prog(t, L(10, 1) + 3, L(10, 1) + 4), 130)
    b += chip(960, 160, "INTAKE OF JANUARY 2025", o1, 36)
    o2 = inout(t, L(10, 2), L(10, 3) - 0.2)
    b += chip(960, 200, "POKHARA", o2, 60, GOLD)
    o3 = prog(t, L(10, 3), L(10, 3) + 0.6)
    b += f'<g opacity="{0.97*o3:.2f}"><path d="M0 1080 L0 985 Q900 935 1920 895 L1920 1080Z" fill="#3B4A2E"/><path d="M0 1080 L0 1030 Q900 990 1920 960 L1920 1080Z" fill="#2C3823"/></g>' + (grass(0, 1920, 985, 11, 160, "#2C3823") if o3 > 0.5 else "")
    run = prog(t, L(10, 3), d)
    for i in range(3):
        x = 200 + 1400 * run - i * 200; y = 905 - 40 * run
        walking = o3 > 0
        b += warm(f'<g opacity="{o3:.2f}">' + doko(x - 28, y - 28 + bob(t + i, walking), 0.5) + character(x, y + bob(t + i, walking), 0.38, RECRUIT, t * 1.3 + i, flip=False) + '</g>')
    b += f'<path d="M100 1000 L1800 930" stroke="{CREAM}" stroke-width="5" stroke-dasharray="14 14" fill="none" opacity="{0.6*o3:.2f}"/>'
    b += chip(1400, 180, "THE DOKO RACE", o3, 54, GOLD) + chip(1400, 290, "uphill · basket of sand · head strap", o3 * prog(t, L(10, 3) + 1.5, L(10, 3) + 2.2), 32)
    return fade(b, t, d, W, H)

def s11(t, d, W, H):  # Afghanistan 2010 — objects only (living person: not drawn)
    b = DEFS + PAINT("g_helmand") + shade(0.35)
    b += chip(960, 140, "HELMAND, AFGHANISTAN · 2010", prog(t, 0.3, 1.0), 44)
    # checkpoint: sandbag wall + roof, seen from outside
    cp = prog(t, 0.5, 1.5)
    g = f'<g opacity="{cp:.2f}" filter="url(#warm)"><rect x="760" y="560" width="420" height="200" fill="#B59B72"/><rect x="740" y="540" width="460" height="28" fill="#8C7550"/>'
    for j in range(4):
        for i in range(9):
            g += f'<rect x="{730 + i*54 + (j%2)*27}" y="{750 + j*30}" width="52" height="28" rx="12" fill="#A88E64" stroke="#7A6440" stroke-width="2"/>'
    g += '<rect x="900" y="610" width="140" height="40" fill="#2A2018"/></g>'
    b += g
    r = random.Random(int(t * 6))
    if L(11, 0) + 3 < t < L(11, 2) + 2:
        for _ in range(3):
            if r.random() < 0.45: b += f'<circle cx="{r.uniform(1300,1850):.0f}" cy="{r.uniform(650,900):.0f}" r="14" fill="#FFE7B0" opacity="0.9" filter="url(#flash)"/>'
        if int(t * 7) % 2: b += '<circle cx="1050" cy="630" r="18" fill="#FFE7B0" opacity="0.9" filter="url(#flash)"/>'
    o1 = prog(t, L(11, 1), L(11, 1) + 0.6) * (1 - prog(t, L(11, 3), L(11, 3) + 0.4))
    b += chip(960, 290, "Acting Sergeant Dipprasad Pun", o1, 40, GOLD)
    # tripod arc
    k = prog(t, L(11, 2) + 0.5, L(11, 2) + 2.0)
    if 0 < k < 1:
        x = 1040 + 600 * k; y = 620 - 260 * math.sin(math.pi * k); a = 720 * k
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><path d="M0 0 L-30 70 M0 0 L30 70 M0 0 L0 75" stroke="#3A3A3A" stroke-width="8"/></g>'
    b += chip(1500, 450, "…he threw the tripod", inout(t, L(11, 2) + 0.6, L(11, 3)), 38)
    o3 = prog(t, L(11, 3), L(11, 3) + 0.6)
    b += dim(0.4 * o3) + medal(960, 520, 1.5, o3, ribbon="#2E4A7A", metal="#D9D9D9") + chip(960, 760, "CONSPICUOUS GALLANTRY CROSS", o3, 44, GOLD)
    return fade(b, t, d, W, H)

def s12(t, d, W, H):  # ending
    b = DEFS + PAINT("g_end") + shade(0.7)
    o0 = inout(t, 0.2, L(12, 1) - 0.2)
    b += text(960, 250, "“Better to die", 90, WHITE, 900, op=o0) + text(960, 360, "than be a coward”", 90, GOLD, 900, op=o0)
    o1 = inout(t, L(12, 1), L(12, 2) - 0.2)
    b += text(960, 300, "AYO GORKHALI!", 140, GOLD, 900, op=o1, ls=6) + text(960, 380, "“The Gurkhas are here”", 44, CREAM, 600, op=o1)
    g = prog(t, 0.6, 2.0) * (1 - prog(t, L(12, 4) + 2, L(12, 4) + 3))
    b += warm("".join(character(560 + i * 200, 900 + bob(t + i, False), 0.42, [GURKHA, GURKHA_WW1, GURKHA_WW2, GURKHA, GURKHA_WW1][i], t + i, op=g, gesture=0.6 if t > L(12, 1) and t < L(12, 2) else 0) for i in range(5)))
    o2 = inout(t, L(12, 2), L(12, 3) - 0.2)
    b += counter_text(960, 330, "4,000+", "Gurkhas serve in the British Army today", o2, 140)
    o3 = inout(t, L(12, 3), L(12, 4) - 0.2)
    for k, w in enumerate(["TOUGHNESS", "LOYALTY", "COURAGE"]):
        ok = o3 * prog(t, L(12, 3) + 2.5 + k * 0.8, L(12, 3) + 3 + k * 0.8)
        b += chip(560 + k * 400, 300, w, ok, 50, GOLD, 360)
    o4 = inout(t, L(12, 4), L(12, 5) - 0.2)
    b += card(510, 210, 900, 130, o4) + text(960, 295, "A Gurkha in your family? Comment ↓", 48, WHITE, 800, op=o4)
    o5 = inout(t, L(12, 5), L(12, 6) - 0.2)
    b += text(960, 220, "NEXT EPISODE", 40, CREAM, 700, op=o5, ls=8) + text(960, 320, "The Death Zone: Why Bodies Stay on Everest", 62, WHITE, 900, op=o5)
    o6 = prog(t, L(12, 6), L(12, 6) + 0.6)
    b += text(960, 300, "HIMALAYA", 120, WHITE, 900, op=o6, ls=10) + text(960, 390, "UNFOLDED", 64, GOLD, 300, op=o6, ls=34)
    return fade(b, t, d, W, H, fout=1.2)

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]

if __name__ == "__main__":
    main(SCENES, "gurkhas")
