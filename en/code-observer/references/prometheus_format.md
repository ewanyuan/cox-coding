# Prometheus Metrics Format Specifications

## Table of Contents
1. Overview
2. Metric Types
3. Format Definition
4. Label Specifications
5. Examples

## Overview

Prometheus uses text-based format to expose metrics data. This specification defines the standard format for Prometheus metrics, including four main metric types: Gauge, Counter, Histogram, and Summary.

## Metric Types

### Gauge

Gauge type metrics represent a value that can arbitrarily go up or down.

**Characteristics**:
- Value can increase or decrease
- Suitable for representing instantaneous values, such as memory usage, temperature, etc.

### Counter

Counter type metrics represent a value that can only increase.

**Characteristics**:
- Value can only increase, cannot decrease (unless reset)
- Suitable for representing cumulative values, such as total requests, total errors, etc.

### Histogram

Histogram type metrics are used to sample and group statistics of observed values (such as request duration).

**Characteristics**:
- Contains multiple time series:
  - `*_bucket`: Count of observations falling in bucket
  - `*_sum`: Sum of all observed values
  - `*_count`: Count of all observations

### Summary

Summary type metrics are used to calculate quantiles of observed values.

**Characteristics**:
- Contains multiple time series:
  - `{quantile="<quantile>"}`: Calculated quantile
  - `*_sum`: Sum of all observed values
  - `*_count`: Count of all observations

## Format Definition

### Basic Format

```
METRIC_NAME{LABEL_NAME="LABEL_VALUE",...} VALUE
```

### Type Declaration

Use comment to declare metric type before metric definition:

```
# TYPE METRIC_NAME METRIC_TYPE
```

Example:

```
# TYPE http_requests_total counter
# TYPE http_request_duration_seconds histogram
# TYPE cpu_usage gauge
```

### HELP Information

Use HELP comment to provide metric description:

```
# HELP METRIC_NAME Metric description
```

## Label Specifications

### Label Naming Rules

- Label names must conform to regex: `[a-zA-Z_][a-zA-Z0-9_]*`
- Label names cannot start with `__` (reserved for internal use)
- Label names recommended to use underscore-separated multiple words

### Label Value Rules

- Label values must be strings, wrapped in double quotes
- If label values contain double quotes, need backslash escaping
- Label values recommended to be semantic, facilitating query and aggregation

### Common Labels

- `job`: Job name
- `instance`: Instance identifier
- `method`: HTTP method (GET, POST, etc.)
- `status`: Status code
- `path`: Request path
- `module`: Module name
- `version`: Version number

## Examples

### Example 1: Gauge Metrics

```
# TYPE cpu_usage gauge
# HELP cpu_usage CPU usage percentage
cpu_usage{host="server1",region="us-west"} 45.2
cpu_usage{host="server2",region="us-east"} 67.8

# TYPE memory_usage_bytes gauge
# HELP memory_usage_bytes Memory usage in bytes
memory_usage_bytes{host="server1"} 8589934592
memory_usage_bytes{host="server2"} 10737418240
```

### Example 2: Counter Metrics

```
# TYPE http_requests_total counter
# HELP http_requests_total Total HTTP requests
http_requests_total{method="GET",status="200"} 12345
http_requests_total{method="GET",status="404"} 567
http_requests_total{method="POST",status="200"} 2345
http_requests_total{method="POST",status="500"} 23

# TYPE errors_total counter
# HELP errors_total Total errors
errors_total{type="database"} 45
errors_total{type="network"} 12
errors_total{type="application"} 8
```

### Example 3: Histogram Metrics

```
# TYPE http_request_duration_seconds histogram
# HELP http_request_duration_seconds HTTP request duration distribution
http_request_duration_seconds_bucket{le="0.1"} 10000
http_request_duration_seconds_bucket{le="0.5"} 45000
http_request_duration_seconds_bucket{le="1.0"} 80000
http_request_duration_seconds_bucket{le="5.0"} 95000
http_request_duration_seconds_bucket{le="+Inf"} 100000
http_request_duration_seconds_sum 250000
http_request_duration_seconds_count 100000

# TYPE function_execution_time_ms histogram
# HELP function_execution_time_ms Function execution time distribution
function_execution_time_ms_bucket{function="process_order",le="10"} 5000
function_execution_time_ms_bucket{function="process_order",le="50"} 45000
function_execution_time_ms_bucket{function="process_order",le="100"} 80000
function_execution_time_ms_bucket{function="process_order",le="+Inf"} 100000
function_execution_time_ms_sum{function="process_order"} 5500000
function_execution_time_ms_count{function="process_order"} 100000
```

### Example 4: Summary Metrics

```
# TYPE response_time summary
# HELP response_time Response time statistics
response_time{quantile="0.5"} 0.123
response_time{quantile="0.9"} 0.456
response_time{quantile="0.99"} 0.789
response_time_sum 12345.6
response_time_count 100000

# TYPE function_duration summary
# HELP function_duration Function execution time statistics
function_duration{function="process_order",quantile="0.5"} 125.5
function_duration{function="process_order",quantile="0.9"} 234.5
function_duration{function="process_order",quantile="0.99"} 456.7
function_duration_sum{function="process_order"} 125500
function_duration_count{function="process_order"} 1000
```

### Example 5: Complete Metrics File

```
# TYPE cpu_usage gauge
# HELP cpu_usage CPU usage percentage
cpu_usage{host="server1",region="us-west"} 45.2
cpu_usage{host="server2",region="us-east"} 67.8

# TYPE http_requests_total counter
# HELP http_requests_total Total HTTP requests
http_requests_total{method="GET",status="200"} 12345
http_requests_total{method="GET",status="404"} 567
http_requests_total{method="POST",status="200"} 2345
http_requests_total{method="POST",status="500"} 23

# TYPE http_request_duration_seconds histogram
# HELP http_request_duration_seconds HTTP request duration distribution
http_request_duration_seconds_bucket{le="0.1"} 10000
http_request_duration_seconds_bucket{le="0.5"} 45000
http_request_duration_seconds_bucket{le="1.0"} 80000
http_request_duration_seconds_bucket{le="5.0"} 95000
http_request_duration_seconds_bucket{le="+Inf"} 100000
http_request_duration_seconds_sum 250000
http_request_duration_seconds_count 100000

# TYPE response_time summary
# HELP response_time Response time statistics
response_time{quantile="0.5"} 0.123
response_time{quantile="0.9"} 0.456
response_time{quantile="0.99"} 0.789
response_time_sum 12345.6
response_time_count 100000
```

## Validation Rules

1. **Metric name must be valid**: Conforms to naming specification
2. **Metric value must be numeric**: Can be integer or floating-point
3. **Label values must be wrapped in double quotes**: Correctly escape special characters
4. **Type declaration must precede metric definition**: Use `# TYPE` comment
5. **Histogram must include bucket, sum, count**: Missing any is incomplete
6. **Summary must include quantile, sum, count**: Missing any is incomplete

## Precautions

- Metric naming should be semantic, easy to understand
- Label quantity shouldn't be too many, avoid high cardinality issues
- Counter type metrics can only reset at service startup or restart
- Histogram suitable when observed value range known
- Summary suitable when need precise quantiles
- Regularly check metric data validity and accuracy
