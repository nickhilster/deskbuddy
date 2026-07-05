from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "happy-excited.svg").read_text()

# quick alert pulse: scale punch in, eyes widen, settle
SCALES = [1.0, 1.18, 1.05, 1.15, 1.0]
DURS = [150, 150, 200, 200, 300]
specs = []
for scale, dur in zip(SCALES, DURS):
    specs.append({
        "outer_transform": f"translate(7.5 7.5) scale({scale:.2f}) translate(-7.5 -7.5)",
        "duration": dur,
    })

render_animation(SRC, specs, str(ASSETS / "notification-alert.apng"))
