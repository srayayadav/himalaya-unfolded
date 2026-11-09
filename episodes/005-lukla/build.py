"""Episode 005 — Lukla. Realistic cut from ChatGPT images (img/S*.jpg), Kaggle stills/clips (kaggle/),
code graphics (img/g_*.png). Run after the Kaggle job: python3 build.py [main|shorts|all]"""
import sys, os, json, subprocess
sys.path.insert(0, "../../pipeline")
from realcut import Shot, build

L = json.load(open("lines.json")); lines, idx, times = L["lines"], L["idx"], L["times"]
gi = {tuple(k): i for i, k in enumerate(idx)}          # (section, sentence) -> line index
t = lambda s, n: times[gi[(s, n)]][0]

def src(key):
    """Visual key -> file. Clips fall back to their source still if the clip is missing."""
    if key.startswith("m"):
        p = f"kaggle/{key}_wan.mp4"
        if os.path.exists(p): return p, "clip"
        fb = json.load(open("assets.json"))["motion"][key]["src"]
        return (f"img/{fb}" if fb.startswith("S") else f"kaggle/{fb}"), "in"
    if key.startswith("S"): return f"img/{key}.jpg", None
    if key.startswith("k"): return f"kaggle/{key}.jpg", None
    if key.startswith("g_"): return f"img/{key}.png", None
    return key, None

# (section, sentence, visual, move, flash)
PLAN = [
 ("S01",0,"m01","clip",0),("S01",2,"S07","right",0),("S01",3,"m10","clip",0),("S01",4,"k26_valley","in",0),
 ("S01",5,"S03","in",1),("S01",6,"k01_everest","out",0),("S01",8,"m04","clip",0),("S01",9,"S02","left",0),
 ("S02",0,"g_map","in",1),("S02",2,"k02_town","right",0),("S02",4,"m03","clip",0),("S02",5,"k05_porters_now","left",0),
 ("S02",7,"k04_bridge","in",0),("S02",8,"k24_village","out",0),
 ("S03",0,"m06","clip",1),("S03",1,"k06_school","in",0),("S03",2,"m05","clip",0),("S03",3,"k07_oldplane","right",0),
 ("S03",4,"k08_terminal","in",0),("S03",6,"S06","out",0),("S03",7,"k12_wall","up",0),
 ("S04",0,"g_runway","in",1),("S04",2,"k09_bigrunway","out",0),("S04",3,"k11_uphill","in",0),("S04",5,"S03","up",0),
 ("S04",7,"k10_apron","left",0),("S04",8,"g_runway","out",0),
 ("S05",0,"S07","in",1),("S05",2,"S04","right",0),("S05",3,"k27_takeoff","in",0),("S05",6,"k12_wall","up",0),
 ("S05",7,"m11","clip",0),("S05",9,"k22_wait","out",0),
 ("S06",0,"k14_window","in",1),("S06",1,"S08","in",0),("S06",3,"k13_cockpit","right",0),("S06",5,"k21_planning","in",0),
 ("S06",7,"k10_apron","out",0),
 ("S07",0,"m15","clip",1),("S07",1,"k19_storm","left",0),("S07",3,"k17_tower","in",0),("S07",4,"S10","out",0),
 ("S07",5,"k16_waiting","in",0),("S07",7,"S09","right",0),
 ("S08",0,"k20_cloudplane","in",1),("S08",1,"k18_report","in",0),("S08",2,"k15_fog","left",0),("S08",5,"k18_report","out",0),
 ("S08",7,"k28_flags","in",0),("S08",9,"k12_wall","up",0),
 ("S09",0,"S11","in",1),("S09",1,"k26_valley","right",0),("S09",2,"k21_planning","in",0),("S09",4,"g_runway","in",0),
 ("S09",6,"k22_wait","out",0),("S09",7,"k08_terminal","in",0),
 ("S10",0,"S04","in",1),("S10",1,"k24_village","right",0),("S10",2,"k06_school","in",0),("S10",3,"m23","clip",0),
 ("S10",4,"k10_apron","left",0),("S10",6,"S02","out",0),
 ("S11",0,"k01_everest","in",1),("S11",2,"g_runway","in",0),("S11",3,"S11","right",0),("S11",5,"k26_valley","out",0),
 ("S11",6,"k05_porters_now","in",0),
 ("S12",0,"m12","clip",1),("S12",1,"k27_takeoff","in",0),("S12",3,"k28_flags","out",0),
 ("S12",4,"../sample-real/kaggle/h7_kathmandu_s23.jpg","in",1),
]
TITLES = [(t("S01",5)+0.3, t("S01",6), "WORLD'S MOST DANGEROUS?")]
LABELS = [(t("S01",4)+0.3, t("S01",5), "LUKLA, NEPAL"),
          (t("S03",0)+0.3, t("S03",1), "AI RECONSTRUCTION · 1964"),
          (t("S03",2)+0.3, t("S03",3), "AI RECONSTRUCTION · 1960s"),
          (t("S03",4)+0.3, t("S03",5), "RENAMED IN 2008"),
          (t("S06",0)+0.3, t("S06",1), "ELEVATION ≈ 2,846 m"),
          (t("S08",0)+0.3, t("S08",1), "27 MAY 2017 · OFFICIAL REPORT"),
          (t("S12",3)+0.3, t("S12",4), "HIMALAYA UNFOLDED"),
          (t("S12",4)+0.3, times[-1][1], "NEXT: PRITHVI NARAYAN SHAH")]

SHORTS = [  # (first sentence, last sentence, title)
 (("S03",0), ("S03",7), "Why Was Lukla Airport Built? #shorts", "WHY WAS LUKLA BUILT?"),
 (("S05",0), ("S05",5), "Why Lukla's Runway Slopes Uphill #shorts", "WHY IS THE RUNWAY UPHILL?"),
 (("S09",0), ("S09",7), "Why Pilots Can't Just Go Around at Lukla #shorts", "NO EASY GO-AROUND"),
 (("S11",0), ("S11",4), "Is Lukla Really the Most Dangerous? #shorts", "THE MOST DANGEROUS?"),
]

def main():
    shots = []
    for s, n, key, move, fl in PLAN:
        p, kind = src(key)
        shots.append(Shot(p, 0.0 if (s, n) == ("S01", 0) else t(s, n), "clip" if kind == "clip" else (kind or move), bool(fl)))
    build(shots, lines, times, "voice.wav", "main.mp4", titles=TITLES, labels=LABELS, workdir="cut")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "main.mp4", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                    "-c:a", "copy", "lukla_main.mp4"], check=True)
    # chapters + srt
    ch = [(t(s["id"], 0), s["head"].split("—")[-1].strip().title()) for s in json.load(open("sections.json"))]
    ch[0] = (0.0, ch[0][1])
    open("chapters.txt", "w").write("\n".join(f"{int(a//60)}:{int(a%60):02d} {h}" for a, h in ch) + "\n")
    def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int((x%1)*1000):03d}"
    open("lukla_main.srt", "w").write("\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{l}\n" for i, (l, (a, b)) in enumerate(zip(lines, times))))

def shorts():
    from hu import make_short
    for a, b, title, on in SHORTS:
        st, en = times[gi[a]][0] - 0.2, times[gi[b]][1] + 0.6
        if en - st > 59: en = st + 59
        name = "short_" + title.split()[1].lower().strip("'") + ".mp4"
        make_short("lukla_main.mp4", st, en, on, "", out=name)
        print(name, round(en - st, 1))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("main", "all"): main()
    if what in ("shorts", "all"): shorts()
