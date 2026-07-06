import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "spark" / "assets" / "_gen"))
from svg2apng import render_svg_to_pil  # reuse the proven PyQt5 rasterizer

BRAND_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = Path(__file__).resolve().parents[3] / "assets"
SVG_SRC = (BRAND_DIR / "deskbuddy-mark.svg").read_text()

# assets/icon.png: 512x512 master
icon_png = render_svg_to_pil(SVG_SRC, size=512)
icon_png.save(ASSETS_DIR / "icon.png")

# assets/icon.ico: multi-resolution Windows icon
sizes = [16, 24, 32, 48, 64, 128, 256]
frames = [render_svg_to_pil(SVG_SRC, size=s) for s in sizes]
frames[-1].save(
    ASSETS_DIR / "icon.ico",
    format="ICO",
    sizes=[(s, s) for s in sizes],
)

# Tray icons: small square, flattened onto transparent background
tray = render_svg_to_pil(SVG_SRC, size=32)
tray.save(ASSETS_DIR / "tray-icon.png")
tray.save(ASSETS_DIR / "tray-iconTemplate.png")

# Flash variant: same mark, used for taskbar-flash-on-complete
flash = render_svg_to_pil(SVG_SRC, size=32)
flash.save(ASSETS_DIR / "tray-icon-flash.png")

# Dock icon (macOS): matches assets/icon.png at dock tile scale per the
# existing comment in src/main.js about the ~72.6% fill convention
dock = render_svg_to_pil(SVG_SRC, size=512)
dock.save(ASSETS_DIR / "dock-icon.png")

print("wrote icon.png, icon.ico, tray-icon.png, tray-iconTemplate.png, tray-icon-flash.png, dock-icon.png")
