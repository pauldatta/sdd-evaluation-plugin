---
name: eval-adk-skill
description: >-
  Generates, scaffolds, validates, and runs 4-Tier Stratified golden evaluation
  datasets (*.evalset.json), test configs (eval_config.json), and comprehensive
  evaluation reports for Single-Agent and Multi-Agent Systems (MAS) built on Google ADK.
---

# Eval ADK Skill: 4-Tier Golden Evalset Engineering & Evaluation for Multi-Agent Systems

This skill provides recipes, schemas, scripts, and evaluation runners for authoring enterprise-grade **Golden Evaluation Datasets (`*.evalset.json`)**, **Evaluation Configurations (`eval_config.json`)**, and generating final **Evaluation Reports** for Multi-Agent Systems (MAS) built on Google Agent Development Kit (ADK) and Vertex AI.

Sample reference datasets and configurations are available in [references/rag_eval_golden.evalset.json](file:///Users/anhduc/API/others/evaluation-plugins/skills/eval-adk-skill/references/rag_eval_golden.evalset.json) and [references/eval_config.json](file:///Users/anhduc/API/others/evaluation-plugins/skills/eval-adk-skill/references/eval_config.json).

---

## 🎯 Quick Start Workflow

### 1. Generate a 4-Tier Stratified Golden Evalset & Config
To scaffold a new `*.evalset.json` dataset following the 4-Tier Stratification Recipe and referencing the sample golden seed dataset:

```bash
uv run python skills/eval-adk-skill/scripts/generate_evalset.py \
  --output evals/golden/golden_mas_eval.evalset.json \
  --seed skills/eval-adk-skill/references/rag_eval_golden.evalset.json \
  --config skills/eval-adk-skill/references/eval_config.json \
  --name "rag_eval_fixed" \
  --set-id "rag_eval_2"
```

### 2. Validate Evalset Balance & Schema Integrity
To verify Google ADK schema compliance and check 4-tier stratification percentages:

```bash
uv run python skills/eval-adk-skill/scripts/validate_evalset.py \
  --file skills/eval-adk-skill/references/rag_eval_golden.evalset.json
```

### 3. Run Evaluation & Export Final Markdown Report
To execute the evaluation against the MAS root agent and produce the final report:

```bash
uv run python evals/golden/export_eval_report.py \
  --agent_module backend.hr_agents \
  --evalset skills/eval-adk-skill/references/rag_eval_golden.evalset.json \
  --config skills/eval-adk-skill/references/eval_config.json \
  --output evals/golden/eval_results_report.md
```

---

## 🏗️ 4-Tier Stratification Recipe for Multi-Agent Evalsets

Never build an evaluation dataset with only direct factual lookups. Follow the **4-Tier Enterprise Stratification Distribution**:

```mermaid
pie title Multi-Agent Golden Evalset Stratification
    "Happy Path / Direct Lookup (40%)" : 40
    "MAS Gotchas & Routing Traps (30%)" : 30
    "Hallucination Baits / Absent Policies (15%)" : 15
    "Out-of-Scope / Boundary Probes (15%)" : 15
```

1. **Happy Path / Direct Factual Lookups (40%):** Standard single-agent and multi-agent queries testing clean routing, factual retrieval, and policy lookups across `rag_agent`, `workweek_agent`, and `service_immediately_agent`.
   - *Example 1 (`sick_leave_policy`):* Inquiring about paid outpatient sick leave (14 days entitlement) and medical certificate submission deadline (within 48 hours for >2 days absence).
   - *Example 2 (`vacation_accrual_and_shift`):* Vacation entitlement for 8 years tenure (21 days annual accrual) and shift logging requirement for 12-hour shifts (1.5 vacation days).
   - *Example 3 (`ramp_back_time_policy`):* Working hour minimums (50% normal hours) and pay requirements (100% normal salary) during 2-week Ramp-Back time.
2. **MAS Gotchas & Routing Traps (30%):** Complex multi-hop queries requiring cross-agent sequential planning, priority anti-inflation overrides, transactional rollbacks, or categorical prohibition overrides.
   - *Example 1 (`expense_gift_card_violation` - Prohibition Override):* Inquiring about expensing a $45 gift card for a host family. While host gifts under $50 are permitted, gift cards and cash are strictly prohibited.
   - *Example 2 (`ethics_room_salon_violation` - Prohibition Override):* $80 room salon client entertainment is strictly prohibited regardless of being under the $100 manager approval threshold.
   - *Example 3 (Cross-Agent Sequential Planning):* Remote home office equipment request requires checking policy (`rag_agent`), extracting verified shipping address (`workweek_agent`), and opening a Facilities delivery ticket in ServiceImmediately (`service_immediately_agent`).
   - *Example 4 (Priority Anti-Inflation Guardrail):* Routine password reset submitted with priority `'1 - Critical'` is automatically intercepted and downgraded to `'4 - Low'`.
3. **Hallucination Baits / Absent Policies (15%):** Plausible-sounding queries on ungrounded topics not present in any policy document (e.g., pet helicopter transport, crypto meal stipends, subsidized luxury yacht rentals). Verifies that agents query RAG and cleanly state that no such policy exists rather than fabricating rules.
4. **Out-of-Scope / Boundary Probes (15%):** Off-topic requests (e.g., Python coding, geopolitical commentary, stock trading advice). Verifies that the root orchestrator immediately refuses without invoking specialist subagents (`tool_uses: []`).

---

## 📋 Google ADK Native `*.evalset.json` Schema

Every test case in a Google ADK evaluation dataset follows the native format exemplified in [references/rag_eval_golden.evalset.json](file:///Users/anhduc/API/others/evaluation-plugins/skills/eval-adk-skill/references/rag_eval_golden.evalset.json):

```json
{
  "eval_set_id": "rag_eval_2",
  "name": "rag_eval_fixed",
  "description": "Evaluation suite for the HR agent covering simple and complex policy Q&A, ethics, leave operations, and adversarial testing based on the Altostrat Singapore Employee Policy Handbook.",
  "eval_cases": [
    {
      "eval_id": "sick_leave_policy",
      "session_input": {
        "app_name": "hr_agents",
        "user_id": "EMP-4",
        "state": {}
      },
      "conversation": [
        {
          "invocation_id": "turn_1_sick_leave",
          "user_content": {
            "role": "user",
            "parts": [
              {
                "text": "How many days of paid outpatient sick leave do I get per year, and what is the deadline to submit a Medical Certificate if I'm out sick for 3 days?"
              }
            ]
          },
          "final_response": {
            "role": "model",
            "parts": [
              {
                "text": "Based on Altostrat's HR policies, here is the information regarding your sick leave:\n\n* **Paid Outpatient Sick Leave:** You are entitled to up to **14 days** of paid outpatient sick leave per calendar year, compensated at 100% of your base salary.\n* **Medical Certificate (MC) Deadline:** Since your sick leave exceeds two workdays (3 days), you are required to submit a medical certificate from a registered medical practitioner. The deadline to submit this certificate is within **48 hours** of taking the leave. Please note that if the certificate is not submitted on time, the company reserves the right to decline paid sick leave or classify the absence as unpaid leave.\n\n**Sources:**\n* [Altostrat Singapore Employee Policy Handbook - Section 1.1 Outpatient Sick Time & Hospitalization Leave](gs://aiproject-429506-hr-policies-source/ALTOSTRAT SINGAPORE EMPLOYEE POLICY HANDBOOK & CONDUCT GUIDELINES v2.pdf)\n* [Altostrat Singapore Employee Policy Handbook - Section 19.4 Notification and Medical Certificates (MC)](gs://aiproject-429506-hr-policies-source/ALTOSTRAT SINGAPORE EMPLOYEE POLICY HANDBOOK & CONDUCT GUIDELINES.pdf)\n\nPlease let me know if you would like me to check your current sick leave balance or help you submit a sick leave request in the system!"
              }
            ]
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "rag_agent",
                "args": {
                  "request": "How many days of paid outpatient sick leave are employees entitled to per year, and what is the deadline to submit a Medical Certificate if out sick for 3 days?"
                }
              }
            ],
            "intermediate_responses": []
          }
        }
      ]
    }
  ]
}
```

---

## ⚙️ Evaluation Config (`eval_config.json`)

Quantitative thresholds for ADK evaluation defined in [references/eval_config.json](file:///Users/anhduc/API/others/evaluation-plugins/skills/eval-adk-skill/references/eval_config.json):

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 0.8,
    "response_match_score": 0.8
  }
}
```

- **`tool_trajectory_avg_score`**: Measures whether the agent called the expected subagents and MCP tools in sequence.
- **`response_match_score`**: Evaluates semantic similarity between the model's final synthesized response and the ground truth.

---

## 🛡️ Execution & Reporting Harness

Run the evaluation and export a clean Markdown report for stakeholder review using `evals/golden/export_eval_report.py`.
