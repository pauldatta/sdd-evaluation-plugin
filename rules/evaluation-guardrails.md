# SDD Evaluation Guardrails

These rules apply whenever the `sdd-evaluation` skill is active.

## Evidence-Based Scoring

- **Never fabricate content.** Every claim about the SDD must reference text that actually exists in the document. If you can't find it, the section is missing — that's a finding, not a guess.
- **Read the rubric before scoring.** Load `references/sdd-rubric.md` and apply the specific indicators for each score level. Do not score from memory or general impressions.
- **Cite the section.** Every dimension score must reference the specific section(s) of the document that justify it. "The Architecture section scores 3/5 because..." — not "Architecture seems adequate."
- **Score below 4 requires suggestions.** For any dimension scoring below 4, provide at least one specific, actionable improvement. What would the author need to add, change, or clarify?

## Document Acquisition

- **Ask before guessing the source.** If the user says "evaluate my SDD" but doesn't provide a file path or pasted content — ask. Do not assume the document is already in context.
- **Accept any source format.** The user may provide a local file path (`.md`, `.txt`, `.pdf`) or paste the content directly. Handle both.
- **Verify completeness.** Before starting evaluation, confirm you have the full document — not a summary, partial draft, or truncated paste.

## Diagram and Image Handling

- **Treat diagrams as evidence.** Mermaid code blocks and inline images in Markdown count as architecture diagrams for Dimension 2 and Dimension 6 scoring.
- **Describe what you observe.** When evaluating images or diagrams, describe what they depict and how they contribute to (or contradict) the text. Do not ignore visual content.
- **Missing diagrams are findings.** If the Architecture section has no diagrams of any kind, note it as a gap.

## Objectivity

- **Calibrate to context.** A hackathon SDD is graded differently from a production system design. State the context before scoring and adjust expectations — but never skip dimensions entirely.
- **Don't inflate nits to critical findings.** A minor formatting issue is not a red flag. Reserve red flags for genuine design gaps (no failure modes, no alternatives considered, no data model).
- **Acknowledge strengths.** The evaluation must include at least two specific, honest observations about what the document does well.
