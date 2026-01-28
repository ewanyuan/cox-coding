# Log Format Specifications

## Table of Contents
1. Overview
2. JSON Format Logs
3. Text Format Logs
4. Field Descriptions
5. Examples

## Overview

This specification defines the standard format for observability logs, supporting two formats: JSON format and text format. Log files are used to record code execution paths, function calls, and exception information.

## JSON Format Logs

### Structure Definition

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

### Required Fields

- `timestamp`: ISO 8601 format timestamp
- `level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `message`: Log message

### Optional Fields

- `trace_id`: Distributed tracing ID
- `span_id`: Span identifier
- `parent_id`: Parent Span identifier
- `function`: Function name or method name
- `duration_ms`: Execution duration in milliseconds
- `args`: Function parameters
- `result`: Function return result
- `exception`: Exception information (includes type, message, stack_trace)
- `context`: Context information

## Text Format Logs

### Format Definition

Text format logs follow following format:

```
[TIMESTAMP] [LEVEL] message content
```

Example:

```
[2024-01-15 10:30:45] [INFO] Function process_order executed
[2024-01-15 10:30:46] [ERROR] ValueError: Invalid parameter
[2024-01-15 10:30:47] [DEBUG] function:processOrder duration:125ms
```

### Function Call Record Format

```
[2024-01-15 10:30:45] [INFO] function:process_order duration:125.5ms args:order_id=ORD-001,user_id=USER-001
```

### Exception Record Format

```
[2024-01-15 10:30:46] [ERROR] ValueError: Invalid parameter at line 123
```

## Field Descriptions

### timestamp

Timestamp supports multiple formats:
- ISO 8601 format: `2024-01-15T10:30:45.123Z`
- Normal format: `2024-01-15 10:30:45`
- Bracketed format: `[2024-01-15 10:30:45]`

### level

Supported log levels (in priority order from high to low):
- `CRITICAL`: Critical error, system cannot continue running
- `ERROR`: Error, but system can continue running
- `WARNING`: Warning, potential issue
- `INFO`: Informational message
- `DEBUG`: Debug information
- `TRACE`: More detailed tracing information

### function

Function or method name, used to trace execution paths. Recommended format:
- Python: `module.function`
- Java: `com.example.Class.method`
- JavaScript: `Class.method`

### duration_ms

Function execution duration in milliseconds, used for performance analysis.

### exception

Exception information structure:
```json
{
  "type": "ValueError",
  "message": "Invalid parameter",
  "stack_trace": "Complete stack trace"
}
```

## Examples

### Example 1: Complete JSON Log

```json
{"timestamp":"2024-01-15T10:30:45.123Z","level":"INFO","trace_id":"trace-123","span_id":"span-456","message":"Order processed successfully","function":"process_order","duration_ms":125.5,"args":{"order_id":"ORD-001","user_id":"USER-001"},"result":{"status":"success","order_total":299.99},"context":{"module":"order_service","version":"1.2.0"}}
```

### Example 2: Exception Log

```json
{"timestamp":"2024-01-15T10:30:46.789Z","level":"ERROR","message":"Failed to process payment","exception":{"type":"PaymentGatewayError","message":"Payment gateway unavailable","stack_trace":"Traceback (most recent call last):\n  File 'payment.py', line 45, in process_payment\n    gateway.charge(amount)\nPaymentGatewayError: Payment gateway unavailable"},"context":{"module":"payment_service","order_id":"ORD-001"}}
```

### Example 3: Text Format Log

```
[2024-01-15 10:30:45] [INFO] Starting order processing
[2024-01-15 10:30:45] [DEBUG] function:processOrder duration:125.5ms
[2024-01-15 10:30:46] [ERROR] PaymentGatewayError: Payment gateway unavailable at payment.py:45
[2024-01-15 10:30:47] [WARNING] Retry attempt 1 failed
[2024-01-15 10:30:48] [INFO] Order ORD-001 processed successfully
```

## Validation Rules

1. **Timestamp must be valid**: Conforms to ISO 8601 or supported text format
2. **Log level must be valid**: Must be one of predefined levels
3. **JSON format must be compliant**: Can be correctly parsed as JSON object
4. **Duration field must be numeric**: duration_ms must be numeric type
5. **Exception information must be complete**: Must include type and message fields

## Precautions

- Recommend using JSON format, facilitates machine parsing and analysis
- Use log levels appropriately, avoid abusing ERROR level
- duration_ms field only used in function call records
- Exception logs should include complete stack trace information
- context field used to provide additional context information, helpful for issue localization
