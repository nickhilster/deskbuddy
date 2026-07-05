import re
from pathlib import Path
from svg2apng import render_svg_to_pil, save_apng

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "thinking-confused.svg").read_text()

# 6 frames: head tilt -15 -> -7.5 -> 0 (blink) -> 7.5 -> 15 -> -15 (loop restart)
ANGLES = [-15, -7.5, 0, 7.5, 15, -15]
BLINK_FRAMES = {2}  # index of the center/blink frame


def build_frame(angle: float, blink: bool) -> str:
    svg = SRC
    svg = svg.replace(
        'transform="rotate(-15 7.5 4)"', f'transform="rotate({angle} 7.5 4)"'
    )

    # question mark fades out near center, back in as head tilts away
    q_opacity = min(1.0, abs(angle) / 15)
    svg = re.sub(
        r'(<text x="11.5" y="-8" font-size="3" font-weight="bold" fill="#FF9933")(>\?</text>)',
        rf'\1 opacity="{q_opacity:.2f}"\2',
        svg,
    )

    if blink:
        # replace both eyes (white circle + pupil + highlight) with a closed-eye line
        svg = re.sub(
            r'<circle cx="5" cy="3" r="1\.8" fill="white"/>\s*'
            r'<circle cx="5" cy="3\.2" r="1\.2" fill="#4A90E2"/>\s*'
            r'<circle cx="5\.2" cy="2\.8" r="0\.5" fill="white" opacity="0\.7"/>',
            '<line x1="3.4" y1="3" x2="6.6" y2="3" stroke="#2E5C8A" stroke-width="0.4" stroke-linecap="round"/>',
            svg,
        )
        svg = re.sub(
            r'<circle cx="10" cy="3" r="1\.8" fill="white"/>\s*'
            r'<circle cx="10" cy="3\.2" r="1\.2" fill="#4A90E2"/>\s*'
            r'<circle cx="10\.2" cy="2\.8" r="0\.5" fill="white" opacity="0\.7"/>',
            '<line x1="8.4" y1="3" x2="11.6" y2="3" stroke="#2E5C8A" stroke-width="0.4" stroke-linecap="round"/>',
            svg,
        )
    return svg


frames = []
for i, angle in enumerate(ANGLES):
    svg = build_frame(angle, i in BLINK_FRAMES)
    frames.append(render_svg_to_pil(svg, size=200))

out = ASSETS / "thinking-confused.apng"
save_apng(frames, str(out), durations=500, loop=0)
