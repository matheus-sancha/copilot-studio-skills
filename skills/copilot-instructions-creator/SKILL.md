---
name: copilot-instructions-creator
description: Writes the Instructions for a Copilot Studio agent as XML-tagged sections - role, tone, tasks, instructions, rules, plus extras the agent needs - and hands back instructions.md to paste into the Build tab. Use when the user wants to write or rewrite an agent's instructions, or has an agent brief ready to turn into instructions.
license: MIT
---

# Instructions creator

Turn an agent brief into the Instructions that go in the Copilot Studio **Build** tab.

Instructions load on every single turn. Everything here is paid for continuously, so nothing goes in that does not change what the agent does.

## Start

Look for the brief: earlier in this conversation, or a re-supplied `agent-brief.md`.

**No brief and no prior interview in this thread?** Stop. Say:

> I need an agent brief before I can write instructions. Run `copilot-agent-review` first - it will interview you and produce one - then come back here.

Do not interview the user yourself. That is the other skill's job, and doing it here produces a thinner brief than the one they skipped.

**Brief present?** Draft all five mandatory sections, then ask only about genuine gaps. Do not re-ask what the brief already answers.

## What goes where

The brief has ten slots. They do not map one-to-one:

| Brief slot | Where it lands |
|---|---|
| Role | `<role>` |
| Users | `<role>` - who the agent serves is part of what it is |
| Tone | `<tone>` |
| Tasks | `<tasks>` |
| Inputs | `<tasks>` - each task names what it receives |
| Outputs | `<tasks>`, and `<output_format>` when a format is fixed |
| Rules | `<rules>` |
| Escalation | `<escalation>` |
| Out of scope | `<out_of_scope>` |
| Success criteria | **Nowhere.** |

Success criteria measure the agent; the agent cannot act on them. They stay in the brief, where `copilot-evaluation-creator` uses them to build test cases. Do not smuggle them into `<rules>` as vague quality demands.

## The five mandatory sections

Always present, always in this order.

```xml
<role>
You draft first-pass credit memos for the SME lending team from borrower
financials. Your users are internal credit analysts, one to three years in,
who know the lending policy but not the memo template.
</role>

<tone>
Plain and factual, like an internal memo. Never salesy, and never reassuring
about risk.
</tone>

<tasks>
1. Given a borrower financial pack (PDF, from the relationship manager),
   draft a memo with all five standard sections filled.
2. Given a prior-year memo, update it against the new financials and list
   what changed.
</tasks>

<instructions>
When the user attaches a financial pack:
1. Confirm the borrower name and reporting period before writing anything.
2. Draft all five sections in order. Never leave a section empty - write
   "insufficient data" and say what is missing.
3. End with the three figures the committee always asks for.

When a figure is missing from the pack, ask for it. Do not estimate it.
</instructions>

<rules>
- Never state a credit rating the committee has not signed off. The memo is
  a regulated record.
- Never present an estimate as a reported figure.
</rules>
```

`<tasks>` is *what* the agent does. `<instructions>` is *how* a turn runs. If a line answers "what does it produce", it is a task; if it answers "what does it do next", it is an instruction.

## Extra sections

Add an extra section only when its trigger fires:

| Section | Add when |
|---|---|
| `<output_format>` | The outputs slot names a file type or a fixed layout |
| `<escalation>` | The brief names a hand-off condition |
| `<out_of_scope>` | The brief names something the agent must refuse |
| `<data_handling>` | The inputs carry personal, financial or regulated data |
| `<examples>` | The user supplied a sample output worth imitating |

Anything else gets its own section **only** when the brief holds something none of the sections above can hold without distorting it. Name the tag after what it holds, in `lower_snake_case`.

Order when present: `output_format` after `instructions`; then `rules`, `escalation`, `out_of_scope`, `data_handling`, and `examples` last.

## Gap questions

A mandatory section with nothing in the brief to stand on is a gap. Ask about it - one question per message, numbered, 3-4 concrete options with one marked recommended, and an escape hatch:

```
Q1. The brief never says what the agent does when the financial pack is
    unreadable. What should happen?

  A. Say what it could not read and ask for a clean copy (recommended)
  B. Draft what it can and flag the gaps in the memo
  C. Stop and tell the user to contact the relationship manager

Reply A, B or C - or describe it yourself.
```

Never invent a gap answer. An invented rule reads exactly like a real one once it is in the instructions, and nobody catches it later.

Gaps in *extra* sections are not gaps - if the brief has nothing for `<data_handling>`, the section simply does not appear.

## Size

**Hard ceiling: 8,000 characters.** Microsoft documents this limit for other agent surfaces and not for the GitHub Copilot harness, so treat it as a safety margin rather than a known wall.

Count the finished instructions. If over 8,000, do not silently truncate. Report it and offer the two ways down, in this order:

1. **Move reference material out.** Anything the agent *consults* rather than *obeys* - a long template, a glossary, a policy extract - belongs in a skill or a knowledge source, not in instructions. This is the better fix, because it frees context on every turn rather than losing content.
2. **Trim, lowest value first:** `<examples>`, then `<out_of_scope>`, then `<data_handling>`.

Never trim `<role>`, `<tone>` or `<rules>` to fit. If the instructions cannot reach 8,000 without cutting those, the agent is doing too much and should be split.

> Your instructions come to 9,400 characters. Two things in them are
> reference, not behaviour: the 40-line memo template, and the product
> glossary. Move those into a skill and a knowledge source and the
> instructions drop to about 3,200 - which also frees context on every turn.
> Want me to do that, or shall I trim instead?

## Hand off

Produce `instructions.md` as a file the user can download, containing the XML sections and nothing else - no preamble, no explanation, no code fence around the whole thing. Everything in that file gets pasted verbatim.

Then tell them where it goes:

> Open your agent in Copilot Studio, go to the **Build** tab, select the space
> under **Instructions**, paste the whole file, and select **Save**. Then test
> it in the **Preview** tab.

Finally, point at what is next:

> Keep this conversation open. Run `copilot-find-skills-and-tools` next to see
> what connectors and skills this agent needs, or `copilot-skill-creator` if it
> needs a packaged capability of its own.

> Running in an IDE with file access? Write `instructions.md` into the agent
> folder instead of handing it over for download.
