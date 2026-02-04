---
name: cox
version: v1.0.0
description: Cox Programming - Safeguarding your AI programming experience. Helps development teams grasp project progress, identify development risks, and understand system health status. Provides project progress tracking, iteration management (MVP-driven), task status management, development assumption recording, application module monitoring, test tracing points, and anomaly analysis functions. Supports both static web and interactive web solutions, suitable for different environments and team sizes. Web pages are grouped by iteration, clearly presenting the progress and tasks of each iteration.
dependency:
  python:
    - flask>=2.0.0  # Only required for interactive web solution
  system: []
---

# COX Programming - Safeguarding your AI programming experience

## Task Objectives
- **COX's Role**: COX is an **AI Programming Navigator**, responsible for project management and observability, not directly writing code or implementing functions
- **Collaboration Mode**: COX collaborates with development skills
  - COX: Responsible for project planning, iteration management, progress tracking, issue tracking
  - Development Skills (e.g., cox-coding): Responsible for specific function implementation and code writing
- Capabilities include:
  1. Project dimension: Track iteration progress, task status, development assumptions
  2. Application dimension: Monitor application function module status
  3. Test dimension: Manage test tracing points, analyze anomalies

## Trigger Conditions

COX will be triggered in any of the following situations:

### Software Development Support (Core Scenario)
When users propose software development requirements, COX should **actively enable** project management and iteration management processes:
- **User Expression**: "Make a blog", "Develop a calculator", "Implement XX function", "Make an e-commerce system"
- **Collaboration Process**:
  1. COX understands requirements, plans project structure and iterations
  2. COX generates observability data (project progress, task list, module planning)
  3. COX passes planning to development skills (e.g., cox-coding) for specific implementation
  4. COX continuously tracks progress, updates observability data

**Sample Dialogue**:
```
User: HI COX, make a calculator
COX: Okay, I'll help you plan the calculator project development. Let me first create project observability data...
[Call script to generate data, plan iterations and tasks]
COX: Project planning completed, including the following modules:
- UI Interface Module
- Calculation Logic Module
- History Record Module

Now I'll break down iteration tasks, then ask development skills to implement specific functions.
```

### Project Progress
- "Want to know how project progress is going", "What's the iteration completion rate?"
- "Check task status", "Which tasks are completed", "What's left to do"

### Issue Tracking
- "How to track frequent bugs", "How to handle recurring issues", "Need to record issues to resolve"
- "Are there any anomalies that need attention"

### Quality Assurance
- "Need to monitor API performance", "How to discover system anomalies", "How's test coverage"
- "API response time slow", "System has anomalies"

### Team Collaboration
- "Need to share project information", "Let team members understand current status", "Need visual dashboard"

## Deployment Solution Selection

Before starting, please select a deployment solution based on team needs. Detailed configuration instructions are in [references/deployment_details.md](references/deployment_details.md).

### Interactive Web Solution (Recommended)
- **Features**: Provides local Web interface, supports real-time data refresh (every 30 seconds), supports interaction
- **Applicable Scenarios**: Real-time monitoring required
- **Usage Threshold**: Requires Flask installation (`pip install flask`)
- **Usage Method**: Call `scripts/run_web_observability.py --mode web`, access http://localhost:5000

### Static Web Solution
- **Features**: Generates static HTML files, data embedded in HTML, no additional JSON files required
- **Applicable Scenarios**: Restricted environments (such as online sandbox environments), quick requirement validation
- **Usage Threshold**: No additional dependencies required (no need to install Flask)
- **Usage Method**: Call `scripts/run_web_observability.py --mode static`, generates `observability.html` file
- **Refresh Method**: Click refresh button to re-render data (static mode doesn't support auto-refresh)

### Comprehensive Solution (Not Available Yet)
- Features: Professional observability tools using Prometheus + Grafana, Docker deployment
- Applicable Scenarios: Preparing to migrate to production environment, requiring professional monitoring capabilities
- Status: Not open yet, will be launched after improving data integration and configuration schemes

## Quick Start

### Step 1: Generate Observability Data

**Recommended Method: Use Script to Generate Data**

To ensure data format 100% complies with specification, recommend using data generation script:

```bash
# Method 1: Generate minimal dataset (quick experience)
python scripts/generate_observability_data.py \
  --mode minimal \
  --project-name "My Project" \
  --app-name "My Application"

# Method 2: Generate custom modules (recommended)
# Agent should decompose tasks based on actual requirements, not use sample tasks
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Calculator Project" \
  --app-name "Calculator Application" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"}]'


# Method 2.5: Use custom iteration names (recommended)
# Specify meaningful names for each iteration, not default "Iteration N"
python scripts/generate_observability_data.py   --mode complete   --project-name "Calculator Project"   --app-name "Calculator Application"   --iterations 4   --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"}]'   --iteration-names '["Core Foundation and Platform Configuration","Planning Management and Assumption Management","Content Generation Workflow","Intelligent Assistance and Optimization"]'

# Method 3: Generate complete example (includes test suite framework, but tasks, tracing points, anomalies left empty)
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Calculator Project" \
  --app-name "Calculator Application" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"}]'
```

Script generates three JSON files in current directory:
- `project_data.json`: Project iteration and task data
- `app_status.json`: Application module status data
- `test_metrics.json`: Test tracing points and anomaly data

**Core Principles**:
- **Sample data only provides minimal skeleton**, doesn't fill any false business data
- **Tasks, tracing points, anomalies default to empty**, filled by agent based on actual situation
- Everything based on real data, avoid producing misleading information

**About Tasks**:
- **Script Behavior**: Default generates empty tasks array, no additional parameters needed. Agent should decompose tasks based on actual requirements then populate.
- **Task Fields**:
  - `task_id`: Task ID (e.g., TASK-001)
  - `task_name`: Task name (specific description, e.g., "Design calculator UI interface")
  - `status`: Task status (todo/in_progress/completed/delayed)
  - `assignee`: Responsible person (optional, fill when team collaboration needed)
  - `priority`: Priority (low/medium/high/critical)
  - `tags`: Tags (optional, for classification)

**About Tracing Points and Anomalies**:
- **Default Empty**: Tracing points and anomalies generated by script are both empty arrays `[]`
- **Real Data Filling**: Should be filled by agent based on actual monitoring data
- **Data Fields**:
  - `tracing_points`: Test tracing points (module, location, status, metric type)
  - `anomalies`: Anomaly records (type, description, severity, status, occurrence count, time)

**Custom Module Explanation**:
- Use `--modules` parameter to define modules actually needed by project
- Module list in JSON format, containing id and name fields
- When calling script, agent should automatically infer suitable modules based on project requirements

**⚠️ Key Rule: Module Definition Rule**
- **Modules must be user-verifiable functions**, not technical components
- **Prohibited Module Names**: "UI Module", "Backend Module", "Database Module", "Logic Module", "Interface Module", etc.
- **Correct Module Examples**: "User Login", "Article List", "Add to Cart", "Search", "Payment"
- **Think from user perspective**: "What can I see and test?" not "How is it implemented?"

**Subsequent Usage**:
- Directly modify generated JSON files to adapt to actual project
- Data format instructions in [references/data_format.md](references/data_format.md)

### Step 2: Select Solution and Start

**Interactive Web Solution (Recommended)**:
```bash
# Start Web server (need to install Flask first: pip install flask)
python scripts/run_web_observability.py \
  --mode web \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 127.0.0.1 \
  --port 5000

# Access http://127.0.0.1:5000 to view interface, data auto-refreshes every 30 seconds
```

**Static Web Solution**:
```bash
# Generate static HTML file (no Flask required)
# Data will be inlined to HTML, no additional JSON files needed
python scripts/run_web_observability.py \
  --mode static \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output observability.html

# Directly open observability.html in browser to view interface
# Data inlined, no other files needed
```

**Explanation**:
- Web mode: Data updates in real-time, no regeneration needed, access http://127.0.0.1:5000 to view interface
- Static mode: Data inlined to HTML file, generate once then data fixed, click refresh button to re-render

### Step 3: Call skill-manager to store deployment information
After deployment, call **skill-manager** skill to store deployment information, facilitate subsequent management and skill collaboration.

Detailed call methods in [references/deployment_details.md](references/deployment_details.md).

### Step 4: Continuously Update Data
During development, regularly update data files, then regenerate static HTML (static mode) or refresh page (Web mode). Agent can help you analyze existing data, identify content needing updates.

### Step 5: Guidance after skill execution completion

**Agent should actively remind users**:
After executing COX skill, agent should actively remind user to view project page, inform current status and next action suggestions.

**Standard Guidance Process**:

1. **Inform user data generated**
   - Clearly state project data files generated
   - Explain project page generated

2. **Provide viewing method**
   - Web mode: Access http://127.0.0.1:5000
   - Static mode: Open observability.html in browser

3. **Summarize current iteration plan**
   - Read current_iteration from project_data.json
   - List all tasks in current iteration (task_name, status)
   - Explain number of completed/in-progress/pending tasks

4. **Identify next action**
   - Find tasks with status pending or todo
   - Sort by priority: critical > high > medium > low
   - Recommend next task to handle

5. **Coordinate other skills**
   - For development tasks, suggest calling development skills (e.g., cox-coding)
   - For testing tasks, suggest updating test_metrics.json
   - For deployment tasks, suggest calling skill-manager

6. **User Confirmation**
   - Ask user: "Which task would you like to start now?"
   - Call corresponding skill based on user selection

**Sample Dialogue**:
```
Agent: COX has generated project data for you.

You can view project page via the following methods:
- Web mode: Access http://127.0.0.1:5000
- Static mode: Open observability.html in browser

Current iteration: Iteration 1 - Basic Function Development
- Completed: 2 tasks
- In Progress: 1 task
- Pending: 3 tasks

COX suggests next action:
1. Complete task "User Login API" (priority: high)
2. Start task "Data Persistence Module" (priority: medium)

Which task would you like to start now? Or do you have other ideas?
```

## Core Function Explanation

### Functions Agent Can Handle
- **Requirement Analysis and Module Planning**: According to user requirements (e.g., "make a calculator") analyze core functions, automatically infer suitable module list
- **Data Generation Guidance**: Generate custom module list based on project requirements, call data generation script
- **Data Analysis**: Analyze existing observability data, identify project bottlenecks
- **Usage Guidance**: Answer questions about selection and deployment of two solutions
- **Data Update Suggestions**: Provide data update suggestions based on development progress
- **Module Status Updates**: Use `scripts/collect_data.py update-module` command to update module maturity after code analysis and user confirmation
- **User Feedback Processing**: Record user feedback from interactive web, incorporate into next iteration planning based on priority
- **Issue Tracking and Response**: Identify complex and recurring issues, automatically update observation data (TODO tasks, assumption analysis, tracing point suggestions)

Detailed workflow: [Agent Workflow Guide](references/agent-workflows.md)

### Script Implementation Functions
- **Data Generation**: `scripts/generate_observability_data.py` generates observability data compliant with specification (avoid large model hallucinations)
- **Data Collection and Validation**: `scripts/collect_data.py`
  - Validate whether JSON data format complies with specification
  - **update-module Command**: Update module status after code analysis and user confirmation
  - Usage: `python scripts/collect_data.py update-module --app app_status.json --module "ModuleName" --status optimized --rate 1.0 --notes "..."`
- **Static Web Generation**: `scripts/run_web_observability.py --mode static` generates static HTML file (data inlined, no Flask needed)
- **Interactive Web Service**: `scripts/run_web_observability.py --mode web` starts Flask Web server
- **Skill-manager Storage Tool**: `scripts/store_to_skill_manager.py` stores deployment information and issue tracking information

## Iteration Management Process

### Trigger Conditions
When users propose needs for developing new functions, building new projects, or implementing complex requirements, agent should actively enable iteration management process.

### MVP-Driven Iteration Splitting Principle

When splitting iterations, agent should follow **MVP (Minimum Viable Product)** principle:

1. **First Iteration**: Core Functionality
   - Identify user-visible core functions
   - Implement with simplest approach
   - Deliver quickly for user confirmation

2. **Second Iteration**: Enhanced Functionality
   - Adjust based on user feedback
   - Add secondary functions
   - Optimize user experience

3. **Subsequent Iterations**: Improvement and Optimization
   - Gradually improve details
   - Performance optimization
   - Edge case handling

### Iteration Planning Method

**Two-Phase Planning**:

**Phase 1 - At Project Startup**:
- Preliminary plan 2-3 iterations' general direction
- Call data generation script: `--iterations 3`
- Generate iteration framework, but `tasks` array empty
- Each iteration contains `modules` list, but no detailed tasks

**Phase 2 - Detailed Planning for Each Iteration**:
- Plan detailed tasks for first iteration, populate `tasks` array
- After completion, plan next iteration based on user feedback
- Each iteration adjusted based on latest user feedback

**Key Points**:
- ✅ Have iteration framework first, then fill detailed tasks one by one
- ❌ Don't plan all details for all iterations at the beginning

Detailed iteration planning method, risk assessment and implementation decision guidelines in [references/iteration_management.md](references/iteration_management.md).

### Iteration Management Process

**Step 1: Requirement Analysis and Iteration Splitting**
1. Understand core objectives of user requirements
2. Identify user-visible function points
3. Split into multiple iterations according to priority
4. Each iteration focuses on a clear objective

**Step 2: Call Data Generation Script**
Agent automatically infers module list based on project requirements and calls data generation script.

**Step 3: Agent Decomposes Tasks and Populates Data**
1. Analyze user requirements, decompose specific tasks
2. Fill `tasks` array for each iteration
3. Set task status and priority

Detailed script call parameters, task field explanations and examples in [references/iteration_management.md](references/iteration_management.md).

**Step 4: Confirm Iteration Plan with User**
1. Show first iteration plan and expected outcomes
2. Ask user if agree
3. Adjust plan based on user feedback

**Step 5: Collaborate with Development Skills and Update Data**
1. Pass iteration planning and task list to development skills (e.g., cox-coding)
2. Development skills implement specific functions, COX tracks progress
3. Update task status and module completion rate
4. Confirm outcomes with user
5. Ask if proceed to next iteration

Detailed collaboration examples and dialogue flows in [references/iteration_management.md](references/iteration_management.md).

### Module Maturity Update Trigger Method

Module maturity data updated via two methods:

**Method 1: AI Active Inquiry (Main Method)**
- **Trigger Timing**: Iteration completion, important milestone
- **Inquiry Content**: Module status, completion rate, notes
- **Update Method**: AI automatically updates `app_status.json`

**Method 2: Interactive Web Support (Auxiliary Method)**
- **Applicable Scenario**: Using interactive web solution
- **Operation Method**: User directly modifies module status on web page
- **Advantage**: User can update anytime, no need to wait for AI inquiry

Detailed update process, sample dialogues and web display instructions in [references/iteration_management.md](references/iteration_management.md).

### Module and Iteration Relationship

**Same concept, different perspectives**:

| Dimension | Modules in Iteration (project_data.json) | Module Maturity (app_status.json) |
|------|--------------------------------|----------------------------|
| File | project_data.json | app_status.json |
| Perspective | Planning: What to do in this iteration | Status: How far along we are now |
| Field | `expected_completion` | `status`, `completion_rate` |
| Update Timing | During iteration planning | Continuously updated during development |

**Key Points**:
- One iteration can involve multiple modules
- One module can span multiple iterations
- Same module in both files associated via `module_id`

### Important Notes
- **COX doesn't develop directly**: COX responsible for project management and observability, development work completed by other skills
- **COX is auxiliary tool**: COX helps with planning and tracking, but doesn't write code
- **Collaboration Mode**: COX + Development Skills (e.g., cox-coding) work together
- **User Can Choose**: User can choose to use only COX for project management, or collaborate with development skills

### Notes
- Each iteration's objective must be clear and verifiable
- Prioritize implementing user-visible functions, not internal technical details
- Must confirm with user after each iteration ends
- Next iteration's plan should be based on user feedback
- Timely update `project_data.json` to reflect actual progress
- Modules involved in each iteration determined during planning, not afterwards
- Module maturity updated via two methods: AI active inquiry (main) and interactive web (auxiliary)
- Module completion rate automatically calculated by agent based on task completion, user can adjust

## Task Risk Assessment and Implementation Decision

### Overview

Each task besides `priority` (importance level) has `risk_level` (risk level). Agent automatically assesses risk level when planning tasks, judges execution strategy based on two dimensions when implementing.

### Risk Assessment Standards

Agent automatically judges task risk based on following dimensions:

| Judgment Dimension | high (high risk) | low (low risk) |
|---------|---------------|--------------|
| **Modification Scope** | Core modules, multi-file modifications | Single file, local modifications |
| **Impact Scope** | Affects multiple functions | Affects single function |
| **Modification Type** | Data structure changes, architecture adjustments | UI adjustments, text modifications |
| **Rollback Ability** | Hard to rollback | Easy to rollback |

**Examples**:
- `high`: Modify user authentication process, refactor data model, change API interface
- `low`: Adjust button style, modify error message text, add log output

### Implementation Decision Logic

**Sorting Rules**:
1. First sort by `priority`: critical > high > medium > low
2. Then group by `risk_level`

**Implementation Strategy**:

| Combination | Strategy | Explanation |
|-----|------|------|
| Critical + Low | Batch processing | Can do multiple tasks together, batch verification |
| Critical + High | Individual processing + Immediate verification | Do one by one, verify immediately after each completion |
| High + Low | Batch processing | Can do multiple tasks together, batch verification |
| High + High | Individual processing + Immediate verification | Do one by one, verify immediately after each completion |
| Medium/Low + Low | Batch processing | Can do multiple tasks together |
| Medium/Low + High | Individual processing | Suggest individual processing, decide whether to verify immediately based on situation |

**Core Principles**:
- ✅ Low-risk tasks can be modified together, batch verification, improve efficiency
- ❌ Don't mix high-risk and multiple low-risk tasks together
- ❌ Don't not verify promptly after completing high-risk task
- ✅ After implementing high-risk task, remind user to verify immediately

Detailed user reminder formats, sample workflows and best practices in [references/iteration_management.md](references/iteration_management.md).

## User Feedback Processing Flow

### Overview

When user marks module as `has_issue` on interactive web page, Agent should record issue, handle by priority when planning next iteration.

### Priority Guide

| Priority | Type | Example |
|----------|------|----------|
| Critical | Security Issue | Data leak, authentication bypass |
| High | Functional BUG | Core function unusable, crashes |
| High | Performance Issue | Slow response, timeouts |
| Medium | UI/UX Optimization | "Not aesthetic enough", hard to use |
| Medium | Small BUG | Typos, small style issues |
| Low | Feature Suggestions | "Would be nice if could add..." |

### Process Overview

```
User marks has_issue
    ↓
    Record issue (issue ID, priority, affected module)
    ↓
    Continue current work (don't interrupt)
    ↓
    When user says "continue" or "plan next iteration"
    ↓
    Collect all pending items:
    - Existing TODO tasks
    - User feedback issues
    ↓
    Evaluate priority for all items
    ↓
    Plan next iteration based on priority
    ↓
    Execute tasks according to plan
    ↓
    Ask user for confirmation after completion
    ↓
    Update module status after user confirms
```

### Processing Principles

1. **Don't interrupt current work**: After recording user feedback, continue completing current iteration
2. **Batch processing**: When planning next iteration, evaluate all pending items and feedback uniformly
3. **Priority-driven**: High-priority issues processed first
4. **User confirmation**: Must get user confirmation before updating status after resolving issue

Detailed workflow, priority matrix, and scenario handling in [references/agent-workflows.md](references/agent-workflows.md).

## Issue Tracking and Response

### Overview

When encountering complex or recurring issues, Agent should actively initiate issue tracking process to ensure systematic handling and continuous monitoring.

### Trigger Conditions

Agent should actively trigger issue tracking when:
1. **Complex Issues**: Involving multiple modules, requiring multi-step resolution
2. **Recurring Issues**: Same issue appears 2+ times in conversation without resolution

### Response Process

1. **Identify Issue and Determine Affected Modules**
2. **Update project_data.json**: Add TODO task with issue details
3. **Update test_metrics.json**: Add tracing point suggestions
4. **Update project_data.json**: Add assumption analysis
5. **Call skill-manager**: Store issue information
6. **Report User**: Inform taken measures

Detailed process, implementation steps, and examples in [references/issue_tracking_details.md](references/issue_tracking_details.md).

## Data Format Reference

### project_data.json
Contains project iteration and task information. Format specification in [references/data_format.md](references/data_format.md).

### app_status.json
Contains application module status information. Format specification in [references/data_format.md](references/data_format.md).

### test_metrics.json
Contains test metrics and anomaly information. Format specification in [references/data_format.md](references/data_format.md).

## Common Issues

### JSON Format Issues
When encountering "Extra data" error during parsing, likely contains invisible characters. Solution: Use Python to re-read and write file, or use `python -m json.tool` to verify format.

### Module ID Consistency
Ensure module IDs consistent between project_data.json and app_status.json. Inconsistent IDs cause data association failure.

### File Permissions
On some systems, may encounter permission issues when modifying files. Solutions: Use Python os module instead of bash commands, or modify file permissions.

Detailed troubleshooting methods and solutions in [references/troubleshooting.md](references/troubleshooting.md).

## Best Practices

1. **Use Scripts**: Always use data generation scripts instead of manually editing JSON files
2. **Regular Updates**: Update data files regularly to reflect actual project status
3. **Meaningful Iterations**: Give iterations meaningful names instead of generic "Iteration N"
4. **User-Centric Modules**: Define modules from user perspective, not technical implementation
5. **Risk Awareness**: Assess task risks and adjust implementation strategy accordingly
6. **Collaborative Workflow**: Use COX for planning and tracking, other skills for implementation
7. **Continuous Feedback**: Regularly collect user feedback and incorporate into planning

By following these practices, you can maximize the benefits of COX for project management and observability.