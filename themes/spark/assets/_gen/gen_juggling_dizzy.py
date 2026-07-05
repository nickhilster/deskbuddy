from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "dizzy-overwhelmed.svg").read_text()

N = 8
specs = []
for i in range(N):
    angle = 45 * i  # full 360 spin over 8 frames, matches base pose's 45deg start
    subs = [
        (r'transform="rotate\(45 7\.5 4\)"', f'transform="rotate({angle} 7.5 4)"'),
    ]
    specs.append({"subs": subs, "duration": 300})

render_animation(SRC, specs, str(ASSETS / "juggling-dizzy.apng"))
