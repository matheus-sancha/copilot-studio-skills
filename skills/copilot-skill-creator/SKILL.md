---
name: copilot-skill-creator
description: Builds one custom Agent Skill for a Copilot Studio agent and hands back the SKILL.md ready to upload. Use when the user wants to package a capability as a skill, needs an agent to produce a document in a fixed format, or asks how to turn a task into a reusable skill.
license: MIT
---

# Skill creator

Build one Agent Skill for the user's Copilot Studio agent, ready to upload.

## Start

Read the agent brief - earlier in this conversation, or a re-supplied `agent-brief.md`.

**Brief present?** Name the tasks that would work better as a skill than as instructions, and let the user choose one:

> Three tasks in your brief look like skills rather than instructions:
>
>   A. Draft the memo from a financial pack
>   B. Update a prior-year memo against new figures
>   C. Produce the committee pack (pptx)
>
> Which shall I build? An agent holds at most 8 skills; you are using 0.

**No brief?** Ask what capability they want to package, then continue. Do not run a full agent interview - that is `copilot-agent-review`.

Build **one skill per run**. A user who wants three runs this three times, and gets three focused skills instead of one bulk batch nobody checked.

## Is it a skill or is it instructions?

A task earns its own skill when at least one is true:

- It needs bundled reference material - a template, a rulebook, a lookup table.
- It follows a fixed multi-step procedure that must run the same way every time.
- It produces a specific output format with its own conventions.
- It is only needed sometimes, so loading it always would waste context.

Otherwise it belongs in the agent's instructions. Say so rather than building it:

> "Answer questions about the lending policy" is not a skill - it is what the
> agent already does. Put it in the instructions instead.

## What a generated skill looks like

Always a **single `SKILL.md` file**. No `scripts/` folder, no bundled resources - so the user uploads the `.md` directly with nothing to package.

```markdown
---
name: committee-pack-builder
description: Produces the monthly credit committee pack as a pptx from approved memos. Use when the user asks for the committee pack, the monthly deck, or slides for committee.
---

# Committee pack builder

<what this skill produces, in one line>

## Steps

1. ...
2. ...

## Rules

- ...

## Output

<what the finished file looks like - lifted from the right playbook>
```

Frontmatter is not negotiable. Copilot Studio silently skips a skill that breaks these:

- `name`: max 64 characters, lowercase letters, numbers and hyphens only, no leading, trailing or consecutive hyphen.
- `description`: **one line**. State what it does *and* when to use it, with the words a user would actually type. This is the only thing the runtime sees when deciding whether to activate the skill, so a vague description means a skill that never fires.
- Quote any value containing a colon: `description: "Builds: the pack"`.
- Save as UTF-8 without a byte-order mark.
- Keep the whole file under 20,000 characters.

## Python goes inside SKILL.md

When a step needs code, write the Python **into `SKILL.md`** as a fenced block and tell the agent to run it. Never produce a separate script file.

````markdown
Run this to check the totals before writing anything:

```python
rows = [...]          # parsed from the workbook
total = sum(r["amount"] for r in rows)
print(f"{len(rows)} rows, total {total:,.2f}")
```

If the totals do not match the cover sheet, stop and tell the user.
````

Two constraints on that code, both from the sandbox it runs in:

- **Prefer the standard library.** Microsoft publishes no list of preinstalled packages and nothing can be installed at runtime, so an import is a gamble.
- **No network.** The sandbox has no internet access, so code cannot fetch anything. Data must already be in the conversation.

If a library is genuinely needed, name it in the skill and have it say clearly what to do when the import fails, rather than failing silently.

Do not write code for building Office or PDF files. The harness creates and edits Word, Excel, PowerPoint and PDF files natively - code there duplicates what already works and adds a dependency you cannot verify.

## Output format

When the skill produces a file, read the playbook for that format and adapt its fragment into the skill's `## Output` section:

| Format | Playbook |
|---|---|
| Excel | [references/output-xlsx.md](references/output-xlsx.md) |
| PowerPoint | [references/output-pptx.md](references/output-pptx.md) |
| Word | [references/output-docx.md](references/output-docx.md) |
| PDF | [references/output-pdf.md](references/output-pdf.md) |
| Markdown | [references/output-md.md](references/output-md.md) |
| HTML | [references/output-html.md](references/output-html.md) |

Read only the one you need. The fragment is a starting point - adapt it to this agent's actual output, and keep the rules.

## Check before handing over

Run this list and fix anything that fails:

- `name` obeys the character rules and matches what you called the skill.
- `description` is one line and names the words a user would type.
- The file is under 20,000 characters.
- Every step is something the agent can actually do - no step assumes a tool the agent does not have.
- Any inline Python is standard library, or names its dependency explicitly.
- The skill does one thing. If it has two unrelated jobs, split it and build the other next run.

## Hand off

Produce the `SKILL.md` as a file the user can download. Name the file after the skill.

> Open your agent in Copilot Studio, go to the **Build** tab, select **Skills**,
> then **Add skill** > **Upload a skill**, and drop this file in. Test it in the
> **Preview** tab by asking for the thing it does.
>
> If it does not appear after saving, the frontmatter failed validation - check
> the file is UTF-8 without a BOM and that `name` uses only lowercase letters,
> numbers and hyphens.

Then say what is left:

> That is 1 of your 8 skill slots. Run me again to build the next one, or run
> `copilot-evaluation-creator` to build tests for what you have.

> Running in an IDE with file access? Write the skill folder into the agent
> directory instead of handing the file over for download.
