from pathlib import Path
from PIL import Image
from svg2apng import render_svg_to_pil, save_apng

ASSETS = Path(__file__).resolve().parent.parent
sleeping = (ASSETS / "sleeping.svg").read_text()
tired = (ASSETS / "tired-bored.svg").read_text()
idle = (ASSETS / "idle-curious.svg").read_text()

# stretch variant of tired-bored: arms up instead of drooping
tired_stretch = tired.replace(
    '<line x1="3" y1="4" x2="1" y2="6.5" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="0.8" cy="6.8" r="0.6" fill="#6BA3F5"/>',
    '<line x1="3" y1="4" x2="0.5" y2="-2" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="0.3" cy="-2.3" r="0.6" fill="#6BA3F5"/>',
).replace(
    '<line x1="12" y1="4" x2="14" y2="6.5" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="14.2" cy="6.8" r="0.6" fill="#6BA3F5"/>',
    '<line x1="12" y1="4" x2="14.5" y2="-2" stroke="#4A90E2" stroke-width="0.8" stroke-linecap="round"/>\n'
    '    <circle cx="14.7" cy="-2.3" r="0.6" fill="#6BA3F5"/>',
)
# widen the yawn for the stretch pose
tired_stretch = tired_stretch.replace(
    '<ellipse cx="7.5" cy="6" rx="0.7" ry="1.1" fill="#000000"/>',
    '<ellipse cx="7.5" cy="6.2" rx="1.1" ry="1.6" fill="#000000"/>',
)

img_sleep = render_svg_to_pil(sleeping, size=200)
img_tired = render_svg_to_pil(tired, size=200)
img_stretch = render_svg_to_pil(tired_stretch, size=200)
img_idle = render_svg_to_pil(idle, size=200)


def blend(a, b, t):
    return Image.blend(a, b, t)


frames = [
    img_sleep,
    blend(img_sleep, img_tired, 0.6),
    img_stretch,
    blend(img_stretch, img_idle, 0.6),
    img_idle,
]
durations = [350, 250, 500, 250, 350]  # ~1.7s total, matches "1.5s" spec closely

save_apng(frames, str(ASSETS / "waking-stretch.apng"), durations, loop=0)
