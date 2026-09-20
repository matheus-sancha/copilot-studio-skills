# The Copilot Studio Agent Skill contract

Research for [issue #2](https://github.com/matheus-sancha/copilot-studio-skills/issues/2). Verified 2026-09-20 against Microsoft Learn and the Agent Skills specification.

## Answer in brief

A skill is a folder whose only required file is `SKILL.md` — YAML frontmatter carrying `name` and `description`, then Markdown instructions. Copilot Studio accepts **either** a bare `.md` file **or** a `.zip` containing `SKILL.md` plus supporting files ([skills-add-existing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing)). This is the open [Agent Skills format](https://agentskills.io/specification), originally from Anthropic, so a skill written for Claude Code is structurally the same artifact.

Three facts change how this repo must be built:

1. **Skills only exist on the GitHub Copilot harness.** The standard harness and the Copilot chat harness do not support them ([harnesses-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)). Every skill in this repo has that as a hard prerequisite, and the README must say so.
2. **Bundled resources only survive the `.zip` path.** Uploading a bare `SKILL.md` carries no `references/` or `assets/`, and **downloading** a skill back out of Copilot Studio returns only a Markdown file ([skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)) — a round-trip through the product silently drops bundled files.
3. **The agent already creates Word/Excel/PowerPoint/PDF files natively and offers them as downloads.** No code-interpreter plumbing is needed for the "emit a document" flow this repo is built around.

## The file contract

### Required structure

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

Source: [Agent Skills specification — Directory structure](https://agentskills.io/specification). Copilot Studio describes the same thing as "a required `SKILL.md` file … plus optional supported resource files and optional supported scripts and supporting folders" ([skills-add-existing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing)).

### Frontmatter schema

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | "Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen." Also: must not contain consecutive hyphens, and **must match the parent directory name** |
| `description` | Yes | "Max 1024 characters. Non-empty. Describes what the skill does and when to use it." |
| `license` | No | License name or a bundled license file |
| `compatibility` | No | "Max 500 characters" — environment requirements |
| `metadata` | No | Arbitrary string→string map |
| `allowed-tools` | No | Space-separated pre-approved tools (experimental; support varies by client) |

Source: [Agent Skills specification — Frontmatter](https://agentskills.io/specification).

Copilot Studio independently states the same naming rule in its own UI guidance: "Use only lowercase letters, numbers, and hyphens. Don't start or end the name with a hyphen" ([skills-create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create)).

### Copilot Studio's own load-time validation

Copilot Studio publishes the exact reasons a skill is silently skipped at load ([skills-manage — Troubleshoot skills that don't load](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)). Each is a rule this repo must satisfy:

| Failure | Rule it implies |
|---|---|
| Invalid YAML frontmatter | Quote any string value containing a colon — `description: "My: skill"` |
| Missing `name` / `description` | Both must be present and non-empty |
| **Description too long** | "The effective `description` is longer than the model-facing catalog can accept. Shorten the description to a single line" |
| Duplicate skill name | "Two skills in the same agent use the same folder name" — all six skills in this repo must have distinct names, since a user may load several at once |
| Unreadable `SKILL.md` | Must be **UTF-8 without a byte-order mark** |
| Resource file wasn't written | A bundled file failed to install — re-upload the package |
| Skill package rejected | The `.zip` failed structural validation |

The last two are the strongest available evidence that bundled resources are genuinely installed and read at runtime: "Skills whose supporting files were partially written still load, but the agent might behave differently at runtime because some of the referenced content is missing."

## Installing, replacing, and removing

All from the **Build** tab ([skills-add-existing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing), [skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)):

- **Upload** — Build → components panel → **Skills** → **Add skill** → **Upload a skill** → drag-and-drop or browse. "The system validates the file and adds the skill to your agent."
- **Replace** — select the skill → **…** → **Replace** → browse to the new file.
- **Download** — select the skill → **…** → **Download**. Returns "a Markdown file containing the skill name and description in YAML front matter, plus instructions. The filename matches the skill's name." **Bundled resources are not included.**
- **Delete** — select the **X** next to the skill → confirm. "Deleting a skill removes it permanently from this agent."

Prerequisite for all of the above: "An agent created with the GitHub Copilot harness" ([skills-add-existing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing)).

Two other authoring paths exist that this repo does not use but should be aware of, since a user may reach for them: **Create from blank** and **Generate with AI** ([skills-create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create)).

## Limits

### Documented and applicable

| Item | Limit | Source |
|---|---|---|
| Size per file the agent creates | **10 MB** | [created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview) |
| Created-file retention | "28 days after the last activity in the conversation" | [created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview) |
| Behaviour over 10 MB | "The file isn't surfaced in the response. The turn continues, and the agent typically explains why the file wasn't produced." | [created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview) |
| User attachment size | **16 MiB** per file | [attachments-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/attachments-overview) |
| Attachment retention | 28 days after last activity | [attachments-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/attachments-overview) |
| URL attachment timeout | 30 seconds; must be publicly reachable | [attachments-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/attachments-overview) |
| Agent icon | PNG, 100 KB or less | [authoring-instructions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions) |

### Specification guidance (recommendations, not enforced)

From [Agent Skills — Progressive disclosure](https://agentskills.io/specification):

- Metadata (`name` + `description`) ≈ **100 tokens**, loaded at startup for every installed skill.
- Full `SKILL.md` body — "**< 5000 tokens recommended**", loaded on activation.
- "Keep your main `SKILL.md` under **500 lines**. Move detailed reference material to separate files."
- "Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains."
- Resources in `scripts/`, `references/`, `assets/` load only when required.

### Not documented — treat as unknown

- **No published character cap on a skill body** for the GitHub Copilot harness.
- **No published cap on the number of skills per agent** for the GitHub Copilot harness.
- **No published character cap on agent instructions** for the GitHub Copilot harness. [authoring-instructions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions) documents a 42-character *name* limit for Copilot-chat-harness agents and states no instruction limit for either.
- **The exact `description` cap Copilot Studio enforces.** The spec says 1024 characters; Copilot Studio says only "longer than the model-facing catalog can accept."

> **Trap — do not cite the quotas page.** [requirements-quotas](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas) lists "Instructions for a Copilot agent | 8,000 characters" and "Skills | 100 per agent", and both are routinely quoted as if universal. That article opens with: "This article describes features used in agents or agent flows powered by the **standard harness**." Its "Skills" row refers to [Azure Bot Service skills](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-add-skills) — an unrelated feature that happens to share the word — and the 8,000-character row is scoped to agents extending Microsoft 365 Copilot. Neither governs Agent Skills on the GitHub Copilot harness.

### The limit that actually bites

There is no per-field cap to design against; there is a **combined context budget**. `CONTEXT_LENGTH_EXCEEDED`: "The combined size of the agent's instructions, the conversation history, the tool definitions, and any tool results is larger than the model can process in a single turn. Long conversations and large numbers of tools are the most common causes." The documented remedies are to shorten instructions, reduce attached tools, start a new conversation, or pick a model with a larger context window ([troubleshooting-error-codes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes)).

This is the real constraint on a repo of six skills meant to be loaded together, and it compounds with the map's decision to carry context in one long chat thread.

## Code execution and file output

Two distinct features share the phrase "code interpreter". Keep them apart.

**1. The GitHub Copilot harness runtime** — what this repo targets. It "natively creates and edits Word, Excel, PowerPoint, and PDF files, supports skills and memory, and runs each task in a secure sandbox governed by Copilot Studio" ([harnesses-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)). The harness comparison table confirms file creation and skills are GitHub-Copilot-harness-only; both are "Not a focus" on the other two harnesses.

Command execution exists and is policed per command: "When an agent uses a tool that runs commands (for example, a code interpreter or a shell tool), Copilot Studio applies safety checks before each command is executed. If a command matches an unsafe pattern, the command isn't executed and the agent reports that the operation was blocked … The block appears as a step in the activity trace" ([troubleshooting-error-codes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes)).

File delivery to the user is automatic and needs no configuration: "You don't configure this behavior explicitly. When the agent needs to write a file to complete a turn, it produces one and includes it in the response." The response carries a **created file card** with the file name, type, a preview or icon, and a **Download** action, rendered "in every surface where the agent runs" — the Preview tab, Teams, Microsoft 365 Copilot, and web chat ([created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview)). Users can also refer back to a created file in a later turn and get an updated version.

**2. Copilot Studio's "code interpreter" feature** — a *prompt*-level capability, enabled per prompt in prompt builder, on the standard-harness side. "Code interpreter is a Python execution engine integrated within Copilot Studio and prompt builder prompts" ([faq-code-interpreter](https://learn.microsoft.com/en-us/microsoft-copilot-studio/faq-code-interpreter)). Its documented limitations are worth knowing because they likely describe the sandbox family generally:

- No reading text from image-based (scanned) PDFs; text-based PDFs are fine.
- "Session timeouts for long-running tasks."
- "Restrictions on external network access."
- "No support for reading files with data protections."
- "Images created with code interpreter are not rendered in the Teams and Microsoft 365 Copilot channel."
- Tenant admins must enable it in the Power Platform admin center; **"This setting is off by default."**
- Public clouds only — no GCC / GCC High.

**Unverified:** whether a Python file bundled in a skill's `scripts/` folder is executed by the GitHub Copilot harness the way Claude Code would run it. Microsoft documents that packages *may* contain scripts and that a command-running tool exists, but no Learn page states that bundled skill scripts are directly executable, nor names the Python runtime or its installed libraries. Design the skills so that **no bundled script is load-bearing** until this is tested in a live tenant.

## Addendum — the adjacent surface (added while resolving [issue #9](https://github.com/matheus-sancha/copilot-studio-skills/issues/9))

Microsoft documents the same Agent Skills format far more precisely for **custom skills in declarative agents** (Agent Builder / Microsoft 365 Copilot) than it does for Copilot Studio. That is a *different product surface*, so the numbers below are a strong signal rather than proof for the GitHub Copilot harness — [issue #12](https://github.com/matheus-sancha/copilot-studio-skills/issues/12) exists to confirm them in a live tenant. Where Copilot Studio is silent, these are the best available figures to design against.

### Package shape — `SKILL.md` at the zip root

```text
my-skill.zip
|-- SKILL.md              # required
|-- <resource files>      # optional
`-- <scripts or folders>  # optional
```

Source: [agent-builder-add-skills](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills). `SKILL.md` sits at the **root of the archive**, not inside a wrapper folder. "Upload the complete `.zip` package. Don't upload `SKILL.md` by itself."

**One zip holds one skill.** There is no documented multi-skill archive. Copilot Studio's own failure table treats skill name and folder name as one-to-one ("Two skills in the same agent use the same folder name"), and the spec requires `name` to match the parent directory. Six skills means six packages and six uploads.

### Support matrix

| Item | Agent Builder | Agents Toolkit |
|---|---|---|
| Maximum skills per agent | **8** | **8** |
| Skill package | Compressed `.zip`, maximum 50 MB | Skill directory; `.zip` isn't supported |
| Maximum file size | 25 MB per file | Complete app package limited to 10 MB |
| Maximum files per package | 350 files across all skills | 350 files across all skills |
| Directory hierarchy | "Maximum directory depth is 3" | "Maximum directory depth is 3" |
| Reuse across agents | "Not supported at this stage of the preview" | Same |

Source: [declarative-agent-skills — Support matrix](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills).

**Skill instructions "must be under 20,000 characters."** This is the only concrete instruction cap Microsoft publishes anywhere for the format. Treat it as the design budget per `SKILL.md`.

The 8-skill ceiling is the sharper constraint for this repo: six skills consume 75% of an agent's budget, leaving two slots for the user's own. It is an argument for the router advising users to load only the skill they need next, rather than all six at once.

### Scripts do execute — inside a hard sandbox

This resolves part of what the main findings above marked unverified. Supported types:

| Category | File types |
|---|---|
| Instructions and resources | `.json`, `.xml`, `.yaml`, `.yml`, `.ini`, `.config`, `.utf8`, `.docx`, `.doc`, `.docm`, `.pdf`, `.txt`, `.rtf`, `.md`, `.ppt`, `.pptx`, `.ppsm`, `.xlsx`, `.xls`, `.xlsm`, `.csv`, `.tsv`, `.html`, `.htm`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.log` |
| Scripts and binaries | `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.sh`, `.bash` |

Sandbox limits ([declarative-agent-skills — Script execution sandbox](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills)):

- Internet or network access from scripts: "Not supported. The sandbox has no network access at runtime."
- Package installation: "Not supported. A skill can't install packages at runtime."
- Preinstalled packages: "A skill can use packages already present in the sandbox. **Don't depend on a package unless its availability is confirmed.**"
- Connectors, API plugins and MCP servers: reachable by the agent through the orchestrator, but "Scripts can't call them through the sandbox."

The conclusion in the main findings stands and is now better founded: a bundled script may run, but since no package list is published and none can be installed, **no bundled script should be load-bearing**. Prefer instructions the harness executes with its native Office and PDF file creation.

Also noted: skill files are stored in "tenant-scoped SharePoint Embedded containers", sensitivity labels are retained and honored, and — a live preview bug — "Agents that have both skills and embedded files aren't supported yet."

## Verified in a live tenant — 2026-09-20

Everything above this point is documentation. This section is **observation**, from uploading real bundles to a real agent on the GitHub Copilot harness, and it outranks the documented claims where they differ.

### Packaging

- **`SKILL.md` must be at the archive root.** A bundle with the files wrapped in a `skill-name/` folder is rejected with: *"Upload failed. Bundle is missing a root-level SKILL.md file."* The flat shape documented above is correct; the spec's "name must match the parent directory name" rule does **not** mean the zip carries that directory.
- **Watch the path separators.** PowerShell's `Compress-Archive` writes entry paths as `references\file.md` with backslashes. The ZIP format requires forward slashes. Build bundles with `System.IO.Compression.ZipFile` and explicit forward-slash entry names, or the package can be refused with no useful error.

### Runtime capabilities

Three distinct capabilities, all confirmed:

| Capability | Result |
|---|---|
| A root-level `.zip` installs and appears in the components panel | works |
| Files in `references/` are readable at runtime | works — the agent quoted a playbook it was pointed at |
| Files in `scripts/` **execute** and return output | works — exit code 0 |

The third is the significant one. Microsoft documents skill script execution only for declarative agents; no Learn page states it works on this harness. It does.

### The sandbox

```
python:   3.12.14 (main, Aug 18 2026, 15:00:50) [GCC 13.2.0]
platform: Linux-6.12.8+-x86_64-with-glibc2.38
```

Package availability, probed by import:

| Status | Packages |
|---|---|
| **Available** | `openpyxl`, `xlsxwriter`, `docx` (python-docx), `pptx` (python-pptx), `reportlab`, `pypdf`, `PIL` (Pillow), `pandas`, `numpy`, `matplotlib`, `requests`, `bs4`, `lxml`, `yaml`, `jinja2` |
| **Missing** | `fpdf` |

Fifteen of sixteen probed packages are present. This replaces the earlier guidance to treat every import as a gamble — for these names, availability is a measured fact.

> **`requests` imports but cannot be used.** Microsoft states the sandbox has no network access at runtime, so an HTTP call will fail regardless of the import succeeding. **Availability is not usability.** The same caution applies to anything in `bs4` or `lxml` that fetches rather than parses.

Two caveats on the list itself: it reflects one tenant at one moment, and Microsoft still publishes no package guarantee. Re-run [`diagnostics/script-probe/`](../../diagnostics/script-probe) to check another tenant or a later date.

### What this overturned

The findings above originally concluded that "no bundled script should be load-bearing", reasoning from the absence of a published package list. That was the right call on the evidence then and is **wrong now**: scripts execute, and the packages that matter for document generation are present. See [What does copilot-skill-creator say about bundling scripts and resources?](https://github.com/matheus-sancha/copilot-studio-skills/issues/14).

## Billing

Every page in the GitHub Copilot harness documentation set repeats the same notice: "Usage-based billing applies to using, building, testing, and evaluating agents. These actions might consume Copilot Credits" ([skills-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview)). Uploading this repo's six skills and running an interview through them costs credits, and the README should not pretend otherwise.

## Implications for the map

- **Ship `.zip` bundles, not loose files** — it is the only packaging that carries `references/` and `assets/`. Feeds [issue #9](https://github.com/matheus-sancha/copilot-studio-skills/issues/9).
- **Skill folder name must equal the `name` in frontmatter**, lowercase-hyphen, ≤64 chars. All six planned names already comply.
- **Write `description` as one line**, well under 1024 characters, since Copilot Studio enforces an undocumented shorter cap.
- **Save every `SKILL.md` as UTF-8 without BOM** — a real hazard authoring on Windows, where PowerShell's `Out-File`/`>` default to UTF-8 *with* BOM.
- **Budget against total context, not a per-field cap.** Keep each `SKILL.md` under 500 lines and push detail into `references/`, so progressive disclosure keeps the resting footprint at roughly 100 tokens per installed skill. This matters most for the router in [issue #10](https://github.com/matheus-sancha/copilot-studio-skills/issues/10), which is loaded for the whole session.
- **The document-output playbooks in [issue #6](https://github.com/matheus-sancha/copilot-studio-skills/issues/6) should instruct, not script.** The harness creates Office and PDF files natively and surfaces a download card by itself; the playbook's job is to specify structure and content, not to ship Python. Keep each generated file under 10 MB.
- **The README must state the prerequisite plainly**: these skills require an agent on the GitHub Copilot harness, and do not work on the standard or Copilot chat harnesses.
- **Warn against the download round-trip** — pulling a skill back out of Copilot Studio returns Markdown only and loses bundled resources. The repo is the source of truth.
