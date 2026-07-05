import math
from pathlib import Path
from svg2apng import render_svg_to_pil, save_apng

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "idle-curious.svg").read_text()

# swap the playful curious eyebrows for a straighter, focused look (borrowed
# styling from thinking-confused.svg) so the pose reads as concentration, not idle play
SRC = SRC.replace(
    '<path d="M 4 1.5 Q 5 1 6 1.2" stroke="#2E5C8A" stroke-width="0.3" fill="none" stroke-linecap="round"/>\n'
    '    <path d="M 9 1.2 Q 10 1 11 1.5" stroke="#2E5C8A" stroke-width="0.3" fill="none" stroke-linecap="round"/>',
    '<path d="M 4 1.2 L 6 1" stroke="#2E5C8A" stroke-width="0.35" stroke-linecap="round"/>\n'
    '    <path d="M 9 1 L 11 1.2" stroke="#2E5C8A" stroke-width="0.35" stroke-linecap="round"/>',
)
# neutral focused mouth instead of playful smile
SRC = SRC.replace(
    '<path d="M 6 5.5 Q 7.5 6.2 9 5.5" stroke="#000000" stroke-width="0.3" fill="none" stroke-linecap="round"/>',
    '<path d="M 6.3 5.9 L 8.7 5.9" stroke="#000000" stroke-width="0.3" fill="none" stroke-linecap="round"/>',
)

N_FRAMES = 6
DURATION_MS = 400  # 2.4s


def build_frame(i: int) -> str:
    angle = 2 * math.pi * i / N_FRAMES
    body_dy = 1.2 * math.sin(angle)  # positive = nod down

    svg = SRC.replace(
        '<g id="body-js">',
        f'<g id="body-js" transform="translate(0 {body_dy:.2f})">',
    )
    return svg


frames = [render_svg_to_pil(build_frame(i), size=200) for i in range(N_FRAMES)]

out = ASSETS / "working-nod.apng"
save_apng(frames, str(out), durations=DURATION_MS, loop=0)
