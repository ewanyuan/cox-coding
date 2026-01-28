# JSON Data Format Specifications

## Table of Contents
1. Overview
2. Application Status Data Format (app_status.json)
3. Project Data Format (project_data.json)
4. Test Metrics Data Format (test_metrics.json)
5. General Validation Rules

## Overview

This specification defines three JSON data formats: application status data, project data, and test metrics data. These data are used for cross-dimensional observability analysis.

## Application Status Data Format (app_status.json)

### Structure Definition

```json
{
  "modules": [
    {
      "module_name": "order_service",
      "status": "active",
      "owner": "zhangsan",
      "completion_rate": 85,
      "description": "Order processing service"
    },
    {
      "module_name": "payment_service",
      "status": "in_development",
      "owner": "lisi",
      "completion_rate": 60,
      "description": "Payment processing service"
    }
  ]
}
```

### Field Descriptions

- `module_name`: Module name (required, string)
- `status`: Module status (required, string)
  - `active`: Active
  - `in_development`: In development
  - `completed`: Completed
  - `failed`: Failed
  - `blocked`: Blocked
- `owner`: Owner (required, string)
- `completion_rate`: Completion rate (required, numeric, 0-100)
- `description`: Module description (optional, string)

### Example

```json
{
  "modules": [
    {
      "module_name": "order_service",
      "status": "active",
      "owner": "zhangsan",
      "completion_rate": 85,
      "description": "Order processing service"
    },
    {
      "module_name": "payment_service",
      "status": "in_development",
      "owner": "lisi",
      "completion_rate": 60,
      "description": "Payment processing service"
    },
    {
      "module_name": "user_service",
      "status": "completed",
      "owner": "wangwu",
      "completion_rate": 100,
      "description": "User management service"
    },
    {
      "module_name": "inventory_service",
      "status": "blocked",
      "owner": "zhaoliu",
      "completion_rate": 30,
      "description": "Inventory management service"
    }
  ]
}
```

## Project Data Format (project_data.json)

### Structure Definition

```json
{
  "project_name": "E-commerce Platform Refactoring",
  "iterations": [
    {
      "name": "Iteration 1: Order Service Refactoring",
      "status": "completed",
      "tasks": [
        {
          "task_id": "TASK-001",
          "title": "Optimize Order Query API",
          "status": "completed",
          "assignee": "zhangsan"
        },
        {
          "task_id": "TASK-002",
          "title": "Refactor Order Creation API",
          "status": "in_progress",
          "assignee": "lisi"
        }
      ]
    }
  ],
  "assumptions": [
    "Assume order volume remains stable during refactoring",
    "Assume third-party payment interface remains compatible"
  ]
}
```

### Field Descriptions

#### Top-Level Fields

- `project_name`: Project name (required, string)
- `iterations`: Iteration list (required, array)
- `assumptions`: Development assumption list (optional, array)

#### Iteration Fields

- `name`: Iteration name (required, string)
- `status`: Iteration status (required, string)
  - `planned`: Planned
  - `in_progress`: In progress
  - `completed`: Completed
  - `cancelled`: Cancelled
- `tasks`: Task list (required, array)

#### Task Fields

- `task_id`: Task ID (required, string)
- `title`: Task title (required, string)
- `status`: Task status (required, string)
  - `todo`: Todo
  - `in_progress`: In progress
  - `done`: Done
  - `cancelled`: Cancelled
- `assignee`: Task assignee (optional, string)

### Example

```json
{
  "project_name": "E-commerce Platform Refactoring",
  "iterations": [
    {
      "name": "Iteration 1: Order Service Refactoring",
      "status": "completed",
      "tasks": [
        {
          "task_id": "TASK-001",
          "title": "Optimize Order Query API",
          "status": "done",
          "assignee": "zhangsan"
        },
        {
          "task_id": "TASK-002",
          "title": "Refactor Order Creation API",
          "status": "done",
          "assignee": "lisi"
        },
        {
          "task_id": "TASK-003",
          "title": "Optimize Order Status Update",
          "status": "done",
          "assignee": "wangwu"
        }
      ]
    },
    {
      "name": "Iteration 2: Payment Service Refactoring",
      "status": "in_progress",
      "tasks": [
        {
          "task_id": "TASK-004",
          "title": "Integrate Payment Interface",
          "status": "in_progress",
          "assignee": "lisi"
        },
        {
          "task_id": "TASK-005",
          "title": "Handle Payment Callback",
          "status": "todo",
          "assignee": "zhaoliu"
        },
        {
          "task_id": "TASK-006",
          "title": "Optimize Refund Process",
          "status": "todo",
          "assignee": "wangwu"
        }
      ]
    }
  ],
  "assumptions": [
    "Assume order volume remains stable during refactoring",
    "Assume third-party payment interface remains compatible",
    "Assume database migration downtime不超过2 hours"
  ]
}
```

## Test Metrics Data Format (test_metrics.json)

### Structure Definition

```json
{
  "test_suites": [
    {
      "name": "Order Service Test Suite",
      "total_tests": 50,
      "passed_tests": 48,
      "failed_tests": 1,
      "skipped_tests": 1,
      "execution_time": 125.5
    }
  ],
  "tracking_points": [
    {
      "name": "order_created",
      "status": "active",
      "module": "order_service",
      "description": "Order creation instrumentation point"
    }
  ],
  "exceptions": [
    {
      "type": "AssertionError",
      "message": "Expected 200 but got 500",
      "stack_trace": "Traceback...",
      "test_case": "test_order_create"
    }
  ],
  "coverage": {
    "line_coverage": 85.5,
    "branch_coverage": 78.2,
    "function_coverage": 90.0,
    "statement_coverage": 88.5
  }
}
```

### Field Descriptions

#### Test Suite Fields

- `name`: Test suite name (required, string)
- `total_tests`: Total test count (required, integer)
- `passed_tests`: Passed test count (required, integer)
- `failed_tests`: Failed test count (required, integer)
- `skipped_tests`: Skipped test count (required, integer)
- `execution_time`: Execution time (required, numeric, unit: seconds)

#### Instrumentation Point Fields

- `name`: Instrumentation point name (required, string)
- `status`: Instrumentation point status (required, string)
  - `active`: Active
  - `inactive`: Inactive
- `module`: Belonging module (optional, string)
- `description`: Description (optional, string)

#### Exception Fields

- `type`: Exception type (required, string)
- `message`: Exception message (required, string)
- `stack_trace`: Stack trace (optional, string)
- `test_case`: Associated test case (optional, string)

#### Coverage Fields

- `line_coverage`: Line coverage (required, numeric, 0-100)
- `branch_coverage`: Branch coverage (required, numeric, 0-100)
- `function_coverage`: Function coverage (required, numeric, 0-100)
- `statement_coverage`: Statement coverage (required, numeric, 0-100)

### Example

```json
{
  "test_suites": [
    {
      "name": "Order Service Test Suite",
      "total_tests": 50,
      "passed_tests": 48,
      "failed_tests": 1,
      "skipped_tests": 1,
      "execution_time": 125.5
    },
    {
      "name": "Payment Service Test Suite",
      "total_tests": 35,
      "passed_tests": 33,
      "failed_tests": 2,
      "skipped_tests": 0,
      "execution_time": 98.3
    },
    {
      "name": "User Service Test Suite",
      "total_tests": 40,
      "passed_tests": 40,
      "failed_tests": 0,
      "skipped_tests": 0,
      "execution_time": 75.2
    }
  ],
  "tracking_points": [
    {
      "name": "order_created",
      "status": "active",
      "module": "order_service",
      "description": "Order creation instrumentation point"
    },
    {
      "name": "payment_success",
      "status": "active",
      "module": "payment_service",
      "description": "Payment success instrumentation point"
    },
    {
      "name": "user_login",
      "status": "active",
      "module": "user_service",
      "description": "User login instrumentation point"
    },
    {
      "name": "inventory_update",
      "status": "inactive",
      "module": "inventory_service",
      "description": "Inventory update instrumentation point"
    }
  ],
  "exceptions": [
    {
      "type": "AssertionError",
      "message": "Expected 200 but got 500",
      "stack_trace": "Traceback (most recent call last):\n  File 'test_order.py', line 45, in test_order_create\n    assert response.status_code == 200\nAssertionError: Expected 200 but got 500",
      "test_case": "test_order_create"
    },
    {
      "type": "TimeoutError",
      "message": "Payment gateway timeout after 30s",
      "stack_trace": "Traceback (most recent call last):\n  File 'test_payment.py', line 23, in test_payment_process\n    result = gateway.process_payment(amount)\nTimeoutError: Payment gateway timeout after 30s",
      "test_case": "test_payment_process"
    }
  ],
  "coverage": {
    "line_coverage": 85.5,
    "branch_coverage": 78.2,
    "function_coverage": 90.0,
    "statement_coverage": 88.5
  }
}
```

## General Validation Rules

1. **JSON format must be valid**: Can be correctly parsed as JSON object or array
2. **Required fields must exist**: Cannot lack required fields
3. **Field types must be correct**:
   - String fields must be string type
   - Numeric fields must be numeric type
   - Boolean fields must be boolean type
   - Array fields must be array type
4. **Enum values must be valid**: Status, level and other fields must be within predefined enum value ranges
5. **Numeric ranges must be reasonable**:
   - Completion rate: 0-100
   - Coverage: 0-100
   - Execution time: >= 0

## Precautions

- String fields recommended to use UTF-8 encoding
- Numeric fields avoid scientific notation unless extremely large or small
- Date time fields recommended to use ISO 8601 format
- Array fields recommended to keep element types consistent
- Nested object depth shouldn't be too deep (recommended not exceeding 3 layers)
- For optional fields, if not needed can omit, reducing data volume
