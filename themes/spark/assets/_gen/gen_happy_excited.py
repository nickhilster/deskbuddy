import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "happy-excited.svg").read_text()

N = 8
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    jump = -2.5 * max(0, math.sin(angle))  # only bounces upward, settles on ground
    tilt = 8 * math.sin(angle)
    arm_lift = 1.5 * max(0, math.sin(angle))
    subs = [
        (r'transform="translate\(0, -2\) rotate\(-5 7\.5 4\)"',
         f'transform="translate(0, {jump - 2:.2f}) rotate({-5 + tilt:.2f} 7.5 4)"'),
        (r'(<line x1="2" y1="2" x2="-0\.5" y2=")-1(" stroke="#4A90E2")',
         rf'\g<1>{-1 - arm_lift:.2f}\g<2>'),
        (r'(<line x1="13" y1="2" x2="15\.5" y2=")-1(" stroke="#4A90E2")',
         rf'\g<1>{-1 - arm_lift:.2f}\g<2>'),
    ]
    specs.append({"subs": subs, "duration": 350})

render_animation(SRC, specs, str(ASSETS / "happy-excited.apng"))
