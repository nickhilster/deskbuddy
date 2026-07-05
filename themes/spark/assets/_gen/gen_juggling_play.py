import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "playful-mischievous.svg").read_text()

N = 8
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    bounce = -1.8 * abs(math.sin(angle))
    tilt = 8 + 6 * math.sin(angle)
    subs = [
        (r'transform="rotate\(8 7\.5 4\)"', f'transform="rotate({tilt:.2f} 7.5 4)"'),
    ]
    specs.append({
        "subs": subs,
        "outer_transform": f"translate(0 {bounce:.2f})",
        "duration": 350,
    })

render_animation(SRC, specs, str(ASSETS / "juggling-play.apng"))
