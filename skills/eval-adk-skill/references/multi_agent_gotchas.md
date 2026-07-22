# Multi-Agent Systems (MAS) Evaluation Gotchas & Rubrics

Evaluating Multi-Agent Systems (MAS) introduces failure modes that never occur in single-agent architectures. This cheatsheet outlines the 4 critical MAS failure categories and the rubric dimensions required to evaluate them.

---

## 🚨 The 4 Critical MAS Failure Modes

### 1. Delegation Ping-Pong & Routing Loops
- **The Failure:** The Orchestrator routes a query to Subagent A, Subagent A determines it lacks tools and routes back to Orchestrator or Subagent B, creating an infinite or token-expensive routing cycle.
- **Eval Detection:** Capture conversation trajectory turn length. Any query taking $> 4$ internal agent-to-agent hops for a simple lookup is penalized on `delegation`.

### 2. Role Drift & Privilege Escalation
- **The Failure:** A subagent specialized in *HR Information* attempts to execute SQL database updates or calculate payroll tax deductions instead of delegating to `payroll_agent`.
- **Eval Detection:** Inspect tool call traces per agent ID. Ensure each subagent only invokes tools registered under its authorized schema.

### 3. Conflicting Cross-Agent Advice
- **The Failure:** `leave_agent` says "45 days unpaid leave is approved", while `compliance_agent` says "leaves >30 days are prohibited without VP sign-off". The Orchestrator presents both without resolving the conflict.
- **Eval Detection:** Score `reasoning` and `consensus` dimensions. The final synthesized output must present a unified, coherent response resolving internal policy conflicts.

### 4. Parametric Answering without Tool Grounding
- **The Failure:** A subagent answers from pre-trained weights without querying its retrieval tool (e.g. `read_concept` or `search_db`), causing stale data delivery.
- **Eval Detection:** The **Grounding Zero Cap Gate** enforces that any claim missing from `RETRIEVED EVIDENCE` caps the case score at $40\%$ max.

---

## 📊 MAS Rubric Dimensions Cheatsheet

| Dimension | Scale | 0 Points | 1 Point | 2 Points |
| :--- | :---: | :--- | :--- | :--- |
| **`delegation`** | 0, 1, 2 | Routed to the wrong subagent or entered a loop. | Correct subagent invoked after unnecessary intermediate hops. | Optimal, direct delegation to the exact specialist agent. |
| **`grounding`** | 0, 1, 2 | Claims made without underlying tool evidence trace. | Minor extrapolation beyond retrieved evidence. | 100% faithful to tool call return payloads. |
| **`correctness`** | 0, 1, 2 | Factually wrong or missed sub-questions. | Partially correct; missed cross-agent dependency. | Fully accurate across all sub-questions and agents. |
| **`reasoning`** | 0, 1, 2 | Fell for gotcha / conflicting advice. | Noted exception but reached ambiguous conclusion. | Clearly navigated cross-agent overrides and calculations. |
| **`abstention`** | 0, 1, 2 | Hallucinated a process or answered out-of-domain. | Vague or hesitant refusal. | Polite, definitive refusal stating exact system scope. |
| **`citation`** | 0, 1, 2 | Missing or hallucinated citations. | Cites document title but wrong section number. | Exact section numbers and handling subagent names cited. |
