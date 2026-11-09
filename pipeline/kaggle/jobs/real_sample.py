# Kaggle GPU job: realistic stills (RealVisXL V5.0, SDXL fine-tune, CreativeML Open RAIL++-M:
# commercial use OK) + motion clips (Wan 2.2 TI2V-5B, Apache-2.0; falls back to SVD-XT if Wan fails
# or is too slow on the T4). Outputs to /kaggle/working/out/.
import subprocess, sys, time, os, json
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers>=0.35", "transformers", "accelerate",
                "ftfy", "imageio", "imageio-ffmpeg"], check=True)
import torch
from PIL import Image
OUT = "/kaggle/working/out"
LOOK = (", cinematic still from a historical documentary, shot on 35mm film, natural light, muted warm sepia "
        "colour grade, shallow depth of field, highly detailed, photorealistic")
NEG = ("cartoon, painting, illustration, anime, 3d render, text, letters, watermark, logo, modern clothes, "
       "sunglasses, blurry, deformed hands, extra fingers, gore, blood")
GURKHA = ("a Nepali Gurkha rifleman of the early 1900s, brown skin, short black hair, lean weathered face, "
          "wide-brimmed khaki slouch hat with the brim pinned up on one side, khaki wool tunic, leather belt")
SHOTS = {
  "h1_portrait": f"close-up portrait of {GURKHA}, calm determined eyes looking past the camera, mountain mist behind",
  "h2_ridge": f"{GURKHA} standing alone on a misty Himalayan ridge at dawn, seen from behind, rifle slung on his shoulder, snowy peaks far away",
  "h3_march": "a long column of Gurkha soldiers in khaki slouch hats marching up a steep stone mountain trail in the Himalayan foothills, 1910s, dust and morning light",
  "h4_medal": "a bronze Victoria Cross medal with a crimson ribbon lying on dark velvet, dramatic side light, macro close-up",
  "h5_title": "the Himalaya at sunrise seen from a high ridge, layers of blue mountains and golden light on snowy peaks, wide landscape",
  "h6_gorkha": "aerial view of an old hill town on a high ridge in central Nepal, terraced green hills falling away on both sides, morning mist in the valleys",
  "h7_kathmandu": "an old Newar city square in the Kathmandu valley in the 18th century, brick buildings with carved wooden windows, tiered roofs, soft morning light, empty square",
  "h8_farmers": "Nepali hill farmers carrying woven bamboo baskets on their backs walking up a steep stone path between terraced fields, early 1900s",
  "h9_khukuri": "a traditional Nepali khukuri knife lying on a rough wooden table, the steel blade bends forward and downward at an angle like a bent elbow, the sharp edge on the inner curve, polished wooden handle, black leather scabbard beside it, dramatic window light",
}
MOTION = {"h2_ridge": "the soldier's coat and the mist move gently in the wind, clouds drift slowly over the peaks",
          "h3_march": "the soldiers march steadily up the trail, dust rises from their boots",
          "h8_farmers": "the farmers walk slowly up the stone path, baskets swaying on their backs"}
log = {}

t0 = time.time()
from diffusers import StableDiffusionXLPipeline
pipe = StableDiffusionXLPipeline.from_pretrained("SG161222/RealVisXL_V5.0", torch_dtype=torch.float16,
                                                 variant="fp16", use_safetensors=True).to("cuda")
for name, p in SHOTS.items():
    for seed in (11, 23):
        g = torch.Generator("cuda").manual_seed(seed)
        im = pipe(prompt=p + LOOK, negative_prompt=NEG, num_inference_steps=32, guidance_scale=5.5,
                  width=1344, height=768, generator=g).images[0]
        im.save(f"{OUT}/{name}_s{seed}.jpg", quality=93)
    print("still", name, round(time.time() - t0), "s", flush=True)
del pipe; torch.cuda.empty_cache()
log["stills_s"] = round(time.time() - t0)

def wan_clip(name, prompt, budget_s):
    from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
    from diffusers.utils import export_to_video
    t = time.time()
    vae = AutoencoderKLWan.from_pretrained("Wan-AI/Wan2.2-TI2V-5B-Diffusers", subfolder="vae", torch_dtype=torch.float32)
    wp = WanImageToVideoPipeline.from_pretrained("Wan-AI/Wan2.2-TI2V-5B-Diffusers", vae=vae, torch_dtype=torch.float16)
    wp.enable_model_cpu_offload()
    img = Image.open(f"{OUT}/{name}_s11.jpg").convert("RGB").resize((832, 480))
    fr = wp(image=img, prompt=prompt + ", cinematic, realistic, subtle natural motion",
            negative_prompt="static, distorted, morphing faces, extra limbs, text, blurry",
            height=480, width=832, num_frames=49, num_inference_steps=30, guidance_scale=5.0).frames[0]
    export_to_video(fr, f"{OUT}/{name}_wan.mp4", fps=16)
    return round(time.time() - t)

used_wan = False
try:
    secs = wan_clip("h2_ridge", MOTION["h2_ridge"], 1500)
    log["wan_first_s"] = secs; used_wan = True
    print("wan h2 done", secs, "s", flush=True)
    if secs < 1500:
        for n in ("h3_march", "h8_farmers"):
            log[f"wan_{n}_s"] = wan_clip(n, MOTION[n], 1500); print("wan", n, "done", flush=True)
except Exception as e:
    log["wan_error"] = repr(e)[:500]; print("WAN FAILED", e, flush=True)

if not used_wan or "wan_h3_march_s" not in log:
    from diffusers import StableVideoDiffusionPipeline
    sp = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt",
                                                      torch_dtype=torch.float16, variant="fp16")
    sp.enable_model_cpu_offload()
    for n in MOTION:
        if os.path.exists(f"{OUT}/{n}_wan.mp4"): continue
        src = Image.open(f"{OUT}/{n}_s11.jpg").convert("RGB").resize((1024, 576))
        frames = sp(src, num_frames=25, decode_chunk_size=2, motion_bucket_id=110, noise_aug_strength=0.02,
                    generator=torch.manual_seed(7)).frames[0]
        os.makedirs(f"{OUT}/{n}_svd", exist_ok=True)
        for i, f in enumerate(frames): f.save(f"{OUT}/{n}_svd/{i:02d}.jpg", quality=93)
        print("svd", n, "done", flush=True)
json.dump(log, open(f"{OUT}/log.json", "w"), indent=1)
print("ALL DONE", log, flush=True)
