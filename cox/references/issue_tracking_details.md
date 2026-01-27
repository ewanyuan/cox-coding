# 问题追踪与响应详细流程

本文档提供复杂问题和重复问题的完整追踪和响应流程。

## 目录
- [触发条件](#触发条件)
- [响应步骤](#响应步骤)
- [智能体处理流程](#智能体处理流程)
- [使用示例](#使用示例)

---

## 触发条件

当以下情况发生时，智能体应主动触发问题追踪与响应：

1. **复杂问题**
   - 用户反馈涉及多个模块
   - 需要多步骤解决
   - 需要跨团队协作

2. **重复问题**
   - 同一问题在对话中多次出现（2次或更多）
   - 且未能顺利解决

---

## 响应步骤

### 步骤1：识别问题并确定影响模块

分析用户描述的问题，识别：
- 涉及的应用模块（从`app_status.json`中查找）
- 相关的迭代和任务（从`project_data.json`中查找）
- 问题的复杂度等级（high/medium/low）

### 步骤2：更新项目维度TODO列表

在`project_data.json`的当前迭代中添加新的TODO任务：

```json
{
  "task_id": "ISSUE-<序号>",
  "task_name": "问题追踪：<问题描述>",
  "status": "todo",
  "assignee": "<负责人，如有>",
  "priority": "<问题复杂度>",
  "tags": ["issue-tracker", "<相关模块>"],
  "issue_details": {
    "description": "<问题详细描述>",
    "affected_modules": ["<模块1>", "<模块2>"],
    "first_reported": "<首次报告时间>",
    "occurrence_count": <出现次数>,
    "complexity": "<high/medium/low>"
  }
}
```

### 步骤3：添加问题相关假设分析

在`project_data.json`的当前迭代中添加假设：

```json
{
  "assumption_id": "ASSUMP-ISSUE-<序号>",
  "description": "<假设描述，如：该问题可能由X原因导致>",
  "status": "pending",
  "validation_date": null,
  "related_issue": "ISSUE-<序号>",
  "assumption_type": "<root-cause/impact-scope/solution-approach>"
}
```

### 步骤4：建议添加相关埋点

在`test_metrics.json`的`tracing_points`中添加埋点建议：

```json
{
  "point_id": "TRACE-ISSUE-<序号>",
  "module": "<相关模块>",
  "location": "<建议位置，如：src/module.py:<行号>>",
  "metric_type": "<counter/histogram>",
  "status": "inactive",
  "last_verified": null,
  "purpose": "<埋点目的，如：追踪问题发生的次数或持续时间>",
  "related_issue": "ISSUE-<序号>"
}
```

### 步骤5：调用skill-manager存储问题信息

调用**skill-manager**技能存储问题追踪信息。

**方式一：使用辅助脚本（推荐）**
```bash
python scripts/store_to_skill_manager.py issue \
  --issue-id ISSUE-001 \
  --description "订单创建接口在高峰期经常超时" \
  --modules "订单处理模块,数据库模块" \
  --complexity high \
  --count 3
```

**方式二：直接调用 skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# 读取cox现有配置
existing_config = storage.get_config("cox") or {}
existing_logs = storage.get_logs("cox") or {}

# 更新配置：添加问题信息
existing_config["issue_id"] = "ISSUE-<序号>"
existing_config["issue_description"] = "<问题描述>"
existing_config["affected_modules"] = ["<模块1>", "<模块2>"]
existing_config["complexity"] = "<high/medium/low>"
existing_config["occurrence_count"] = <出现次数>
existing_config["first_reported"] = "<时间>"
existing_config["last_updated"] = "<时间>"

# 追加日志
existing_logs.append({
    "time": "<时间>",
    "level": "WARNING",
    "message": "检测到复杂/重复问题，已更新观测数据",
    "issue_id": "ISSUE-<序号>"
})

# 保存
storage.save("cox", config=existing_config, logs=existing_logs)
```

---

## 智能体处理流程

1. 监控对话上下文，识别复杂问题和重复问题
2. 分析问题影响范围，确定相关模块
3. 生成问题ID（格式：ISSUE-NNN）
4. 更新`project_data.json`：添加TODO任务和假设
5. 更新`test_metrics.json`：添加埋点建议
6. 调用skill-manager存储问题追踪信息
7. 向用户报告已采取的观测更新措施

---

## 使用示例

**用户反馈**："订单创建接口在高峰期经常超时，已经影响了3个客户"

**智能体响应**：

1. **识别为复杂问题**（高复杂度）
   - 涉及订单模块、影响多个客户

2. **确定影响模块**
   - 订单处理模块

3. **生成问题ID**
   - ISSUE-001

4. **更新数据文件**
   - 添加TODO任务：ISSUE-001
   - 添加假设：订单量超过当前处理能力
   - 添加埋点建议：订单处理时间histogram

5. **调用skill-manager存储问题信息**
   ```bash
   python scripts/store_to_skill_manager.py issue \
     --issue-id ISSUE-001 \
     --description "订单创建接口在高峰期经常超时" \
     --modules "订单处理模块,数据库模块" \
     --complexity high \
     --count 3
   ```

6. **报告用户**
   > 已识别为复杂问题，已更新观测：
   > - TODO任务：ISSUE-001
   > - 假设分析：订单量超过当前处理能力
   > - 埋点建议：订单处理时间histogram
   >
   > 问题信息已存储到skill-manager
