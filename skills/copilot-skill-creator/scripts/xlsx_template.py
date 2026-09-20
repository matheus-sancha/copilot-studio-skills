"""Template: build an .xlsx with exact control over layout and formats.

Copy into a generated skill and adapt. Use this only when the harness's own
file creation cannot give the control you need - a fixed template, real
formulas, specific number formats. For an ordinary spreadsheet, describe the
output and let the harness build it.

Obeys the rules in references/output-xlsx.md: one header row, frozen; no
merged cells in a data range; dates as dates; numbers as numbers.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

# --- adapt from here -------------------------------------------------------
SHEET_NAME = "Summary"
HEADERS = ["Region", "Units", "Revenue", "Reported"]
ROWS = [
    # text, int, float, date - types matter, do not pass these as strings
    ["EMEA", 1204, 88231.5, "2026-03-31"],
    ["AMER", 980, 71044.0, "2026-03-31"],
]
MONEY_COLUMNS = {"C"}
DATE_COLUMNS = {"D"}
OUTPUT = "summary.xlsx"
# --- to here ---------------------------------------------------------------

wb = Workbook()
ws = wb.active
ws.title = SHEET_NAME

ws.append(HEADERS)
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal="left")

for row in ROWS:
    ws.append(row)

# One header row, frozen. Never a title row above it - it breaks filters,
# pivots and every downstream import.
ws.freeze_panes = "A2"

for column in MONEY_COLUMNS:
    for cell in ws[column][1:]:
        cell.number_format = "#,##0.00"
        cell.alignment = Alignment(horizontal="right")

for column in DATE_COLUMNS:
    for cell in ws[column][1:]:
        cell.number_format = "yyyy-mm-dd"

# Width to content, so nothing renders as ####.
for i, header in enumerate(HEADERS, start=1):
    longest = max([len(str(header))] + [len(str(r[i - 1])) for r in ROWS])
    ws.column_dimensions[get_column_letter(i)].width = longest + 2

wb.save(OUTPUT)
print(f"wrote {OUTPUT}: {len(ROWS)} rows across {len(HEADERS)} columns")
