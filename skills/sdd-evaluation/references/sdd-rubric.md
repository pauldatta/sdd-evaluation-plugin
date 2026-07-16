# SDD Scoring Rubric

Six-dimension rubric for evaluating Software Design Documents. Each dimension is scored 1–5 with specific indicators at each level.

---

## Dimension 1: Problem Definition (Weight: 20%)

Evaluates how clearly and completely the document defines the problem being solved.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Problem is crisply defined with user impact quantified. Success criteria are specific, measurable, and time-bound. Target users are identified with personas or segments. The "why now" is compelling and evidence-backed. |
| 4 | **Strong** | Problem is well-defined with clear user impact. Success criteria exist and are measurable. Target users are identified. Minor gaps in quantification or timing justification. |
| 3 | **Adequate** | Problem is stated but somewhat vague. Success criteria exist but are not all measurable ("improve performance" without targets). Target users are mentioned but not characterized. |
| 2 | **Weak** | Problem statement is ambiguous or conflates problem with solution. Success criteria are missing or unmeasurable. Target users are assumed rather than identified. |
| 1 | **Missing** | No clear problem statement. The document jumps to the solution without explaining what problem it solves or who it's for. |

**Key questions to score this dimension:**
- Can you explain the problem to someone outside the team in one paragraph?
- Would you know if the problem was solved? What would you measure?
- Who specifically suffers from this problem today?

---

## Dimension 2: Architecture & Design (Weight: 25%)

Evaluates the technical solution design, component structure, and architectural thinking.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Architecture diagram with clear data flows. Components have defined responsibilities and interfaces. Trade-offs between alternatives are discussed with rationale. Technology choices are justified. Failure modes are identified. API contracts or schemas are defined. |
| 4 | **Strong** | Architecture is clearly described with a diagram. Components and their relationships are defined. At least one alternative approach is considered. Technology choices are stated with basic rationale. |
| 3 | **Adequate** | Architecture is described in text but may lack diagrams. Components are listed but interfaces between them are vague. Technology choices are stated without strong justification. No alternatives discussed. |
| 2 | **Weak** | Architecture section is a list of technologies ("we'll use React, Node, PostgreSQL") without explaining how they connect. No diagrams. No discussion of component boundaries or data flow. |
| 1 | **Missing** | No architecture section, or the section describes only the tech stack with no structural design. |

**Key questions to score this dimension:**
- Could an engineer implement this from the description without guessing about component boundaries?
- Does the document explain why this architecture over alternatives?
- Are data flows and API contracts defined or just assumed?

---

## Dimension 3: Non-Functional Requirements (Weight: 20%)

Evaluates coverage of security, scalability, reliability, performance, and cost considerations.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Security model defined (auth, authz, data protection). Scalability targets stated with projected load. Reliability requirements (SLOs, failover strategy). Performance budgets defined. Cost estimates or constraints documented. |
| 4 | **Strong** | Most NFR categories addressed with specific targets. Security considerations present. At least one of scalability/reliability/performance has measurable targets. |
| 3 | **Adequate** | Some NFRs mentioned but without specific targets ("should be fast", "needs to be secure"). Security is acknowledged but not detailed. Missing 2+ major NFR categories. |
| 2 | **Weak** | NFRs are a brief afterthought — one paragraph covering all concerns generically. No specific targets or strategies for any category. |
| 1 | **Missing** | No non-functional requirements section. The document implicitly assumes everything will be fast, secure, and scalable without discussion. |

**Key questions to score this dimension:**
- What happens if this system gets 10x the expected traffic?
- How is user data protected at rest and in transit?
- What is the target availability? What happens during an outage?

---

## Dimension 4: Risk Analysis (Weight: 15%)

Evaluates identification of risks, unknowns, dependencies, and mitigation strategies.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Risks are categorized (technical, operational, organizational). Each risk has likelihood, impact, and a mitigation or contingency plan. Dependencies on external systems or teams are explicitly called out. Known unknowns are listed with investigation plans. |
| 4 | **Strong** | Key risks are identified with mitigations. Dependencies are listed. Some risk prioritization. May be missing contingency plans for lower-priority risks. |
| 3 | **Adequate** | Risks are listed but mitigations are vague or missing for some. Dependencies mentioned but impact not assessed. No prioritization of risks by severity. |
| 2 | **Weak** | Risk section exists but is a generic list ("scope creep", "time constraints") with no project-specific analysis or mitigations. |
| 1 | **Missing** | No risk analysis. The document implies everything will go according to plan. |

**Key questions to score this dimension:**
- What could go wrong technically that would require a design change?
- What external dependencies could block or delay this project?
- What does the team not yet know, and how will they find out?

---

## Dimension 5: Feasibility & Planning (Weight: 10%)

Evaluates whether the proposed solution can actually be built with the available resources and timeline.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Implementation plan with phases and milestones. Resource needs identified. Timeline is realistic with buffer. Dependencies ordered logically. Clear definition of MVP vs. full scope. Validation or proof-of-concept plan included. |
| 4 | **Strong** | Implementation phases defined. Timeline exists and seems realistic. MVP scope identified. Resource needs mentioned. |
| 3 | **Adequate** | Some implementation ordering exists but timeline is vague or missing. MVP not clearly distinguished from full scope. Resource needs assumed rather than stated. |
| 2 | **Weak** | A brief "implementation plan" that is essentially "build it" without phases, ordering, or timeline. |
| 1 | **Missing** | No implementation plan, timeline, or discussion of feasibility. |

**Key questions to score this dimension:**
- Could a team start working tomorrow with this plan? What would they build first?
- Is the timeline realistic given the team size and complexity?
- What is the MVP that proves the concept vs. the full vision?

---

## Dimension 6: Clarity & Communication (Weight: 10%)

Evaluates the quality of the document as a communication artifact — readability, diagrams, and terminology consistency.

| Score | Level | Indicators |
|-------|-------|------------|
| 5 | **Exceptional** | Clear, concise writing. Diagrams supplement text effectively. Terminology is consistent and defined where non-obvious. The document tells a coherent story from problem to solution. A reader unfamiliar with the project could follow it. |
| 4 | **Strong** | Well-written and organized. At least one diagram. Terminology is mostly consistent. Minor areas could be clearer. |
| 3 | **Adequate** | Readable but verbose or disorganized in places. No diagrams or diagrams don't match the text. Some undefined jargon or inconsistent terminology. |
| 2 | **Weak** | Hard to follow. Sections seem out of order or disconnected. Heavy jargon without definitions. No visual aids. |
| 1 | **Missing** | Poorly written, disorganized, or so brief that it communicates almost nothing. |

**Key questions to score this dimension:**
- Could a new team member understand this document without a walkthrough?
- Do the diagrams match what the text describes?
- Is the same concept referred to by the same name throughout?

---

## Calculating the Weighted Score

```
Weighted Score = (Problem × 0.20) + (Architecture × 0.25) + (NFRs × 0.20)
               + (Risks × 0.15) + (Feasibility × 0.10) + (Clarity × 0.10)
```

Map to verdict:
- **4.5 – 5.0** → STRONG PASS
- **3.5 – 4.4** → PASS
- **2.5 – 3.4** → CONDITIONAL
- **1.5 – 2.4** → NEEDS WORK
- **1.0 – 1.4** → INSUFFICIENT
