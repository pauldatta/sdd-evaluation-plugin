# Module 3: Evaluation Plugins & Skills

This repository is a curated collection of evaluation skills and plugins designed for **Module 3** (AI Agent & Technical Spec Evaluation). It provides AI agents and developers with standardized rubrics, step-by-step evaluation workflows, guardrails, and templates to assess Software Design Documents (SDDs), measure architecture drift, generate 4-tier golden datasets, and run comprehensive AI agent evaluation suites.

These skills are compatible across multi-agent environments including **Antigravity**, **Gemini CLI**, **Claude Code**, and Jetski.

> **Note:** This collection of skills in the `skills/` directory is designed to be modular and will continue to grow as new evaluation metrics, domain rubrics, and diagnostic tools are added.

---

## 📁 Repository Structure

```
evaluation-plugins/
├── plugin.json                          # Plugin manifest and metadata
├── rules/                               # System rules and skill guardrails
│   └── sdd-evaluation-guardrails.md      # Behavioral guardrails for SDD evaluation
├── skills/                              # Modular skills directory (extensible)
│   ├── agent-eval-guide/                # AI Agent Evaluation Design & Report Authoring Skill
│   ├── architecture-drift-evaluation/  # Code vs SDD Architecture Drift Evaluation Skill
│   ├── eval-adk-skill/                  # 4-Tier Golden Evalset Engineering & Evaluation for Google ADK
│   ├── eval-agentcli-skill/             # ADK Agent Evaluation Runner & Preflight Check Skill
│   └── sdd-evaluation/                  # Software Design Document Evaluation Skill
└── README.md
```

---

## 🛠 Available Skills

### 1. `agent-eval-guide` — Agent Evaluation Design & Report Authoring
- **Location:** `skills/agent-eval-guide/`
- **Description:** Guides software engineers and AI practitioners through assessing any **Business Requirements Document (BRD)** and creating a 2-section **Agent Evaluation Report** (`evaluation_report.md`).
- **Key Features:**
  - **BRD Assessment:** Extracts functional requirements, non-functional requirements (NFRs), and AI safety guardrails.
  - **Section 1 (Approach & Design):** Maps test scenarios across use cases, defines scoring metrics/formulas, cost models, and synthetic dataset curation rules.
  - **Section 2 (Execution Results & Diagnostics):** Standardizes pass/fail reporting, failure root-cause analysis, and actionable remediation steps (prompt tuning, tool schema updates, rubric recalibration).
- **How to Use:**
  - Reference the instructions in [`skills/agent-eval-guide/SKILL.md`](skills/agent-eval-guide/SKILL.md).
  - Follow structural guidelines in [`skills/agent-eval-guide/references/report_template.md`](skills/agent-eval-guide/references/report_template.md) and [`skills/agent-eval-guide/references/approach_guide.md`](skills/agent-eval-guide/references/approach_guide.md).

### 2. `architecture-drift-evaluation` — Architecture Drift Evaluation
- **Location:** `skills/architecture-drift-evaluation/`
- **Description:** Evaluates a code repository against its Software Design Document (SDD) and BRD context to measure **Architecture Drift** — the delta between proposed architecture and actual implementation.
- **Key Features:** Audits component topology, design patterns, API & data contracts, deployment scripts, evaluation assets, and operational readiness.
- **How to Use:** Reference the instructions in [`skills/architecture-drift-evaluation/SKILL.md`](skills/architecture-drift-evaluation/SKILL.md).

### 3. `eval-adk-skill` — ADK 4-Tier Golden Evalset & MAS Evaluation
- **Location:** `skills/eval-adk-skill/`
- **Description:** Scaffolds, validates, and executes 4-Tier Stratified golden evaluation datasets (`*.evalset.json`), test configs (`eval_config.json`), and evaluation reports for Single-Agent and Multi-Agent Systems built on Google ADK.
- **How to Use:** Reference the instructions in [`skills/eval-adk-skill/SKILL.md`](skills/eval-adk-skill/SKILL.md).

### 4. `eval-agentcli-skill` — ADK Agent CLI Evaluation Runner
- **Location:** `skills/eval-agentcli-skill/`
- **Description:** Orchestrates preflight environment checks and executes Google Agents CLI (`google-agents-cli eval run`) to evaluate ADK agents.
- **How to Use:** Reference the instructions in [`skills/eval-agentcli-skill/SKILL.md`](skills/eval-agentcli-skill/SKILL.md).

### 5. `sdd-evaluation` — Software Design Document Evaluation
- **Location:** `skills/sdd-evaluation/`
- **Description:** Evaluates Software Design Documents (SDDs) across 6 weighted dimensions to produce scored verdicts, evidence citations, gap analyses, and actionable improvement recommendations.
- **Evaluation Dimensions:**
  1. **Problem Definition (20%):** Clarity of problem, user impact, success metrics.
  2. **Architecture & Design (25%):** Component structure, data flow, trade-offs, and visual diagrams.
  3. **Non-Functional Requirements (20%):** Security, scalability, reliability, cost.
  4. **Risk Analysis (15%):** Risk identification, mitigations, dependencies.
  5. **Feasibility & Planning (10%):** Timelines, milestones, resource allocation.
  6. **Clarity & Communication (10%):** Technical writing quality, consistent terminology, diagram clarity.
- **How to Use:**
  - **Slash Command:** `/sdd-evaluate`
  - **Natural Language:** "Evaluate my SDD", "Score this design doc", "Review the design document at docs/sdd.md"
  - **Input Formats:** Accepts local file paths (`.md`, `.txt`, etc.) or pasted Markdown content. Handles Mermaid diagrams and embedded images.
  - **Output:** Produces a structured verdict (e.g., `STRONG PASS`, `PASS`, `CONDITIONAL`, `NEEDS WORK`) along with JSON metadata and recommendations.
  - Reference instructions in [`skills/sdd-evaluation/SKILL.md`](skills/sdd-evaluation/SKILL.md), rubric in [`skills/sdd-evaluation/references/sdd-rubric.md`](skills/sdd-evaluation/references/sdd-rubric.md), and template in [`skills/sdd-evaluation/references/sdd-template.md`](skills/sdd-evaluation/references/sdd-template.md).

---

## 🔒 Evaluation Rules & Guardrails

The `rules/` folder contains guardrails for skill execution:
- **`sdd-evaluation-guardrails.md`**: Enforces evidence-based scoring, objectivity & calibration, and visual diagram verification specifically for the `sdd-evaluation` skill.

See [`rules/sdd-evaluation-guardrails.md`](rules/sdd-evaluation-guardrails.md) for details.

---

## 🚀 Adding New Skills

As Module 3 expands, new skills should follow the standard structure:

```
skills/<skill-name>/
├── SKILL.md                 # Frontmatter (name, description) + detailed workflow instructions
├── references/              # (Optional) Templates, rubrics, and reference guides
└── README.md                # (Optional) Skill overview
```

When adding a skill, update `plugin.json` if applicable and register the new skill in this `README.md`.
