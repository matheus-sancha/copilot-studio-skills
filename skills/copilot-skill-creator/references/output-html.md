# HTML output

## Fragment to adapt

```markdown
## Output

Produce a single self-contained `.html` file named `<subject>-<period>.html`.

- Everything inline: CSS in one `<style>` block, no external stylesheets,
  no CDN scripts, no remote fonts or images. The file must render correctly
  with no network connection.
- A `<title>` naming the document and its period.
- Semantic structure: one `<h1>`, then `<h2>`/`<h3>`, real `<table>` markup
  with `<thead>` for data.
- Readable at phone width as well as on a desktop.

Tell the user what the page shows before they open it.
```

## Rules

- **Self-contained, always.** One file, nothing fetched at runtime. A page that needs the internet fails in exactly the situations it gets used - forwarded by email, opened from a shared drive, viewed offline.
- **Images as data URIs** if they are genuinely needed. Otherwise leave them out; they are usually the reason the file is too large.
- **Semantic HTML.** Real headings, real tables, real lists. A page built from `<div>`s is unreadable to assistive technology and to anything that tries to extract the data later.
- **One `<h1>`.** Everything else descends from it.
- **Legible defaults.** Body text at least 16px, line height around 1.5, a maximum line length around 70 characters. Dark text on a light background unless the user asked otherwise.
- **Tables scroll, pages do not.** Wrap a wide table in a container that scrolls sideways rather than letting the whole page scroll horizontally.
- **No JavaScript unless it earns its place.** Sorting a long table earns it; animating a heading does not. Anything interactive must still show its content with scripting disabled.

## When HTML is the right choice

Choose HTML when the output benefits from layout or colour and the reader will open it in a browser - a dashboard-style summary, a formatted report, anything with charts. Choose PDF when it will be printed or filed, and Markdown when it will be edited or version-controlled.

## Size

Keep the file under 10 MB. If it is over, the cause is almost always embedded images - reduce their resolution or drop them, and say which you did.
