# 可观测数据格式规范

## 目录
- [项目数据格式 (project_data.json)](#项目数据格式-project_datajson)
- [应用状态格式 (app_status.json)](#应用状态格式-app_statusjson)
- [测试指标格式 (test_metrics.json)](#测试指标格式-test_metricsjson)
- [数据验证规则](#数据验证规则)

## 项目数据格式 (project_data.json)

### 结构定义
```json
{
  "project_name": "项目名称",
  "current_iteration": "迭代编号",
  "iterations": [
    {
      "iteration_id": "迭代唯一标识",
      "iteration_name": "迭代名称",
      "status": "迭代状态",
      "start_date": "开始日期",
      "end_date": "结束日期",
      "tasks": [
        {
          "task_id": "任务唯一标识",
          "task_name": "任务名称",
          "status": "任务状态",
          "assignee": "负责人",
          "priority": "优先级",
          "risk_level": "风险等级",
          "tags": ["标签1", "标签2"]
        }
      ],
      "modules": [
        {
          "module_id": "模块唯一标识",
          "module_name": "模块名称",
          "expected_completion": 0.8
        }
      ],
      "assumptions": [
        {
          "assumption_id": "假设唯一标识",
          "description": "假设描述",
          "status": "验证状态",
          "validation_date": "验证日期"
        }
      ]
    }
  ]
}
```

### 字段说明

| 字段路径 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| project_name | string | 是 | 项目名称 |
| current_iteration | string | 是 | 当前迭代编号 |
| iterations | array | 是 | 迭代列表 |
| iterations[].iteration_id | string | 是 | 迭代唯一标识 |
| iterations[].iteration_name | string | 是 | 迭代名称 |
| iterations[].status | string | 是 | 迭代状态：`not_started`/`in_progress`/`completed`/`delayed` |
| iterations[].start_date | string | 否 | 开始日期，格式：YYYY-MM-DD |
| iterations[].end_date | string | 否 | 结束日期，格式：YYYY-MM-DD |
| iterations[].tasks | array | 是 | 任务列表 |
| iterations[].tasks[].task_id | string | 是 | 任务唯一标识 |
| iterations[].tasks[].task_name | string | 是 | 任务名称 |
| iterations[].tasks[].status | string | 是 | 任务状态：`todo`/`in_progress`/`review`/`done`/`blocked` |
| iterations[].tasks[].assignee | string | 否 | 负责人 |
| iterations[].tasks[].priority | string | 否 | 优先级：`low`/`medium`/`high`/`critical` |
| iterations[].tasks[].risk_level | string | 否 | 风险等级：`low`/`high`，Agent 根据修改范围和影响自动评估 |
| iterations[].tasks[].tags | array | 否 | 标签列表 |
| iterations[].modules | array | 是 | 涉及的模块列表 |
| iterations[].modules[].module_id | string | 是 | 模块唯一标识 |
| iterations[].modules[].module_name | string | 是 | 模块名称 |
| iterations[].modules[].expected_completion | number | 是 | 该迭代预期达到的模块完成率（0-1） |
| iterations[].assumptions | array | 是 | 假设列表 |
| iterations[].assumptions[].assumption_id | string | 是 | 假设唯一标识 |
| iterations[].assumptions[].description | string | 是 | 假设描述 |
| iterations[].assumptions[].status | string | 是 | 验证状态：`pending`/`validated`/`invalidated` |
| iterations[].assumptions[].validation_date | string | 否 | 验证日期，格式：YYYY-MM-DD |

### 完整示例
```json
{
  "project_name": "电商平台重构",
  "current_iteration": "ITER-2024-Q1-02",
  "iterations": [
    {
      "iteration_id": "ITER-2024-Q1-01",
      "iteration_name": "第一阶段：订单模块重构",
      "status": "completed",
      "start_date": "2024-01-01",
      "end_date": "2024-01-31",
      "tasks": [
        {
          "task_id": "TASK-001",
          "task_name": "订单创建接口重构",
          "status": "done",
          "assignee": "张三",
          "priority": "high",
          "tags": ["backend", "api"]
        },
        {
          "task_id": "TASK-002",
          "task_name": "订单支付流程优化",
          "status": "in_progress",
          "assignee": "李四",
          "priority": "critical",
          "tags": ["backend", "payment"]
        }
      ],
      "assumptions": [
        {
          "assumption_id": "ASSUMP-001",
          "description": "订单量不会超过10万单/天",
          "status": "validated",
          "validation_date": "2024-01-20"
        }
      ]
    },
    {
      "iteration_id": "ITER-2024-Q1-02",
      "iteration_name": "第二阶段：商品模块重构",
      "status": "in_progress",
      "start_date": "2024-02-01",
      "end_date": "2024-02-29",
      "tasks": [
        {
          "task_id": "TASK-003",
          "task_name": "商品搜索功能实现",
          "status": "todo",
          "assignee": "王五",
          "priority": "high",
          "tags": ["backend", "search"]
        }
      ],
      "assumptions": [
        {
          "assumption_id": "ASSUMP-002",
          "description": "商品数量不超过100万",
          "status": "pending",
          "validation_date": null
        }
      ]
    }
  ]
}
```

## 应用状态格式 (app_status.json)

### 结构定义
```json
{
  "app_name": "应用名称",
  "version": "应用版本",
  "last_updated": "最后更新时间",
  "modules": [
    {
      "module_name": "模块名称",
      "status": "模块状态",
      "owner": "负责人",
      "completion_rate": 0.85,
      "last_update": "最后更新时间",
      "notes": "备注信息"
    }
  ]
}
```

### 字段说明

| 字段路径 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| app_name | string | 是 | 应用名称 |
| version | string | 否 | 应用版本 |
| last_updated | string | 是 | 最后更新时间，格式：YYYY-MM-DD HH:MM:SS |
| modules | array | 是 | 模块列表 |
| modules[].module_name | string | 是 | 模块名称 |
| modules[].status | string | 是 | 模块状态：`pending`/`developed`/`confirmed`/`optimized` |
| modules[].owner | string | 否 | 负责人 |
| modules[].completion_rate | number | 否 | 完成率，范围0.0-1.0 |
| modules[].last_update | string | 否 | 最后更新时间，格式：YYYY-MM-DD HH:MM:SS |
| modules[].notes | string | 否 | 备注信息 |

### 模块状态枚举值说明
- `pending`：待开发
- `developed`：已开发待确认
- `confirmed`：已确认完成
- `optimized`：已确认待优化

### 完整示例
```json
{
  "app_name": "电商平台后端服务",
  "version": "v2.0.0",
  "last_updated": "2024-02-15 10:30:00",
  "modules": [
    {
      "module_name": "用户认证模块",
      "status": "confirmed",
      "owner": "张三",
      "completion_rate": 1.0,
      "last_update": "2024-02-10 15:20:00",
      "notes": "已完成JWT认证集成"
    },
    {
      "module_name": "订单处理模块",
      "status": "developed",
      "owner": "李四",
      "completion_rate": 0.85,
      "last_update": "2024-02-14 11:00:00",
      "notes": "核心功能已完成，等待测试"
    },
    {
      "module_name": "支付集成模块",
      "status": "pending",
      "owner": "王五",
      "completion_rate": 0.0,
      "last_update": "2024-02-01 09:00:00",
      "notes": "等待支付接口文档"
    },
    {
      "module_name": "库存管理模块",
      "status": "optimized",
      "owner": "赵六",
      "completion_rate": 1.0,
      "last_update": "2024-02-12 16:45:00",
      "notes": "已完成性能优化，响应时间降低50%"
    }
  ]
}
```

## 测试指标格式 (test_metrics.json)

### 结构定义
```json
{
  "last_updated": "最后更新时间",
  "test_suites": [
    {
      "suite_name": "测试套件名称",
      "total_tests": 100,
      "passed_tests": 95,
      "failed_tests": 3,
      "skipped_tests": 2,
      "coverage": 0.87,
      "last_run": "最后运行时间"
    }
  ],
  "tracing_points": [
    {
      "point_id": "埋点唯一标识",
      "module": "所属模块",
      "location": "埋点位置",
      "metric_type": "指标类型",
      "status": "埋点状态",
      "last_verified": "最后验证时间"
    }
  ],
  "anomalies": [
    {
      "anomaly_id": "异常唯一标识",
      "type": "异常类型",
      "severity": "严重程度",
      "description": "异常描述",
      "first_occurred": "首次发生时间",
      "last_occurred": "最后发生时间",
      "occurrence_count": 5,
      "status": "处理状态"
    }
  ]
}
```

### 字段说明

| 字段路径 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| last_updated | string | 是 | 最后更新时间，格式：YYYY-MM-DD HH:MM:SS |
| test_suites | array | 是 | 测试套件列表 |
| test_suites[].suite_name | string | 是 | 测试套件名称 |
| test_suites[].total_tests | number | 是 | 测试用例总数 |
| test_suites[].passed_tests | number | 是 | 通过测试数 |
| test_suites[].failed_tests | number | 是 | 失败测试数 |
| test_suites[].skipped_tests | number | 是 | 跳过测试数 |
| test_suites[].coverage | number | 否 | 代码覆盖率，范围0.0-1.0 |
| test_suites[].last_run | string | 是 | 最后运行时间，格式：YYYY-MM-DD HH:MM:SS |
| tracing_points | array | 是 | 埋点列表 |
| tracing_points[].point_id | string | 是 | 埋点唯一标识 |
| tracing_points[].module | string | 是 | 所属模块 |
| tracing_points[].location | string | 是 | 埋点位置（文件路径:行号） |
| tracing_points[].metric_type | string | 是 | 指标类型：`counter`/`gauge`/`histogram`/`summary` |
| tracing_points[].status | string | 是 | 埋点状态：`active`/`inactive`/`deprecated` |
| tracing_points[].last_verified | string | 是 | 最后验证时间，格式：YYYY-MM-DD HH:MM:SS |
| anomalies | array | 是 | 异常列表 |
| anomalies[].anomaly_id | string | 是 | 异常唯一标识 |
| anomalies[].type | string | 是 | 异常类型：`performance`/`functional`/`integration`/`security` |
| anomalies[].severity | string | 是 | 严重程度：`low`/`medium`/`high`/`critical` |
| anomalies[].description | string | 是 | 异常描述 |
| anomalies[].first_occurred | string | 是 | 首次发生时间，格式：YYYY-MM-DD HH:MM:SS |
| anomalies[].last_occurred | string | 是 | 最后发生时间，格式：YYYY-MM-DD HH:MM:SS |
| anomalies[].occurrence_count | number | 是 | 发生次数 |
| anomalies[].status | string | 是 | 处理状态：`open`/`investigating`/`resolved`/`ignored` |

### 完整示例
```json
{
  "last_updated": "2024-02-15 14:25:00",
  "test_suites": [
    {
      "suite_name": "单元测试套件",
      "total_tests": 120,
      "passed_tests": 115,
      "failed_tests": 3,
      "skipped_tests": 2,
      "coverage": 0.85,
      "last_run": "2024-02-15 10:00:00"
    },
    {
      "suite_name": "集成测试套件",
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
      "module": "订单模块",
      "location": "src/order_service.py:45",
      "metric_type": "counter",
      "status": "active",
      "last_verified": "2024-02-14 16:00:00"
    },
    {
      "point_id": "TRACE-002",
      "module": "支付模块",
      "location": "src/payment_service.py:78",
      "metric_type": "histogram",
      "status": "active",
      "last_verified": "2024-02-15 09:00:00"
    },
    {
      "point_id": "TRACE-003",
      "module": "库存模块",
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
      "description": "订单创建接口响应时间超过2秒",
      "first_occurred": "2024-02-10 14:30:00",
      "last_occurred": "2024-02-15 13:45:00",
      "occurrence_count": 23,
      "status": "investigating"
    },
    {
      "anomaly_id": "ANOM-002",
      "type": "functional",
      "severity": "medium",
      "description": "支付回调偶尔丢失",
      "first_occurred": "2024-02-12 09:15:00",
      "last_occurred": "2024-02-14 16:20:00",
      "occurrence_count": 8,
      "status": "open"
    }
  ]
}
```

## 数据验证规则

### 通用规则
1. 所有日期格式必须为 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`
2. 所有枚举字段的值必须在允许的枚举范围内
3. 数值范围必须符合字段定义（如完成率0.0-1.0）
4. 数值关系必须符合逻辑（如通过测试数 <= 总测试数）

### JSON格式验证
使用 `scripts/collect_data.py` 进行数据格式验证：

```bash
python scripts/collect_data.py validate --project project_data.json --app app_status.json --test test_metrics.json
```

### 常见错误
1. **枚举值错误**：status字段使用了不在枚举范围内的值
2. **数值超范围**：completion_rate大于1.0或小于0.0
3. **日期格式错误**：日期格式不符合YYYY-MM-DD或YYYY-MM-DD HH:MM:SS
4. **逻辑错误**：passed_tests > total_tests
5. **必填字段缺失**：缺少required字段

### 自动生成初始数据
如果不确定如何创建初始数据，可以向智能体描述项目情况，智能体会根据规范生成初始数据文件。
