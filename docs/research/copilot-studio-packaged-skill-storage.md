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
