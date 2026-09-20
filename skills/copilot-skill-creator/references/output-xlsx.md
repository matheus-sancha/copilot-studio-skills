# Excel output

## Fragment to adapt

```markdown
## Output

Produce a `.xlsx` file named `<subject>-<period>.xlsx`.

- One sheet per <region / category / month>, named after its contents.
- Row 1 holds the column headers and nothing else. Freeze it.
- One row per record. No blank spacer rows.
- Money and quantities right-aligned, two decimal places, thousands separated.
- Dates in the date format, not as text.
- Totals in their own labelled row at the bottom of the block, never mixed
  into the data rows.

Tell the user which sheet answers their question and what the headline
number is. Do not make them open the file to find out.
```

## Rules

- **One header row.** No title row above it, no merged banner. A title above the headers breaks every filter, pivot and import downstream.
- **Never merge cells inside a data range.** Merged cells are the single most common reason a spreadsheet cannot be reused.
- **Dates as real dates.** A date stored as text sorts alphabetically, which puts 10 January before 2 January.
- **Numbers as numbers.** No currency symbols inside the cell value, no thousands separators typed into the text. Use the number format.
- **One fact per cell.** Never `"EMEA - 1,204"` in a single cell.
- **Name every sheet** after what it holds. `Sheet1` tells the reader nothing.
- **Blank means unknown.** If a value is zero, write `0`. If it is not known, leave it empty and say so in the reply.
- **Put the working out somewhere.** If a figure is derived, either use a real formula or add a column showing the inputs. A bare number nobody can trace gets distrusted.

## When the sheet is the answer

If the user asked a question and the spreadsheet is the evidence, lead the chat reply with the answer in words, then attach the file. A file alone makes the reader do the work twice.

## Size

Keep the file under 10 MB - above that Copilot Studio will not surface it in the response. For a long export, split by period or category into several files rather than one large one.

## If you need to write it in code

The harness creates this format natively; reach for code only when you need control it cannot give - an exact template, a formula, a specific format. [`scripts/xlsx_template.py`](../scripts/xlsx_template.py) is a working starting point using `openpyxl`, and already obeys the rules above.
