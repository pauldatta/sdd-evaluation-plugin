---
name: evaluation
description: Performs ADK Agent Evaluation.
---

# Agent Evaluation

You are the Orchestration Agent.

## Instructions
1. Run `bash scripts/preflight_check.sh` to verify credentials and ensure required GCP APIs are enabled.
2. You MUST read the `google-agents-cli-eval` skill first.
3. Ensure the golden dataset (`tests/eval/datasets/evalset.json` or `evals/evalset.json`) is placed in the agent's expected location.
4. Execute `uv sync && uvx google-agents-cli eval run` using bash.
5. Capture the console output and any generated evaluation report into `artifacts/docs/eval_report.md`. If the CLI fails, try to fix the schema of `evalset.json` based on the CLI error or `google-agents-cli-eval` skill schema.
6. Provide a summary of the scores in the artifact.


## Output
Produce `artifacts/docs/eval_report.md` with the evaluation summary and confirm it ran successfully.

**A2A Constraints:**
If A2A is required, you MUST write local startup scripts using `to_a2a(app, port=800X)` for all Sub-agents and spawn them in the background (e.g. `nohup uv run python ... &`) BEFORE executing `agents-cli eval run`. Terminate them after.
