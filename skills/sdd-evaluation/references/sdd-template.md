# Canonical SDD Template

Use this template as the reference standard when performing gap analysis in Phase 2 (Structural Scan) of the SDD evaluation. Every section listed here is expected in a complete Software Design Document. Missing sections are findings — not assumptions that the author "probably thought about it."

> **Context calibration:** Not every project needs every section at the same depth. A hackathon SDD may have a lightweight Risk Register. A production system design should have all sections fully populated. The evaluator should note missing sections and assess whether the omission is reasonable given the context.

---

## Template Sections

### 1. Title & Metadata

```markdown
# [Project/Feature Name] — Software Design Document

- **Author(s):** [names]
- **Date:** [creation date]
- **Status:** [Draft / In Review / Approved / Superseded]
- **Reviewers:** [names]
- **Last Updated:** [date]
```

**Why it matters:** Metadata establishes ownership, currency, and review status. A doc without an author or date is an orphan — nobody is accountable for its accuracy.

---

### 2. Problem Statement

```markdown
## Problem Statement

### What problem are we solving?
[Clear, specific description of the problem]

### Who is affected?
[Target users, personas, or user segments]

### What is the impact?
[Quantified impact — user pain, business cost, operational burden]

### Why now?
[What makes this problem urgent or timely]
```

**Why it matters:** The problem statement is the foundation. If the problem isn't clear, the solution is guessing.

---

### 3. Context & Constraints

```markdown
## Context & Constraints

### Current State
[How does the system/process work today? What exists already?]

### Constraints
[Technical constraints, organizational constraints, timeline, budget, team size]

### Assumptions
[Explicit assumptions the design relies on — surfaced, not hidden]

### Out of Scope
[What this design explicitly does NOT address]
```

**Why it matters:** Constraints and assumptions prevent scope creep and surface misunderstandings early. Out-of-scope is as important as in-scope.

---

### 4. Proposed Solution

```markdown
## Proposed Solution

### Overview
[High-level description of the proposed approach — 2-3 paragraphs max]

### Alternatives Considered
| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Option A]  | ...  | ...  | ...            |
| [Option B]  | ...  | ...  | ...            |

### Key Design Decisions
[Decisions made and the rationale behind them]
```

**Why it matters:** Alternatives considered demonstrate engineering judgment. A design that didn't evaluate options is a design that got lucky.

---

### 5. Architecture

```markdown
## Architecture

### System Architecture Diagram
[Diagram showing components, data flows, and external integrations]

### Component Descriptions
| Component | Responsibility | Technology | Interfaces |
|-----------|---------------|------------|------------|
| [Name]    | [What it does] | [Tech]    | [APIs/protocols] |

### Data Flow
[How data moves through the system — from input to output]

### Integration Points
[External systems, APIs, services this design depends on or exposes]
```

**Why it matters:** The architecture section turns an idea into an implementable blueprint. Without it, engineers will design the architecture themselves — differently, and probably inconsistently.

---

### 6. Data Model

```markdown
## Data Model

### Entity Definitions
[Key entities, their attributes, and relationships]

### Schema
[Database schema, data structures, or storage format]

### Data Lifecycle
[How data is created, read, updated, deleted, and archived]

### Data Privacy
[PII handling, data retention, encryption at rest/in transit]
```

**Why it matters:** Data models are the hardest thing to change after implementation starts. Getting them right in the design phase saves weeks of migration pain.

---

### 7. API Contracts

```markdown
## API Contracts

### Endpoints / Interfaces
| Method | Endpoint | Request | Response | Auth |
|--------|----------|---------|----------|------|
| POST   | /api/v1/... | {...} | {...}  | Bearer |

### Error Handling
[Error response format, status codes, error categories]

### Versioning Strategy
[How API versions are managed]
```

**Why it matters:** API contracts are the agreement between teams. Undefined APIs lead to integration surprises.

---

### 8. Non-Functional Requirements

```markdown
## Non-Functional Requirements

### Security
[Authentication, authorization, data protection, threat model]

### Scalability
[Expected load, scaling strategy, capacity limits]

### Reliability
[Availability target, failover strategy, backup/recovery]

### Performance
[Latency targets, throughput requirements, performance budget]

### Cost
[Infrastructure cost estimates, scaling cost model]
```

**Why it matters:** NFRs determine whether the system works in the real world — not just on a developer's laptop.

---

### 9. Risk Register

```markdown
## Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| [Description] | High/Med/Low | High/Med/Low | [Strategy] | [Person] |

### Known Unknowns
[Things the team doesn't know yet, with a plan to find out]

### Dependencies
[External dependencies with risk assessment]
```

**Why it matters:** Risk without mitigation is worry. Mitigation without ownership is hope. Neither ships software.

---

### 10. Implementation Plan

```markdown
## Implementation Plan

### Phases / Milestones
| Phase | Deliverable | Timeline | Dependencies |
|-------|-------------|----------|-------------|
| 1     | [MVP / Foundation] | [dates] | [none / Phase 0] |
| 2     | [Feature X] | [dates] | [Phase 1] |

### Resource Needs
[Team size, skills needed, infrastructure needs]

### Validation Plan
[How the team will verify the implementation matches the design]
```

**Why it matters:** A design without an implementation plan is an essay, not an engineering document.

---

### 11. Success Metrics

```markdown
## Success Metrics

| Metric | Target | Measurement Method | Timeline |
|--------|--------|-------------------|----------|
| [What to measure] | [Specific target] | [How to measure it] | [When to measure] |
```

**Why it matters:** If you can't measure success, you can't know if you achieved it.

---

### 12. Open Questions

```markdown
## Open Questions

- [ ] [Question 1 — what needs to be resolved and by whom]
- [ ] [Question 2]
```

**Why it matters:** Open questions are honest. A document with no open questions either solved everything (unlikely) or hid the gaps (likely).

---

## Using This Template for Gap Analysis

When scanning a submitted SDD:

1. Check each section header above against the submitted document
2. Mark each as: ✅ Present | ❌ Missing | ⚠️ Placeholder (TBD/TODO)
3. Sections that are present but lack the depth described above should be noted in the Deep Analysis phase
4. Context-adjust: not every section needs production depth for a hackathon project, but every section should at least be acknowledged
