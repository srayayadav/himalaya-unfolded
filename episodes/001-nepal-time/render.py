import subprocess, math, json, os, sys
W, H, FPS = 1920, 1080, 30
times = json.load(open("times.json"))
GOLD = "#F6C66B"; CREAM = "#F3DCC0"; WHITE = "#FFFFFF"; SNOW = "#EEF1F8"

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, a, b): return ease((t - a) / (b - a))

DEFS = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1633"/><stop offset="0.55" stop-color="#2E2656"/><stop offset="0.8" stop-color="#8E5466"/><stop offset="1" stop-color="#E08D52"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1633"/><stop offset="1" stop-color="#241F4A"/></linearGradient>
<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E5896"/><stop offset="1" stop-color="#3B2F66"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#342E62"/><stop offset="1" stop-color="#1B1B42"/></linearGradient>
<linearGradient id="g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#15173A"/><stop offset="1" stop-color="#070B1D"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.55"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
</defs>'''

STARS = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="0.6"/>' for x, y, r in
    [(160,120,2.5),(420,70,2),(760,160,2),(1100,90,2.5),(1420,150,2),(1700,80,2.5),(1840,260,2),(300,300,2),(1560,320,2),(980,250,1.5)])

def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{body}</svg>'
def text(x, y, s, size, fill=WHITE, weight=700, anchor="middle", op=1, ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="{weight}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" opacity="{op:.3f}">{s}</text>'

def ridge(pts, fill, dy=0):
    d = "M" + " L".join(f"{x} {y+dy}" for x, y in pts) + f" L{pts[-1][0]} {H} L{pts[0][0]} {H}Z"
    return f'<path d="{d}" fill="{fill}"/>'

def cap(pts, i, frac=0.28, dy=0):
    (x0,y0),(x,y),(x1,y1) = pts[i-1], pts[i], pts[i+1]
    lx,ly = x+(x0-x)*frac, y+(y0-y)*frac; rx,ry = x+(x1-x)*frac, y+(y1-y)*frac
    my = max(ly, ry)
    p=[(x,y),(rx,ry),(x+(rx-x)*0.55,my+(y-my)*0.15+10),(x+(rx-x)*0.2,ry-(ry-y)*0.1),(x-(x-lx)*0.15,my+6),(x-(x-lx)*0.55,ly-(ly-y)*0.05),(lx,ly)]
    return '<path d="M' + " L".join(f"{a:.0f} {b+dy:.0f}" for a,b in p) + f'Z" fill="{SNOW}"/>'

R1 = [(0,800),(200,720),(380,770),(560,650),(720,730),(900,600),(1080,700),(1260,640),(1440,740),(1620,670),(1800,750),(1920,720)]
R2 = [(0,880),(180,820),(360,860),(560,790),(760,850),(960,800),(1160,870),(1360,810),(1560,870),(1760,820),(1920,850)]
R3 = [(0,960),(220,910),(440,950),(660,900),(880,945),(1100,905),(1320,955),(1540,910),(1760,950),(1920,925)]
def range_(dy=0, snow=True):
    s = ridge(R1, "url(#g1)", dy)
    if snow: s += cap(R1,3,dy=dy)+cap(R1,5,dy=dy)+cap(R1,9,dy=dy)
    return s + ridge(R2, "url(#g2)", dy) + ridge(R3, "url(#g3)", dy)

def clock(cx, cy, r, hour, minute, label, sub, op=1, minute_col=GOLD):
    ticks = ""
    for i in range(60):
        a = math.radians(i*6); big = i % 5 == 0
        r1 = r - (34 if big else 16)
        ticks += f'<line x1="{cx+math.sin(a)*r1:.1f}" y1="{cy-math.cos(a)*r1:.1f}" x2="{cx+math.sin(a)*(r-8):.1f}" y2="{cy-math.cos(a)*(r-8):.1f}" stroke="{CREAM}" stroke-width="{6 if big else 2.5}" stroke-linecap="round" opacity="{0.9 if big else 0.45}"/>'
    ha = math.radians((hour % 12 + minute/60) * 30); ma = math.radians(minute * 6)
    return f'''<g opacity="{op:.3f}">
<circle cx="{cx}" cy="{cy}" r="{r}" fill="#141737" stroke="{CREAM}" stroke-width="6" stroke-opacity="0.5"/>{ticks}
<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(ha)*r*0.5:.1f}" y2="{cy-math.cos(ha)*r*0.5:.1f}" stroke="{WHITE}" stroke-width="16" stroke-linecap="round"/>
<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(ma)*r*0.78:.1f}" y2="{cy-math.cos(ma)*r*0.78:.1f}" stroke="{minute_col}" stroke-width="10" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="14" fill="{GOLD}"/>
{text(cx, cy+r+80, label, 56, WHITE, 800, ls=6)}{text(cx, cy+r+140, sub, 40, CREAM, 500)}</g>'''

def fade(body, t, dur, fin=0.35, fout=0.35):
    o = min(clamp(t/fin) if fin else 1, clamp((dur-t)/fout) if fout else 1)
    return body + f'<rect width="{W}" height="{H}" fill="#070B1D" opacity="{1-o:.3f}"/>'

# ---------- scenes ----------
def s1(t, d):
    p = prog(t, 0.4, 3.2); mins = 345*p
    b = f'<rect width="{W}" height="{H}" fill="url(#night)"/>{STARS}'
    b += clock(620, 470, 300, int(mins//60), mins%60, "NEPAL", "Kathmandu")
    b += text(1320, 330, "World time + ...", 52, CREAM, 500, op=prog(t,0.2,0.8))
    b += text(1320, 560, f"+{int(mins//60)}:{int(mins%60):02d}", 220, GOLD, 800)
    b += text(1320, 660, "hours ahead of UTC", 46, CREAM, 500, op=prog(t,2.6,3.4))
    return fade(b, t, d, fout=0.25)

def s2(t, d):
    p = prog(t, 0.8, 2.6)
    b = f'<rect width="{W}" height="{H}" fill="url(#night)"/>{STARS}'
    b += clock(560, 440, 250, 5, 30, "INDIA", "UTC +5:30", minute_col=CREAM)
    b += clock(1360, 440, 250, 5, 30 + 15*p, "NEPAL", "UTC +5:45")
    b += f'<path d="M 860 440 L 1060 440" stroke="{GOLD}" stroke-width="6" stroke-dasharray="14 12" opacity="{p:.2f}"/>'
    b += text(960, 400, f"+{int(round(15*p))} min", 64, GOLD, 800, op=clamp(p*2))
    return fade(b, t, d, fin=0.25, fout=0.25)

def s3(t, d):
    m = prog(t, 1.8, 3.6)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{STARS}'
    b += f'<circle cx="1380" cy="{780-170*m:.0f}" r="100" fill="{GOLD}" opacity="{m:.2f}"/>'
    b += range_(dy=(1-m)*420)
    sc = 0.85 + 0.15*prog(t,0,0.8)
    b += f'<g transform="translate(960 380) scale({sc:.3f})">{text(0, 0, "WHY 5:45?", 170, WHITE, 800, op=prog(t,0,0.6)*(1-m*0.0), ls=8)}</g>'
    b += text(960, 480, "The answer is a mountain.", 60, CREAM, 500, op=prog(t,2.0,2.8))
    return fade(b, t, d, fin=0.25, fout=0.3)

GS = [(0,840),(240,760),(470,810),(700,640),(860,560),(960,420),(1080,560),(1240,650),(1480,760),(1700,700),(1920,780)]
def s4(t, d):
    sun = prog(t, 0.2, 3.5)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{STARS}'
    sy = 640 - 380*sun
    b += f'<circle cx="960" cy="{sy:.0f}" r="260" fill="url(#glow)"/><circle cx="960" cy="{sy:.0f}" r="95" fill="{GOLD}"/>'
    b += ridge(GS, "url(#g1)") + cap(GS, 5, 0.3)
    b += ridge(R3, "url(#g3)", 60)
    # labels
    lp = prog(t, 2.6, 3.4)
    b += f'<line x1="1000" y1="440" x2="1220" y2="330" stroke="{CREAM}" stroke-width="3" opacity="{lp:.2f}"/>'
    b += text(1240, 320, "Gauri Shankar", 58, WHITE, 800, "start", lp)
    b += text(1240, 380, "7,134 m  ·  sacred peak", 38, CREAM, 500, "start", lp)
    kp = prog(t, 4.2, 5.0)
    b += f'<circle cx="420" cy="905" r="12" fill="{GOLD}" opacity="{kp:.2f}"/>' + text(420, 965, "Kathmandu", 40, CREAM, 600, op=kp)
    b += f'<path d="M 450 905 L 900 905" stroke="{CREAM}" stroke-width="3" stroke-dasharray="8 10" opacity="{kp*0.7:.2f}"/>' + text(680, 885, "east →", 34, CREAM, 500, op=kp)
    mp = prog(t, 5.8, 7.4)
    b += f'<line x1="960" y1="40" x2="960" y2="{40+1000*mp:.0f}" stroke="{GOLD}" stroke-width="5" stroke-dasharray="18 12"/>'
    b += f'<rect x="560" y="70" width="360" height="96" rx="18" fill="#0B1633" opacity="{0.85*prog(t,6.6,7.3):.2f}"/>'
    b += text(740, 136, "86.25° E", 62, GOLD, 800, op=prog(t,6.6,7.3))
    return fade(b, t, d, fin=0.25, fout=0.3)

def s5(t, d):
    b = f'<rect width="{W}" height="{H}" fill="url(#night)"/>{STARS}'
    x0, x1, y = 200, 1720, 330
    sweep = prog(t, 0.3, 3.0); deg = 86.25*sweep
    xs = x0 + (x1-x0)*sweep
    b += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{CREAM}" stroke-width="4" opacity="0.4"/>'
    b += f'<line x1="{x0}" y1="{y}" x2="{xs:.0f}" y2="{y}" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    for i in range(0, 87, 10):
        tx = x0 + (x1-x0)*i/86.25
        b += f'<line x1="{tx:.0f}" y1="{y-16}" x2="{tx:.0f}" y2="{y+16}" stroke="{CREAM}" stroke-width="3" opacity="0.6"/>'
    b += text(x0, y+70, "0° Greenwich", 36, CREAM, 500, "start")
    b += text(x1, y+70, "86.25° E", 36, GOLD, 700, "end")
    b += f'<circle cx="{xs:.0f}" cy="{y}" r="16" fill="{GOLD}"/>'
    b += text(xs, y-50, f"{deg:.2f}°  =  {deg*4:.0f} min", 44, WHITE, 700, op=clamp(sweep*3))
    b += text(960, 180, "Every 1° east  =  4 minutes", 64, WHITE, 800, op=prog(t,0,0.6))
    e1, e2 = prog(t, 3.6, 4.4), prog(t, 6.0, 6.8)
    b += text(960, 620, "86.25  ×  4  =  345 minutes", 92, WHITE, 800, op=e1)
    b += text(960, 800, "= 5 h 45 min", 150, GOLD, 800, op=e2)
    return fade(b, t, d, fin=0.25, fout=0.3)

def s6(t, d):
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{STARS}'
    b += f'<circle cx="1480" cy="660" r="95" fill="{GOLD}"/>' + range_()
    b += text(960, 330, "A country that tells time", 88, WHITE, 800, op=prog(t,0.1,0.8))
    b += text(960, 440, "by its mountains.", 88, GOLD, 800, op=prog(t,0.6,1.3))
    b += text(960, 560, "HIMALAYA UNFOLDED", 44, CREAM, 700, op=prog(t,2.4,3.2), ls=10)
    return fade(b, t, d, fin=0.25, fout=0.8)

starts = [0, times[1][0], times[2][0], times[3][0], times[4][0], times[5][0]]
end = times[5][1] + 2.2
bounds = list(zip(starts, starts[1:] + [end]))
scenes = [s1, s2, s3, s4, s5, s6]

def render_scene(i, frames_only=None):
    a, bnd = bounds[i]; d = bnd - a; n = round(d*FPS)
    if frames_only is not None:
        for ft in frames_only:
            open(f"preview_s{i+1}_{ft}.svg","w").write(svg(scenes[i](ft, d)))
            subprocess.run(["rsvg-convert", f"preview_s{i+1}_{ft}.svg", "-o", f"preview_s{i+1}_{ft}.png"], check=True)
        return
    tmp = f"scenes/s{i+1}.tmp.mp4"
    ff = subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-i","-",
        "-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r",str(FPS),tmp], stdin=subprocess.PIPE)
    for f in range(n):
        png = subprocess.run(["rsvg-convert","-f","png"], input=svg(scenes[i](f/FPS, d)).encode(), capture_output=True, check=True).stdout
        ff.stdin.write(png)
    ff.stdin.close()
    if ff.wait() == 0: os.replace(tmp, f"scenes/s{i+1}.mp4")
    print("scene", i+1, "frames", n, flush=True)

if __name__ == "__main__":
    os.makedirs("scenes", exist_ok=True)
    if sys.argv[1] == "preview":
        for i, ts in enumerate([[3.0],[2.8],[3.5],[8.0],[7.5],[3.5]]): render_scene(i, ts)
    else:
        for i in map(int, sys.argv[2:]): render_scene(i)
