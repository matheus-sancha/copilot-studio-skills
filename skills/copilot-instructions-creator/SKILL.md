---
name: copilot-instructions-creator
description: Writes the Instructions for a Copilot Studio agent as XML-tagged sections - role, tone, tasks, instructions, rules, plus knowledge routing, tool use and connected agents where they apply. Drafts them early, revises them once tools and skills exist, then hands back instructions.md to paste into the Build tab. Use when the user wants to write, revise or review an agent's instructions.
license: MIT
---

# Instructions creator

Turn an agent brief into the Instructions that go in the Copilot Studio **Build** tab.

Instructions load on every single turn. Everything here is paid for continuously, so nothing goes in that does not change what the agent does.

## Two passes

This skill runs **twice** in a build, and the difference matters.

**Draft pass** - right after the brief exists, before tools and skills. Produce the full instructions **in the conversation** and get the user to correct them. **Emit no file.** The sections that reference tools, skills and connected agents cannot be accurate yet, and instructions pasted into the Build tab now would only be edited by hand and then overwritten.

**Revise pass** - after tools and skills exist. Take the draft from this conversation, rewrite the sections that reference them, and **now** emit `instructions.md`. One file, one paste, at the end.

Work out which pass you are in from the conversation: if tools or skills have been added since the draft, you are revising. If there is no draft yet, you are drafting. If genuinely unclear, ask.

## Start

Look for the brief: earlier in this conversation, or a re-supplied `agent-brief.md`.

**No brief and no prior interview in this thread?** Stop. Say:

> I need an agent brief before I can write instructions. Run `copilot-agent-review` first - it will interview you and produce one - then come back here.

Do not interview the user yourself. That is the other skill's job, and doing it here produces a thinner brief than the one they skipped.

**Brief present?** Draft all five mandatory sections, then ask only about genuine gaps. Do not re-ask what the brief already answers.

**Revising?** Say what changed and what you left alone, so the user can trust the result without rereading all of it:

> Rewrote `<tasks>` to name the CRM tool, added `<tool_use>` and
> `<knowledge_routing>`. Left `<role>`, `<tone>` and `<rules>` exactly as we
> agreed them.

## What goes where

The brief has thirteen slots. They do not map one-to-one:

| Brief slot | Where it lands |
|---|---|
| Role | `<role>` |
| Users | `<role>` - who the agent serves is part of what it is |
| Tone | `<tone>` |
| Tasks | `<tasks>` |
| Inputs | `<tasks>` - each task names what it receives |
| Knowledge | `<knowledge_routing>` |
| Outputs | `<tasks>`, and `<output_format>` when a format is fixed |
| Rules | `<rules>` |
| Escalation | `<escalation>` |
| Connected agents | `<connected_agents>` |
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
| `<knowledge_routing>` | The brief names a knowledge source, or one is attached to the agent |
| `<tool_use>` | The tool plan lists any tool, connector or workflow |
| `<connected_agents>` | The brief names another agent this one hands work to |
| `<escalation>` | The brief names a hand-off condition |
| `<out_of_scope>` | The brief names something the agent must refuse |
| `<data_handling>` | The inputs carry personal, financial or regulated data |
| `<examples>` | The user supplied a sample output worth imitating |

Anything else gets its own section **only** when the brief holds something none of the sections above can hold without distorting it. Name the tag after what it holds, in `lower_snake_case`.

Order when present: `output_format`, `knowledge_routing`, `tool_use` and `connected_agents` after `instructions`; then `rules`, `escalation`, `out_of_scope`, `data_handling`, and `examples` last.

`<knowledge_routing>` and `<connected_agents>` come from the brief, so the draft pass can write both. `<tool_use>` cannot - nothing it names exists until the tool plan does, which is what the **revise pass** is for.

### `<knowledge_routing>`

Say where an answer comes from, and what happens when it is not there. An agent with knowledge attached and no routing will answer confidently from its own reasoning when the source disagrees.

```xml
<knowledge_routing>
Answer from the lending policy knowledge source for anything about limits,
covenants or approval thresholds. Quote the clause you used.
If the policy does not cover the question, say so and answer from general
practice - and label which you did.
If the policy and a document the user attached disagree, the policy wins.
Say that the attachment conflicts, and where.
Never state a policy position you cannot point to.
</knowledge_routing>
```

### `<tool_use>`

Say when to reach for a tool rather than answer, and what to do when a call goes wrong. Both failure branches matter: the orchestrator picks tools by description, so near-duplicate tools are the common cause of the wrong one firing.

```xml
<tool_use>
Call the CRM tool for anything about a specific named customer - never answer
from memory about a customer's record.
Call it once. If it returns nothing, say the record was not found rather
than retrying or guessing.
If a call fails, tell the user what failed and what you could not determine.
Do not carry on as though it succeeded.
If two tools could serve a request, prefer the one that only reads.
</tool_use>
```

### `<connected_agents>`

Name each delegate and the exact signal that hands work to it. The failure to design against is an agent that either hoards work it should pass on, or passes on work it should have done.

```xml
<connected_agents>
Hand quote and discount requests to the Pricing agent. Pass the customer
name and the products asked about.
Everything else stays with you, including questions that merely mention
price in passing.
When you hand off, tell the user you are doing so and why.
</connected_agents>
```

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

Never trim `<role>`, `<tone>`, `<rules>`, `<tool_use>` or `<knowledge_routing>` to fit. Those five decide what the agent does and where its answers come from; cutting them produces a shorter agent that is wrong. If the instructions cannot reach 8,000 without cutting them, the agent is doing too much and should be split.

> Your instructions come to 9,400 characters. Two things in them are
> reference, not behaviour: the 40-line memo template, and the product
> glossary. Move those into a skill and a knowledge source and the
> instructions drop to about 3,200 - which also frees context on every turn.
> Want me to do that, or shall I trim instead?

## Hand off

### After the draft pass

Show the instructions in the conversation and ask the user to correct them. **Produce no file.** Then say why, and what happens next:

> This is the draft. Nothing goes into the Build tab yet - once you add tools
> and skills, the sections that reference them have to be rewritten, and
> anything you hand-edited in the box would be lost.
>
> Keep this conversation open. Run `copilot-find-skills-and-tools` next, then
> `copilot-skill-creator` if the agent needs a packaged capability. Come back
> here afterwards and I will revise these against what you actually built.

### After the revise pass

Produce `instructions.md` as a file the user can download, containing the XML sections and nothing else - no preamble, no explanation, no code fence around the whole thing. Everything in that file gets pasted verbatim.

> Save this file. To apply it: **Build** tab > the space under
> **Instructions** > paste the whole file > **Save**.
>
> Saved instructions take effect **immediately**, including in a conversation
> that is already running. That is the reason not to paste them mid-build: it
> rewrites the agent you are building with, halfway through. If you are working
> through the build route, stage 7 applies them.
>
> When you do apply them, test in a fresh chat. An old conversation carries
> history that muddies what you are reading.
>
> If you are working through the build route, do not paste it yet - stage 7
> applies everything at once, and there is still a stage to go.
>
> Run `copilot-evaluation-creator` next to build the tests.
>
> If you add or remove a tool, skill or connected agent later, come back - the
> instructions name them, so they go stale the moment those change.

> Running in an IDE with file access? Write `instructions.md` into the agent
> folder instead of handing it over for download.
