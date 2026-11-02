"""Gate for hand-written SVG figures: no <text> may run past its box or the viewBox.

Width is estimated, not measured: a monospace glyph is about 0.62 em wide, bold about 8% more. The check is
conservative on purpose; a label that passes here fits in the browser with room to spare.

    python -I svg_gate.py page.html        -> prints the offenders, exit 1 when any
"""
import html
import re
import sys

SVG = re.compile(r'<svg[^>]*viewBox="0 0 (\d+) (\d+)"(.*?)</svg>', re.S)
RECT = re.compile(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"')
TEXT = re.compile(r'<text x="(\d+)" y="(\d+)"([^>]*)>([^<]*)</text>')
EM = 0.62
BOLD = 1.08
PAD = 4


def check(html_text: str, default_font_size: int = 12) -> list[str]:
    problems: list[str] = []
    for n, m in enumerate(SVG.finditer(html_text), 1):
        vbw, body = int(m.group(1)), m.group(3)
        rects = [tuple(map(int, r.groups())) for r in RECT.finditer(body)]
        for tm in TEXT.finditer(body):
            x, y, attrs, txt = int(tm.group(1)), int(tm.group(2)), tm.group(3), html.unescape(tm.group(4))
            fs_m = re.search(r'font-size="(\d+)"', attrs)
            fs = int(fs_m.group(1)) if fs_m else default_font_size
            width = len(txt) * fs * EM * (BOLD if 'font-weight="700"' in attrs else 1.0)
            anchor_m = re.search(r'text-anchor="(\w+)"', attrs)
            anchor = anchor_m.group(1) if anchor_m else "start"
            left = x - width if anchor == "end" else x - width / 2 if anchor == "middle" else x
            right = left + width
            box = next((r for r in rects if r[0] <= x <= r[0] + r[2] and r[1] <= y <= r[1] + r[3]), None)
            lim_l, lim_r = (box[0] + PAD, box[0] + box[2] - PAD) if box else (0, vbw)
            if right > lim_r + 0.5 or left < lim_l - 0.5:
                where = "box" if box else "viewBox"
                problems.append(f"figure {n}: '{txt[:48]}' spans {left:.0f}-{right:.0f}, {where} allows {lim_l}-{lim_r}")
    return problems


def main(path: str) -> int:
    with open(path, encoding="utf-8") as fh:
        problems = check(fh.read())
    for p in problems:
        print("SVG text overflow:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
