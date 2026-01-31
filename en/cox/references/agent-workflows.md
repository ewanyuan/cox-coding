# Agent Workflow Detailed Guide

This document provides detailed workflow guidance for Agents using the Cox skill.

---

## 1. Module Status Update Workflow

### Prerequisites

Before Agent uses the `update-module` command, ensure:
1. Code analysis and implementation are complete
2. User confirmation is obtained (user explicitly states satisfaction or issue is resolved)
3. Module current status is normal (not `has_issue`)

### Correct Update Timing

```
✓ Correct Flow:
1. User marks has_issue
2. User says "Continue" or "Plan next iteration"
3. Agent incorporates issue into iteration tasks
4. Execute tasks, resolve issue
5. Ask user for confirmation: "Issue resolved, are you satisfied?"
6. After user confirms, use update-module to update status

✗ Incorrect Flow:
1. User marks has_issue
2. Agent immediately uses update-module to override without waiting for user input
```

### Usage

```bash
python scripts/collect_data.py update-module \
  --app app_status.json \
  --module "ModuleName" \
  --status optimized \
  --rate 1.0 \
  --notes "Optimization complete, user confirmed satisfaction"
```

### Dialogue Example

```
User: Marks View Post List as has_issue, description: "Not beautiful enough"

Agent: I have recorded your feedback:
       - Module: View Post List
       - Issue: Not beautiful enough
       - Priority: Medium (UI/UX optimization)

       I will incorporate this issue into the next iteration planning.

User: OK, continue planning next iteration

Agent: Planning ITER-003, I found:
       - ISSUE-001: View Post List "Not beautiful enough" (Medium)
       - TASK-011: Add search functionality (High)

       Suggested priority order:
       1. TASK-011: Add search functionality
       2. ISSUE-001: Optimize View Post List UI

       Shall we proceed?

User: Yes

[Agent executes tasks...]

Agent: ISSUE-001 completed:
       - Redesigned post list layout
       - Optimized card styles and spacing
       - Added more visual elements

       Please check the results, are you satisfied?

User: Satisfied

Agent: Received, updating module status...

[Uses update-module command to update status]
```

---

## 2. User Feedback Handling Workflow

### Flow Diagram

```mermaid
flowchart TB
    Start[User marks has_issue on webpage] --> Record[Agent records issue]
    Record --> Continue[Continue current work]
    Continue --> UserInput{User input}
    UserInput -->|"Continue" or "Plan next iteration"| Collect[Collect all pending items]
    Collect --> Tasks[Existing pending tasks]
    Collect --> Issues[User feedback issues]
    Tasks --> Prioritize[Evaluate priority]
    Issues --> Prioritize
    Prioritize --> Sort[Sort by priority]
    Sort --> Plan[Plan next iteration]
    Plan --> Execute[Execute tasks]
    Execute --> Confirm[Ask user for confirmation]
    Confirm --> UserConfirm{User confirms?}
    UserConfirm -->|Yes| Update[Use update-module to update status]
    UserConfirm -->|No| Plan
```

### Priority Evaluation Matrix

| Priority | Type | Evaluation Criteria | Example |
|----------|------|-------------------|---------|
| **Critical** | Security | Data breach, permission bypass | User can access others' data without login |
| **High** | Functional Bug | Core feature not working | Post creation completely broken |
| **High** | Performance | Severe impact on usage | Page load exceeds 10 seconds |
| **Medium** | UI/UX | Poor experience but functional | "Not beautiful enough", "Hard to use" |
| **Medium** | Minor Bug | Doesn't affect main features | Typos, small style issues |
| **Low** | Feature Request | Nice to have | "Would be nice to have dark mode" |

### Handling Principles

1. **Don't interrupt current work**: After recording user feedback, continue completing current iteration
2. **Batch processing**: When planning next iteration, evaluate all pending items and feedback together
3. **Priority-driven**: Handle high-priority issues first
4. **User confirmation**: Must get user confirmation before updating module status after issue resolution

---

## 3. Iteration Management Detailed Workflow

### Phase 1: Project Initiation

```
User requirement
    ↓
Agent analyzes core features
    ↓
Agent infers module list
    ↓
Invoke data generation script:
  --iterations 3
  --modules '[{"id":"MOD-001","name":"..."}]'
    ↓
Generate iteration framework (tasks array is empty)
```

### Phase 2: Plan First Iteration

```
Confirm ITER-001 goals with user
    ↓
Fill ITER-001 tasks array
    ↓
Each task contains:
  - task_id
  - task_name
  - status: todo
  - priority
  - risk_level
  - tags
    ↓
Confirm plan with user
    ↓
Start execution
```

### Phase 3: Complete and Plan Next

```
ITER-001 complete
    ↓
Collect user feedback
    ↓
Collect has_issue marks from webpage
    ↓
Evaluate priority
    ↓
Fill ITER-002 tasks array
    ↓
Confirm plan with user
    ↓
Start execution
```

### Key Points

- ✓ Iteration framework first, detailed tasks filled incrementally
- ✓ Each iteration adjusted based on latest user feedback
- ✓ User feedback issues included in pending evaluation
- ✗ Don't plan all details for all iterations at once

---

## 4. Issue Tracking Workflow

### When to Trigger

Agent should proactively trigger issue tracking:
1. **Complex Issues**: Involve multiple modules, require multi-step resolution
2. **Recurring Issues**: Same issue appears 2+ times in conversation and remains unresolved

### Processing Steps

```
1. Identify issue → Determine affected modules
2. Generate issue ID → ISSUE-NNN
3. Update project_data.json → Add TODO tasks
4. Update test_metrics.json → Add instrumentation recommendations (if applicable)
5. Invoke skill-manager → Store issue information
6. Report to user → Explain measures taken
```

---

## 5. Common Scenario Handling

### Scenario 1: User marks has_issue on webpage

```
Agent response:
"I see you marked [Module Name] has an issue: [Issue description]
 I have recorded this issue (ISSUE-NNN), priority: [Evaluation result]
 I will handle it when planning the next iteration.
 Should I continue the current iteration, or handle this issue now?"
```

### Scenario 2: Planning next iteration

```
Agent response:
"Planning [Iteration Name], I found:

 Pending tasks:
 - TASK-XXX: [Task name] ([Priority])

 User feedback:
 - ISSUE-XXX: [Issue description] ([Priority])

 Suggested iteration plan:
 1. [Task list sorted by priority]

 Does this plan work for you?"
```

### Scenario 3: Task complete, ask for confirmation

```
Agent response:
"[ISSUE-XXX/TASK-XXX] completed:
 - What was done
 - Which files were modified

 Please confirm if you are satisfied?"

 After user confirms:
 "Received, updating module status..."
 [Execute update-module]
 "Module [Module Name] status updated to [Status]"
```

---

## 6. Data Format Reference

### Modules in project_data.json

```json
{
  "iteration_id": "ITER-001",
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "View Post List",
      "expected_completion": 0.8
    }
  ]
}
```

### Modules in app_status.json

```json
{
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "View Post List",
      "status": "has_issue",
      "completion_rate": 0.8,
      "owner": "Developer",
      "last_update": "2026-01-30",
      "notes": "Post list implemented",
      "issue_description": "Not beautiful enough."
    }
  ]
}
```

---

## Appendix

### A. update-module Command Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| --app | Yes | app_status.json file path |
| --module | Yes | Module name |
| --status | Yes | Target status: pending/developed/confirmed/optimized |
| --rate | No | Completion rate 0.0-1.0, default 1.0 |
| --notes | No | Notes/Comments |

### B. Status Values

| Status | Meaning | Usage Scenario |
|--------|---------|----------------|
| pending | Pending development | Module not yet started |
| developed | Developed | Features implemented, awaiting verification |
| confirmed | Confirmed | Features verified, awaiting optimization |
| optimized | Optimized | Features completed and optimized |
| has_issue | Has issue | User marked an issue |

### C. Priority Values

| Priority | Meaning | Response Time |
|----------|---------|---------------|
| critical | Critical | Handle immediately |
| high | High | Next iteration priority |
| medium | Medium | Next iteration as appropriate |
| low | Low | When time permits |

### D. Risk Level Values

| Risk | Meaning | Handling Strategy |
|------|---------|-------------------|
| high | High risk | Handle separately, verify immediately after completion |
| low | Low risk | Can batch with other low-risk tasks, verify together |
