# PowerPoint output

## Fragment to adapt

```markdown
## Output

Produce a `.pptx` named `<subject>-<period>.pptx`.

Fixed running order:

1. Title slide - subject, period, date prepared.
2. One-slide summary - the three things the audience must take away.
3. One slide per <section>, in the order the audience expects them.
4. Closing slide - decisions required, each with an owner.

Every slide:
- A headline that states the point, not the topic. "Margin fell 4pts on
  freight costs", not "Margin".
- At most six bullets, at most two lines each.
- Any number on the slide traceable to a named source.

Tell the user what the deck concludes before they open it.
```

## Rules

- **Headlines assert, they do not label.** A slide titled "Q3 Results" makes the reader find the point. A slide titled "Q3 revenue grew 8%, all of it from EMEA" has already delivered it.
- **One idea per slide.** If a slide needs the word "also", it is two slides.
- **Six bullets, two lines each, maximum.** Past that nobody reads it and it should be a document instead.
- **No paragraphs on a slide.** If the content only works as prose, produce a Word file and say why.
- **Charts beat tables; tables beat lists of numbers.** A table over about 5x5 belongs in an attached spreadsheet, not on a slide.
- **Every number carries its source and period.** An untraceable figure on a committee slide is worse than no figure.
- **Keep the deck short enough to present.** Roughly one slide per minute of the meeting it was made for. Ask how long the slot is if the brief does not say.

## Speaker notes

Put the detail that supports each slide in the speaker notes rather than on the slide. This is where the caveats, the method and the secondary numbers belong - available to whoever presents, invisible to the room.

## Template

If the user supplied a branded template or an example deck, match its section order and slide types. Do not invent a new structure alongside an existing house style.

## Size

Keep the file under 10 MB. Images are almost always the cause - if the deck is heavy, say so and offer to reduce the image resolution.

## If you need to write it in code

The harness creates this format natively; reach for code only when you need control it cannot give - an exact template, a formula, a specific format. [`scripts/pptx_template.py`](../scripts/pptx_template.py) is a working starting point using `python-pptx`, and already obeys the rules above.
