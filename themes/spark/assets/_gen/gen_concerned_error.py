from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "concerned-error.svg").read_text()

N = 6
TEAR_DY = [0, 0.4, 0.8, 1.3, 1.8, 0]
SHAKE_DX = [0, -0.3, 0, 0.3, 0, 0]

specs = []
for i in range(N):
    dy = TEAR_DY[i]
    dx = SHAKE_DX[i]
    tear_opacity = 0 if dy == 0 else 1.0
    subs = [
        (r'<path d="M 5 4\.8 L 5 5\.3" stroke="#6BA3F5" stroke-width="0\.3"/>',
         f'<path d="M 5 {4.8+dy:.2f} L 5 {5.3+dy:.2f}" stroke="#6BA3F5" stroke-width="0.5" opacity="{tear_opacity:.2f}"/>'),
        (r'<circle cx="5" cy="5\.5" r="0\.3" fill="#6BA3F5"/>',
         f'<circle cx="5" cy="{5.5+dy:.2f}" r="0.55" fill="#6BA3F5" opacity="{tear_opacity:.2f}"/>'),
        (r'<path d="M 10 4\.8 L 10 5\.3" stroke="#6BA3F5" stroke-width="0\.3"/>',
         f'<path d="M 10 {4.8+dy:.2f} L 10 {5.3+dy:.2f}" stroke="#6BA3F5" stroke-width="0.5" opacity="{tear_opacity:.2f}"/>'),
        (r'<circle cx="10" cy="5\.5" r="0\.3" fill="#6BA3F5"/>',
         f'<circle cx="10" cy="{5.5+dy:.2f}" r="0.55" fill="#6BA3F5" opacity="{tear_opacity:.2f}"/>'),
        (r'(<!-- Concerned hand on chest/chin -->\s*)<g>',
         rf'\g<1><g transform="translate({dx:.2f} 0)">'),
    ]
    specs.append({"subs": subs, "duration": 350})

render_animation(SRC, specs, str(ASSETS / "concerned-error.apng"))
