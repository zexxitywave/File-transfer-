"""Generate the project presentation for the FTP server / SRFT project.

15 slides, 16:9. Every figure is taken from the repository; there are no
placeholders to fill in.

Run:  py -3 presentation/make_deck.py
Out:  presentation/Secure-Resumable-File-Transfer.pptx
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).with_name("Secure-Resumable-File-Transfer.pptx")

# ---------------------------------------------------------------- palette ----
NAVY = RGBColor(0x0B, 0x1F, 0x3A)
NAVY_SOFT = RGBColor(0x16, 0x33, 0x57)
BLUE = RGBColor(0x1E, 0x6F, 0xD9)
BLUE_LIGHT = RGBColor(0xE8, 0xF1, 0xFD)
CYAN = RGBColor(0x11, 0x8A, 0xA0)
CYAN_LIGHT = RGBColor(0xEC, 0xF6, 0xF8)
CYAN_LINE = RGBColor(0xB4, 0xDD, 0xE6)
GREEN = RGBColor(0x1E, 0x8E, 0x5A)
GREEN_LIGHT = RGBColor(0xE7, 0xF6, 0xEF)
GREEN_LINE = RGBColor(0xBF, 0xE3, 0xD1)
AMBER = RGBColor(0xB5, 0x6E, 0x00)
AMBER_LIGHT = RGBColor(0xFD, 0xF3, 0xE0)
AMBER_LINE = RGBColor(0xE8, 0xD4, 0xAE)
RED = RGBColor(0xC0, 0x39, 0x2B)
RED_LIGHT = RGBColor(0xFC, 0xEC, 0xEA)
RED_LINE = RGBColor(0xEE, 0xC4, 0xBE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xB8, 0xCA, 0xDE)
GREY = RGBColor(0x4A, 0x55, 0x68)
GREY_LIGHT = RGBColor(0x8A, 0x96, 0xA8)
LINE = RGBColor(0xD8, 0xE0, 0xEC)
BG = RGBColor(0xF7, 0xF9, 0xFC)

FONT = "Segoe UI"
FONT_BOLD = "Segoe UI Semibold"
MONO = "Consolas"

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.62)
CONTENT_W = W - 2 * MARGIN

AUTHOR = "zexxitywave"
REPO = "github.com/zexxitywave/File-transfer-"

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]

_state = {"n": 0}


# ---------------------------------------------------------------- helpers ----
def new_slide(footer=True):
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE
    _state["n"] += 1
    if footer:
        text(s, f"Secure Resumable File Transfer  ·  v1.0.0  ·  {AUTHOR}",
             MARGIN, H - Inches(0.46), Inches(8), Inches(0.28),
             9, color=GREY_LIGHT)
        text(s, str(_state["n"]), W - MARGIN - Inches(1), H - Inches(0.46),
             Inches(1), Inches(0.28), 9, color=GREY_LIGHT, align=PP_ALIGN.RIGHT)
    return s


def text(slide, body, l, t, w, h, size=14, bold=False, color=GREY,
         font=FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         spacing=1.0, space_after=0, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(body.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        if space_after:
            p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = color
        if bold and font == FONT:
            f.name = FONT_BOLD
    return box


def bullets(slide, items, l, t, w, h, size=14, color=GREY, gap=9,
            marker="\u2022", spacing=1.12):
    """items: str, or (str, level). 'Head||rest' bolds the head in navy."""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        body, level = (item, 0) if isinstance(item, str) else item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = spacing
        p.space_after = Pt(gap)
        mark = marker if level == 0 else "\u2013"
        r = p.add_run()
        r.text = f"{mark}  "
        r.font.name, r.font.size, r.font.color.rgb = FONT, Pt(size), BLUE
        head, sep, tail = body.partition("||")
        if sep:
            r = p.add_run()
            r.text = head
            r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(size), True
            r.font.color.rgb = NAVY
            r = p.add_run()
            r.text = tail
            r.font.name, r.font.size = FONT, Pt(size)
            r.font.color.rgb = color
        else:
            r = p.add_run()
            r.text = body
            r.font.name, r.font.size = FONT, Pt(size)
            r.font.color.rgb = color
    return box


def rect(slide, l, t, w, h, fill=BLUE_LIGHT, line=None,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05):
    s = slide.shapes.add_shape(shape, l, t, w, h)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    s.shadow.inherit = False
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.16)
    tf.margin_top = tf.margin_bottom = Inches(0.1)
    return s


def header(slide, title, kicker=None, accent=BLUE):
    rect(slide, Inches(0), Inches(0), W, Inches(1.06), fill=NAVY,
         shape=MSO_SHAPE.RECTANGLE)
    rect(slide, Inches(0), Inches(1.06), W, Inches(0.055), fill=accent,
         shape=MSO_SHAPE.RECTANGLE)
    if kicker:
        text(slide, kicker.upper(), MARGIN, Inches(0.15), CONTENT_W,
             Inches(0.24), 10.5, bold=True, color=RGBColor(0x7E, 0xB4, 0xF0))
        text(slide, title, MARGIN, Inches(0.41), CONTENT_W, Inches(0.5),
             26, bold=True, color=WHITE)
    else:
        text(slide, title, MARGIN, Inches(0.3), CONTENT_W, Inches(0.5),
             27, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)


def code(slide, body, l, t, w, h, size=12.5, fill=NAVY,
         fg=RGBColor(0xD8, 0xE6, 0xF5)):
    s = rect(slide, l, t, w, h, fill=fill, radius=0.03)
    tf = s.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.22)
    for i, line in enumerate(body.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.24
        r = p.add_run()
        r.text = line
        r.font.name, r.font.size = MONO, Pt(size)
        r.font.color.rgb = fg
    return s


def table(slide, headers, rows, l, t, w, widths=None, size=11.5,
          head_size=11, row_h=Inches(0.36), head_h=Inches(0.4),
          align_first_bold=True):
    n_rows, n_cols = len(rows) + 1, len(headers)
    shape = slide.shapes.add_table(n_rows, n_cols, l, t, w,
                                   head_h + row_h * len(rows))
    tbl = shape.table
    tbl.first_row = True
    tbl.horz_banding = False
    if widths:
        total = sum(widths)
        for i, val in enumerate(widths):
            tbl.columns[i].width = int(w * val / total)
    tbl.rows[0].height = head_h
    for r in range(1, n_rows):
        tbl.rows[r].height = row_h

    for c, head in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.margin_left = cell.margin_right = Inches(0.1)
        cell.margin_top = cell.margin_bottom = 0
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        r = cell.text_frame.paragraphs[0].add_run()
        r.text = head
        r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(head_size), True
        r.font.color.rgb = WHITE

    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if ri % 2 else BG
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = 0
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.line_spacing = 1.05
            r = p.add_run()
            r.text = val
            bold = ci == 0 and align_first_bold
            r.font.name = FONT_BOLD if bold else FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = NAVY if ci == 0 else GREY
    return tbl


def card(slide, l, t, w, h, title, items, accent=BLUE, fill=BLUE_LIGHT,
         line=None, title_size=14, size=11.5):
    rect(slide, l, t, w, h, fill=fill, line=line, radius=0.04)
    rect(slide, l, t, Inches(0.055), h, fill=accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, title, l + Inches(0.24), t + Inches(0.15), w - Inches(0.4),
         Inches(0.3), title_size, bold=True, color=NAVY)
    bullets(slide, items, l + Inches(0.24), t + Inches(0.54), w - Inches(0.42),
            h - Inches(0.66), size=size, gap=6, spacing=1.1)


def badge(slide, l, t, w, h, label, fill, size=13,
          shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2):
    """Centred chip with no vertical text margin, so the glyph cannot overflow."""
    s = rect(slide, l, t, w, h, fill=fill, shape=shape, radius=radius)
    tf = s.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(size), True
    r.font.color.rgb = WHITE
    return s


def chip(slide, l, t, w, h, label, fill=NAVY, fg=WHITE, size=13,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, line=None):
    s = rect(slide, l, t, w, h, fill=fill, shape=shape, radius=radius, line=line)
    tf = s.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.1
    r = p.add_run()
    r.text = label
    r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(size), True
    r.font.color.rgb = fg
    return s


def flow(slide, steps, l, t, w, box_h=Inches(0.5), gap=Inches(0.17),
         accent=CYAN):
    for i, label in enumerate(steps):
        y = t + i * (box_h + gap)
        last = i == len(steps) - 1
        s = chip(slide, l, y, w, box_h, label,
                 fill=accent if last else NAVY_SOFT, size=12, radius=0.06)
        if not last:
            text(slide, "\u25bc", l + w / 2 - Inches(0.15), y + box_h,
                 Inches(0.3), gap, 9, color=GREY_LIGHT, align=PP_ALIGN.CENTER)
    return t + len(steps) * (box_h + gap)


def stat(slide, l, t, w, h, value, label, accent=BLUE, fill=BLUE_LIGHT):
    rect(slide, l, t, w, h, fill=fill, radius=0.06)
    text(slide, value, l, t + Inches(0.12), w, Inches(0.46), 25, bold=True,
         color=accent, align=PP_ALIGN.CENTER)
    text(slide, label, l + Inches(0.1), t + Inches(0.62), w - Inches(0.2),
         h - Inches(0.7), 10, color=GREY, align=PP_ALIGN.CENTER, spacing=1.08)


def note(slide, body, l, t, w, h, accent=AMBER, fill=AMBER_LIGHT,
         line=AMBER_LINE, size=12, bold_lead=None):
    rect(slide, l, t, w, h, fill=fill, line=line, radius=0.05)
    if bold_lead:
        text(slide, bold_lead, l + Inches(0.26), t + Inches(0.13),
             w - Inches(0.5), Inches(0.26), size, bold=True, color=accent)
        text(slide, body, l + Inches(0.26), t + Inches(0.42), w - Inches(0.5),
             h - Inches(0.52), size - 0.5, color=NAVY, spacing=1.16)
    else:
        text(slide, body, l + Inches(0.26), t, w - Inches(0.5), h, size,
             color=accent, spacing=1.18, anchor=MSO_ANCHOR.MIDDLE)


# ============================================================== slide 1 ======
s = new_slide(footer=False)
rect(s, Inches(0), Inches(0), W, H, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, Inches(0), Inches(0), Inches(0.09), H, fill=CYAN, shape=MSO_SHAPE.RECTANGLE)
rect(s, W - Inches(4.4), Inches(0), Inches(4.4), H, fill=RGBColor(0x10, 0x28, 0x49),
     shape=MSO_SHAPE.RECTANGLE)

text(s, "CAPSTONE PROJECT  ·  SECURE FILE TRANSFER", Inches(1.05), Inches(1.28),
     Inches(7.6), Inches(0.3), 12, bold=True, color=RGBColor(0x62, 0xC8, 0xD8))
text(s, "Secure Resumable\nFile Transfer", Inches(1.05), Inches(1.7),
     Inches(7.7), Inches(1.9), 48, bold=True, color=WHITE, spacing=0.95)
rect(s, Inches(1.05), Inches(3.58), Inches(1.5), Inches(0.05), fill=CYAN,
     shape=MSO_SHAPE.RECTANGLE)
text(s, "A C++20 client\u2013server file transfer tool with end-to-end TLS "
        "encryption, automatic resumption after a dropped connection, and "
        "SHA-256 integrity verification on every upload.",
     Inches(1.05), Inches(3.88), Inches(7.3), Inches(0.9), 14.5, color=PALE,
     spacing=1.28)

tags = ["C++20", "TLS 1.2+", "SHA-256", "Resumable", "CMake", "51 tests"]
for i, tag in enumerate(tags):
    chip(s, Inches(1.05) + Inches(1.28) * i, Inches(4.94), Inches(1.16),
         Inches(0.36), tag, fill=RGBColor(0x17, 0x38, 0x5F), size=10,
         line=RGBColor(0x2C, 0x5A, 0x8C))

text(s, "Presented by", W - Inches(3.85), Inches(1.5), Inches(3.3), Inches(0.3),
     11, bold=True, color=CYAN)
text(s, AUTHOR, W - Inches(3.85), Inches(1.88), Inches(3.4), Inches(0.4), 22,
     bold=True, color=WHITE)
text(s, "Project author and maintainer", W - Inches(3.85), Inches(2.34),
     Inches(3.4), Inches(0.3), 11, color=PALE)

rows = [
    ("Repository", "github.com/zexxitywave/\nFile-transfer-", True),
    ("Version", "1.0.0", False),
    ("Language", "C++20", False),
    ("Platforms", "Windows and Linux", False),
    ("Tests", "51 end-to-end checks", False),
    ("License", "MIT", False),
]
y = Inches(3.0)
for label, value, mono in rows:
    text(s, label, W - Inches(3.85), y, Inches(1.5), Inches(0.26), 10.5,
         color=GREY_LIGHT)
    text(s, value, W - Inches(2.35), y - Inches(0.03), Inches(2.1),
         Inches(0.72), 12, bold=True, color=WHITE, font=MONO if mono else FONT,
         spacing=1.15)
    y += Inches(0.58) if mono else Inches(0.34)

text(s, "Secure Resumable File Transfer  ·  August 2026", Inches(1.05),
     Inches(6.42), Inches(7), Inches(0.3), 11, color=GREY_LIGHT)

# ============================================================== slide 2 ======
s = new_slide()
header(s, "The Problem, and the Answer", kicker="01  ·  Motivation")
text(s, "Why a conventional FTP upload is not good enough", MARGIN, Inches(1.4),
     Inches(7.5), Inches(0.3), 15, bold=True, color=NAVY)
bullets(s, [
    "Cleartext on the wire.||  FTP sends the username, the password and the file "
    "contents in plain text. Anyone on the path can read all of it.",
    "No resumption.||  A dropped connection restarts the transfer from byte zero. "
    "On a large file that wastes the bandwidth and the time already spent.",
    "Unverified delivery.||  Most tools declare success once a write() call "
    "returns. Nothing proves the bytes that landed on disk are correct.",
    "Silent corruption under concurrency.||  Two clients writing the same "
    "destination interleave their chunks into one mangled file, with no error.",
    "Unsafe file names.||  A name containing path separators lets the client "
    "choose where it writes on the server.",
], MARGIN, Inches(1.8), Inches(7.5), Inches(3.4), size=13.5, gap=13)

card(s, Inches(8.4), Inches(1.4), Inches(4.3), Inches(3.8),
     "What the brief asked for", [
         "A secure, system-level file transfer service",
         "Encrypted transport",
         "Reliability over an unreliable network",
         "Provable data integrity",
         "Multiple simultaneous clients",
     ], accent=CYAN, fill=CYAN_LIGHT, line=CYAN_LINE)

note(s, "A TLS-encrypted client\u2013server uploader that resumes an interrupted "
        "transfer from the last byte the server already holds, verifies every "
        "upload with SHA-256, and refuses unsafe requests before writing a byte.",
     MARGIN, Inches(5.45), CONTENT_W, Inches(1.0), accent=GREEN,
     fill=GREEN_LIGHT, line=GREEN_LINE, size=13.5, bold_lead="The answer")

# ============================================================== slide 3 ======
s = new_slide()
header(s, "Objectives and Scope", kicker="02  ·  Requirements")
card(s, MARGIN, Inches(1.4), Inches(6.05), Inches(3.4),
     "In scope \u2014 what the system does", [
         "Encrypt all traffic with TLS 1.2 or newer, using SNI",
         "Verify the server certificate by default: chain and host name",
         "Resume an interrupted upload from the last stored byte",
         "Verify integrity with SHA-256 after every transfer",
         "Serve several clients concurrently from a small thread pool",
         "Reject unsafe file names before anything is written",
         "Build and test on Linux and Windows from one CMake project",
     ], accent=GREEN, fill=GREEN_LIGHT, line=GREEN_LINE)
card(s, Inches(7.28), Inches(1.4), Inches(5.42), Inches(3.4),
     "Out of scope \u2014 deliberately not built", [
         "Download or retrieval. The client can only upload.",
         "Authentication. The server accepts any client that can reach the port.",
         "Authorisation or per-user accounts.",
         "Bulk directory synchronisation.",
         "A kernel-mode device driver, which the brief also asked for.",
     ], accent=AMBER, fill=AMBER_LIGHT, line=AMBER_LINE)
text(s, "Requirement traceability", MARGIN, Inches(5.05), Inches(6), Inches(0.3),
     14, bold=True, color=NAVY)
text(s, "All 20 functional and 12 non-functional requirements are listed in "
        "docs/PRD.md, and every one is traced to the automated check that covers "
        "it in docs/TEST_PLAN.md \u2014 there is no requirement without evidence.",
     MARGIN, Inches(5.42), CONTENT_W, Inches(0.6), 13, color=GREY, spacing=1.22)

# ============================================================== slide 4 ======
s = new_slide()
header(s, "Technology Stack", kicker="03  ·  What it is built with")
table(s, ["Layer", "Technology", "Why it was chosen"], [
    ("Language", "C++20", "RAII and move semantics for safe manual memory management"),
    ("Build system", "CMake 3.15+", "One project file builds MSVC, MinGW and GCC"),
    ("Networking", "Boost.Asio", "Header-only, portable over WinSock and BSD sockets, fully async"),
    ("Security", "OpenSSL 3.x", "Provides both the TLS transport and the EVP SHA-256 digest"),
    ("Concurrency", "std::thread pool", "A shared io_context run on 2 to 4 worker threads"),
    ("Testing", "Bash + PowerShell", "End-to-end scripts over real TLS, driven by CTest"),
    ("CI/CD", "GitHub Actions", "Builds and tests both platforms on every push"),
], MARGIN, Inches(1.42), CONTENT_W, widths=[2.3, 2.4, 7.3], size=12,
    head_size=11.5, row_h=Inches(0.5), head_h=Inches(0.42))
note(s, "Boost is headers only, so nothing Boost is linked. OpenSSL is linked, "
        "so both its headers and its libraries are required at build time. "
        "Measured on: Windows 11 x64 with GCC 16 (MSYS2 UCRT64, Ninja) and "
        "GCC 15.2 (MinGW-w64), OpenSSL 3.6.4, Boost 1.88, CMake 3.15+.",
     MARGIN, Inches(5.5), CONTENT_W, Inches(0.86), size=12)

# ============================================================== slide 5 ======
s = new_slide()
header(s, "System Architecture", kicker="04  ·  Six layers, one-directional dependencies")
layers = [
    ("Entry point", "main.cpp", "Command line parsing, certificate discovery, "
     "event loop, exit codes. No protocol logic.", BLUE),
    ("Transport", "server.cpp  \u00b7  client.cpp", "Accept and connect, own the TLS "
     "stream, drive the transfer.", CYAN),
    ("Session logic", "serverSession.cpp", "The protocol state machine: validation, "
     "chunk loop, integrity verdict, filename policy.", GREEN),
    ("Support", "checksum.cpp  \u00b7  logging.hpp", "Incremental SHA-256; thread-safe "
     "logging with a terminal-aware progress bar.", AMBER),
    ("Contract", "protocol.hpp", "Wire constants and status codes \u2014 the only "
     "vocabulary both sides share. No logic, so they cannot disagree.", NAVY_SOFT),
    ("Build", "CMakeLists.txt", "Dependency discovery, TLS asset staging, MinGW "
     "runtime staging, CTest registration.", GREY),
]
y = Inches(1.38)
LAYER_H, LAYER_GAP = Inches(0.74), Inches(0.1)
for i, (name, files, desc, colour) in enumerate(layers):
    rect(s, MARGIN, y, Inches(8.3), LAYER_H, fill=BG, line=LINE, radius=0.05)
    rect(s, MARGIN, y, Inches(0.05), LAYER_H, fill=colour, shape=MSO_SHAPE.RECTANGLE)
    text(s, name, MARGIN + Inches(0.22), y + Inches(0.1), Inches(1.5),
         Inches(0.24), 12, bold=True, color=colour)
    text(s, files, MARGIN + Inches(1.75), y + Inches(0.1), Inches(2.6),
         Inches(0.24), 11, bold=True, color=NAVY, font=MONO)
    text(s, desc, MARGIN + Inches(0.22), y + Inches(0.38), Inches(7.9),
         Inches(0.32), 10.5, color=GREY)
    if i < len(layers) - 1:
        text(s, "\u25bc", MARGIN + Inches(0.3), y + LAYER_H - Inches(0.02),
             Inches(0.3), Inches(0.14), 8, color=GREY_LIGHT, align=PP_ALIGN.CENTER)
    y += LAYER_H + LAYER_GAP

card(s, Inches(9.16), Inches(1.38), Inches(3.54), Inches(2.0),
     "Codebase size", [
         "11 files, 1,701 lines of C++",
         "6 headers (359 lines), 5 sources (1,342 lines)",
         "Largest file: serverSession.cpp, 495 lines",
     ], accent=BLUE)
card(s, Inches(9.16), Inches(3.52), Inches(3.54), Inches(2.32),
     "Design rules", [
         "Dependencies point one way only",
         "protocol.hpp and logging.hpp use nothing from the project",
         "Server is non-copyable by design",
         "Default port 9000, default host 127.0.0.1",
     ], accent=CYAN, fill=CYAN_LIGHT, line=CYAN_LINE)

# ============================================================== slide 6 ======
s = new_slide()
header(s, "Wire Protocol", kicker="05  ·  The contract between client and server")
code(s, """client                                  server
  |---- uint32  name_len --------------------->|
  |---- name_len bytes  filename -------------->|
  |---- 64 bytes  hex SHA-256 ----------------->|
  |---- uint64  file_size --------------------->|
  |                                           |  the whole request is
  |                                           |  validated BEFORE anything
  |                                           |  is stored
  |<--- 1 byte  status (proceed / refused) ----|
  |<--- uint64  resume_offset -----------------|  only when proceeding
  |---- payload, 64 KB chunks ---------------->|
  |<--- 1 byte  status (verified / failed) ----|""",
     MARGIN, Inches(1.38), Inches(7.5), Inches(3.58), size=12)
bullets(s, [
    "Validate, then refuse.||  A rejection is reported as a status byte, never as "
    "a misleading resume offset \u2014 otherwise a refused client would read the "
    "offset as truth and corrupt its file.",
    "Host byte order, one write per scalar.||  This removes struct padding as a "
    "source of corruption.",
    "The stored file length IS the resume offset.||  Uploads are saved as "
    "received_<name>, so there is no separate checkpoint to keep consistent.",
    "Five status codes.||  proceed / ok, checksum mismatch, rejected, busy, error.",
], Inches(8.3), Inches(1.42), Inches(4.4), Inches(3.5), size=12, gap=11)
note(s, "The protocol is not versioned, so a client and a server must be the "
        "same build. A version byte in the header is the first thing to add.",
     MARGIN, Inches(5.24), CONTENT_W, Inches(0.84), size=12.5,
     bold_lead="Known limitation")

# ============================================================== slide 7 ======
s = new_slide()
header(s, "Core Features \u2014 Encryption and Integrity",
       kicker="06  ·  Secure by default, and provable", accent=GREEN)
card(s, MARGIN, Inches(1.4), Inches(6.05), Inches(3.5),
     "Encrypted and verified transport", [
         "TLS 1.2 or newer via OpenSSL, with SNI; SSLv2 and SSLv3 disabled",
         "Chain AND host name verified by default, IP literals such as 127.0.0.1 "
         "included, via a custom host-verify callback",
         "Fail closed \u2014 with no CA to verify against, the client refuses to start",
         "No silent downgrade \u2014 --insecure exists for troubleshooting and warns",
         "The CA is found next to the executable, then in ./tls_key, and the "
         "resolved path is printed before connecting",
         "The server refuses to start without a certificate and a key",
     ], accent=GREEN, fill=GREEN_LIGHT, line=GREEN_LINE, size=11.5)
text(s, "Proven integrity, not reported integrity", Inches(7.28), Inches(1.4),
     Inches(5.42), Inches(0.3), 14, bold=True, color=NAVY)
steps = [
    ("Client hashes", "SHA-256 of the source, streamed through OpenSSL EVP"),
    ("Client declares", "the 64-character hex digest leads the request header"),
    ("Server hashes", "the stored bytes as they arrive, same EVP call"),
    ("Server compares", "computed against declared"),
    ("Verdict", "match \u2192 success, exit 0;  mismatch \u2192 file deleted, "
     "non-zero exit"),
]
y = Inches(1.82)
for i, (head, body) in enumerate(steps):
    last = i == len(steps) - 1
    h = Inches(0.6)
    rect(s, Inches(7.28), y, Inches(5.42), h, fill=GREEN_LIGHT if last else BG,
         line=GREEN_LINE if last else LINE, radius=0.05)
    rect(s, Inches(7.28), y, Inches(0.05), h, fill=GREEN if last else BLUE,
         shape=MSO_SHAPE.RECTANGLE)
    text(s, head, Inches(7.5), y + Inches(0.16), Inches(1.7), Inches(0.26),
         12, bold=True, color=GREEN if last else BLUE)
    text(s, body, Inches(9.2), y + Inches(0.08), Inches(3.4), Inches(0.46),
         11, color=GREY, spacing=1.12, anchor=MSO_ANCHOR.MIDDLE)
    y += h + Inches(0.1)
bullets(s, [
    "Bounded memory.||  The digest is computed incrementally through a 64 KB "
    "buffer, so hashing a 64 GiB file costs the same memory as hashing 64 KB.",
    "A mismatch deletes the evidence.||  The stored file is removed, so a later "
    "resume cannot build on corrupt bytes. Tested by deliberately tampering with "
    "a stored file and checking it is rejected.",
], Inches(7.28), Inches(5.1), Inches(5.42), Inches(1.62), size=11.5, gap=8)

# ============================================================== slide 8 ======
s = new_slide()
header(s, "Core Features \u2014 Resumption and Concurrency",
       kicker="06  ·  Reliable over a bad link, safe under load", accent=CYAN)
text(s, "Automatic resumption", MARGIN, Inches(1.38), Inches(4.6), Inches(0.3),
     14, bold=True, color=NAVY)
end = flow(s, [
    "Client starts the upload",
    "Connection is lost mid-transfer",
    "Client reconnects, re-sends the header",
    "Server replies with its resume offset",
    "Only the missing bytes are sent",
    "Transfer completes and is verified",
], MARGIN, Inches(1.78), Inches(4.6), box_h=Inches(0.44), gap=Inches(0.14))
note(s, "No checkpoint file: the resume offset is simply the current size of "
        "received_<name> on disk, so there is no extra state to corrupt and it "
        "survives a server restart for free. A stored copy larger than the source "
        "is treated as stale and restarted from zero.",
     MARGIN, end + Inches(0.05), Inches(4.6), Inches(1.6), accent=CYAN,
     fill=CYAN_LIGHT, line=CYAN_LINE, size=11.5, bold_lead="Derived state")

text(s, "Concurrent and write-safe", Inches(5.6), Inches(1.38), Inches(7.1),
     Inches(0.3), 14, bold=True, color=NAVY)
bullets(s, [
    "Worker pool of 2 to 4 threads.||  min(4, hardware_concurrency) with a floor "
    "of 2, all running one shared io_context. The client runs a single thread.",
    "One operation in flight per session.||  Each step is asynchronous, so a "
    "session's handlers are serialised by construction rather than by a lock, "
    "and a slow client never occupies a worker.",
    "A 64 KB chunk buffer, allocated once per session||  and reused for every "
    "chunk, so there is no per-chunk allocation.",
    "One writer per destination.||  A second client asking for a name already in "
    "use is refused as busy and exits non-zero, rather than writing over the "
    "transfer in progress. The claim is released on every exit path.",
    "Minimal shared state.||  Only the destination claim set and the log are "
    "shared, both guarded by a mutex.",
], Inches(5.6), Inches(1.78), Inches(7.1), Inches(3.45), size=12, gap=10)
stat(s, Inches(5.6), Inches(5.34), Inches(1.68), Inches(1.3), "4",
     "concurrent uploads\nverified intact", accent=GREEN, fill=GREEN_LIGHT)
stat(s, Inches(7.46), Inches(5.34), Inches(1.68), Inches(1.3), "2\u20134",
     "worker\nthreads", accent=BLUE)
stat(s, Inches(9.32), Inches(5.34), Inches(1.68), Inches(1.3), "64 KB",
     "chunk\nsize", accent=CYAN, fill=CYAN_LIGHT)
stat(s, Inches(11.18), Inches(5.34), Inches(1.52), Inches(1.3), "1",
     "writer per\ndestination", accent=AMBER, fill=AMBER_LIGHT)

# ============================================================== slide 9 ======
s = new_slide()
header(s, "Security Design", kicker="07  ·  Controls, and their limits", accent=RED)
table(s, ["Control", "How it is implemented"], [
    ("Encrypted transport", "TLS 1.2 or newer via OpenSSL, with SNI; SSLv2 and SSLv3 disabled"),
    ("Certificate verification", "Chain and host name checked by default, IP literals such as 127.0.0.1 included"),
    ("No silent downgrade", "--insecure is available for troubleshooting only, and prints a warning"),
    ("Fail closed", "The client refuses to start when it has no CA to verify against"),
    ("Strict name validation", "No path separators, no .., no control characters, no reserved device names; max 255 characters, max 64 GiB"),
    ("Integrity", "SHA-256 compared after every transfer; a mismatch deletes the stored file"),
    ("Exclusive writes", "One writer per destination; contention is refused as busy rather than overwritten"),
], MARGIN, Inches(1.4), CONTENT_W, widths=[3.0, 9.0], size=12, head_size=11.5,
    row_h=Inches(0.46), head_h=Inches(0.42))
note(s, "Any client that can reach the port may upload. The system must not be "
        "exposed to an untrusted network. docs/SECURITY.md documents the threat "
        "model and how to harden a deployment.",
     MARGIN, Inches(5.06), CONTENT_W, Inches(0.96), accent=RED, fill=RED_LIGHT,
     line=RED_LINE, size=12.5, bold_lead="The honest limit: the server "
     "authenticates nobody.")

# ============================================================= slide 10 ======
s = new_slide()
header(s, "Testing and Measured Results", kicker="08  ·  Verification from the outside")
stats = [
    ("~267 MB/s", "8 MB transfer on loopback,\ndigests matched", GREEN, GREEN_LIGHT),
    ("0.03 s", "wall-clock for that\n8 MB transfer", BLUE, BLUE_LIGHT),
    ("220 MB", "interrupted then resumed,\nfinal digest matched", CYAN, CYAN_LIGHT),
    ("51", "automated checks:\n50 passed, 1 skipped", GREEN, GREEN_LIGHT),
]
for i, (v, l, a, f) in enumerate(stats):
    stat(s, MARGIN + Inches(2.98) * i, Inches(1.38), Inches(2.72), Inches(1.24),
         v, l, accent=a, fill=f)

text(s, "How it is tested", MARGIN, Inches(2.78), Inches(6.4), Inches(0.3), 14,
     bold=True, color=NAVY)
bullets(s, [
    "No mocks and no unit-test framework.||  The suite starts a real server and "
    "drives real clients over real TLS, then checks the outcome from outside the "
    "process. Every defect on the next slide was found this way.",
    "Registered with CTest,||  so CI and a developer run the identical thing. The "
    "Windows suite covers the whole requirement list; a Bash smoke test gives "
    "Linux CI one real transfer with an externally computed SHA-256.",
    "Measured on three toolchain configurations,||  including a run with an empty "
    "PATH: 50 passed, 0 failed, 1 skipped. A real 14,466-byte PDF invoice was "
    "verified with an external SHA-256 tool and a byte-for-byte comparison.",
], MARGIN, Inches(3.16), Inches(6.4), Inches(2.4), size=11, gap=8)

note(s, "Windows 11 Home x64  \u00b7  GCC 16.x, MSYS2 UCRT64, Ninja  \u00b7  "
        "GCC 15.2, MinGW-w64 (CLion)  \u00b7  OpenSSL 3.6.4  \u00b7  Boost 1.88 "
        "headers  \u00b7  CMake 3.15+  \u00b7  PowerShell 5.1",
     MARGIN, Inches(5.66), Inches(6.4), Inches(0.72), accent=BLUE,
     fill=BLUE_LIGHT, size=11.5)
note(s, "Not yet done: the full 997-file bulk run, and a cross-machine transfer.",
     MARGIN, Inches(6.46), Inches(6.4), Inches(0.52), size=11)

table(s, ["Test group", "Checks", "Covers"], [
    ("Command line handling", "10", "FR-17, FR-19"),
    ("Clean transfer", "6", "FR-01, FR-02, FR-06, FR-14"),
    ("Certificate verification", "4+1 skip", "FR-03, FR-04, FR-05"),
    ("Integrity", "5", "FR-12, FR-13, FR-18"),
    ("Resuming", "5", "FR-08, FR-09"),
    ("Interruption", "5", "FR-20"),
    ("Concurrency", "14", "FR-10, FR-11"),
    ("Server with no certificate", "1", "FR-16"),
], Inches(7.28), Inches(2.78), Inches(5.42), widths=[3.0, 1.3, 2.9], size=10,
    head_size=10.5, row_h=Inches(0.235), head_h=Inches(0.3))

card(s, Inches(7.28), Inches(5.06), Inches(5.42), Inches(1.5),
     "Also verified", [
         "24 MB resume sent only the missing bytes",
         "Four concurrent uploads, all intact",
         "Every one of the 20 requirements traced",
     ], accent=GREEN, fill=GREEN_LIGHT, line=GREEN_LINE, size=10.5)

# ============================================================= slide 11 ======
s = new_slide()
header(s, "Defects Found and Fixed by the Suite",
       kicker="09  ·  What testing actually caught", accent=AMBER)
defects = [
    ("1", "Server could not replace a stale upload on Windows",
     "A leftover partial file blocked the next transfer"),
    ("2", "A killed client's failure was invisible to the test script",
     "The suite passed while the client had died"),
    ("3", "The busy check failed intermittently",
     "A race between claiming and releasing a destination"),
    ("4", "Concurrent sessions produced garbled log lines",
     "Interleaved writes from several threads on one line"),
    ("5", "A redirected server log was buried under progress updates",
     "Progress is now drawn only when the output is a terminal"),
    ("6", "Transfer rate printed as 0.0286102",
     "A floating-point formatting defect, now two decimals"),
    ("7", "The MinGW build produced no output and returned instantly",
     "Exit code 0xC0000135 from missing runtime DLLs; now staged by the build"),
    ("8", "Client failed to verify the certificate from another directory",
     "The CA is now looked up next to the executable"),
]
for i, (num, title, detail) in enumerate(defects):
    col, row = divmod(i, 4)
    x = MARGIN + col * Inches(6.35)
    y = Inches(1.44) + row * Inches(1.0)
    rect(s, x, y, Inches(5.98), Inches(0.86), fill=BG, line=LINE, radius=0.05)
    badge(s, x + Inches(0.16), y + Inches(0.26), Inches(0.34), Inches(0.34),
          num, AMBER, size=11)
    text(s, title, x + Inches(0.62), y + Inches(0.13), Inches(5.2), Inches(0.4),
         12, bold=True, color=NAVY, spacing=1.1)
    text(s, detail, x + Inches(0.62), y + Inches(0.54), Inches(5.2),
         Inches(0.26), 10.5, color=GREY, spacing=1.05)
note(s, "It printed nothing, returned success, and only appeared on MinGW. It is "
        "the reason CI runs the same MinGW toolchain as the local build.",
     MARGIN, Inches(5.62), CONTENT_W, Inches(0.8), size=12,
     bold_lead="Defect 7 was the worst-shaped of the eight.")

# ============================================================= slide 12 ======
s = new_slide()
header(s, "CI/CD Pipeline and Design Decisions",
       kicker="10  ·  Automated verification, deliberate choices", accent=CYAN)
card(s, MARGIN, Inches(1.38), Inches(6.05), Inches(2.32),
     "ci.yml \u2014 every push and pull request", [
         "Linux (ubuntu-latest): install dependencies, generate the certificate, "
         "configure Release with Ninja, build, run the smoke test",
         "Windows (MSYS2 UCRT64): the same toolchain family as the local build, "
         "so CI catches MinGW-specific problems",
         "Runs the full ctest suite; uploads logs and received files as artefacts "
         "on failure",
     ], accent=GREEN, fill=GREEN_LIGHT, line=GREEN_LINE, size=11)
card(s, Inches(7.28), Inches(1.38), Inches(5.42), Inches(2.32),
     "release.yml \u2014 on a v* tag", [
         "verify: greps the version out of CMakeLists.txt and fails the release if "
         "the tag does not match it",
         "Builds and tests both platforms, then packages a Linux tar.gz and a "
         "Windows zip containing every DLL",
         "Generates SHA256SUMS.txt and publishes only when all jobs succeed",
     ], accent=BLUE, size=11)

text(s, "Design decisions: what was chosen, and what was rejected", MARGIN,
     Inches(3.86), Inches(9), Inches(0.3), 14, bold=True, color=NAVY)
table(s, ["Decision", "Rejected", "Reason"], [
    ("Async, one operation in flight", "Thread per connection",
     "A thread per client cannot scale, and a blocking session pins a worker"),
    ("Resume offset = stored file length", "A checkpoint file",
     "No extra state to corrupt, and it survives a server restart for free"),
    ("Validate the header, then refuse", "Accept, then discover",
     "A refusal must never be mistakable for a resume instruction"),
    ("One writer per destination", "Last-writer-wins",
     "Stops two clients silently interleaving chunks into one corrupt file"),
    ("Incremental EVP hashing", "Load the file into memory",
     "Bounded memory: 64 GiB costs the same as 64 KB"),
    ("Host byte order, one write per scalar", "A packed struct on the wire",
     "Removes struct padding as a source of corruption"),
], MARGIN, Inches(4.24), Inches(9.1), widths=[3.1, 2.4, 4.6], size=10.5,
    head_size=10.5, row_h=Inches(0.35), head_h=Inches(0.3))

card(s, Inches(9.9), Inches(4.24), Inches(2.8), Inches(2.4),
     "Also in the repo", [
         "Dependabot v2",
         "Bug and feature issue templates",
         "Pull request template",
         "The version lives only in CMakeLists.txt, so a build and a release "
         "cannot drift apart",
     ], accent=CYAN, fill=CYAN_LIGHT, line=CYAN_LINE, size=10.5)

# ============================================================= slide 13 ======
s = new_slide()
header(s, "Challenges, Limitations and Future Scope",
       kicker="11  ·  The hard parts, and what is next", accent=CYAN)
text(s, "Challenges faced, and what they taught", MARGIN, Inches(1.38),
     Inches(6.05), Inches(0.3), 14, bold=True, color=NAVY)
bullets(s, [
    "Making the busy check reliable.||  A race between claiming and releasing a "
    "destination caused intermittent failures; fixed with a mutex-guarded set "
    "and a release on every exit path.",
    "Thread-safe logging with a live progress bar.||  Concurrent sessions "
    "interleaved their writes into garbled lines; fixed with a logging mutex and "
    "in-place redraw.",
    "MinGW and OpenSSL.||  FindOpenSSL ignores MinGW's libssl.a, and the build "
    "failed silently with 0xC0000135; fixed with a header and library search "
    "fallback plus automatic DLL staging.",
    "Certificate lookup from any directory.||  Verification failed when the "
    "client ran from elsewhere; fixed by looking next to the executable and "
    "printing the resolved path before connecting.",
    "Async handler chains.||  Keeping exactly one operation in flight without a "
    "deadlock or a use-after-free when a session is aborted mid-chain.",
    "The lesson:||  every real defect came from running real transfers, not from "
    "reading the code. That is now how I test my own work.",
], MARGIN, Inches(1.76), Inches(6.05), Inches(4.5), size=11.5, gap=9)

card(s, Inches(7.28), Inches(1.38), Inches(5.42), Inches(3.02),
     "Current limitations", [
         "No download path.||  The client can only upload; retrieval is the "
         "highest-value feature to add.",
         "The server authenticates nobody.||  No accounts, no authorisation.",
         "The device-driver component of the brief is not covered.||  The "
         "system is C++20 with system-level networking but has no kernel module.",
         "The protocol is not versioned,||  so client and server must be the "
         "same build. The 997-file bulk run and a cross-machine transfer are "
         "not done.",
     ], accent=AMBER, fill=AMBER_LIGHT, line=AMBER_LINE, size=11)
card(s, Inches(7.28), Inches(4.54), Inches(5.42), Inches(2.04),
     "Planned next", [
         "Download with the same integrity model, and resumable downloads",
         "Mutual TLS, so the server can authenticate the client",
         "Directory sync and multi-file transfers",
         "A version byte in the header, then Linux and macOS releases",
     ], accent=GREEN, fill=GREEN_LIGHT, line=GREEN_LINE, size=11)

# ============================================================= slide 14 ======
s = new_slide()
header(s, "Demonstration", kicker="12  ·  Five minutes, live")
demo = [
    ("1", "Clean build and a single transfer",
     "Generate the certificate, configure, build, start the server, send an 8 MB "
     "file. The client prints the throughput and the server confirms the hash."),
    ("2", "Interrupt and resume",
     "Start a 220 MB upload, kill the client mid-transfer, re-run the same "
     "command. The server reports the bytes it already holds and the transfer "
     "continues from there."),
    ("3", "Concurrent clients",
     "Run four uploads at once. All four complete intact, and a fifth asking for "
     "a busy destination is refused as busy with a non-zero exit."),
    ("4", "Integrity failure",
     "Tamper with a stored file. The digest no longer matches, so the file is "
     "deleted and the client exits non-zero."),
]
y = Inches(1.42)
for num, head, body in demo:
    h = Inches(1.16)
    rect(s, MARGIN, y, Inches(9.3), h, fill=BG, line=LINE, radius=0.05)
    badge(s, MARGIN + Inches(0.2), y + Inches(0.37), Inches(0.42), Inches(0.42),
          num, BLUE, size=13)
    text(s, head, MARGIN + Inches(0.78), y + Inches(0.18), Inches(8.2),
         Inches(0.28), 13.5, bold=True, color=NAVY)
    text(s, body, MARGIN + Inches(0.78), y + Inches(0.52), Inches(8.2),
         Inches(0.6), 11.5, color=GREY, spacing=1.15)
    y += h + Inches(0.14)
card(s, Inches(10.2), Inches(1.42), Inches(2.5), Inches(2.2),
     "Before the demo", [
         "Clean build directory",
         "Certificate present",
         "Test files ready",
     ], accent=CYAN, fill=CYAN_LIGHT, line=CYAN_LINE, size=11)
text(s, "Steps 2 to 4 are the ones that separate this from a file copy.",
     Inches(10.2), Inches(3.82), Inches(2.5), Inches(1.2), 12, color=GREY,
     spacing=1.2)
code(s, """./FTP server 9000
# [SERVER] Listening on 9000
#   (TLS enabled)
$ ./FTP client ../note.txt
# [SUCCESS] Server verified the
#   file (hash matches)""",
     Inches(10.2), Inches(4.9), Inches(2.5), Inches(1.5), size=7)

# ============================================================= slide 15 ======
s = new_slide()
header(s, "Conclusion", kicker="12  ·  What was delivered")
bullets(s, [
    "A working secure file transfer system.||  A C++20 client\u2013server uploader "
    "with end-to-end TLS, automatic resumption after a dropped connection, and "
    "SHA-256 verification on every upload.",
    "Deliberate engineering decisions.||  Six documented layers with "
    "one-directional dependencies, an asynchronous design that serves many "
    "clients from a 2 to 4 thread pool, and one writer per destination.",
    "Proven, not asserted.||  51 automated end-to-end checks over real TLS, all "
    "20 functional requirements traced to evidence, 8 real defects found and "
    "fixed, and ~267 MB/s measured on loopback.",
    "Reproducible anywhere.||  One CMake project builds and tests on Linux and "
    "Windows; GitHub Actions verifies both on every push, and tagged releases "
    "publish checksums.",
    "Documented for review.||  PRD, architecture, UML, development plan, test "
    "plan, changelog, contribution guide, security policy and code of conduct, "
    "all in the repository.",
], MARGIN, Inches(1.46), Inches(8.2), Inches(4.4), size=13, gap=14)
summary = [
    ("1,701", "lines of C++ across\n11 files", BLUE, BLUE_LIGHT),
    ("51", "automated checks\n50 passed, 1 skipped", GREEN, GREEN_LIGHT),
    ("8", "defects found\nand fixed", AMBER, AMBER_LIGHT),
    ("2", "platforms\nLinux and Windows", CYAN, CYAN_LIGHT),
]
for i, (v, l, a, f) in enumerate(summary):
    stat(s, Inches(9.35), Inches(1.46) + Inches(1.28) * i, Inches(3.35),
         Inches(1.16), v, l, accent=a, fill=f)
note(s, "Thank you \u2014 questions and feedback are welcome.",
     MARGIN, Inches(6.14), CONTENT_W, Inches(0.62), accent=GREEN,
     fill=GREEN_LIGHT, line=GREEN_LINE, size=13)

# ============================================================= slide 16 ======
s = new_slide(footer=False)
rect(s, Inches(0), Inches(0), W, H, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, Inches(0), Inches(0), W, Inches(0.09), fill=CYAN, shape=MSO_SHAPE.RECTANGLE)
text(s, "Thank you", Inches(1.2), Inches(1.95), Inches(10.9), Inches(1.0), 52,
     bold=True, color=WHITE, align=PP_ALIGN.CENTER)
rect(s, W / 2 - Inches(0.75), Inches(3.08), Inches(1.5), Inches(0.05), fill=CYAN,
     shape=MSO_SHAPE.RECTANGLE)
text(s, "Questions and feedback are welcome", Inches(1.2), Inches(3.4),
     Inches(10.9), Inches(0.4), 17, color=PALE, align=PP_ALIGN.CENTER)
text(s, "Secure Resumable File Transfer  ·  C++20  ·  TLS 1.2+  ·  SHA-256  ·  CMake",
     Inches(1.2), Inches(4.12), Inches(10.9), Inches(0.3), 12.5, color=CYAN,
     align=PP_ALIGN.CENTER)
chip(s, Inches(4.05), Inches(4.72), Inches(5.23), Inches(0.62), REPO,
     fill=RGBColor(0x10, 0x28, 0x49), size=13, radius=0.1,
     line=RGBColor(0x2C, 0x5A, 0x8C))
text(s, f"Presented by {AUTHOR}  ·  Maintainer, Secure Resumable File Transfer  "
        "·  MIT licensed  ·  Version 1.0.0",
     Inches(1.2), Inches(5.72), Inches(10.9), Inches(0.3), 11.5,
     color=GREY_LIGHT, align=PP_ALIGN.CENTER)
text(s, "Source, docs, tests and CI: github.com/zexxitywave/File-transfer-",
     Inches(1.2), Inches(6.06), Inches(10.9), Inches(0.3), 11,
     color=RGBColor(0x4A, 0x5A, 0x70), align=PP_ALIGN.CENTER)

prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides)} slides)")