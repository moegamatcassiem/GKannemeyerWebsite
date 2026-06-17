"""
One-off script to generate placeholder wood-tone SVG images for the
gallery section. Run with: python generate_placeholders.py

These exist so the gallery looks reasonable before real project
photos are added. Once real photos are available, just point the
gallery_items "image" values in content.py at the new files (jpg/png
work fine) and these can be deleted.
"""

import math
import os

WOODS = [
    {"name": "Oak", "top": "#C9A66B", "bottom": "#8B6B3D", "grain": "#73502B"},
    {"name": "Walnut", "top": "#6B4A30", "bottom": "#3B2818", "grain": "#241509"},
    {"name": "Maple", "top": "#E8D9B5", "bottom": "#C9B083", "grain": "#A98F61"},
    {"name": "Cherry", "top": "#8C4A33", "bottom": "#5A2B1D", "grain": "#3C1A11"},
    {"name": "Ash", "top": "#D8CDB8", "bottom": "#A89A7C", "grain": "#8A7B5C"},
    {"name": "Mahogany", "top": "#5C2A1E", "bottom": "#2E140D", "grain": "#190B06"},
]

WIDTH, HEIGHT = 800, 600

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "gallery")
os.makedirs(OUT_DIR, exist_ok=True)


def grain_path(seed_offset):
    """Build a wavy horizontal path string to look like wood grain."""
    points = []
    y = 80 + seed_offset
    for x in range(0, WIDTH + 40, 40):
        wave = math.sin((x + seed_offset * 30) / 90) * 14
        points.append((x, y + wave))
    d = f"M {points[0][0]},{points[0][1]} "
    for x, y in points[1:]:
        d += f"L {x:.1f},{y:.1f} "
    return d


for i, wood in enumerate(WOODS, start=1):
    grain_lines = ""
    for g in range(6):
        offset = g * 90 + 20
        grain_lines += (
            f'<path d="{grain_path(offset)}" fill="none" '
            f'stroke="{wood["grain"]}" stroke-width="2" opacity="0.35"/>'
        )

    svg = f'''<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad{i}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{wood['top']}"/>
      <stop offset="100%" stop-color="{wood['bottom']}"/>
    </linearGradient>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grad{i})"/>
  <g>{grain_lines}</g>
  <rect x="0" y="{HEIGHT - 64}" width="280" height="64" fill="#1E140D" opacity="0.55"/>
  <text x="24" y="{HEIGHT - 26}" font-family="monospace" font-size="20" fill="#F4ECDC" letter-spacing="2">
    {wood['name'].upper()}
  </text>
</svg>'''

    out_path = os.path.join(OUT_DIR, f"placeholder-{i}.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Wrote {out_path}")
