---
name: code-observer
description: Code debugging assistant, helps you see how code runs. When you say "I want to see why this function is so slow", "code errors during execution, don't know where the problem is", "business logic too complex, can't clarify execution order", I'll help trace code execution paths, find slow points, locate error causes. When discovering skill optimization points, will ask whether to invoke skill-evolution-driver for optimization
dependency: {}
---

# Code Debugging Assistant

## Task Objectives
- This Skill is used to: Help you better understand how code runs, more intuitive and simple than traditional breakpoint debugging
- Capabilities include:
  - Tell you code execution order, which functions were called
  - Find where code runs slow (which functions take long time)
  - Help locate error causes (where exception thrown, how exception propagated)
  - Provide specific code modification suggestions
- Trigger Conditions: When you say "observe code execution", "code quality", "optimize code", "code runs slow", "don't know where error is", "logic too complex can't clarify", "want to see how code executes" or similar expressions

## Operation Steps

### 1. Environment Preparation and Data Acquisition

**Step 1.1: Debugging Environment Confirmation**
- Agent asks developer about debugging environment status
- If debugging environment terminal not open, provide opening guidance:
  - Command or operation steps to open application terminal
  - Specific configuration to start debugging tool (possibly called cox or similar)
- Wait for developer to confirm debugging environment ready

**Step 1.2: Query Data Storage Location**
- Before getting logs or metrics information, must first invoke `skill-manager` skill to query debugging tool's (such as cox) data storage location information
- Query content:
  - Storage path for log file (observability.log)
  - Storage path for metrics data (metrics.prom) (if any)
  - Storage path for application status data (app_status.json) (if any)
  - Storage path for project data (project_data.json) (if any)
  - Storage path for test data (test_metrics.json) (if any)
- Get actual file paths based on query results

**Step 1.3: Acquire Observability Data**
- Agent reads following data files based on queried storage paths:
  - Log files (from queried paths)
  - Metrics data (optional, from queried paths)
  - Application status data (optional, from queried paths)
  - Project data (optional, from queried paths)
  - Test data (optional, from queried paths)

### 2. Data Parsing and Analysis

**Step 2.1: Parse Log Data**
Invoke `scripts/parse_logs.py` to process (using actual paths queried from skill-manager):
```bash
python3 scripts/parse_logs.py --log-file <log path queried from skill-manager> --output ./parsed_logs.json
```
- Extract execution path information
- Identify function calls and durations
- Locate exception throw positions

**Step 2.2: Parse Metrics Data** (if any)
Invoke `scripts/parse_prometheus.py` to process (using actual paths queried from skill-manager):
```bash
python3 scripts/parse_prometheus.py --prom-file <metrics path queried from skill-manager> --output ./parsed_metrics.json
```

**Step 2.3: Analyze Multi-Dimensional Data** (if any)
Invoke corresponding analysis scripts (using actual paths queried from skill-manager):
```bash
python3 scripts/analyze_app_status.py --input <app_status path queried from skill-manager> --output ./app_analysis.json
python3 scripts/analyze_project_data.py --input <project_data path queried from skill-manager> --output ./project_analysis.json
python3 scripts/analyze_test_metrics.py --input <test_metrics path queried from skill-manager> --output ./test_analysis.json
```

### 3. Full Process Tracing Report Generation

**Step 3.1: Generate Tracing Report**
Invoke `scripts/generate_trace_report.py` to generate full-process visualized tracing:
```bash
python3 scripts/generate_trace_report.py \
  --logs ./parsed_logs.json \
  --metrics ./parsed_metrics.json \
  --app-status ./app_analysis.json \
  --project-data ./project_analysis.json \
  --test-metrics ./test_analysis.json \
  --output ./trace_report.md
```

**Step 3.2: Report Content Structure**
- Execution path visualization: Function call chain and timeline
- Performance metrics analysis: Duration distribution, bottleneck identification
- Exception tracing: Exception stack, trigger path, root cause analysis
- Cross-dimensional correlation: Project/application/test status correlation analysis

### 4. Problem Diagnosis and Solution Generation

**Step 4.1: Agent Analyzes Tracing Report**
- Identify performance bottlenecks: high-duration functions, frequently-called hot paths
- Locate exception root causes: Exception propagation paths, prerequisite condition analysis
- Assess code quality: Complexity, duplicate code, potential risks

**Step 4.2: Generate Solutions**
- For performance issues: Optimization suggestions, caching strategies, concurrency processing solutions
- For exception issues: Exception handling enhancement, boundary condition checks, defensive programming
- For architecture issues: Module decoupling, dependency optimization, design pattern application

**Step 4.3: Code Fix Suggestions**
- Provide specific code modification examples
- Explain modification rationale and expected effects
- Give testing and verification suggestions

### 5. Execution Log Recording

**Step 5.1: Data Integrity Check**
- Check whether all data required by this skill can be obtained from debugging tool (such as cox):
  - Log files: Exist and readable
  - Metrics data: Exists (optional)
  - Application status data: Exists (optional)
  - Project data: Exists (optional)
  - Test data: Exists (optional)
- Assess data quality issues:
  - Whether logs contain necessary information (time, level, message, etc.)
  - Whether metrics data format is correct
  - Whether JSON data structure is complete and valid

**Step 5.2: Problem Identification and Recording (Mandatory)**
- This skill depends on other skills' (such as cox) output files for code analysis
- **When discovering following situations, MUST invoke `skill-manager` skill to record issues**:
  - **Dependency file doesn't exist**: Such as cox's observability.log file doesn't exist
  - **Dependency file unreadable**: File exists but cannot be read (permission issue, file corruption, etc.)
  - **Dependency file format doesn't meet requirements**: File exists but format doesn't meet this skill's parsing requirements
  - **Dependency file content incomplete**: File exists but lacks required fields or data
  - **Dependency file quality doesn't meet needs**: File content quality insufficient to support effective code analysis
  - **Data read failure**: Exception or error occurs when attempting to read dependency files
  - **Data parsing failure**: File read succeeds but errors during parsing
  - **Any other dependency issues affecting normal skill execution**

- **Importance of Problem Recording**:
  - This skill's execution depends on other skills' output results
  - If dependency files don't exist or don't meet needs, this skill cannot execute analysis normally
  - Recording these issues helps improve dependent skills' data output
  - Provides problem tracking and optimization basis for skill collaboration

**Step 5.3: Problem Record Format (Mandatory)**
When invoking `skill-manager`, must strictly follow following JSON format to record issues:

```json
{
  "level": "critical / high / medium / low",
  "message": "[Problem Phenomenon] [Problem Cause] [Problem Impact]"
}
```

**Format Description**:
- `level` (required): Issue severity
  - `critical`: Critical issue, completely blocks skill execution (such as critical dependency file missing)
  - `high`: High priority issue, seriously affects skill functionality (such as main dependency file format error)
  - `medium`: Medium priority issue, partially affects functionality (such as optional dependency file missing)
  - `low`: Low priority issue, minor impact (such as partial data incomplete)

- `message` (required): Issue description, must include three parts
  - [Problem Phenomenon]: Specifically describe what problem occurred
  - [Problem Cause]: Analyze problem's cause
  - [Problem Impact]: Explain problem's impact on this skill's execution

**Format Examples**:

```json
{
  "level": "critical",
  "message": "[No observability.log file][cox skill's intermediate solution (Web interface) doesn't generate log files][Cannot perform execution path tracing, this skill cannot work normally]"
}
```

```json
{
  "level": "medium",
  "message": "[metrics.prom file format incorrect][Missing required TYPE comment lines][Cannot parse Prometheus metrics, performance analysis functionality limited]"
}
```

```json
{
  "level": "high",
  "message": "[observability.log file lacks timestamp field][Log output configuration incomplete][Cannot track code execution path chronologically, tracing report incomplete]"
}
```

**Step 5.4: Value Proposition**
- Record dependent skills' (such as cox) data output issues
- Help improve dependent skills' data quality and output format
- Provide problem tracking and continuous optimization mechanism for skill collaboration
- Ensure this skill can normally execute code analysis tasks

**Step 5.5: Skill Optimization Point Identification and Suggestions (Agent Processing)**

Agent needs to determine whether discovered issues involve skill optimization points:

**Judgment Criteria**:
1. **Skill Configuration Issues**: Issues involve skill's configuration information (such as SKILL.md lacks required fields, version field missing, etc.)
2. **Script Issues**: Issues involve skill's script output (such as log format incorrect, data fields missing, etc.)
3. **Documentation Issues**: Issues involve skill's documentation (such as unclear description, incomplete steps, etc.)
4. **Integration Issues**: Issues involve skill collaboration (such as interface incompatibility, data format inconsistency, etc.)

**Optimization Point Identification Examples**:

**Example 1: Log Format Issue → Skill Optimization Point**
- Issue description: `observability.log file lacks timestamp field`
- Optimization point judgment: Involves cox skill's log output format
- Optimization type: Script output optimization
- Suggested action: Invoke skill-evolution-driver skill

**Example 2: Configuration Missing Issue → Skill Optimization Point**
- Issue description: `cox's SKILL.md lacks version field`
- Optimization point judgment: Involves skill configuration information
- Optimization type: Format improvement
- Suggested action: Invoke skill-evolution-driver skill

**Example 3: Data Quality Issue → Non-Skill Optimization Point**
- Issue description: `Test coverage data incomplete`
- Optimization point judgment: Belongs to user data issue, doesn't involve skill itself
- Optimization type: Data completion
- Suggested action: Remind user to supplement data

**Agent Response Flow**:

1. **Analyze discovered issue list**
   - Iterate through all issues recorded in Step 5.2
   - Determine whether each issue involves skill optimization points

2. **Identify Skill Optimization Points**
   - If issue involves skill configuration, script output, documentation or collaboration
   - Mark as skill optimization point
   - Record involved skill name and optimization type

3. **Ask User**
   If skill optimization points exist, Agent should ask user:

   ```
   During this code analysis, discovered following skill optimization points:

   1. Skill: cox
      - Optimization type: Script output optimization
      - Issue: observability.log file lacks timestamp field
      - Impact: Cannot track code execution path chronologically

   Need to invoke skill-evolution-driver skill to handle these optimization points? (y/n)
   ```

4. **Handle User Selection**

   **Select y (Yes)**:
   - Invoke skill-evolution-driver skill
   - Pass optimization point list (skill name, optimization type, issue description)
   - Wait for skill-evolution-driver to execute optimization

   **Select n (No)**:
   - Skip optimization point handling
   - Continue executing subsequent steps (such as generating tracing report)
   - Suggest user can manually invoke skill-evolution-driver later

**Precautions**:
- Optimization point identification is Agent's analysis judgment, not simple keyword matching
- Need to combine issue context and skill knowledge for judgment
- If uncertain whether it's a skill optimization point, can consult user
- Optimization point identification doesn't affect this skill's core functionality (code analysis)

## Resource Index

### Essential Scripts
- `scripts/parse_logs.py`: Parse structured logs, extract execution paths, function calls and exception information
- `scripts/parse_prometheus.py`: Parse Prometheus metrics data, extract performance metrics
- `scripts/analyze_app_status.py`: Analyze application module status and completion rates
- `scripts/analyze_project_data.py`: Analyze project iteration progress and task status
- `scripts/analyze_test_metrics.py`: Analyze test instrumentation points and anomalies
- `scripts/generate_trace_report.py`: Integrate multi-dimensional data, generate full-process visualized tracing report

### Domain References
- `references/log_format.md`: Log format specifications and parsing rules (read timing: before parsing logs)
- `references/prometheus_format.md`: Prometheus metrics format specifications (read timing: before parsing metrics)
- `references/json_data_format.md`: JSON data format specifications (read timing: before analyzing JSON data)
- `references/trace_analysis_guide.md`: Tracing analysis guide and methodology (read timing: before generating report)

### Output Assets
- `assets/trace_templates/execution_trace.md`: Execution tracing report template
- `assets/trace_templates/performance_metrics.md`: Performance metrics report template
- `assets/trace_templates/error_analysis.md`: Exception analysis report template

## Precautions

- **Important**: Before getting logs or metrics information, must first invoke `skill-manager` skill to query debugging tool's (such as cox) data storage location information
- **Very Important (Mandatory)**: During execution, if discovered dependent output files don't exist or don't meet requirements, must invoke `skill-manager` skill to record issues following Step 5.3 format
- **Mandatory Rule**: When dependency files missing, unreadable, format error, content incomplete or quality doesn't meet needs, must record issues, must not skip
- Only read reference documents when needed, keep context concise
- Technical data processing prioritizes invoking scripts (log parsing, metrics extraction, report generation)
- Problem analysis and solution generation completed by Agent, fully leveraging its reasoning capabilities
- Tracing reports use Markdown format, facilitating visualized display and version control
- Support progressive analysis: Can use only log data, or fuse multi-dimensional data to enhance analysis depth
- All data file paths must be obtained from `skill-manager` querying debugging tool
- Problem recording must strictly follow Step 5.3 JSON format, include level and message fields

## Usage Examples

### Example 1: Basic Code Tracing
**User Scenario**: "I want to see how this function executes, why so slow"
**Execution Method**: Invoke skill-manager query + scripts + Agent analysis + execution log recording
**Key Steps**:
```bash
# 1. Invoke skill-manager to query debugging tool's log storage path
# (Completed through Agent invoking skill-manager)

# 2. Parse logs (use queried actual paths)
python3 scripts/parse_logs.py --log-file <queried log path> --output ./parsed_logs.json

# 3. Generate tracing report
python3 scripts/generate_trace_report.py --logs ./parsed_logs.json --output ./trace_report.md

# 4. Agent analyzes report and generates solutions

# 5. Data integrity check and issue recording
# If issues discovered, must invoke skill-manager to record issues following Step 5.3 format
```

### Example 2: Comprehensive Code Analysis
**User Scenario**: "Help comprehensively analyze code execution, check for performance issues or errors"
**Execution Method**: Invoke skill-manager query + all scripts + Agent deep analysis + execution log recording
**Key Steps**:
```bash
# 1. Invoke skill-manager to query all data file storage paths of debugging tool
# (Completed through Agent invoking skill-manager)

# 2. Parse all data sources (use queried actual paths)
python3 scripts/parse_logs.py --log-file <queried log path> --output ./parsed_logs.json
python3 scripts/parse_prometheus.py --prom-file <queried metrics path> --output ./parsed_metrics.json
python3 scripts/analyze_app_status.py --input <queried app_status path> --output ./app_analysis.json
python3 scripts/analyze_project_data.py --input <queried project_data path> --output ./project_analysis.json
python3 scripts/analyze_test_metrics.py --input <queried test_metrics path> --output ./test_analysis.json

# 3. Generate comprehensive analysis report
python3 scripts/generate_trace_report.py \
  --logs ./parsed_logs.json \
  --metrics ./parsed_metrics.json \
  --app-status ./app_analysis.json \
  --project-data ./project_analysis.json \
  --test-metrics ./test_analysis.json \
  --output ./trace_report.md

# 4. Agent conducts cross-dimensional correlation analysis, generates comprehensive solutions

# 5. Data integrity check and issue recording
# Check all data complete, if missing or format errors, must invoke skill-manager to record following Step 5.3 format
```

### Example 3: Performance Issue Troubleshooting
**User Scenario**: "Code runs too slow, help find where it's slow"
**Execution Method**: Invoke skill-manager query + scripts extract metrics + Agent analyze bottlenecks + execution log recording
**Key Points**:
- Invoke skill-manager to query debugging tool's log and metrics storage paths
- Parse logs to extract function call durations (use queried actual paths)
- Analyze metrics data to identify high-duration operations (use queried actual paths)
- Agent generates performance optimization suggestions (caching, concurrency, algorithm optimization)
- Check data integrity, if data missing or format errors, invoke skill-manager to record issues

### Example 4: Error Location
**User Scenario**: "Code errors during execution, don't know where problem is"
**Execution Method**: Agent analysis + skill-manager recording (mandatory)
**Key Points**:
- Discovered log file missing
- **Must** invoke `skill-manager` to record issues following Step 5.3 format:

```json
{
  "level": "critical",
  "message": "[No observability.log file][cox skill's intermediate solution (Web interface) doesn't generate log files][Cannot perform execution path tracing, this skill cannot work normally]"
}
```

**Issue Recording Description**:
- `level`: "critical" - Because log file is this skill's critical dependency, missing completely blocks skill execution
- `message`: Includes [Problem Phenomenon][Problem Cause][Problem Impact] three parts, conforms to Step 5.3 format requirements
