# Performance Metrics Report Template

## Performance Overview

**Analysis Time Range**: {{START_TIME}} - {{END_TIME}}
**Total Requests**: {{TOTAL_REQUESTS}}
**Average Response Time**: {{AVG_RESPONSE_TIME}} ms
**P95 Response Time**: {{P95_RESPONSE_TIME}} ms
**P99 Response Time**: {{P99_RESPONSE_TIME}} ms

## Resource Usage Statistics

### CPU Usage

| Time Period | Avg Usage (%) | Max Usage (%) | Min Usage (%) |
|-------------|---------------|---------------|---------------|
{{CPU_USAGE_TABLE}}

### Memory Usage

| Time Period | Avg Usage (MB) | Max Usage (MB) | Peak Time |
|-------------|----------------|----------------|-----------|
{{MEMORY_USAGE_TABLE}}

### I/O Statistics

| Type | Total Operations | Total Duration (ms) | Avg Duration (ms) |
|------|------------------|---------------------|-------------------|
| Read | {{READ_COUNT}} | {{READ_DURATION}} | {{READ_AVG}} |
| Write | {{WRITE_COUNT}} | {{WRITE_DURATION}} | {{WRITE_AVG}} |

## Performance Bottleneck Analysis

### High Duration Operations

| Rank | Function/Operation | Duration (ms) | Call Count | % of Total Duration |
|------|--------------------|---------------|------------|---------------------|
{{HIGH_DURATION_OPS_TABLE}}

### High Frequency Operations

| Rank | Function/Operation | Call Count | Total Duration (ms) | Avg Duration (ms) |
|------|--------------------|------------|---------------------|-------------------|
{{HIGH_FREQUENCY_OPS_TABLE}}

### Hot Paths

| Path | Total Duration (ms) | Call Count | Bottleneck Function |
|------|---------------------|------------|---------------------|
{{HOT_PATH_TABLE}}

## Performance Trend Analysis

### Response Time Trend

```
{{RESPONSE_TIME_TREND_CHART}}
```

### Resource Usage Trend

```
{{RESOURCE_USAGE_TREND_CHART}}
```

## Performance Optimization Recommendations

### Immediate Optimization (High Priority)

1. {{IMMEDIATE_OPTIMIZATION_1}}
   - Problem description: {{PROBLEM_DESCRIPTION_1}}
   - Optimization plan: {{OPTIMIZATION_PLAN_1}}
   - Expected improvement: {{EXPECTED_IMPROVEMENT_1}}

2. {{IMMEDIATE_OPTIMIZATION_2}}
   - Problem description: {{PROBLEM_DESCRIPTION_2}}
   - Optimization plan: {{OPTIMIZATION_PLAN_2}}
   - Expected improvement: {{EXPECTED_IMPROVEMENT_2}}

### Planned Optimization (Medium Priority)

1. {{PLANNED_OPTIMIZATION_1}}
   - Problem description: {{PROBLEM_DESCRIPTION_1}}
   - Optimization plan: {{OPTIMIZATION_PLAN_1}}
   - Expected improvement: {{EXPECTED_IMPROVEMENT_1}}

### Continuous Optimization (Low Priority)

1. {{ONGOING_OPTIMIZATION_1}}
   - Problem description: {{PROBLEM_DESCRIPTION_1}}
   - Optimization plan: {{OPTIMIZATION_PLAN_1}}
   - Expected improvement: {{EXPECTED_IMPROVEMENT_1}}

## Performance Baseline Comparison

| Metric | Current Value | Baseline Value | Difference | Status |
|--------|---------------|----------------|------------|--------|
| Avg Response Time | {{CURRENT_AVG}} | {{BASELINE_AVG}} | {{DIFF_AVG}} | {{STATUS_AVG}} |
| P95 Response Time | {{CURRENT_P95}} | {{BASELINE_P95}} | {{DIFF_P95}} | {{STATUS_P95}} |
| Throughput (requests/sec) | {{CURRENT_TPS}} | {{BASELINE_TPS}} | {{DIFF_TPS}} | {{STATUS_TPS}} |
| Error Rate (%) | {{CURRENT_ERROR_RATE}} | {{BASELINE_ERROR_RATE}} | {{DIFF_ERROR_RATE}} | {{STATUS_ERROR_RATE}} |

## Performance Monitoring Alerts

### Triggered Alerts

| Alert Level | Trigger Time | Metric | Current Value | Threshold |
|-------------|--------------|--------|---------------|-----------|
{{ALERT_TABLE}}

### Potential Risks

| Risk Item | Current Status | Recommended Action |
|-----------|----------------|-------------------|
{{RISK_TABLE}}
