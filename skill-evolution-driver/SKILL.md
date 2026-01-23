---
name: skill-evolution-driver
description: 帮助团队持续改进技能，自动发现技能优化机会（如缺少必要信息、格式问题、需要更新版本等），执行安全更新流程（备份、修改、测试、还原），确保技能质量随项目推进不断提升
dependency:
  python: []
  system: []
---

# 技能进化驱动师

## 任务目标
- 本 Skill 用于：驱动技能进行自我进化，随着项目过程推进持续优化
- 能力包含：
  1. 监控skill-manager存储的数据，识别技能优化机会
  2. 在空闲时提醒用户潜在的优化建议
  3. 维护技能优化任务清单
  4. 执行技能更新流程（备份、更新、测试、还原）
  5. 管理技能版本号
- 触发条件：以下任一情况触发
  - **用户直接需求**："优化技能"、"改进技能"、"技能需要更新"、"技能升级"、"修复技能问题"
  - **自动监控触发**：监控到skill-manager存储的技能数据中有待优化的任务（如：status=pending的优化任务、日志中的错误和警告、缺失的必要字段）
  - **版本相关**："技能版本号需要更新"、"需要记录技能变更"
  - **质量相关**："技能格式不正确"、"需要检查技能质量"、"技能测试不通过"

## 优化识别

### 数据来源
从skill-manager存储的技能数据中分析优化机会：

1. **缺失信息**：技能配置中缺乏必要字段（如version）
2. **格式问题**：数据格式不符合规范
3. **重复信息**：存在冗余或重复的内容
4. **使用模式**：根据访问频率和方式识别改进点
5. **错误日志**：从日志中识别常见错误或警告
6. **跨技能协作问题**：从其他技能的日志中识别对当前技能的依赖问题或改进建议

### 优化类型
- **format_improvement**：格式改进
- **content_optimization**：内容优化
- **version_update**：版本号更新
- **bug_fix**：Bug修复
- **feature_enhancement**：功能增强

## 进化流程

### 步骤1：提醒用户

#### 自动监控触发
智能体定期检查 skill-manager 存储的数据，识别优化机会：

**检查工具**：调用 `scripts/check_optimization_opportunities.py`
```bash
# 检查所有技能
python scripts/check_optimization_opportunities.py

# 检查特定技能
python scripts/check_optimization_opportunities.py --skill-name dev-observability
```

**检查内容**：
1. **待处理任务**：检查 skill-evolution-driver 自身存储的优化任务（status=pending）
2. **缺失字段**：检查技能配置是否缺少必要字段（如 version、deploy_mode、manual_path）
3. **错误日志**：检查技能日志中的 ERROR/WARNING/CRITICAL 日志
4. **目录问题**：检查技能目录结构是否符合规范

**提醒格式**：
```
检测到潜在优化机会：
- 技能：skill-name
- 优化类型：format_improvement
- 描述：SKILL.md缺少version字段
- 是否开始优化？（y/n）
```

#### 用户主动触发
当用户表达以下需求时，直接提醒用户：
- "优化技能"、"改进技能"
- "技能需要更新"、"技能升级"
- "修复技能问题"
- "技能版本号需要更新"
- "技能格式不正确"、"需要检查技能质量"

### 步骤2：维护任务清单
若用户同意，调用skill-manager存储优化任务：

```json
{
  "task_id": "OPT-001",
  "skill_name": "skill-name",
  "optimization_type": "format_improvement",
  "description": "SKILL.md缺少version字段",
  "status": "pending",
  "feasibility": "pending",
  "backup_path": "",
  "old_version": "",
  "new_version": "",
  "test_result": "",
  "notes": "",
  "created_at": "2024-01-22 12:00:00",
  "updated_at": "2024-01-22 12:00:00"
}
```

存储方式：更新 skill-evolution-driver 在 skill-manager 中的配置
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")
existing_config = storage.get_config("skill-evolution-driver") or {}
existing_config["optimization_tasks"] = [task_dict]  # 任务列表
storage.save_config("skill-evolution-driver", existing_config)
```

### 步骤3：分析可行性
分析该技能的优化可行性：

**可行性评估标准**：
- 技能目录结构完整
- SKILL.md格式正确
- 脚本语法正确
- 依赖关系清晰
- 优化内容明确

**不可行情况**：
- 技能目录不存在或损坏
- SKILL.md格式错误，无法解析
- 优化内容不明确或过于复杂
- 优化可能破坏现有功能

更新任务状态：
- 可行：`feasibility: "feasible"`
- 不可行：`feasibility: "not_feasible"`，并在`notes`中说明原因

### 步骤4：备份技能
调用 `scripts/backup_skill.py` 备份技能：

```bash
python scripts/backup_skill.py --skill-dir /workspace/projects/skill-name
```

备份文件格式：`skill-name.backup.<timestamp>.skill`

更新任务：
- `backup_path: "/workspace/projects/skill-name.backup.<timestamp>.skill"`

### 步骤5：更新技能
执行具体的优化操作，并更新版本号：

1. **执行优化**：根据优化类型修改技能内容
2. **更新版本号**：调用 `scripts/update_version.py`

```bash
python scripts/update_version.py --skill-dir /workspace/projects/skill-name --type patch
```

版本号类型：
- `patch`：修订版本（v1.0.0 -> v1.0.1）
- `minor`：次版本（v1.0.0 -> v1.1.0）
- `major`：主版本（v1.0.0 -> v2.0.0）

更新任务：
- `old_version: "v1.0.0"`
- `new_version: "v1.0.1"`

### 步骤6：进行测试
对更新后的技能进行测试验证：

**测试内容**：
1. SKILL.md格式验证（YAML前言区）
2. 脚本语法检查（Python语法）
3. 目录结构验证（符合固定结构）
4. 依赖完整性检查（dependency字段）

测试脚本：
```bash
python scripts/backup_skill.py --validate-only --skill-dir /workspace/projects/skill-name
```

### 步骤7：处理测试结果

**测试不通过**：
1. 调用 `scripts/restore_skill.py` 还原技能
2. 使用 `manage_optimization_tasks.py` 更新任务状态

```bash
# 还原技能
python scripts/restore_skill.py --backup-file <备份路径> --skill-dir /workspace/projects/skill-name

# 更新任务状态
python scripts/manage_optimization_tasks.py update \
  --task-id OPT-001 \
  --status failed \
  --test-result failed \
  --notes "测试失败：SKILL.md格式错误"
```

**测试通过**：
1. 使用 `manage_optimization_tasks.py` 更新任务状态
2. 打包新的.skill文件
3. 告知用户更新内容
4. 提醒用户重新加载技能

```bash
# 更新任务状态
python scripts/manage_optimization_tasks.py update \
  --task-id OPT-001 \
  --status completed \
  --test-result passed \
  --notes "优化成功：已添加version字段" \
  --new-version v1.0.1 \
  --backup-path /workspace/projects/skill-name.backup.20260122120000.skill
```

**重要**：必须更新任务状态为 `completed`，避免下次检查时重复提醒相同的优化机会。

### 步骤8：通知用户
根据测试结果通知用户：

**测试通过**：
```
✓ 技能优化成功
- 技能：skill-name
- 版本：v1.0.0 -> v1.0.1
- 更新内容：添加version字段
- 备份：skill-name.backup.<timestamp>.skill

请重新加载AI交互界面以使用更新后的技能。
```

**测试不通过**：
```
✗ 技能优化失败
- 技能：skill-name
- 原因：测试失败
- 详情：SKILL.md格式错误
- 技能已还原
```

## 核心功能说明

### 智能体可处理的功能
- 监控skill-manager数据，识别优化机会
- 在空闲时提醒用户优化建议
- 维护技能优化任务清单
- 分析优化可行性
- 执行优化操作
- 进行测试验证
- 处理测试结果
- 通知用户

### 脚本实现的功能
- **检查优化机会**：`scripts/check_optimization_opportunities.py` 扫描skill-manager数据，自动识别优化机会（过滤已完成的任务）
- **管理优化任务**：`scripts/manage_optimization_tasks.py` 提供优化任务的增删改查功能（add/update/list）
- **备份技能**：`scripts/backup_skill.py` 备份整个skill目录
- **还原技能**：`scripts/restore_skill.py` 从备份还原技能
- **更新版本号**：`scripts/update_version.py` 增加SKILL.md中的version字段
- **测试验证**：`scripts/backup_skill.py --validate-only` 验证技能格式

## 资源索引
- **优化机会检查工具**：见 [scripts/check_optimization_opportunities.py](scripts/check_optimization_opportunities.py)（自动扫描skill-manager数据，识别优化机会，过滤已完成的任务）
- **优化任务管理工具**：见 [scripts/manage_optimization_tasks.py](scripts/manage_optimization_tasks.py)（优化任务的增删改查）
- **备份工具**：见 [scripts/backup_skill.py](scripts/backup_skill.py)（备份技能目录）
- **还原工具**：见 [scripts/restore_skill.py](scripts/restore_skill.py)（从备份还原技能）
- **版本管理**：见 [scripts/update_version.py](scripts/update_version.py)（更新版本号）
- **优化指南**：见 [references/optimization_guide.md](references/optimization_guide.md)（优化类型、测试标准、最佳实践）

## 注意事项
- 优化前必须备份技能
- 优化过程中保持task状态同步更新
- 测试不通过必须还原技能
- 版本号遵循语义化版本规范
- 重大变更需用户明确确认
- 优化完成后必须更新任务状态为 `completed`，避免重复提醒
- 优化后需提醒用户重新加载技能

## 最佳实践
- 定期监控skill-manager数据，识别优化机会
- 优先处理高价值、低风险的优化
- 优化前充分分析可行性
- 保持详细的优化日志
- 定期清理过期的备份文件
- 向用户提供清晰的优化说明

## 使用示例

### 示例1：添加version字段
检测到skill-name的SKILL.md缺少version字段。

1. 提醒用户
2. 用户同意后，创建优化任务
3. 分析可行性：可行
4. 备份技能：skill-name.backup.20240122120000.skill
5. 更新SKILL.md，添加version: v1.0.0
6. 测试验证：通过
7. 更新任务状态：completed
8. 通知用户：优化成功

### 示例2：格式改进
检测到skill-name的SKILL.md格式不符合规范。

1. 提醒用户
2. 用户同意后，创建优化任务
3. 分析可行性：可行
4. 备份技能
5. 修正SKILL.md格式
6. 测试验证：通过
7. 更新任务状态：completed
8. 通知用户：优化成功

### 示例3：不可行的优化
检测到skill-name的优化内容过于复杂。

1. 提醒用户
2. 用户同意后，创建优化任务
3. 分析可行性：不可行
4. 更新任务状态：failed
5. 更新备注：优化内容过于复杂，需要人工介入
6. 通知用户：优化不可行，需人工处理
