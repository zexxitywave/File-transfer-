"""Generate the project presentation for the FTP server / SRFT project.

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
GREEN = RGBColor(0x1E, 0x8E, 0x5A)
GREEN_LIGHT = RGBColor(0xE7, 0xF6, 0xEF)
AMBER = RGBColor(0xB5, 0x6E, 0x00)
AMBER_LIGHT = RGBColor(0xFD, 0xF3, 0xE0)
RED = RGBColor(0xC0, 0x39, 0x2B)
RED_LIGHT = RGBColor(0xFC, 0xEC, 0xEA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
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
        text(s, f"Secure Resumable File Transfer  ·  v1.0.0",
             MARGIN, H - Inches(0.46), Inches(7), Inches(0.28),
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
    """items: list of str, or (str, level) tuples. Level 1 uses an en-dash."""
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
        head, sep, tail = body.partition("||")
        if sep:
            r = p.add_run()
            r.text = f"{marker if level == 0 else '\u2013'}  "
            r.font.name, r.font.size, r.font.color.rgb = FONT, Pt(size), BLUE
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
            r.text = f"{marker if level == 0 else '\u2013'}  "
            r.font.name, r.font.size, r.font.color.rgb = FONT, Pt(size), BLUE
            r = p.add_run()
            r.text = tail
            r.font.name, r.font.size = FONT, Pt(size)
            r.font.color.rgb = color
    return box


def rect(slide, l, t, w, h, fill=BLUE_LIGHT, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         radius=0.05):
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


def code(slide, body, l, t, w, h, size=12.5, fill=NAVY, fg=RGBColor(0xD8, 0xE6, 0xF5)):
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
    shape = slide.shapes.add_table(n_rows, n_cols, l, t, w, head_h + row_h * len(rows))
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

    def fill(cell, rgb):
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb

    for c, head in enumerate(headers):
        cell = tbl.cell(0, c)
        fill(cell, NAVY)
        cell.margin_left = cell.margin_right = Inches(0.1)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = head
        r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(head_size), True
        r.font.color.rgb = WHITE

    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            fill(cell, WHITE if ri % 2 else BG)
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.line_spacing = 1.05
            r = p.add_run()
            r.text = val
            r.font.name = FONT_BOLD if (ci == 0 and align_first_bold) else FONT
            r.font.size = Pt(size)
            r.font.bold = ci == 0 and align_first_bold
            r.font.color.rgb = NAVY if ci == 0 else GREY
    return tbl


def card(slide, l, t, w, h, title, items, accent=BLUE, fill=BLUE_LIGHT,
         title_size=14, size=11.5):
    rect(slide, l, t, w, h, fill=fill, radius=0.04)
    rect(slide, l, t, Inches(0.055), h, fill=accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, title, l + Inches(0.24), t + Inches(0.16), w - Inches(0.4),
         Inches(0.34), title_size, bold=True, color=NAVY)
    bullets(slide, items, l + Inches(0.24), t + Inches(0.58), w - Inches(0.42),
            h - Inches(0.7), size=size, gap=6, spacing=1.1)


def badge(slide, l, t, w, h, label, fill, size=13, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
          radius=0.2):
    """A centred number/label chip with no vertical text margin, so the glyph
    cannot overflow the shape."""
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


def flow(slide, steps, l, t, w, box_h=Inches(0.52), gap=Inches(0.2),
         accent=CYAN, fill=RGBColor(0xEC, 0xF6, 0xF8)):
    for i, label in enumerate(steps):
        y = t + i * (box_h + gap)
        colour = accent if i == len(steps) - 1 else NAVY_SOFT
        s = rect(slide, l, y, w, box_h, fill=colour, radius=0.06)
        tf = s.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = label
        r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(12.5), True
        r.font.color.rgb = WHITE
        if i < len(steps) - 1:
            text(slide, "\u25bc", l + w / 2 - Inches(0.15), y + box_h,
                 Inches(0.3), gap, 10, color=GREY_LIGHT, align=PP_ALIGN.CENTER)


def stat(slide, l, t, w, h, value, label, accent=BLUE, fill=BLUE_LIGHT):
    rect(slide, l, t, w, h, fill=fill, radius=0.06)
    text(slide, value, l, t + Inches(0.14), w, Inches(0.5), 27, bold=True,
         color=accent, align=PP_ALIGN.CENTER)
    text(slide, label, l + Inches(0.12), t + Inches(0.68), w - Inches(0.24),
         h - Inches(0.76), 10.5, color=GREY, align=PP_ALIGN.CENTER, spacing=1.1)


# ============================================================== slide 1 ======
s = new_slide(footer=False)
rect(s, Inches(0), Inches(0), W, H, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, Inches(0), Inches(0), Inches(0.09), H, fill=CYAN, shape=MSO_SHAPE.RECTANGLE)
rect(s, W - Inches(4.5), Inches(0), Inches(4.5), H,
     fill=RGBColor(0x10, 0x28, 0x49), shape=MSO_SHAPE.RECTANGLE)

text(s, "CAPSTONE PROJECT  ·  SECURE FILE TRANSFER", Inches(1.05), Inches(1.32),
     Inches(7.6), Inches(0.3), 12, bold=True, color=RGBColor(0x62, 0xC8, 0xD8))
text(s, "Secure Resumable\nFile Transfer", Inches(1.05), Inches(1.75),
     Inches(7.7), Inches(1.9), 48, bold=True, color=WHITE, spacing=0.95)
rect(s, Inches(1.05), Inches(3.62), Inches(1.5), Inches(0.05), fill=CYAN,
     shape=MSO_SHAPE.RECTANGLE)
text(s, "A C++20 client\u2013server file transfer tool with end-to-end TLS "
        "encryption, automatic resumption after a dropped connection, and "
        "SHA-256 integrity verification on every upload.",
     Inches(1.05), Inches(3.92), Inches(7.3), Inches(0.9), 14.5,
     color=RGBColor(0xB8, 0xCA, 0xDE), spacing=1.28)

for i, tag in enumerate(["C++20", "TLS 1.2+", "SHA-256", "Resumable", "CMake"]):
    x = Inches(1.05) + Inches(1.44) * i
    sh = rect(s, x, Inches(4.98), Inches(1.28), Inches(0.36),
              fill=RGBColor(0x17, 0x38, 0x5F), line=RGBColor(0x2C, 0x5A, 0x8C))
    sh.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = sh.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = tag
    r.font.name, r.font.size, r.font.bold = FONT_BOLD, Pt(10.5), True
    r.font.color.rgb = RGBColor(0x9E, 0xD8, 0xE6)

text(s, "Presented by", W - Inches(3.95), Inches(1.5), Inches(3.4),
     Inches(0.3), 11, bold=True, color=CYAN)
text(s, "[ Your Full Name ]\n[ Roll No / Regd. No ]\n[ Department, College ]",
     W - Inches(3.95), Inches(1.9), Inches(3.5), Inches(1.5), 16, bold=True,
     color=WHITE, spacing=1.42)
text(s, "Project Guide", W - Inches(3.95), Inches(3.62), Inches(3.4),
     Inches(0.3), 11, bold=True, color=CYAN)
text(s, "[ Faculty Name ]", W - Inches(3.95), Inches(4.02), Inches(3.5),
     Inches(0.4), 16, bold=True, color=WHITE)
text(s, "Repository", W - Inches(3.95), Inches(4.86), Inches(3.4),
     Inches(0.3), 11, bold=True, color=CYAN)
text(s, "github.com/zexxitywave/\nFile-transfer-", W - Inches(3.95),
     Inches(5.26), Inches(3.5), Inches(0.7), 13, color=RGBColor(0xB8, 0xCA, 0xDE),
     font=MONO, spacing=1.25)
text(s, "Version 1.0.0  ·  August 2026", Inches(1.05), Inches(6.42),
     Inches(7), Inches(0.3), 11, color=GREY_LIGHT)

# ============================================================== slide 2 ======
s = new_slide()
header(s, "Agenda", kicker="What this talk covers")
agenda = [
    ("01", "Problem & Motivation", "Why a plain FTP upload is not good enough"),
    ("02", "Objectives & Scope", "What the system must and must not do"),
    ("03", "Technology Stack", "Languages, libraries and tooling"),
    ("04", "System Architecture", "Six layers, one-directional dependencies"),
    ("05", "Wire Protocol", "The handshake and the 64 KB chunk loop"),
    ("06", "Core Features", "TLS, resumption, integrity, concurrency"),
    ("07", "Security Design", "Controls and honest threat-model limits"),
    ("08", "Testing & Results", "51 end-to-end checks and measured throughput"),
    ("09", "Defects Found & Fixed", "8 real bugs the suite caught"),
    ("10", "CI/CD Pipeline", "GitHub Actions on Linux and Windows"),
    ("11", "Design Decisions", "Alternatives rejected, and why"),
    ("12", "Challenges & Learnings", "The hard parts, honestly"),
    ("13", "Limitations & Future Scope", "What is not built yet"),
    ("14", "Demo, Conclusion & Q&A", "Live run of the system"),
]
col_w, row_h = Inches(6.05), Inches(0.35)
for i, (num, name, sub) in enumerate(agenda):
    col, row = divmod(i, 7)
    x = MARGIN + col * (col_w + Inches(0.32))
    y = Inches(1.5) + row * (row_h + Inches(0.16))
    text(s, num, x, y, Inches(0.45), row_h, 12.5, bold=True, color=BLUE)
    text(s, name, x + Inches(0.45), y, Inches(2.6), row_h, 13, bold=True,
         color=NAVY)
    text(s, sub, x + Inches(3.02), y + Inches(0.02), col_w - Inches(3.02),
         row_h, 10.5, color=GREY_LIGHT)

# ============================================================== slide 3 ======
s = new_slide()
header(s, "Problem & Motivation", kicker="01  ·  Why this project exists")
text(s, "The problems with a conventional FTP upload", MARGIN, Inches(1.42),
     CONTENT_W, Inches(0.3), 15, bold=True, color=NAVY)
bullets(s, [
    "Cleartext on the wire.||  FTP sends the username, the password and the file "
    "contents in plain text. Anyone on the path can read all of it.",
    "No resumption.||  A dropped connection means the transfer restarts from byte "
    "zero. On a large file that wastes the bandwidth and the time already spent.",
    "Unverified delivery.||  Most tools declare success once a write() call "
    "returns. Nothing proves the bytes that actually landed on disk are correct.",
    "Silent corruption under concurrency.||  Two clients writing the same "
    "destination interleave their chunks into one mangled file, with no error.",
    "Unsafe file names.||  A name containing path separators lets a client "
    "choose where it writes on the server.",
], MARGIN, Inches(1.82), Inches(7.55), Inches(3.6), size=13.5, gap=13)

card(s, Inches(8.45), Inches(1.42), Inches(4.25), Inches(3.7),
     "The requirement from the brief", [
         "A secure, system-level file transfer service",
         "Encrypted transport",
         "Reliable transfer over an unreliable network",
         "Provable data integrity",
         "Multiple simultaneous clients",
     ], accent=CYAN, fill=RGBColor(0xEC, 0xF6, 0xF8))

rect(s, MARGIN, Inches(5.5), CONTENT_W, Inches(1.32), fill=GREEN_LIGHT,
     line=RGBColor(0xBF, 0xE3, 0xD1))
text(s, "The solution", MARGIN + Inches(0.3), Inches(5.66), Inches(2.2),
     Inches(0.3), 13, bold=True, color=GREEN)
text(s, "A TLS-encrypted client\u2013server uploader that resumes an interrupted "
        "transfer from the last byte the server already holds, verifies every "
        "upload with SHA-256, and refuses unsafe requests before writing a byte.",
     MARGIN + Inches(2.5), Inches(5.66), Inches(9.2), Inches(1.0), 13.5,
     color=NAVY, spacing=1.24)

# ============================================================== slide 4 ======
s = new_slide()
header(s, "Objectives & Scope", kicker="02  ·  Requirements")
card(s, MARGIN, Inches(1.45), Inches(6.05), Inches(3.55),
     "In scope \u2014 what the system does", [
         "Encrypt all traffic with TLS 1.2 or newer, using SNI",
         "Verify the server certificate by default: chain and host name",
         "Resume an interrupted upload from the last stored byte",
         "Verify integrity with SHA-256 after every transfer",
         "Serve several clients concurrently from a small thread pool",
         "Reject unsafe file names before anything is written",
         "Build and test on both Linux and Windows from one CMake project",
     ], accent=GREEN, fill=GREEN_LIGHT)
card(s, Inches(7.28), Inches(1.45), Inches(5.42), Inches(3.55),
     "Out of scope \u2014 deliberately not built", [
         "Download / retrieval. The client can only upload.",
         "Authentication. The server accepts any client that can reach the port.",
         "Authorisation or per-user accounts.",
         "Bulk directory synchronisation.",
         "A kernel-mode device driver, which the original brief also asked for.",
     ], accent=AMBER, fill=AMBER_LIGHT)
text(s, "Requirement traceability", MARGIN, Inches(5.28), Inches(6), Inches(0.3),
     14, bold=True, color=NAVY)
text(s, "All 20 functional and 12 non-functional requirements are listed in "
        "docs/PRD.md. Every one is traced to the automated check that covers it "
        "in docs/TEST_PLAN.md \u2014 there is no requirement without evidence.",
     MARGIN, Inches(5.66), CONTENT_W, Inches(0.9), 13, color=GREY, spacing=1.24)

# ============================================================== slide 5 ======
s = new_slide()
header(s, "Technology Stack", kicker="03  ·  What it is built with")
table(s, ["Layer of the stack", "Technology", "Why it was chosen"], [
    ("Language", "C++20", "RAII, move semantics and coroutine-ready async for safe manual memory management"),
    ("Build system", "CMake 3.15+", "One project file builds MSVC, MinGW and GCC from the same sources"),
    ("Networking", "Boost.Asio", "Header-only, portable over WinSock and BSD sockets, fully async"),
    ("Security", "OpenSSL 3.x", "Provides both the TLS transport and the EVP SHA-256 digest"),
    ("Concurrency", "std::thread pool", "A shared io_context run on 2\u20134 worker threads"),
    ("Testing", "Bash + PowerShell", "End-to-end scripts over real TLS, driven by CTest"),
    ("CI/CD", "GitHub Actions", "Builds and tests both platforms on every push and pull request"),
    ("Documentation", "Markdown + Mermaid", "PRD, architecture, UML, development plan and test plan in-repo"),
], MARGIN, Inches(1.42), CONTENT_W, widths=[2.5, 2.1, 7.0],
    size=12, head_size=11.5, row_h=Inches(0.5), head_h=Inches(0.42))
text(s, "Note: Boost is headers only, so nothing Boost is linked. OpenSSL is "
        "linked, so both its headers and its libraries are required at build time.",
     MARGIN, Inches(6.1), CONTENT_W, Inches(0.4), 11.5, color=GREY_LIGHT,
     italic=True)

# ============================================================== slide 6 ======
s = new_slide()
header(s, "System Architecture", kicker="04  ·  Six layers, one-directional dependencies")
layers = [
    ("Entry point", "main.cpp", "Command line parsing, certificate discovery, "
     "event loop, exit codes. No protocol logic.", BLUE),
    ("Transport", "server.cpp  ·  client.cpp", "Accept and connect, own the TLS "
     "stream, drive the transfer.", CYAN),
    ("Session logic", "serverSession.cpp", "The protocol state machine: "
     "validation, chunk loop, integrity verdict, filename policy.", GREEN),
    ("Support", "checksum.cpp  ·  logging.hpp", "Incremental SHA-256; "
     "thread-safe logging with a terminal-aware progress bar.", AMBER),
    ("Contract", "protocol.hpp", "Wire constants and status codes \u2014 the only "
     "vocabulary the two sides share. No logic, so they cannot disagree.", NAVY_SOFT),
    ("Build", "CMakeLists.txt", "Dependency discovery, TLS asset staging, MinGW "
     "runtime staging, CTest registration.", GREY),
]
y = Inches(1.4)
LAYER_H, LAYER_GAP = Inches(0.74), Inches(0.1)
for i, (name, files, desc, colour) in enumerate(layers):
    h = LAYER_H
    sh = rect(s, MARGIN, y, Inches(8.3), h, fill=BG, line=LINE, radius=0.05)
    rect(s, MARGIN, y, Inches(0.05), h, fill=colour, shape=MSO_SHAPE.RECTANGLE)
    text(s, name, MARGIN + Inches(0.22), y + Inches(0.1), Inches(1.5), Inches(0.24),
         12, bold=True, color=colour)
    text(s, files, MARGIN + Inches(1.75), y + Inches(0.1), Inches(2.4), Inches(0.24),
         11, bold=True, color=NAVY, font=MONO)
    text(s, desc, MARGIN + Inches(0.22), y + Inches(0.38), Inches(7.9),
         Inches(0.32), 10.5, color=GREY)
    if i < len(layers) - 1:
        text(s, "\u25bc", MARGIN + Inches(0.3),
             y + LAYER_H - Inches(0.02), Inches(0.3), Inches(0.14), 8,
             color=GREY_LIGHT, align=PP_ALIGN.CENTER)
    y += h + LAYER_GAP

card(s, Inches(9.16), Inches(1.4), Inches(3.54), Inches(2.05),
     "Codebase size", [
         "11 files, 1,701 lines of C++",
         "6 headers (359 lines), 5 sources (1,342 lines)",
         "Largest file: serverSession.cpp, 495 lines",
     ], accent=BLUE)
card(s, Inches(9.16), Inches(3.6), Inches(3.54), Inches(2.28),
     "Design rules", [
         "Dependencies point one way only",
         "protocol.hpp and logging.hpp use nothing from the project",
         "Server is non-copyable by design",
         "Default port 9000, default host 127.0.0.1",
     ], accent=CYAN, fill=RGBColor(0xEC, 0xF6, 0xF8))

# ============================================================== slide 7 ======
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
     MARGIN, Inches(1.4), Inches(7.5), Inches(3.62), size=12)
bullets(s, [
    "Validate, then refuse.||  A rejection is reported as a status byte, never "
    "as a misleading resume offset \u2014 otherwise a refused client would read "
    "the offset as truth and corrupt its file.",
    "Host byte order, one write per scalar.||  Removes struct padding as a "
    "source of corruption.",
    "The stored file length IS the resume offset.||  Uploads are saved as "
    "received_<name>, so there is no separate checkpoint to keep consistent.",
    "Five status codes.||  proceed / ok, checksum mismatch, rejected, busy, error.",
], Inches(8.3), Inches(1.45), Inches(4.4), Inches(3.5), size=12, gap=11)
rect(s, MARGIN, Inches(5.28), CONTENT_W, Inches(0.72), fill=AMBER_LIGHT,
     line=RGBColor(0xE8, 0xD4, 0xAE))
text(s, "Known limitation:  the protocol is not versioned, so a client and a "
        "server must be the same build. A version byte in the header is the "
        "first thing to add.",
     MARGIN + Inches(0.28), Inches(5.5), CONTENT_W - Inches(0.5), Inches(0.4),
     12.5, color=AMBER)

# ============================================================== slide 8 ======
s = new_slide()
header(s, "Feature 1 \u2014 Encrypted and Verified TLS",
       kicker="06  ·  Security on the wire", accent=GREEN)
bullets(s, [
    "TLS 1.2 or newer||  via OpenSSL, with SNI so the server is addressed by "
    "name. SSLv2 and SSLv3 are explicitly disabled and single-DH-use is set.",
    "Chain AND host name verified by default.||  A custom host-verify callback "
    "checks the name against the certificate, including IP literals such as "
    "127.0.0.1.",
    "Fail closed.||  If the client has no CA to verify against, it refuses to "
    "start rather than connecting without checking anything.",
    "No silent downgrade.||  --insecure exists only for troubleshooting, and it "
    "prints a warning when it is used.",
    "Certificate discovery that actually works.||  The client looks for "
    "server.crt next to the executable, then in ./tls_key where the build copies "
    "it, and prints the resolved path before connecting.",
    "The server refuses to start without a certificate||  and without a key.",
], MARGIN, Inches(1.45), Inches(7.6), Inches(4.6), size=13, gap=12)
code(s, """$ ./FTP server 9000
# [SERVER] Certificate loaded:
#          tls_key/server.crt
# [SERVER] Listening on port 9000 (TLS enabled)

$ ./FTP client ../note.txt 127.0.0.1 9000
# [CLIENT] Verifying against:
#          tls_key/server.crt
# [CLIENT] TLS handshake OK (TLSv1.3)
# [SUCCESS] Server verified the file (hash matches)""",
     Inches(8.45), Inches(1.45), Inches(4.25), Inches(2.6), size=9.5)
card(s, Inches(8.45), Inches(4.2), Inches(4.25), Inches(1.85),
     "Why it matters", [
         "A name mismatch fails loudly instead of quietly",
         "Self-signed dev cert is fine for localhost, not for deployment",
     ], accent=GREEN, fill=GREEN_LIGHT, size=11)

# ============================================================== slide 9 ======
s = new_slide()
header(s, "Feature 2 \u2014 Automatic Resumption",
       kicker="06  ·  Surviving a dropped connection", accent=CYAN)
flow(s, [
    "Client starts the upload",
    "Connection is lost mid-transfer",
    "Client reconnects and re-sends the header",
    "Server replies with its resume offset",
    "Only the missing bytes are sent",
    "Transfer completes and is verified",
], MARGIN, Inches(1.45), Inches(4.5))
bullets(s, [
    "No checkpoint file.||  The resume offset is simply the current size of "
    "received_<name> on disk. There is no extra state that can be corrupted, and "
    "it survives a server restart for free.",
    "Stale partials are handled.||  If the stored copy is larger than the "
    "source, it is treated as stale and the transfer restarts from zero rather "
    "than producing a corrupt file.",
    "Bandwidth is actually saved.||  Measured: a 24 MB transfer re-sent only the "
    "bytes that were missing, and a 220 MB transfer was interrupted and resumed "
    "to a matching digest.",
    "Proven by the test suite.||  The suite kills a client in the middle of a "
    "transfer, re-runs the same command, and checks the final hash.",
], Inches(5.45), Inches(1.5), Inches(7.25), Inches(4.4), size=13, gap=13)
rect(s, MARGIN, Inches(5.72), Inches(4.5), Inches(0.62), fill=RGBColor(0xEC, 0xF6, 0xF8),
     line=RGBColor(0xB4, 0xDD, 0xE6))
text(s, "Design choice: derived state over stored state.",
     MARGIN + Inches(0.22), Inches(5.9), Inches(4.1), Inches(0.3), 12,
     bold=True, color=CYAN)

# ============================================================= slide 10 ======
s = new_slide()
header(s, "Feature 3 \u2014 Integrity Verification",
       kicker="06  ·  Proof the bytes arrived", accent=GREEN)
steps = [
    ("Client computes", "SHA-256 of the source file, streaming, via OpenSSL EVP"),
    ("Client declares", "the 64-character hex digest is the first thing in the "
     "request header"),
    ("Server hashes", "the stored bytes as they arrive, using the same EVP call"),
    ("Server compares", "computed digest against the declared digest"),
    ("Verdict", "match \u2192 success, exit 0.  Mismatch \u2192 the stored file "
     "is deleted and the client exits non-zero"),
]
y = Inches(1.45)
for i, (head, body) in enumerate(steps):
    h = Inches(0.82)
    last = i == len(steps) - 1
    rect(s, MARGIN, y, Inches(6.9), h,
         fill=GREEN_LIGHT if last else BG, line=RGBColor(0xBF, 0xE3, 0xD1) if last else LINE,
         radius=0.05)
    rect(s, MARGIN, y, Inches(0.05), h, fill=GREEN if last else BLUE,
         shape=MSO_SHAPE.RECTANGLE)
    text(s, head, MARGIN + Inches(0.22), y + Inches(0.12), Inches(2.0),
         Inches(0.26), 12.5, bold=True, color=GREEN if last else BLUE)
    text(s, body, MARGIN + Inches(2.15), y + Inches(0.12), Inches(4.6),
         Inches(0.62), 11.5, color=GREY, spacing=1.15)
    y += h + Inches(0.11)
bullets(s, [
    "Bounded memory.||  The digest is computed incrementally through a 64 KB "
    "buffer, so hashing a 64 GiB file costs the same memory as hashing 64 KB.",
    "The client exits 0 only when the server confirms a matching hash.||  "
    "Success is never reported on a local write() returning.",
    "Mismatch deletes the evidence.||  A file that does not match is removed "
    "from disk, so a later resume cannot build on corrupt bytes.",
    "Tested by tampering.||  The suite deliberately corrupts a stored file and "
    "checks that it is rejected and removed.",
], Inches(7.85), Inches(1.5), Inches(4.85), Inches(4.6), size=12.5, gap=13)

# ============================================================= slide 11 ======
s = new_slide()
header(s, "Feature 4 \u2014 Concurrency and Write Safety",
       kicker="06  \u00b7  Many clients, one safe destination", accent=BLUE)
text(s, "Concurrency model", MARGIN, Inches(1.42), Inches(6), Inches(0.3), 15,
     bold=True, color=NAVY)
bullets(s, [
    "Worker pool of 2 to 4 threads.||  min(4, hardware_concurrency), with a "
    "floor of 2, all running one shared io_context.",
    "One operation in flight per session.||  Each step is asynchronous, so a "
    "session's own handlers are serialised by construction rather than by a "
    "lock, and a slow client never occupies a worker.",
    "The client runs a single thread.||  One connection, nothing to parallelise.",
    "64 KB chunk buffer, allocated once per session||  and reused for every "
    "chunk, so there is no per-chunk allocation.",
    "Minimal shared state.||  Only the destination claim set and the log are "
    "shared, both guarded by a mutex.",
], MARGIN, Inches(1.82), Inches(6.9), Inches(3.5), size=12.5, gap=11)
rect(s, MARGIN, Inches(5.42), Inches(6.9), Inches(0.92), fill=BLUE_LIGHT)
text(s, "The trade-off, stated plainly", MARGIN + Inches(0.24), Inches(5.56),
     Inches(6.4), Inches(0.26), 12, bold=True, color=BLUE)
text(s, "A blocking design would pin a worker thread per slow client. Going "
        "async buys concurrency from a small fixed pool at the cost of a longer "
        "handler chain.",
     MARGIN + Inches(0.24), Inches(5.86), Inches(6.4), Inches(0.5), 11.5,
     color=NAVY, spacing=1.16)

text(s, "One writer per destination", Inches(7.85), Inches(1.42), Inches(5),
     Inches(0.3), 15, bold=True, color=NAVY)
bullets(s, [
    "The server keeps a claim set of destination names currently being written.",
    "A second client asking for a name already in use is refused as busy and "
    "exits non-zero.",
    "It never writes over the transfer in progress \u2014 the alternative, "
    "last-writer-wins, silently interleaves two clients into one corrupt file.",
    "The claim is released on every exit path, including an aborted or failed "
    "session.",
    "Verified: four concurrent uploads of different files all completed "
    "byte-for-byte intact.",
], Inches(7.85), Inches(1.82), Inches(4.85), Inches(2.9), size=12.5, gap=11)
stat(s, Inches(7.85), Inches(4.95), Inches(1.48), Inches(1.4), "4",
     "concurrent\nuploads verified", accent=GREEN, fill=GREEN_LIGHT)
stat(s, Inches(9.61), Inches(4.95), Inches(1.48), Inches(1.4), "2\u20134",
     "worker\nthreads", accent=BLUE)
stat(s, Inches(11.37), Inches(4.95), Inches(1.33), Inches(1.4), "64 KB",
     "chunk\nsize", accent=CYAN, fill=RGBColor(0xEC, 0xF6, 0xF8))

# ============================================================= slide 12 ======
s = new_slide()
header(s, "Security Design", kicker="07  ·  Controls and limits", accent=RED)
table(s, ["Control", "How it is implemented"], [
    ("Encrypted transport", "TLS 1.2 or newer via OpenSSL, with SNI; SSLv2 and SSLv3 disabled"),
    ("Certificate verification", "Chain and host name checked by default, IP literals such as 127.0.0.1 included"),
    ("No silent downgrade", "--insecure is available for troubleshooting only, and prints a warning"),
    ("Fail closed", "The client refuses to start when it has no CA to verify against"),
    ("Strict name validation", "No path separators, no .., no control characters, no reserved device names; max 255 characters, max 64 GiB"),
    ("Integrity", "SHA-256 compared after every transfer; a mismatch deletes the stored file"),
    ("Exclusive writes", "One writer per destination; contention is refused as busy rather than overwritten"),
], MARGIN, Inches(1.42), CONTENT_W, widths=[3.0, 9.0], size=12, head_size=11.5,
    row_h=Inches(0.5), head_h=Inches(0.42))
rect(s, MARGIN, Inches(5.22), CONTENT_W, Inches(1.0), fill=RED_LIGHT,
     line=RGBColor(0xEE, 0xC4, 0xBE))
text(s, "The honest limit:  the server authenticates nobody.", MARGIN + Inches(0.3),
     Inches(5.4), CONTENT_W - Inches(0.6), Inches(0.28), 13, bold=True, color=RED)
text(s, "Any client that can reach the port may upload. The system must not be "
        "exposed to an untrusted network. docs/SECURITY.md documents the threat "
        "model and how to harden a deployment.",
     MARGIN + Inches(0.3), Inches(5.72), CONTENT_W - Inches(0.6), Inches(0.5),
     12.5, color=NAVY, spacing=1.18)

# ============================================================= slide 13 ======
s = new_slide()
header(s, "Testing Strategy", kicker="08  ·  Verification from the outside")
bullets(s, [
    "No mocks and no unit-test framework.||  The suite starts a real server and "
    "drives real clients over real TLS, then checks the outcome from outside the "
    "process. Every defect listed later was found this way.",
    "Two suites, registered with CTest.||  A 51-check PowerShell suite drives "
    "the whole requirement list; a Bash smoke test gives Linux CI one real "
    "transfer with an externally computed SHA-256 comparison.",
    "Registered with CTest, so CI and a developer run the identical thing.||",
], MARGIN, Inches(1.45), CONTENT_W, Inches(1.7), size=13, gap=10)
table(s, ["Test group", "Checks", "Covers"], [
    ("Command line handling", "10", "FR-17, FR-19"),
    ("Clean transfer", "6", "FR-01, FR-02, FR-06, FR-14, FR-19"),
    ("Certificate verification", "4 + 1 skipped", "FR-03, FR-04, FR-05"),
    ("Integrity", "5", "FR-12, FR-13, FR-18"),
    ("Resuming", "5", "FR-08, FR-09"),
    ("Interruption", "5", "FR-20"),
    ("Concurrency", "14", "FR-10, FR-11"),
    ("Server without a certificate", "1", "FR-16"),
], MARGIN, Inches(3.32), Inches(7.4), widths=[3.6, 1.5, 3.3], size=11.5,
    head_size=11, row_h=Inches(0.38), head_h=Inches(0.4))
card(s, Inches(8.35), Inches(3.32), Inches(4.35), Inches(1.75),
     "Coverage", [
         "All 20 functional requirements traced to a check",
         "12 non-functional requirements reviewed separately",
         "docs/TEST_PLAN.md holds the full traceability matrix",
     ], accent=GREEN, fill=GREEN_LIGHT, size=11)
stat(s, Inches(8.35), Inches(5.25), Inches(2.1), Inches(1.15), "51",
     "checks in 8 groups", accent=GREEN, fill=GREEN_LIGHT)
stat(s, Inches(10.6), Inches(5.25), Inches(2.1), Inches(1.15), "20/20",
     "requirements traced", accent=BLUE)

# ============================================================= slide 14 ======
s = new_slide()
header(s, "Test Results and Measured Performance",
       kicker="08  ·  Numbers, not claims")
stats = [
    ("~267 MB/s", "8 MB transfer on\nloopback, digests matched", GREEN, GREEN_LIGHT),
    ("0.03 s", "wall-clock for that\n8 MB transfer", BLUE, BLUE_LIGHT),
    ("220 MB", "interrupted then resumed,\nfinal digest matched", CYAN, RGBColor(0xEC, 0xF6, 0xF8)),
    ("4", "concurrent uploads,\nall byte-for-byte intact", GREEN, GREEN_LIGHT),
]
for i, (v, l, a, f) in enumerate(stats):
    stat(s, MARGIN + Inches(2.98) * i, Inches(1.45), Inches(2.72), Inches(1.35),
         v, l, accent=a, fill=f)
text(s, "Measured results", MARGIN, Inches(3.05), Inches(6), Inches(0.3), 15,
     bold=True, color=NAVY)
bullets(s, [
    "51 checks run on three toolchain configurations: 50 passed, 0 failed, "
    "1 skipped \u2014 including a run with an empty PATH.",
    "24 MB resume: only the missing bytes were sent, confirmed by the server.",
    "A real 14,466-byte PDF invoice was verified by an external SHA-256 tool, a "
    "size comparison, a byte-for-byte comparison and a header/trailer check.",
], MARGIN, Inches(3.45), Inches(7.4), Inches(2.2), size=12.5, gap=11)
card(s, Inches(8.35), Inches(3.05), Inches(4.35), Inches(3.2),
     "Environment", [
         "Windows 11 Home x64",
         "GCC 16.x, MSYS2 UCRT64, Ninja",
         "GCC 15.2, MinGW-w64 (CLion)",
         "OpenSSL 3.6.4, Boost 1.88 headers",
         "CMake 3.15+, C++20",
         "PowerShell 5.1",
     ], accent=BLUE, size=11.5)
rect(s, MARGIN, Inches(5.85), Inches(7.4), Inches(0.6), fill=AMBER_LIGHT,
     line=RGBColor(0xE8, 0xD4, 0xAE))
text(s, "Not yet done: the full 997-file bulk run, and a cross-machine transfer.",
     MARGIN + Inches(0.26), Inches(6.03), Inches(7), Inches(0.3), 11.5,
     color=AMBER)

# ============================================================= slide 15 ======
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
     "Interleaved writes from several threads on one terminal line"),
    ("5", "A redirected server log was buried under progress updates",
     "Progress is now drawn only when the output is a terminal"),
    ("6", "Transfer rate printed as 0.0286102",
     "A floating-point formatting defect, now two decimals"),
    ("7", "The MinGW build produced no output and returned instantly",
     "Exit code 0xC0000135, missing runtime DLLs; the build now stages them"),
    ("8", "Client failed to verify the certificate from another directory",
     "The CA is now looked up next to the executable"),
]
for i, (num, title, detail) in enumerate(defects):
    col, row = divmod(i, 4)
    x = MARGIN + col * Inches(6.35)
    y = Inches(1.48) + row * Inches(1.02)
    rect(s, x, y, Inches(5.98), Inches(0.88), fill=BG, line=LINE, radius=0.05)
    badge(s, x + Inches(0.16), y + Inches(0.27), Inches(0.34), Inches(0.34),
          num, AMBER, size=11)
    text(s, title, x + Inches(0.62), y + Inches(0.14), Inches(5.2), Inches(0.4),
         12, bold=True, color=NAVY, spacing=1.1)
    text(s, detail, x + Inches(0.62), y + Inches(0.55), Inches(5.2),
         Inches(0.28), 10.5, color=GREY, spacing=1.05)
text(s, "Defect 7 was the worst-shaped failure of the eight: it printed nothing, "
        "returned success, and only appeared on MinGW. It is the reason CI runs "
        "the same MinGW toolchain as the local build.",
     MARGIN, Inches(5.72), CONTENT_W, Inches(0.6), 12.5, color=GREY, spacing=1.2)

# ============================================================= slide 16 ======
s = new_slide()
header(s, "CI/CD and DevOps Pipeline", kicker="10  ·  Built and verified automatically")
card(s, MARGIN, Inches(1.45), Inches(6.05), Inches(3.5),
     "ci.yml \u2014 every push and pull request", [
         "Triggers: push to main, pull request to main, manual dispatch",
         "Linux job (ubuntu-latest): install cmake, ninja, g++, libssl-dev, "
         "libboost-dev",
         "Generates the development certificate, configures Release with Ninja, "
         "builds, runs the smoke test on port 9300",
         "Windows job (MSYS2 UCRT64): same toolchain family as the local build",
         "Runs the full ctest suite; uploads logs and received files as "
         "artefacts if it fails",
         "Deliberately the same toolchain, so CI catches MinGW-specific problems",
     ], accent=GREEN, fill=GREEN_LIGHT, size=11.5)
card(s, Inches(7.28), Inches(1.45), Inches(5.42), Inches(3.5),
     "release.yml \u2014 on a v* tag", [
         "verify: greps the version out of CMakeLists.txt and fails the release "
         "if the tag does not match",
         "Builds and tests both platforms",
         "Packages ftp-server-<version>-linux-x86_64.tar.gz and a Windows zip "
         "containing every DLL",
         "Generates SHA256SUMS.txt",
         "Extracts the matching CHANGELOG section into NOTES.md, failing if it "
         "is absent",
         "Publishes the release only when all three jobs succeed",
     ], accent=BLUE, size=11.5)
text(s, "Also in the repository", MARGIN, Inches(5.15), Inches(6), Inches(0.3),
     14, bold=True, color=NAVY)
bullets(s, [
    "Dependabot v2 ||  \u00b7  pull request and issue templates (bug and feature)",
    "The version string lives in CMakeLists.txt only ||  \u2014  it is compiled "
    "into the binary and referenced by CHANGELOG.md, so a release and a build "
    "cannot drift apart",
    "TLS assets and MinGW runtime DLLs are staged next to the executable ||  "
    "automatically at build time",
], MARGIN, Inches(5.52), CONTENT_W, Inches(1.2), size=12, gap=8)

# ============================================================= slide 17 ======
s = new_slide()
header(s, "Key Design Decisions", kicker="11  ·  Alternatives rejected, and why")
table(s, ["Decision", "Rejected alternative", "Reason"], [
    ("Asynchronous, one operation in flight",
     "Thread per connection",
     "A thread per client cannot scale, and a blocking session pins a worker for the whole transfer"),
    ("Resume offset = stored file length",
     "A separate checkpoint file",
     "No extra state that can be corrupted, and it survives a server restart for free"),
    ("Validate the header, then refuse",
     "Accept, then discover the problem",
     "A refusal must never be mistakable for a resume instruction"),
    ("One writer per destination",
     "Last-writer-wins or unique names",
     "Stops two clients silently interleaving chunks into one corrupt file"),
    ("Incremental EVP hashing",
     "Load the whole file into memory",
     "Bounded memory for any file size: 64 GiB costs the same as 64 KB"),
    ("received_<name> prefix",
     "Overwrite the source name",
     "Keeps uploads clear of existing files and makes partials recognisable"),
    ("Host byte order, one write per scalar",
     "A packed struct on the wire",
     "Removes struct padding as a source of corruption"),
    ("Progress only when output is a terminal",
     "Always print progress",
     "A redirected log would be buried under hundreds of identical lines"),
], MARGIN, Inches(1.42), CONTENT_W, widths=[3.5, 3.0, 5.5], size=11,
    head_size=11, row_h=Inches(0.5), head_h=Inches(0.42))

# ============================================================= slide 18 ======
s = new_slide()
header(s, "Challenges Faced and What They Taught Me",
       kicker="12  ·  The hard parts, honestly", accent=CYAN)
challenges = [
    ("Making the busy check reliable",
     "A race between claiming and releasing a destination caused intermittent "
     "failures. Fixed with a mutex-guarded set and a release on every exit path."),
    ("Thread-safe logging with a live progress bar",
     "Concurrent sessions interleaved their writes into garbled lines. Fixed "
     "with a logging mutex and in-place redraw of a single progress line."),
    ("MinGW and OpenSSL",
     "FindOpenSSL ignores MinGW's libssl.a, and the build failed silently with "
     "0xC0000135 from missing runtime DLLs. Fixed with a header/library search "
     "fallback and automatic DLL staging."),
    ("Certificate lookup from any directory",
     "Verification failed when the client ran from elsewhere. Fixed by looking "
     "next to the executable and printing the resolved path before connecting."),
    ("Async handler chains",
     "Keeping exactly one operation in flight per session, without a deadlock or "
     "a use-after-free when a session is aborted mid-chain."),
    ("Verifying from the outside",
     "Every real defect came from running real transfers, not from reading the "
     "code. That is now how I test my own work."),
]
for i, (head, body) in enumerate(challenges):
    col, row = divmod(i, 3)
    x = MARGIN + col * Inches(6.35)
    y = Inches(1.48) + row * Inches(1.62)
    rect(s, x, y, Inches(5.98), Inches(1.42), fill=RGBColor(0xEC, 0xF6, 0xF8),
         line=RGBColor(0xB4, 0xDD, 0xE6), radius=0.05)
    rect(s, x, y, Inches(0.05), Inches(1.42), fill=CYAN, shape=MSO_SHAPE.RECTANGLE)
    text(s, head, x + Inches(0.24), y + Inches(0.16), Inches(5.5), Inches(0.28),
         13, bold=True, color=NAVY)
    text(s, body, x + Inches(0.24), y + Inches(0.5), Inches(5.5), Inches(0.8),
         11.5, color=GREY, spacing=1.15)

# ============================================================= slide 19 ======
s = new_slide()
header(s, "Limitations and Future Scope",
       kicker="13  ·  What is not built yet", accent=AMBER)
card(s, MARGIN, Inches(1.45), Inches(6.05), Inches(4.3),
     "Current limitations", [
         "No download path. ||  The client can only upload; retrieval is the "
         "highest-value feature to add next.",
         "The server authenticates nobody. ||  No accounts, no authorisation, no "
         "per-user quota.",
         "The device-driver component of the brief is not covered. ||  The "
         "system is C++20 with system-level networking but contains no kernel "
         "module.",
         "The protocol is not versioned. ||  A client and a server must be the "
         "same build.",
         "Verification gaps. ||  The 997-file bulk run and a cross-machine "
         "transfer are not done; no Linux or macOS run has been performed "
         "locally.",
     ], accent=AMBER, fill=AMBER_LIGHT, size=12)
card(s, Inches(7.28), Inches(1.45), Inches(5.42), Inches(4.3),
     "Planned next", [
         "Download with the same integrity model",
         "Resumable downloads with a range-style offset",
         "Mutual TLS, so the server can authenticate the client",
         "Directory sync and multi-file transfers",
         "A version byte in the header for protocol evolution",
         "Sidecar metadata for richer resumable state",
         "Linux and macOS build verification, then a release for each",
     ], accent=GREEN, fill=GREEN_LIGHT, size=12)

# ============================================================= slide 20 ======
s = new_slide()
header(s, "Demonstration", kicker="14  ·  Five minutes, live")
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
y = Inches(1.5)
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
card(s, Inches(10.2), Inches(1.5), Inches(2.5), Inches(2.3),
     "Before the demo", [
         "Clean build directory",
         "Certificate present",
         "Test files ready",
     ], accent=CYAN, fill=RGBColor(0xEC, 0xF6, 0xF8), size=11)
text(s, "Steps 2 to 4 are the ones that separate this from a file copy.",
     Inches(10.2), Inches(4.0), Inches(2.5), Inches(1.2), 12, color=GREY,
     spacing=1.2)

# ============================================================= slide 21 ======
s = new_slide()
header(s, "Conclusion", kicker="14  ·  What was delivered")
bullets(s, [
    "A working secure file transfer system.||  A C++20 client\u2013server uploader "
    "with end-to-end TLS, automatic resumption after a dropped connection, and "
    "SHA-256 verification on every upload.",
    "Deliberate engineering decisions.||  Six documented layers with "
    "one-directional dependencies, an asynchronous design that serves many "
    "clients from a 2\u20134 thread pool, and one writer per destination.",
    "Proven, not asserted.||  51 automated end-to-end checks over real TLS, all "
    "20 functional requirements traced to evidence, 8 real defects found and "
    "fixed, and ~267 MB/s measured on loopback.",
    "Reproducible anywhere.||  One CMake project builds and tests on Linux and "
    "Windows; GitHub Actions verifies both on every push, and tagged releases "
    "publish signed checksums.",
    "Documented for review.||  PRD, architecture, UML, development plan, test "
    "plan, changelog, contribution guide, security policy and code of conduct, "
    "all in the repository.",
], MARGIN, Inches(1.5), Inches(8.2), Inches(4.4), size=13, gap=14)
summary = [
    ("1,701", "lines of C++ across\n11 files", BLUE, BLUE_LIGHT),
    ("51", "automated checks\n50 passed, 1 skipped", GREEN, GREEN_LIGHT),
    ("8", "defects found\nand fixed", AMBER, AMBER_LIGHT),
    ("2", "platforms\nLinux and Windows", CYAN, RGBColor(0xEC, 0xF6, 0xF8)),
]
for i, (v, l, a, f) in enumerate(summary):
    stat(s, Inches(9.35), Inches(1.5) + Inches(1.28) * i, Inches(3.35),
         Inches(1.16), v, l, accent=a, fill=f)

# ============================================================= slide 22 ======
s = new_slide(footer=False)
rect(s, Inches(0), Inches(0), W, H, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, Inches(0), Inches(0), W, Inches(0.09), fill=CYAN, shape=MSO_SHAPE.RECTANGLE)
text(s, "Thank you", Inches(1.2), Inches(2.15), Inches(10.9), Inches(1.0), 52,
     bold=True, color=WHITE, align=PP_ALIGN.CENTER)
rect(s, W / 2 - Inches(0.75), Inches(3.28), Inches(1.5), Inches(0.05), fill=CYAN,
     shape=MSO_SHAPE.RECTANGLE)
text(s, "Questions and feedback are welcome", Inches(1.2), Inches(3.6),
     Inches(10.9), Inches(0.4), 17, color=RGBColor(0xB8, 0xCA, 0xDE),
     align=PP_ALIGN.CENTER)
text(s, "Secure Resumable File Transfer  ·  C++20  ·  TLS 1.2+  ·  SHA-256  ·  CMake",
     Inches(1.2), Inches(4.35), Inches(10.9), Inches(0.3), 12.5, color=CYAN,
     align=PP_ALIGN.CENTER)
rect(s, Inches(4.05), Inches(4.95), Inches(5.23), Inches(0.62),
     fill=RGBColor(0x10, 0x28, 0x49), line=RGBColor(0x2C, 0x5A, 0x8C), radius=0.1)
text(s, "github.com/zexxitywave/File-transfer-", Inches(4.05), Inches(5.12),
     Inches(5.23), Inches(0.3), 13, color=WHITE, font=MONO,
     align=PP_ALIGN.CENTER)
text(s, "[ Your Name ]  ·  [ Roll No ]  ·  [ Department, College ]  ·  "
        "Guide: [ Faculty Name ]",
     Inches(1.2), Inches(5.95), Inches(10.9), Inches(0.3), 11.5,
     color=GREY_LIGHT, align=PP_ALIGN.CENTER)

prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides)} slides)")