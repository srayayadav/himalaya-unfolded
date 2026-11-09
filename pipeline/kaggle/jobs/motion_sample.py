# Kaggle GPU job: depth map (Depth Anything V2 Small, Apache-2.0) + image-to-video
# (Stable Video Diffusion XT, Stability AI Community License: commercial use OK under $1M revenue).
import io, subprocess, sys, time
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "diffusers>=0.30", "transformers", "accelerate"], check=True)
import torch
from PIL import Image
OUT = "/kaggle/working/out"
for name, data in INPUTS.items():
    stem = name.rsplit(".", 1)[0]
    img = Image.open(io.BytesIO(data)).convert("RGB")
    # 1) depth
    from transformers import pipeline
    t = time.time()
    dp = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=0)
    d = dp(img)["depth"].resize(img.size)
    d.save(f"{OUT}/{stem}_depth.png"); del dp; torch.cuda.empty_cache()
    print("depth done", round(time.time() - t), "s", flush=True)
    # 2) motion
    from diffusers import StableVideoDiffusionPipeline
    t = time.time()
    pipe = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt",
                                                        torch_dtype=torch.float16, variant="fp16")
    pipe.enable_model_cpu_offload()
    src = img.resize((1024, 576))
    for mb in (40, 90):
        g = torch.manual_seed(7)
        frames = pipe(src, num_frames=25, decode_chunk_size=2, motion_bucket_id=mb, noise_aug_strength=0.02,
                      fps=7, generator=g).frames[0]
        for i, f in enumerate(frames):
            f.save(f"{OUT}/{stem}_svd{mb}_{i:02d}.jpg", quality=93)
        print("svd", mb, "done", round(time.time() - t), "s", flush=True)
