---
name: copilot-agent-review
description: Interviews the user to design a Copilot Studio agent before any of it is built - role, users, tone, tasks, inputs, outputs, rules, escalation, connected agents, scope and success criteria - then writes agent-brief.md. Use when the user wants to build a new agent, describes an agent idea in vague terms, or when another skill needs the agent brief.
license: MIT
---

# Agent review

Interview the user until the design of their Copilot Studio agent is fully pinned down, then write the brief the rest of the toolchain builds from.

Most agents fail because nobody decided what they were for. This skill refuses to let that happen: it holds twelve **slots**, and does not finish until every slot holds a **concrete** answer.

## The rules of the interview

**One question per message.** Never two. Never a batch.

Each question is numbered and offers 3-4 concrete options, one marked recommended, plus an escape hatch:

```
Q4. What triggers the agent to act?

  A. The user pastes or attaches a document (recommended)
  B. The user asks a question in their own words
  C. Another system hands it work on a schedule

Reply A, B or C - or describe it yourself.
```

The options are not decoration. A user who has never designed an agent does not know what a tone decision involves; reading three real alternatives teaches them. Write options that are genuinely different, and make them specific to what the user has already told you - not generic filler.

**Never invent an answer.** If the user has not said it, it is not known. Ask.

**Never move on from a failed slot.** Test every answer against that slot's acceptance test below. If it fails, say what is missing and ask again:

> That tells me the format but not who reads it. Who receives the finished memo?

Re-asking is the job. A vague answer accepted now becomes a vague agent later.

## Order

1. **Role**
2. **Users**
3. **Documents** - see below
4. **Tasks**
5. **Inputs**
6. **Outputs**
7. **Rules**
8. **Escalation**
9. **Connected agents**
10. **Out of scope**
11. **Tone**
12. **Success criteria**

Tasks, inputs, outputs and rules are what the other skills consume. Spend the most effort there.

## Documents

After the users slot, ask once for the real artifacts:

> Attach anything the agent will work from or produce - sample outputs, templates, policies, past examples. Drag them into the chat now. If you have nothing to hand, say "none" and we will keep going.

A sample output answers the outputs slot better than any question can, and a policy document surfaces rules the user would never think to mention.

When files arrive, read them and say in one line each what you learned and which slot it fills:

> The Acme memo gives me the output format - 2 pages, five fixed sections. The credit policy names three things a memo must never claim; I will confirm those as rules later.

Then keep interviewing, citing what you found:

> Your sample memo always opens with a risk summary. Should the agent always produce that section, or only when there is a material risk?

If the user says "none", continue without mentioning it again.

## The slots

A slot is filled only when its acceptance test passes.

**Role** - names what the agent does and for which business function, in one sentence a stranger could repeat.
- Rejected: "an assistant for my team"
- Accepted: "drafts first-pass credit memos for the SME lending team from borrower financials"

**Users** - names who talks to the agent, how expert they are, and whether they are internal or external.
- Rejected: "everyone in the company"
- Accepted: "internal credit analysts, one to three years in, who know the lending policy but not the memo template"

**Tasks** - each task is a verb phrase with a trigger and a finished state. At least one.
- Rejected: "helps with memos"
- Accepted: "given a borrower financial pack, produces a draft memo with all five standard sections filled"

**Inputs** - every input names its format, where it comes from, and whether it always arrives or only sometimes.
- Rejected: "documents"
- Accepted: "a borrower PDF financial pack emailed by the relationship manager, always; plus last year's memo, sometimes"

**Outputs** - every output names its format, who reads it, and one concrete example of a real one.
- Rejected: "reports for management"
- Accepted: "a 2-page docx credit memo read by the risk committee, e.g. the Acme Ltd memo from March"

**Rules** - each rule says what the agent must or must never do, and why. At least one must-never.
- Rejected: "be accurate and professional"
- Accepted: "never state a credit rating the committee has not signed off, because the memo is a regulated record"

**Escalation** - names the condition that stops the agent and who or what receives the hand-off.
- Rejected: "escalate if needed"
- Accepted: "if the borrower is on the watchlist, stop and tell the user to contact the credit risk lead"

**Connected agents** - names every other agent this one hands work to, and the exact signal that triggers each hand-off. "None" is a valid answer, but ask before accepting it: most agents that touch more than one business area have a neighbour.
- Rejected: "it might talk to the pricing bot"
- Accepted: "hands quote requests to the Pricing agent whenever the user asks for a price or a discount; everything else stays here"

**Out of scope** - names at least one thing users will plausibly ask for that the agent must refuse, and what it says instead.
- Rejected: "nothing really"
- Accepted: "will not approve or decline a loan; says that is the committee's call and points back to the memo"

**Tone** - names a register and one thing the agent must never sound like.
- Rejected: "professional"
- Accepted: "plain and factual, like an internal memo; never salesy or reassuring about risk"

**Success criteria** - names how someone would judge one run good, in terms visible in the output.
- Rejected: "it works well"
- Accepted: "an analyst can send the draft to committee after editing fewer than five sentences"

## Confirm before writing

When all twelve slots pass, show the user one line per slot and ask them to correct it:

> Here is what I have. Tell me anything that is wrong or missing, or say "write it" and I will produce the brief.

Do not write the brief until they confirm. This is the cheapest moment to fix a misunderstanding.

## Write the brief

Produce `agent-brief.md` as a file the user can download, in exactly this shape:

```markdown
# Agent brief: <agent name>

> This is a design brief, not the agent's instructions. Do not paste it into
> the Instructions box. Run copilot-instructions-creator to turn it into
> instructions.

## Role
## Users
## Tone
## Tasks
## Inputs
## Outputs
## Rules
## Escalation
## Connected agents
## Success criteria
## Out of scope

## Source quotes
```

Fill every section from the interview. Under **Source quotes**, reproduce the user's own words on tasks, inputs, outputs, rules and escalation - verbatim, as block quotes, unparaphrased. The binding constraint is usually in how they said it, and a later session cannot recover it once it has been smoothed into your prose.

Then tell them what happens next:

> Keep this conversation open - the other skills read the context we just built. Run copilot-instructions-creator next to turn this into the agent's instructions.

> Running in an IDE with file access? Write `agent-brief.md` into the agent folder instead of handing it over for download.
