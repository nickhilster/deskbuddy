import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "happy-excited.svg").read_text()

# redirect the raised-arm celebration pose into a "carrying a box in front" pose
SRC = SRC.replace(
    '<line x1="2" y1="2" x2="-0.5" y2="-1" stroke="#4A90E2" stroke-width="0.9" stroke-linecap="round"/>\n'
    '    <circle cx="-1" cy="-1.5" r="0.7" fill="#6BA3F5"/>',
    '<line x1="2" y1="2" x2="6" y2="8" stroke="#4A90E2" stroke-width="0.9" stroke-linecap="round"/>\n'
    '    <circle cx="6" cy="8.2" r="0.7" fill="#6BA3F5"/>',
)
SRC = SRC.replace(
    '<line x1="13" y1="2" x2="15.5" y2="-1" stroke="#4A90E2" stroke-width="0.9" stroke-linecap="round"/>\n'
    '    <circle cx="16" cy="-1.5" r="0.7" fill="#6BA3F5"/>',
    '<line x1="13" y1="2" x2="9" y2="8" stroke="#4A90E2" stroke-width="0.9" stroke-linecap="round"/>\n'
    '    <circle cx="9" cy="8.2" r="0.7" fill="#6BA3F5"/>',
)
# invisible carried object hint (a subtle box outline between the hands)
SRC = SRC.replace(
    "</svg>",
    '<rect x="6" y="7" rx="0.5" width="3" height="2.2" fill="none" stroke="#FFB347" '
    'stroke-width="0.3" opacity="0.5"/></svg>',
)

N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    bounce = 0.6 * math.sin(angle)
    puff = 1.0 + 0.04 * max(0, math.sin(angle))
    specs.append({
        "outer_transform": (
            f"translate(0 {bounce:.2f}) translate(7.5 4) scale({puff:.3f} 1) translate(-7.5 -4)"
        ),
        "duration": 450,
    })

render_animation(SRC, specs, str(ASSETS / "carrying-proud.apng"))
