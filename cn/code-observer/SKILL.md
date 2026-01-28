---
name: code-observer
description: 代码调试智能助手，帮助你看到代码是怎么运行的。当你说"我想看看这个函数为什么会这么慢"、"代码运行到一半就报错了，不知道哪里出问题"、"这个业务逻辑太复杂了，我理不清楚执行顺序"时，我会帮你追踪代码执行路径，找出慢的地方，定位错误原因。在发现技能优化点时，会询问是否调用skill-evolution-driver进行优化
dependency: {}
---

# 代码调试智能助手

## 任务目标
- 本 Skill 用于：帮你更好地理解代码是怎么运行的，比传统断点调试更简单直观
- 能力包含：
  - 告诉你代码的执行顺序，哪些函数被调用了
  - 找出代码运行慢的地方（哪些函数耗时多）
  - 帮你定位报错原因（哪里抛出了异常，异常是怎么传播的）
  - 给出具体的代码修改建议
- 触发条件：当你说"观察代码运行情况"、"代码质量"、"优化代码"、"代码跑得慢"、"不知道哪里出错了"、"这个逻辑太复杂理不清楚"、"想看看代码是怎么执行的"等类似表达时

## 操作步骤

### 1. 环境准备与数据获取

**步骤 1.1：调试环境确认**
- 智能体询问开发者调试环境状态
- 如果调试环境终端未打开，提供开启指导：
  - 打开应用终端的命令或操作步骤
  - 启动调试工具（可能叫dev-observability或类似名称）的具体配置
- 等待开发者确认调试环境已就绪

**步骤 1.2：查询数据存储位置**
- 在获取日志或指标信息前，必须先调用 `skill-manager` 技能查询调试工具（如dev-observability）的数据存储位置信息
- 查询内容：
  - 日志文件（observability.log）的存储路径
  - 指标数据（metrics.prom）的存储路径（如果有）
  - 应用状态数据（app_status.json）的存储路径（如果有）
  - 项目数据（project_data.json）的存储路径（如果有）
  - 测试数据（test_metrics.json）的存储路径（如果有）
- 根据查询结果获取实际的文件路径

**步骤 1.3：获取观测数据**
- 智能体根据查询到的存储路径，读取以下数据文件：
  - 日志文件（从查询到的路径）
  - 指标数据（可选，从查询到的路径）
  - 应用状态数据（可选，从查询到的路径）
  - 项目数据（可选，从查询到的路径）
  - 测试数据（可选，从查询到的路径）

### 2. 数据解析与分析

**步骤 2.1：解析日志数据**
调用 `scripts/parse_logs.py` 处理（使用从skill-manager查询到的实际路径）：
```bash
python3 scripts/parse_logs.py --log-file <从skill-manager查询到的日志路径> --output ./parsed_logs.json
```
- 提取执行路径信息
- 识别函数调用与耗时
- 定位异常抛出位置

**步骤 2.2：解析指标数据**（如果有）
调用 `scripts/parse_prometheus.py` 处理（使用从skill-manager查询到的实际路径）：
```bash
python3 scripts/parse_prometheus.py --prom-file <从skill-manager查询到的metrics路径> --output ./parsed_metrics.json
```

**步骤 2.3：分析多维数据**（如果有）
调用对应的分析脚本（使用从skill-manager查询到的实际路径）：
```bash
python3 scripts/analyze_app_status.py --input <从skill-manager查询到的app_status路径> --output ./app_analysis.json
python3 scripts/analyze_project_data.py --input <从skill-manager查询到的project_data路径> --output ./project_analysis.json
python3 scripts/analyze_test_metrics.py --input <从skill-manager查询到的test_metrics路径> --output ./test_analysis.json
```

### 3. 全流程追踪报告生成

**步骤 3.1：生成追踪报告**
调用 `scripts/generate_trace_report.py` 生成全流程可视化追踪：
```bash
python3 scripts/generate_trace_report.py \
  --logs ./parsed_logs.json \
  --metrics ./parsed_metrics.json \
  --app-status ./app_analysis.json \
  --project-data ./project_analysis.json \
  --test-metrics ./test_analysis.json \
  --output ./trace_report.md
```

**步骤 3.2：报告内容结构**
- 执行路径可视化：函数调用链与时间轴
- 性能指标分析：耗时分布、瓶颈识别
- 异常追踪：异常堆栈、触发路径、根因分析
- 跨维度关联：项目/应用/测试状态关联分析

### 4. 问题诊断与解决方案生成

**步骤 4.1：智能体分析追踪报告**
- 识别性能瓶颈：高耗时函数、频繁调用的热点路径
- 定位异常根因：异常传播路径、前置条件分析
- 评估代码质量：复杂度、重复代码、潜在风险

**步骤 4.2：生成解决方案**
- 针对性能问题：优化建议、缓存策略、并发处理方案
- 针对异常问题：异常处理增强、边界条件检查、防御性编程
- 针对架构问题：模块解耦、依赖优化、设计模式应用

**步骤 4.3：代码修复建议**
- 提供具体的代码修改示例
- 说明修改理由与预期效果
- 给出测试验证建议

### 5. 运行日志记录

**步骤 5.1：数据完整性检查**
- 检查本技能所需的数据是否都能从调试工具（如dev-observability）获取：
  - 日志文件：是否存在且可读取
  - 指标数据：是否存在（可选）
  - 应用状态数据：是否存在（可选）
  - 项目数据：是否存在（可选）
  - 测试数据：是否存在（可选）
- 评估数据质量问题：
  - 日志是否包含必要的信息（时间、级别、消息等）
  - 指标数据格式是否正确
  - JSON数据结构是否完整且有效

**步骤 5.2：问题识别与记录（强制执行）**
- 本技能依赖其他技能（如dev-observability）的输出文件进行代码分析
- **当发现以下情况时，必须调用 `skill-manager` 技能记录问题**：
  - **依赖文件不存在**：如dev-observability的observability.log文件不存在
  - **依赖文件不可读取**：文件存在但无法读取（权限问题、文件损坏等）
  - **依赖文件格式不符合要求**：文件存在但格式不符合本技能的解析要求
  - **依赖文件内容不完整**：文件存在但缺少必需字段或数据
  - **依赖文件质量不满足需要**：文件内容质量不足以支持有效的代码分析
  - **数据读取失败**：尝试读取依赖文件时发生异常或错误
  - **数据解析失败**：文件读取成功但解析时出现错误
  - **其他任何影响本技能正常执行的依赖问题**

- **问题记录的重要性**：
  - 本技能的执行依赖于其他技能的输出结果
  - 如果依赖文件不存在或不满足需要，本技能无法正常执行分析
  - 记录这些问题可以帮助改进依赖技能的数据输出
  - 为技能协作提供问题追踪和优化依据

**步骤 5.3：问题记录格式（强制执行）**
调用 `skill-manager` 时，必须严格按照以下JSON格式记录问题：

```json
{
  "level": "critical / high / medium / low",
  "message": "【问题现象】 【问题原因】 【问题影响】"
}
```

**格式说明**：
- `level`（必需）：问题严重程度
  - `critical`：严重问题，完全阻塞技能执行（如关键依赖文件缺失）
  - `high`：高优先级问题，严重影响技能功能（如主要依赖文件格式错误）
  - `medium`：中等优先级问题，部分功能受影响（如可选依赖文件缺失）
  - `low`：低优先级问题，轻微影响（如部分数据不完整）

- `message`（必需）：问题描述，必须包含三个部分
  - 【问题现象】：具体描述发生了什么问题
  - 【问题原因】：分析问题产生的原因
  - 【问题影响】：说明问题对本技能执行的影响

**格式示例**：

```json
{
  "level": "critical",
  "message": "【没有 observability.log 文件】【dev-observability技能的中等方案（Web界面）不生成日志文件】【无法进行执行路径追踪，本技能无法正常工作】"
}
```

```json
{
  "level": "medium",
  "message": "【metrics.prom 文件格式不正确】【缺少必要的 TYPE 注释行】【无法解析Prometheus指标，性能分析功能受限】"
}
```

```json
{
  "level": "high",
  "message": "【observability.log 文件缺少 timestamp 字段】【日志输出配置不完整】【无法按时间顺序追踪代码执行路径，追踪报告不完整】"
}
```

**步骤 5.4：价值主张**
- 记录依赖技能（如dev-observability）的数据输出问题
- 帮助改进依赖技能的数据质量和输出格式
- 为技能协作提供问题追踪和持续优化机制
- 确保本技能能够正常执行代码分析任务

**步骤 5.5：技能优化点识别与建议（智能体处理）**

智能体在分析发现的问题时，需要判断是否涉及技能的优化点：

**判断标准**：
1. **技能配置问题**：问题涉及技能的配置信息（如 SKILL.md 缺少必要字段、version 字段缺失等）
2. **脚本问题**：问题涉及技能的脚本输出（如日志格式不正确、数据字段缺失等）
3. **文档问题**：问题涉及技能的说明文档（如描述不清、步骤不完整等）
4. **集成问题**：问题涉及技能间的协作（如接口不兼容、数据格式不一致等）

**优化点识别示例**：

**示例1：日志格式问题 → 技能优化点**
- 问题描述：`observability.log 文件缺少 timestamp 字段`
- 优化点判断：涉及 dev-observability 技能的日志输出格式
- 优化类型：脚本输出优化
- 建议行动：调用 skill-evolution-driver 技能

**示例2：配置缺失问题 → 技能优化点**
- 问题描述：`dev-observability 的 SKILL.md 缺少 version 字段`
- 优化点判断：涉及技能配置信息
- 优化类型：格式改进
- 建议行动：调用 skill-evolution-driver 技能

**示例3：数据质量问题 → 非技能优化点**
- 问题描述：`测试覆盖率数据不完整`
- 优化点判断：属于用户数据问题，不涉及技能本身
- 优化类型：数据完善
- 建议行动：提醒用户补充数据

**智能体响应流程**：

1. **分析发现的问题列表**
   - 遍历步骤 5.2 记录的所有问题
   - 判断每个问题是否涉及技能优化点

2. **识别技能优化点**
   - 如果问题涉及技能配置、脚本输出、文档或协作
   - 标记为技能优化点
   - 记录涉及的技能名称和优化类型

3. **询问用户**
   如果存在技能优化点，智能体应向用户询问：

   ```
   在本次代码分析中，发现以下技能优化点：

   1. 技能：dev-observability
      - 优化类型：脚本输出优化
      - 问题：observability.log 文件缺少 timestamp 字段
      - 影响：无法按时间顺序追踪代码执行路径

   是否需要调用 skill-evolution-driver 技能来处理这些优化点？（y/n）
   ```

4. **处理用户选择**

   **选择 y（是）**：
   - 调用 skill-evolution-driver 技能
   - 传递优化点列表（技能名称、优化类型、问题描述）
   - 等待 skill-evolution-driver 执行优化

   **选择 n（否）**：
   - 跳过优化点处理
   - 继续执行后续步骤（如生成追踪报告）
   - 建议用户后续可以手动调用 skill-evolution-driver

**注意事项**：
- 优化点识别是智能体的分析判断，不是简单的关键词匹配
- 需要结合问题上下文和技能知识进行判断
- 如果不确定是否为技能优化点，可以咨询用户
- 优化点识别不影响本技能的核心功能（代码分析）

## 资源索引

### 必要脚本
- `scripts/parse_logs.py`：解析结构化日志，提取执行路径、函数调用与异常信息
- `scripts/parse_prometheus.py`：解析Prometheus指标数据，提取性能指标
- `scripts/analyze_app_status.py`：分析应用模块状态与完成率
- `scripts/analyze_project_data.py`：分析项目迭代进度与任务状态
- `scripts/analyze_test_metrics.py`：分析测试埋点与异常情况
- `scripts/generate_trace_report.py`：整合多维数据，生成全流程可视化追踪报告

### 领域参考
- `references/log_format.md`：日志格式规范与解析规则（读取时机：解析日志前）
- `references/prometheus_format.md`：Prometheus指标格式规范（读取时机：解析指标前）
- `references/json_data_format.md`：JSON数据格式规范（读取时机：分析JSON数据前）
- `references/trace_analysis_guide.md`：追踪分析指南与方法论（读取时机：生成报告前）

### 输出资产
- `assets/trace_templates/execution_trace.md`：执行追踪报告模板
- `assets/trace_templates/performance_metrics.md`：性能指标报告模板
- `assets/trace_templates/error_analysis.md`：异常分析报告模板

## 注意事项

- **重要**：在获取日志或指标信息前，必须先调用 `skill-manager` 技能查询调试工具（如dev-observability）的数据存储位置信息
- **非常重要（强制执行）**：在执行过程中，如果发现依赖的输出文件不存在或不符合要求，必须按照步骤5.3的格式调用 `skill-manager` 技能记录问题
- **强制执行规则**：当依赖文件缺失、不可读、格式错误、内容不完整或质量不满足需要时，必须记录问题，不得跳过
- 仅在需要时读取参考文档，保持上下文简洁
- 技术性数据处理优先调用脚本（日志解析、指标提取、报告生成）
- 问题分析与解决方案生成由智能体完成，充分利用其推理能力
- 追踪报告采用Markdown格式，便于可视化展示与版本控制
- 支持渐进式分析：可仅使用日志数据，也可融合多维数据提升分析深度
- 所有数据文件的路径都必须从 `skill-manager` 查询调试工具获得
- 问题记录必须严格按照步骤5.3的JSON格式，包含level和message字段

## 使用示例

### 示例 1：基础代码追踪
**用户场景**："我想看看这个函数是怎么执行的，为什么这么慢"
**执行方式**：调用skill-manager查询 + 脚本 + 智能体分析 + 运行日志记录
**关键步骤**：
```bash
# 1. 调用skill-manager查询调试工具的日志存储路径
# （通过智能体调用skill-manager完成）

# 2. 解析日志（使用查询到的实际路径）
python3 scripts/parse_logs.py --log-file <查询到的日志路径> --output ./parsed_logs.json

# 3. 生成追踪报告
python3 scripts/generate_trace_report.py --logs ./parsed_logs.json --output ./trace_report.md

# 4. 智能体分析报告并生成解决方案

# 5. 数据完整性检查与问题记录
# 如果发现问题，必须按照步骤5.3的格式调用skill-manager记录问题
```

### 示例 2：全面代码分析
**用户场景**："帮我全面分析一下代码的运行情况，看看有没有性能问题或错误"
**执行方式**：调用skill-manager查询 + 全脚本 + 智能体深度分析 + 运行日志记录
**关键步骤**：
```bash
# 1. 调用skill-manager查询调试工具的所有数据文件存储路径
# （通过智能体调用skill-manager完成）

# 2. 解析所有数据源（使用查询到的实际路径）
python3 scripts/parse_logs.py --log-file <查询到的日志路径> --output ./parsed_logs.json
python3 scripts/parse_prometheus.py --prom-file <查询到的metrics路径> --output ./parsed_metrics.json
python3 scripts/analyze_app_status.py --input <查询到的app_status路径> --output ./app_analysis.json
python3 scripts/analyze_project_data.py --input <查询到的project_data路径> --output ./project_analysis.json
python3 scripts/analyze_test_metrics.py --input <查询到的test_metrics路径> --output ./test_analysis.json

# 3. 生成全面分析报告
python3 scripts/generate_trace_report.py \
  --logs ./parsed_logs.json \
  --metrics ./parsed_metrics.json \
  --app-status ./app_analysis.json \
  --project-data ./project_analysis.json \
  --test-metrics ./test_analysis.json \
  --output ./trace_report.md

# 4. 智能体进行跨维度关联分析，生成综合解决方案

# 5. 数据完整性检查与问题记录
# 检查所有数据是否完整，如有缺失或格式问题，必须按照步骤5.3的格式调用skill-manager记录
```

### 示例 3：性能问题排查
**用户场景**："代码运行太慢了，帮我找出哪里慢"
**执行方式**：调用skill-manager查询 + 脚本提取指标 + 智能体分析瓶颈 + 运行日志记录
**关键要点**：
- 调用skill-manager查询调试工具的日志和metrics存储路径
- 解析日志提取函数调用耗时（使用查询到的实际路径）
- 分析指标数据识别高耗时操作（使用查询到的实际路径）
- 智能体生成性能优化建议（缓存、并发、算法优化）
- 检查数据完整性，如果数据缺失或格式错误，调用skill-manager记录问题

### 示例 4：错误定位
**用户场景**："代码运行到一半就报错了，不知道哪里出问题"
**执行方式**：智能体分析 + skill-manager记录（强制）
**关键要点**：
- 检查到日志文件缺失
- **必须**按照步骤5.3的格式调用 `skill-manager` 记录问题：

```json
{
  "level": "critical",
  "message": "【没有 observability.log 文件】【dev-observability技能的中等方案（Web界面）不生成日志文件】【无法进行执行路径追踪，本技能无法正常工作】"
}
```

**问题记录说明**：
- `level`: "critical" - 因为日志文件是本技能的关键依赖，缺失会完全阻塞技能执行
- `message`: 包含【问题现象】【问题原因】【问题影响】三个部分，符合步骤5.3的格式要求
