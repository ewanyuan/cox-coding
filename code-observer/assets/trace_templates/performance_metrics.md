# 性能指标报告模板

## 性能概览

**分析时间范围**: {{START_TIME}} - {{END_TIME}}
**总请求数**: {{TOTAL_REQUESTS}}
**平均响应时间**: {{AVG_RESPONSE_TIME}} ms
**P95响应时间**: {{P95_RESPONSE_TIME}} ms
**P99响应时间**: {{P99_RESPONSE_TIME}} ms

## 资源使用统计

### CPU使用率

| 时间段 | 平均使用率(%) | 最大使用率(%) | 最小使用率(%) |
|--------|--------------|--------------|--------------|
{{CPU_USAGE_TABLE}}

### 内存使用

| 时间段 | 平均使用(MB) | 最大使用(MB) | 峰值时刻 |
|--------|--------------|--------------|----------|
{{MEMORY_USAGE_TABLE}}

### I/O统计

| 类型 | 总操作数 | 总耗时(ms) | 平均耗时(ms) |
|------|----------|-------------|-------------|
| 读操作 | {{READ_COUNT}} | {{READ_DURATION}} | {{READ_AVG}} |
| 写操作 | {{WRITE_COUNT}} | {{WRITE_DURATION}} | {{WRITE_AVG}} |

## 性能瓶颈分析

### 高耗时操作

| 排名 | 函数/操作 | 耗时(ms) | 调用次数 | 占总耗时比例(%) |
|------|-----------|----------|----------|-----------------|
{{HIGH_DURATION_OPS_TABLE}}

### 频繁调用操作

| 排名 | 函数/操作 | 调用次数 | 总耗时(ms) | 平均耗时(ms) |
|------|-----------|----------|-----------|-------------|
{{HIGH_FREQUENCY_OPS_TABLE}}

### 热点路径

| 路径 | 总耗时(ms) | 调用次数 | 瓶颈函数 |
|------|-----------|----------|----------|
{{HOT_PATH_TABLE}}

## 性能趋势分析

### 响应时间趋势

```
{{RESPONSE_TIME_TREND_CHART}}
```

### 资源使用趋势

```
{{RESOURCE_USAGE_TREND_CHART}}
```

## 性能优化建议

### 立即优化（高优先级）

1. {{IMMEDIATE_OPTIMIZATION_1}}
   - 问题描述: {{PROBLEM_DESCRIPTION_1}}
   - 优化方案: {{OPTIMIZATION_PLAN_1}}
   - 预期提升: {{EXPECTED_IMPROVEMENT_1}}

2. {{IMMEDIATE_OPTIMIZATION_2}}
   - 问题描述: {{PROBLEM_DESCRIPTION_2}}
   - 优化方案: {{OPTIMIZATION_PLAN_2}}
   - 预期提升: {{EXPECTED_IMPROVEMENT_2}}

### 计划优化（中优先级）

1. {{PLANNED_OPTIMIZATION_1}}
   - 问题描述: {{PROBLEM_DESCRIPTION_1}}
   - 优化方案: {{OPTIMIZATION_PLAN_1}}
   - 预期提升: {{EXPECTED_IMPROVEMENT_1}}

### 持续优化（低优先级）

1. {{ONGOING_OPTIMIZATION_1}}
   - 问题描述: {{PROBLEM_DESCRIPTION_1}}
   - 优化方案: {{OPTIMIZATION_PLAN_1}}
   - 预期提升: {{EXPECTED_IMPROVEMENT_1}}

## 性能基准对比

| 指标 | 当前值 | 基准值 | 差异 | 状态 |
|------|--------|--------|------|------|
| 平均响应时间 | {{CURRENT_AVG}} | {{BASELINE_AVG}} | {{DIFF_AVG}} | {{STATUS_AVG}} |
| P95响应时间 | {{CURRENT_P95}} | {{BASELINE_P95}} | {{DIFF_P95}} | {{STATUS_P95}} |
| 吞吐量(请求/秒) | {{CURRENT_TPS}} | {{BASELINE_TPS}} | {{DIFF_TPS}} | {{STATUS_TPS}} |
| 错误率(%) | {{CURRENT_ERROR_RATE}} | {{BASELINE_ERROR_RATE}} | {{DIFF_ERROR_RATE}} | {{STATUS_ERROR_RATE}} |

## 性能监控告警

### 已触发告警

| 告警级别 | 触发时间 | 指标 | 当前值 | 阈值 |
|----------|----------|------|--------|------|
{{ALERT_TABLE}}

### 潜在风险

| 风险项 | 当前状态 | 建议措施 |
|--------|----------|----------|
{{RISK_TABLE}}
