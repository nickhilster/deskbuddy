import math
from pathlib import Path
from svg2apng import render_animation, render_svg_to_pil, save_apng
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent
playful = (ASSETS / "playful-mischievous.svg").read_text()
happy = (ASSETS / "happy-excited.svg").read_text()
dizzy = (ASSETS / "dizzy-overwhelmed.svg").read_text()
idle = (ASSETS / "idle-curious.svg").read_text()

# --- react-left-cheeky: grins cheeky, waves at user (playful base, wave via arm swing) ---
N = 6
specs = []
for i in range(N):
    angle = math.pi * i / (N - 1)  # 0 -> pi, one wave swing then back
    wave = 3 * math.sin(angle)
    subs = [
        (r'<line x1="2" y1="2\.5" x2="-0\.5" y2="0" stroke="#4A90E2" stroke-width="0\.9" stroke-linecap="round"/>',
         f'<line x1="2" y1="2.5" x2="{-0.5+wave:.2f}" y2="0" stroke="#4A90E2" stroke-width="0.9" stroke-linecap="round"/>'),
        (r'<circle cx="-1\.2" cy="-0\.5" r="0\.7" fill="#6BA3F5"/>',
         f'<circle cx="{-1.2+wave:.2f}" cy="-0.5" r="0.7" fill="#6BA3F5"/>'),
    ]
    specs.append({"subs": subs, "duration": 420})
render_animation(playful, specs, str(ASSETS / "react-left-cheeky.apng"))

# --- react-right-cheeky: laughs, spins/turns away playfully ---
N = 6
specs = []
for i in range(N):
    t = i / (N - 1)
    angle = 8 + 60 * t if t < 0.7 else 8 + 60 * (1 - t) / 0.3 * 0.3
    specs.append({
        "subs": [(r'transform="rotate\(8 7\.5 4\)"', f'transform="rotate({angle:.1f} 7.5 4)"')],
        "duration": 350,
    })
render_animation(playful, specs, str(ASSETS / "react-right-cheeky.apng"))

# --- react-flail: panics, flails arms, dizzy, "caught!" moment ---
N = 10
specs = []
for i in range(N):
    angle = 2 * math.pi * i / 4  # fast wobble, faster than dizzy's slow spin
    wobble = 12 * math.sin(angle)
    jitter = 0.6 * math.sin(angle * 2)
    specs.append({
        "subs": [(r'transform="rotate\(45 7\.5 4\)"', f'transform="rotate({45+wobble:.1f} 7.5 4)"')],
        "outer_transform": f"translate({jitter:.2f} {abs(jitter):.2f})",
        "duration": 150,
    })
render_animation(dizzy, specs, str(ASSETS / "react-flail.apng"))

# --- react-drag-playful: enjoys motion, bounces along, body follows drag ---
N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    bounce = -1.5 * abs(math.sin(angle))
    tilt = 6 * math.sin(angle)
    specs.append({
        "subs": [(r'transform="rotate\(8 7\.5 4\)"', f'transform="rotate({8+tilt:.1f} 7.5 4)"')],
        "outer_transform": f"translate(0 {bounce:.2f})",
        "duration": 300,
    })
render_animation(playful, specs, str(ASSETS / "react-drag-playful.apng"))

# --- react-drag-left: resists playfully (lean away), surprised, then goes along ---
N = 6
LEANS = [0, -6, -8, -4, 2, 0]
specs = []
for lean in LEANS:
    specs.append({"outer_transform": f"rotate({lean} 7.5 4)", "duration": 300})
render_animation(idle, specs, str(ASSETS / "react-drag-left.apng"))

# --- react-drag-right: goes eagerly, excited, bounces toward destination ---
N = 6
specs = []
for i in range(N):
    t = i / (N - 1)
    lean = 10 * t
    bounce = -1 * math.sin(math.pi * t)
    specs.append({"outer_transform": f"translate(0 {bounce:.2f}) rotate({lean:.1f} 7.5 4)", "duration": 280})
render_animation(happy, specs, str(ASSETS / "react-drag-right.apng"))

print("done")
