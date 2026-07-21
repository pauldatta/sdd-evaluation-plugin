# Architecture Drift Evaluation — Detailed Scoring Rubric

This document provides explicit integer scoring criteria (1–5) for each of the four core axes. Every axis score **MUST be an integer (1, 2, 3, 4, or 5)** based on cited evidence from the SDD and codebase.

> [!IMPORTANT]
> **Scope Calibration Rule**: Features, infrastructure, or components explicitly designated in the SDD as *"Future State Design"*, *"Future Readiness"*, *"Phase 2"*, or *"Out of Scope for MVP"* (e.g., future Redis caching, Bigtable stores, or Pub/Sub event buffers) **MUST NOT** deduct points from any axis score. Only features and components intended for the current release/MVP are evaluated for drift.

> [!CAUTION]
> **Generalized Evaluation Principles for Architectural Drift**:
> 1. **Environment Isolation & Portability**: Any implementation choices that prevent code from executing seamlessly across environments (dev, staging, prod, CI/CD, multi-user runtime) — such as fixed hostnames/IPs, machine-specific file paths, static user identities, or hardcoded project IDs — represent severe architectural drift and **CAP affected axes at MAX SCORE 3**.
> 2. **Security & IAM Boundary Realization**: Any shortcuts that bypass intended authentication, authorization, tenant isolation, PII guardrails, or secret management specifications in the SDD (e.g., hardcoding test identity headers, bypassing token validation, embedding secrets in code) represent critical security drift and **CAP affected axes at MAX SCORE 3**.
> 3. **Unfulfilled SDD Commitments**: Any component, design pattern, infrastructure manifest (IaC, deployment scripts), evaluation asset, or operational mechanism specified as in-scope in the SDD that is omitted, broken, or replaced with an ad-hoc workaround represents architectural drift and **CAPS affected axes at MAX SCORE 3**.
> 4. **High Bar for Score 5 (Exact Alignment)**: Score 5 is reserved ONLY for implementations with zero environment assumptions, zero security/IAM shortcuts, and zero unfulfilled SDD commitments.

---

## Axis 1: Component & Topology Alignment (Weight: 30%)

Evaluates whether the planned services, sub-agents, MCP servers, packages, modules, and layered boundaries specified in the SDD exist in the codebase and maintain their designated responsibilities.

| Score | Rating | Criteria & Indicators |
|:---:|:---:|---|
| **5** | **Exact Alignment** | All specified components, microservices/modules, background workers, and boundary layers exist precisely as specified in the SDD. No missing planned components and no unapproved rogue modules. Component boundaries and responsibilities strictly match the design document. |
| **4** | **Minor Structural Variation** | All core components and services exist. Minor non-breaking differences in directory naming, module splitting, or sub-package organization (e.g., combining two small helper services specified separately into a unified service module). Responsibilities remain well-isolated. |
| **3** | **Moderate Component Drift** | Most major components exist, but 1 or 2 secondary services/modules specified in the SDD are missing or merged into unrelated modules. Some responsibilities overlap or leak across module boundaries. |
| **2** | **Major Topology Divergence** | Core components specified in the SDD (e.g., dedicated worker service, evaluation engine, database adapter) are completely missing or collapsed into a single monolithic script. Major architectural boundaries are ignored. |
| **1** | **Complete Structural Mismatch** | Codebase topology bears almost no resemblance to the SDD architecture diagram. Planned multi-tier/multi-agent architecture is replaced by ad-hoc scripts or unstructured code. |

---

## Axis 2: Design Pattern & Abstraction Drift (Weight: 25%)

Evaluates whether the implementation adheres to the architectural design patterns, abstractions, and middleware pipelines specified in the SDD (e.g., Agent/MCP tool definitions, controller-service-repository, dependency injection, async task queues).

| Score | Rating | Criteria & Indicators |
|:---:|:---:|---|
| **5** | **Pattern Compliant** | Architectural patterns specified in the SDD are consistently implemented. Abstractions are clean and unbypassed (e.g., routers interact strictly through service interfaces, database access is encapsulated within repository/storage adapters, agent tools adhere to standard interfaces). |
| **4** | **Minor Pattern Shortcuts** | Specified design patterns are followed across >85% of the codebase. Occasional minor shortcuts (e.g., a simple read-only endpoint accessing ORM models directly instead of going through the storage adapter facade), but core architectural abstractions remain solid. |
| **3** | **Noticeable Abstraction Leakage** | Mixed design patterns. Several endpoints bypass service/adapter layers. High-level orchestrators contain low-level business logic. Abstractions leak implementation details across component boundaries. |
| **4** → **2** | **Systemic Pattern Bypass** | Key design patterns specified in the SDD are largely ignored. Services query databases directly, sub-agents bypass orchestrator protocols, or middleware guards (auth, rate-limiting, error handling) are missing across core paths. |
| **1** | **No Architectural Abstractions** | Code is completely unstructured with anti-patterns throughout (e.g., global state mutation, tight coupling, copy-pasted business logic, zero separation of concerns). |

---

## Axis 3: API & Data Contract Compliance (Weight: 20%)

Evaluates whether REST/gRPC endpoints, DTO schemas, database tables, ORM entities, and event payloads in code match the contract specifications in the SDD.

| Score | Rating | Criteria & Indicators |
|:---:|:---:|---|
| **5** | **Strict Schema Compliance** | All API routes, HTTP methods, path parameters, request/response DTOs, and database tables/fields strictly conform to the contracts defined in the SDD. Schema types, field constraints, and relationships are 100% aligned. |
| **4** | **Backward-Compatible Extensions** | API routes and database schemas match the SDD. Minor additive changes present in code (e.g., additional optional response fields or extra filter parameters) that enhance functionality without violating the SDD contract. |
| **3** | **Field/Type Discrepancies** | Core endpoints and tables exist, but several field names, data types, or status codes differ from the SDD specification (e.g., SDD specifies `status: Enum` but code uses string, or required payload fields in SDD are missing/optional in code). |
| **2** | **Breaking Contract Deviations** | Multiple API route paths, request payload structures, or database schemas break compatibility with the SDD specification. Key endpoint routes specified in the SDD are missing or return entirely different data structures. |
| **1** | **Arbitrary / Undocumented Contracts** | Endpoint signatures and database structures appear completely arbitrary with no correlation to the SDD contract specifications. |

---

## Axis 4: Deployment, Evaluation & Operational Readiness (Weight: 25%)

Evaluates whether deployment scripts/documentation, evaluation assets/verifications, and operational mechanisms specified in the SDD were actually delivered and function as designed.

| Score | Rating | Criteria & Indicators |
|:---:|:---:|---|
| **5** | **Fully Realized Operations & Evals** | **Deployment**: Containerization (`Dockerfile`), build/deploy scripts (`Makefile`, Terraform, Cloud Run), and setup documentation (`README.md`) exist and match SDD deployment topology.<br>**Evaluation**: Specified test suites, evaluation scripts (`run_all_evals.py`), benchmark datasets (`evalset.json`), and evaluation methodology docs exist and run cleanly.<br>**Operational**: Auth boundaries, secret handling (`.env.example`), logging/telemetry, and health checks match SDD NFR commitments. |
| **4** | **Minor Operational/Eval Gaps** | Deployment scripts, Dockerfile, setup docs, and test suites are present. Minor gaps exist (e.g., build target missing an optional flag, or evaluation dataset missing 1 non-critical test case), but deployment and evaluations are fully executable. |
| **3** | **Partial Deployment/Eval Delivery** | Core application runs, but key deployment or evaluation artifacts specified in the SDD are missing (e.g., missing Dockerfile or Terraform script, setup docs are incomplete, or evaluation harness lacks benchmark datasets). |
| **2** | **Major Operational Omision** | Deployment scripts are broken or absent. No evaluation suite or benchmark datasets exist despite being specified in the SDD. Environment configuration and secret handling are unmanaged or hardcoded. |
| **1** | **Non-Deployable & Unevaluated** | Zero deployment scripts, zero documentation, zero evaluation test suites. Code cannot be deployed or verified without extensive re-engineering. |
