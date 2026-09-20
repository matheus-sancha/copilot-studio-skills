# copilot-studio-skills

Six Agent Skills that help you design and build a Microsoft Copilot Studio agent. You upload them to the agent you are building, work through them, and delete them before you publish.

They are development scaffolding, not part of the finished agent.

## Requirements

An agent created with the **GitHub Copilot harness**. Skills are not supported on the standard harness or the Copilot chat harness.

Building, testing and evaluating agents on this harness consumes Copilot Credits.

## Download

| Skill | What it does | |
|---|---|---|
| `copilot-studio-agent-creator` | Routes you through the build, one stage at a time | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-studio-agent-creator.md) |
| `copilot-agent-review` | Interviews you until the agent's design is pinned down, then writes `agent-brief.md` | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-agent-review.md) |
| `copilot-instructions-creator` | Writes the agent's Instructions as XML-tagged sections | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-instructions-creator.md) |
| `copilot-find-skills-and-tools` | Works out which connectors, MCP servers and workflows the agent needs | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-find-skills-and-tools.md) |
| `copilot-skill-creator` | Builds a custom skill for the agent, including document-output playbooks | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-skill-creator.zip) |
| `copilot-evaluation-creator` | Builds an evaluation set as a CSV for the Evaluate tab | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-evaluation-creator.md) |

All releases: [Releases](https://github.com/matheus-sancha/copilot-studio-skills/releases).

## Install

1. Open your agent in Copilot Studio.
2. **Build** tab > **Skills** > **Add skill** > **Upload a skill**.
3. Drop in the file. Repeat for all six.

Five of them are a single `.md`. `copilot-skill-creator` is a `.zip`, because it carries reference files and scripts and only the `.zip` format brings those along. Copilot Studio accepts both.

An agent holds **8 skills** in total, and these six take six of them. Leave all six loaded for the whole build — nothing else is installed until the end, so the slots are never contested. The last stage deletes them and installs what you built.

**A skill you upload does not reach a conversation that is already running.** Start a new chat after installing these six, and after installing anything else later. This is the single most useful thing to know about the product: a skill that is installed but not yet active looks exactly like one that failed to install.

## How to use them

Skills activate on what you ask for, not on their filename. You describe what you want and the orchestrator picks the skill whose description matches.

**Start in the Preview tab** and say:

> Help me build this agent. Where do I start?

`copilot-studio-agent-creator` answers, asks what you already have, and names the skill to use first. From then on, follow what it tells you.

**Keep the whole build in one conversation.** Each skill reads what the earlier ones established, so a new chat loses the design.

**Change nothing in the agent until the end.** Stages 1 to 6 are design work — each hands you a file to save. You apply them all at stage 7, in one pass. This is not tidiness, and the two components fail in opposite directions: a skill you upload does not reach the conversation you are in *at all*, while instructions land *immediately* and rewrite the agent you are building with, halfway through. Nothing in the route needs an applied component, so deferring costs you nothing.

**To reach a specific skill,** ask for the thing it does — "interview me about this agent", "write the instructions", "build me an evaluation set". Naming the skill outright works too if it does not fire on the description alone.

### What comes back, and where it goes

Each stage hands you a file. **Save them all and apply nothing until stage 7**, which walks you through it in this order:

| File | Where it goes, at stage 7 |
|---|---|
| `agent-brief.md` | Nowhere. Keep it. It is the design record, and how you recover if the conversation is lost. Do **not** paste it into Instructions. |
| A generated `SKILL.md` | **Build** > **Skills**, the same way you installed these — but delete the six `copilot-*` skills first, or the slots are not free. |
| `tool-plan.md` | Work through it in **Build** > **Tools**, adding what it lists. |
| `instructions.md` | Paste the whole file into **Build** > **Instructions**, then **Save**. |
| `evaluation-set.csv` | **Evaluate** tab > **New evaluation**, drag it onto the **Data source** area. |

Then **start a new chat** before you test. Nothing you just installed is live in a conversation that was already open.

### If a skill does not respond as expected

- **Nothing happens** — first, are you in the same conversation you uploaded it from? Installed skills do not reach a running conversation. Start a new chat. If it still does nothing, check it appears in the components panel: a skill that fails validation is skipped silently.
- **The agent says its own `SKILL.md` is empty** — it is not. A skill installed from a `.zip` is stored as a `<!-- bic:bundle=… -->` pointer, so an agent reading its own file finds a marker and concludes the package is broken. Ignore the diagnosis and start a new chat.
- **The wrong skill answers** — say the skill's name directly.
- **It asks for something you already gave it** — you are probably in a new conversation. Re-upload `agent-brief.md` and say which stages you finished.

## Remove

Select the **X** next to the skill in the components panel, then confirm.

Delete every `copilot-*` skill before you publish the agent.

## The route

1. `copilot-agent-review` — produces `agent-brief.md`
2. `copilot-instructions-creator` *(draft)* — drafts the instructions in the conversation; no file yet
3. `copilot-find-skills-and-tools` — produces `tool-plan.md`
4. `copilot-skill-creator` — one skill per capability
5. `copilot-instructions-creator` *(revise)* — produces `instructions.md`
6. `copilot-evaluation-creator` — produces `evaluation-set.csv`
7. **Apply it all** — the only stage that changes the agent

Instructions are written twice on purpose. They name the agent's tools, skills and connected agents, so they cannot be finished before those exist.

Stages 3 and 4 are skippable when the agent needs no tools and no custom skills.

## Diagnostics

`script-probe` is not part of the route. It is a throwaway skill for checking how a tenant behaves: whether bundled scripts execute, whether bundled reference files are readable, and which Python packages the sandbox has. Upload it when you are investigating something, read what it reports, then delete it.

| Skill | What it does | |
|---|---|---|
| `script-probe` | Runs a bundled script and reads a bundled reference file, then reports what worked | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/script-probe.zip) |

## Repository

```
skills/       one folder per skill; SKILL.md plus any references
diagnostics/  throwaway probes for checking tenant behaviour
docs/         research notes behind the design decisions
scripts/      builds the release assets from source
```

Releases carry the uploadable assets, built by `scripts/build-release.ps1`: a bare `.md` for a skill that is a single `SKILL.md`, a `.zip` for one that bundles anything. The repository itself stays source-only.

The script is where the packaging traps live. It refuses a skill whose frontmatter `name` does not match its folder, writes zip entries with forward slashes — `Compress-Archive` writes backslashes, which the format forbids and Copilot Studio can reject with no useful error — and `-Verify` checks every archive has `SKILL.md` at its root and no file carries a UTF-8 BOM.

## Status

Checked on 2026-09-20, on a live agent built with the GitHub Copilot harness. Each row says how, so you can judge it or repeat it.

| Claim | How it was checked |
|---|---|
| A `.zip` with `SKILL.md` at its root installs | uploaded; a bundle wrapped in a folder is rejected with *"Bundle is missing a root-level SKILL.md file"* |
| A bare `SKILL.md` installs | uploaded; stored inline rather than behind a bundle pointer |
| Bundled `references/` are readable at runtime | the agent quoted a marker string that exists nowhere but inside the bundle |
| Bundled `scripts/` execute | `script-probe` ran its bundled script and returned its output |
| Six skills install into one agent together | all six installed, all six listed in the components panel |
| An installed skill does not reach a conversation already running | a skill that looked inert became active in a new chat, unchanged |
| A packaged skill's instructions survive upload | the skill downloaded back byte-identical to the uploaded `.zip` |
| Saved Instructions *do* reach a conversation already running | a fingerprint token added mid-conversation appeared in the very next reply |

**Not checked, and stated here rather than implied:**

- **That each of the six activates on a plain-language request.** Several were, not all six individually. A skill activates on its `description`, so this is the claim most worth testing in your own tenant.
- **Whether an added tool reaches a conversation already running.** Instructions were tested and do; skills were tested and do not. Tools were not. The route defers them regardless, so nothing here depends on it.
- **The 8-skill ceiling.** Microsoft publishes that figure for Agent Builder, a different surface. No Copilot Studio page states a limit for this harness, and it has not been tested here.

Microsoft's documentation is wrong in one place that matters: downloading a packaged skill returns the original `.zip`, not the Markdown file [the docs describe](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage). Better than documented — the round-trip keeps bundled files — but do not build on the documented behaviour.

The sandbox and format facts behind these skills are recorded in [`docs/research/`](docs/research), marked according to whether they came from Microsoft's documentation or from direct observation.

## License

MIT — see [LICENSE](LICENSE).
