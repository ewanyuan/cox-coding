# JSON数据格式规范

## 目录
1. 概览
2. 应用状态数据格式（app_status.json）
3. 项目数据格式（project_data.json）
4. 测试指标数据格式（test_metrics.json）
5. 通用验证规则

## 概览

本规范定义了三种JSON数据格式：应用状态数据、项目数据和测试指标数据。这些数据用于跨维度的可观测性分析。

## 应用状态数据格式（app_status.json）

### 结构定义

```json
{
  "modules": [
    {
      "module_name": "order_service",
      "status": "active",
      "owner": "zhangsan",
      "completion_rate": 85,
      "description": "订单处理服务"
    },
    {
      "module_name": "payment_service",
      "status": "in_development",
      "owner": "lisi",
      "completion_rate": 60,
      "description": "支付处理服务"
    }
  ]
}
```

### 字段说明

- `module_name`: 模块名称（必需，字符串）
- `status`: 模块状态（必需，字符串）
  - `active`: 已激活
  - `in_development`: 开发中
  - `completed`: 已完成
  - `failed`: 失败
  - `blocked`: 阻塞
- `owner`: 负责人（必需，字符串）
- `completion_rate`: 完成率（必需，数值，0-100）
- `description`: 模块描述（可选，字符串）

### 示例

```json
{
  "modules": [
    {
      "module_name": "order_service",
      "status": "active",
      "owner": "zhangsan",
      "completion_rate": 85,
      "description": "订单处理服务"
    },
    {
      "module_name": "payment_service",
      "status": "in_development",
      "owner": "lisi",
      "completion_rate": 60,
      "description": "支付处理服务"
    },
    {
      "module_name": "user_service",
      "status": "completed",
      "owner": "wangwu",
      "completion_rate": 100,
      "description": "用户管理服务"
    },
    {
      "module_name": "inventory_service",
      "status": "blocked",
      "owner": "zhaoliu",
      "completion_rate": 30,
      "description": "库存管理服务"
    }
  ]
}
```

## 项目数据格式（project_data.json）

### 结构定义

```json
{
  "project_name": "电商平台重构",
  "iterations": [
    {
      "name": "迭代1：订单服务重构",
      "status": "completed",
      "tasks": [
        {
          "task_id": "TASK-001",
          "title": "订单查询接口优化",
          "status": "completed",
          "assignee": "zhangsan"
        },
        {
          "task_id": "TASK-002",
          "title": "订单创建接口重构",
          "status": "in_progress",
          "assignee": "lisi"
        }
      ]
    }
  ],
  "assumptions": [
    "假设订单量在重构期间保持稳定",
    "假设第三方支付接口保持兼容"
  ]
}
```

### 字段说明

#### 顶层字段

- `project_name`: 项目名称（必需，字符串）
- `iterations`: 迭代列表（必需，数组）
- `assumptions`: 开发假设列表（可选，数组）

#### 迭代字段

- `name`: 迭代名称（必需，字符串）
- `status`: 迭代状态（必需，字符串）
  - `planned`: 计划中
  - `in_progress`: 进行中
  - `completed`: 已完成
  - `cancelled`: 已取消
- `tasks`: 任务列表（必需，数组）

#### 任务字段

- `task_id`: 任务ID（必需，字符串）
- `title`: 任务标题（必需，字符串）
- `status`: 任务状态（必需，字符串）
  - `todo`: 待办
  - `in_progress`: 进行中
  - `done`: 已完成
  - `cancelled`: 已取消
- `assignee`: 任务负责人（可选，字符串）

### 示例

```json
{
  "project_name": "电商平台重构",
  "iterations": [
    {
      "name": "迭代1：订单服务重构",
      "status": "completed",
      "tasks": [
        {
          "task_id": "TASK-001",
          "title": "订单查询接口优化",
          "status": "done",
          "assignee": "zhangsan"
        },
        {
          "task_id": "TASK-002",
          "title": "订单创建接口重构",
          "status": "done",
          "assignee": "lisi"
        },
        {
          "task_id": "TASK-003",
          "title": "订单状态更新优化",
          "status": "done",
          "assignee": "wangwu"
        }
      ]
    },
    {
      "name": "迭代2：支付服务重构",
      "status": "in_progress",
      "tasks": [
        {
          "task_id": "TASK-004",
          "title": "支付接口对接",
          "status": "in_progress",
          "assignee": "lisi"
        },
        {
          "task_id": "TASK-005",
          "title": "支付回调处理",
          "status": "todo",
          "assignee": "zhaoliu"
        },
        {
          "task_id": "TASK-006",
          "title": "退款流程优化",
          "status": "todo",
          "assignee": "wangwu"
        }
      ]
    }
  ],
  "assumptions": [
    "假设订单量在重构期间保持稳定",
    "假设第三方支付接口保持兼容",
    "假设数据库迁移期间停机时间不超过2小时"
  ]
}
```

## 测试指标数据格式（test_metrics.json）

### 结构定义

```json
{
  "test_suites": [
    {
      "name": "订单服务测试套件",
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
      "description": "订单创建埋点"
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

### 字段说明

#### 测试套件字段

- `name`: 测试套件名称（必需，字符串）
- `total_tests`: 测试总数（必需，整数）
- `passed_tests`: 通过测试数（必需，整数）
- `failed_tests`: 失败测试数（必需，整数）
- `skipped_tests`: 跳过测试数（必需，整数）
- `execution_time`: 执行时间（必需，数值，单位：秒）

#### 埋点字段

- `name`: 埋点名称（必需，字符串）
- `status`: 埋点状态（必需，字符串）
  - `active`: 已激活
  - `inactive`: 未激活
- `module`: 所属模块（可选，字符串）
- `description`: 描述（可选，字符串）

#### 异常字段

- `type`: 异常类型（必需，字符串）
- `message`: 异常消息（必需，字符串）
- `stack_trace`: 堆栈跟踪（可选，字符串）
- `test_case`: 关联的测试用例（可选，字符串）

#### 覆盖率字段

- `line_coverage`: 行覆盖率（必需，数值，0-100）
- `branch_coverage`: 分支覆盖率（必需，数值，0-100）
- `function_coverage`: 函数覆盖率（必需，数值，0-100）
- `statement_coverage`: 语句覆盖率（必需，数值，0-100）

### 示例

```json
{
  "test_suites": [
    {
      "name": "订单服务测试套件",
      "total_tests": 50,
      "passed_tests": 48,
      "failed_tests": 1,
      "skipped_tests": 1,
      "execution_time": 125.5
    },
    {
      "name": "支付服务测试套件",
      "total_tests": 35,
      "passed_tests": 33,
      "failed_tests": 2,
      "skipped_tests": 0,
      "execution_time": 98.3
    },
    {
      "name": "用户服务测试套件",
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
      "description": "订单创建埋点"
    },
    {
      "name": "payment_success",
      "status": "active",
      "module": "payment_service",
      "description": "支付成功埋点"
    },
    {
      "name": "user_login",
      "status": "active",
      "module": "user_service",
      "description": "用户登录埋点"
    },
    {
      "name": "inventory_update",
      "status": "inactive",
      "module": "inventory_service",
      "description": "库存更新埋点"
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

## 通用验证规则

1. **JSON格式必须有效**：可以正确解析为JSON对象或数组
2. **必需字段必须存在**：不能缺少必需字段
3. **字段类型必须正确**：
   - 字符串字段必须是字符串类型
   - 数值字段必须是数字类型
   - 布尔字段必须是布尔类型
   - 数组字段必须是数组类型
4. **枚举值必须有效**：状态、级别等字段必须在预定义的枚举值范围内
5. **数值范围必须合理**：
   - 完成率：0-100
   - 覆盖率：0-100
   - 执行时间：>= 0

## 注意事项

- 字符串字段建议使用UTF-8编码
- 数值字段避免使用科学计数法，除非特别大或特别小
- 日期时间字段建议使用ISO 8601格式
- 数组字段建议保持元素类型一致
- 嵌套对象层级不宜过深（建议不超过3层）
- 对于可选字段，如果不需要可以省略，减少数据体积
