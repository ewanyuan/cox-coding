# 日志格式规范

## 目录
1. 概览
2. JSON格式日志
3. 文本格式日志
4. 字段说明
5. 示例

## 概览

本规范定义了可观测日志的标准格式，支持两种格式：JSON格式和文本格式。日志文件用于记录代码执行路径、函数调用和异常信息。

## JSON格式日志

### 结构定义

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "trace_id": "trace-12345",
  "span_id": "span-67890",
  "parent_id": "parent-11111",
  "message": "Function executed successfully",
  "function": "process_order",
  "duration_ms": 125.5,
  "args": {
    "order_id": "ORD-001",
    "user_id": "USER-001"
  },
  "result": {
    "status": "success",
    "order_total": 299.99
  },
  "exception": {
    "type": "ValueError",
    "message": "Invalid parameter",
    "stack_trace": "Traceback (most recent call last):\n  ..."
  },
  "context": {
    "module": "order_service",
    "version": "1.2.0"
  }
}
```

### 必需字段

- `timestamp`: ISO 8601格式的时间戳
- `level`: 日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
- `message`: 日志消息

### 可选字段

- `trace_id`: 分布式追踪ID
- `span_id`: Span标识符
- `parent_id`: 父Span标识符
- `function`: 函数名或方法名
- `duration_ms`: 执行耗时（毫秒）
- `args`: 函数参数
- `result`: 函数返回结果
- `exception`: 异常信息（包含type、message、stack_trace）
- `context`: 上下文信息

## 文本格式日志

### 格式定义

文本格式日志遵循以下格式：

```
[TIMESTAMP] [LEVEL] message content
```

示例：

```
[2024-01-15 10:30:45] [INFO] Function process_order executed
[2024-01-15 10:30:46] [ERROR] ValueError: Invalid parameter
[2024-01-15 10:30:47] [DEBUG] function:processOrder duration:125ms
```

### 函数调用记录格式

```
[2024-01-15 10:30:45] [INFO] function:process_order duration:125.5ms args:order_id=ORD-001,user_id=USER-001
```

### 异常记录格式

```
[2024-01-15 10:30:46] [ERROR] ValueError: Invalid parameter at line 123
```

## 字段说明

### timestamp

时间戳支持多种格式：
- ISO 8601格式：`2024-01-15T10:30:45.123Z`
- 普通格式：`2024-01-15 10:30:45`
- 带括号格式：`[2024-01-15 10:30:45]`

### level

支持的日志级别（按优先级从高到低）：
- `CRITICAL`: 严重错误，系统无法继续运行
- `ERROR`: 错误，但系统可以继续运行
- `WARNING`: 警告，潜在问题
- `INFO`: 信息性消息
- `DEBUG`: 调试信息
- `TRACE`: 更详细的追踪信息

### function

函数或方法名称，用于追踪执行路径。建议格式：
- Python: `module.function`
- Java: `com.example.Class.method`
- JavaScript: `Class.method`

### duration_ms

函数执行耗时，单位为毫秒。用于性能分析。

### exception

异常信息结构：
```json
{
  "type": "ValueError",
  "message": "Invalid parameter",
  "stack_trace": "完整堆栈跟踪"
}
```

## 示例

### 示例1：完整的JSON日志

```json
{"timestamp":"2024-01-15T10:30:45.123Z","level":"INFO","trace_id":"trace-123","span_id":"span-456","message":"Order processed successfully","function":"process_order","duration_ms":125.5,"args":{"order_id":"ORD-001","user_id":"USER-001"},"result":{"status":"success","order_total":299.99},"context":{"module":"order_service","version":"1.2.0"}}
```

### 示例2：异常日志

```json
{"timestamp":"2024-01-15T10:30:46.789Z","level":"ERROR","message":"Failed to process payment","exception":{"type":"PaymentGatewayError","message":"Payment gateway unavailable","stack_trace":"Traceback (most recent call last):\n  File 'payment.py', line 45, in process_payment\n    gateway.charge(amount)\nPaymentGatewayError: Payment gateway unavailable"},"context":{"module":"payment_service","order_id":"ORD-001"}}
```

### 示例3：文本格式日志

```
[2024-01-15 10:30:45] [INFO] Starting order processing
[2024-01-15 10:30:45] [DEBUG] function:processOrder duration:125.5ms
[2024-01-15 10:30:46] [ERROR] PaymentGatewayError: Payment gateway unavailable at payment.py:45
[2024-01-15 10:30:47] [WARNING] Retry attempt 1 failed
[2024-01-15 10:30:48] [INFO] Order ORD-001 processed successfully
```

## 验证规则

1. **时间戳必须有效**：符合ISO 8601或支持的文本格式
2. **日志级别必须有效**：必须是预定义的级别之一
3. **JSON格式必须符合规范**：可以正确解析为JSON对象
4. **耗时字段必须为数字**：duration_ms必须是数值类型
5. **异常信息必须完整**：包含type和message字段

## 注意事项

- 建议使用JSON格式，便于机器解析和分析
- 日志级别使用要恰当，避免滥用ERROR级别
- duration_ms字段仅在函数调用记录中使用
- 异常日志应包含完整的堆栈跟踪信息
- context字段用于提供额外的上下文信息，有助于问题定位
