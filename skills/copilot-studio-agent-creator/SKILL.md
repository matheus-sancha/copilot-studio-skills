---
name: copilot-studio-agent-creator
description: Routes the user through building a Copilot Studio agent - working out which stage they are at and which skill to load next, from first idea through instructions, tools, skills and tests. Use when the user wants to build an agent, does not know where to start, or asks what to do next.
license: MIT
---

# Agent creator

Work out where the user is, and tell them which skill to load next.

This skill does not build anything. It routes. Each stage is a separate skill, and all six stay loaded from start to finish - nothing is added to or removed from the agent until the build is over.

## How the build works

Say this once, at the start:

> Upload all six `copilot-*` skills now and leave them loaded until the build
> is done. I will tell you which one to use at each stage.
>
> Two things to do as we go:
> - **Keep this one conversation** for the whole build. Each skill reads what
>   the earlier ones established, and if the conversation is lost, the brief is
>   how we pick up where we left off.
> - **Save every file I hand you, and change nothing in the agent until the
>   end.** A skill you upload, a tool you add or instructions you paste do not
>   reach a conversation that is already running - they take effect in the next
>   one. So applying anything now would either do nothing, or cost us this
>   conversation to pick up. Stage 7 applies it all in one pass.
>
> Your instructions get drafted early but only handed over near the end, once
> the tools and skills they refer to actually exist.

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
7. **Apply it all** - the only stage that changes the agent. Nothing before it touches the Build tab.

**Nothing is applied until stage 7.** Stages 1 to 6 are design work: each hands back a file the user saves. This is not tidiness - a component added to an agent does not reach a conversation already in progress, so a skill uploaded at stage 4 would not be live here anyway, and restarting the chat to make it live would throw away the build. Deferring costs nothing, because no stage needs an uploaded component to be running: stage 5 only has to *name* the tools and skills, not call them.

**Instructions are written twice on purpose.** They name the agent's tools, skills and connected agents, so they cannot be finished before those exist. The draft at stage 2 is there to catch design errors while the thinking is fresh; the file only arrives at stage 5, so there is one paste and nothing to hand-edit in between.

Stages 3 and 4 are skippable when the agent needs no tools and no packaged capabilities - and when both are skipped, stage 5 is just a confirmation that the draft still stands. Stages 1, 2 and 6 are never skippable: an agent with no brief, no instructions or no tests is not finished.

## Hand off a stage

Each time, say which skill to use, what it will do, and what they get back.

> Stage 1 of 7.
>
> Ask `copilot-agent-review` to interview you. Expect to be pushed for
> specifics - it will not accept a vague answer. It hands back
> `agent-brief.md`.
>
> Come back here when it is done.

### Stage 7 - apply it all

The only stage that changes the agent. Reach it when stages 1 to 6 have produced what they owe, and hand over an ordered checklist built from what **this** build actually produced - naming each generated skill, listing the tools from `tool-plan.md`, and dropping any line for a stage that was skipped.

Tell them to do it in this order, and say why the order matters:

> Stage 7 of 7. Nothing left to decide - go and apply it.
>
> 1. **Build** > **Skills**: delete all six `copilot-*` skills. Do this first -
>    an agent holds 8, and mine are using six of the slots.
> 2. **Build** > **Skills**: upload `<each skill from stage 4>`.
> 3. **Build** > **Tools**: add `<each tool from tool-plan.md>`.
> 4. **Build** > **Instructions**: paste `instructions.md` in full, **Save**.
> 5. **Start a new chat**, then test in **Preview**. None of the above is live
>    in a conversation that was already open - including this one.
> 6. **Evaluate** tab > **New evaluation**: drop in `evaluation-set.csv`.
>
> Keep `agent-brief.md`. It is the design record, and the only way back if you
> want to change something later.

Step 5 is the one people skip. Say it plainly: testing in this conversation tests the agent as it was before any of this.

When they return from any stage, confirm it produced what it owes before moving on. A stage that ended without it is not finished, however long it took.

| Stage | Owes |
|---|---|
| 1 | `agent-brief.md` |
| 2 | a draft the user has read and agreed - **no file** |
| 3 | `tool-plan.md` |
| 4 | one skill file per capability |
| 5 | `instructions.md` |
| 6 | `evaluation-set.csv` |
| 7 | the agent actually changed, and a new chat started to test it |

## When the thread is lost

If the user arrives with no context and a build already underway:

> Re-upload `agent-brief.md` and tell me which stages you finished. We pick up
> from there.

If they have no brief either, they start at stage 1. Say so plainly rather than trying to reconstruct it from memory - a half-remembered brief produces an agent nobody checked.

## Before they ship

Stage 7 deletes the `copilot-*` skills as its first step. If they reach the end with any still installed, say so once:

> Delete every `copilot-*` skill from the agent before you publish. They were
> here to build the agent, not to be part of it.

> Running in an IDE with file access? The same route applies, but each skill
> writes its file into the agent folder instead of handing it to you.
