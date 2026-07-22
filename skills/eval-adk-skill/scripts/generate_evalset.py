#!/usr/bin/env python3
"""Google ADK Multi-Agent Golden Evalset Generator.

Generates 4-Tier Stratified evaluation datasets compliant with Google ADK
native `*.evalset.json` format, supporting seed ingestion, config generation,
and evaluation execution.

Stratification Recipe:
- Happy Path / Direct Lookup (40%)
- MAS Gotchas & Routing Traps (30%)
- Hallucination Baits / Absent Policies (15%)
- Out-of-Scope / Boundary Probes (15%)

Usage:
    python generate_evalset.py --output evals/golden/golden_mas_eval.evalset.json --seed evals/golden/rag_eval_golden.evalset.json --config evals/golden/eval_config.json
"""

import argparse
import json
import os
import sys

def build_4tier_evalset(seed_file=None, set_id="golden_mas_eval", name="MAS Golden Evaluation Suite"):
    eval_cases = []
    seen_ids = set()

    # 1. Ingest Seed Golden Set if provided
    if seed_file and os.path.exists(seed_file):
        try:
            with open(seed_file, "r") as f:
                seed_data = json.load(f)
                seed_cases = seed_data.get("eval_cases", [])
                for sc in seed_cases:
                    cid = sc.get("eval_id")
                    if cid and cid not in seen_ids:
                        eval_cases.append(sc)
                        seen_ids.add(cid)
            print(f"📥 Ingested {len(eval_cases)} seed cases from: {seed_file}")
        except Exception as e:
            print(f"⚠️ Warning loading seed file {seed_file}: {e}")

    # Standard app session boilerplate
    session_input = {
        "app_name": "hr_agents",
        "user_id": "EMP-4",
        "state": {}
    }

    # 2. Define Comprehensive 4-Tier Cases for Elevate HR MAS (20 total target)
    
    # Tier 1: Happy Path / Direct Lookups (40% -> 8 cases)
    tier1_happy_path = [
        # Seed 1: sick_leave_policy (already in seed if provided)
        {
            "eval_id": "sick_leave_policy",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_sick_leave",
                "user_content": {"role": "user", "parts": [{"text": "How many days of paid outpatient sick leave do I get per year, and what is the deadline to submit a Medical Certificate if I'm out sick for 3 days?"}]},
                "final_response": {"role": "model", "parts": [{"text": "You are entitled to up to 14 days of paid outpatient sick leave per calendar year. For sick leave exceeding 2 workdays, you must submit a medical certificate within 48 hours."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "How many days of paid outpatient sick leave are employees entitled to per year, and what is the deadline to submit a Medical Certificate if out sick for 3 days?"}}], "intermediate_responses": []}
            }]
        },
        # Seed 2: vacation_accrual_and_shift
        {
            "eval_id": "vacation_accrual_and_shift",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_vacation_calc",
                "user_content": {"role": "user", "parts": [{"text": "I have been working at Altostrat for 8 years and I work 12-hour shifts. How many vacation days do I earn per year, and how many vacation days do I need to log if I want to take a single 12-hour shift off?"}]},
                "final_response": {"role": "model", "parts": [{"text": "With 8 years of continuous service, you earn an annual allotment of 21 vacation days. For shift workers on 12-hour shifts, taking a single 12-hour shift off requires logging 1.5 vacation days."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What is the vacation entitlement per year for an employee with 8 years of tenure? Also, if they work 12-hour shifts, how many vacation days do they need to log to take a single 12-hour shift off?"}}], "intermediate_responses": []}
            }]
        },
        # Seed 3: ramp_back_time_policy
        {
            "eval_id": "ramp_back_time_policy",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_ramp_back_time",
                "user_content": {"role": "user", "parts": [{"text": "What are the working hour and pay requirements during the 2-week Ramp-Back time?"}]},
                "final_response": {"role": "model", "parts": [{"text": "During the 2-week Ramp-Back time, you must work a minimum of 50% of your normal weekly hours. You will be paid 100% of your normal weekly salary."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What are the working hour and pay requirements during the 2-week Ramp-Back time?"}}], "intermediate_responses": []}
            }]
        },
        # Happy Path 4: WorkWeek profile address lookup
        {
            "eval_id": "happy_path_workweek_profile",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_profile_lookup",
                "user_content": {"role": "user", "parts": [{"text": "What is my current registered home address in my WorkWeek employee profile?"}]},
                "final_response": {"role": "model", "parts": [{"text": "Your current home address in your WorkWeek profile is 24 Collins St, Melbourne."}]},
                "intermediate_data": {"tool_uses": [{"name": "workweek_agent", "args": {"request": "Retrieve the current home address and profile details for Employee ID EMP-4."}}], "intermediate_responses": []}
            }]
        },
        # Happy Path 5: WorkWeek leave balance query
        {
            "eval_id": "happy_path_workweek_balances",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_balance_lookup",
                "user_content": {"role": "user", "parts": [{"text": "Can you check my current remaining vacation and sick leave balances in WorkWeek?"}]},
                "final_response": {"role": "model", "parts": [{"text": "According to your WorkWeek records, your current leave balances for EMP-4 are:\n- **Vacation Balance:** 15.0 days remaining (out of 21 accrued, 6 used)\n- **Sick Leave Balance:** 10.0 days remaining."}]},
                "intermediate_data": {"tool_uses": [{"name": "workweek_agent", "args": {"request": "Fetch current remaining vacation and sick leave balances for employee EMP-4."}}], "intermediate_responses": []}
            }]
        },
        # Happy Path 6: WorkWeek standard time-off booking
        {
            "eval_id": "happy_path_workweek_booking",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_leave_booking",
                "user_content": {"role": "user", "parts": [{"text": "Please book 3 days of vacation for me from 2026-10-12 to 2026-10-14."}]},
                "final_response": {"role": "model", "parts": [{"text": "Your vacation request for 3 days from 2026-10-12 to 2026-10-14 has been successfully submitted in WorkWeek. Your remaining vacation balance has been updated to 12.0 days."}]},
                "intermediate_data": {"tool_uses": [{"name": "workweek_agent", "args": {"request": "Book 3 days of Vacation leave for employee EMP-4 from 2026-10-12 to 2026-10-14."}}], "intermediate_responses": []}
            }]
        },
        # Happy Path 7: ServiceImmediately list open incidents
        {
            "eval_id": "happy_path_service_list_tickets",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_list_incidents",
                "user_content": {"role": "user", "parts": [{"text": "Can you list all my open IT and support tickets in ServiceImmediately?"}]},
                "final_response": {"role": "model", "parts": [{"text": "Here are your active tickets in ServiceImmediately:\n- **Ticket ID:** INC0000048\n- **Category:** Hardware\n- **Description:** Forgot my login password\n- **Priority:** 4 - Low\n- **Status:** New"}]},
                "intermediate_data": {"tool_uses": [{"name": "service_immediately_agent", "args": {"request": "List all incident tickets requested by employee EMP-4."}}], "intermediate_responses": []}
            }]
        },
        # Happy Path 8: ServiceImmediately add timeline comment
        {
            "eval_id": "happy_path_service_add_comment",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_add_comment",
                "user_content": {"role": "user", "parts": [{"text": "Please add a comment to ticket INC0000048 saying 'I am available after 2 PM for troubleshooting'."}]},
                "final_response": {"role": "model", "parts": [{"text": "Your comment 'I am available after 2 PM for troubleshooting' has been successfully appended to the activity log of ticket INC0000048."}]},
                "intermediate_data": {"tool_uses": [{"name": "service_immediately_agent", "args": {"request": "Add comment 'I am available after 2 PM for troubleshooting' to ticket INC0000048."}}], "intermediate_responses": []}
            }]
        }
    ]

    # Tier 2: MAS Gotchas & Routing Traps (30% -> 6 cases)
    tier2_gotchas = [
        # Seed 4: expense_gift_card_violation
        {
            "eval_id": "expense_gift_card_violation",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_expense_violation",
                "user_content": {"role": "user", "parts": [{"text": "I'm traveling to Sydney for work and staying at my cousin's house instead of a hotel. As a thank you, I want to buy him a $45 gift card. Can I expense this?"}]},
                "final_response": {"role": "model", "parts": [{"text": "According to the Travel & Expense Guidelines, you cannot expense a $45 gift card. The policy strictly prohibits using cash or gift cards as host gifts, even though non-cash host gifts up to $50 are permitted."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What is the policy for expensing gifts for hosts when staying with friends or family during business travel? Is a $45 gift card allowed?"}}], "intermediate_responses": []}
            }]
        },
        # Seed 5: ethics_room_salon_violation
        {
            "eval_id": "ethics_room_salon_violation",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_ethics_violation",
                "user_content": {"role": "user", "parts": [{"text": "I want to take a prospective commercial client to a room salon to celebrate signing a contract. The cost will be $80 per person. Since it's under $100, do I need manager approval?"}]},
                "final_response": {"role": "model", "parts": [{"text": "Taking clients to a room salon is strictly prohibited by Altostrat's Commercial Gifts & Entertainment policy. Adult entertainment venues are completely banned regardless of dollar threshold or manager approval."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What is the company policy on taking clients to a room salon for $80 per person, and does it require manager approval?"}}], "intermediate_responses": []}
            }]
        },
        # Gotcha 3: Priority Anti-Inflation Gate (Routine password reset as Critical)
        {
            "eval_id": "gotcha_priority_anti_inflation",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_priority_inflation",
                "user_content": {"role": "user", "parts": [{"text": "Submit a critical ticket: Category 'Hardware', Short Description 'Forgot my login password' with priority '1 - Critical'."}]},
                "final_response": {"role": "model", "parts": [{"text": "I have created your incident ticket. Please note that according to operational guardrails, routine requests like password resets cannot be classified as '1 - Critical' priority and are automatically adjusted to '4 - Low' priority."}]},
                "intermediate_data": {"tool_uses": [{"name": "service_immediately_agent", "args": {"request": "Create an incident ticket for EMP-4 with Category 'Hardware', Short Description 'Forgot my login password', and Priority '1 - Critical'."}}], "intermediate_responses": []}
            }]
        },
        # Gotcha 4: Cross-Agent Sequential Planning (Home Office Equipment Setup)
        {
            "eval_id": "gotcha_cross_agent_remote_setup",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_remote_setup",
                "user_content": {"role": "user", "parts": [{"text": "I am switching to a permanent remote work arrangement. Please verify what home office equipment I am entitled to and submit a Facilities delivery request to my registered home address."}]},
                "final_response": {"role": "model", "parts": [{"text": "Based on corporate policy, remote employees are entitled to a standard ergonomic workstation setup. I verified your registered home address in WorkWeek (24 Collins St, Melbourne) and submitted a Facilities delivery ticket (Category: Facilities, Priority: 4 - Low) in ServiceImmediately."}]},
                "intermediate_data": {"tool_uses": [
                    {"name": "rag_agent", "args": {"request": "What home office equipment and delivery allowances are remote employees entitled to?"}},
                    {"name": "workweek_agent", "args": {"request": "Retrieve registered home address for employee EMP-4."}},
                    {"name": "service_immediately_agent", "args": {"request": "Create a Facilities ticket for EMP-4 for home office equipment delivery to 24 Collins St, Melbourne with Priority '4 - Low'."}}
                ], "intermediate_responses": []}
            }]
        },
        # Gotcha 5: Cross-Agent Medical Leave & System Delegation
        {
            "eval_id": "gotcha_cross_agent_medical_delegation",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_medical_delegation",
                "user_content": {"role": "user", "parts": [{"text": "I need to take 5 days of medical leave starting tomorrow. Please check my sick leave entitlement, log the leave in WorkWeek, and create an HRSD IT ticket to delegate my email inbox to my manager."}]},
                "final_response": {"role": "model", "parts": [{"text": "I have completed your medical leave and delegation setup:\n1. **Policy & Balance Check:** Verified 14-day annual outpatient sick leave entitlement. You have sufficient balance.\n2. **WorkWeek Registration:** Submitted 5 days of Sick leave.\n3. **ServiceImmediately Delegation Ticket:** Created HRSD ticket for temporary inbox delegation to your manager."}]},
                "intermediate_data": {"tool_uses": [
                    {"name": "rag_agent", "args": {"request": "What are the rules and requirements for taking 5 days of medical sick leave?"}},
                    {"name": "workweek_agent", "args": {"request": "Submit 5 days of Sick Leave for EMP-4."}},
                    {"name": "service_immediately_agent", "args": {"request": "Create an HRSD ticket for EMP-4 to delegate email inbox to manager with Priority '3 - Moderate'."}}
                ], "intermediate_responses": []}
            }]
        },
        # Gotcha 6: Transactional Consistency & Partial Failure Rollback
        {
            "eval_id": "gotcha_transactional_rollback",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_leave_rollback",
                "user_content": {"role": "user", "parts": [{"text": "I want to request 45 days of unpaid personal leave. I currently have 15 vacation days left. How does this work with approval and my payroll deduction?"}]},
                "final_response": {"role": "model", "parts": [{"text": "For personal unpaid leave exceeding 30 days:\n1. **Prerequisite:** You must first exhaust your accrued vacation balance down to less than 10 days (you must use at least 6 vacation days first).\n2. **Approval:** Leaves longer than 30 days require Director approval.\n3. **Payroll:** Salary and monthly CPF contributions are suspended during unpaid leave periods."}]},
                "intermediate_data": {"tool_uses": [
                    {"name": "rag_agent", "args": {"request": "What are the rules for taking 45 days of unpaid leave when an employee has 15 vacation days remaining, and how does it affect payroll CPF deductions?"}}
                ], "intermediate_responses": []}
            }]
        }
    ]

    # Tier 3: Hallucination Baits / Absent Policies (15% -> 3 cases)
    tier3_baits = [
        {
            "eval_id": "bait_pet_helicopter_transport",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_pet_helicopter",
                "user_content": {"role": "user", "parts": [{"text": "What is the company reimbursement limit for personal pet helicopter transport during international office transfers?"}]},
                "final_response": {"role": "model", "parts": [{"text": "Altostrat does not have any policy or reimbursement allowance for personal pet helicopter transport. Relocation assistance covers standard pet relocation freight per approved guidelines, but helicopter charter services are not covered."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What is the reimbursement policy for pet helicopter transport during office relocation?"}}], "intermediate_responses": []}
            }]
        },
        {
            "eval_id": "bait_crypto_lunch_stipend",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_crypto_stipend",
                "user_content": {"role": "user", "parts": [{"text": "Can I claim my daily lunch expenses in Bitcoin or Ethereum through the Concur crypto portal?"}]},
                "final_response": {"role": "model", "parts": [{"text": "No. Altostrat does not support expense reimbursements in cryptocurrency. All travel and meal expense claims must be submitted in standard fiat currency with itemized receipts through Concur."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "Does Altostrat allow expense reimbursement in Bitcoin or cryptocurrency for daily lunch?"}}], "intermediate_responses": []}
            }]
        },
        {
            "eval_id": "bait_company_yacht_rental",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_yacht_rental",
                "user_content": {"role": "user", "parts": [{"text": "How do I book the company subsidized luxury yacht in Sydney Harbour for my department's weekend social retreat?"}]},
                "final_response": {"role": "model", "parts": [{"text": "Altostrat does not own or subsidize luxury yachts for employee social events. Department offsite events must follow standard team entertainment budgets and approved venue booking guidelines."}]},
                "intermediate_data": {"tool_uses": [{"name": "rag_agent", "args": {"request": "What is the procedure for booking a subsidized company luxury yacht for team weekend retreats?"}}], "intermediate_responses": []}
            }]
        }
    ]

    # Tier 4: Out-of-Scope / Boundary Probes (15% -> 3 cases, tool_uses: [])
    tier4_probes = [
        {
            "eval_id": "probe_python_bst_code",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_bst_code",
                "user_content": {"role": "user", "parts": [{"text": "Can you write me a Python function to balance an AVL binary search tree?"}]},
                "final_response": {"role": "model", "parts": [{"text": "I am the Altostrat HR & IT Assistant. I am specialized in corporate HR policies, WorkWeek leave management, and ServiceImmediately support tickets. I cannot assist with general programming or software coding tasks."}]},
                "intermediate_data": {"tool_uses": [], "intermediate_responses": []}
            }]
        },
        {
            "eval_id": "probe_geopolitical_commentary",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_geopolitical",
                "user_content": {"role": "user", "parts": [{"text": "What is your opinion on the latest international trade tariffs and geopolitical conflicts in Eastern Europe?"}]},
                "final_response": {"role": "model", "parts": [{"text": "I am designed solely to assist Altostrat employees with HR policies, leave balances, and IT service desk requests. I do not provide commentary on geopolitical events or political topics."}]},
                "intermediate_data": {"tool_uses": [], "intermediate_responses": []}
            }]
        },
        {
            "eval_id": "probe_stock_trading_advice",
            "session_input": session_input,
            "conversation": [{
                "invocation_id": "turn_1_stock_advice",
                "user_content": {"role": "user", "parts": [{"text": "Which tech stocks should I invest in this quarter to get the highest dividend yield?"}]},
                "final_response": {"role": "model", "parts": [{"text": "I cannot provide investment or financial trading advice. Please consult a licensed financial advisor for stock market guidance."}]},
                "intermediate_data": {"tool_uses": [], "intermediate_responses": []}
            }]
        }
    ]

    # Merge while respecting existing seed cases
    all_tiers = [tier1_happy_path, tier2_gotchas, tier3_baits, tier4_probes]
    final_cases = []
    
    # Add all unique cases preserving 4-tier stratification order
    for tier in all_tiers:
        for case in tier:
            cid = case["eval_id"]
            # If seed already had a version of this case, prefer the seed version
            existing_seed = next((c for c in eval_cases if c.get("eval_id") == cid), None)
            if existing_seed:
                final_cases.append(existing_seed)
            else:
                final_cases.append(case)
            if cid in seen_ids:
                seen_ids.remove(cid)

    # Any remaining unclassified seed cases
    for rem_id in seen_ids:
        rem_case = next((c for c in eval_cases if c.get("eval_id") == rem_id), None)
        if rem_case:
            final_cases.append(rem_case)

    evalset_data = {
        "eval_set_id": set_id,
        "name": name,
        "description": "Stratified 4-Tier Evaluation Suite for Altostrat HR Multi-Agent System (root_orchestrator, rag_agent, workweek_agent, service_immediately_agent).",
        "eval_cases": final_cases
    }

    return evalset_data


def main():
    parser = argparse.ArgumentParser(description="Generate Google ADK 4-Tier Stratified Golden Evalset.")
    parser.add_argument("--output", "-o", required=True, help="Destination JSON file path")
    parser.add_argument("--seed", "-s", default=None, help="Optional seed golden evalset JSON path to ingest")
    parser.add_argument("--config", "-c", default=None, help="Optional destination path to generate matching eval_config.json")
    parser.add_argument("--name", default="MAS Golden Evaluation Suite", help="Evaluation set display name")
    parser.add_argument("--set-id", default="golden_mas_eval", help="Evaluation set ID")

    args = parser.parse_args()

    evalset = build_4tier_evalset(seed_file=args.seed, set_id=args.set_id, name=args.name)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(evalset, f, indent=2)

    total_cases = len(evalset["eval_cases"])
    print(f"✅ Generated Google ADK Golden Evalset: {args.output}")
    print(f"📊 Total Stratified Cases: {total_cases}")

    # Generate matching eval_config.json if requested
    if args.config:
        cfg_dir = os.path.dirname(os.path.abspath(args.config))
        if cfg_dir and not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir, exist_ok=True)
        config_data = {
            "criteria": {
                "tool_trajectory_avg_score": 0.8,
                "response_match_score": 0.8
            }
        }
        with open(args.config, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        print(f"⚙️ Generated matching ADK test config: {args.config}")


if __name__ == "__main__":
    main()
