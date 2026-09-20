# PDF output

## Fragment to adapt

```markdown
## Output

Produce a `.pdf` named `<subject>-<period>.pdf`.

- Same fixed section order every time, with real headings so the PDF carries
  a navigable outline.
- A footer on every page: document name, period, page number.
- Tables sized to fit the page width - never let a column run off the edge.
- State the preparation date on the first page.

PDF is final. Before producing it, confirm nothing is still awaiting a value.
```

## Rules

- **Choose PDF only when the file must not be edited** - something circulated, filed, signed or sent outside the organisation. If the recipient will change it, produce Word instead and say why.
- **Fixed sections, real headings.** Headings become the PDF outline, which is the only navigation a long PDF has.
- **Page furniture matters.** Pages get printed and separated, so every page must identify the document it came from. Document name, period, page number.
- **Nothing provisional.** A PDF looks authoritative regardless of what is in it. No `TBD`, no unresolved placeholders, no figures still awaiting confirmation. If something is unresolved, either it is stated as unresolved in a sentence, or the file is not produced yet.
- **Tables must fit.** A table wider than the page silently loses columns. Fewer columns, or landscape, or an attached spreadsheet for the full detail.
- **Say what cannot be recovered.** If the PDF is a rendering of data the user may need to work with, offer the underlying spreadsheet alongside it.

## Scanned input

If the source is a scanned or image-based PDF, the text cannot be read. Say so plainly and ask for a text-based copy rather than guessing at the contents.

## Size

Keep the file under 10 MB. For long reports, split by section or period - one deliverable per chapter - rather than producing one oversized file that will not be surfaced at all.

## If you need to write it in code

The harness creates this format natively; reach for code only when you need control it cannot give - an exact template, a formula, a specific format. [`scripts/pdf_template.py`](../scripts/pdf_template.py) is a working starting point using `reportlab`, and already obeys the rules above.
