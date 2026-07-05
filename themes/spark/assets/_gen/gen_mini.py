import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
idle = (ASSETS / "idle-curious.svg").read_text()
happy = (ASSETS / "happy-excited.svg").read_text()
playful = (ASSETS / "playful-mischievous.svg").read_text()
sleeping = (ASSETS / "sleeping.svg").read_text()

# --- mini-idle-peek: peeks out from corner with a playful lean, then retreats ---
N = 6
specs = []
for i in range(N):
    t = i / (N - 1)
    peek = 6 * math.sin(math.pi * t)  # emerges then retreats
    lean = 10 * math.sin(math.pi * t)
    specs.append({"outer_transform": f"translate({peek:.2f} 0) rotate({lean:.1f} 7.5 4)", "duration": 400})
render_animation(playful, specs, str(ASSETS / "mini-idle-peek.apng"))

# --- mini-peek: subtle, shy peek (smaller amplitude, slower) ---
N = 6
specs = []
for i in range(N):
    t = i / (N - 1)
    peek = 3 * math.sin(math.pi * t)
    specs.append({"outer_transform": f"translate({peek:.2f} 0)", "duration": 500})
render_animation(idle, specs, str(ASSETS / "mini-peek.apng"))

# --- mini-look: glances around from the edge, eyes sweep + slight head turn ---
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    eye_dx = 1.6 * math.sin(angle)
    turn = 5 * math.sin(angle)
    specs.append({
        "subs": [(r'<g id="eyes-js">', f'<g id="eyes-js" transform="translate({eye_dx:.2f} 0)">')],
        "outer_transform": f"rotate({turn:.1f} 7.5 4)",
        "duration": 350,
    })
render_animation(idle, specs, str(ASSETS / "mini-look.apng"))

# --- mini-alert-excited: jumps up excitedly from the edge, eyes wide "Hey!" ---
N = 6
RISE = [10, 6, -1, 1, -0.5, 0]  # rises into view then settles with a small bounce
specs = []
for dy in RISE:
    specs.append({"outer_transform": f"translate(0 {dy:.2f})", "duration": 220})
render_animation(happy, specs, str(ASSETS / "mini-alert-excited.apng"))

# --- mini-celebrate: happy dance at the edge, rhythmic bouncing ---
N = 8
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    bounce = -2 * abs(math.sin(angle))
    tilt = 8 * math.sin(angle)
    specs.append({"outer_transform": f"translate(0 {bounce:.2f}) rotate({tilt:.1f} 7.5 4)", "duration": 300})
render_animation(happy, specs, str(ASSETS / "mini-celebrate.apng"))

# --- mini-enter-bounce: bounces onto screen with energy, playful entrance ---
N = 6
OFFSETS = [-20, -10, -2, 2, -1, 0]
specs = []
for dx in OFFSETS:
    specs.append({"outer_transform": f"translate({dx:.2f} 0)", "duration": 250})
render_animation(playful, specs, str(ASSETS / "mini-enter-bounce.apng"))

# --- mini-crabwalk: scuttles sideways along the screen edge ---
N = 8
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    dx = 4 * math.sin(angle)
    tilt = 6 * math.cos(angle)
    specs.append({"outer_transform": f"translate({dx:.2f} 0) rotate({tilt:.1f} 7.5 4)", "duration": 250})
render_animation(idle, specs, str(ASSETS / "mini-crabwalk.apng"))

# --- mini-sleep-cozy: curled up asleep in the corner, peaceful breathing ---
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    breathe = 2 + 0.4 * math.sin(angle)
    specs.append({
        "subs": [(r'transform="translate\(0, 2\)"', f'transform="translate(0, {breathe:.2f})"')],
        "duration": 550,
    })
render_animation(sleeping, specs, str(ASSETS / "mini-sleep-cozy.apng"))

print("done")
