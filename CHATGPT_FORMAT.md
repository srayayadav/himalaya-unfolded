# Himalaya Unfolded: what ChatGPT delivers for each video

Santosh agreed on 9 Nov 2026 to split the work:
- **ChatGPT** does the research, script, photos, thumbnails and upload text.
- **Claude** does the voice, motion, editing and Shorts.

Deliver exactly this, in **one zip file** named `ep<NNN>-<short-slug>.zip` (e.g. `ep005-lukla.zip`).
Don't ask questions; follow HANDOVER.md and decide yourself.

## 1. `script.txt` (the narration, English, 6–8 minutes, 900–1,150 words)
- One sentence per line. Start every line with the shot it belongs to, in square brackets:
  ```
  [S01] Lukla's runway is just 527 metres long.
  [S01] And at one end, there is a mountain wall.
  [S02] Every pilot who lands here gets exactly one chance.
  ```
- A shot covers 1–2 sentences (3–8 seconds). Expect about **35–60 shots** per video.
- Structure:
  - Hook in the first 15 seconds
  - Context / map
  - 3-act story
  - One surprising fact
  - Ending plus a teaser for the next video
- Numbers are written the way they are spoken: "eighteen fourteen", not "1814".
- Every fact must have a source. List the sources at the bottom after a line `SOURCES:`, one URL per line.

## 2. `shots.txt` (one line per shot)
```
S01 | motion | a small plane on final approach to a short mountain runway, clouds below | label: LUKLA, NEPAL
S02 | still  | close-up of a pilot's hands on the controls, cockpit light |
S03 | map    | Nepal, with Lukla and Kathmandu marked | label: KATHMANDU → LUKLA
S04 | still  | ... | title: THE MOST DANGEROUS AIRPORT
```
- **still**: Claude adds a slow zoom/pan.
- **motion**: Claude makes it move with AI. Use this for **8–12 shots** per video, the ones where movement matters (walking, flying, water, wind, crowds).
- **map**: no image needed. Claude draws a real-border map. Say what to show.
- `label:` is a small place/date label. `title:` is a big title (max 1–2 per video).

## 3. Images `S01.jpg`, `S02.jpg`, … (one per still/motion shot)
- **16:9 landscape**, at least 1536×864, realistic, cinematic, warm film grade (see the style guide in HANDOVER.md).
- **No text, letters or watermarks** in the images.
- Keep recurring characters the same: reuse one fixed description and your reference image.
- Check details: era-correct clothes, Nepali (Newar) architecture, no pagodas/castles from other countries, no modern objects in history scenes.
  - Khukuri: the blade bends down and forward at an "elbow"; the sharp edge is on the inner curve. Never a straight knife.
  - Gurkha hats: wide-brimmed slouch hat, never a conical straw hat.
- No real photos of real people, and no likeness of any living person.

## 4. Thumbnails `thumb_a.png`, `thumb_b.png`, `thumb_c.png` (1280×720)
- 3–5 big words maximum, high contrast.
- Each one clearly different: place-led, person-led, big-question.

## 5. `upload.txt`
- Title (curiosity, under 60 characters, no clickbait lies)
- Description: 2-line hook; the line "Chapters: (Claude will fill in timestamps)"; sources; the line "Narration uses an AI voice. Visuals are AI-generated reconstructions."; then `#Nepal #History #Himalaya`
- Tags (comma-separated, using real high-search phrases)
- Playlist name
- **Shorts:** 3–4 ideas. For each one, the shot range (e.g. `S12–S18`, 30–55 seconds, starting where a sentence starts) and a "Why…?"/"How…?" title under 50 characters ending in `#shorts`.
- Share post: 2–3 honest lines for Nepali Facebook groups.

## Then
Santosh attaches the zip in the Claude chat and writes **"video banau"**. Claude then:
1. Narrates the script (Michael voice)
2. Makes the motion shots move (free Kaggle GPU)
3. Draws the maps
4. Edits the full video with captions, transitions and music
5. Cuts the Shorts
6. Sends everything back for approval
