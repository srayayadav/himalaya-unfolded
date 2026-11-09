# Kaggle GPU job for one episode (realistic workflow, Nov 2026).
# Embedded inputs: assets.json = {"stills": {name: prompt}, "motion": {name: {"src": file, "prompt": text}}}
# plus any source images named in "motion" (ChatGPT images). Generated stills can also be motion sources.
# Stills: RealVisXL V5.0 (OpenRAIL++-M). Motion: Wan 2.2 TI2V-5B (Apache-2.0), 33 frames @ 832x480.
import subprocess, sys, time, os, json, gc, io
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers>=0.35", "transformers", "accelerate",
                "ftfy", "imageio", "imageio-ffmpeg"], check=True)
import torch
from PIL import Image
OUT = "/kaggle/working/out"
spec = json.loads(INPUTS["assets.json"].decode())
LOOK = (", photorealistic documentary photograph, natural light, realistic colours with a gentle warm film grade, "
        "35mm, sharp detail, cinematic composition")
NEG = ("cartoon, painting, illustration, anime, 3d render, text, letters, numbers, watermark, logo, signage, "
       "blurry, deformed, extra fingers, crash, wreckage, fire, gore")
log = {"stills": {}, "motion": {}}
def save_log(): json.dump(log, open(f"{OUT}/log.json", "w"), indent=1)

t0 = time.time()
if spec.get("stills"):
    from diffusers import StableDiffusionXLPipeline
    pipe = StableDiffusionXLPipeline.from_pretrained("SG161222/RealVisXL_V5.0", torch_dtype=torch.float16,
                                                     variant="fp16", use_safetensors=True).to("cuda")
    for name, p in spec["stills"].items():
        g = torch.Generator("cuda").manual_seed(11)
        im = pipe(prompt=p + LOOK, negative_prompt=NEG, num_inference_steps=30, guidance_scale=5.5,
                  width=1344, height=768, generator=g).images[0]
        im.save(f"{OUT}/{name}.jpg", quality=93); log["stills"][name] = round(time.time() - t0)
        print("still", name, flush=True)
    del pipe; gc.collect(); torch.cuda.empty_cache(); save_log()

if spec.get("motion"):
    from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
    from diffusers.utils import export_to_video
    vae = AutoencoderKLWan.from_pretrained("Wan-AI/Wan2.2-TI2V-5B-Diffusers", subfolder="vae", torch_dtype=torch.float32)
    wp = WanImageToVideoPipeline.from_pretrained("Wan-AI/Wan2.2-TI2V-5B-Diffusers", vae=vae, torch_dtype=torch.float16)
    wp.enable_sequential_cpu_offload(); vae.enable_tiling()
    for name, m in spec["motion"].items():
        t = time.time()
        try:
            src = m["src"]
            img = (Image.open(io.BytesIO(INPUTS[src])) if src in INPUTS else Image.open(f"{OUT}/{src}")).convert("RGB")
            img = img.resize((832, 480))
            fr = wp(image=img, prompt=m["prompt"] + ", cinematic, realistic, smooth natural motion",
                    negative_prompt="static, distorted, morphing, warping buildings, extra limbs, text, blurry, crash",
                    height=480, width=832, num_frames=33, num_inference_steps=25, guidance_scale=5.0).frames[0]
            export_to_video(fr, f"{OUT}/{name}_wan.mp4", fps=16)
            log["motion"][name] = round(time.time() - t)
        except Exception as e:
            log["motion"][name] = "ERROR " + repr(e)[:300]; gc.collect(); torch.cuda.empty_cache()
        print("motion", name, log["motion"][name], flush=True); save_log()
save_log(); print("ALL DONE", round(time.time() - t0), flush=True)
