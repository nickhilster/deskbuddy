import math
import re
from pathlib import Path
from svg2apng import render_svg_to_pil, save_apng

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "idle-curious.svg").read_text()

N_FRAMES = 6
DURATION_MS = 400  # 6 * 400 = 2.4s


def build_frame(i: int) -> str:
    angle = 2 * math.pi * i / N_FRAMES
    eye_dx = 1.6 * math.sin(angle)
    body_dy = -0.5 * math.cos(angle)  # lean in when eyes centered, out at extremes

    svg = SRC
    svg = svg.replace(
        '<g id="body-js">',
        f'<g id="body-js" transform="translate(0 {body_dy:.2f})">',
    )
    svg = svg.replace(
        '<g id="eyes-js">',
        f'<g id="eyes-js" transform="translate({eye_dx:.2f} 0)">',
    )
    return svg


frames = [render_svg_to_pil(build_frame(i), size=200) for i in range(N_FRAMES)]

out = ASSETS / "working-watch.apng"
save_apng(frames, str(out), durations=DURATION_MS, loop=0)
