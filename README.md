# copilot-studio-skills

Six Agent Skills that help you design and build a Microsoft Copilot Studio agent. You upload them to the agent you are building, work through them, and delete them before you publish.

They are development scaffolding, not part of the finished agent.

## Requirements

An agent created with the **GitHub Copilot harness**. Skills are not supported on the standard harness or the Copilot chat harness.

Building, testing and evaluating agents on this harness consumes Copilot Credits.

## Download

| Skill | What it does | |
|---|---|---|
| `copilot-studio-agent-creator` | Routes you through the build, one stage at a time | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-studio-agent-creator.zip) |
| `copilot-agent-review` | Interviews you until the agent's design is pinned down, then writes `agent-brief.md` | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-agent-review.zip) |
| `copilot-instructions-creator` | Writes the agent's Instructions as XML-tagged sections | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-instructions-creator.zip) |
| `copilot-find-skills-and-tools` | Works out which connectors, MCP servers and workflows the agent needs | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-find-skills-and-tools.zip) |
| `copilot-skill-creator` | Builds a custom skill for the agent, including document-output playbooks | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-skill-creator.zip) |
| `copilot-evaluation-creator` | Builds an evaluation set as a CSV for the Evaluate tab | [Download](https://github.com/matheus-sancha/copilot-studio-skills/releases/latest/download/copilot-evaluation-creator.zip) |

All releases: [Releases](https://github.com/matheus-sancha/copilot-studio-skills/releases).

## Install

1. Open your agent in Copilot Studio.
2. **Build** tab > **Skills** > **Add skill** > **Upload a skill**.
3. Drop in the `.zip`. Repeat for all six.

An agent holds **8 skills** in total. These six take six of them, so before you start building skills for the agent itself, remove the `copilot-*` skills you have finished with. The router tells you when.

## How to use them

Skills activate on what you ask for, not on their filename. You describe what you want and the orchestrator picks the skill whose description matches.

**Start in the Preview tab** and say:

> Help me build this agent. Where do I start?

`copilot-studio-agent-creator` answers, asks what you already have, and names the skill to use first. From then on, follow what it tells you.

**Keep the whole build in one conversation.** Each skill reads what the earlier ones established, so a new chat loses the design.

**To reach a specific skill,** ask for the thing it does — "interview me about this agent", "write the instructions", "build me an evaluation set". Naming the skill outright works too if it does not fire on the description alone.

### What comes back, and where it goes

Each stage hands you a file. None of them install themselves.

| File | Where it goes |
|---|---|
| `agent-brief.md` | Keep it. It is the design record, and how you recover if the conversation is lost. Do **not** paste it into Instructions. |
| `tool-plan.md` | Work through it in **Build** > **Tools**, adding what it lists. |
| A generated `SKILL.md` | Upload it in **Build** > **Skills**, the same way you installed these. |
| `instructions.md` | Paste the whole file into **Build** > **Instructions**, then **Save**. |
| `evaluation-set.csv` | **Evaluate** tab > **New evaluation**, drag it onto the **Data source** area. |

### If a skill does not respond as expected

- **Nothing happens** — the skill may not have loaded. A skill that fails validation is skipped silently; check it appears in the components panel.
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

Instructions are written twice on purpose. They name the agent's tools, skills and connected agents, so they cannot be finished before those exist.

Stages 3 and 4 are skippable when the agent needs no tools and no custom skills.

## Repository

```
skills/       one folder per skill; SKILL.md plus any references
diagnostics/  throwaway probes for checking tenant behaviour
docs/         research notes behind the design decisions
```

Releases carry the uploadable `.zip` bundles. The repository itself stays source-only.

## Status

Verified in a live tenant: the bundles install, bundled reference files are readable, bundled scripts execute, all six skills load together, and each one activates correctly.

The sandbox and format facts behind these skills are recorded in [`docs/research/`](docs/research), marked according to whether they came from Microsoft's documentation or from direct observation.

## License

MIT — see [LICENSE](LICENSE).
