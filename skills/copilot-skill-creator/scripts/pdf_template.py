"""Template: build a .pdf with page furniture and a table that fits.

Copy into a generated skill and adapt. Use reportlab - fpdf is NOT available
in the Copilot Studio sandbox.

Choose PDF only when the file must not be edited: something circulated,
filed, signed, or sent outside the organisation. If the recipient will change
it, produce a .docx instead.

Obeys the rules in references/output-pdf.md: real headings, a footer on every
page, tables sized to the page, nothing provisional.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# --- adapt from here -------------------------------------------------------
TITLE = "Q3 credit review"
PERIOD = "Quarter ended 30 September 2026"
PREPARED = "Prepared 2026-09-20"
SECTIONS = [
    ("Summary", "Portfolio performing within appetite. One concentration breach."),
    ("Concentration", "Acme Ltd represents 38% of exposure against a 35% limit."),
]
TABLE_HEAD = ["Borrower", "Exposure", "Limit"]
TABLE_ROWS = [
    ["Acme Ltd", "750,000", "800,000"],
    ["Beta Ltd", "210,000", "400,000"],
]
OUTPUT = "credit-review.pdf"
# --- to here ---------------------------------------------------------------

styles = getSampleStyleSheet()


def furniture(canvas, doc):
    """Every page identifies the document it came from. Pages get separated."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(20 * mm, 12 * mm, f"{TITLE} - {PERIOD}")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


story = [
    Paragraph(TITLE, styles["Title"]),
    Paragraph(f"{PERIOD}. {PREPARED}.", styles["Normal"]),
    Spacer(1, 8 * mm),
]

for heading, body in SECTIONS:
    story.append(Paragraph(heading, styles["Heading2"]))   # becomes the PDF outline
    story.append(Paragraph(body, styles["BodyText"]))
    story.append(Spacer(1, 4 * mm))

# Fixed widths so no column silently runs off the page.
usable = A4[0] - 40 * mm
table = Table([TABLE_HEAD] + TABLE_ROWS, colWidths=[usable * 0.5, usable * 0.25, usable * 0.25])
table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
]))
story.append(table)

SimpleDocTemplate(OUTPUT, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm).build(
    story, onFirstPage=furniture, onLaterPages=furniture
)
print(f"wrote {OUTPUT}: {len(SECTIONS)} sections, {len(TABLE_ROWS)} table rows")
