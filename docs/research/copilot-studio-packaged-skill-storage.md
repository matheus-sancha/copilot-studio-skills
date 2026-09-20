# How Copilot Studio stores an uploaded skill `.zip`

Research for the stub-`SKILL.md` failure seen in the `Document Translator` agent, 2026-09-20.
Sources: Microsoft Learn, Microsoft's own Copilot Studio VS Code extension source, and a
Microsoft-published sample solution export.

## Answer in brief

`<!-- bic:bundle=... -->` is **not an error and not a truncation**. It is the storage shape of every
skill uploaded as a `.zip`. A packaged skill is stored as several Dataverse components:

| Component | Holds |
|---|---|
| `<bot>.skill.<name>_<sfx>` — `kind: InlineAgentSkill` | `content: <!-- bic:bundle=<zip schema name> -->` — a pointer, never the body |
| `<bot>.file.skillmd_<sfx>` — `FileAttachmentComponent`, display name `./SKILL.md` | the real `SKILL.md`, full body |
| `<bot>.file.<path>_<sfx>` — one per bundled file | `references/...`, `scripts/...` |

A skill uploaded as a **bare `.md`** is stored differently: the body goes straight into the skill
component's `content`, tagged `<!-- bic:source=upload -->`.

So "zip skills show a stub, `.md` skills show a body" is the expected difference between the two
storage shapes — it is **not**, on its own, evidence that the upload lost the instructions.

## The evidence

### The marker is minted by Microsoft's own code

[`SkillLayout.cs`](https://github.com/microsoft/vscode-copilotstudio/blob/main/src/CopilotStudio.McsCore/SkillLayout.cs)
in `microsoft/vscode-copilotstudio`:

```csharp
internal const string BundleMarkerPrefix = "<!-- bic:bundle=";
internal const string BundleMarkerSuffix = " -->";

internal static string BuildBundleMarker(string bundleSchemaName)
    => $"{BundleMarkerPrefix}{bundleSchemaName}{BundleMarkerSuffix}";

internal static string MintBundleSchemaName(string folderName, string botName)
{
    var stem = new string(folderName.Where(c => c <= 127 && char.IsLetterOrDigit(c)).ToArray());
    stem = stem.Length == 0 ? "skill" : stem;
    return $"{botName}{LspProjection.FileAttachmentInfix}{stem}{hash8}zip";
}
```

`MintBundleSchemaName` reproduces the observed string exactly. For `copilot-find-skills-and-tools`
on an agent whose bot schema name is `cr7a0_documenttranslator_CjvKwI`:

```
cr7a0_documenttranslator_CjvKwI . file . copilotfindskillsandtools zip _akRmb
└──────── bot schema name ─────┘ └──────┘ └──── hyphens stripped ───┘
                        FileAttachmentInfix
```

The hyphens vanish because `MintBundleSchemaName` keeps only ASCII letters and digits. This is a
**minted name**, not a filename the platform failed to read.

### The projection deliberately shadows `SKILL.md` with the marker

Same file, `ResolveContent`:

```csharp
var bundle = ReadAnchorMetadata(fileAccessor, folderName).Bundle ?? TryGetBundleFromMarker(currentContent);
if (bundle != null)
{
    return BuildBundleMarker(bundle);
}
return manifestIsComponent ? currentContent : ReadManifestText(fileAccessor, folderName) ?? currentContent;
```

When a bundle exists, the content resolved for the skill is **always** the marker — the real manifest
text is never substituted in. `SkillBodyProjection.TryGetManifestWrite` makes the same cut from the
other direction: it refuses to write a `SKILL.md` for any skill whose content carries a bundle marker.

### A healthy packaged skill, from Microsoft's own sample

[`new-copilot-studio-tech-guide`](https://github.com/microsoft/new-copilot-studio-tech-guide) ships an
exported solution with both shapes side by side.

Packaged (`.zip`) — `botcomponents/...skill.slip-pdf-generator_2i4/data`:

```yaml
kind: InlineAgentSkill
content: <!-- bic:bundle=crskill_slip_pdf_generator_zip_0282983e69e6 -->
```

Bare `.md` — `botcomponents/Default_draft_IsBewO.skill.card-reissue/data`:

```yaml
kind: InlineAgentSkill
content: |
  ---
  name: card-reissue
  description: Replace (reissue) a member's BlastPass card when it is lost, stolen, or damaged. ...
  ---
  <!-- bic:source=upload -->
  # BlastPass Card Reissue
  ...
```

And the packaged skill's body is present in the same solution as its own component —
`botcomponents/cra24a45_skill_md_30aa9a7b2b7c/filedata/SKILL.md` opens with full, real frontmatter and
a full body. `PackagedSkillKnowledgeFileTests.cs` models exactly this fan-out: one `InlineAgentSkill`
plus `./SKILL.md` plus `./scripts/Get-UsWeather.ps1`, all parented to the skill.

These sample skills run bundled Python. **Packaged skills work.**

### A healthy packaged skill keeps its real description

[`PackagedSkillWorkspace/behaviors/get-us-weather.mcs.yml`](https://github.com/microsoft/vscode-copilotstudio/blob/main/src/LanguageServers/PowerPlatformLS/UnitTests/PowerPlatformLS.UnitTests/TestData/Workspace/PackagedSkillWorkspace/behaviors/get-us-weather.mcs.yml):

```yaml
mcs.metadata:
  componentName: get-us-weather
  description: Get the current weather.
kind: InlineAgentSkill
content: <!-- bic:bundle=crf9a_nagentn1_T2U1EY.file.getusweatherzip_hq06y -->
```

The marker sits next to a **real description parsed out of the zip's `SKILL.md` frontmatter**.

## The one genuine anomaly

In the failing agent the description is the **skill name repeated**:

```yaml
name: copilot-find-skills-and-tools
description: copilot-find-skills-and-tools
```

Microsoft's healthy packaged skill carries a real description in the same slot. The description is the
only thing the orchestrator sees at rest — it is what decides whether a skill activates at all
([skills-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview):
"The orchestration runtime decides when to activate a skill based on the user's message and the skill's
description"). A name-shaped description is a description that will rarely match anything.

So the question is not "where did the body go" — it is **"was the frontmatter parsed at install"**.

## What documentation does and does not settle

Documented ([skills-add-existing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing)):

> A ZIP file that must include a `SKILL.md` file, with the skill name and description formatted in YAML
> front matter and instructions in Markdown. The package can optionally include supporting files, such
> as scripts, templates, and reference documents.

> The system validates the file and adds the skill to your agent.

Documented ([skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)) —
the load-time failure table, of which three rows are live candidates here:

| Reason | Fix |
|---|---|
| Description too long | "Shorten the description to a single line that summarizes the skill's purpose." |
| Resource file wasn't written | "Re-export the skill package, verify each file is present and readable, then upload again." |
| Skill package rejected | "Re-export the package from a working editor and try again." |

Also documented there, and the closest match to the symptom:

> Skills whose supporting files were partially written still load, but the agent might behave
> differently at runtime because some of the referenced content is missing. Re-upload the package to
> restore the full set of files.

**Not settled by any source:** whether the model, at runtime, receives the packaged skill's real
`SKILL.md` body or the marker. No Learn page states it, and the VS Code projection — an *authoring*
surface, not the runtime — resolves it to the marker either way.

## The three checks that settle it

None of these can be answered by reading. All are cheap.

1. **The components panel.** Open a stubbed skill in Build → Skills. If the Description field shows the
   real one-line description from the repo, the frontmatter parsed and only the file view is a
   projection. If it shows the skill name, the install did not read the frontmatter.
2. **Download it.** `...` → **Download** returns "a Markdown file containing the skill name and
   description in YAML front matter, plus instructions". Full body back means the platform holds it; a
   157-byte stub back means it does not.
3. **Make it fire.** Ask for something only the body could answer, and check the behaviour against an
   instruction that exists nowhere but inside `SKILL.md`. This is the only check that tests the runtime
   rather than the store.

## Bearing on the repo

- The released `.zip` bundles are **not** implicated by this evidence. All seven were re-verified on
  2026-09-20: `SKILL.md` at archive root, full byte counts, `references/` and `scripts/` intact.
  `copilot-studio-agent-creator/SKILL.md` is 5,204 bytes in the repo and 5,204 in the bundle.
- The failure is **not deterministic by skill**. Across two observations of the same seven bundles a
  different subset stubbed each time — three of them both times. Whatever the cause, it is not bundle
  content.
- Until check 1 or 2 comes back, the README's "Verified in a live tenant: the bundles install" is
  unsupported for the packaged path and should not be relied on.

## Verified in a live tenant — 2026-09-20

The three checks were run on the `Document Translator` agent. All seven skills had been uploaded as
`.zip` from the release page. Results, and what each one closes:

| Check | Result | Closes |
|---|---|---|
| Description field in the components panel | "All of them read as a sentence" | the frontmatter **is** parsed at install |
| `...` > Download, `script-probe` | **1,514 bytes** — byte-identical to `script-probe.zip` | the platform stores the **whole archive** |
| `...` > Download, `copilot-skill-creator` | ~16.8 KB — within rounding of the 16,934-byte bundle, nowhere near the 9,792-byte `SKILL.md` | same |
| `script-probe` fired in Preview | reported okay, both fingerprints returned | the runtime receives the real body **and** the bundled files |

Two things follow, and they overturn the reasoning that opened this document.

**The `.zip` path works end to end.** A `1,514`-byte download cannot come from a bare `SKILL.md` upload —
the file is 1,117 bytes. `script-probe` was still installed as a bundle when it fired, executed its
bundled script, and read its bundled reference file. There is no packaging defect, and nothing in the
released bundles needs to change.

**Download does not behave as documented.** [skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)
says the download returns "a Markdown file containing the skill name and description in YAML front
matter, plus instructions". For a packaged skill it returns the original `.zip` instead. That is better
than documented — the round-trip does **not** lose bundled resources the way the earlier
[skill contract note](copilot-studio-skill-contract.md) warned — but the documentation is wrong, and
anything built on the documented behaviour is built on sand.

### The real failure mode

> "After the first error the agent asked me to re-upload them as `SKILL.md` files, which still worked
> only when I started a new chat session."

**A skill added to an agent does not reach a conversation already in progress.** The skill set appears
to be bound when the conversation starts. Re-uploading was never what fixed it; starting a new chat
was. The same fix would have worked without re-uploading anything.

This explains every symptom in the original report:

- The agent read its own `SKILL.md` and found a `bic:bundle` marker — the normal storage projection,
  as established above — and concluded the package was broken.
- It proposed re-uploading the three skills as unzipped folders. That would have appeared to work,
  because the re-upload is followed by a new conversation, and the new conversation is the actual fix.
- The failing subset changed between observations without the bundles changing, because what varied was
  which uploads predated the open conversation.

### The contradiction this exposes

The README tells users to **keep the whole build in one conversation**, because each stage reads what
the earlier ones established. The route's stage 4 hands the user a generated `SKILL.md` to upload. Those
two cannot both hold: uploading the skill requires a new conversation, and a new conversation loses the
design. This is a route defect, not a packaging defect, and it is the thing actually worth fixing.

### Instructions bind the other way — 2026-09-20

Tested after the route change, because four shipped files were hedging on it.

**Method.** A live conversation was opened and answered. With that conversation still open, this line was appended to the agent's Instructions and saved:

```
Always end every single reply with this exact token on its own line: INSTR-BOUND-9312
```

| Conversation | Token in the reply? |
|---|---|
| the one already running | **yes** |
| a new one | yes |

**Saved Instructions take effect immediately, including in a conversation already in progress.** Skills are the exception, not the rule: they are bound when the conversation starts, instructions are not.

This does not weaken the case for deferring everything to stage 7 — it strengthens it, and changes the reason. A skill applied mid-build does nothing, which wastes a step. Instructions applied mid-build do something worse: they rewrite the agent you are using to run the build, halfway through it.

**Tools were not tested.** The check needs a tool the tenant can add and a visible activity trace, and it was not worth the configuration change for something nothing depends on. Whether an added tool reaches a running conversation remains unknown, and the shipped files say so rather than guessing.

### A caution on the description

The name-shaped `description: copilot-find-skills-and-tools` reported at the top of this document was
never in the store. The components panel shows real descriptions for every skill. It exists only in the
stub the agent read, so it is an artifact of the projection — not evidence of a failed install.
