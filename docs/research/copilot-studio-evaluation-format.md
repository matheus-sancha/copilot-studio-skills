# The Copilot Studio evaluation format

Research for [issue #3](https://github.com/matheus-sancha/copilot-studio-skills/issues/3). Verified 2026-09-20 against Microsoft Learn.

## Answer in brief

Evaluation lives on the **Evaluate** tab. An **evaluation** is a named test set; a **conversation** is one test case. Conversations are written by hand, generated with AI, or **uploaded as a CSV** ([analytics-agent-evaluation-intro](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro)).

One finding overrides everything else about how `copilot-evaluation-creator` should be designed:

> **The General quality test method doesn't compare responses to expected answers.**
> — [analytics-agent-evaluation-intro](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro)

And General quality is the *only* method on this harness: "Currently, the only available test method is **General quality**, an AI-based assessment of whether responses meet quality standards, such as relevance and completeness."

So on the GitHub Copilot harness, an expected answer is a field you may fill but nothing currently scores against it. **The test question is the entire lever.** A skill that pours effort into crafting precise expected outputs is optimising something the platform ignores; a skill that crafts probing *questions* is optimising the only input that reaches the grader.

> **Note the two documentation sets.** `/agents-experience/analytics-agent-evaluation-*` covers the GitHub Copilot harness — this repo's target. `/analytics-agent-evaluation-*` without that segment covers the **standard harness**, and carries richer capability that does **not** apply here. Quoting the wrong one is the main hazard in this area.

## What the feature offers on this harness

| Concept | Meaning |
|---|---|
| Evaluation | "a named test set that combines conversations with a test method" |
| Conversation | "a test case that represents a scenario you want your agent to handle. Each conversation includes user messages and optionally expected agent responses" |
| Test method | Scores the responses. **General quality** only |
| User profile | "the authenticated profile that runs the evaluation" — set it so tools and connections are actually exercised |

Status: "This is a production-ready preview feature."

## Creating a test set

Three routes ([analytics-agent-evaluation-create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-create)):

**1. Upload a CSV.** Evaluate tab → **New evaluation** → **Data source** → drag the file on, or browse.

> "Select the **CSV** link to download a template that shows the correct file format. The maximum file size is 5 MB."

**2. Generate with AI.** **Quick conversation set** produces 10 conversations "based on the agent's description, instructions, and topics". After a first run, **Add conversations** offers **Generate 25 conversations** or **Generate 50 conversations**.

**3. Write manually.** **Add conversations** → **Write**. "Add a user question for each conversation. Optionally, add an expected agent response."

Then the **Configure test set** panel takes a required **Name**, the **Test method**, and the **User profile**, and **Evaluate** runs it or **Save** stores it.

## The CSV columns — unverified

**Microsoft does not document the column headers for the GitHub Copilot harness CSV.** The page says only to download the template.

The **standard harness** import format is fully specified, and is the obvious candidate for what the template contains ([analytics-agent-evaluation-create, standard harness](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create)):

> Add the following headings, in this order, in the first row:
> - Question
> - Expected response

with, on that harness: "The file can contain up to 100 questions", "Each question can be up to 1,000 characters, including spaces", and "The file must be in comma separated values (CSV) or text format."

**Do not assume those carry over.** The harnesses differ elsewhere in this exact area, and the GitHub Copilot harness page states a 5 MB file limit while saying nothing about 100 questions or 1,000 characters. Downloading the template and reading its header row is a one-minute job in a live tenant and is folded into [issue #12](https://github.com/matheus-sancha/copilot-studio-skills/issues/12).

Until then, `copilot-evaluation-creator` must tell the user to download the template and match its headers rather than emitting headers from memory.

## Scoring

Per test case, General quality returns **Pass** or **Fail** — "**General quality**: How the responses scored on the test method, either **Pass** or **Fail**." The evaluation summary reports a **Score** ("The overall score of conversations that passed the general quality test method"), plus **Duration**, **Test cases**, **Data type** and **User profile** ([analytics-agent-evaluation-view](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-view)).

"**Data type**: The type of test set. Only the Conversation data type is available."

Scoring is automatic and model-graded. There is no human-rating workflow documented on this harness, and no pass-score threshold to configure — that configurability belongs to the standard harness.

Runs are repeatable and comparable: "Run the same evaluation multiple times. Each run is saved separately, so you can compare results across runs." Results export via **…** → **Export test results** to "a CSV file that includes all conversations, responses, and scores."

## Limits

| Item | Value | Source |
|---|---|---|
| CSV upload size | 5 MB | [create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-create) |
| AI generation batch sizes | 10, then 25 or 50 | [create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-create) |
| Conversations per evaluation | **Not documented** | — |
| Characters per question | **Not documented** | — |
| Results retention | **Not documented** for this harness; the standard harness states 89 days | [standard harness results](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-results) |
| Run duration | "Depending on the number of conversations, this process might take several minutes" | [results](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-results) |

Evaluating is billed: "Usage-based billing applies to using, building, testing, and evaluating agents. These actions might consume Copilot Credits." A large test set is a real cost, not just a wait.

## What the standard harness has that this one does not

Recorded because it is the likely near-future shape of this feature, and because it explains why so much writing about Copilot Studio evaluation does not match what a GitHub-Copilot-harness user sees. On the **standard harness** ([create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create)):

| Test method | Measures | Scoring |
|---|---|---|
| General quality | Response quality | Scored out of 100% |
| Content safety | Harmful content | Pass/fail |
| Compare meaning | Meaning vs expected answer | Scored out of 100% |
| Tool use | Whether expected resources were called | Pass/fail |
| Keyword match | Expected keywords present | Pass/fail |
| Text similarity | Text vs expected answer | Scored out of 100% |
| Exact match | Exact match to expected answer | Pass/fail |
| Custom | Your own criteria and labels | Pass/fail |

"All test methods, except *general quality*, require expected responses or keywords." Every method that would consume an expected answer is absent from the GitHub Copilot harness today — which is precisely why expected answers do nothing there yet.

## Implications for `copilot-evaluation-creator`

- **Invest in questions, not expected answers.** The question is the only input the grader sees. Cases should probe the rules, the scope boundary, the escalation trigger and the edge cases from the brief, phrased as a real user would phrase them.
- **Still write expected responses.** The field exists, the UI accepts them, they cost little, and they are what a human reads when auditing a Fail. Say plainly in the skill that they are not scored today.
- **Success criteria become the human review rubric.** The brief's success-criteria slot — deliberately excluded from instructions in [issue #5](https://github.com/matheus-sancha/copilot-studio-skills/issues/5) — cannot be scored automatically here, because nothing compares output to an expectation. It belongs in the hand-off text as what the user should look for when reading results.
- **Do not emit CSV headers from memory.** Tell the user to download the template from the **CSV** link and match it.
- **Size the set against cost and the 5 MB ceiling**, and note that Microsoft's own AI generation produces 10/25/50 — a reasonable anchor for how many cases is normal.
- **Tell the user to set the User profile.** An evaluation run under the wrong profile silently fails to exercise tools and connections, which makes a passing score meaningless.
