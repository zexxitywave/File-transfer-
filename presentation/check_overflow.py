"""Estimate rendered text size and flag overflow inside every shape.

Approximate but conservative metrics:
  Segoe UI  average glyph advance ~= 0.50 em
  Consolas  fixed advance       ~= 0.55 em
  line box   ~= 1.20 x font size
"""

import math
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu, Pt

EMU_IN = 914400
DECK = Path(__file__).with_name("Secure-Resumable-File-Transfer.pptx")
prs = Presentation(DECK)
SW, SH = prs.slide_width / EMU_IN, prs.slide_height / EMU_IN

ADVANCE = {"Consolas": 0.55}
DEFAULT_ADVANCE = 0.50


def para_lines(p, width_in):
    """Number of visual lines for one paragraph at the given usable width."""
    runs = p.runs
    if not runs:
        return 0
    size = max((r.font.size.pt if r.font.size else 18) for r in runs)
    mono = any((r.font.name or "") == "Consolas" for r in runs)
    adv = ADVANCE.get("Consolas", DEFAULT_ADVANCE) if mono else DEFAULT_ADVANCE
    char_in = adv * size / 72.0
    if char_in <= 0:
        return 0
    text = "".join(r.text for r in runs)
    hard = text.count("\n") + 1
    per_line = max(1, int(width_in / char_in))
    total = 0
    for seg in text.split("\n"):
        total += max(1, math.ceil(len(seg) / per_line))
    spacing = p.line_spacing if isinstance(p.line_spacing, float) else 1.0
    return total * hard if hard > 1 else total, size, spacing


issues = []
for idx, slide in enumerate(prs.slides, start=1):
    for sh in slide.shapes:
        if sh.has_table:
            tbl = sh.table
            for ri, row in enumerate(tbl.rows):
                for ci, cell in enumerate(row.cells):
                    cw = tbl.columns[ci].width / EMU_IN - 0.2
                    ch = row.height / EMU_IN
                    need = sum(para_lines(p, cw)[0] * 1.2 *
                               para_lines(p, cw)[1] / 72 *
                               (para_lines(p, cw)[2] or 1.0)
                               for p in cell.text_frame.paragraphs)
                    if need > ch + 0.02:
                        issues.append(
                            f"slide {idx}: table cell r{ri}c{ci} needs "
                            f"{need:.2f}in, has {ch:.2f}in :: {cell.text[:45]!r}")
            continue
        if not sh.has_text_frame:
            continue
        tf = sh.text_frame
        if not tf.text.strip():
            continue
        wrap = tf.word_wrap is not False
        ml = (tf.margin_left or 0) / EMU_IN
        mr = (tf.margin_right or 0) / EMU_IN
        mt = (tf.margin_top or 0) / EMU_IN
        mb = (tf.margin_bottom or 0) / EMU_IN
        box_w = sh.width / EMU_IN - ml - mr
        box_h = sh.height / EMU_IN - mt - mb
        top_in = sh.top / EMU_IN

        need_h = 0.0
        widest = 0.0
        for p in tf.paragraphs:
            if not p.runs:
                continue
            lines, size, spacing = para_lines(p, box_w if wrap else 10 ** 6)
            need_h += lines * 1.2 * size / 72.0 * (spacing or 1.0)
            if p.space_after:
                need_h += p.space_after.pt / 72.0
            for r in p.runs:
                s = r.font.size.pt if r.font.size else 18
                adv = ADVANCE.get("Consolas", DEFAULT_ADVANCE) \
                    if (r.font.name or "") == "Consolas" else DEFAULT_ADVANCE
                widest = max(widest, len(r.text) * adv * s / 72.0)

        if need_h > box_h + 0.03:
            issues.append(
                f"slide {idx}: text needs {need_h:.2f}in but box is "
                f"{box_h:.2f}in (top={top_in:.2f}) :: "
                f"{tf.text.strip()[:60]!r}")
        if not wrap and widest > box_w + 0.03:
            issues.append(
                f"slide {idx}: NO-WRAP line is {widest:.2f}in wide, box "
                f"{box_w:.2f}in :: {tf.text.strip()[:60]!r}")
        if top_in + mt + need_h > SH - 0.02:
            issues.append(
                f"slide {idx}: text bottom {top_in + mt + need_h:.2f}in "
                f"exceeds slide height {SH:.2f}in :: {tf.text.strip()[:60]!r}")

if "--verbose" in sys.argv:
    print(f"slides: {len(prs.slides)}")
if issues:
    print(f"{len(issues)} potential layout issue(s):")
    for i in issues:
        print("  -", i)
else:
    print("OK: no estimated text overflow, no no-wrap overrun.")