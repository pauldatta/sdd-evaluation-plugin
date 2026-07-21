---
name: agent-eval-guide
description: >-
  Guides participants through assessing any Business Requirements Document (BRD) and designing a comprehensive AI Agent evaluation report (Section 1: Evaluation Approach & Design; Section 2: Execution Results Output & Diagnostics) using benchmark methodologies, metric selection rules, and test diagnostic frameworks.
---

# Agent Evaluation Design & Report Authoring Skill (`agent-eval-guide`)

## Overview

This skill guides software engineers and AI practitioners through assessing any **Business Requirements Document (BRD)** and creating a high-quality, 2-section **Agent Evaluation Report** (`evaluation_report.md`). 

The evaluation framework provides a systematic methodology for evaluating AI Agents across functional use cases, non-functional requirements (NFRs), system safety guardrails, and multi-turn conversational trajectories.

### Recommended Evaluation Artifacts Layout

When preparing evaluation assets for an AI Agent repository, structure your files as follows:

```
my-agent/
├── app/                              # Core agent implementation & prompt configurations
├── tests/
│   ├── eval/                         # Evaluation suite ◄
│   │   ├── datasets/                 
│   │   │   ├── eval-data.json        # Evaluation dataset file
│   │   │   └── eval-data-2.json      # You can have 1 or more dataset files
│   │   ├── eval_config.yaml          # Metrics and threshold configurations
│   │   └── evaluation_report.md      # 2-Section Evaluation Report (Approach & Execution Results)
│   ├── integration/                  # End-to-end integration tests
│   └── unit/                         # Unit tests
├── pyproject.toml                    # Dependencies & project metadata
└── README.md
```

---

## Reference Assets & Guidance Files

This skill relies on two core reference documents located in `references/`:

1. **[approach_guide.md](references/approach_guide.md)**: Benchmark Evaluation Approach Guide. Details the structural sections, content requirements, metric selection rationale, cost modeling, and scoring formulations for authoring an evaluation approach.
2. **[report_template.md](references/report_template.md)**: Evaluation Report Template. Provides the canonical markdown structure for the evaluation report.

> **CRITICAL REPORT FORMAT MANDATE**: When generating the evaluation report (`tests/eval/evaluation_report.md`), follow the structure and section layout defined in **[report_template.md](references/report_template.md)**. You may include additional content if relevant.

---

## Step-by-Step Guide: Assessing a Business Requirements Document (BRD)

Before writing an evaluation report, perform a thorough analysis of the target Business Requirements Document (`brd.md`):

### 1. Extract Functional Requirements & Use Case Scenarios
Review the functional scope specified in the BRD and group capabilities into evaluation categories:
- **Knowledge & Policy Systems**: Evaluate coverage across knowledge repositories, documentation stores, and factual query resolution.
- **Transactional & Action Workflows**: Evaluate system read/write actions, data validation rules, and backend API interactions.
- **Multi-System Orchestration**: Evaluate workflows that require coordinating multiple tools, sub-agents, or cross-system steps.

### 2. Identify Non-Functional Requirements & Safety Guardrails
Extract system constraints and operational expectations from the BRD:
- **AI Safety & System Governance**: Define evaluation coverage for system safety policies, data privacy rules, and operational boundaries.
- **Fault Tolerance & Reliability**: Define evaluation coverage for system handling of service disruptions, error states, and performance constraints.

### 3. Formulate Evaluation Assumptions & Context Scope
Explicitly document scope context and assumptions:
- **Organizational Context & Personas**: User roles, access permissions, and deployment scale.
- **User Input Diversity**: Expected input variations, regional or language requirements, and user communication characteristics.
- **Operational Priorities**: High-priority workflows and critical risk areas.

---

## Structuring the 2-Section Evaluation Report

When generating `tests/eval/evaluation_report.md`, follow the template structure defined in **[report_template.md](references/report_template.md)**. The report includes two core sections:

### Section 1: Evaluation Approach & Design

Section 1 documents your evaluation methodology and design rationale. It must align with the guidance in **[approach_guide.md](references/approach_guide.md)** and cover four core domains:

1. **Relevance to BRD & Evaluation Assumptions**:
   - Explicitly detail evaluation assumptions.
   - Verify alignment of test scenarios with BRD requirements and use cases.

2. **Approach Quality & Rigor**:
   - **Use Case Evaluation Matrix**: Map test scenarios across all functional patterns.
   - **Target Metrics & Selection Rationale**: Justify metric choices against business goals.
   - **Score Calculation & Formulas**: Define mathematical aggregation formulas across individual metrics.
   - **Evaluation Data Curation**: Explain evaluation data generation methodologies and turn structures.

3. **Cost & Time Considerations**:
   - Model end-to-end evaluation costs.
   - Define runtime batching, concurrency worker limits, and rate-limit handling strategies. Use the token budget template in **[approach_guide.md Section 5](references/approach_guide.md#5-cost--efficiency-optimization-architecture)**.

4. **Guardrail & Validation Rigor**:
   - Detail test data acquisition for AI safety, governance, and operational fault tolerance.

### Section 2: Execution Results Analysis & Test Diagnostics

Section 2 details the execution log, test suite pass/fail metrics, and diagnostics following **[report_template.md Section 2](references/report_template.md#section-2-evaluation-execution-output--results)**:

1. **Execution Summary & Pass Rate**:
   - Report overall execution status (`PASSED` or `FAILED`), total test count, passed count, failed count, and pass rate.
2. **Failure Root Cause Diagnostics**:
   - For any failed test case, diagnose **why it failed**: failing metric, expected vs. actual response, expected vs. actual API tool calls, and payload parameter mismatches.
3. **Actionable Tuning & Remediation Recommendations**:
   - Provide concrete, actionable tuning steps for failed tests:
     - **Prompt / Instruction Tuning**: Refining system prompts, role boundaries, or routing guidelines.
     - **Tool & Routing Adjustments**: Adjusting tool schemas, parameter parsers, or router dispatching rules.
     - **Threshold Calibration**: Recalibrating LLM-as-a-Judge rubrics or metric thresholds.
     - **Agent Logic & Guardrail Updates**: Updating backend logic for edge cases and boundary handling.

---

## Evaluation Scoring & Quality Rubric

Evaluation reports are assessed on a **1.0 to 5.0 floating-point scale** across core domain dimensions. Define a suitable overall score calculation formula for your approach, for example:

$$S_{\text{overall}} = w_{\text{relevance}} \cdot S_{\text{relevance}} + w_{\text{rigor}} \cdot S_{\text{rigor}} + w_{\text{efficiency}} \cdot S_{\text{cost\_time}} + w_{\text{guardrails}} \cdot S_{\text{guardrails}}$$

### Domain Scoring Guidance

| Domain | Focus Area |
| :--- | :--- |
| **BRD Relevance & Assumptions** | Alignment with BRD use cases, realistic assumption formulation, and domain scope context. |
| **Approach Quality & Rigor** | Comprehensive test matrix, justified metric selection, clear formulas, and synthetic dataset curation rigor. |
| **Cost & Time Considerations** | Budget calculations, evaluation efficiency. |
| **Guardrail & Validation Rigor** | Safety test coverage and operational fault resilience. |

---

## Key Best Practices & Anti-Patterns

- **DO**: Ground every evaluation scenario in explicit BRD requirement IDs.
- **DO**: Follow the template layout in **[references/report_template.md](references/report_template.md)** strictly when generating reports.
- **DO**: Include both single-turn and multi-turn dialogue scenarios.
- **DO**: Provide step-by-step reasoning for LLM-as-a-Judge evaluations and implement human sampling strategies (see **[approach_guide.md Section 6](references/approach_guide.md#6-scoring-formulation--aggregation-strategy)**).
- **DON'T**: Rely solely on simple string matching for free-text response evaluations.
- **DON'T**: Omit backend fault tolerance or safety guardrails from test suites.
