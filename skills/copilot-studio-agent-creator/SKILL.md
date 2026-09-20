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

> Upload all six `copilot-*` skills now and leave them loaded. I will tell you
> which one to use at each stage.
>
> Three things to do as we go:
> - **Keep this one conversation** for the whole build. Each skill reads what
>   the earlier ones established.
> - **Save every file I hand you.** If this conversation is ever lost, the
>   brief is how we pick up where we left off.
> - **Watch the slot count.** An agent holds 8 skills. These six take six of
>   them, so before we build skills for your agent itself, we remove the
>   `copilot-*` skills you are finished with.
>
> Your instructions get drafted early but only handed over near the end, once
> the tools and skills they refer to actually exist. Nothing goes into the
> Build tab's Instructions box until then.

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
| B | `copilot-instructions-creator` (draft pass) |
| C | `copilot-find-skills-and-tools` |
| D | `copilot-instructions-creator` (revise pass), then `copilot-evaluation-creator` |

If their answer does not fit cleanly, place them at the **earliest** stage they have not genuinely completed. A thin brief is not a brief.

## The route

1. **`copilot-agent-review`** - interviews them and produces `agent-brief.md`.
2. **`copilot-instructions-creator`** *(draft)* - drafts the instructions in the conversation. **No file yet.**
3. **`copilot-find-skills-and-tools`** - recommends connectors, tools and pre-built skills; produces `tool-plan.md`.
4. **`copilot-skill-creator`** - packages a capability as a skill. Repeat per skill.
5. **`copilot-instructions-creator`** *(revise)* - rewrites the sections that reference tools, skills and connected agents, then produces `instructions.md`.
6. **`copilot-evaluation-creator`** - builds `evaluation-set.csv` for the Evaluate tab.

**Instructions are written twice on purpose.** They name the agent's tools, skills and connected agents, so they cannot be finished before those exist. The draft at stage 2 is there to catch design errors while the thinking is fresh; the file only arrives at stage 5, so there is one paste and nothing to hand-edit in between.

Stages 3 and 4 are skippable when the agent needs no tools and no packaged capabilities - and when both are skipped, stage 5 is just a confirmation that the draft still stands. Stages 1, 2 and 6 are never skippable: an agent with no brief, no instructions or no tests is not finished.

## Hand off a stage

Each time, say which skill to use, what it will do, and what they get back.

> Stage 1 of 6.
>
> Ask `copilot-agent-review` to interview you. Expect to be pushed for
> specifics - it will not accept a vague answer. It hands back
> `agent-brief.md`.
>
> Come back here when it is done.

### Before stage 4

Stage 4 creates skills for the agent itself, and the slot count matters there. Say:

> We are about to add skills to your agent, and it can hold 8 in total. Six of
> those are mine. Remove `copilot-agent-review` and `copilot-instructions-creator`
> now - we are done with the first, and the second is not needed again until
> stage 5, when you can re-upload it.
>
> That frees enough room to build what your agent actually needs.

When they return, confirm the stage produced what it owes before moving on. A stage that ended without it is not finished, however long it took.

| Stage | Owes |
|---|---|
| 1 | `agent-brief.md` |
| 2 | a draft the user has read and agreed - **no file** |
| 3 | `tool-plan.md` |
| 4 | one skill file per capability |
| 5 | `instructions.md` |
| 6 | `evaluation-set.csv` |

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
