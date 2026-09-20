---
name: copilot-skill-creator
description: Builds one custom Agent Skill for a Copilot Studio agent - instructions, bundled references and runnable scripts - and hands it back ready to upload. Use when the user wants to package a capability as a skill, needs an agent to produce a document in a fixed format, or asks how to turn a task into a reusable skill.
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

Start from a **single `SKILL.md`**, and add bundled files only when one of the tests below is met. A single file uploads as a bare `.md` with nothing to package; the moment anything is bundled, it has to be zipped.

```
skill-name/
  SKILL.md        required
  references/     material the agent reads
  scripts/        code the agent runs
```

All three work on this harness - verified, not assumed. Bundled reference files are readable at runtime, and bundled scripts execute.

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

## Inline code or a bundled script

Both run. The choice is about size and reuse, not capability.

**Write it inline in `SKILL.md`** when the code is short, used once, and reads as part of the instructions - roughly fifteen lines or fewer:

````markdown
Check the totals before writing anything:

```python
total = sum(r["amount"] for r in rows)
print(f"{len(rows)} rows, total {total:,.2f}")
```

If they do not match the cover sheet, stop and tell the user.
````

**Bundle it as `scripts/name.py`** when any of these is true:

- It runs to more than about fifteen lines.
- More than one step uses it.
- It must produce identical output every time, so the model must not be free to paraphrase it.

Bundled scripts must be **self-contained and print their result** - the agent reads standard output. Have the script fail loudly with a clear message rather than returning something plausible and wrong.

Never split one piece of logic across both places.

### The sandbox

Measured on a live tenant, not inferred:

```
python 3.12 on Linux
```

These packages are **available** - use them directly, no defensive import:

`openpyxl` · `xlsxwriter` · `docx` · `pptx` · `reportlab` · `pypdf` · `PIL` · `pandas` · `numpy` · `matplotlib` · `bs4` · `lxml` · `yaml` · `jinja2`

`fpdf` is **not** available - use `reportlab` for PDF generation.

Two hard limits:

- **No network.** `requests` imports successfully but every call fails, because the sandbox has no internet access at runtime. The same applies to anything in `bs4` or `lxml` that fetches rather than parses. All data must already be in the conversation.
- **No installation.** Nothing can be pip-installed at runtime. Anything outside the list above is a gamble - if the skill needs one, say so in the skill and have it report clearly when the import fails.

The list reflects one tenant at one moment and Microsoft guarantees nothing. If a generated skill depends on a package, tell the user to confirm it in their own tenant.

### Do not script what the harness does natively

The harness creates and edits Word, Excel, PowerPoint and PDF files by itself. Reach for `openpyxl` or `python-pptx` only when you need control the harness cannot give - an exact template, a formula, a precise cell format. For ordinary documents, describe the output and let the harness build it.

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
- Any Python, inline or bundled, uses only packages confirmed available, and a bundled script prints its result.
- The skill does one thing. If it has two unrelated jobs, split it and build the other next run.

## Hand off

### A single-file skill

Produce the `SKILL.md` as a file the user can download, named after the skill. No packaging needed.

> Open your agent in Copilot Studio, go to the **Build** tab, select **Skills**,
> then **Add skill** > **Upload a skill**, and drop this file in. Test it in the
> **Preview** tab by asking for the thing it does.

### A skill with bundled files

Hand over every file, and tell the user how to package it. **`SKILL.md` must sit at the root of the zip** - a bundle with everything inside a `skill-name/` folder is rejected with *"Bundle is missing a root-level SKILL.md file."*

```
skill-name.zip
  SKILL.md              <- at the root, not inside a folder
  references/...
  scripts/...
```

> Put `SKILL.md` and the folders in one directory, then zip **the contents**,
> not the directory itself. On Windows: open the folder, select all the items
> inside it, right-click > **Send to** > **Compressed (zipped) folder**.
>
> Before uploading, open the `.zip` and check `SKILL.md` is the first thing you
> see. If you see a folder instead, you zipped one level too high.

If the user builds bundles with PowerShell, warn them: `Compress-Archive` writes entry paths with backslashes, which the zip format does not allow, and the package can be refused with no useful error. Use `System.IO.Compression.ZipFile` with forward-slash entry names instead.

### Either way

> If the skill does not appear after saving, the frontmatter failed validation -
> check the file is UTF-8 without a BOM and that `name` uses only lowercase
> letters, numbers and hyphens.

Then say what is left:

> That is 1 of your 8 skill slots. Run me again to build the next one, or run
> `copilot-evaluation-creator` to build tests for what you have.

> Running in an IDE with file access? Write the skill folder into the agent
> directory instead of handing the file over for download.
