# 执行追踪报告模板

## 执行概览

**分析时间范围**: {{START_TIME}} - {{END_TIME}}
**追踪ID**: {{TRACE_ID}}
**总执行时间**: {{TOTAL_DURATION}} ms

## 执行路径可视化

### 调用树

```
{{CALL_TREE_VISUALIZATION}}
```

### 时间轴

| 时间戳 | 耗时(ms) | 函数/操作 | 级别 | 状态 |
|--------|----------|-----------|------|------|
{{EXECUTION_TIMELINE_TABLE}}

## 执行路径详情

### 核心路径

| 序号 | 函数名 | 耗时(ms) | 调用次数 | 平均耗时(ms) | 最大耗时(ms) |
|------|--------|----------|----------|-------------|-------------|
{{CORE_PATH_TABLE}}

### 分支路径

| 序号 | 函数名 | 耗时(ms) | 触发条件 |
|------|--------|----------|----------|
{{BRANCH_PATH_TABLE}}

## 并发分析

### 并发事件

| 时间点 | 并发数 | 并发函数列表 |
|--------|--------|--------------|
{{CONCURRENCY_TABLE}}

### 竞争条件检测

- 检测到潜在竞争条件: {{RACE_CONDITION_COUNT}} 处
- 详细信息:
{{RACE_CONDITION_DETAILS}}

## 执行路径建议

### 优化建议

1. {{OPTIMIZATION_SUGGESTION_1}}
2. {{OPTIMIZATION_SUGGESTION_2}}
3. {{OPTIMIZATION_SUGGESTION_3}}

### 风险提示

- {{RISK_WARNING_1}}
- {{RISK_WARNING_2}}
