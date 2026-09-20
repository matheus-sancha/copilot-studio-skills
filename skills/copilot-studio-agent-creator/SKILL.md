---
name: copilot-studio-agent-creator
description: Routes the user through building a Copilot Studio agent - working out which stage they are at and which skill to load next, from first idea through instructions, tools, skills and tests. Use when the user wants to build an agent, does not know where to start, or asks what to do next.
license: MIT
---

# Agent creator

Work out where the user is, and tell them which skill to load next.

This skill does not build anything. It routes. Each stage is a separate skill the user loads, runs, and removes.

## How the build works

Say this once, at the start:

> I will point you to one skill at a time. Load it, run it, then remove it
> before loading the next - an agent holds only 8 skills, and every loaded
> skill takes up context that this conversation needs.
>
> Two things to do as we go:
> - **Keep this one conversation** for the whole build. Each skill reads what
>   the earlier ones established.
> - **Save every file I hand you.** If this conversation is ever lost, the
>   brief is how we pick up where we left off.

## Place them

Ask one question, and route on the answer:

```
Which of these do you already have?

  A. Nothing yet - just an idea
  B. A clear written brief of what the agent should do
  C. Instructions already in the agent's Build tab
  D. A working agent I want to test

Reply A, B, C or D - or describe where you are.
```

| Answer | Load next |
|---|---|
| A | `copilot-agent-review` |
| B | `copilot-instructions-creator` |
| C | `copilot-find-skills-and-tools` |
| D | `copilot-evaluation-creator` |

If their answer does not fit cleanly, place them at the **earliest** stage they have not genuinely completed. A thin brief is not a brief.

## The route

1. **`copilot-agent-review`** - interviews them and produces `agent-brief.md`.
2. **`copilot-instructions-creator`** - turns the brief into `instructions.md` for the Build tab.
3. **`copilot-find-skills-and-tools`** - recommends connectors, tools and pre-built skills.
4. **`copilot-skill-creator`** - packages a capability as a skill. Repeat per skill.
5. **`copilot-evaluation-creator`** - builds `evaluation-set.csv` for the Evaluate tab.

Stages 3 and 4 are skippable when the agent needs no tools and no packaged capabilities. Stages 1, 2 and 5 are not - an agent with no brief, no instructions or no tests is not finished.

## Hand off a stage

Each time, say three things: what to remove, what to load, and what they will get back.

> Stage 1 of 5.
>
> Remove any other skill from the **Skills** panel, then upload
> `copilot-agent-review`. It will interview you about the agent - expect to be
> pushed for specifics - and hand back `agent-brief.md`.
>
> Come back here when it is done.

When they return, confirm the stage produced its artifact before moving on. A stage that ended without its file is not finished, however long it took.

## When the thread is lost

If the user arrives with no context and a build already underway:

> Re-upload `agent-brief.md` and tell me which stages you finished. We pick up
> from there.

If they have no brief either, they start at stage 1. Say so plainly rather than trying to reconstruct it from memory - a half-remembered brief produces an agent nobody checked.

## Before they ship

When all stages are done, remind them once:

> Delete every `copilot-*` skill from the agent before you publish. They were
> here to build the agent, not to be part of it.

> Running in an IDE with file access? The same route applies, but each skill
> writes its file into the agent folder instead of handing it to you.
