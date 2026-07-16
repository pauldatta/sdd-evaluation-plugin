# SDD Evaluation Plugin

Evaluate Software Design Documents against a **6-dimension rubric** with scored verdicts, evidence-based findings, and actionable recommendations.

Works with **Antigravity**, **Gemini CLI**, and **Claude Code**.

Accepts SDDs from **Google Docs**, **local Markdown files**, or **pasted content**.

---

## What It Does

The plugin scores your SDD across six weighted dimensions:

| Dimension | Weight | What It Measures |
|---|---|---|
| Problem Definition | 20% | Clarity of the problem, user impact, success criteria |
| Architecture & Design | 25% | Solution structure, component design, data flow, diagrams, trade-offs |
| Non-Functional Requirements | 20% | Security, scalability, reliability, performance, cost |
| Risk Analysis | 15% | Identified risks, mitigations, dependencies, unknowns |
| Feasibility & Planning | 10% | Implementation plan, timeline, resource needs, milestones |
| Clarity & Communication | 10% | Writing quality, diagrams, consistent terminology |

Each dimension is scored **1–5**. The weighted score maps to a verdict:

| Verdict | Score | Meaning |
|---|---|---|
| **STRONG PASS** | 4.5 – 5.0 | Ready for implementation with minor polish |
| **PASS** | 3.5 – 4.4 | Solid — ready with noted improvements |
| **CONDITIONAL** | 2.5 – 3.4 | Needs targeted improvements first |
| **NEEDS WORK** | 1.5 – 2.4 | Major revision required |
| **INSUFFICIENT** | 1.0 – 1.4 | Fundamental rethinking needed |

---

## Installation

### Antigravity

Antigravity automatically discovers plugins from designated directories.

**Global (all workspaces):**

```bash
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git ~/.gemini/config/plugins/sdd-evaluation-plugin
```

**Workspace (current project only):**

```bash
mkdir -p .agents/plugins
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git .agents/plugins/sdd-evaluation-plugin
```

### Gemini CLI

Gemini CLI reads plugins from the same directories as Antigravity.

**Global (all workspaces):**

```bash
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git ~/.gemini/config/plugins/sdd-evaluation-plugin
```

**Workspace (current project only):**

```bash
mkdir -p .agents/plugins
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git .agents/plugins/sdd-evaluation-plugin
```

**For Google Docs support**, install the Google Workspace extension:

```bash
gemini extensions install https://github.com/gemini-cli-extensions/workspace
```

### Claude Code

Claude Code reads skills from `.agents/` directories.

**Workspace (current project):**

```bash
mkdir -p .agents/plugins
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git .agents/plugins/sdd-evaluation-plugin
```

**Global (all projects):**

```bash
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git ~/.claude/plugins/sdd-evaluation-plugin
```

> **Note:** If Claude Code doesn't auto-discover from `~/.claude/plugins/`, add the skill path to your `.claude/settings.json` under the `skills` key.

**For Google Docs support in Claude Code**, add the Google Workspace MCP server to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "npx",
      "args": ["-y", "@anthropic/google-workspace-mcp"]
    }
  }
}
```

Or use any Google Docs MCP server that exposes `docs.getText` and `drive.search` tools.

---

## Quick Start

Once installed, trigger the evaluation with a slash command or natural language.

### Slash Command

```
/sdd-evaluate
```

The agent will ask where your SDD is. Provide one of:

- A **Google Docs URL**: `https://docs.google.com/document/d/1a2b3c4d/edit`
- A **doc name** to search: "the Project Alpha design doc"
- A **file path**: `docs/sdd.md`
- Or just **paste** the content directly

### Natural Language

Ask your coding assistant directly:

> "Evaluate my SDD at https://docs.google.com/document/d/1a2b3c4d/edit"

> "Score the design document in docs/architecture.md"

> "Grade my hackathon design doc — it's called 'Team Rocket SDD' in Google Drive"

> "Review this design doc:" *(then paste the content)*

---

## Source Types

### Google Docs

The agent uses the Google Workspace MCP tools to read your document:

- **URL**: Pass the full Google Docs URL — the tools accept URLs directly (no manual ID extraction needed)
- **Search by name**: The agent searches Google Drive for documents matching your description
- **Multi-tab docs**: All tabs are read and concatenated for evaluation
- **Images**: Embedded images (architecture diagrams, flowcharts) are noted from context. The agent credits the author for including visual aids and evaluates their contribution to architecture and clarity scores
- **Comments & suggestions**: Reviewer comments provide context; suggested edits are not evaluated as accepted content

**Prerequisite:** The Google Workspace extension must be installed (see Installation above).

**Fallback:** If the workspace MCP isn't available, export the Google Doc as Markdown (**File → Download → Markdown**) and provide the local file path instead.

### Local Markdown

The agent reads `.md` files from your workspace:

- **Mermaid diagrams**: Fenced `mermaid` code blocks are treated as architecture diagrams and factored into scoring
- **Inline images**: `![alt](path)` references are resolved and viewed when possible
- **Any text format**: `.md`, `.txt`, and other text files are supported

### Pasted Content

Paste the full SDD content directly into the chat. The agent evaluates it as-is.

> **Tip:** Make sure you paste the complete document, not a summary or excerpt. Truncated documents will get lower scores.

---

## Directory Structure

```
sdd-evaluation-plugin/
├── plugin.json                          # Plugin manifest
├── mcp_config.json                      # MCP server dependencies (Google Workspace)
├── README.md                            # This file
├── skills/
│   └── sdd-evaluation/
│       ├── SKILL.md                     # Evaluation workflow & agent instructions
│       └── references/
│           ├── sdd-rubric.md            # 6-dimension scoring rubric (1–5 scale)
│           ├── sdd-template.md          # Canonical SDD template for gap analysis
│           └── gdocs-integration.md     # Google Docs MCP usage guide
└── rules/
    └── evaluation-guardrails.md         # Behavioral guardrails for objective evaluation
```

---

## Customization

### Adjust the Rubric

Edit `skills/sdd-evaluation/references/sdd-rubric.md` to change dimension weights, scoring indicators, or add new dimensions for your organization's standards.

### Adjust the Template

Edit `skills/sdd-evaluation/references/sdd-template.md` to add or remove sections from the canonical SDD structure your team expects.

### Add Rules

Drop additional `.md` files into `rules/` to add behavioral constraints. For example:
- `rules/enterprise-compliance.md` — require specific compliance sections
- `rules/team-conventions.md` — enforce your team's naming or formatting conventions

---

## License & Ownership

Created by Paul Datta (`pkdatta2000@gmail.com`).

Free for all hackathon participants, solution architects, and engineering teams for self-assessing design documents before implementation.
