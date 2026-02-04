# Iteration Management Process Detailed Guide

## Overview

This document provides detailed implementation guidance and specific operational instructions for the iteration management process in SKILL.md.

## Trigger Conditions and MVP Principles

### Trigger Conditions
When users propose the following requirements, the agent should actively enable the iteration management process:
- Developing new features
- Building new projects
- Implementing complex requirements

### MVP-Driven Iteration Splitting Principles
Detailed implementation guide:

**First Iteration - Core Functionality**
- **Identification Method**: Analyze user requirements to find the core functionality users care about most
- **Implementation Strategy**: Use the simplest technical solution, avoid over-engineering
- **Delivery Standard**: Ensure core functionality is usable and can be verified by the user

**Second Iteration - Enhanced Functionality**
- **Feedback Collection**: Adjust direction based on user feedback from the first iteration
- **Function Extension**: Add secondary but important features
- **Experience Optimization**: Improve user interface and interaction experience

**Subsequent Iterations - Improvement and Optimization**
- **Detail Perfection**: Handle edge cases and exception handling
- **Performance Optimization**: Enhance system performance and response speed
- **Code Quality**: Refactor and optimize code structure

## Detailed Iteration Planning Method

### Two-Phase Planning Detailed Steps

**Phase 1 - At Project Startup**
```bash
# Generate iteration framework
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Project Name" \
  --app-name "Application Name" \
  --iterations 3 \
  --modules '["Module 1", "Module 2", "Module 3"]'
```

**Phase 2 - Detailed Planning for Each Iteration**
- **Task Decomposition**: Break iteration goals into specific executable tasks
- **Priority Sorting**: Sort tasks by importance and dependency relationships
- **Risk Assessment**: Assess risk level for each task

## Detailed Iteration Management Process

### Step 1: Requirements Analysis and Iteration Splitting
**Detailed Operational Guide**:
1. **Requirements Understanding**: Confirm user's real needs through dialogue
2. **Feature Identification**: List all user-visible features
3. **Priority Sorting**: Sort features by user value
4. **Iteration Division**: Assign features to different iterations

### Step 2: Data Generation Script Invocation
**Detailed Parameter Description**:
```bash
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Project Name" \
  --app-name "Application Name" \
  --iterations 3 \
  --modules '[{"id":"MOD-001","name":"Module 1"},{"id":"MOD-002","name":"Module 2"}]' \
  --iteration-names '["Iteration 1 Name", "Iteration 2 Name", "Iteration 3 Name"]'
```

**Task Generation Principles**:
- Script only generates empty tasks array
- All task fields filled by agent based on actual requirements
- Avoid using example data, maintain data authenticity

### Step 3: Task Decomposition and Population
**Detailed Task Field Description**:
```json
{
  "task_id": "TASK-001",
  "task_name": "Specific task description",
  "status": "todo/in_progress/completed/delayed",
  "assignee": "Responsible person (optional)",
  "priority": "low/medium/high/critical",
  "risk_level": "low/high",
  "tags": ["tag1", "tag2"]
}
```

**Task Decomposition Best Practices**:
- Each task should focus on a clear goal
- Task size should be appropriate for tracking and verification
- Consider dependencies between tasks

### Step 4: Confirm Iteration Plan with User
**Confirmation Process**:
1. Show iteration plan and expected outcomes
2. Explain each iteration's goals and value
3. Confirm with user and collect feedback
4. Adjust plan based on feedback

### Step 5: Collaboration with Development Skills
**Collaboration Mode**:
1. Pass task list to development skills
2. Development skills implement specific functions
3. COX tracks progress and updates data
4. Regularly confirm outcomes with user

## Task Risk Assessment and Implementation Decision

### Detailed Risk Assessment Standards

**High-Risk Task Characteristics**:
- Modify core modules or multiple files
- Affect multiple functional modules
- Involve data structure changes or architectural adjustments
- Modifications difficult to roll back

**Low-Risk Task Characteristics**:
- Single file or local modifications
- Affect single function
- UI adjustments or text modifications
- Modifications easy to roll back

### Detailed Implementation Decision Logic

**Sorting Rules**:
1. Sort by priority: critical > high > medium > low
2. Group by risk level: handle high-risk tasks separately

**Implementation Strategy Matrix**:
| Priority | Risk Level | Strategy | Verification Method |
|----------|------------|----------|---------------------|
| Critical | Low | Batch processing | Batch verification |
| Critical | High | Separate processing | Immediate verification |
| High | Low | Batch processing | Batch verification |
| High | High | Separate processing | Immediate verification |
| Medium/Low | Low | Batch processing | Batch verification |
| Medium/Low | High | Separate processing | Verify as needed |

### Detailed User Reminder Format

**Before High-Risk Task Implementation**:
```
**COX Reminder**: About to implement high-risk task 'task name'.
- Affected files: file list
- Impact scope: impact description
- Please verify related functions immediately after completion
```

**After High-Risk Task Implementation**:
```
**COX Reminder**: High-risk task 'task name' completed.
Please verify the following functions immediately:
1. Function 1
2. Function 2
3. Function 3

After verification is complete, I will continue to the next task.
```

## Module Maturity Updates

### Update Trigger Methods

**Method 1: AI Proactive Inquiry**
- **Timing**: After iteration completion, at major milestones
- **Content**: Module status, completion rate, notes
- **Method**: Automatic update of app_status.json

**Method 2: Interactive Web Support**
- **Scenario**: Using interactive web solution
- **Operation**: User modifies directly on web page
- **Advantage**: User can update anytime

### Module Status Management

**Status Transitions**:
- pending → in_progress → developed → confirmed → optimized
- Each status corresponds to different completion rates and verification requirements

### Specific Operational Process

The specific operational process for module status updates, update-module command usage, and dialogue examples are in the "Module Status Update Workflow" section of [agent_workflows.md](agent_workflows.md).

## Web Display Instructions

### Iteration Grouped Display
- **Iteration Cards**: Each iteration displayed independently
- **Current Iteration Marker**: Blue border and "Current" label
- **Progress Bar**: Task completion progress visualization

### Module Maturity Display
- **Module Cards**: Status and completion rate display
- **Progress Bar**: Completion rate visualization
- **Update Time**: Last update time display

## Example Scenarios

### Complete Workflow Example

**User Requirement**: "Build a blog using COX skill"

**COX Response Process**:
1. Understand requirements: Blog system development
2. Plan project: 3 iterations (basic functionality, comment functionality, user system)
3. Generate observability data
4. Show iteration 1 plan
5. Pass to development skill after user confirmation
6. Track progress and update data
7. Ask for module feedback after completion
8. Advance to next iteration

### Task Risk Assessment Example

**Task List**:
1. [Critical+High] Modify user authentication data structure
2. [Critical+Low] Optimize login API response time
3. [High+Low] Add user avatar functionality
4. [Medium+High] Refactor permission management system

**Implementation Recommendations**:
- **Batch 1**: Tasks 2 + 3 (low-risk batch processing)
- **Batch 2**: Task 1 (high-risk separate processing, immediate verification)
- **Batch 3**: Task 4 (verify as needed)

## Best Practices

### Iteration Planning Best Practices
- Each iteration goal clear and verifiable
- Prioritize implementing user-visible functionality
- Update project data promptly to reflect actual progress

### Task Management Best Practices
- Task size appropriate for tracking
- Consider task dependencies
- Update task status regularly

### Risk Management Best Practices
- Handle high-risk tasks separately
- Verify high-risk modifications promptly
- Maintain data backup and rollback capabilities

---

*This document is the detailed implementation guide for the iteration management process in SKILL.md. For specific concepts and process overview, please refer to the SKILL.md document.*