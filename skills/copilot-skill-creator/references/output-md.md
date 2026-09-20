# Markdown output

## Fragment to adapt

```markdown
## Output

Produce a `.md` file named `<subject>-<period>.md`.

- One `#` title, then `##` sections in a fixed order.
- Tables for anything with parallel facts; lists for anything sequential.
- Code, paths, field names and commands in backticks.
- Links carry descriptive text, never "here" or a bare URL.

When the content is short enough to read in the chat, put it in the reply
as well as the file - do not make the user open a file to read four lines.
```

## Rules

- **One `#` per file.** Everything below is `##` and `###`. Multiple top-level headings break every renderer's outline.
- **Heading levels never skip.** `##` then `###`, never `##` then `####`.
- **Tables for parallel facts.** Three things each having a name, a type and a description is a table, not nine bullets.
- **Backticks for anything literal** - filenames, field names, commands, values. It removes the ambiguity between a word used as a word and a word used as a name.
- **Descriptive link text.** `[the lending policy](...)` reads; `[here](...)` does not, and is useless to a screen reader.
- **No trailing whitespace line breaks.** Use a blank line between paragraphs.
- **Front matter only if something consumes it.** YAML at the top of a document nobody parses is noise.

## When Markdown is the right choice

Choose Markdown when the output will be read in a tool that renders it, pasted into a repo, or fed to another agent. Choose Word or PDF when a person will read it as a document, and HTML when it needs styling or must open in a browser.

Markdown is also the right output when the user will *edit* the result and feed it back - it is the only one of these formats that diffs cleanly.

## Short output

Markdown is the one format where the file is often unnecessary. If the result is under roughly forty lines, put it in the chat reply. Offer the file as well only if the user asked for something to keep.
