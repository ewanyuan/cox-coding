# Issue Tracking and Response Detailed Process

This document provides complete tracking and response processes for complex issues and recurring issues.

## Table of Contents
- [Trigger Conditions](#trigger-conditions)
- [Response Steps](#response-steps)
- [Agent Processing Flow](#agent-processing-flow)
- [Usage Examples](#usage-examples)

---

## Trigger Conditions

Agent should proactively trigger issue tracking and response when:

1. **Complex Issues**
   - User feedback involves multiple modules
   - Requires multi-step resolution
   - Requires cross-team collaboration

2. **Recurring Issues**
   - Same issue appears multiple times in conversation (2 or more)
   - And fails to resolve smoothly

---

## Response Steps

### Step 1: Identify Issue and Determine Affected Modules

Analyze user-described issue, identify:
- Involved application modules (from `app_status.json`)
- Related iterations and tasks (from `project_data.json`)
- Issue complexity level (high/medium/low)

### Step 2: Update Project Dimension TODO List

Add new TODO task in current iteration of `project_data.json`:

```json
{
  "task_id": "ISSUE-<sequence>",
  "task_name": "Issue Tracking: <Issue Description>",
  "status": "todo",
  "assignee": "<Assignee, if any>",
  "priority": "<Issue complexity>",
  "tags": ["issue-tracker", "<related module>"],
  "issue_details": {
    "description": "<Detailed issue description>",
    "affected_modules": ["<module1>", "<module2>"],
    "first_reported": "<First report time>",
    "occurrence_count": <occurrence count>,
    "complexity": "<high/medium/low>"
  }
}
```

### Step 3: Add Issue-Related Hypothesis Analysis

Add hypothesis in current iteration of `project_data.json`:

```json
{
  "assumption_id": "ASSUMP-ISSUE-<sequence>",
  "description": "<Hypothesis description, such as: issue may be caused by X>",
  "status": "pending",
  "validation_date": null,
  "related_issue": "ISSUE-<sequence>",
  "assumption_type": "<root-cause/impact-scope/solution-approach>"
}
```

### Step 4: Suggest Adding Related Instrumentation Points

Add instrumentation point recommendation in `test_metrics.json` `tracing_points`:

```json
{
  "point_id": "TRACE-ISSUE-<sequence>",
  "module": "<Related module>",
  "location": "<Suggested location, such as: src/module.py:<line number>>",
  "metric_type": "<counter/histogram>",
  "status": "inactive",
  "last_verified": null,
  "purpose": "<Instrumentation purpose, such as: track issue occurrence count or duration>",
  "related_issue": "ISSUE-<sequence>"
}
```

### Step 5: Invoke skill-manager to Store Issue Information

Invoke **skill-manager** skill to store issue tracking information.

**Method 1: Use Helper Script (Recommended)**
```bash
python scripts/store_to_skill_manager.py issue \
  --issue-id ISSUE-001 \
  --description "Order creation API frequently times out during peak hours" \
  --modules "Order Processing Module,Database Module" \
  --complexity high \
  --count 3
```

**Method 2: Directly Invoke skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# Read cox existing configuration
existing_config = storage.get_config("cox") or {}
existing_logs = storage.get_logs("cox") or {}

# Update configuration: add issue information
existing_config["issue_id"] = "ISSUE-<sequence>"
existing_config["issue_description"] = "<Issue description>"
existing_config["affected_modules"] = ["<module1>", "<module2>"]
existing_config["complexity"] = "<high/medium/low>"
existing_config["occurrence_count"] = <occurrence count>
existing_config["first_reported"] = "<time>"
existing_config["last_updated"] = "<time>"

# Append logs
existing_logs.append({
    "time": "<time>",
    "level": "WARNING",
    "message": "Detected complex/recurring issue, observability data updated",
    "issue_id": "ISSUE-<sequence>"
})

# Save
storage.save("cox", config=existing_config, logs=existing_logs)
```

---

## Agent Processing Flow

1. Monitor conversation context, identify complex issues and recurring issues
2. Analyze issue impact scope, determine related modules
3. Generate issue ID (format: ISSUE-NNN)
4. Update `project_data.json`: add TODO tasks and hypotheses
5. Update `test_metrics.json`: add instrumentation recommendations
6. Invoke skill-manager to store issue tracking information
7. Report taken observation update measures to user

---

## Usage Examples

**User Feedback**: "Order creation API frequently times out during peak hours, already affected 3 customers"

**Agent Response**:

1. **Identify as Complex Issue** (high complexity)
   - Involves order module, affects multiple customers

2. **Determine Affected Modules**
   - Order Processing Module

3. **Generate Issue ID**
   - ISSUE-001

4. **Update Data Files**
   - Add TODO task: ISSUE-001
   - Add hypothesis: Order volume exceeds current processing capacity
   - Add instrumentation recommendation: Order processing time histogram

5. **Invoke skill-manager to Store Issue Information**
   ```bash
   python scripts/store_to_skill_manager.py issue \
     --issue-id ISSUE-001 \
     --description "Order creation API frequently times out during peak hours" \
     --modules "Order Processing Module,Database Module" \
     --complexity high \
     --count 3
   ```

6. **Report to User**
   > Identified as complex issue, observability updated:
   > - TODO task: ISSUE-001
   > - Hypothesis analysis: Order volume exceeds current processing capacity
   > - Instrumentation recommendation: Order processing time histogram
   >
   > Issue information stored to skill-manager
