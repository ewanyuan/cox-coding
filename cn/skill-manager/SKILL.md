---
name: skill-manager
description: 为其他技能提供统一的配置和日志存储服务，支持技能间数据共享和协作
dependency: {}
---

# 技能管理者

## 任务目标
- 本 Skill 用于：为其他技能提供统一的配置和日志存储能力
- 能力包含：
  1. 存储技能配置信息
  2. 存储技能运行日志
  3. 按技能名查询配置和日志
  4. 管理所有技能的存储数据
- 触发条件：被其他技能主动引用，需要存储或读取数据时

## 使用场景

### 场景1：技能存储自己的配置
当技能需要持久化配置信息时，调用技能管理者存储：

```python
from skill_manager import SkillStorage

# 创建存储实例
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# 存储配置
config = {
    "deploy_mode": "simple",
    "output_path": "/path/to/output.log",
    "timestamp": "2024-01-22 12:00:00"
}
storage.save_config("my-skill", config)
```

### 场景2：技能存储运行日志
当技能需要记录运行日志时，调用技能管理者存储：

```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

logs = [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "开始执行"},
    {"time": "2024-01-22 12:05:00", "level": "INFO", "message": "执行完成"}
]
storage.save_logs("my-skill", logs)
```

### 场景3：技能读取其他技能的数据
当技能需要访问其他技能的配置或日志时：

```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# 读取其他技能的配置
other_config = storage.get_config("other-skill")

# 读取其他技能的日志
other_logs = storage.get_logs("other-skill")
```

## 核心功能说明

### 智能体可处理的功能
- API使用咨询：解释如何使用技能管理者的各个功能
- 数据格式建议：根据存储需求推荐合适的数据结构
- 数据分析：分析存储的配置和日志，发现模式或问题
- 存储管理：查看所有已存储的技能，清理过期数据

### 脚本实现的功能
- **SkillStorage类**：完整的存储和读取API，见 [scripts/skill_manager.py](scripts/skill_manager.py)
  - `save_config(skill_name, config)`: 存储技能配置
  - `save_logs(skill_name, logs)`: 存储技能日志
  - `save(skill_name, config, logs)`: 同时存储配置和日志
  - `get_config(skill_name)`: 读取技能配置
  - `get_logs(skill_name)`: 读取技能日志
  - `get_all()`: 读取所有技能数据
  - `list_skills()`: 列出所有已存储的技能
  - `delete(skill_name)`: 删除技能数据

## 数据存储格式

技能管理者使用统一的JSON格式存储数据：

```json
{
  "skill-name-1": {
    "config": {
      "key1": "value1",
      "key2": "value2"
    },
    "logs": [
      {"time": "2024-01-22 12:00:00", "message": "日志1"},
      {"time": "2024-01-22 12:05:00", "message": "日志2"}
    ],
    "last_updated": "2024-01-22 12:05:00"
  },
  "skill-name-2": {
    "config": {},
    "logs": [],
    "last_updated": "2024-01-22 12:10:00"
  }
}
```

## 资源索引
- **核心模块**：见 [scripts/skill_manager.py](scripts/skill_manager.py)（SkillStorage类完整实现）
- **API规范**：见 [references/api_spec.md](references/api_spec.md)（详细的API文档和使用示例）

## 注意事项
- 技能管理者是一个服务型Skill，不主动运行，被其他技能调用
- 存储路径建议使用 `/workspace/projects/skill-data.json` 实现统一管理
- 配置和日志的数据格式由调用技能自行定义，技能管理者只负责存储
- 每次存储会更新 `last_updated` 时间戳
- 支持增量更新，不会覆盖已有的配置或日志（除非显式指定覆盖）

## 最佳实践
- 技能名使用一致的命名规范（如小写字母加连字符）
- 配置数据建议包含必要元数据（如创建时间、版本号等）
- 日志数据建议包含时间戳和日志级别
- 定期清理不再使用的技能数据，避免存储文件过大
- 在技能启动时读取配置，在执行过程中记录日志
- 智能体可以协助查询和分析存储的数据，发现技能协作机会

## 使用示例

### 示例1：技能集成技能管理者
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

# 初始化存储
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# 存储技能配置
skill_config = {
    "mode": "production",
    "output_dir": "/workspace/output",
    "retry_count": 3
}
storage.save_config("my-awesome-skill", skill_config)

# 记录运行日志
execution_logs = [
    {"time": "2024-01-22 10:00:00", "level": "INFO", "message": "开始执行"},
    {"time": "2024-01-22 10:00:05", "level": "INFO", "message": "加载配置"},
    {"time": "2024-01-22 10:00:10", "level": "INFO", "message": "执行完成"}
]
storage.save_logs("my-awesome-skill", execution_logs)
```

### 示例2：查询技能协作数据
```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# 查看所有已存储的技能
all_skills = storage.list_skills()
print(f"已存储的技能: {all_skills}")

# 读取特定技能的配置
config = storage.get_config("dev-observability")
print(f"配置: {config}")

# 读取特定技能的日志
logs = storage.get_logs("dev-observability")
print(f"最近日志: {logs[-5:]}")
```

### 示例3：智能体分析存储数据
当智能体需要分析多个技能的协作情况时：

1. 读取所有技能数据
2. 分析技能间的配置关联
3. 识别共享的依赖或数据
4. 提供优化建议

智能体可以基于存储的数据，发现技能组合的潜在问题和优化机会。
