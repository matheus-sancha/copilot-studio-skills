# Word output

## Fragment to adapt

```markdown
## Output

Produce a `.docx` named `<subject>-<period>.docx`.

Fixed section order, every section present every time:

1. <Section one>
2. <Section two>
3. <Section three>

- Use real heading styles (Heading 1, Heading 2), never bold text pretending
  to be a heading.
- Never leave a section empty. Write "Insufficient data" and state exactly
  what is missing.
- Tables for anything with more than two parallel facts per row.
- Figures carry their period and source on first mention.

Tell the user which sections needed assumptions before they open the file.
```

## Rules

- **Fixed sections, always all of them.** A document whose shape changes run to run cannot be reviewed quickly, and a missing section reads as an oversight rather than a gap. Empty sections say "Insufficient data" and name what is missing.
- **Real heading styles.** Bold paragraphs are invisible to the navigation pane, to a table of contents and to anyone using a screen reader.
- **Front-load the conclusion.** The first paragraph says what the document concludes. Readers of internal documents rarely reach the end.
- **Short paragraphs.** Three or four sentences. A wall of text in a review document does not get read, it gets skimmed and misquoted.
- **Say where numbers came from** on first mention - period, source, and whether reported or derived.
- **Never present an estimate as a reported figure.** If something was inferred, label it in the sentence, not in a footnote.
- **No placeholder text in a delivered file.** No `TBD`, no `[insert name]`, no lorem ipsum. If a value is unknown, say it is unknown.

## Length

Say in the skill roughly how long the document should be - "about two pages", "no more than one page per subsidiary". Without a target the model will write to the length of its input rather than the length the reader needs.

## Template

If the user supplied an existing document, match its section names and order exactly. The value of a standard document is that a reader knows where to look; a better structure that nobody expects is worse than the one they know.

## Size

Keep the file under 10 MB.
