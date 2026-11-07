"""Painted-background workflow (Santosh approved 7 Nov 2026): AI painted landscapes from a free
Kaggle GPU + our animated code characters on top. Example: episodes/sample-painted/sample.py.

HOW TO GET PAINTINGS (needs Santosh's Mac + the Claude app's built-in browser; Kaggle account `epasal`):
1. Open https://www.kaggle.com/code/new in the built-in browser. Settings → Accelerator → GPU T4 x2
   (30 free GPU hours a week; a 20-painting episode uses ~25 min). Internet must be on.
2. Type the code from `kaggle_cell(prompts)` into a cell and run it (Shift+Enter). First run downloads
   SDXL (~7 GB, ~2 min); each 1344×768 painting then takes ~25 s.
3. Look at every painting (screenshot). Reject any with people, text, wrong architecture (pagodas,
   Chinese walls, castles) or anything historically wrong; re-run those prompts with a new seed.
4. Transfer each image to the workspace: in the notebook run `from IPython.display import FileLink;
   FileLink('<name>.png')`, open that link (it is a ...jupyter-proxy.kaggle.net/.../proxy/files/<name>.png
   URL) in a new browser tab, then in that tab run JavaScript that fetches the image, draws it on a
   canvas, and returns `canvas.toDataURL('image/jpeg', 0.9)`. The tool saves the long result to a
   tool-results .txt file; decode the base64 from it with Python into `episodes/<ep>/bg/<name>.jpg`.
5. Stop the Kaggle session when done (it keeps using GPU hours while open).

RULES: paintings are backgrounds only (landscapes, sky, valleys, villages from far away). People,
soldiers, forts, maps and text are always drawn by our code so they are accurate and animated.
Model: stabilityai/stable-diffusion-xl-base-1.0 (CreativeML Open RAIL++-M licence, commercial use OK).
Because the backgrounds are AI-made but not realistic photos, YouTube's altered/synthetic toggle is
not needed; still keep "Visuals include AI-generated painted backgrounds." in the description.
"""
import base64, random

STYLE = (", gouache painting, storybook historical illustration, visible brush strokes, muted warm palette, "
         "soft atmospheric light, wide cinematic composition, empty landscape, no people, no text")
NEG = ("photo, photorealistic, 3d render, text, letters, watermark, logo, modern buildings, cars, people, soldiers, "
       "faces, castle, fortress, great wall, pagoda, temple, blurry, deformed")

def kaggle_cell(prompts, steps=30, seed=1):
    """prompts: dict name -> scene description. Returns notebook code to type into Kaggle."""
    items = ", ".join(f"({n!r}, {p!r})" for n, p in prompts.items())
    return f'''import torch
from diffusers import StableDiffusionXLPipeline
from IPython.display import display
if "pipe" not in globals():
    pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")
STYLE = {STYLE!r}
NEG = {NEG!r}
for name, p in [{items}]:
    g = torch.Generator("cuda").manual_seed({seed})
    im = pipe(prompt=p + STYLE, negative_prompt=NEG, num_inference_steps={steps}, guidance_scale=6.5, width=1344, height=768, generator=g).images[0]
    im.save(f"/kaggle/working/{{name}}.png"); print(name); display(im.resize((672, 384)))
'''

def bg_image(path, W, H, op=1.0):
    """SVG <image> filling the frame with a painting (embedded as data URI; cache the string)."""
    data = base64.b64encode(open(path, "rb").read()).decode()
    return f'<image href="data:image/jpeg;base64,{data}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" opacity="{op}"/>'

# Wrap characters/forts in <g filter="url(#warm)"> so flat colours sit inside the painting's light.
WARM_DEFS = '''<filter id="warm"><feColorMatrix type="matrix" values="0.84 0.03 0.01 0 0.08  0.02 0.80 0.02 0 0.04  0.01 0.02 0.76 0 0.02  0 0 0 1 0"/></filter>
<filter id="flash"><feGaussianBlur stdDeviation="10"/></filter>'''

def grass(x0, x1, y, seed, n=170, col="#5E3A34"):
    """Grass blades over the base of anything we place on a painted slope (hides the hard edge)."""
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); yy = y + r.uniform(0, 18); h = r.uniform(10, 34)
        s += f'<path d="M{x:.0f} {yy:.0f} q{r.uniform(-4,4):.0f} {-h/2:.0f} {r.uniform(-7,7):.0f} {-h:.0f}" stroke="{col}" stroke-width="2.4" fill="none" opacity="0.95"/>'
    return s

def ground_shadow(cx, cy, rx, op=0.45):
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="22" fill="#1A0D0D" opacity="{op}" filter="url(#flash)"/>'
