import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "idle-curious.svg").read_text()

N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    sweep = 2.2 * math.sin(angle)
    rock = 3 * math.sin(angle)
    subs = [
        (r'<line x1="12\.5" y1="4" x2="14\.5" y2="5" stroke="#4A90E2" stroke-width="0\.8" stroke-linecap="round"/>',
         f'<line x1="12.5" y1="4" x2="{14.5 + sweep:.2f}" y2="{5 - abs(sweep) * 0.3:.2f}" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>'),
        (r'<circle cx="14\.7" cy="5\.2" r="0\.6" fill="#6BA3F5"/>',
         f'<circle cx="{14.7 + sweep:.2f}" cy="{5.2 - abs(sweep) * 0.3:.2f}" r="0.6" fill="#6BA3F5"/>'),
        (r'<g id="body-js">', f'<g id="body-js" transform="rotate({rock:.2f} 7.5 4)">'),
    ]
    specs.append({"subs": subs, "duration": 350})

render_animation(SRC, specs, str(ASSETS / "sweeping-tidy.apng"))
