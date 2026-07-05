import re
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "happy-excited.svg").read_text()

N = 8
specs = []
for i in range(N):
    f = i / (N - 1)  # 0 -> 1 progressive amazement
    eye_r = 2 + 1.2 * f
    pupil_r = 1.3 + 0.7 * f
    arm_lift = 2.2 * f

    subs = [
        (r'<circle cx="5" cy="2\.5" r="2" fill="white"/>',
         f'<circle cx="5" cy="{2.5 - 0.3*f:.2f}" r="{eye_r:.2f}" fill="white"/>'),
        (r'<circle cx="5" cy="2\.5" r="1\.3" fill="#000000"/>',
         f'<circle cx="5" cy="{2.5 - 0.3*f:.2f}" r="{pupil_r:.2f}" fill="#000000"/>'),
        (r'<circle cx="10" cy="2\.5" r="2" fill="white"/>',
         f'<circle cx="10" cy="{2.5 - 0.3*f:.2f}" r="{eye_r:.2f}" fill="white"/>'),
        (r'<circle cx="10" cy="2\.5" r="1\.3" fill="#000000"/>',
         f'<circle cx="10" cy="{2.5 - 0.3*f:.2f}" r="{pupil_r:.2f}" fill="#000000"/>'),
        (r'(<line x1="2" y1="2" x2="-0\.5" y2=")-1(" stroke="#4A90E2")',
         rf'\g<1>{-1 - arm_lift:.2f}\g<2>'),
        (r'(<line x1="13" y1="2" x2="15\.5" y2=")-1(" stroke="#4A90E2")',
         rf'\g<1>{-1 - arm_lift:.2f}\g<2>'),
    ]
    if f < 0.5:
        # smile progressively flattens toward "oh" as jaw starts dropping
        subs.append((
            r'<path d="M 5 5\.5 Q 7\.5 7 10 5\.5" stroke="#000000" stroke-width="0\.4" fill="none" stroke-linecap="round"/>',
            f'<path d="M 5 5.5 Q 7.5 {7 - 3*f:.2f} 10 5.5" stroke="#000000" stroke-width="0.4" fill="none" stroke-linecap="round"/>',
        ))
    else:
        # jaw drops open into a round "amazed" mouth
        jaw = (f - 0.5) * 2  # 0 -> 1 over second half
        subs.append((
            r'<path d="M 5 5\.5 Q 7\.5 7 10 5\.5" stroke="#000000" stroke-width="0\.4" fill="none" stroke-linecap="round"/>',
            f'<ellipse cx="7.5" cy="{6 + 0.6*jaw:.2f}" rx="{0.8 + 0.3*jaw:.2f}" ry="{0.6 + 1.3*jaw:.2f}" fill="#000000"/>',
        ))
    specs.append({"subs": subs, "duration": 300})

render_animation(SRC, specs, str(ASSETS / "working-impressed.apng"))
