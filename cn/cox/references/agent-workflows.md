# Agent 工作流程详细指南

本文档详细说明 Agent 使用 Cox 技能时的各种工作流程。

---

## 1. 模块状态更新流程

### 前置检查

Agent 准备使用 `update-module` 命令前，应确保：
1. 已完成代码分析和实现
2. 已得到用户确认（用户明确表示满意或问题已解决）
3. 模块当前状态正常（非 `has_issue`）

### 正确的更新时机

```
✅ 正确流程：
1. 用户标记 has_issue
2. 用户说"继续，规划下一个迭代"
3. Agent 将问题加入迭代任务
4. 执行任务，解决问题
5. 询问用户确认："问题已解决，是否满意？"
6. 用户确认后，使用 update-module 更新状态

❌ 错误流程：
1. 用户标记 has_issue
2. Agent 没等用户说话，直接 update-module 覆盖
```

### 使用方法

```bash
python scripts/collect_data.py update-module \
  --app app_status.json \
  --module "ModuleName" \
  --status optimized \
  --rate 1.0 \
  --notes "已完成优化，用户确认满意"
```

### 对话示例

```
User: View Post List 标记为 has_issue，描述：不够美观

Agent: 我已记录你的反馈：
       - 模块：View Post List
       - 问题描述：不够美观
       - 优先级：Medium (UI/UX 优化)

       我会将这个问题纳入下一个迭代规划。

User: 好，继续规划下一个迭代

Agent: 规划 ITER-003，我发现：
       - ISSUE-001: View Post List "不够美观" (Medium)
       - TASK-011: 添加搜索功能 (High)

       建议优先级排序：
       1. TASK-011: 添加搜索功能
       2. ISSUE-001: 优化 View Post List UI

       可以开始吗？

User: 可以

[Agent 执行任务...]

Agent: ISSUE-001 已完成：
       - 重新设计了帖子列表布局
       - 优化了卡片样式和间距
       - 添加了更多视觉元素

       请查看效果，是否满意？

User: 满意

Agent: 收到，正在更新模块状态...

[使用 update-module 命令更新状态]
```

---

## 2. 用户反馈处理流程

### 流程图

```mermaid
flowchart TB
    Start[用户在网页标记 has_issue] --> Record[Agent 记录问题]
    Record --> Continue[继续当前工作]
    Continue --> UserInput{用户输入}
    UserInput -->|说"继续"或"规划下一迭代"| Collect[收集所有待办内容]
    Collect --> Tasks[原有待办任务]
    Collect --> Issues[用户反馈的问题]
    Tasks --> Prioritize[评估优先级]
    Issues --> Prioritize
    Prioritize --> Sort[按优先级排序]
    Sort --> Plan[规划下一个迭代]
    Plan --> Execute[执行任务]
    Execute --> Confirm[询问用户确认]
    Confirm --> UserConfirm{用户确认?}
    UserConfirm -->|是| Update[使用 update-module 更新状态]
    UserConfirm -->|否| Plan
```

### 优先级评估矩阵

| Priority | Type | 评估标准 | 示例 |
|----------|------|----------|------|
| **Critical** | 安全问题 | 数据泄露、权限绕过 | 用户可以绕过登录访问他人数据 |
| **High** | 功能BUG | 核心功能无法使用 | 发帖功能完全失效 |
| **High** | 性能问题 | 严重影响使用 | 页面加载超过10秒 |
| **Medium** | UI/UX优化 | 体验不佳但功能正常 | "不够美观"、"不好用" |
| **Medium** | 小BUG | 不影响主要功能 | 文字错误、小样式问题 |
| **Low** | 功能建议 | 锦上添花 | "希望能加个暗黑模式" |

### 处理原则

1. **不打断当前工作**：用户反馈记录后，继续完成当前迭代
2. **批量处理**：在规划下一个迭代时，统一评估所有待办和反馈
3. **优先级驱动**：高优先级问题优先处理
4. **用户确认**：问题解决后必须得到用户确认才更新状态

---

## 3. 迭代管理流程

迭代管理的详细理论、MVP原则、风险评估和实施决策见 [iteration_management.md](iteration_management.md)。

本文档聚焦于Agent在迭代管理中的**操作流程**：

### 快速参考

**阶段1：项目启动**
```bash
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "项目名称" \
  --iterations 3 \
  --modules '[{"id":"MOD-001","name":"模块1"}]'
```

**阶段2：规划迭代**
- 与用户确认迭代目标
- 填充 tasks 数组
- 确认计划后开始执行

**阶段3：完成并规划下一个**
- 收集用户反馈和 has_issue 标记
- 评估优先级
- 规划下一个迭代

### 与问题追踪的协作

迭代管理过程中涉及的问题追踪：
- 用户在网页标记 has_issue → 记录问题
- 规划下一迭代时统一评估
- 问题解决后更新模块状态

详见本文档的"用户反馈处理流程"和"问题追踪流程"章节。

---

## 4. 问题追踪流程

### 何时触发

Agent 应主动触发问题追踪：
1. **复杂问题**：涉及多个模块，需要多步解决
2. **重复问题**：同一个问题在对话中出现2次以上且未解决

### 处理步骤

```
1. 识别问题 → 确定影响模块
2. 生成问题ID → ISSUE-NNN
3. 更新 project_data.json → 添加 TODO 任务
4. 更新 test_metrics.json → 添加埋点建议（如适用）
5. 调用 skill-manager → 存储问题信息
6. 报告用户 → 说明已采取的措施
```

---

## 5. 常见场景处理

### 场景1：用户在网页标记 has_issue

```
Agent 的响应：
"我看到你标记了 [模块名] 有问题：[问题描述]
 我已记录此问题（ISSUE-NNN），优先级：[评估结果]
 我会在规划下一个迭代时统一处理。
 是否继续当前迭代，还是现在处理这个问题？"
```

### 场景2：规划下一个迭代

```
Agent 的响应：
"规划 [迭代名称]，我发现：

 待办任务：
 - TASK-XXX: [任务名] ([优先级])

 用户反馈：
 - ISSUE-XXX: [问题描述] ([优先级])

 建议的迭代计划：
 1. [按优先级排序的任务列表]

 这个计划可以吗？"
```

### 场景3：任务完成，询问确认

```
Agent 的响应：
"[ISSUE-XXX/TASK-XXX] 已完成：
 - 具体做了什么
 - 修改了哪些文件

 请确认是否满意？"

 用户确认后：
 "收到，正在更新模块状态..."
 [执行 update-module]
 "模块 [模块名] 状态已更新为 [状态]"
```

---

## 6. 数据格式参考

### project_data.json 中的模块

```json
{
  "iteration_id": "ITER-001",
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "View Post List",
      "expected_completion": 0.8
    }
  ]
}
```

### app_status.json 中的模块

```json
{
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "View Post List",
      "status": "has_issue",
      "completion_rate": 0.8,
      "owner": "Developer",
      "last_update": "2026-01-30",
      "notes": "帖子列表已实现",
      "issue_description": "不够美观。"
    }
  ]
}
```

---

## 附录

### A. update-module 命令参数

| 参数 | 必填 | 说明 |
|------|------|------|
| --app | 是 | app_status.json 文件路径 |
| --module | 是 | 模块名称 |
| --status | 是 | 目标状态：pending/developed/confirmed/optimized |
| --rate | 否 | 完成率 0.0-1.0，默认 1.0 |
| --notes | 否 | 备注说明 |

### B. 状态值说明

| 状态 | 含义 | 使用场景 |
|------|------|----------|
| pending | 待开发 | 模块尚未开始 |
| developed | 已开发 | 功能已实现，待验证 |
| confirmed | 已确认 | 功能已验证，待优化 |
| optimized | 已优化 | 功能已完成并优化 |
| has_issue | 有问题 | 用户标记了问题 |

### C. 优先级值说明

| 优先级 | 含义 | 响应时间 |
|--------|------|----------|
| critical | 关键 | 立即处理 |
| high | 高 | 下一迭代优先 |
| medium | 中 | 下一迭代酌情处理 |
| low | 低 | 有时间再说 |

### D. 风险等级值说明

| 风险 | 含义 | 处理策略 |
|------|------|----------|
| high | 高风险 | 单独处理，完成后立即验证 |
| low | 低风险 | 可与其他低风险任务批量处理，一起验证 |
