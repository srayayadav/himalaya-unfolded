"""Builds a Kaggle script kernel that paints every prompt in episodes/<ep>/paintings.json.
Run by .github/workflows/paintings.yml (cloud, no Mac needed). paintings.json = {"name": "prompt", ...}
or {"name": {"prompt": "...", "seed": 3}}."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from painted import STYLE, NEG

ep, user = sys.argv[1], sys.argv[2]
raw = json.load(open(f"episodes/{ep}/paintings.json"))
items = [(n, v if isinstance(v, str) else v["prompt"], 1 if isinstance(v, str) else v.get("seed", 1)) for n, v in raw.items()]
os.makedirs("kernel", exist_ok=True)
open("kernel/paint.py", "w").write(f'''import subprocess, sys
try:
    import diffusers
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "diffusers"], check=True)
import torch
from diffusers import StableDiffusionXLPipeline
pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")
STYLE = {STYLE!r}
NEG = {NEG!r}
for name, p, seed in {items!r}:
    g = torch.Generator("cuda").manual_seed(seed)
    im = pipe(prompt=p + STYLE, negative_prompt=NEG, num_inference_steps=30, guidance_scale=6.5, width=1344, height=768, generator=g).images[0]
    im.convert("RGB").save(f"/kaggle/working/{{name}}.jpg", quality=92); print("done", name, flush=True)
''')
json.dump({"id": f"{user}/himalaya-unfolded-paintings", "title": "himalaya-unfolded-paintings",
           "code_file": "paint.py", "language": "python", "kernel_type": "script", "is_private": True,
           "enable_gpu": True, "enable_internet": True, "dataset_sources": [], "competition_sources": [],
           "kernel_sources": []}, open("kernel/kernel-metadata.json", "w"), indent=1)
print(len(items), "prompts")
