# Detailed Guide for Agent Workflows

This document details various workflows for Agents using the Cox skill.

---

## 1. Module Status Update Workflow

### Prerequisites

Before preparing to use the `update-module` command, the Agent should ensure:
1. Code analysis and implementation are complete
2. User confirmation has been obtained (user explicitly indicates satisfaction or problem resolution)
3. Current module status is normal (not `has_issue`)

### Proper Update Timing

```
✅ Correct Process:
1. User marks has_issue
2. User says "continue, plan next iteration"
3. Agent adds issue to iteration tasks
4. Executes tasks, resolves issues
5. Asks user for confirmation: "Issue resolved, are you satisfied?"
6. After user confirms, uses update-module to update status

❌ Incorrect Process:
1. User marks has_issue
2. Agent updates status directly without waiting for user input
```

### Usage Method

```bash
python scripts/collect_data.py update-module \
  --app app_status.json \
  --module "ModuleName" \
  --status optimized \
  --rate 1.0 \
  --notes "Optimization completed, user confirmed satisfaction"
```

### Dialogue Example

```
User: View Post List marked as has_issue, description: not aesthetic enough

Agent: I have recorded your feedback:
       - Module: View Post List
       - Issue Description: not aesthetic enough
       - Priority: Medium (UI/UX optimization)

       I will incorporate this issue into the next iteration planning.

User: OK, continue planning next iteration

Agent: Planning ITER-003, I found:
       - ISSUE-001: View Post List "not aesthetic" (Medium)
       - TASK-011: Add search functionality (High)

       Suggested priority order:
       1. TASK-011: Add search functionality
       2. ISSUE-001: Optimize View Post List UI

       Can we begin?

User: Yes

[Agent executes tasks...]

Agent: ISSUE-001 completed:
       - Redesigned post list layout
       - Optimized card styles and spacing
       - Added more visual elements

       Please review the effect, are you satisfied?

User: Satisfied

Agent: Received, updating module status...

[Use update-module command to update status]
```

---

## 2. User Feedback Processing Workflow

### Flowchart

```mermaid
flowchart TB
    Start[User marks has_issue on web page] --> Record[Agent records issue]
    Record --> Continue[Continue current work]
    Continue --> UserInput{User input}
    UserInput -->|Says "continue" or "plan next iteration"| Collect[Collect all pending items]
    Collect --> Tasks[Existing pending tasks]
    Collect --> Issues[User feedback issues]
    Tasks --> Prioritize[Evaluate priorities]
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
| **Critical** | Security Issue | Data leak, privilege bypass | Users can bypass login to access others' data |
| **High** | Functional BUG | Core functions unusable | Posting function completely fails |
| **High** | Performance Issue | Severely impacts usage | Page load exceeds 10 seconds |
| **Medium** | UI/UX Optimization | Poor experience but function normal | "Not aesthetic", "Hard to use" |
| **Medium** | Minor BUG | Doesn't affect main functions | Text errors, minor style issues |
| **Low** | Feature Suggestions | Nice-to-have | "Hope to add dark mode" |

### Processing Principles

1. **Don't interrupt current work**: After recording user feedback, continue completing current iteration
2. **Batch processing**: Evaluate all pending items and feedback uniformly when planning next iteration
3. **Priority-driven**: High-priority issues processed first
4. **User confirmation**: Must get user confirmation before updating status after resolving issue

---

## 3. Iteration Management Workflow

Detailed theory of iteration management, MVP principles, risk assessment and implementation decision-making are in [iteration_management.md](iteration_management.md).

This document focuses on the **operational workflow** for Agents in iteration management:

### Quick Reference

**Phase 1: Project Startup**
```bash
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Project Name" \
  --iterations 3 \
  --modules '[{"id":"MOD-001","name":"Module 1"}]'
```

**Phase 2: Plan Iteration**
- Confirm iteration goals with user
- Populate tasks array
- Begin execution after confirming plan

**Phase 3: Complete and Plan Next**
- Collect user feedback and has_issue markers
- Evaluate priorities
- Plan next iteration

### Collaboration with Issue Tracking

Issues involved in iteration management process:
- User marks has_issue on web → Record issue
- Evaluate collectively when planning next iteration
- Update module status after issue resolved

See "User Feedback Processing Workflow" and "Issue Tracking Workflow" sections in this document.

---

## 4. Issue Tracking Workflow

### When Triggered

Agent should actively trigger issue tracking:
1. **Complex issues**: Involving multiple modules, requiring multi-step resolution
2. **Recurring issues**: Same issue appears 2+ times in conversation without resolution

### Processing Steps

```
1. Identify issue → Determine affected modules
2. Generate issue ID → ISSUE-NNN
3. Update project_data.json → Add TODO task
4. Update test_metrics.json → Add tracing point suggestion (if applicable)
5. Call skill-manager → Store issue information
6. Report user → Explain measures taken
```

---

## 5. Common Scenario Handling

### Scenario 1: User marks has_issue on web page

```
Agent's response:
"I see you marked [module name] as having an issue: [issue description]
 I have recorded this issue (ISSUE-NNN), priority: [evaluation result]
 I will handle it uniformly when planning the next iteration.
 Should I continue current iteration, or handle this issue now?"
```

### Scenario 2: Planning next iteration

```
Agent's response:
"Planning [Iteration Name], I found:

 Pending tasks:
 - TASK-XXX: [Task name] ([Priority])

 User feedback:
 - ISSUE-XXX: [Issue description] ([Priority])

 Suggested iteration plan:
 1. [Priority-ordered task list]

 Is this plan acceptable?"
```

### Scenario 3: Task completed, asking for confirmation

```
Agent's response:
"[ISSUE-XXX/TASK-XXX] completed:
 - Specifically did what
 - Modified which files

 Please confirm if satisfied?"

 After user confirms:
 "Received, updating module status..."
 [Execute update-module]
 "Module [module name] status updated to [status]"
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
      "issue_description": "Not aesthetic enough."
    }
  ]
}
```

---

## Appendix

### A. update-module Command Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| --app | Yes | Path to app_status.json file |
| --module | Yes | Module name |
| --status | Yes | Target status: pending/developed/confirmed/optimized |
| --rate | No | Completion rate 0.0-1.0, default 1.0 |
| --notes | No | Notes |

### B. Status Value Explanation

| Status | Meaning | Usage Scenario |
|--------|---------|----------------|
| pending | Pending development | Module not started yet |
| developed | Developed | Function implemented, pending validation |
| confirmed | Confirmed | Function validated, pending optimization |
| optimized | Optimized | Function completed and optimized |
| has_issue | Has issue | User marked an issue |

### C. Priority Value Explanation

| Priority | Meaning | Response Time |
|----------|---------|---------------|
| critical | Critical | Immediate handling |
| high | High | Next iteration priority |
| medium | Medium | Next iteration as appropriate |
| low | Low | When convenient |

### D. Risk Level Value Explanation

| Risk | Meaning | Handling Strategy |
|------|---------|-------------------|
| high | High risk | Handle separately, verify immediately after completion |
| low | Low risk | Can batch with other low-risk tasks, verify together |