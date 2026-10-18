"""生成一颗随机颜色的五角星 SVG，保存到项目根目录。"""

import colorsys
import datetime as dt
import math
import random
from pathlib import Path


def find_project_root(start: Path) -> Path:
    """从脚本所在目录向上找项目根目录，找不到就用脚本目录。"""
    markers = (".git", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", ".hg")
    for folder in (start, *start.parents):
        if any((folder / m).exists() for m in markers):
            return folder
    return start


def star_points(cx, cy, outer_r, inner_r, tips=5, start_angle=-90.0):
    """返回五角星 10 个顶点坐标（外顶点与内顶点交替）。"""
    pts = []
    for i in range(tips * 2):
        radius = outer_r if i % 2 == 0 else inner_r
        angle = math.radians(start_angle + i * (180.0 / tips))
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return pts


def hsv_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


def random_star_colors():
    """随机生成填充色和更深一点的描边色（同色系）。"""
    h = random.random()
    s = random.uniform(0.65, 0.95)
    v = random.uniform(0.80, 1.00)
    return hsv_hex(h, s, v), hsv_hex(h, s, v * 0.60)


def main():
    today = dt.date.today().isoformat()       
    out_dir = find_project_root(Path(__file__).resolve().parent)
    out_file = out_dir / f"star{today}.svg"

    # 画布与几何参数
    W, H = 400, 460
    cx, cy = W / 2, 190
    outer_r = 150
    inner_r = outer_r * math.sin(math.radians(18)) / math.sin(math.radians(126))  # ≈0.382R

    fill, stroke = random_star_colors()
    points = " ".join(f"{x:.2f},{y:.2f}" for x, y in star_points(cx, cy, outer_r, inner_r))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  <polygon points="{points}" fill="{fill}" stroke="{stroke}"
           stroke-width="3" stroke-linejoin="round"/>
  <text x="{W / 2}" y="405" text-anchor="middle"
        font-family="Helvetica, Arial, sans-serif" font-size="30" font-weight="bold"
        fill="{stroke}">{today}</text>
</svg>
"""

    out_file.write_text(svg, encoding="utf-8")
    print(f"已生成: {out_file}")
    print(f"   填充色: {fill}   描边色: {stroke}")


if __name__ == "__main__":
    main()
