#!/usr/bin/env python3
"""
Красивый QR в SVG: круглые модули, скруглённые «глаза», монограмма в центре.

  .venv/bin/python tools/make_qr.py                # пишет assets/qr*.svg
  .venv/bin/python tools/make_qr.py URL            # другой адрес

Адрес пишется в верхнем регистре: для QR это alphanumeric-режим — меньше модулей,
крупнее точки, легче сканировать. Хост и схема регистронезависимы.
"""
import sys
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent
URL = (sys.argv[1] if len(sys.argv) > 1 else "https://ssaturnn.github.io").upper()
QUIET = 4          # тихая зона, модулей
DOT = 0.46         # радиус точки (модуль = 1)
LOGO = 7           # сторона пустой зоны под монограмму, модулей (нечётное)


def build(ink: str, accent: str, bg: str | None, monogram: str = "AT") -> str:
    qr = segno.make(URL, error="h", micro=False, boost_error=False)
    m = [list(row) for row in qr.matrix]
    n = len(m)
    size = n + 2 * QUIET
    c0 = (n - LOGO) // 2
    c1 = c0 + LOGO

    def in_eye(r, c):
        return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)

    def in_logo(r, c):
        return c0 <= r < c1 and c0 <= c < c1

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
             f'shape-rendering="geometricPrecision">']
    if bg:
        parts.append(f'<rect width="{size}" height="{size}" rx="2.4" fill="{bg}"/>')
    parts.append(f'<g fill="{ink}">')
    for r in range(n):
        for c in range(n):
            if m[r][c] and not in_eye(r, c) and not in_logo(r, c):
                parts.append(f'<circle cx="{c + QUIET + .5}" cy="{r + QUIET + .5}" r="{DOT}"/>')
    parts.append("</g>")

    # «глаза»: внешнее кольцо 7×7 и центр 3×3
    for (er, ec) in [(0, 0), (0, n - 7), (n - 7, 0)]:
        x, y = ec + QUIET, er + QUIET
        parts.append(
            f'<rect x="{x + .5}" y="{y + .5}" width="6" height="6" rx="1.9" '
            f'fill="none" stroke="{ink}" stroke-width="1"/>'
            f'<rect x="{x + 2}" y="{y + 2}" width="3" height="3" rx="0.95" fill="{accent}"/>'
        )

    # монограмма
    cx = cy = size / 2
    parts.append(
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
        f'font-family="Fraunces, \'Source Serif 4\', Georgia, serif" font-size="4.6" '
        f'font-weight="500" letter-spacing="-0.1" fill="{ink}">{monogram}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    (out / "qr.svg").write_text(build(ink="#15171C", accent="#1D3FBF", bg=None))
    (out / "qr-card.svg").write_text(build(ink="#15171C", accent="#1D3FBF", bg="#FFFFFF"))
    (out / "qr-inverse.svg").write_text(build(ink="#F4F1EA", accent="#7EA0FF", bg=None))
    print("QR:", URL)
