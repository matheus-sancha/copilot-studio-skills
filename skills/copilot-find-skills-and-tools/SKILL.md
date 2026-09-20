---
name: copilot-find-skills-and-tools
description: Works out which connectors, MCP servers, workflows and pre-built skills a Copilot Studio agent needs, and writes a tool-plan.md saying where to find each and why. Use when the user asks what tools or connectors their agent needs, how to connect it to another system, or what is already available.
license: MIT
---

# Find skills and tools

Turn the agent's brief into a plan for what to attach to it.

## What exists

Copilot Studio offers exactly three tool types, plus a catalog of pre-built skills.

| Type | Best for |
|---|---|
| **Connectors** | Integrating with well-known services that have pre-built connectors |
| **MCP servers** | Custom or internal services using the MCP standard |
| **Workflows** | Multi-step, automated, deterministic processes |

Connectors "expose actions from hundreds of external services" - Microsoft names SharePoint, Outlook, Salesforce, ServiceNow and SAP as examples. **The full list is not published anywhere**, and availability varies by tenant and licence.

So never assert that a specific connector exists unless Microsoft named it. Name the *type* and the *search*, and let the user confirm what their tenant actually has. A confidently wrong connector name costs more than an honest "search for it here".

## Start

Read the agent brief - earlier in this conversation, or a re-supplied `agent-brief.md`.

**No brief?** Ask what systems the agent must read from or write to, and what it must do that it cannot do by talking. That is enough.

## Find the needs

Work from **inputs** and **tasks**, not from a wish list. Every need is something the agent cannot do with instructions and knowledge alone:

- It must **read live data** from somewhere → a tool.
- It must **write or create** something in another system → a tool.
- It must run a **fixed multi-step process** with approvals or branching → a workflow.
- It must produce a document, follow a procedure, or apply bundled reference material → **not a tool.** That is a skill. Say so, and point at `copilot-skill-creator`.

That last line matters. Users reach for connectors when what they need is instructions, and every unnecessary tool costs context on every turn and makes the orchestrator's job harder.

## Pick the type

For each need, in order:

1. Is it a **well-known external service**? → Connector. Search the gallery by the product's name.
2. Is it an **internal or custom service** that speaks MCP, or could? → MCP server.
3. Is it a **deterministic multi-step process** inside Power Platform? → Workflow.
4. Does a **pre-built skill** already cover it? Check the skill catalog before building anything - Build tab, **Skills**, **Add skill**, and browse.

If two types would work, prefer the one already in the user's tenant. A working connector beats a better-architected MCP server nobody has stood up.

## Write the plan

Produce `tool-plan.md` as a file the user can download, one block per need:

```markdown
## Look up customer records

**Type:** Connector
**Where:** Build tab > Tools > Add a tool > Connectors, search for your CRM
**Why:** A known SaaS product with a pre-built connector, so no code.
**Check:** Confirm it appears in your tenant and is not premium-licensed.
**Then:** Review the tool's description after adding it.
```

Every block carries all five lines. **Check** is not optional - it is what keeps a recommendation honest when the catalogue cannot be verified from here.

Order the blocks by what blocks the agent most: without this tool, does it fail entirely, or just do less?

## Two things that decide whether tools work

Put both in the plan, once:

> **Tool descriptions drive invocation.** After adding a tool, read its description.
> The orchestrator uses the name and description to decide when to call it, so
> vague or overlapping descriptions mean the wrong tool fires, or none does.
> Rename "Ticket tool" to "Create support ticket".

> **Keep the count small.** Every attached tool costs context on every turn, and
> MCP servers also cap how many can run concurrently in one conversation. Remove
> tools the agent does not use.

## Hand off

> Save `tool-plan.md`. You work through it in **Build** > **Tools** at the end
> of the build, not now - adding a tool does not reach a conversation that is
> already running, and nothing left to do here needs the tools live. Some of
> them will want you to sign in or pick which actions to expose; do that as you
> add each one.
>
> Anything in the plan marked as a skill rather than a tool goes to
> `copilot-skill-creator` instead.
>
> Next: `copilot-skill-creator` if the plan names any skills, then back to
> `copilot-instructions-creator` to revise the instructions against what you
> planned. Tool use is exactly the kind of thing that works in a demo and fails
> on the tenth try, so `copilot-evaluation-creator` matters here.

> Running in an IDE with file access? Write `tool-plan.md` into the agent folder
> instead of handing it over for download.
