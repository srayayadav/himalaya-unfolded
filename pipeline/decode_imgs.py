"""Decode a browser javascript_tool result file containing IMGJSON{name: base64}ENDJSON into bg/ folders."""
import sys, json, re, base64, os
raw = open(sys.argv[1]).read()
try:
    arr = json.loads(raw); raw = "".join(x.get("text", "") for x in arr)
except Exception: pass
if raw.startswith('"'): raw = json.JSONDecoder().raw_decode(raw)[0]
m = re.search(r"IMGJSON(.*?)ENDJSON", raw, re.S)
d = json.loads(m.group(1))
for n, b in d.items():
    ep = "003-gurkhas" if n.startswith("g_") else "004-death-zone"
    p = os.path.join(ep, "bg", n + ".jpg"); open(p, "wb").write(base64.b64decode(b)); print(p, os.path.getsize(p))
