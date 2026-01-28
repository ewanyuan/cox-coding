# 异常分析报告模板

## 异常概览

**分析时间范围**: {{START_TIME}} - {{END_TIME}}
**异常总数**: {{TOTAL_EXCEPTIONS}}
**错误率**: {{ERROR_RATE}} %
**最严重的异常**: {{MOST_CRITICAL_EXCEPTION}}

## 异常分类统计

### 按类型分组

| 异常类型 | 发生次数 | 占比(%) | 平均间隔时间(秒) | 最后发生时间 |
|----------|----------|---------|------------------|--------------|
{{EXCEPTION_BY_TYPE_TABLE}}

### 按级别分组

| 级别 | 发生次数 | 占比(%) | 影响评估 |
|------|----------|---------|----------|
| CRITICAL | {{CRITICAL_COUNT}} | {{CRITICAL_PERCENT}} | {{CRITICAL_IMPACT}} |
| ERROR | {{ERROR_COUNT}} | {{ERROR_PERCENT}} | {{ERROR_IMPACT}} |
| WARNING | {{WARNING_COUNT}} | {{WARNING_PERCENT}} | {{WARNING_IMPACT}} |

## 异常详情

### 严重异常列表

| 异常ID | 类型 | 消息 | 发生时间 | 位置 | 影响范围 |
|--------|------|------|----------|------|----------|
{{CRITICAL_EXCEPTIONS_TABLE}}

### 异常堆栈跟踪

#### 异常 1: {{EXCEPTION_TYPE_1}}
**发生时间**: {{OCCURRENCE_TIME_1}}
**触发位置**: {{LOCATION_1}}

**堆栈跟踪**:
```
{{STACK_TRACE_1}}
```

**上下文信息**:
- {{CONTEXT_INFO_1_1}}
- {{CONTEXT_INFO_1_2}}

#### 异常 2: {{EXCEPTION_TYPE_2}}
**发生时间**: {{OCCURRENCE_TIME_2}}
**触发位置**: {{LOCATION_2}}

**堆栈跟踪**:
```
{{STACK_TRACE_2}}
```

**上下文信息**:
- {{CONTEXT_INFO_2_1}}
- {{CONTEXT_INFO_2_2}}

## 异常传播分析

### 传播链

```
{{PROPAGATION_CHAIN_VISUALIZATION}}
```

### 传播统计

| 起始点 | 传播路径 | 影响模块数 | 最终影响 |
|--------|----------|-----------|----------|
{{PROPAGATION_STATS_TABLE}}

## 异常关联分析

### 与性能的关联

- 性能下降相关异常: {{PERFORMANCE_RELATED_COUNT}} 个
- 高耗时操作相关异常: {{HIGH_DURATION_RELATED_COUNT}} 个

| 异常类型 | 相关性能指标 | 关联强度 |
|----------|--------------|----------|
{{PERFORMANCE_CORRELATION_TABLE}}

### 与业务逻辑的关联

- 业务流程中断: {{BUSINESS_INTERRUPT_COUNT}} 次
- 数据一致性影响: {{DATA_CONSISTENCY_IMPACT_COUNT}} 次

| 业务功能 | 相关异常 | 影响程度 |
|----------|----------|----------|
{{BUSINESS_CORRELATION_TABLE}}

## 根因分析

### 根因定位

| 异常ID | 直接原因 | 根本原因 | 责任模块 |
|--------|----------|----------|----------|
{{ROOT_CAUSE_TABLE}}

### 根因分类

| 根因类型 | 异常数 | 占比(%) |
|----------|---------|---------|
| 代码缺陷 | {{CODE_DEFECT_COUNT}} | {{CODE_DEFECT_PERCENT}} |
| 配置错误 | {{CONFIG_ERROR_COUNT}} | {{CONFIG_ERROR_PERCENT}} |
| 资源不足 | {{RESOURCE_INSUFFICIENT_COUNT}} | {{RESOURCE_INSUFFICIENT_PERCENT}} |
| 依赖服务问题 | {{DEPENDENCY_ISSUE_COUNT}} | {{DEPENDENCY_ISSUE_PERCENT}} |
| 并发问题 | {{CONCURRENCY_ISSUE_COUNT}} | {{CONCURRENCY_ISSUE_PERCENT}} |

## 解决方案

### 立即修复（高优先级）

1. 异常: {{IMMEDIATE_FIX_EXCEPTION_1}}
   - 问题描述: {{IMMEDIATE_FIX_PROBLEM_1}}
   - 修复方案: {{IMMEDIATE_FIX_SOLUTION_1}}
   - 预计修复时间: {{IMMEDIATE_FIX_ESTIMATED_TIME_1}}
   - 代码位置: {{IMMEDIATE_FIX_CODE_LOCATION_1}}

2. 异常: {{IMMEDIATE_FIX_EXCEPTION_2}}
   - 问题描述: {{IMMEDIATE_FIX_PROBLEM_2}}
   - 修复方案: {{IMMEDIATE_FIX_SOLUTION_2}}
   - 预计修复时间: {{IMMEDIATE_FIX_ESTIMATED_TIME_2}}
   - 代码位置: {{IMMEDIATE_FIX_CODE_LOCATION_2}}

### 计划修复（中优先级）

1. 异常: {{PLANNED_FIX_EXCEPTION_1}}
   - 问题描述: {{PLANNED_FIX_PROBLEM_1}}
   - 修复方案: {{PLANNED_FIX_SOLUTION_1}}
   - 预计修复时间: {{PLANNED_FIX_ESTIMATED_TIME_1}}

### 长期改进（低优先级）

1. 异常: {{LONG_TERM_FIX_EXCEPTION_1}}
   - 问题描述: {{LONG_TERM_FIX_PROBLEM_1}}
   - 改进方案: {{LONG_TERM_FIX_SOLUTION_1}}
   - 预计完成时间: {{LONG_TERM_FIX_ESTIMATED_TIME_1}}

## 预防措施

### 代码层面

1. {{CODE_PREVENTION_1}}
2. {{CODE_PREVENTION_2}}

### 测试层面

1. {{TEST_PREVENTION_1}}
2. {{TEST_PREVENTION_2}}

### 监控层面

1. {{MONITORING_PREVENTION_1}}
2. {{MONITORING_PREVENTION_2}}

## 验证计划

### 测试用例

| 测试用例ID | 测试场景 | 预期结果 | 验证方法 |
|-----------|----------|----------|----------|
{{TEST_CASE_TABLE}}

### 回归测试

- 需要回归测试的模块: {{REGRESSION_MODULES}}
- 回归测试范围: {{REGRESSION_SCOPE}}
- 预计回归测试时间: {{REGRESSION_ESTIMATED_TIME}}

## 异常趋势

| 时间段 | 异常数 | 趋势 | 原因分析 |
|--------|--------|------|----------|
{{EXCEPTION_TREND_TABLE}}
