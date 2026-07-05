import math
from pathlib import Path
from svg2apng import render_animation

ASSETS = Path(__file__).resolve().parent.parent
SRC = (ASSETS / "sleeping.svg").read_text()

N = 6
specs = []
for i in range(N):
    angle = 2 * math.pi * i / N
    breathe = 2 + 0.5 * math.sin(angle)  # gentle rise/fall around the base translate(0,2)

    def zzz(base_y, phase, amp=1.6):
        drift = -amp * ((math.sin(angle + phase) + 1) / 2)  # float upward
        op = 0.3 + 0.5 * ((math.sin(angle + phase) + 1) / 2)
        return drift, op

    d1, o1 = zzz(-8, 0.0)
    d2, o2 = zzz(-4, 1.2)
    d3, o3 = zzz(0, 2.4)

    subs = [
        (r'transform="translate\(0, 2\)"', f'transform="translate(0, {breathe:.2f})"'),
        (r'<text x="11" y="-8" font-size="2\.5" font-weight="bold" fill="#4A90E2">Z</text>',
         f'<text x="11" y="{-8+d1:.2f}" font-size="2.5" font-weight="bold" fill="#4A90E2" opacity="{o1:.2f}">Z</text>'),
        (r'<text x="12\.5" y="-4" font-size="2" fill="#6BA3F5">z</text>',
         f'<text x="12.5" y="{-4+d2:.2f}" font-size="2" fill="#6BA3F5" opacity="{o2:.2f}">z</text>'),
        (r'<text x="11\.5" y="0" font-size="1\.5" fill="#6BA3F5">z</text>',
         f'<text x="11.5" y="{0+d3:.2f}" font-size="1.5" fill="#6BA3F5" opacity="{o3:.2f}">z</text>'),
    ]
    specs.append({"subs": subs, "duration": 500})

render_animation(SRC, specs, str(ASSETS / "sleeping.apng"))
