# Agent Evaluation Guide Skill (`agent-eval-guide`)

Guide software engineers and AI practitioners through assessing Business Requirements Documents (BRDs) and designing a comprehensive, 2-section **AI Agent Evaluation Report** (`evaluation_report.md`).

Works with **Antigravity**, **Gemini CLI**, **Claude Code**, and **Jetski**.

---

## What It Does

The `agent-eval-guide` skill provides a systematic benchmark methodology for evaluating AI Agents across functional use cases, non-functional requirements (NFRs), system safety guardrails, and multi-turn trajectories.

It guides you through creating a standardized 2-section evaluation report:

| Section | Focus Area | Key Components |
|---|---|---|
| **Section 1: Evaluation Approach & Design** | Methodology & Architecture | BRD Use Case Mapping, Metric Selection & Formulas, Cost & Efficiency Modeling, Dataset Curation Rules, Guardrail Scenarios |
| **Section 2: Execution Results & Diagnostics** | Results & Root Cause Analysis | Execution Summary & Pass Rates, Failure Diagnostics (Tool Calls, Payload Mismatches), Actionable Remediation (Prompt Tuning, Threshold Calibration) |

---

## Recommended Workspace Layout

When organizing evaluation assets in an AI agent project, structure your test suite as follows:

```
my-agent/
├── app/                              # Core agent implementation & prompt configurations
├── tests/
│   ├── eval/                         # Evaluation suite
│   │   ├── datasets/                 
│   │   │   ├── eval-data.json        # Evaluation dataset file(s)
│   │   ├── eval_config.yaml          # Metrics and threshold configurations
│   │   └── evaluation_report.md      # 2-Section Evaluation Report
│   ├── integration/                  # End-to-end integration tests
│   └── unit/                         # Unit tests
├── pyproject.toml                    # Dependencies & project metadata
└── README.md
```

---

## Quick Start

### Natural Language Invocation

Ask your coding assistant:

> "Guide me through creating an evaluation report for our agent using `docs/brd.md`"

> "Help me design an evaluation approach and scoring rubric for this AI agent"

> "Review our evaluation results and generate Section 2 diagnostics for failing tests"

---

## Workflow Overview

1. **BRD Analysis:**
   - Extract Functional Scenarios (Knowledge, Transactional workflows, Multi-system orchestration).
   - Identify Non-Functional Requirements (NFRs) & Safety Guardrails.
   - Establish Evaluation Scope & Assumptions.
2. **Section 1 (Evaluation Approach & Design):**
   - Build Use Case Matrix & Select Metrics.
   - Define Aggregation Formulas & Token/Cost Budgets.
   - Document Test Dataset Curation Strategy.
3. **Section 2 (Execution Results Output & Diagnostics):**
   - Summarize Execution Pass/Fail Rates.
   - Perform Failure Root Cause Diagnostics (actual vs. expected tool calls, LLM responses).
   - Formulate Actionable Tuning Recommendations.

---

## Directory Structure

```
skills/agent-eval-guide/
├── SKILL.md                          # Main evaluation workflow & instructions
├── README.md                         # This file
└── references/
    ├── approach_guide.md             # Benchmark evaluation methodology & cost modeling guide
    └── report_template.md            # Canonical 2-section evaluation report markdown template
```

---

## Reference Guidance & Customization

- **Approach Methodology:** See [`references/approach_guide.md`](references/approach_guide.md) for metric formulation rules, token budget templates, and scoring aggregation formulas.
- **Report Template:** Follow [`references/report_template.md`](references/report_template.md) for the mandatory report section layout when generating `tests/eval/evaluation_report.md`.
