# Benchmark Evaluation Approach Reference Guide (`approach_guide.md`)

## Overview

This document provides a reference framework for structuring, authoring, and organizing an **AI Agent Evaluation Approach & Design** document based on any Business Requirements Document (`brd.md`).

When authoring your evaluation approach, use this guide to ensure your evaluation methodology is comprehensive, structured, mathematically sound, and clearly justified.

---

## 1. Documenting Evaluation Scope & Assumptions

An effective evaluation approach begins by defining the operational scope and context under which the evaluation design was constructed.

### Key Content Elements:
- **System Scope & Integration Boundaries**: Clearly document which backend systems, APIs, and data sources are considered in-scope for evaluation versus those that are out-of-scope.
- **User Personas & Deployment Context**: Describe the target user profiles, organizational characteristics, and operational environment assumed in your evaluation design.
- **Evaluation Assumptions**: State all underlying design assumptions that shape your test scenario selection, dataset structures, and priority weighting.

---

## 2. Structuring the Functional Evaluation Matrix

The evaluation matrix forms the core of Section 1 in your report. It details how functional requirements from the BRD are translated into structured evaluation scenarios.

### Key Content Elements:
- **Use Case Mapping**: Group functional requirements into logical operational categories based on the BRD.
- **Evaluation Scenarios**: For each functional category, describe the scope of test scenarios designed to validate system capabilities.
- **Evaluation Data Methodology**: Explain how evaluation datasets are constructed, curated, and formatted (including dataset sources, synthetic variation generation, and conversational turn structures).
- **Metric Selection & Rationale**: List the target metrics selected for each use case category, along with detailed justifications explaining why each metric is appropriate for measuring success.

---

## 3. Metric Selection & Mathematical Scoring Formulation

Evaluation approaches must define clear, objective metrics and describe how individual test scores are calculated and aggregated.

### Key Content Elements:
- **Metric Definitions**: Define each evaluation metric clearly, specifying what system output or behavior it evaluates (e.g., retrieval accuracy, content groundedness, task execution correctness).
- **Scoring Formulas**: Provide mathematical formulas for metric calculations and describe how single-test scores are combined into category or domain averages.
- **Thresholds & Assertion Criteria**: Document target score thresholds or pass/fail criteria for each metric based on business criticality.

---

## 4. Non-Functional & Guardrail Evaluation Strategy

Document how your evaluation approach assesses non-functional requirements, safety constraints, and system reliability.

### Key Content Elements:
- **AI Safety & Governance**: Describe your evaluation strategy for verifying system adherence to safety policies, data privacy rules, and scope containment.
- **Operational Fault Tolerance & Resilience**: Detail how the evaluation design assesses system handling of backend errors, service disruptions, and performance constraints.

---

## 5. Cost, Time & Efficiency Architecture

A complete evaluation approach addresses the operational overhead of running evaluation suites at scale.

### Key Content Elements:
- **Evaluation Cost Modeling**: Estimate token consumption budgets for dataset generation, agent execution, and LLM-as-a-Judge evaluations.
- **Execution Concurrency & Efficiency**: Describe strategies for managing rate limits, worker concurrency, and execution time during evaluation runs.

---

## 6. Overall Scoring Aggregation & Guidance Rubric

Define an overall scoring formulation $S_{\text{overall}} \in [1.0, 5.0]$ that aggregates domain scores into a final weighted rating, one example could be:

$$S_{\text{overall}} = w_{\text{relevance}} \cdot S_{\text{relevance}} + w_{\text{rigor}} \cdot S_{\text{rigor}} + w_{\text{efficiency}} \cdot S_{\text{cost\_time}} + w_{\text{guardrails}} \cdot S_{\text{guardrails}}$$

*(where weights $w_i \ge 0$ sum to 1.0 based on project priorities).*

### Guidance Score Level Definitions:
- **5.0 (Exceptional)**: Outstanding methodology covering functional patterns, explicit guardrail testing, justified metrics, and complete cost/efficiency modeling.
- **4.0 (Strong)**: Comprehensive coverage of primary use cases with sound metrics, guardrail testing, and evaluation logic.
- **3.0 (Adequate)**: Baseline coverage with standard evaluation metrics.
- **2.0 (Developing)**: Initial evaluation structure; needs improvement in metric selection rationale, cost modeling, or guardrail testing.
- **1.0 (Initial)**: Unstructured setup lacking clear domain scenarios or grounded metrics.

---

## 7. Diagnostic & Remediation Framework

Describe how test execution failure outputs (Section 2 of the report) are analyzed to produce actionable diagnostic feedback and tuning recommendations for prompt, routing, tool, or logic improvements.
