"""Episode 002 remade in the painted-documentary look (7 Nov 2026).
Map scenes are reused from scenes.py; story scenes get Kaggle paintings + animated characters."""
import sys, os, math, random, functools
sys.path.insert(0, "../../pipeline")
from scenes import *
import scenes as S
from characters import character, GURKHA, BRITISH_OFFICER, PRITHVI_NARAYAN, JUNG_BAHADUR
from style2 import TEXTURE_DEFS, smoke, stone_fort, lower_third
from painted import bg_image, WARM_DEFS, grass, ground_shadow

DEFS = TEXTURE_DEFS.replace("<defs>", "<defs>" + WARM_DEFS)

@functools.lru_cache(None)
def P_(name, W=1920, H=1080):
    for p in (f"bg/{name}.jpg", f"../sample-painted/{name}.jpg"):
        if os.path.exists(p): return bg_image(p, W, H)
    raise FileNotFoundError(name)

def shade(op=0.35, top=True):
    """Darken the top (or bottom) of a painting so white titles stay readable."""
    y1, y2 = ("0", "0.45") if top else ("0.55", "1")
    return (f'<linearGradient id="sh{int(top)}" x1="0" y1="0" x2="0" y2="1"><stop offset="{y1}" stop-color="#06142B" stop-opacity="{op}"/>'
            f'<stop offset="{y2}" stop-color="#06142B" stop-opacity="0"/></linearGradient>' if top else
            f'<linearGradient id="sh{int(top)}" x1="0" y1="0" x2="0" y2="1"><stop offset="{y1}" stop-color="#06142B" stop-opacity="0"/>'
            f'<stop offset="{y2}" stop-color="#06142B" stop-opacity="{op}"/></linearGradient>') + f'<rect width="1920" height="1080" fill="url(#sh{int(top)})"/>'

def label(x, y, name, op=1):
    return card(x - 210, y, 420, 58, op) + text(x, y + 40, name, 30, WHITE, 700, op=op)

def walk_x(t, start, x0, x1, dur=2.0):
    return x0 + (x1 - x0) * prog(t, start, start + dur)

def p2(t, d, W, H):  # title card
    b = DEFS + P_("s02_title") + shade(0.55)
    b += text(960, 300, "WHY NEPAL WAS", 110, WHITE, 900, op=prog(t, 0, 0.6), ls=6)
    b += text(960, 420, "NEVER COLONIZED", 120, GOLD, 900, op=prog(t, 0.3, 0.9), ls=6)
    for i, w in enumerate(["A KING'S WARNING", "A BRUTAL WAR", "A DEAL"]):
        o = prog(t, 1.0 + i*1.1, 1.6 + i*1.1)
        b += card(260 + i*500, 860, 420, 90, o) + text(470 + i*500, 920, w, 38, CREAM, 800, op=o, ls=3)
    return fade(b, t, d, W, H)

def p3(t, d, W, H):  # unification map + the king telling it
    b = S.s3(t, d, W, H)
    o = prog(t, L(3,1), L(3,1) + 1)
    x = walk_x(t, L(3,1), -150, 250)
    b = b.replace('<rect width="1920" height="1080" fill="#050B16"', '<g/><rect width="1920" height="1080" fill="#050B16"', 1)
    ch = character(x, 880, 0.62, PRITHVI_NARAYAN, t, talking=L(3,1) < t < L(3,4) + 3, gesture=0.4 + 0.3*math.sin(t))
    return b.replace('<g/>', ch + label(330, 1000, "Prithvi Narayan Shah", o), 1)

def p4(t, d, W, H):  # yam between two boulders, the king says it
    b = DEFS + P_("s04_boulders") + shade(0.45)
    q = prog(t, L(4,1), L(4,1)+0.8)
    b += card(360, 70, 1200, 130, q) + text(960, 155, "“A yam between two boulders”", 64, WHITE, 800, op=q)
    lb, rb = prog(t, L(4,2), L(4,2)+1), prog(t, L(4,2)+2.5, L(4,2)+3.5)
    b += card(250, 640, 420, 80, lb) + text(460, 695, "QING CHINA", 44, WHITE, 900, op=lb)
    b += card(1250, 640, 460, 80, rb) + text(1480, 695, "EAST INDIA COMPANY", 40, WHITE, 900, op=rb)
    squeeze = 18 * math.sin(clamp((t - L(4,3)) / 3) * math.pi)
    y = prog(t, L(4,1), L(4,1)+0.8)
    b += f'<g transform="translate(960 640) rotate(-20) scale({(0.6+0.4*y)*(1-squeeze/120):.3f} {0.6+0.4*y:.3f})" opacity="{y:.2f}" filter="url(#warm)"><ellipse rx="60" ry="104" fill="#A4673A"/><ellipse rx="60" ry="104" fill="none" stroke="#6B3F22" stroke-width="5"/><path d="M-18 -96 Q0 -150 22 -98" stroke="#2E9E5B" stroke-width="11" fill="none"/></g>'
    b += text(960, 800, "NEPAL", 44, GOLD, 900, op=y, ls=8)
    b += '<g filter="url(#warm)">' + character(walk_x(t, 0.2, -160, 230), 900, 0.5, PRITHVI_NARAYAN, t, talking=L(4,1) < t < L(4,4)+4, gesture=0.6) + '</g>'
    b += label(230, 990, "Prithvi Narayan Shah", prog(t, 0.6, 1.4))
    b += text(1260, 1010, "Still quoted by Nepali leaders today", 38, GOLD, 600, op=prog(t, L(4,4), L(4,4)+0.6))
    return fade(b, t, d, W, H)

def p6(t, d, W, H):  # Nalapani on a painted hillside
    b = DEFS + P_("bg_nalapani")
    fx, fy, fw, fh = 300, 360, 430, 140
    b += ground_shadow(fx + fw/2, fy + fh + 6, fw*0.62)
    g = '<g filter="url(#warm)">'
    for i, x in enumerate(range(fx + 50, fx + fw - 30, 62)):
        g += character(x, fy - 12, 0.24, GURKHA, t + i*0.9, talking=(i == 2 and L(6,1) < t < L(6,3)), gesture=(0.5 + 0.5*math.sin(t*1.3)) if i == 2 else (0.3 if i % 2 else 0))
    g += stone_fort(fx, fy, fw, fh, t)
    arrive = prog(t, L(6,1) + 2, L(6,1) + 6)
    for i in range(12):
        x = 2000 - 760*arrive + i*58 - 4*t; y = 880 + (i % 3)*30 + 3*math.sin(t*5 + i)
        g += character(x, y, 0.26, BRITISH_OFFICER, t*1.1 + i*0.4, flip=True)
    b += g + '</g>' + grass(fx - 40, fx + fw + 40, fy + fh - 6, 3)
    r = random.Random(int(t * 3))
    if t > L(6,1) + 3 and r.random() < 0.35:
        b += f'<circle cx="{fx + r.uniform(20, fw-20):.0f}" cy="{fy - 6}" r="26" fill="#FFD27A" opacity="0.85" filter="url(#flash)"/>'
    b += smoke(fx + fw - 30, fy, t, 4, 0.55) + smoke(fx + 40, fy, t + 1.4, 5, 0.45)
    if t > L(6,1) + 4: b += smoke(1300 - 9*t, 820, t + 0.6, 6, 0.4)
    o1 = prog(t, L(6,1), L(6,1)+0.8)
    b += card(1180, 70, 640, 190, o1) + text(1500, 160, "~600 vs ~3,500", 72, GOLD, 900, op=o1) + text(1500, 220, "Capt. Balbhadra Kunwar's garrison", 32, CREAM, 600, op=o1)
    gl = prog(t, L(6,2), L(6,2)+0.6) * (1 - prog(t, L(6,3), L(6,3)+0.6))
    b += card(1180, 290, 640, 130, gl, "#3A1410") + text(1500, 345, "Day 1: Maj. Gen. Gillespie", 36, WHITE, 800, op=gl) + text(1500, 395, "shot and killed", 36, "#FFB4A2", 700, op=gl)
    m = prog(t, L(6,3), L(6,3)+0.6)
    b += card(1180, 290, 640, 130, m) + text(1500, 345, "31 Oct – 30 Nov 1814", 36, WHITE, 800, op=m) + text(1500, 395, "one month under siege", 36, GOLD, 700, op=m)
    b += lower_third(W, H, "NALAPANI, 1814", "a small hill fort near Dehradun", prog(t, 0.4, 1.2) * (1 - prog(t, L(6,1) + 6, L(6,1) + 7)))
    return fade(b, t, d, W, H)

def p8(t, d, W, H):  # three reasons over a painted gorge
    b = DEFS + P_("s08_reasons") + shade(0.6)
    b += text(960, 150, "WHY NOT TAKE THE REST?", 80, WHITE, 900, op=prog(t, 0, 0.7), ls=4)
    items = [("1", "THE MOUNTAINS", "slow, costly, deadly", L(8,1)), ("2", "GOAL ACHIEVED", "lowlands + fixed border", L(8,2)), ("3", "RESPECT", "for the men who fought them", L(8,3))]
    for i, (n, h, s, at) in enumerate(items):
        o = prog(t, at, at + 0.7); x = 210 + i*520; y = 600 + 40*(1-o)
        b += card(x, y, 460, 300, o)
        b += f'<circle cx="{x+230}" cy="{y+80}" r="52" fill="{GOLD}" opacity="{o:.2f}"/>' + text(x+230, y+102, n, 60, "#0B1E33", 900, op=o, shadow=False)
        b += text(x+230, y+195, h, 42, WHITE, 900, op=o) + text(x+230, y+245, s, 30, CREAM, 500, op=o)
    if t > L(8,3):
        b += '<g filter="url(#warm)">' + character(walk_x(t, L(8,3)+0.5, 2100, 1700), 520, 0.42, BRITISH_OFFICER, t, flip=True, gesture=0.3) + '</g>'
    return fade(b, t, d, W, H)

def p9(t, d, W, H):  # Gurkhas march onto a painted ridge
    b = DEFS + P_("s09_gurkhas") + shade(0.45)
    g = '<g filter="url(#warm)">'
    for i in range(7):
        start = 0.4 + i*0.5
        x = walk_x(t, start, -120 - i*30, 330 + i*190, 2.4)
        bob = 6*abs(math.sin(t*6 + i)) if t < start + 2.4 else 0
        g += character(x, 830 - bob, 0.5, GURKHA, t + i*0.7)
    b += g + '</g>'
    o = prog(t, L(9,1), L(9,1)+0.8)
    b += text(960, 230, "GURKHAS", 170, GOLD, 900, op=o, ls=20) + text(960, 320, "recruited by Britain after the war", 46, WHITE, 600, op=o)
    return fade(b, t, d, W, H)

def p10(t, d, W, H):  # Rana era over a painted valley, Jung Bahadur presents it
    b = DEFS + P_("s10_ranas") + shade(0.6)
    y = 300; p = prog(t, 0.3, L(10,3)+2)
    b += f'<line x1="560" y1="{y}" x2="1820" y2="{y}" stroke="{CREAM}" stroke-width="4" opacity="0.4"/>'
    b += f'<line x1="560" y1="{y}" x2="{560+1260*p:.0f}" y2="{y}" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    ev = [(700, "1846", "Ranas take power", L(10,0)), (1180, "1857", "Gurkhas at Lucknow", L(10,2)), (1650, "1914–18", "90,000+ in WWI", L(10,3))]
    for x, yr, s, at in ev:
        o = prog(t, at, at + 0.7)
        b += f'<circle cx="{x}" cy="{y}" r="18" fill="{GOLD}" opacity="{o:.2f}"/>' + card(x - 210, y + 40, 420, 130, o) + text(x, y + 100, yr, 54, GOLD, 900, op=o) + text(x, y + 150, s, 30, WHITE, 600, op=o)
    b += text(1190, 120, "FRIENDSHIP WITH BRITAIN", 60, WHITE, 900, op=prog(t, L(10,1), L(10,1)+0.7), ls=4)
    b += text(1190, 1010, "20,000+ Gurkhas killed, wounded or missing in WWI", 38, "#FFB4A2", 700, op=prog(t, L(10,4), L(10,4)+0.6))
    b += '<g filter="url(#warm)">' + character(walk_x(t, 0.3, -160, 260), 850, 0.6, JUNG_BAHADUR, t, talking=L(10,0) < t < L(10,2)+3, gesture=0.5 + 0.3*math.sin(t*1.1)) + '</g>'
    b += label(260, 1000, "Jung Bahadur Rana", prog(t, 0.8, 1.6))
    return fade(b, t, d, W, H)

def p11(t, d, W, H):  # 1923 treaty in front of a painted palace
    b = DEFS + P_("s02_title") + shade(0.35)
    o = prog(t, L(11,1), L(11,1)+0.8)
    b += f'<g opacity="{o:.2f}"><rect x="610" y="{170+40*(1-o):.0f}" width="700" height="700" rx="14" fill="#EFE3C8"/>'
    for i in range(8):
        b += f'<rect x="680" y="{440+i*38}" width="{560 - (i%3)*80}" height="10" rx="5" fill="#B9A882"/>'
    b += '</g>' + text(960, 270, "TREATY OF FRIENDSHIP", 46, "#3A2A14", 900, op=o, ls=3, shadow=False)
    b += text(960, 335, "21 December 1923 · Singha Durbar", 32, "#5A4526", 600, op=o, shadow=False)
    s = prog(t, L(11,3), L(11,3)+0.4); sc = 1.6 - 0.6*s
    b += f'<g transform="translate(1180 780) rotate(-12) scale({sc:.2f})" opacity="{s:.2f}"><circle r="110" fill="none" stroke="#B3261E" stroke-width="10"/><circle r="92" fill="none" stroke="#B3261E" stroke-width="3"/></g>'
    b += f'<g transform="translate(1180 780) rotate(-12)" opacity="{s:.2f}">' + text(0, -8, "SOVEREIGN", 30, "#B3261E", 900, shadow=False) + text(0, 28, "INDEPENDENT", 26, "#B3261E", 900, shadow=False) + '</g>'
    a = prog(t, L(11,2), L(11,2)+1)
    b += '<g filter="url(#warm)">' + character(walk_x(t, L(11,2), -160, 300), 860, 0.55, BRITISH_OFFICER, t, talking=L(11,2) < t < L(11,2)+2.5)
    b += character(walk_x(t, L(11,2), 2080, 1620), 860, 0.55, dict(JUNG_BAHADUR, coat="#3A2F5F"), t, flip=True, talking=L(11,2)+2.5 < t < L(11,3)) + '</g>'
    b += label(300, 1000, "Lt Col William O'Connor", a) + label(1620, 1000, "Chandra Shumsher Rana", a)
    b += text(960, 120, "RECOGNITION", 64, WHITE, 900, op=prog(t, 0.2, 0.9), ls=8)
    b += text(960, 920, "Two-day national holiday", 38, GOLD, 700, op=prog(t, L(11,4), L(11,4)+0.6)) if len(BEATS[11][2]) > 4 else ""
    return fade(b, t, d, W, H)

def p13(t, d, W, H):  # ending over a painted valley at sunset
    b = DEFS + P_("s13_ending") + shade(0.5)
    for i, w in enumerate(["HARD MOUNTAINS", "HARD FIGHTERS", "CAREFUL DEALS"]):
        o = prog(t, 0.8 + i*0.9, 1.4 + i*0.9) * (1 - prog(t, L(13,1), L(13,1)+0.5))
        b += text(960, 200 + i*80, w, 60, WHITE if i < 2 else GOLD, 900, op=o, ls=4)
    o2 = prog(t, L(13,1), L(13,1)+0.6) * (1 - prog(t, L(13,3), L(13,3)+0.5))
    b += text(960, 260, "The yam was never crushed.", 76, GOLD, 900, op=o2)
    g = prog(t, L(13,2), L(13,2)+1) * (1 - prog(t, L(13,4), L(13,4)+0.6))
    b += f'<g opacity="{g:.2f}" filter="url(#warm)">' + "".join(character(700 + i*130, 900, 0.42, GURKHA, t + i) for i in range(5)) + '</g>'
    o3 = prog(t, L(13,3), L(13,3)+0.6) * (1 - prog(t, L(13,4), L(13,4)+0.5))
    b += card(560, 190, 800, 120, o3) + text(960, 268, "Which mattered most? Comment ↓", 46, WHITE, 800, op=o3)
    o4 = prog(t, L(13,4), L(13,4)+0.6) * (1 - prog(t, L(13,5), L(13,5)+0.5))
    b += text(960, 220, "NEXT EPISODE", 40, CREAM, 700, op=o4, ls=8) + text(960, 310, "The Gurkhas: Why Armies Feared Them", 66, WHITE, 900, op=o4)
    o5 = prog(t, L(13,5), L(13,5)+0.6)
    b += text(960, 260, "HIMALAYA", 120, WHITE, 900, op=o5, ls=10) + text(960, 350, "UNFOLDED", 64, GOLD, 300, op=o5, ls=34)
    return fade(b, t, d, W, H, fout=1.2)

PSCENES = [S.s0, S.s1, p2, p3, p4, S.s5, p6, S.s7, p8, p9, p10, p11, S.s12, p13]
PLIST = [(fn, a, b) for fn, (a, b) in zip(PSCENES, BOUNDS)]

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        paths = []
        for i in [2, 3, 4, 6, 8, 9, 10, 11, 13]:
            fn, a, b = PLIST[i]; ft = min(b - a - 1, max(BEATS[i][2][-1][0] - a + 1.5, 3))
            p = f"pp_{i:02d}.png"; preview(fn, ft, b - a, 1920, 1080, p); paths.append(p)
        contact_sheet(paths, "pp_sheet.png", cols=3, w=640)
    else:
        import glob, json
        os.makedirs("scenes_p", exist_ok=True)
        files = []
        wk, nw = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
        for i, (fn, a, b) in enumerate(PLIST):
            p = f"scenes_p/m{i+1:02d}.mp4"
            if nw > 1 and i % nw != wk: files.append(p); continue
            if not os.path.exists(p):
                old = f"scenes/m{i+1:02d}.mp4"
                if fn in (S.s0, S.s1, S.s5, S.s7, S.s12) and os.path.exists(old): os.link(old, p)
                else: render_scene(fn, b - a, 1920, 1080, p)
            files.append(p); print("scene", i + 1, flush=True)
        if nw > 1: sys.exit(0)
        from script import BEATS as SB
        lines = [l for bt in SB for l in bt]; times = json.load(open("times.json"))
        os.chdir("scenes_p")
        finish([os.path.basename(f) for f in files], "../voice.wav", "../never_colonized_painted.mp4", srt_lines=lines, srt_times=times)
