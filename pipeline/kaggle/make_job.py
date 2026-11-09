"""Wraps a job script for a Kaggle GPU kernel. Files listed in `files` are embedded (base64) so the
kernel needs no repo access; the script reads them via INPUTS[name] -> bytes and writes outputs
into /kaggle/working/out/. Used by .github/workflows/kaggle_job.yml."""
import base64, json, os, sys
script, user, files = sys.argv[1], sys.argv[2], [f for f in sys.argv[3].split(",") if f]
inputs = {os.path.basename(f): base64.b64encode(open(f, "rb").read()).decode() for f in files}
body = open(script).read()
os.makedirs("kernel", exist_ok=True)
open("kernel/job.py", "w").write(
    "import base64, os\nos.makedirs('/kaggle/working/out', exist_ok=True)\n"
    f"INPUTS = {{k: base64.b64decode(v) for k, v in {json.dumps(inputs)}.items()}}\n" + body)
json.dump({"id": f"{user}/himalaya-unfolded-job", "title": "himalaya-unfolded-job", "code_file": "job.py",
           "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True,
           "enable_internet": True, "dataset_sources": [], "competition_sources": [], "kernel_sources": []},
          open("kernel/kernel-metadata.json", "w"), indent=1)
print("job ready", script, list(inputs))
