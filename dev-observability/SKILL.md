---
name: dev-observability
version: v1.0.0
description: 帮助开发团队掌握项目进展、识别开发风险、了解系统健康状态。提供项目进度跟踪、任务状态管理、开发假设记录、应用模块监控、测试埋点和异常分析等功能。支持简单日志和Web界面两种方案，适合不同规模团队
dependency:
  python:
    - flask>=2.0.0
  system: []
---

# 开发阶段可观测底座

## 任务目标
- 本 Skill 用于：帮助团队了解项目整体状况、及时发现问题和风险、提高开发效率
- 能力包含：
  1. 项目维度：跟踪迭代进度、任务状态、开发假设
  2. 应用维度：监控应用功能模块状态
  3. 测试维度：管理测试埋点、分析异常情况
- 触发条件：以下任一情况触发
  - **用户提出**: "透明化"、"确定性协作"、"观察项目情况"、"启用观察"、"了解系统健康状态"、"构建项目监控"、"问题预防"、"效率提升"、"能力积累"
  - **项目进展类**："想知道项目进展如何"、"有没有延期风险"、"迭代完成度是多少"
  - **问题追踪类**："经常出bug怎么跟踪"、"重复问题怎么处理"、"需要记录待解决的问题"
  - **质量保障类**："需要监控接口性能"、"怎么发现系统异常"、"测试覆盖率怎么样"
  - **团队协作类**："需要共享项目信息"、"让团队成员了解现状"、"需要可视化仪表板"

## 部署方案选择

在开始使用前，请根据团队需求选择部署方案。详细配置说明见 [references/deployment_details.md](references/deployment_details.md)。

### 简单方案（推荐初学者）
- 特点：仅生成结构化日志，无界面
- 适用场景：个人开发、快速验证需求
- 使用方式：调用 `scripts/generate_observability_log.py`

### 中等方案（推荐小团队）
- 特点：提供本地Web界面展示可观测数据
- 适用场景：5-10人团队开发、需要可视化界面
- 使用方式：调用 `scripts/run_web_observability.py`，访问 http://localhost:5000

### 全面方案（暂不提供）
- 特点：使用Prometheus+Grafana专业可观测工具，Docker部署
- 适用场景：准备迁移到生产环境、需要专业监控能力
- 状态：暂不开放，待完善数据对接和配置方案后上线

## 快速开始

### 步骤1：准备可观测数据

**首次使用**：按照 [references/data_format.md](references/data_format.md) 中定义的数据格式，准备以下JSON文件：
- `project_data.json`：项目迭代和任务数据
- `app_status.json`：应用模块状态数据
- `test_metrics.json`：测试埋点和异常数据

**后续使用**：如果上述文件已存在，系统会自动读取现有内容，您可以直接更新或查看数据，无需重新准备。

**智能体辅助**：智能体可以协助您：
- 根据项目文档自动生成初始数据文件
- 验证现有数据格式是否正确
- 根据开发进度更新数据内容

### 步骤2：选择方案并启动

**简单方案**：
```bash
python scripts/generate_observability_log.py --project project_data.json --app app_status.json --test test_metrics.json
```

**中等方案**：
```bash
python scripts/run_web_observability.py --project project_data.json --app app_status.json --test test_metrics.json
# 访问 http://localhost:5000 查看界面
```

**说明**：上述脚本会自动读取数据文件的内容，如果文件已存在，则使用现有数据。

### 步骤3：调用skill-manager存储部署信息
部署完成后，调用 **skill-manager** 技能存储部署信息，便于后续管理和技能协作。

详细调用方式见 [references/deployment_details.md](references/deployment_details.md)。

### 步骤4：持续更新数据
在开发过程中，定期更新数据文件，系统会自动读取并刷新显示。智能体可以协助您：
- 分析现有数据，识别需要更新的内容
- 根据开发进度自动更新数据
- 验证更新后的数据格式

## 核心功能说明

### 智能体可处理的功能
- **数据管理**：检查数据文件是否存在，如果存在则读取现有内容
- **数据格式咨询**：根据项目情况推荐合适的数据结构
- **数据内容生成**：根据项目文档自动生成初始数据文件
- **数据内容更新**：根据开发进度更新现有数据文件
- **数据分析**：分析现有可观测数据，识别项目风险和瓶颈
- **使用指导**：解答三种方案的选择和部署问题
- **问题追踪与响应**：识别复杂问题和重复问题，自动更新观测数据（TODO任务、假设分析、埋点建议）

### 脚本实现的功能
- **数据格式验证**：`scripts/collect_data.py` 验证JSON数据格式是否符合规范
- **简单方案日志生成**：`scripts/generate_observability_log.py` 生成结构化可观测日志
- **中等方案Web服务**：`scripts/run_web_observability.py` 启动Flask Web界面
- **Skill-manager存储工具**：`scripts/store_to_skill_manager.py` 存储部署信息和问题追踪信息

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

### 智能体处理流程
1. 监控对话上下文，识别复杂问题和重复问题
2. 分析问题影响范围，确定相关模块
3. 生成问题ID（格式：ISSUE-NNN）
4. 更新`project_data.json`：添加TODO任务和假设
5. 更新`test_metrics.json`：添加埋点建议
6. 调用skill-manager存储问题追踪信息
7. 向用户报告已采取的观测更新措施

## 资源索引
- **数据格式规范**：见 [references/data_format.md](references/data_format.md)（所有数据文件的格式定义、验证规则和示例）
- **部署详细说明**：见 [references/deployment_details.md](references/deployment_details.md)（三种方案的详细配置和使用说明）
- **问题追踪详细流程**：见 [references/issue_tracking_details.md](references/issue_tracking_details.md)（问题追踪与响应的完整流程和示例）
- **部署指南**：见 [references/deployment_guide.md](references/deployment_guide.md)（三种方案的详细部署步骤、配置说明和最佳实践）
- **数据采集工具**：见 [scripts/collect_data.py](scripts/collect_data.py)（数据格式验证和采集工具）
- **日志生成工具**：见 [scripts/generate_observability_log.py](scripts/generate_observability_log.py)（简单方案的日志生成）
- **Web界面服务器**：见 [scripts/run_web_observability.py](scripts/run_web_observability.py)（中等方案的Web服务）
- **Skill-manager存储工具**：见 [scripts/store_to_skill_manager.py](scripts/store_to_skill_manager.py)（存储部署信息和问题追踪信息到skill-manager）
- **Web界面模板**：见 [assets/web_templates/](assets/web_templates/)（HTML模板和样式文件）
- **Docker配置**：见 [assets/docker_compose/](assets/docker_compose/)（全面方案的完整配置）

## 注意事项
- 三种方案使用相同的数据格式，可根据需求随时升级或降级
- 数据文件支持增量更新，无需每次重写全部内容
- 中等方案的Web界面默认在5000端口，可通过参数修改
- 全面方案需要Docker环境，建议先使用中等方案验证需求
- 智能体会自动检查数据文件是否存在，如果存在则读取现有内容
- 智能体可以协助生成初始数据文件、更新现有数据，但持续维护需要团队配合
- 问题追踪功能由智能体自动触发，无需手动操作

## 最佳实践
- **数据初始化**：首次使用时让智能体生成初始数据文件
- **数据更新**：建议每日或每次迭代结束后更新可观测数据
- **数据复用**：数据文件可被多个技能和工具共享，避免重复创建
- **结合CI/CD**：将数据采集集成到CI/CD流程中，实现自动化
- **假设管理**：在project_data.json中记录开发假设，定期验证和更新
- **模块状态跟踪**：使用应用维度监控功能模块状态，识别开发瓶颈
- **异常优先**：在测试维度优先处理高频异常，提升质量
- **问题响应**：利用问题追踪功能，及时更新观测数据，加速问题解决
