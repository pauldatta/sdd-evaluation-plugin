---
name: architecture-drift-evaluation
description: >-
  Evaluates a code repository against its Software Design Document (SDD) and BRD context to measure Architecture Drift.
  Audits component topology, design patterns, API & data contracts, deployment scripts/docs, evaluation assets, and operational readiness.
  Produces an integer-scored rubric (1-5 per axis) and evidence-backed drift report with letter grade.
---

# Architecture Drift Evaluation

## Overview

Measure **Architecture Drift** — the delta between a proposed Software Design Document (SDD) and its actual implementation in code. The BRD provides background business context for design trade-offs, while the SDD serves as the authoritative architectural blueprint.

This evaluation is designed to answer a single critical question: **How much has the implementation moved away from the original SDD plan?**

It produces an evidence-backed scorecard across four core axes with integer scores (1–5) per axis and a weighted aggregate score with an A–F letter grade.

---

## When to Use

- Auditing a newly delivered codebase against its technical design specification.
- Measuring technical debt or architectural drift prior to a major release.
- Evaluating hackathon or contractor deliverables against a required SDD spec.
- Post-implementation architecture review to verify that design goals were realized.

**When NOT to use:**
- Reviewing code quality without a design doc (use `code-quality-evaluation`).
- Reviewing a design doc before implementation starts (use `sdd-evaluation`).
- Evaluating synthetic evaluation datasets in isolation (use `eval-asset-evaluation`).

---

## Evaluation Workflow

```
PHASE 1: SCOPE & CONTEXT  ──→ PHASE 2: SPEC ANALYSIS  ──→ PHASE 3: CODEBASE AUDIT  ──→ PHASE 4: SCORING & REPORT
          │                              │                          │                              │
          ▼                              ▼                          ▼                              ▼
  Gather SDD, BRD,             Extract components,         Examine code structure,        Score axes 1–5 (integers),
  & Code Repository            contracts, deployment,      endpoints, models, scripts,    compute weighted score,
                               & evaluation specs          & eval harnesses               & cite file evidence
```

### Phase 1: Scope & Context

1. **Verify BRD & SDD Artifacts with User (MANDATORY)**:
   - Search the workspace/repository for the Software Design Document (SDD) and Business Requirements Document (BRD).
   - **Confirm Document Selection**: Present the identified BRD and SDD files to the user for confirmation.
   - **Handle Missing/Ambiguous Specs**: If either the SDD or BRD is missing, unreadable, or ambiguous, **STOP AND ASK THE USER** to provide or specify the correct document paths. Do NOT proceed on unverified assumptions.
2. **Identify Target Codebase**: Confirm the repository path, primary module directories, and build system configuration.
3. **Present Scope Summary to User**:
   ```
   SCOPE SUMMARY:
   - Target Codebase: [repo/path]
   - SDD Specification: [sdd_file_path] (Confirmed)
   - BRD Context: [brd_file_path] (Confirmed)
   - Tech Stack: [language, framework, build system]
   → Proceeding with architecture drift evaluation. Please confirm or provide alternate spec documents.
   ```

### Phase 2: Spec Analysis (SDD Blueprint Extraction & Scope Calibration)

Extract the target architectural specifications from the SDD:
- **Scope Calibration Rule (CRITICAL)**: Distinguish between **In-Scope Current MVP** deliverables and **Future State / Post-MVP** architecture.
  - Features, infrastructure, or components explicitly marked in the SDD as *"Future State Design"*, *"Future Readiness"*, *"Phase 2"*, or *"Out of Scope for MVP"* (e.g., future Redis caching, Bigtable scale stores, Pub/Sub pipelines) **MUST NOT** penalize current implementation scores.
  - Log future-state notes separately as *Informational / Future Alignment Notes*.
- **Planned Component Topology**: Expected current-phase services, modules, layers, sub-agents, MCP servers, and boundary interfaces.
- **Architectural Patterns**: Intended current-phase design patterns (e.g., controller-service-repository, agent/MCP orchestration, event-driven pipelines).
- **API & Data Contracts**: Current-phase REST/gRPC endpoint signatures, DTOs, database models, schemas, and event payloads.
- **Deployment & Operational Spec**: Container configuration (`Dockerfile`), deployment scripts (`Makefile`, Terraform, Cloud Run), environment variables, and setup documentation (`README.md`).
- **Evaluation & Test Strategy**: Specified test suites, evaluation frameworks, benchmark scripts (`run_all_evals.py`), evaluation datasets (`evalset.json`), and methodology docs.

### Phase 3: Codebase Audit (SDD vs. Code Inspection)
Walk the codebase looking for architectural deviations. For each finding, cite exact file paths and line ranges.
- **Missing Components**: Modules or services specified in SDD but absent in code.
- **Rogue / Unapproved Components**: Substantial code modules present in code but not specified in SDD.
- **Pattern Bypass**: Bypassing layered architecture (e.g., router calling DB directly, skipping service layer).
- **Contract Mismatch**: Endpoints or database models that deviate from SDD schemas.
- **Deployment & Eval Gaps**: Missing Dockerfiles, broken build targets, absent setup docs, or unfulfilled benchmark/evaluation test suites.

### Phase 4: Critical Scoring & Report Generation
Score each of the 4 axes using **strict integers (1, 2, 3, 4, or 5)** based on the rubric indicators in `references/drift-rubric.md`. Compute the weighted aggregate score and assign a final letter grade.

---

## Core Rubric Axes & Weights

| # | Axis | Weight | Integer Score Focus (1–5) |
|---|------|:---:|---------------------------|
| 1 | **Component & Topology Alignment** | **30%** | Are all planned services, modules, sub-agents/MCP servers, and layered boundaries present as specified in the SDD? Identifies missing services, misplaced responsibilities, or unapproved rogue modules. |
| 2 | **Design Pattern & Abstraction Drift** | **25%** | Does the codebase follow specified architectural patterns (e.g., Agent/MCP tool definitions, repository pattern, clean layering)? Identifies leaky abstractions, bypassed middleware, or monolithic shortcuts. |
| 3 | **API & Data Contract Compliance** | **20%** | Do actual REST/gRPC endpoints, DTO schemas, database entities, ORM models, and event payloads match the specs in the SDD? |
| 4 | **Deployment, Evaluation & Operational Readiness** | **25%** | **Deployment Details & Documentation**: Are specified container configs (`Dockerfile`), build/deploy scripts (`Makefile`, Terraform, Cloud Run), and setup docs (`README.md`) present and aligned?<br>**Evaluation Assets**: Are specified test suites, benchmark scripts (`run_all_evals.py`), golden evaluation datasets (`evalset.json`), and methodology docs implemented as planned?<br>**Operational Topology**: Are auth boundaries, secret handling, logging/telemetry, and health endpoints realized? |

---

## Scoring Rules & Grade Scale

- **Educational Rigor & Generalized Principles (CRITICAL)**:
  The primary objective is for users and development teams to learn from architectural drift analysis. The evaluator MUST be critical, thorough, and un-lenient. Apply the following generalized principles to all components:

  1. **Principle 1: Environment Isolation & Portability**: Any code, script, or configuration that relies on environment-specific assumptions (e.g., fixed local hostnames/ports, machine-specific file paths, static user identities, or hardcoded project IDs) prevents execution across dev/staging/prod/CI environments and represents architectural drift. **CAP affected axes at maximum 3**.
  2. **Principle 2: Security & IAM Boundary Realization**: Any shortcuts that bypass intended authentication, authorization, tenant isolation, PII guardrails, or secret management specifications in the SDD (e.g., hardcoding test identity headers, bypassing token validation, embedding secrets in code) represent critical security drift. **CAP affected axes at maximum 3**.
  3. **Principle 3: Unfulfilled SDD Commitments**: Any component, design pattern, infrastructure manifest (IaC, deployment scripts), evaluation asset, or operational mechanism specified as in-scope in the SDD that is omitted, broken, or replaced with an ad-hoc workaround represents architectural drift. **CAP affected axes at maximum 3**.
  4. **Principle 4: High Bar for Score 5 (Exact Alignment)**: Score 5 is reserved ONLY for implementations with zero environment assumptions, zero security/IAM shortcuts, and zero unfulfilled SDD commitments.

- **Axis Scores**: Strict integers (`1`, `2`, `3`, `4`, `5`).
- **Weighted Score**: Calculated as `sum(axis.score * axis.weight)`. Can contain decimals (e.g., `3.65`).
- **Grade Scale**:

| Grade | Weighted Score | Meaning |
|:---:|:---:|---|
| **A** | **4.5 – 5.0** | **On Plan (Minimal Drift)** — Fully portable, secure, and strictly matches all in-scope SDD specs. |
| **B** | **3.5 – 4.4** | **Minor Drift** — Key architecture aligned; minor structural or config variations without portability/security gaps. |
| **C** | **2.5 – 3.4** | **Moderate Drift** — Functional, but carrying environment hardcoding, IAM shortcuts, or unfulfilled deployment/eval specs. |
| **D** | **1.5 – 2.4** | **Severe Drift** — Major components missing, misplaced responsibilities, or unapproved architectural workarounds. |
| **F** | **1.0 – 1.4** | **Complete Divergence** — Implementation bears little resemblance to the SDD plan. |

---

## Output JSON Schema (`ArchitectureDriftEvalResult`)

Evaluations using this skill produce structured output matching the following JSON schema:

```json
{
  "overall_drift_score": 3.75,
  "grade": "B",
  "drift_level": "Minor Drift",
  "summary": "Detailed summary of architectural drift assessment...",
  "axes": [
    {
      "name": "Component & Topology Alignment",
      "score": 4,
      "weight": 0.30,
      "evidence": "Evidence citing specific files (e.g., app/routers/evaluation.py)...",
      "gaps": ["Audit service specified in SDD Section 4.2 was omitted from implementation."]
    },
    {
      "name": "Design Pattern & Abstraction Drift",
      "score": 4,
      "weight": 0.25,
      "evidence": "Observed clean controller-service-repository pattern in app/services/...",
      "gaps": ["Direct DB queries found in router handler app/routers/runs.py:45."]
    },
    {
      "name": "API & Data Contract Compliance",
      "score": 3,
      "weight": 0.20,
      "evidence": "Endpoint schemas in app/elevate/main.py match SDD spec except for metadata payload.",
      "gaps": ["Submission model missing metadata_json field specified in SDD section 5.1."]
    },
    {
      "name": "Deployment, Evaluation & Operational Readiness",
      "score": 4,
      "weight": 0.25,
      "evidence": "Dockerfile, Makefile, and run_all_evals.py present and executable.",
      "gaps": ["Evaluation dataset missing 2 required edge-case benchmark suites."]
    }
  ],
  "structural_drift_findings": [
    {
      "category": "Missing Component",
      "sdd_specification": "Audit Logging Service specified in SDD Section 4.2",
      "code_reality": "No logging service found under app/services/",
      "impact": "High"
    }
  ],
  "top_recommendations": [
    "Implement the Audit Logging Service under app/services/audit.py as specified in SDD Section 4.2.",
    "Refactor direct DB queries in app/routers/runs.py to use the storage adapter service."
  ],
  "red_flags": []
}
```

---

## Reference Material

- `references/drift-rubric.md`: Detailed integer scoring criteria (1–5) for each axis.
- `references/drift-checklist.md`: Step-by-step evidence collection and verification checklist.
