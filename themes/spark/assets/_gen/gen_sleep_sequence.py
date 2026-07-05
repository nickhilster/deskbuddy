import math
from pathlib import Path
from svg2apng import render_animation, render_svg_to_pil, save_apng
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent
tired = (ASSETS / "tired-bored.svg").read_text()
sleeping = (ASSETS / "sleeping.svg").read_text()

# yawning: big yawn, rubs eyes, stretches (6 frames, ~3s)
tired_rub = tired.replace(
    '<line x1="3" y1="4" x2="1" y2="6.5" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="0.8" cy="6.8" r="0.6" fill="#6BA3F5"/>',
    '<line x1="3" y1="4" x2="5" y2="2" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="5.2" cy="1.8" r="0.6" fill="#6BA3F5"/>',
)
N = 6
specs = []
for i in range(N):
    t = i / (N - 1)
    yawn_ry = 1.1 + 0.8 * math.sin(math.pi * t)  # opens then closes
    stretch_arm_y = -2 * math.sin(math.pi * t)  # right arm rises then settles
    subs = [
        (r'<ellipse cx="7\.5" cy="6" rx="0\.7" ry="1\.1" fill="#000000"/>',
         f'<ellipse cx="7.5" cy="6" rx="{0.7+0.2*math.sin(math.pi*t):.2f}" ry="{yawn_ry:.2f}" fill="#000000"/>'),
        (r'<line x1="12" y1="4" x2="14" y2="6\.5" stroke="#4A90E2" stroke-width="0\.8" stroke-linecap="round"/>',
         f'<line x1="12" y1="4" x2="{14 + stretch_arm_y*0.2:.2f}" y2="{6.5 + stretch_arm_y:.2f}" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>'),
        (r'<circle cx="14\.2" cy="6\.8" r="0\.6" fill="#6BA3F5"/>',
         f'<circle cx="{14.2 + stretch_arm_y*0.2:.2f}" cy="{6.8 + stretch_arm_y:.2f}" r="0.6" fill="#6BA3F5"/>'),
    ]
    specs.append({"subs": subs, "duration": 500})
render_animation(tired_rub, specs, str(ASSETS / "yawning.apng"))

# dozing: eyes flutter half-open/closed, soft snores, head nods (loops infinitely, 6 frames)
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    nod = 0.8 * math.sin(angle)
    eyelid_ry = 0.9 + 0.9 * max(0, math.sin(angle))  # flutter: mostly closed, peeks open
    z_op = 0.4 + 0.4 * ((math.sin(angle + 1) + 1) / 2)
    subs = [
        (r'transform="translate\(0, 2\)"', f'transform="translate(0, {2+nod:.2f})"'),
        (r'<path d="M 3\.8 2\.8 Q 5 3\.5 6\.2 2\.8" stroke="#000000" stroke-width="0\.8" fill="#4A90E2"/>',
         f'<path d="M 3.8 2.8 Q 5 {2.8+eyelid_ry:.2f} 6.2 2.8" stroke="#000000" stroke-width="0.8" fill="#4A90E2"/>'),
        (r'<path d="M 8\.8 2\.8 Q 10 3\.5 11\.2 2\.8" stroke="#000000" stroke-width="0\.8" fill="#4A90E2"/>',
         f'<path d="M 8.8 2.8 Q 10 {2.8+eyelid_ry:.2f} 11.2 2.8" stroke="#000000" stroke-width="0.8" fill="#4A90E2"/>'),
        (r'<g opacity="0\.7">', f'<g opacity="{z_op:.2f}">'),
    ]
    specs.append({"subs": subs, "duration": 450})
render_animation(sleeping, specs, str(ASSETS / "dozing.apng"))

# collapsing: body tilts/falls into a peaceful heap (4 frames, ~0.8s, plays once)
N = 4
angles = [0, 25, 55, 80]
drops = [0, 1, 2.5, 3.5]
specs = []
for angle, drop in zip(angles, drops):
    specs.append({
        "outer_transform": f"translate(0 {drop:.2f}) rotate({angle} 7.5 4)",
        "duration": 200,
    })
render_animation(sleeping, specs, str(ASSETS / "collapsing.apng"))

print("done")
