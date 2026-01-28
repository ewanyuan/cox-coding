# Prometheus指标格式规范

## 目录
1. 概览
2. 指标类型
3. 格式定义
4. 标签规范
5. 示例

## 概览

Prometheus使用基于文本的格式来暴露指标数据。本规范定义了Prometheus指标的标准格式，包括四种主要指标类型：Gauge、Counter、Histogram和Summary。

## 指标类型

### Gauge（仪表盘）

Gauge类型的指标表示一个可以任意上下波动的数值。

**特点**：
- 数值可以增加或减少
- 适合表示瞬时值，如内存使用、温度等

### Counter（计数器）

Counter类型的指标表示一个只能递增的数值。

**特点**：
- 数值只能增加，不能减少（除非重置）
- 适合表示累积值，如请求总数、错误总数等

### Histogram（直方图）

Histogram类型的指标用于对观察值（如请求持续时间）进行采样和分组统计。

**特点**：
- 包含多个时间序列：
  - `*_bucket`: 观察值落区间的计数
  - `*_sum`: 所有观察值的总和
  - `*_count`: 观察值的总数

### Summary（摘要）

Summary类型的指标用于计算观察值的分位数。

**特点**：
- 包含多个时间序列：
  - `{quantile="<分位数>"}`: 计算的分位数
  - `*_sum`: 所有观察值的总和
  - `*_count`: 观察值的总数

## 格式定义

### 基本格式

```
METRIC_NAME{LABEL_NAME="LABEL_VALUE",...} VALUE
```

### 类型声明

在指标定义前使用注释声明指标类型：

```
# TYPE METRIC_NAME METRIC_TYPE
```

示例：

```
# TYPE http_requests_total counter
# TYPE http_request_duration_seconds histogram
# TYPE cpu_usage gauge
```

### 帮助信息

使用HELP注释提供指标说明：

```
# HELP METRIC_NAME 指标说明
```

## 标签规范

### 标签命名规则

- 标签名必须符合正则表达式：`[a-zA-Z_][a-zA-Z0-9_]*`
- 标签名不能以`__`开头（保留用于内部使用）
- 标签名建议使用下划线分隔的多个单词

### 标签值规则

- 标签值必须是字符串，使用双引号包裹
- 标签值中如果包含双引号，需要使用反斜杠转义
- 标签值建议具有语义化，便于查询和聚合

### 常用标签

- `job`: 作业名称
- `instance`: 实例标识
- `method`: HTTP方法（GET、POST等）
- `status`: 状态码
- `path`: 请求路径
- `module`: 模块名称
- `version`: 版本号

## 示例

### 示例1：Gauge指标

```
# TYPE cpu_usage gauge
# HELP cpu_usage CPU使用率百分比
cpu_usage{host="server1",region="us-west"} 45.2
cpu_usage{host="server2",region="us-east"} 67.8

# TYPE memory_usage_bytes gauge
# HELP memory_usage_bytes 内存使用量（字节）
memory_usage_bytes{host="server1"} 8589934592
memory_usage_bytes{host="server2"} 10737418240
```

### 示例2：Counter指标

```
# TYPE http_requests_total counter
# HELP http_requests_total HTTP请求总数
http_requests_total{method="GET",status="200"} 12345
http_requests_total{method="GET",status="404"} 567
http_requests_total{method="POST",status="200"} 2345
http_requests_total{method="POST",status="500"} 23

# TYPE errors_total counter
# HELP errors_total 错误总数
errors_total{type="database"} 45
errors_total{type="network"} 12
errors_total{type="application"} 8
```

### 示例3：Histogram指标

```
# TYPE http_request_duration_seconds histogram
# HELP http_request_duration_seconds HTTP请求持续时间分布
http_request_duration_seconds_bucket{le="0.1"} 10000
http_request_duration_seconds_bucket{le="0.5"} 45000
http_request_duration_seconds_bucket{le="1.0"} 80000
http_request_duration_seconds_bucket{le="5.0"} 95000
http_request_duration_seconds_bucket{le="+Inf"} 100000
http_request_duration_seconds_sum 250000
http_request_duration_seconds_count 100000

# TYPE function_execution_time_ms histogram
# HELP function_execution_time_ms 函数执行时间分布
function_execution_time_ms_bucket{function="process_order",le="10"} 5000
function_execution_time_ms_bucket{function="process_order",le="50"} 45000
function_execution_time_ms_bucket{function="process_order",le="100"} 80000
function_execution_time_ms_bucket{function="process_order",le="+Inf"} 100000
function_execution_time_ms_sum{function="process_order"} 5500000
function_execution_time_ms_count{function="process_order"} 100000
```

### 示例4：Summary指标

```
# TYPE response_time summary
# HELP response_time 响应时间统计
response_time{quantile="0.5"} 0.123
response_time{quantile="0.9"} 0.456
response_time{quantile="0.99"} 0.789
response_time_sum 12345.6
response_time_count 100000

# TYPE function_duration summary
# HELP function_duration 函数执行时间统计
function_duration{function="process_order",quantile="0.5"} 125.5
function_duration{function="process_order",quantile="0.9"} 234.5
function_duration{function="process_order",quantile="0.99"} 456.7
function_duration_sum{function="process_order"} 125500
function_duration_count{function="process_order"} 1000
```

### 示例5：完整的指标文件

```
# TYPE cpu_usage gauge
# HELP cpu_usage CPU使用率百分比
cpu_usage{host="server1",region="us-west"} 45.2
cpu_usage{host="server2",region="us-east"} 67.8

# TYPE http_requests_total counter
# HELP http_requests_total HTTP请求总数
http_requests_total{method="GET",status="200"} 12345
http_requests_total{method="GET",status="404"} 567
http_requests_total{method="POST",status="200"} 2345
http_requests_total{method="POST",status="500"} 23

# TYPE http_request_duration_seconds histogram
# HELP http_request_duration_seconds HTTP请求持续时间分布
http_request_duration_seconds_bucket{le="0.1"} 10000
http_request_duration_seconds_bucket{le="0.5"} 45000
http_request_duration_seconds_bucket{le="1.0"} 80000
http_request_duration_seconds_bucket{le="5.0"} 95000
http_request_duration_seconds_bucket{le="+Inf"} 100000
http_request_duration_seconds_sum 250000
http_request_duration_seconds_count 100000

# TYPE response_time summary
# HELP response_time 响应时间统计
response_time{quantile="0.5"} 0.123
response_time{quantile="0.9"} 0.456
response_time{quantile="0.99"} 0.789
response_time_sum 12345.6
response_time_count 100000
```

## 验证规则

1. **指标名称必须有效**：符合命名规范
2. **指标值必须为数字**：可以是整数或浮点数
3. **标签值必须用双引号包裹**：正确转义特殊字符
4. **类型声明必须在指标定义之前**：使用`# TYPE`注释
5. **Histogram必须包含bucket、sum、count**：缺少任何一个都是不完整的
6. **Summary必须包含quantile、sum、count**：缺少任何一个都是不完整的

## 注意事项

- 指标命名应具有语义化，便于理解
- 标签数量不宜过多，避免高基数问题
- Counter类型指标只能在服务启动或重启时重置
- Histogram适合观察值范围已知的情况
- Summary适合需要精确分位数的情况
- 定期检查指标数据的有效性和准确性
