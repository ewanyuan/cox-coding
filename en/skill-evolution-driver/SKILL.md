---
name: skill-evolution-driver
description: Helps teams continuously improve skills, automatically discovers skill optimization opportunities (such as missing necessary information, format issues, need version updates, etc.), executes safe update processes (backup, modify, test, restore), ensures skill quality continuously improves with project progress
dependency:
  python: []
  system: []
---

# Skill Evolution Driver

## Task Objectives
- This Skill is used to: Drive skill self-evolution, continuously optimize as project progresses
- Capabilities include:
  1. Monitor skill-manager stored data, identify skill optimization opportunities
  2. Remind users of potential optimization suggestions during idle time
  3. Maintain skill optimization task list
  4. Execute skill update processes (backup, update, test, restore)
  5. Manage skill version numbers
- Trigger Conditions: Triggered under any of following
  - **User direct request**: "Optimize skills", "improve skills", "skills need update", "skill upgrade", "fix skill issues"
  - **Automatic monitoring trigger**: Monitoring skill-manager stored skills data finds pending optimization tasks (such as: status=pending optimization tasks, errors and warnings in logs, missing required fields)
  - **Version related**: "Skill version number needs update", "need to record skill changes"
  - **Quality related**: "Skill format incorrect", "need to check skill quality", "skill tests failing"

## Optimization Identification

### Data Sources

Analyze optimization opportunities from skill-manager stored skill data:

1. **Missing Information**: Skill configuration lacks necessary fields (such as version)
2. **Format Issues**: Data format doesn't comply with specifications
3. **Duplicate Information**: Redundant or duplicate content exists
4. **Usage Patterns**: Identify improvement points based on access frequency and method
5. **Error Logs**: Identify common errors or warnings from logs
6. **Cross-Skill Collaboration Issues**: From other skills' logs identify dependency issues or improvement suggestions for current skill

### Optimization Types
- **format_improvement**: Format improvement
- **content_optimization**: Content optimization
- **version_update**: Version number update
- **bug_fix**: Bug fix
- **feature_enhancement**: Feature enhancement

## Evolution Process

### Step 1: Remind User

#### Automatic Monitoring Trigger
Agent periodically checks skill-manager stored data, identifies optimization opportunities:

**Check Tool**: Invoke `scripts/check_optimization_opportunities.py`
```bash
# Check all skills
python scripts/check_optimization_opportunities.py

# Check specific skill
python scripts/check_optimization_opportunities.py --skill-name dev-observability
```

**Check Content**:
1. **Pending Tasks**: Check skill-evolution-driver's own stored optimization tasks (status=pending)
2. **Missing Fields**: Check if skill configuration lacks necessary fields (such as version, deploy_mode, manual_path)
3. **Error Logs**: Check for ERROR/WARNING/CRITICAL logs in skill logs
4. **Directory Issues**: Check if skill directory structure complies with specifications

**Reminder Format**:
```
Detected potential optimization opportunities:
- Skill: skill-name
- Optimization type: format_improvement
- Description: SKILL.md lacks version field
- Start optimization? (y/n)
```

#### User Direct Trigger
When user expresses following needs, directly remind user:
- "Optimize skills", "improve skills"
- "Skills need update", "skill upgrade"
- "Fix skill issues"
- "Skill version number needs update"
- "Skill format incorrect", "need to check skill quality"

### Step 2: Maintain Task List

If user agrees, invoke skill-manager to store optimization tasks:

```json
{
  "task_id": "OPT-001",
  "skill_name": "skill-name",
  "optimization_type": "format_improvement",
  "description": "SKILL.md lacks version field",
  "status": "pending",
  "feasibility": "pending",
  "backup_path": "",
  "old_version": "",
  "new_version": "",
  "test_result": "",
  "notes": "",
  "created_at": "2024-01-22 12:00:00",
  "updated_at": "2024-01-22 12:00:00"
}
```

Storage method: Update skill-evolution-driver's configuration in skill-manager
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")
existing_config = storage.get_config("skill-evolution-driver") or {}
existing_config["optimization_tasks"] = [task_dict]  # Task list
storage.save_config("skill-evolution-driver", existing_config)
```

### Step 3: Analyze Feasibility

Analyze that skill's optimization feasibility:

**Feasibility Assessment Criteria**:
- Skill directory structure complete
- SKILL.md format correct
- Script syntax correct
- Dependency relationships clear
- Optimization content clear

**Infeasible Situations**:
- Skill directory doesn't exist or corrupted
- SKILL.md format error, cannot parse
- Optimization content unclear or too complex
- Optimization may break existing functionality

Update task status:
- Feasible: `feasibility: "feasible"`
- Not feasible: `feasibility: "not_feasible"`, and explain reason in `notes`

### Step 4: Backup Skill

Invoke `scripts/backup_skill.py` to backup skill:

```bash
python scripts/backup_skill.py --skill-dir /workspace/projects/skill-name
```

Backup file format: `skill-name.backup.<timestamp>.skill`

Update task:
- `backup_path: "/workspace/projects/skill-name.backup.<timestamp>.skill"`

### Step 5: Update Skill

Execute specific optimization operations, and update version number:

1. **Execute Optimization**: Modify skill content based on optimization type
2. **Update Version Number**: Invoke `scripts/update_version.py`

```bash
python scripts/update_version.py --skill-dir /workspace/projects/skill-name --type patch
```

Version number types:
- `patch`: Patch version (v1.0.0 -> v1.0.1)
- `minor`: Minor version (v1.0.0 -> v1.1.0)
- `major`: Major version (v1.0.0 -> v2.0.0)

Update task:
- `old_version: "v1.0.0"`
- `new_version: "v1.0.1"`

### Step 6: Test

Test and verify updated skill:

**Test Content**:
1. SKILL.md format validation (YAML frontmatter)
2. Script syntax check (Python syntax)
3. Directory structure validation (complies with fixed structure)
4. Dependency integrity check (dependency field)

Test script:
```bash
python scripts/backup_skill.py --validate-only --skill-dir /workspace/projects/skill-name
```

### Step 7: Handle Test Results

**Test Failed**:
1. Invoke `scripts/restore_skill.py` to restore skill
2. Use `manage_optimization_tasks.py` to update task status

```bash
# Restore skill
python scripts/restore_skill.py --backup-file <backup path> --skill-dir /workspace/projects/skill-name

# Update task status
python scripts/manage_optimization_tasks.py update \
  --task-id OPT-001 \
  --status failed \
  --test-result failed \
  --notes "Test failed: SKILL.md format error"
```

**Test Passed**:
1. Use `manage_optimization_tasks.py` to update task status
2. Package new .skill file
3. Inform user of update content
4. Remind user to reload skill

```bash
# Update task status
python scripts/manage_optimization_tasks.py update \
  --task-id OPT-001 \
  --status completed \
  --test-result passed \
  --notes "Optimization successful: added version field" \
  --new-version v1.0.1 \
  --backup-path /workspace/projects/skill-name.backup.20260122120000.skill
```

**Important**: Must update task status to `completed`, avoid next check repeating same optimization opportunity.

### Step 8: Notify User

Notify user based on test results:

**Test Passed**:
```
✓ Skill optimization successful
- Skill: skill-name
- Version: v1.0.0 -> v1.0.1
- Update content: Added version field
- Backup: skill-name.backup.<timestamp>.skill

Please reload AI interaction interface to use updated skill.
```

**Test Failed**:
```
✗ Skill optimization failed
- Skill: skill-name
- Reason: Test failed
- Details: SKILL.md format error
- Skill has been restored
```

## Core Functionality Description

### Agent-Processable Functions
- Monitor skill-manager data, identify optimization opportunities
- Remind users of optimization suggestions during idle time
- Maintain skill optimization task list
- Analyze optimization feasibility
- Execute optimization operations
- Perform test verification
- Handle test results
- Notify users

### Script-Implemented Functions
- **Check optimization opportunities**: `scripts/check_optimization_opportunities.py` scans skill-manager data, automatically identifies optimization opportunities (filters completed tasks)
- **Manage optimization tasks**: `scripts/manage_optimization_tasks.py` provides add/delete/update/query functionality for optimization tasks
- **Backup skill**: `scripts/backup_skill.py` backs up entire skill directory
- **Restore skill**: `scripts/restore_skill.py` restores skill from backup
- **Update version number**: `scripts/update_version.py` increments version field in SKILL.md
- **Test verification**: `scripts/backup_skill.py --validate-only` validates skill format

## Resource Index
- **Optimization opportunity check tool**: See [scripts/check_optimization_opportunities.py](scripts/check_optimization_opportunities.py) (automatically scans skill-manager data, identifies optimization opportunities, filters completed tasks)
- **Optimization task management tool**: See [scripts/manage_optimization_tasks.py](scripts/manage_optimization_tasks.py) (add/delete/update/query for optimization tasks)
- **Backup tool**: See [scripts/backup_skill.py](scripts/backup_skill.py) (backs up skill directory)
- **Restore tool**: See [scripts/restore_skill.py](scripts/restore_skill.py) (restores skill from backup)
- **Version management**: See [scripts/update_version.py](scripts/update_version.py) (updates version number)
- **Optimization guide**: See [references/optimization_guide.md](references/optimization_guide.md) (optimization types, test standards, best practices)

## Precautions
- Must backup skill before optimization
- Keep task status synchronized during optimization process
- Must restore skill if test fails
- Version number follows semantic versioning specification
- Major changes require explicit user confirmation
- After optimization complete, must update task status to `completed`, avoid repeating reminders
- After optimization, remind user to reload skill

## Best Practices
- Periodically monitor skill-manager data, identify optimization opportunities
- Prioritize handling high-value, low-risk optimizations
- Before optimization, fully analyze feasibility
- Maintain detailed optimization logs
- Periodically clean expired backup files
- Provide users with clear optimization descriptions

## Usage Examples

### Example 1: Add version Field
Detected skill-name's SKILL.md lacks version field.

1. Remind user
2. After user agrees, create optimization task
3. Analyze feasibility: feasible
4. Backup skill: skill-name.backup.20240122120000.skill
5. Update SKILL.md, add version: v1.0.0
6. Test verification: passed
7. Update task status: completed
8. Notify user: optimization successful

### Example 2: Format Improvement
Detected skill-name's SKILL.md format doesn't comply with specifications.

1. Remind user
2. After user agrees, create optimization task
3. Analyze feasibility: feasible
4. Backup skill
5. Fix SKILL.md format
6. Update version number: v1.0.0 -> v1.0.1
7. Test verification: passed
8. Update task status: completed
9. Notify user: optimization successful

### Example 3: Infeasible Optimization
Detected skill-name's optimization content too complex.

1. Remind user
2. After user agrees, create optimization task
3. Analyze feasibility: not feasible
4. Update task status: failed
5. Update notes: Optimization content too complex, requires manual intervention
6. Notify user: optimization infeasible, needs manual handling
