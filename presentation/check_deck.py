"""Sanity-check the generated deck: bounds, empty slides, text dump."""

import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

# The console on Windows is cp1252 and cannot encode the glyphs the deck uses
# (▼, ·, —). Fall back to replacement instead of crashing mid-dump.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

DECK = Path(__file__).with_name("Secure-Resumable-File-Transfer.pptx")
prs = Presentation(DECK)
SW, SH = prs.slide_width, prs.slide_height
TOL = Emu(9525 * 12)  # ~0.012" slack

problems = []
for idx, slide in enumerate(prs.slides, start=1):
    texts = []
    for sh in slide.shapes:
        if sh.left is None:
            continue
        if sh.left < -TOL or sh.top < -TOL or sh.left + sh.width > SW + TOL \
                or sh.top + sh.height > SH + TOL:
            problems.append(
                f"slide {idx}: shape out of bounds "
                f"L={sh.left} T={sh.top} R={sh.left + sh.width} B={sh.top + sh.height}"
            )
        if sh.has_text_frame and sh.text_frame.text.strip():
            texts.append(sh.text_frame.text.strip().replace("\n", " | "))
        if sh.has_table:
            for r in sh.table.rows:
                for c in r.cells:
                    if c.text.strip():
                        texts.append(c.text.strip())
    if not texts:
        problems.append(f"slide {idx}: no text content")

if "--dump" in sys.argv:
    for idx, slide in enumerate(prs.slides, start=1):
        print(f"\n=== SLIDE {idx} ===")
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                print("  " + sh.text_frame.text.strip().replace("\n", " / "))
            if sh.has_table:
                for r in sh.table.rows:
                    print("  | " + " | ".join(c.text for c in r.cells))
else:
    print(f"slides: {len(prs.slides)}  size: {SW / 914400:.3f} x {SH / 914400:.3f} in")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
    else:
        print("OK: no out-of-bounds shapes, no empty slides.")