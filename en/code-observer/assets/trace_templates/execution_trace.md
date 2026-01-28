# Execution Tracing Report Template

## Execution Overview

**Analysis Time Range**: {{START_TIME}} - {{END_TIME}}
**Trace ID**: {{TRACE_ID}}
**Total Execution Time**: {{TOTAL_DURATION}} ms

## Execution Path Visualization

### Call Tree

```
{{CALL_TREE_VISUALIZATION}}
```

### Timeline

| Timestamp | Duration (ms) | Function/Operation | Level | Status |
|-----------|---------------|--------------------|-------|--------|
{{EXECUTION_TIMELINE_TABLE}}

## Execution Path Details

### Core Path

| Sequence | Function Name | Duration (ms) | Call Count | Avg Duration (ms) | Max Duration (ms) |
|----------|---------------|---------------|------------|-------------------|-------------------|
{{CORE_PATH_TABLE}}

### Branch Path

| Sequence | Function Name | Duration (ms) | Trigger Condition |
|----------|---------------|---------------|-------------------|
{{BRANCH_PATH_TABLE}}

## Concurrency Analysis

### Concurrent Events

| Time Point | Concurrency | Concurrent Function List |
|------------|-------------|--------------------------|
{{CONCURRENCY_TABLE}}

### Race Condition Detection

- Detected potential race conditions: {{RACE_CONDITION_COUNT}} locations
- Details:
{{RACE_CONDITION_DETAILS}}

## Execution Path Recommendations

### Optimization Suggestions

1. {{OPTIMIZATION_SUGGESTION_1}}
2. {{OPTIMIZATION_SUGGESTION_2}}
3. {{OPTIMIZATION_SUGGESTION_3}}

### Risk Warnings

- {{RISK_WARNING_1}}
- {{RISK_WARNING_2}}
