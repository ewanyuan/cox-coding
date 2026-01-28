---
name: cox
version: v1.0.0
description: Cox Programming - Safeguarding your AI programming experience. Helps development teams manage project progress, identify development risks, and understand system health. Provides project progress tracking, iteration management (MVP-driven), task status management, development hypothesis recording, application module monitoring, test instrumentation and anomaly analysis. Supports both static webpage and interactive webpage solutions for different environments and team sizes. Web pages display grouped by iteration, clearly presenting each iteration's progress and tasks.
dependency:
  python:
    - flask>=2.0.0  # Only required for interactive webpage solution
  system: []
---

# Cox Programming - Safeguarding Your AI Programming Experience

## Task Objectives
- **Cox's Role**: Cox is an **AI Programming Navigator**, responsible for project management and observability, not directly writing code or implementing features
- **Collaboration Mode**: Cox works in conjunction with development skills
  - Cox: Responsible for project planning, iteration management, progress tracking, issue tracking
  - Development skills (such as cox-coding): Responsible for specific feature implementation and code writing
- Capabilities include:
  1. Project Dimension: Track iteration progress, task status, development hypotheses
  2. Application Dimension: Monitor application feature module status
  3. Test Dimension: Manage test instrumentation points, analyze anomalies

## Trigger Conditions

Cox is triggered under any of the following conditions:

### Software Development Support (Core Scenario)
When users propose software development requirements, Cox should **proactively enable** project management and iteration management processes:
- **User Expression**: "Build a blog", "Develop a calculator", "Implement XX feature", "Build an e-commerce system"
- **Collaboration Process**:
  1. Cox understands requirements, plans project structure and iterations
  2. Cox generates observability data (project progress, task lists, module planning)
  3. Cox passes planning to development skills (such as cox-coding) for specific implementation
  4. Cox continuously tracks progress, updates observability data

**Example Dialogue**:
```
User: Build a calculator using Cox skill
Cox: Understood, I'll help plan the calculator project development. Let me first create project observability data...
[Invoke scripts to generate data, plan iterations and tasks]
Cox: Project planning complete, includes the following modules:
- UI Interface Module
- Calculation Logic Module
- History Module

Now I'll break down iteration tasks, then request development skills to implement specific features.
```

### Project Progress and Risks
- "Want to know project progress", "any delay risks", "iteration completion percentage"
- "View task status", "which tasks completed", "what's still pending"

### Issue Tracking
- "How to track frequent bugs", "handle recurring issues", "need to record unresolved problems"
- "What risks exist", "any anomalies needing attention"

### Quality Assurance
- "Need to monitor API performance", "discover system anomalies", "test coverage status"
- "API response slow", "system has anomalies"

### Team Collaboration
- "Need to share project information", "let team understand status", "need visualization dashboard"

## Deployment Solution Selection

Before starting use, select a deployment solution based on team requirements. See [references/deployment_details.md](references/deployment_details.md) for detailed configuration instructions.

### Static Webpage Solution
- **Characteristics**: Generates static HTML files, data inlined in HTML, no separate JSON files needed
- **Use Cases**: Restricted environments (such as online sandbox environments), quick requirement validation
- **Usage Barrier**: No additional dependencies required (no Flask installation needed)
- **Usage**: Invoke `scripts/run_web_observability.py --mode static`, generates `observability.html` file
- **Refresh Method**: Click refresh button to re-render data (static mode doesn't support auto-refresh)

### Interactive Webpage Solution (Recommended)
- **Characteristics**: Provides local Web interface, supports real-time data refresh (every 30 seconds), supports interaction
- **Use Cases**: Need real-time monitoring
- **Usage Barrier**: Requires Flask installation (`pip install flask`)
- **Usage**: Invoke `scripts/run_web_observability.py --mode web`, visit http://localhost:5000

### Comprehensive Solution (Not Currently Available)
- Characteristics: Use Prometheus+Grafana professional observability tools, Docker deployment
- Use Cases: Preparing to migrate to production environment, need professional monitoring capabilities
- Status: Not yet available, pending data integration and configuration solution completion

## Quick Start

### Step 1: Generate Observability Data

**Recommended Method: Use Script to Generate Data**

To ensure data format is 100% compliant, it's recommended to use the data generation script:

```bash
# Method 1: Generate minimal dataset (quick experience)
python scripts/generate_observability_data.py \
  --mode minimal \
  --project-name "My Project" \
  --app-name "My App"

# Method 2: Generate custom modules (recommended)
# Agent should break down tasks based on actual requirements, not use example tasks
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Calculator Project" \
  --app-name "Calculator App" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"}]'

# Method 3: Generate complete example (includes test suite framework, but tasks, instrumentation points, anomalies left empty)
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Calculator Project" \
  --app-name "Calculator App" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"}]'
```

The script generates three JSON files in the current directory:
- `project_data.json`: Project iteration and task data
- `app_status.json`: Application module status data
- `test_metrics.json`: Test instrumentation and anomaly data

**Core Principles**:
- **Example data provides minimal skeleton only**, does not populate any fake business data
- **Tasks, instrumentation points, anomalies default to empty**, to be filled by Agent based on actual situation
- Everything based on real data, avoid misleading

**Regarding Tasks**:
- **Script behavior**: By default generates empty tasks array, no additional parameters needed. Agent should fill real data after breaking down tasks based on actual requirements
- **Task fields**:
  - `task_id`: Task ID (such as TASK-001)
  - `task_name`: Task name (specific description, such as "Design calculator UI interface")
  - `status`: Task status (todo/in_progress/completed/delayed)
  - `assignee`: Assignee (optional, fill if team collaboration needed)
  - `priority`: Priority (low/medium/high/critical)
  - `tags`: Tags (optional, for categorization)

**Regarding Instrumentation Points and Anomalies**:
- **Default to empty**: Script-generated tracing_points and anomalies are both empty arrays `[]`
- **Real data filling**: Should be populated by Agent based on actual monitoring data
- **Data fields**:
  - `tracing_points`: Test instrumentation points (module, location, status, metric type)
  - `anomalies`: Anomaly records (type, description, severity, status, occurrence count, time)

**Custom Module Description**:
- Use `--modules` parameter to define modules actually needed by project
- Module list in JSON format, contains id and name fields
- When Agent invokes script, should automatically infer appropriate modules based on project requirements

**Subsequent Use**:
- Directly modify generated JSON files to fit actual project
- See [references/data_format.md](references/data_format.md) for data format specifications

### Step 2: Select Solution and Launch

**Static Webpage Solution (Recommended)**:
```bash
# Generate static HTML file (no Flask required)
# Data inlined into HTML, no separate JSON files needed
python scripts/run_web_observability.py \
  --mode static \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output observability.html

# Open observability.html directly in browser to view interface
# Data inlined, no other files needed
```

**Interactive Webpage Solution**:
```bash
# Launch Web server (first install Flask: pip install flask)
python scripts/run_web_observability.py \
  --mode web \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 127.0.0.1 \
  --port 5000

# Visit http://127.0.0.1:5000 to view interface, data auto-refreshes every 30 seconds
```

**Notes**:
- Static mode: Data inlined into HTML file, fixed after generation, click refresh button to re-render
- Web mode: Real-time data updates, no need to regenerate, visit http://127.0.0.1:5000 to view interface

### Step 3: Invoke skill-manager to Store Deployment Information

After deployment complete, invoke **skill-manager** skill to store deployment information, facilitating future management and skill collaboration.

See [references/deployment_details.md](references/deployment_details.md) for detailed invocation methods.

### Step 4: Continuously Update Data

During development, periodically update data files, then regenerate static HTML (static mode) or refresh page (Web mode). Agent can assist you in analyzing existing data and identifying content needing updates.

### Step 5: Post-Execution Guidance

**Agent should proactively remind user**:
After executing Cox skill, Agent should proactively remind user to view project page and inform current status and next action recommendations.

**Standard Guidance Process**:

1. **Inform user data generated**
   - Clearly state project data files have been generated
   - State project page has been generated

2. **Provide viewing method**
   - Static mode: Open observability.html in browser
   - Web mode: Visit http://127.0.0.1:5000

3. **Summarize current iteration plan**
   - Read current_iteration from project_data.json
   - List all tasks in current iteration (task_name, status)
   - State completed/in-progress/pending task counts

4. **Identify next actions**
   - Find tasks with status pending or todo
   - Sort by priority: critical > high > medium > low
   - Recommend next task to handle

5. **Coordinate other skills**
   - For tasks requiring development, suggest invoking development skill (such as cox-coding)
   - For tasks requiring testing, suggest updating test_metrics.json
   - For tasks requiring deployment, suggest invoking skill-manager

6. **User confirmation**
   - Ask user: "Which task would you like to start handling now?"
   - Invoke corresponding skill based on user selection

**Example Dialogue**:
```
Agent: Project data generation complete.

You can view project page through:
- Static mode: Open observability.html in browser
- Web mode: Visit http://127.0.0.1:5000

Current iteration: Iteration 1 - Core Feature Development
- Completed: 2 tasks
- In Progress: 1 task
- Pending: 3 tasks

Recommended next actions:
1. Complete task "User Login API" (priority: high)
2. Start task "Data Persistence Module" (priority: medium)

Which task would you like to start handling now? Or do you have other ideas?
```

## Core Functionality Description

### Agent-Processable Functions
- **Requirement Analysis & Module Planning**: Based on user requirements (such as "Build a calculator"), analyze core features, automatically infer appropriate module list
- **Data Generation Guidance**: Generate custom module list based on project requirements, invoke data generation script
- **Data Analysis**: Analyze existing observability data, identify project risks and bottlenecks
- **Usage Guidance**: Answer solution selection and deployment questions
- **Data Update Recommendations**: Provide data update recommendations based on development progress
- **Issue Tracking & Response**: Identify complex issues and recurring issues, automatically update observability data (TODO tasks, hypothesis analysis, instrumentation recommendations)

### Script-Implemented Functions
- **Data Generation**: `scripts/generate_observability_data.py` generates compliant observability data (avoiding LLM hallucinations)
- **Data Format Validation**: `scripts/collect_data.py` validates JSON data format compliance
- **Static Webpage Generation**: `scripts/run_web_observability.py --mode static` generates static HTML files (data inlined, no Flask)
- **Interactive Webpage Service**: `scripts/run_web_observability.py --mode web` launches Flask Web server
- **Skill-manager Storage Tool**: `scripts/store_to_skill_manager.py` stores deployment information and issue tracking information

## Iteration Management Process

### Trigger Conditions
When user proposes need to develop new features, build new projects, or implement complex requirements, Agent should proactively enable iteration management process.

### MVP-Driven Iteration Breakdown Principles

Agent should follow **MVP (Minimum Viable Product)** principles when breaking down iterations:

1. **First Iteration**: Core features
   - Identify user-visible core features
   - Implement in simplest way
   - Quick delivery for user confirmation

2. **Second Iteration**: Enhanced features
   - Adjust based on user feedback
   - Add secondary features
   - Optimize user experience

3. **Subsequent Iterations**: Improvement & optimization
   - Gradually refine details
   - Performance optimization
   - Edge case handling

### Iteration Management Process

**Step 1: Requirement Analysis & Iteration Breakdown**
1. Understand core objective of user requirements
2. Identify user-visible feature points
3. Break into multiple iterations by priority
4. Each iteration focuses on a clear objective

**Step 2: Invoke Data Generation Script (Using Custom Modules)**
Agent should automatically infer module list based on project requirements:

```bash
# Example: Calculator project
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "Calculator Project" \
  --app-name "Calculator App" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI Interface Module"},{"id":"MOD-002","name":"Calculation Logic Module"},{"id":"MOD-003","name":"History Module"}]'
```

**About Task Generation**:
- Script follows minimal dataset principle, generates no placeholder tasks
- tasks array always empty `[]`, to be filled with real data by Agent or user manually
- All task fields (task_id, task_name, assignee, etc.) should be filled based on actual project requirements

**Step 3: Agent Breaks Down Tasks and Populates Data**
1. Analyze user requirements, break down specific tasks
2. Populate tasks array for each iteration
3. Tasks should include specific descriptions (such as "Design calculator UI interface", "Implement addition/subtraction/multiplication/division operations")
4. assignee field optional, only fill when team collaboration needed
5. Set status for each task (todo/in_progress/completed)

**Example**: Calculator project task breakdown
```json
{
  "iteration_id": "ITER-001",
  "iteration_name": "First Iteration",
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "UI Interface Module",
      "expected_completion": 0.8
    }
  ],
  "tasks": [
    {
      "task_id": "TASK-001",
      "task_name": "Design Calculator UI Interface",
      "status": "completed",
      "priority": "high",
      "tags": ["UI", "Design"]
    },
    {
      "task_id": "TASK-002",
      "task_name": "Implement Basic Addition/Subtraction/Multiplication/Division Operations",
      "status": "in_progress",
      "priority": "critical",
      "tags": ["Core Features"]
    }
  ]
}
```

**Step 4: Confirm Iteration Plan with User**
1. Present first iteration plan and expected outcomes
2. Ask user if agree
3. Adjust plan based on user feedback

**Step 5: Collaborate with Development Skills and Update Data**
1. Pass iteration planning and task list to development skills (such as cox-coding)
2. Development skills implement specific features, Cox tracks progress
3. Update task status and module completion rate
4. Confirm outcomes with user
5. Ask whether to proceed to next iteration

### Cox and Development Skill Collaboration Example

```
User: Build a calculator

Cox: Understood, I'll help plan the calculator project. Let me first create observability data...

[Cox invokes scripts to generate data, plan iterations and tasks]

Cox: Project planning complete:
📋 Project name: Calculator Project
📦 Module planning:
  - UI Interface Module
  - Calculation Logic Module
  - History Module

📅 First iteration plan:
  - Design calculator UI interface
  - Implement addition/subtraction/multiplication/division operations
  - Expected completion time: 7 days

[Task list generated, now requesting development skills to start implementation...]

Development Skill: Task received, starting implementation...

[Cox continuously tracks progress, updates task status]

Cox: First iteration progress update:
✅ UI interface design - Completed
✅ Basic calculation operations - Completed
⏳ Testing and optimization - In Progress (60%)

Current module completion rate: 75%
Proceed to second iteration?
```

### Module Maturity Update Trigger Methods

Module maturity data updated via two methods:

**Method 1: AI Proactive Inquiry (Primary Method)**
- **Trigger Timing**: Periodically or at key milestones (such as iteration completion, important milestones)
- **Inquiry Content**:
  1. Feedback on current involved modules
  2. Module current status (pending/in_progress/developed/confirmed/optimized)
  3. Module completion rate (AI auto-calculates based on task completion, user can adjust)
  4. Whether need to add notes
- **Update Method**: AI automatically updates app_status.json

**Example Dialogue**:
```
Agent: Iteration 1 complete, let me confirm module progress:
- User Module (expected completion rate 80%)
  - Current task completion: 3/4 completed
  - Auto-calculated completion rate: 75%
  - Please confirm current module status and actual completion rate?

User: Status is in_progress, actual completion rate is 80%

Agent: Module data updated:
- User Module: status in_progress, completion rate 80%, last updated 2024-01-26
```

**Method 2: Interactive Webpage Support (Auxiliary Method)**
- **Use Case**: User uses interactive webpage solution (--mode web)
- **Operation Method**: User can directly select/modify module status labels on webpage
- **AI Behavior**:
  1. AI continuously tracks data changes on webpage
  2. Uses data to drive subsequent decision strategies
  3. When user modifies module status, AI will notice and confirm on next interaction
- **Advantage**: User can update anytime, no need to wait for AI inquiry

### Webpage Display Description

Cox's webpage displays grouped by iteration:
- **Iteration Card**: Each iteration is a separate card
- **Current Iteration Marker**: Current iteration card has blue border and "Current" label
- **Progress Bar**: Shows task completion progress for each iteration
- **Task List**: Task list under each iteration, includes status, assignee, priority
- **Involved Modules**: Shows modules involved in each iteration and expected completion rate
- **Development Hypotheses**: Shows development hypotheses and verification status for each iteration

**Module Maturity Display**:
- **Module Card**: Shows status and completion rate for each module
- **Progress Bar**: Visualizes module completion rate
- **Last Update Time**: Shows last update time of module data
- **Auto Update**: AI proactive inquiry or user modification on webpage auto-updates

### Example Scenario

**User says**: "Use Cox skill to build a blog"

**Agent Response**:
1. Understand requirement: User wants Cox to assist blog system development
2. Cox plans project:
   - Iteration 1: Core blog features (article list, article detail, publish article)
   - Iteration 2: Comment feature
   - Iteration 3: User system
3. Cox generates observability data (project progress, task list, module planning)
4. Cox presents Iteration 1 plan to user
5. After user confirmation, Cox passes tasks to development skill (such as cox-coding)
6. Development skills implement features, Cox continuously tracks progress and updates observability data
7. Upon completion, ask for module feedback, update module maturity
8. Ask whether to proceed to Iteration 2

**Step 6: Advance to Next Iteration**
1. Plan next iteration based on user feedback
2. Plan tasks and involved modules for next iteration
3. Update iteration plan in project_data.json
4. Repeat steps 4-5

### Important Notes
- **Cox doesn't directly develop**: Cox responsible for project management and observability, development done by other skills
- **Cox is auxiliary tool**: Cox helps plan and track, but doesn't write code
- **Collaboration Mode**: Cox + development skills (such as cox-coding) work together
- **User can choose independently**: User can choose to only use Cox for project management, or use together with development skills

### Precautions
- Each iteration objective must be clear and verifiable
- Prioritize user-visible features, not internal technical details
- Must confirm with user after each iteration
- Next iteration plan should be based on user feedback
- Timely update project_data.json to reflect actual progress
- Modules involved in iteration determined during planning, not asked afterwards
- Module maturity updated via two methods: AI proactive inquiry (primary) and interactive webpage (auxiliary)
- Module completion rate auto-calculated by Agent based on task completion, user can adjust

## Issue Tracking & Response

### Trigger Conditions
Agent should proactively trigger issue tracking and response when:
1. **Complex Issues**: User feedback involves multiple modules, requires multi-step resolution, or needs cross-team collaboration
2. **Recurring Issues**: Same issue appears multiple times in conversation (2 or more), and fails to resolve smoothly

### Response Steps Overview
1. Identify issue and determine affected modules
2. Update project dimension TODO list
3. Add issue-related hypothesis analysis
4. Suggest adding related instrumentation points
5. Invoke skill-manager to store issue information

See [references/issue_tracking_details.md](references/issue_tracking_details.md) for detailed response process and usage examples.

### Agent Processing Flow
1. Monitor conversation context, identify complex issues and recurring issues
2. Analyze issue impact scope, determine related modules
3. Generate issue ID (format: ISSUE-NNN)
4. Update project_data.json: add TODO tasks and hypotheses
5. Update test_metrics.json: add instrumentation recommendations
6. Invoke skill-manager to store issue tracking information
7. Report taken observation update measures to user

## Resource Index
- **Data Format Specifications**: See [references/data_format.md](references/data_format.md) (format definitions, validation rules, and examples for all data files)
- **Troubleshooting Guide**: See [references/troubleshooting.md](references/troubleshooting.md) (common issues, error codes, and solutions)
- **Deployment Details**: See [references/deployment_details.md](references/deployment_details.md) (detailed configuration and usage instructions for both solutions)
- **Issue Tracking Details**: See [references/issue_tracking_details.md](references/issue_tracking_details.md) (complete process and examples for issue tracking and response)
- **Deployment Guide**: See [references/deployment_guide.md](references/deployment_guide.md) (detailed deployment steps, configuration instructions, and best practices for both solutions)
- **Data Generation Tool**: See [scripts/generate_observability_data.py](scripts/generate_observability_data.py) (generate compliant observability data, avoid LLM hallucinations)
- **Data Collection Tool**: See [scripts/collect_data.py](scripts/collect_data.py) (data format validation and collection tool)
- **Web Interface Server**: See [scripts/run_web_observability.py](scripts/run_web_observability.py) (static/Web dual-mode interface generation)
- **Skill-manager Storage Tool**: See [scripts/store_to_skill_manager.py](scripts/store_to_skill_manager.py) (store deployment information and issue tracking information to skill-manager)
- **Web Interface Templates**: See [assets/web_templates/](assets/web_templates/) (HTML templates and style files)
- **Docker Configuration**: See [assets/docker_compose/](assets/docker_compose/) (complete configuration for comprehensive solution)

## Precautions
- Both solutions use same data format, can switch anytime based on requirements
- Data files support incremental updates, no need to rewrite entire content each time
- Recommend using scripts rather than LLM to generate data, avoiding format errors
- Interactive solution Web interface defaults to port 5000, can modify via parameters
- Comprehensive solution requires Docker environment, recommend using static solution first to validate requirements

## Best Practices
- **Data Initialization**: Use `generate_observability_data.py` script to generate initial data files, ensure 100% correct format
- **Data Updates**: Recommend updating observability data daily or after each iteration
- **Data Reuse**: Data files can be shared by multiple skills and tools, avoiding duplicate creation
- **Solution Selection**: Use static solution for restricted environments (such as sandboxes), interactive solution for real-time monitoring needs
- **Hypothesis Management**: Record development hypotheses in project_data.json, regularly verify and update
- **Module Status Tracking**: Use application dimension monitoring to track module status, identify development bottlenecks
- **Anomaly Priority**: Prioritize handling high-frequency anomalies in test dimension, improve quality
- **Issue Response**: Utilize issue tracking functionality, timely update observability data, accelerate issue resolution
- **Data Validation**: Before generating observability interface, use check scripts to validate data consistency:
  ```bash
  # Check module consistency
  python scripts/check_module_consistency.py

  # Validate JSON format
  python -m json.tool project_data.json > /dev/null
  python -m json.tool app_status.json > /dev/null
  python -m json.tool test_metrics.json > /dev/null
  ```
- **Troubleshooting**: When encountering issues, see [references/troubleshooting.md](references/troubleshooting.md)
