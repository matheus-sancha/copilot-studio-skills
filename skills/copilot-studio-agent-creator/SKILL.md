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
>   end.** A skill you upload does not reach this conversation at all - it takes
>   effect in the next one. Instructions are the opposite: they land
>   immediately, so pasting them now would rewrite the agent you are building
>   with, halfway through the build. Both are reasons to wait. Stage 7 applies
>   it all in one pass.
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
7. **Apply it all, and publish** - the only stage that changes the agent. Hands over `publish-copy.md` first, then an ordered checklist. Nothing before it touches the Build tab.

**Nothing is applied until stage 7.** Stages 1 to 6 are design work: each hands back a file the user saves. This is not tidiness - an uploaded skill does not reach a conversation already in progress, so a skill uploaded at stage 4 would not be live here anyway, and restarting the chat to make it live would throw away the build. Deferring costs nothing, because no stage needs an installed component to be running: stage 5 only has to *name* the tools and skills, not call them.

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

### Stage 7 - apply it all, and publish

The only stage that changes the agent. Reach it when stages 1 to 6 have produced what they owe.

Hand over **two things in the same message, copy first**. Step 1 of the checklist deletes this skill, so anything not handed over now cannot be handed over at all.

#### First, `publish-copy.md`

Copilot Studio refuses to publish an agent that has no **name, description or instructions**. The description is the one piece of user-facing copy the product demands, and a maker who has just spent six stages on the agent should not be writing it from a blank box.

Produce a file with three parts, drawn from the brief - not invented:

| Part | Length | Built from | Where it goes |
|---|---|---|---|
| **Short description** | one or two sentences | role, users, the headline task | the **Description** field - required before Copilot Studio will publish |
| **Long description** | three or four short paragraphs | tasks, inputs, knowledge, out of scope | **no field on this harness.** For the organization catalog entry, a Teams or Microsoft 365 listing, or the message announcing it |
| **Disclaimer** | three or four lines | rules, escalation, anything regulated in the brief | no field either. Put it at the foot of the long description, and consider a line in the agent's own instructions |

Be straight about that third column. Only the short description has a documented home; the other two are copy the user places wherever they announce the agent. Do not tell them to paste it into a field that does not exist.

```markdown
## Short description

Drafts first-pass credit memos for the SME lending team from borrower
financials, so an analyst starts from a filled template rather than a blank one.

## Long description

Give it a borrower financial pack and it drafts all five standard sections of
the credit memo, ending with the three figures the committee always asks for.
Give it last year's memo alongside new financials and it updates the memo and
lists what changed.

It answers policy questions from the lending policy knowledge source and quotes
the clause it used. Where the policy is silent it says so, and answers from
general practice - labelled as such.

It will not state a credit rating the committee has not signed off, and it will
not estimate a figure that is missing from the pack. It asks instead.

## Disclaimer

This agent drafts; it does not decide. Every memo is a first pass and must be
reviewed by the analyst who owns the file before it goes to committee.

Figures come from the pack you supply. Check them against the source before
relying on any number in the output.

It is not a system of record. Nothing it produces is a regulated record until a
human commits it as one.
```

Match the agent. A read-only internal helper does not need a regulated-record warning, and pretending otherwise teaches people to skip disclaimers. Write what is actually true of **this** agent, from what the brief captured - and if the brief captured no rules and no escalation, say the disclaimer is thin because the design never named a limit, rather than padding it.

#### Then, the checklist

Build it from what **this** build actually produced - naming each generated skill, listing the tools from `tool-plan.md`, and dropping any line for a stage that was skipped.

Tell them to do it in this order, and say why the order matters:

> Stage 7 of 7. Nothing left to decide - go and apply it.
>
> **Save `publish-copy.md` before step 1.** Step 1 deletes me.
>
> 1. **Build** > **Skills**: delete all six `copilot-*` skills. Do this first -
>    an agent holds 8, and mine are using six of the slots.
> 2. **Build** > **Skills**: upload `<each skill from stage 4>`.
> 3. **Build** > **Tools**: add `<each tool from tool-plan.md>`.
> 4. **Build** > **Instructions**: paste `instructions.md` in full, **Save**.
> 5. **Start a new chat**, then test in **Preview**. None of the above is live
>    in a conversation that was already open - including this one.
> 6. **Evaluate** tab > **New evaluation**: drop in `evaluation-set.csv`.
> 7. When the tests look right: paste the short description into **Description**,
>    then **Publish**. The long description and disclaimer go wherever you
>    announce the agent.
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
| 7 | `publish-copy.md`, then the agent actually changed, and a new chat started to test it |

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
