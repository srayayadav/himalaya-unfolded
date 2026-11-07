import subprocess
from scenes import *
W, H = 1280, 720
PT = projector(79.6, 26.0, 88.6, 30.8, 120, 300, 1160, 710)
b = f'<rect width="{W}" height="{H}" fill="#3A1410"/>'
b += f'<rect width="{W}" height="{H}" fill="url(#night)" opacity="0.35"/>'
b += f'<circle cx="640" cy="560" r="420" fill="url(#glow)"/>'
b += '<g filter="url(#ts)">' + country_path('Nepal', PT, GOLD, 1, GOLD, 1) + '</g>'
b += text(600, 525, "NEPAL", 64, "#3A1410", 900, op=1, shadow=False, ls=6)
b += text(640, 130, "NEVER", 130, WHITE, 900, ls=6)
b += text(640, 255, "COLONIZED?", 130, GOLD, 900, ls=6)
b += f'<rect x="910" y="590" width="330" height="90" rx="16" fill="#C8553D"/>' + text(1075, 652, "HOW?!", 60, WHITE, 900, shadow=False)
open("thumb.svg", "w").write(svg(b, W, H))
subprocess.run(["rsvg-convert", "thumb.svg", "-o", "thumb.png"], check=True)
