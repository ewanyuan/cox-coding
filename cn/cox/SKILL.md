---
name: cox
version: v1.0.0
description: Cox 编程 - 为您的 AI 编程体验保驾护航。帮助开发团队掌握项目进展、识别开发风险、了解系统健康状态。提供项目进度跟踪、迭代管理（MVP驱动）、任务状态管理、开发假设记录、应用模块监控、测试埋点和异常分析等功能。支持静态网页和交互网页两种方案，适合不同环境和团队规模。网页按迭代分组展示，清晰呈现每个迭代的进度和任务。
dependency:
  python:
    - flask>=2.0.0  # 仅交互网页方案需要
  system: []
---

# COX 编程 - 为您的 AI 编程体验保驾护航

## 任务目标
- **COX 的角色**：COX 是**AI 编程导航员**，负责项目管理和可观测，不直接编写代码或实现功能
- **协作模式**：COX 与开发技能配合使用
  - COX：负责项目规划、迭代管理、进度跟踪、问题追踪
  - 开发技能（如 cox-coding）：负责具体的功能实现和代码编写
- 能力包含：
  1. 项目维度：跟踪迭代进度、任务状态、开发假设
  2. 应用维度：监控应用功能模块状态
  3. 测试维度：管理测试埋点、分析异常情况

## 触发条件

COX 会在以下任一情况触发：

### 软件开发支持（核心场景）
当用户提出软件开发需求时，COX 应**主动启用**项目管理和迭代管理流程：
- **用户表达**："做一个博客"、"开发计算器"、"实现XX功能"、"做一个电商系统"
- **协作流程**：
  1. COX 理解需求，规划项目结构和迭代
  2. COX 生成可观测数据（项目进度、任务列表、模块规划）
  3. COX 将规划传递给开发技能（如 cox-coding）进行具体实现
  4. COX 持续跟踪进度，更新可观测数据

**示例对话**：
```
用户：HI COX, 做个计算器
COX：好的，我来帮你规划计算器项目的开发。让我先创建项目可观测数据...
[调用脚本生成数据，规划迭代和任务]
COX：项目已规划完成，包含以下模块：
- UI界面模块
- 计算逻辑模块
- 历史记录模块

现在我来拆解迭代任务，然后请开发技能实现具体功能。
```

### 项目进展
- "想知道项目进展如何"、"迭代完成度是多少"
- "查看任务状态"、"哪些任务完成了"、"还有哪些待办"

### 问题追踪
- "经常出bug怎么跟踪"、"重复问题怎么处理"、"需要记录待解决的问题"
- "有没有需要关注的异常"

### 质量保障
- "需要监控接口性能"、"怎么发现系统异常"、"测试覆盖率怎么样"
- "接口响应时间慢"、"系统有异常"

### 团队协作
- "需要共享项目信息"、"让团队成员了解现状"、"需要可视化仪表板"

## 部署方案选择

在开始使用前，请根据团队需求选择部署方案。详细配置说明见 [references/deployment_details.md](references/deployment_details.md)。

### 交互网页方案（推荐）
- **特点**：提供本地 Web 界面，支持实时数据刷新（每 30 秒），支持交互
- **适用场景**：需要实时监控
- **使用门槛**：需要安装 Flask（`pip install flask`）
- **使用方式**：调用 `scripts/run_web_observability.py --mode web`，访问 http://localhost:5000

### 静态网页方案
- **特点**：生成静态 HTML 文件，数据内联到 HTML 中，无需额外的 JSON 文件
- **适用场景**：受限环境（如在线沙盒环境）、快速验证需求
- **使用门槛**：无需任何额外依赖（不需要安装 Flask）
- **使用方式**：调用 `scripts/run_web_observability.py --mode static`，生成 `observability.html` 文件
- **刷新方式**：点击刷新按钮重新渲染数据（静态模式不支持自动刷新）

### 全面方案（暂不提供）
- 特点：使用 Prometheus + Grafana 专业可观测工具，Docker 部署
- 适用场景：准备迁移到生产环境、需要专业监控能力
- 状态：暂不开放，待完善数据对接和配置方案后上线

## 快速开始

### 步骤1：生成可观测数据

**推荐方式：使用脚本生成数据**

为了确保数据格式 100% 符合规范，建议使用数据生成脚本：

```bash
# 方式1：生成最小数据集（快速体验）
python scripts/generate_observability_data.py \
  --mode minimal \
  --project-name "我的项目" \
  --app-name "我的应用"

# 方式2：生成自定义模块（推荐）
# 智能体应根据实际需求拆解任务，而不是使用示例任务
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "计算器项目" \
  --app-name "计算器应用" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI界面模块"},{"id":"MOD-002","name":"计算逻辑模块"}]'


# 方式2.5：使用自定义迭代名称（推荐）
# 为每个迭代指定有意义的名称，而不是默认的"第N次迭代"
python scripts/generate_observability_data.py   --mode complete   --project-name "计算器项目"   --app-name "计算器应用"   --iterations 4   --modules '[{"id":"MOD-001","name":"UI界面模块"},{"id":"MOD-002","name":"计算逻辑模块"}]'   --iteration-names '["核心基础与平台配置","计划管理与假设管理","内容生成工作流","智能辅助与优化"]'

# 方式3：生成完整示例（包含测试套件框架，但任务、埋点、异常留空）
python scripts/generate_observability_data.py \
  --mode complete \
  --project-name "计算器项目" \
  --app-name "计算器应用" \
  --iterations 2 \
  --modules '[{"id":"MOD-001","name":"UI界面模块"},{"id":"MOD-002","name":"计算逻辑模块"}]'
```

脚本会在当前目录生成三个 JSON 文件：
- `project_data.json`：项目迭代和任务数据
- `app_status.json`：应用模块状态数据
- `test_metrics.json`：测试埋点和异常数据

**核心原则**：
- **示例数据仅提供最小骨架**，不填充任何虚假的业务数据
- **任务、埋点、异常默认为空**，由智能体根据实际情况填写
- 一切以真实数据为准，避免产生误导

**关于任务的说明**：
- **脚本行为**：默认生成空的 tasks 数组，无需额外参数。智能体应根据实际需求拆解任务后填充。
- **任务字段**：
  - `task_id`: 任务ID（如 TASK-001）
  - `task_name`: 任务名称（具体描述，如"设计计算器UI界面"）
  - `status`: 任务状态（todo/in_progress/completed/delayed）
  - `assignee`: 负责人（可选，如需要团队协作时填写）
  - `priority`: 优先级（low/medium/high/critical）
  - `tags`: 标签（可选，用于分类）

**关于埋点和异常的说明**：
- **默认为空**：脚本生成的 tracing_points 和 anomalies 均为空数组 `[]`
- **真实数据填写**：应由智能体根据实际监控数据填充
- **数据字段**：
  - `tracing_points`: 测试埋点（模块、位置、状态、指标类型）
  - `anomalies`: 异常记录（类型、描述、严重程度、状态、发生次数、时间）

**自定义模块说明**：
- 使用 `--modules` 参数可以定义项目实际需要的模块
- 模块列表为 JSON 格式，包含 id 和 name 字段
- 智能体在调用脚本时，应根据项目需求自动推断合适的模块

**⚠️ 关键规则：模块定义规则**
- **模块必须是用户可验证的功能**，而不是技术组件
- **禁止的模块名**："UI模块"、"后端模块"、"数据库模块"、"逻辑模块"、"接口模块"等
- **正确的模块示例**："用户登录"、"文章列表"、"添加到购物车"、"搜索"、"支付"
- **从用户角度思考**："我可以看到和测试什么？"而不是"它是如何实现的？"

**后续使用**：
- 直接修改生成的 JSON 文件以适应实际项目
- 数据格式说明见 [references/data_format.md](references/data_format.md)

### 步骤2：选择方案并启动

**交互网页方案（推荐）**：
```bash
# 启动 Web 服务器（需要先安装 Flask：pip install flask）
python scripts/run_web_observability.py \
  --mode web \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 127.0.0.1 \
  --port 5000

# 访问 http://127.0.0.1:5000 查看界面，数据每 30 秒自动刷新
```

**静态网页方案**：
```bash
# 生成静态 HTML 文件（无需 Flask）
# 数据会被内联到 HTML 中，无需额外的 JSON 文件
python scripts/run_web_observability.py \
  --mode static \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output observability.html

# 直接用浏览器打开 observability.html 查看界面
# 数据已内联，无需其他文件
```

**说明**：
- Web 模式：数据实时更新，无需重新生成，访问 http://127.0.0.1:5000 查看界面
- 静态模式：数据内联到 HTML 文件中，生成一次后数据固定，点击刷新按钮可重新渲染

### 步骤3：调用skill-manager存储部署信息
部署完成后，调用 **skill-manager** 技能存储部署信息，便于后续管理和技能协作。

详细调用方式见 [references/deployment_details.md](references/deployment_details.md)。

### 步骤4：持续更新数据
在开发过程中，定期更新数据文件，然后重新生成静态 HTML（静态模式）或刷新页面（Web 模式）。智能体可以协助您分析现有数据，识别需要更新的内容。

### 步骤5：技能执行完成后的引导

**智能体应主动提醒用户**：
执行完 COX 技能后，智能体应主动提醒用户查看项目页面，并告知当前状态和后续行动建议。

**标准引导流程**：

1. **告知用户数据已生成**
   - 明确说明项目数据文件已生成
   - 说明项目页面已生成

2. **提供查看方式**
   - Web 模式：访问 http://127.0.0.1:5000
   - 静态模式：用浏览器打开 observability.html

3. **总结当前迭代计划**
   - 读取 project_data.json 中的 current_iteration
   - 列出当前迭代的所有任务（task_name、status）
   - 说明已完成/进行中/待办的任务数量

4. **识别下一步行动**
   - 查找状态为 pending 或 todo 的任务
   - 按优先级（priority）排序：critical > high > medium > low
   - 推荐下一个要处理的任务

5. **协调其他技能**
   - 对于需要开发的任务，建议调用开发技能（如 cox-coding）
   - 对于需要测试的任务，建议更新 test_metrics.json
   - 对于需要部署的任务，建议调用 skill-manager

6. **用户确认**
   - 询问用户："您希望现在开始处理哪个任务？"
   - 根据用户选择调用相应的技能

**示例对话**：
```
智能体：COX 已为您生成项目数据。

您可以通过以下方式查看项目页面：
- Web 模式：访问 http://127.0.0.1:5000
- 静态模式：用浏览器打开 observability.html

当前迭代：迭代1 - 基础功能开发
- 已完成：2 个任务
- 进行中：1 个任务
- 待办：3 个任务

COX 建议的下一步行动：
1. 完成任务"用户登录接口"（优先级：high）
2. 开始任务"数据持久化模块"（优先级：medium）

您希望现在开始处理哪个任务？或者您有其他想法？
```

## 核心功能说明

### 智能体可处理的功能
- **需求分析与模块规划**：根据用户需求（如"做一个计算器"）分析核心功能，自动推断合适的模块列表
- **数据生成指导**：根据项目需求生成自定义模块列表，调用数据生成脚本
- **数据分析**：分析现有可观测数据，识别项目瓶颈
- **使用指导**：解答两种方案的选择和部署问题
- **数据更新建议**：根据开发进度提供数据更新建议
- **模块状态更新**：使用 `scripts/collect_data.py update-module` 命令在代码分析和用户确认后更新模块成熟度
- **用户反馈处理**：从交互网页记录用户反馈，根据优先级纳入下一迭代规划
- **问题追踪与响应**：识别复杂问题和重复问题，自动更新观测数据（TODO任务、假设分析、埋点建议）

详细工作流程见：[Agent 工作流程指南](references/agent-workflows.md)

**关键工作流程**：
- 用户反馈处理：[references/agent-workflows.md](references/agent-workflows.md#2-user-feedback-processing-workflow)
- 问题追踪：[references/agent-workflows.md](references/agent-workflows.md#4-issue-tracking-workflow)
- 常见场景：[references/agent-workflows.md](references/agent-workflows.md#5-common-scenario-handling)

**重要：用户反馈处理**
- **在规划任何迭代之前，必须检查 app_status.json 中的用户反馈（状态为 "has_issue" 的模块）**
- 用户反馈位置：app_status.json（module.status = "has_issue"，module.issue_description）
- 检查时机：在最终确定迭代任务之前（步骤3.5）
- 优先级评估：使用 references/agent-workflows.md 中的优先级评估矩阵
- **用户反馈必须被视为高优先级输入，并在迭代规划中明确报告**

### 脚本实现的功能
- **数据生成**：`scripts/generate_observability_data.py` 生成符合规范的可观测数据（避免大模型幻觉）
- **数据采集与验证**：`scripts/collect_data.py`
  - 验证 JSON 数据格式是否符合规范
  - **update-module 命令**：在代码分析和用户确认后更新模块状态
  - 用法：`python scripts/collect_data.py update-module --app app_status.json --module "ModuleName" --status optimized --rate 1.0 --notes "..."`
- **静态网页生成**：`scripts/run_web_observability.py --mode static` 生成静态 HTML 文件（数据内联，无需 Flask）
- **交互网页服务**：`scripts/run_web_observability.py --mode web` 启动 Flask Web 服务器
- **Skill-manager存储工具**：`scripts/store_to_skill_manager.py` 存储部署信息和问题追踪信息

## 迭代管理流程

### 触发条件
当用户提出需要开发新功能、构建新项目或进行复杂需求实现时，智能体应主动启用迭代管理流程。

### MVP 驱动的迭代拆分原则

智能体在拆分迭代时，应遵循 **MVP（最小可行产品）** 原则：

1. **第一迭代**：核心功能
   - 识别用户可见的核心功能
   - 用最简单的方式实现
   - 快速交付让用户确认

2. **第二迭代**：增强功能
   - 根据用户反馈调整
   - 添加次要功能
   - 优化用户体验

3. **后续迭代**：完善与优化
   - 逐步完善细节
   - 性能优化
   - 边缘情况处理

### 迭代规划方法

**两阶段规划**：

**阶段1 - 项目启动时**：
- 初步规划 2-3 个迭代的大致方向
- 调用数据生成脚本: `--iterations 3`
- 生成迭代框架，但 `tasks` 数组为空
- 每个 iteration 包含 `modules` 列表，但不包含详细任务

**阶段2 - 逐个迭代详细规划**：
- 规划第一个迭代的详细任务，填充 `tasks` 数组
- 完成后，基于用户反馈规划下一个迭代
- 每个迭代都基于最新的用户反馈调整

**关键点**：
- ✅ 先有迭代框架，逐个填充详细任务
- ❌ 不是一开始就规划所有迭代的所有细节

详细迭代规划方法、风险评估和实施决策指南见 [references/iteration_management.md](references/iteration_management.md)。

### 迭代管理流程

**步骤1：需求分析与迭代拆分**
1. 理解用户需求的核心目标
2. 识别用户可见的功能点
3. 按照优先级拆分成多个迭代
4. 每个迭代聚焦于一个明确的目标

**步骤2：调用数据生成脚本**
智能体根据项目需求自动推断模块列表并调用数据生成脚本。

**步骤3：智能体拆解任务并填充数据**
1. 分析用户需求，拆解具体任务
2. 为每个迭代填充 `tasks` 数组
3. 设置任务状态和优先级

**步骤3.5：检查用户反馈（关键）**
在最终确定迭代任务之前，智能体必须：

1. **扫描用户反馈**
   - 读取 app_status.json
   - 查找所有状态为 "has_issue" 的模块
   - 提取每个受影响模块的 issue_description

2. **评估反馈优先级**
   - 使用 [references/agent-workflows.md](references/agent-workflows.md#priority-evaluation-matrix) 中的优先级评估矩阵
   - 确定优先级：Critical > High > Medium > Low

3. **为反馈创建任务**
   - 创建任务，名称为："修复用户反馈：[issue_description]"
   - 根据矩阵设置优先级
   - 添加标签："user-feedback"
   - 根据复杂度设置 risk_level

4. **在迭代中优先级排序**
   - Critical/High 优先级反馈 → 当前迭代
   - Medium/Low 优先级反馈 → 下一迭代
   - 在迭代说明中记录决策

详细脚本调用参数、任务字段说明和示例见 [references/iteration_management.md](references/iteration_management.md)。

**步骤4：与用户确认迭代计划**
1. 展示第一迭代的计划和预期成果
2. **列出任何用户反馈任务及其优先级**
3. **说明哪些反馈包含在当前迭代中**
4. **说明哪些反馈推迟到未来迭代（并说明原因）**
5. 询问用户是否同意
6. 根据用户反馈调整计划

**步骤5：与开发技能协作并更新数据**
1. 将迭代规划和任务列表传递给开发技能（如 cox-coding）
2. 开发技能实现具体功能，COX 跟踪进度
3. 更新任务状态和模块完成率
4. 与用户确认成果
5. 询问是否进入下一迭代

详细协作示例和对话流程见 [references/iteration_management.md](references/iteration_management.md)。

### 模块成熟度更新触发方式

模块成熟度数据通过以下两种方式更新：

**方式1：AI 主动询问（主要方式）**
- **触发时机**：迭代完成、重要里程碑
- **询问内容**：模块状态、完成率、备注
- **更新方式**：AI 自动更新 `app_status.json`

**方式2：交互网页支持（辅助方式）**
- **适用场景**：使用交互网页方案
- **操作方式**：用户在网页上直接修改模块状态
- **优势**：用户可以随时更新，无需等待 AI 询问

详细更新流程、示例对话和网页显示说明见 [references/iteration_management.md](references/iteration_management.md)。

### 模块与迭代关系

**同一个概念，不同视角**：

| 维度 | 迭代中的模块 (project_data.json) | 模块成熟度 (app_status.json) |
|------|--------------------------------|----------------------------|
| 文件 | project_data.json | app_status.json |
| 视角 | 规划：这个迭代要做什么 | 状态：现在做到什么程度 |
| 字段 | `expected_completion` | `status`, `completion_rate` |
| 更新时机 | 迭代规划时 | 开发过程中持续更新 |

**关键点**：
- 一个迭代可以涉及多个模块
- 一个模块可以跨越多个迭代
- 通过 `module_id` 关联两个文件中的同一模块

### 重要说明
- **COX 不直接开发**：COX 负责项目管理和可观测，开发工作由其他技能完成
- **COX 是辅助工具**：COX 帮助规划和跟踪，但不编写代码
- **协作模式**：COX + 开发技能（如 cox-coding）协同工作
- **用户可自主选择**：用户可以选择仅使用 COX 进行项目管理，或与开发技能配合使用

### 注意事项
- 每个迭代的目标必须明确且可验证
- 优先实现用户可见的功能，而非内部技术细节
- 每个迭代结束后必须与用户确认
- 下一迭代的计划应基于用户的反馈
- 及时更新 `project_data.json` 反映实际进展
- 每个迭代涉及的模块在规划时确定，不是事后询问
- 模块成熟度通过两种方式更新：AI 主动询问（主要）和交互网页（辅助）
- 模块完成率由智能体根据任务完成情况自动计算，用户可调整

## 任务风险评估与实施决策

### 概述

每个任务除了 `priority`（重要等级）外，还有 `risk_level`（风险等级）。Agent 在规划任务时自动评估风险等级，在实施时根据两个维度判断执行策略。

### 风险评估标准

Agent 根据以下维度自动判断任务风险：

| 判断维度 | high（大风险） | low（小风险） |
|---------|---------------|--------------|
| **修改范围** | 核心模块、多文件修改 | 单文件、局部修改 |
| **影响范围** | 影响多个功能 | 影响单一功能 |
| **修改类型** | 数据结构变更、架构调整 | UI调整、文本修改 |
| **可回滚性** | 难以回滚 | 容易回滚 |

**示例**：
- `high`：修改用户认证流程、重构数据模型、更改 API 接口
- `low`：调整按钮样式、修改错误提示文案、添加日志输出

### 实施决策逻辑

**排序规则**：
1. 首先按 `priority` 排序：critical > high > medium > low
2. 然后按 `risk_level` 分组

**实施策略**：

| 组合 | 策略 | 说明 |
|-----|------|------|
| Critical + Low | 批量处理 | 可以多个任务一起做，批量验证 |
| Critical + High | 单独处理 + 立即验证 | 一个一个做，每个做完立即验证 |
| High + Low | 批量处理 | 可以多个任务一起做，批量验证 |
| High + High | 单独处理 + 立即验证 | 一个一个做，每个做完立即验证 |
| Medium/Low + Low | 批量处理 | 可以多个任务一起做 |
| Medium/Low + High | 单独处理 | 建议单独处理，根据情况决定是否立即验证 |

**核心原则**：
- ✅ 风险小的任务可以一起修改，批量验证，提高效率
- ❌ 不要将大风险和多个小风险混在一起做
- ❌ 做了大风险任务后，不要不及时验证
- ✅ 实施大风险任务后，提醒用户立即验证

详细用户提醒格式、示例工作流和最佳实践见 [references/iteration_management.md](references/iteration_management.md)。

## 用户反馈处理流程

### 概述

当用户在交互式网页上标记模块为 `has_issue` 时，Agent 应记录问题，在下次规划迭代时按优先级处理。

### 优先级指南

| 优先级 | 类型 | 示例 |
|----------|------|----------|
| Critical | 安全问题 | 数据泄露、认证绕过 |
| High | 功能BUG | 核心功能无法使用、崩溃 |
| High | 性能问题 | 响应缓慢、超时 |
| Medium | UI/UX优化 | "不够美观"、不好用 |
| Medium | 小BUG | 错别字、小样式问题 |
| Low | 功能建议 | "如果能加...就好了" |

### 流程概述

```
用户标记 has_issue
    ↓
COX 记录问题（不立即修复）
    ↓
继续当前工作
    ↓
用户说"继续"或"规划下一迭代"
    ↓
COX 对所有问题和任务进行优先级排序
    ↓
基于优先级规划迭代
    ↓
执行并询问用户确认
    ↓
更新模块状态
```

详细工作流程和对话示例见：[Agent 工作流程指南 - 用户反馈处理](references/agent-workflows.md#user-feedback-handling)

## 问题追踪与响应

### 触发条件
当以下情况发生时，智能体应主动触发问题追踪与响应：
1. **复杂问题**：用户反馈涉及多个模块、需要多步骤解决或需要跨团队协作的问题
2. **重复问题**：同一问题在对话中多次出现（2次或更多），且未能顺利解决

### 响应步骤概述
1. 识别问题并确定影响模块
2. 更新项目维度TODO列表
3. 添加问题相关假设分析
4. 建议添加相关埋点
5. 调用skill-manager存储问题信息

详细响应流程和使用示例见 [references/issue_tracking_details.md](references/issue_tracking_details.md)。

### Agent 处理流程
1. 监控对话上下文，识别复杂问题和重复问题
2. 分析问题影响范围，确定相关模块
3. 生成问题ID（格式：ISSUE-NNN）
4. 更新`project_data.json`：添加TODO任务和假设
5. 更新`test_metrics.json`：添加埋点建议
6. 调用skill-manager存储问题追踪信息
7. **COX** 向用户报告已采取的观测更新措施

## 资源索引
- **数据格式规范**：见 [references/data_format.md](references/data_format.md)（所有数据文件的格式定义、验证规则和示例）
- **故障排查指南**：见 [references/troubleshooting.md](references/troubleshooting.md)（常见问题、错误代码和解决方法）
- **部署详细说明**：见 [references/deployment_details.md](references/deployment_details.md)（两种方案的详细配置和使用说明）
- **问题追踪详细流程**：见 [references/issue_tracking_details.md](references/issue_tracking_details.md)（问题追踪与响应的完整流程和示例）
- **部署指南**：见 [references/deployment_guide.md](references/deployment_guide.md)（两种方案的详细部署步骤、配置说明和最佳实践）
- **数据生成工具**：见 [scripts/generate_observability_data.py](scripts/generate_observability_data.py)（生成符合规范的可观测数据，避免大模型幻觉）
- **数据采集工具**：见 [scripts/collect_data.py](scripts/collect_data.py)（数据格式验证和采集工具）
- **Web界面服务器**：见 [scripts/run_web_observability.py](scripts/run_web_observability.py)（静态/Web 两种模式的界面生成）
- **Skill-manager存储工具**：见 [scripts/store_to_skill_manager.py](scripts/store_to_skill_manager.py)（存储部署信息和问题追踪信息到skill-manager）
- **Web界面模板**：见 [assets/web_templates/](assets/web_templates/)（HTML模板和样式文件）
- **Docker配置**：见 [assets/docker_compose/](assets/docker_compose/)（全面方案的完整配置）

## 注意事项
- 两种方案使用相同的数据格式，可根据需求随时切换
- 数据文件支持增量更新，无需每次重写全部内容
- 生成数据时建议使用脚本而非大模型生成，避免格式错误
- 交互方案的Web界面默认在5000端口，可通过参数修改
- 全面方案需要Docker环境，建议先使用静态方案验证需求

## 最佳实践
- **数据初始化**：使用 `generate_observability_data.py` 脚本生成初始数据文件，确保格式 100% 正确
- **数据更新**：建议每日或每次迭代结束后更新可观测数据
- **数据复用**：数据文件可被多个技能和工具共享，避免重复创建
- **方案选择**：日常开发使用交互方案（需安装Flask），受限环境（如沙盒）使用静态方案
- **假设管理**：在project_data.json中记录开发假设，定期验证和更新
- **模块状态跟踪**：使用应用维度监控功能模块状态，识别开发瓶颈
- **异常优先**：在测试维度优先处理高频异常，提升质量
- **问题响应**：利用问题追踪功能，及时更新观测数据，加速问题解决
- **数据验证**：生成可观测界面前，使用检查脚本验证数据一致性：
  ```bash
  # 检查模块一致性
  python scripts/check_module_consistency.py
  
  # 验证 JSON 格式
  python -m json.tool project_data.json > /dev/null
  python -m json.tool app_status.json > /dev/null
  python -m json.tool test_metrics.json > /dev/null
  ```
- **故障排查**：遇到问题时，查看 [references/troubleshooting.md](references/troubleshooting.md)
