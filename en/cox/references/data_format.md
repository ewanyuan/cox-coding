# Observability Data Format Specification

## Table of Contents
- [Project Data Format (project_data.json)](#project-data-format-project_datajson)
- [Application Status Format (app_status.json)](#application-status-format-app_statusjson)
- [Test Metrics Format (test_metrics.json)](#test-metrics-format-test_metricsjson)
- [Data Validation Rules](#data-validation-rules)

## Project Data Format (project_data.json)

### Structure Definition
```json
{
  "project_name": "Project Name",
  "current_iteration": "Iteration Number",
  "iterations": [
    {
      "iteration_id": "Unique Iteration Identifier",
      "iteration_name": "Iteration Name",
      "status": "Iteration Status",
      "start_date": "Start Date",
      "end_date": "End Date",
      "tasks": [
        {
          "task_id": "Unique Task Identifier",
          "task_name": "Task Name",
          "status": "Task Status",
          "assignee": "Responsible Person",
          "priority": "Priority",
          "risk_level": "Risk Level",
          "tags": ["Tag1", "Tag2"]
        }
      ],
      "modules": [
        {
          "module_id": "Unique Module Identifier",
          "module_name": "Module Name",
          "expected_completion": 0.8
        }
      ],
      "assumptions": [
        {
          "assumption_id": "Unique Assumption Identifier",
          "description": "Assumption Description",
          "status": "Validation Status",
          "validation_date": "Validation Date"
        }
      ]
    }
  ]
}
```

### Field Descriptions

| Field Path | Type | Required | Description |
|------------|------|----------|-------------|
| project_name | string | Yes | Project name |
| current_iteration | string | Yes | Current iteration number |
| iterations | array | Yes | List of iterations |
| iterations[].iteration_id | string | Yes | Unique iteration identifier |
| iterations[].iteration_name | string | Yes | Iteration name |
| iterations[].status | string | Yes | Iteration status: `not_started`/`in_progress`/`completed`/`delayed` |
| iterations[].start_date | string | No | Start date, format: YYYY-MM-DD |
| iterations[].end_date | string | No | End date, format: YYYY-MM-DD |
| iterations[].tasks | array | Yes | List of tasks |
| iterations[].tasks[].task_id | string | Yes | Unique task identifier |
| iterations[].tasks[].task_name | string | Yes | Task name |
| iterations[].tasks[].status | string | Yes | Task status: `todo`/`in_progress`/`review`/`done`/`blocked` |
| iterations[].tasks[].assignee | string | No | Responsible person |
| iterations[].tasks[].priority | string | No | Priority: `low`/`medium`/`high`/`critical` |
| iterations[].tasks[].risk_level | string | No | Risk level: `low`/`high`, Agent evaluates automatically based on modification scope and impact |
| iterations[].tasks[].tags | array | No | List of tags |
| iterations[].modules | array | Yes | List of involved modules |
| iterations[].modules[].module_id | string | Yes | Unique module identifier |
| iterations[].modules[].module_name | string | Yes | Module name |
| iterations[].modules[].expected_completion | number | Yes | Expected module completion rate for this iteration (0-1) |
| iterations[].assumptions | array | Yes | List of assumptions |
| iterations[].assumptions[].assumption_id | string | Yes | Unique assumption identifier |
| iterations[].assumptions[].description | string | Yes | Assumption description |
| iterations[].assumptions[].status | string | Yes | Validation status: `pending`/`validated`/`invalidated` |
| iterations[].assumptions[].validation_date | string | No | Validation date, format: YYYY-MM-DD |

### Complete Example
```json
{
  "project_name": "E-commerce Platform Refactoring",
  "current_iteration": "ITER-2024-Q1-02",
  "iterations": [
    {
      "iteration_id": "ITER-2024-Q1-01",
      "iteration_name": "Phase 1: Order Module Refactoring",
      "status": "completed",
      "start_date": "2024-01-01",
      "end_date": "2024-01-31",
      "tasks": [
        {
          "task_id": "TASK-001",
          "task_name": "Order Creation Interface Refactoring",
          "status": "done",
          "assignee": "Zhang San",
          "priority": "high",
          "tags": ["backend", "api"]
        },
        {
          "task_id": "TASK-002",
          "task_name": "Order Payment Process Optimization",
          "status": "in_progress",
          "assignee": "Li Si",
          "priority": "critical",
          "tags": ["backend", "payment"]
        }
      ],
      "assumptions": [
        {
          "assumption_id": "ASSUMP-001",
          "description": "Order volume will not exceed 100,000 orders/day",
          "status": "validated",
          "validation_date": "2024-01-20"
        }
      ]
    },
    {
      "iteration_id": "ITER-2024-Q1-02",
      "iteration_name": "Phase 2: Product Module Refactoring",
      "status": "in_progress",
      "start_date": "2024-02-01",
      "end_date": "2024-02-29",
      "tasks": [
        {
          "task_id": "TASK-003",
          "task_name": "Product Search Function Implementation",
          "status": "todo",
          "assignee": "Wang Wu",
          "priority": "high",
          "tags": ["backend", "search"]
        }
      ],
      "assumptions": [
        {
          "assumption_id": "ASSUMP-002",
          "description": "Product quantity will not exceed 1 million",
          "status": "pending",
          "validation_date": null
        }
      ]
    }
  ]
}
```

## Application Status Format (app_status.json)

### Structure Definition
```json
{
  "app_name": "Application Name",
  "version": "Application Version",
  "last_updated": "Last Update Time",
  "modules": [
    {
      "module_name": "Module Name",
      "status": "Module Status",
      "owner": "Responsible Person",
      "completion_rate": 0.85,
      "last_update": "Last Update Time",
      "notes": "Notes"
    }
  ]
}
```

### Field Descriptions

| Field Path | Type | Required | Description |
|------------|------|----------|-------------|
| app_name | string | Yes | Application name |
| version | string | No | Application version |
| last_updated | string | Yes | Last update time, format: YYYY-MM-DD HH:MM:SS |
| modules | array | Yes | List of modules |
| modules[].module_name | string | Yes | Module name |
| modules[].status | string | Yes | Module status: `pending`/`developed`/`confirmed`/`optimized` |
| modules[].owner | string | No | Responsible person |
| modules[].completion_rate | number | No | Completion rate, range 0.0-1.0 |
| modules[].last_update | string | No | Last update time, format: YYYY-MM-DD HH:MM:SS |
| modules[].notes | string | No | Notes |

### Module Status Enum Values Description
- `pending`: Pending development
- `developed`: Developed, awaiting confirmation
- `confirmed`: Confirmed complete
- `optimized`: Confirmed, awaiting optimization

### Complete Example
```json
{
  "app_name": "E-commerce Backend Service",
  "version": "v2.0.0",
  "last_updated": "2024-02-15 10:30:00",
  "modules": [
    {
      "module_name": "User Authentication Module",
      "status": "confirmed",
      "owner": "Zhang San",
      "completion_rate": 1.0,
      "last_update": "2024-02-10 15:20:00",
      "notes": "JWT authentication integration completed"
    },
    {
      "module_name": "Order Processing Module",
      "status": "developed",
      "owner": "Li Si",
      "completion_rate": 0.85,
      "last_update": "2024-02-14 11:00:00",
      "notes": "Core functionality completed, awaiting testing"
    },
    {
      "module_name": "Payment Integration Module",
      "status": "pending",
      "owner": "Wang Wu",
      "completion_rate": 0.0,
      "last_update": "2024-02-01 09:00:00",
      "notes": "Awaiting payment interface documentation"
    },
    {
      "module_name": "Inventory Management Module",
      "status": "optimized",
      "owner": "Zhao Liu",
      "completion_rate": 1.0,
      "last_update": "2024-02-12 16:45:00",
      "notes": "Performance optimization completed, response time reduced by 50%"
    }
  ]
}
```

## Test Metrics Format (test_metrics.json)

### Structure Definition
```json
{
  "last_updated": "Last Update Time",
  "test_suites": [
    {
      "suite_name": "Test Suite Name",
      "total_tests": 100,
      "passed_tests": 95,
      "failed_tests": 3,
      "skipped_tests": 2,
      "coverage": 0.87,
      "last_run": "Last Run Time"
    }
  ],
  "tracing_points": [
    {
      "point_id": "Unique Tracing Point Identifier",
      "module": "Module Name",
      "location": "Tracing Point Location",
      "metric_type": "Metric Type",
      "status": "Tracing Point Status",
      "last_verified": "Last Verified Time"
    }
  ],
  "anomalies": [
    {
      "anomaly_id": "Unique Anomaly Identifier",
      "type": "Anomaly Type",
      "severity": "Severity Level",
      "description": "Anomaly Description",
      "first_occurred": "First Occurrence Time",
      "last_occurred": "Last Occurrence Time",
      "occurrence_count": 5,
      "status": "Processing Status"
    }
  ]
}
```

### Field Descriptions

| Field Path | Type | Required | Description |
|------------|------|----------|-------------|
| last_updated | string | Yes | Last update time, format: YYYY-MM-DD HH:MM:SS |
| test_suites | array | Yes | List of test suites |
| test_suites[].suite_name | string | Yes | Test suite name |
| test_suites[].total_tests | number | Yes | Total number of test cases |
| test_suites[].passed_tests | number | Yes | Number of passed tests |
| test_suites[].failed_tests | number | Yes | Number of failed tests |
| test_suites[].skipped_tests | number | Yes | Number of skipped tests |
| test_suites[].coverage | number | No | Code coverage, range 0.0-1.0 |
| test_suites[].last_run | string | Yes | Last run time, format: YYYY-MM-DD HH:MM:SS |
| tracing_points | array | Yes | List of tracing points |
| tracing_points[].point_id | string | Yes | Unique tracing point identifier |
| tracing_points[].module | string | Yes | Module name |
| tracing_points[].location | string | Yes | Tracing point location (file path:line number) |
| tracing_points[].metric_type | string | Yes | Metric type: `counter`/`gauge`/`histogram`/`summary` |
| tracing_points[].status | string | Yes | Tracing point status: `active`/`inactive`/`deprecated` |
| tracing_points[].last_verified | string | Yes | Last verified time, format: YYYY-MM-DD HH:MM:SS |
| anomalies | array | Yes | List of anomalies |
| anomalies[].anomaly_id | string | Yes | Unique anomaly identifier |
| anomalies[].type | string | Yes | Anomaly type: `performance`/`functional`/`integration`/`security` |
| anomalies[].severity | string | Yes | Severity level: `low`/`medium`/`high`/`critical` |
| anomalies[].description | string | Yes | Anomaly description |
| anomalies[].first_occurred | string | Yes | First occurrence time, format: YYYY-MM-DD HH:MM:SS |
| anomalies[].last_occurred | string | Yes | Last occurrence time, format: YYYY-MM-DD HH:MM:SS |
| anomalies[].occurrence_count | number | Yes | Occurrence count |
| anomalies[].status | string | Yes | Processing status: `open`/`investigating`/`resolved`/`ignored` |

### Complete Example
```json
{
  "last_updated": "2024-02-15 14:25:00",
  "test_suites": [
    {
      "suite_name": "Unit Test Suite",
      "total_tests": 120,
      "passed_tests": 115,
      "failed_tests": 3,
      "skipped_tests": 2,
      "coverage": 0.85,
      "last_run": "2024-02-15 10:00:00"
    },
    {
      "suite_name": "Integration Test Suite",
      "total_tests": 50,
      "passed_tests": 48,
      "failed_tests": 2,
      "skipped_tests": 0,
      "coverage": 0.72,
      "last_run": "2024-02-15 09:30:00"
    }
  ],
  "tracing_points": [
    {
      "point_id": "TRACE-001",
      "module": "Order Module",
      "location": "src/order_service.py:45",
      "metric_type": "counter",
      "status": "active",
      "last_verified": "2024-02-14 16:00:00"
    },
    {
      "point_id": "TRACE-002",
      "module": "Payment Module",
      "location": "src/payment_service.py:78",
      "metric_type": "histogram",
      "status": "active",
      "last_verified": "2024-02-15 09:00:00"
    },
    {
      "point_id": "TRACE-003",
      "module": "Inventory Module",
      "location": "src/inventory_service.py:32",
      "metric_type": "gauge",
      "status": "inactive",
      "last_verified": "2024-02-10 11:00:00"
    }
  ],
  "anomalies": [
    {
      "anomaly_id": "ANOM-001",
      "type": "performance",
      "severity": "high",
      "description": "Order creation interface response time exceeds 2 seconds",
      "first_occurred": "2024-02-10 14:30:00",
      "last_occurred": "2024-02-15 13:45:00",
      "occurrence_count": 23,
      "status": "investigating"
    },
    {
      "anomaly_id": "ANOM-002",
      "type": "functional",
      "severity": "medium",
      "description": "Payment callback occasionally lost",
      "first_occurred": "2024-02-12 09:15:00",
      "last_occurred": "2024-02-14 16:20:00",
      "occurrence_count": 8,
      "status": "open"
    }
  ]
}
```

## Data Validation Rules

### General Rules
1. All date formats must be `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`
2. All enum field values must be within allowed range
3. Numeric ranges must comply with field definitions (e.g., completion rate 0.0-1.0)
4. Numerical relationships must be logically consistent (e.g., passed tests <= total tests)

### JSON Format Validation
Use `scripts/collect_data.py` for data format validation:

```bash
python scripts/collect_data.py validate --project project_data.json --app app_status.json --test test_metrics.json
```

### Common Errors
1. **Enum Value Error**: Status field uses value outside allowed enum range
2. **Numeric Range Exceeded**: completion_rate greater than 1.0 or less than 0.0
3. **Date Format Error**: Date format doesn't match YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
4. **Logic Error**: passed_tests > total_tests
5. **Required Field Missing**: Missing required field

### Auto-generating Initial Data
If unsure how to create initial data, describe project situation to the agent, who will generate initial data files according to specification.