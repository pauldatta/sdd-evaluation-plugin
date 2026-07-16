---
name: sdd-evaluation
description: >-
  Evaluates a Software Design Document (SDD) for completeness, technical rigor,
  and implementation readiness. Produces a scored rubric across 6 dimensions with
  specific improvement suggestions. Use when a team submits a design doc for
  review, when judging hackathon design documents, or when a team wants to
  self-assess their design before implementation. Also use when asked to review,
  score, grade, or evaluate any design document, technical spec, or architecture
  proposal. Accepts local Markdown/text files or pasted content as input.
---

# SDD Evaluation

## How to Invoke

Users can trigger this skill by:

- **Slash command:** `/sdd-evaluate` (Antigravity, Gemini CLI, Claude Code)
- **Natural language:** "Evaluate my SDD", "Score this design doc", "Grade my architecture proposal", "Review the design document at [URL/path]"
- **Auto-activation keywords:** The skill auto-activates when the agent sees any combination of ("evaluate", "score", "grade", "review", "assess") + ("SDD", "design doc", "design document", "architecture proposal", "technical spec")

**Input:** The user provides the SDD as one of:

| Input Type | Example | How to Read |
|---|---|---|
| Local file path | `docs/sdd.md` or `./design.md` | Read the file from the workspace |
| Pasted content | (user pastes the full document) | Use the pasted text directly |

If the user says "evaluate my SDD" without providing a source, ask:
> "Where is your SDD? Share a file path in your repo or paste the content directly."

## Overview

Score a Software Design Document across six dimensions and produce actionable improvement suggestions. The evaluation produces a structured verdict — not vague commentary. Every finding cites the specific section of the document that drives it.

This skill is designed for two audiences:
1. **Judges and reviewers** evaluating hackathon submissions or architecture proposals
2. **Authoring teams** who want to self-assess their design before committing engineering hours

## When to Use

- A team submits a design document for review or judging
- You need to score and rank multiple design documents
- A team asks "is our design doc ready for implementation?"
- Before a design review meeting to prepare structured feedback
- When evaluating hackathon submissions that include technical specifications

**When NOT to use:** Evaluating code (use `code-quality-evaluation` instead), reviewing a one-page RFC or brief proposal (apply lighter-weight feedback), or generating a design doc from scratch (use a spec-driven-development workflow instead).

## The Evaluation Workflow

The evaluation has four phases. Complete each phase fully before advancing.

```
ACQUIRE ──→ INTAKE ──→ STRUCTURAL SCAN ──→ DEEP ANALYSIS ──→ VERDICT
  │            │              │                    │               │
  ▼            ▼              ▼                    ▼               ▼
Get the      Identify       Check for           Score each       Produce
document     context        missing             dimension        the final
             & audience     sections            1–5              report
```

### Phase 0: Document Acquisition

Get the full document content before anything else.

1. **Determine the source.** Check what the user provided — a local file path or pasted text.
2. **Read the document.**
   - **Local file:** Read the file from the workspace. Parse `mermaid` fenced code blocks as architecture diagrams. Resolve `![alt](path)` image references and view images when possible.
   - **Pasted content:** Use it directly.
3. **Handle images and diagrams.**
   - **Mermaid code blocks** in Markdown count as architecture diagrams. Evaluate their content for Dimension 2 (Architecture & Design) and Dimension 6 (Clarity & Communication).
   - **Inline images in Markdown** (`![diagram](path)`) — resolve and view the image file. Factor it into the architecture and clarity scores.
4. **Verify completeness.** Confirm you have the full document — not a summary, partial draft, or truncated paste. If the document is split across multiple files, gather all parts.

### Phase 1: Intake

Establish context before evaluating.

1. **Identify the document.** Confirm the title, author, and any metadata present.
2. **Identify the context.** What is this document for? A hackathon project? A production system? A proof of concept? Context calibrates expectations — a hackathon SDD won't have the same depth as a production system design.
3. **Identify the audience.** Who will read this document? Engineers implementing it? Executives approving budget? Other teams integrating with it? This affects what "complete" means.
4. **Surface your assumptions.** Before proceeding, list any assumptions you're making about scope, maturity, or constraints.

```
INTAKE SUMMARY:
- Document: [title/filename]
- Source: [local file / pasted]
- Context: [hackathon / production / PoC / migration]
- Audience: [implementing team / reviewers / leadership]
- Diagrams found: [yes — N diagrams / no]
- Assumptions: [list]
→ Proceeding with evaluation. Correct me if any of the above is wrong.
```

### Phase 2: Structural Scan

Compare the document against the canonical SDD template in `references/sdd-template.md`.

1. **Check for missing sections.** Flag every section from the template that is absent or empty. Missing sections are findings — do not assume the author "probably thought about it."
2. **Check for placeholder content.** Sections that contain only "TBD", "TODO", or "to be determined" count as missing.
3. **Check for structural coherence.** Does the document flow logically? Are sections in a sensible order? Is there a clear narrative from problem to solution?

Produce a gap analysis:

```
STRUCTURAL SCAN:
✅ Present: [list of sections found]
❌ Missing: [list of sections absent]
⚠️  Placeholder: [list of sections with TBD/TODO content]
📊 Diagrams: [list of diagrams found — mermaid blocks, embedded images, etc.]
📋 Coherence: [assessment of document flow]
```

### Phase 3: Deep Analysis

Score the document across the six dimensions defined in `references/sdd-rubric.md`. For each dimension:

1. **Read the rubric.** Load `references/sdd-rubric.md` and apply the specific indicators for each score level.
2. **Cite evidence.** Every score must reference the specific section(s) of the document that justify it. "The Architecture section scores 3/5 because it describes components but lacks a data flow diagram and doesn't address failure modes" — not "Architecture seems adequate."
3. **Factor in diagrams.** Mermaid diagrams, embedded images, and architecture visuals contribute to Dimension 2 (Architecture & Design) and Dimension 6 (Clarity & Communication). Their absence is a finding.
4. **Provide suggestions.** For any dimension scoring below 4, provide specific, actionable suggestions for improvement. What would the author need to add, change, or clarify to raise the score?

**The six dimensions:**

| # | Dimension | Weight | What It Measures |
|---|-----------|--------|-----------------|
| 1 | Problem Definition | 20% | Clarity of the problem, user impact, success criteria |
| 2 | Architecture & Design | 25% | Solution structure, component design, data flow, trade-offs, **diagrams** |
| 3 | Non-Functional Requirements | 20% | Security, scalability, reliability, performance, cost |
| 4 | Risk Analysis | 15% | Identified risks, mitigations, dependencies, unknowns |
| 5 | Feasibility & Planning | 10% | Implementation plan, timeline, resource needs, milestones |
| 6 | Clarity & Communication | 10% | Writing quality, **diagrams**, consistent terminology |

### Phase 4: Verdict

Produce the final evaluation as a JSON object matching this structure:

```json
{
  "summary": "2-3 sentence overall assessment",
  "source": "local file path / pasted content",
  "context": "hackathon / production / PoC",
  "dimensions": [
    {
      "name": "Problem Definition",
      "score": 4,
      "weight": 0.20,
      "evidence": "The doc clearly defines...",
      "gaps": ["No quantified user impact", "Missing success metrics timeline"]
    }
    // ... other dimensions: Architecture & Design, Non-Functional Reqs, Risk Analysis, Feasibility & Planning, Clarity & Communication
  ],
  "weighted_score": 3.85,
  "verdict": "PASS",
  "top_recommendations": [
    "Add measurable success criteria with target dates",
    "Include an architecture diagram showing data flows"
  ],
  "red_flags": ["No alternatives considered for database choice"],
  "missing_sections": ["Risk Register", "Data Model"],
  "diagrams_found": ["1 Mermaid flowchart in Architecture section"],
  "whats_done_well": [
    "Problem statement is crisp with quantified user impact",
    "Clear implementation phases with dependencies mapped"
  ]
}
```

**Verdict thresholds:**

| Verdict | Weighted Score | Meaning |
|---------|---------------|---------|
| STRONG PASS | 4.5 – 5.0 | Exceptional — ready for implementation with minor polish |
| PASS | 3.5 – 4.4 | Solid — ready for implementation with noted improvements |
| CONDITIONAL | 2.5 – 3.4 | Needs targeted improvements before implementation |
| NEEDS WORK | 1.5 – 2.4 | Significant gaps — major revision required |
| INSUFFICIENT | 1.0 – 1.4 | Fundamental rethinking needed — not ready for review |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's just a hackathon, the design doc doesn't need to be thorough" | A hackathon design doc doesn't need production depth, but it must still clearly define the problem and proposed solution. Sloppy thinking in the doc means sloppy implementation. |
| "The team knows the context — they don't need to write it down" | If the judge or reviewer can't understand the doc without the team explaining it, the doc failed. Write for the reader, not for yourself. |
| "We'll figure out the architecture as we code" | That's not a plan, that's hope. Even a rough architecture section with known unknowns is better than silence. |
| "NFRs don't matter for a prototype" | Security, basic error handling, and scalability thinking matter at every stage. A prototype that ignores these teaches nothing about whether the real thing would work. |
| "The doc is long enough, it must be thorough" | Length is not depth. A 20-page doc that doesn't address failure modes or data flows is less useful than a 5-page doc that does. |
| "We listed the risks — isn't that enough?" | Listing risks without mitigations is a worry list, not risk analysis. Every risk needs a response strategy. |
| "The diagrams are in our heads" | If it's not on paper, it's not in the doc. Undrawn diagrams are invisible to reviewers and future team members. |

## Red Flags

- The problem statement describes the solution instead of the problem
- Architecture section is a list of technologies with no explanation of how they connect
- No data model, schema, or API contract defined anywhere in the doc
- The doc uses "we'll handle that later" for security, auth, or error handling
- Success criteria are unmeasurable ("make it fast", "good UX", "scalable")
- Diagrams contradict the text description
- No mention of how the system fails or recovers
- The doc doesn't mention a single trade-off or alternative considered
- Risk section is absent or contains only "low risk"
- The implementation plan has no milestones or ordering

## Verification

Before submitting your evaluation:

- [ ] Document was fully acquired and read (not truncated or partial)
- [ ] All six dimensions have been scored with cited evidence
- [ ] Every score below 4 has at least one specific improvement suggestion
- [ ] The verdict matches the weighted score threshold
- [ ] Critical findings are genuinely critical (not inflated nits)
- [ ] "What's Done Well" contains at least two specific, honest observations
- [ ] The improvement roadmap is ordered by impact, not by section order
- [ ] The report uses the structured template from Phase 4
- [ ] No placeholder or TODO content remains in the evaluation
- [ ] Diagrams (Mermaid, images) were factored into Architecture & Clarity scores
