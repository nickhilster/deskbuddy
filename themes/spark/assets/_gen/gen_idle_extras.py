import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
tired = (ASSETS / "tired-bored.svg").read_text()
playful = (ASSETS / "playful-mischievous.svg").read_text()

# idle-tired-bored: subtle slouch/breathe loop, referenced by idleAnimations
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    slouch = 1.5 + 0.4 * math.sin(angle)
    specs.append({
        "subs": [(r'transform="translate\(0, 1\.5\)"', f'transform="translate(0, {slouch:.2f})"')],
        "duration": 500,
    })
render_animation(tired, specs, str(ASSETS / "idle-tired-bored.apng"))

# idle-playful-mischievous: subtle wink/lean loop, referenced by idleAnimations
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    tilt = 8 + 4 * math.sin(angle)
    specs.append({
        "subs": [(r'transform="rotate\(8 7\.5 4\)"', f'transform="rotate({tilt:.2f} 7.5 4)"')],
        "duration": 450,
    })
render_animation(playful, specs, str(ASSETS / "idle-playful-mischievous.apng"))

print("done")
