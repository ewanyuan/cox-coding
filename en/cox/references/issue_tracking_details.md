# Issue Tracking and Response Detailed Process

This document provides complete tracking and response processes for complex and recurring issues.

## Table of Contents
- [Trigger Conditions](#trigger-conditions)
- [Response Steps](#response-steps)
- [Agent Processing Flow](#agent-processing-flow)
- [Usage Examples](#usage-examples)

---

## Trigger Conditions

When the following situations occur, the agent should actively trigger issue tracking and response:

1. **Complex Issues**
   - User feedback involves multiple modules
   - Requires multi-step resolution
   - Requires cross-team collaboration

2. **Recurring Issues**
   - Same issue appears multiple times in conversation (2 or more)
   - And remains unresolved

---

## Response Steps

### Step 1: Identify Issue and Determine Affected Modules

Analyze user-described issue, identifying:
- Affected application modules (from `app_status.json`)
- Related iterations and tasks (from `project_data.json`)
- Issue complexity level (high/medium/low)

### Step 2: Update Project Dimensional TODO List

Add new TODO task to current iteration in `project_data.json`:

```json
{
  "task_id": "ISSUE-<sequence number>",
  "task_name": "Issue Tracking: <issue description>",
  "status": "todo",
  "assignee": "<responsible person, if any>",
  "priority": "<issue complexity>",
  "tags": ["issue-tracker", "<related module>"],
  "issue_details": {
    "description": "<detailed issue description>",
    "affected_modules": ["<module1>", "<module2>"],
    "first_reported": "<first reported time>",
    "occurrence_count": <occurrence count>,
    "complexity": "<high/medium/low>"
  }
}
```

### Step 3: Add Issue-Related Assumption Analysis

Add assumption to current iteration in `project_data.json`:

```json
{
  "assumption_id": "ASSUMP-ISSUE-<sequence number>",
  "description": "<assumption description, e.g.: this issue may be caused by X reason>",
  "status": "pending",
  "validation_date": null,
  "related_issue": "ISSUE-<sequence number>",
  "assumption_type": "<root-cause/impact-scope/solution-approach>"
}
```

### Step 4: Suggest Adding Related Tracing Points

Add tracing point suggestion to `tracing_points` in `test_metrics.json`:

```json
{
  "point_id": "TRACE-ISSUE-<sequence number>",
  "module": "<related module>",
  "location": "<suggested location, e.g.: src/module.py:<line number>>",
  "metric_type": "<counter/histogram>",
  "status": "inactive",
  "last_verified": null,
  "purpose": "<tracing point purpose, e.g.: track frequency or duration of issue occurrence>",
  "related_issue": "ISSUE-<sequence number>"
}
```

### Step 5: Call skill-manager to Store Issue Information

Call **skill-manager** skill to store issue tracking information.

**Method One: Using auxiliary script (recommended)**
```bash
python scripts/store_to_skill_manager.py issue \
  --issue-id ISSUE-001 \
  --description "Order creation interface often times out during peak hours" \
  --modules "Order Processing Module, Database Module" \
  --complexity high \
  --count 3
```

**Method Two: Directly calling skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# Read existing cox configuration
existing_config = storage.get_config("cox") or {}
existing_logs = storage.get_logs("cox") or {}

# Update configuration: add issue information
existing_config["issue_id"] = "ISSUE-<sequence number>"
existing_config["issue_description"] = "<issue description>"
existing_config["affected_modules"] = ["<module1>", "<module2>"]
existing_config["complexity"] = "<high/medium/low>"
existing_config["occurrence_count"] = <occurrence count>
existing_config["first_reported"] = "<time>"
existing_config["last_updated"] = "<time>"

# Append logs
existing_logs.append({
    "time": "<time>",
    "level": "WARNING",
    "message": "Detected complex/recurring issue, observation data updated",
    "issue_id": "ISSUE-<sequence number>"
})

# Save
storage.save("cox", config=existing_config, logs=existing_logs)
```

---

## Agent Processing Flow

1. Monitor conversation context, identifying complex and recurring issues
2. Analyze issue impact scope, determining related modules
3. Generate issue ID (format: ISSUE-NNN)
4. Update `project_data.json`: add TODO task and assumption
5. Update `test_metrics.json`: add tracing point suggestion
6. Call skill-manager to store issue tracking information
7. Report to user about taken observation update measures

---

## Usage Examples

**User Feedback**: "Order creation interface often times out during peak hours, affecting 3 customers"

**Agent Response**:

1. **Identify as complex issue** (high complexity)
   - Involves order module, affects multiple customers

2. **Determine affected modules**
   - Order Processing Module

3. **Generate issue ID**
   - ISSUE-001

4. **Update data files**
   - Add TODO task: ISSUE-001
   - Add assumption: Order volume exceeds current processing capacity
   - Add tracing point suggestion: Order processing time histogram

5. **Call skill-manager to store issue information**
   ```bash
   python scripts/store_to_skill_manager.py issue \
     --issue-id ISSUE-001 \
     --description "Order creation interface often times out during peak hours" \
     --modules "Order Processing Module, Database Module" \
     --complexity high \
     --count 3
   ```

6. **Report to user**
   > Identified as complex issue, observation updated:
   > - TODO task: ISSUE-001
   > - Assumption analysis: Order volume exceeds current processing capacity
   > - Tracing point suggestion: Order processing time histogram
   >
   > Issue information stored to skill-manager