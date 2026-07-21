# Architecture Drift Evaluation — Inspection & Verification Checklist

Use this checklist during **Phase 2 (Spec Analysis)** and **Phase 3 (Codebase Audit)** to systematically gather file evidence and identify architectural drift.

---

## 1. Spec Analysis Checklist (Extracting the SDD Blueprint)

Before auditing code, extract and list the expected design specifications from the SDD:

- [ ] **Document & Specification Verification**:
  - Locate BRD and SDD files in the target project.
  - Confirm document selection with the user. If missing or ambiguous, prompt the user for exact paths.
- [ ] **Target Architecture & Topology**:
  - List all services, microservices, background workers, sub-agents, and MCP tools specified in SDD Section 3 & 4.
  - Record expected directory names, module packages, and layered boundaries.
- [ ] **Architectural Patterns**:
  - Record specified design patterns (e.g., Controller-Service-Repository, Event Producer/Consumer, Agent Orchestrator).
- [ ] **API & Data Contracts**:
  - List expected API endpoint routes, HTTP methods, and payload structures.
  - List expected database tables, primary keys, relationships, and ORM entities.
- [ ] **Deployment Specifications**:
  - Record expected container setup (`Dockerfile`), build automation (`Makefile`, scripts), IaC (`Terraform`, Cloud Run manifests), and setup guide (`README.md`).
- [ ] **Evaluation & Verification Strategy**:
  - Record specified test runner suites, benchmark scripts (`run_all_evals.py`), synthetic golden datasets (`*.evalset.json`), and evaluation methodology documents.

---

## 2. Codebase Audit Checklist (SDD vs. Code Inspection)

### Axis 1: Component & Topology Inspection
- [ ] Run `tree` or list directory structure to verify top-level package alignment with SDD.
- [ ] Check for **Missing Components**: Are all SDD-planned modules present in code?
- [ ] Check for **Rogue Components**: Are there unapproved services or modules not described in the SDD?
- [ ] Verify component boundaries: Do services import across boundaries cleanly without circular dependencies?

### Axis 2: Design Pattern & Abstraction Inspection
- [ ] Inspect API router/controller files: Do handlers delegate to business logic services, or do they make direct DB/external calls?
- [ ] Inspect agent/MCP tools: Are agent tools encapsulated using standard SDK hooks/decorators?
- [ ] Inspect storage & database layer: Is database access isolated within ORM models and repository/storage adapters?
- [ ] Inspect error handling & logging: Is error handling centralized or copy-pasted across endpoints?

### Axis 3: API & Data Contract Inspection
- [ ] Compare API endpoint routes in code against SDD route specifications.
- [ ] Inspect request payload schemas (Pydantic/TypeScript DTOs) against SDD contract schemas.
- [ ] Inspect database migration files (`alembic/versions/` or SQL scripts) and ORM models (`models.py`) against SDD database design.
- [ ] Verify status codes, enum values, and field nullability against SDD requirements.

### Axis 4: Deployment, Evaluation & Operational Inspection
- [ ] **Deployment Artifacts**:
  - Verify `Dockerfile` exists, builds cleanly, and uses appropriate multi-stage builds if specified.
  - Verify `Makefile` or build scripts contain standard target commands (`build`, `test`, `dev`, `deploy`).
  - Verify `README.md` contains clear setup instructions matching the actual environment setup.
- [ ] **Evaluation Assets & Test Harness**:
  - Verify test suites (`tests/` or `pytest`) exist and execute cleanly.
  - Verify benchmark scripts (e.g., `run_all_evals.py`) and evaluation datasets (`*.evalset.json`) specified in SDD exist and are valid JSON.
  - Verify evaluation documentation (e.g., `evaluation_report.md` or `tests/eval/`) matches SDD evaluation specifications.
- [ ] **Operational Controls**:
  - Verify `.env.example` exists with all required configuration environment variables.
  - Verify health check endpoints (`/health` or `/livez`) exist and return structured status.

---

## 3. Evidence Logging Format

When recording findings, format evidence using explicit line references:

```markdown
- **Finding**: [Description of drift]
  - **SDD Specification**: [Citation from SDD Section X.Y]
  - **Code Reality**: [Citation from file path and line number, e.g., app/routers/runs.py:L45-L60]
  - **Impact**: [High / Medium / Low]
```
