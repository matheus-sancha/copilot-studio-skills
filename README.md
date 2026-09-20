# copilot-studio-skills

Six Agent Skills that help you design and build a Microsoft Copilot Studio agent. You upload them to the agent you are building, work through them, and delete them before you publish.

They are development scaffolding, not part of the finished agent.

## Requirements

An agent created with the **GitHub Copilot harness**. Skills are not supported on the standard harness or the Copilot chat harness.

Building, testing and evaluating agents on this harness consumes Copilot Credits.

## Download

| Skill | What it does | Download |
|---|---|---|
| `copilot-studio-agent-creator` | Routes you through the build, one stage at a time | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-studio-agent-creator.zip) |
| `copilot-agent-review` | Interviews you until the agent's design is pinned down, then writes `agent-brief.md` | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-agent-review.zip) |
| `copilot-instructions-creator` | Writes the agent's Instructions as XML-tagged sections | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-instructions-creator.zip) |
| `copilot-find-skills-and-tools` | Works out which connectors, MCP servers and workflows the agent needs | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-find-skills-and-tools.zip) |
| `copilot-skill-creator` | Builds a custom skill for the agent, including document-output playbooks | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-skill-creator.zip) |
| `copilot-evaluation-creator` | Builds an evaluation set as a CSV for the Evaluate tab | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/copilot-evaluation-creator.zip) |

All releases: [Releases](https://github.com/matheus-sancha/copilot-studio-skills/releases).

### Diagnostic

| Bundle | What it does | Download |
|---|---|---|
| `script-probe` | Reports whether bundled Python scripts execute in your tenant, and which packages are importable | [zip](https://github.com/matheus-sancha/copilot-studio-skills/releases/download/v0.1.0/script-probe.zip) |

Not one of the six. Upload it, say **"run the probe"**, then delete it.

It ships `scripts/probe.py` plus a marker file in `references/`, so the result is unambiguous: if the agent quotes the marker **and** returns the script output, bundled scripts execute. If it quotes the marker but produces no script output, files install and are readable but scripts do not run.

Source: [`diagnostics/script-probe/`](diagnostics/script-probe).

## Install

1. Open your agent in Copilot Studio.
2. **Build** tab > **Skills** > **Add skill** > **Upload a skill**.
3. Drop in the `.zip`.

Start with `copilot-studio-agent-creator` and let it tell you what to load next.

Keep only the router plus the one skill you are using, and remove each skill when its stage is done. An agent holds at most 8 skills, and every loaded skill competes for the same context as your conversation.

Keep the whole build in **one conversation** — each skill reads what the earlier ones established.

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

Pre-release. The skills are written and validated against Microsoft's published format, but not yet confirmed end to end in a live tenant — see [issue #12](https://github.com/matheus-sancha/copilot-studio-skills/issues/12).

## License

MIT — see [LICENSE](LICENSE).
