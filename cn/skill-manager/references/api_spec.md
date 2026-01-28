# 技能管理者 API 规范

## 目录
- [概述](#概述)
- [快速开始](#快速开始)
- [核心API](#核心api)
- [数据格式](#数据格式)
- [使用示例](#使用示例)
- [最佳实践](#最佳实践)

## 概述

技能管理者为其他技能提供统一的配置和日志存储服务，支持技能间数据共享和协作。

**核心特性**：
- 统一的JSON格式存储
- 简洁的Python API
- 支持增量更新
- 灵活的路径配置
- 完整的查询和管理功能

**设计理念**：
- 服务导向：作为被动服务被其他技能调用
- 数据中立：不限制配置和日志的数据格式
- 简单易用：提供直观的API接口
- 可扩展性：支持大量技能和数据

## 快速开始

### 安装和导入

```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

# 初始化存储实例
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")
```

### 基本使用

```python
# 存储配置
storage.save_config("my-skill", {
    "mode": "production",
    "output_dir": "/workspace/output"
})

# 存储日志
storage.save_logs("my-skill", [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "开始执行"}
])

# 读取数据
config = storage.get_config("my-skill")
logs = storage.get_logs("my-skill")
```

## 核心API

### SkillStorage 类

#### `__init__(self, data_path: str = None)`

初始化技能存储实例。

**参数**：
- `data_path`: 数据文件路径，默认为 `/workspace/projects/skill-data.json`

**示例**：
```python
# 使用默认路径
storage = SkillStorage()

# 使用自定义路径
storage = SkillStorage(data_path="/custom/path/skill-data.json")
```

---

#### `save_config(self, skill_name: str, config: Dict[str, Any])`

存储技能配置。

**参数**：
- `skill_name`: 技能名称（建议使用小写字母和连字符）
- `config`: 配置数据（字典格式）

**示例**：
```python
storage.save_config("my-skill", {
    "deploy_mode": "simple",
    "output_path": "/workspace/output/log.txt",
    "access_method": "cat /workspace/output/log.txt",
    "manual_path": "/workspace/projects/my-skill/SKILL.md",
    "timestamp": "2024-01-22 12:00:00"
})
```

**注意**：每次调用会覆盖该技能的配置，如需保留部分配置应先读取再合并。

---

#### `save_logs(self, skill_name: str, logs: List[Dict[str, Any]], append: bool = True)`

存储技能日志。

**参数**：
- `skill_name`: 技能名称
- `logs`: 日志数据（列表格式）
- `append`: 是否追加到现有日志，`True`为追加，`False`为覆盖

**示例**：
```python
# 追加日志
storage.save_logs("my-skill", [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "开始执行"},
    {"time": "2024-01-22 12:05:00", "level": "INFO", "message": "执行完成"}
], append=True)

# 覆盖日志
storage.save_logs("my-skill", new_logs, append=False)
```

---

#### `save(self, skill_name: str, config: Dict[str, Any] = None, logs: List[Dict[str, Any]] = None, append_logs: bool = True)`

同时存储技能配置和日志。

**参数**：
- `skill_name`: 技能名称
- `config`: 配置数据（可选）
- `logs`: 日志数据（可选）
- `append_logs`: 日志是否追加到现有日志

**示例**：
```python
storage.save(
    skill_name="my-skill",
    config={"mode": "production"},
    logs=[{"time": "2024-01-22 12:00:00", "message": "开始"}],
    append_logs=True
)
```

---

#### `get_config(self, skill_name: str) -> Optional[Dict[str, Any]]`

读取技能配置。

**参数**：
- `skill_name`: 技能名称

**返回值**：配置数据字典，如果技能不存在则返回`None`

**示例**：
```python
config = storage.get_config("my-skill")
if config:
    print(f"部署模式: {config.get('deploy_mode')}")
else:
    print("技能不存在")
```

---

#### `get_logs(self, skill_name: str) -> Optional[List[Dict[str, Any]]]`

读取技能日志。

**参数**：
- `skill_name`: 技能名称

**返回值**：日志数据列表，如果技能不存在则返回`None`

**示例**：
```python
logs = storage.get_logs("my-skill")
if logs:
    print(f"总日志数: {len(logs)}")
    print(f"最近日志: {logs[-1]}")
```

---

#### `get(self, skill_name: str) -> Optional[Dict[str, Any]]`

读取技能的所有数据（配置和日志）。

**参数**：
- `skill_name`: 技能名称

**返回值**：包含`config`、`logs`、`last_updated`的字典

**示例**：
```python
skill_data = storage.get("my-skill")
if skill_data:
    config = skill_data["config"]
    logs = skill_data["logs"]
    last_updated = skill_data["last_updated"]
```

---

#### `get_all(self) -> Dict[str, Any]`

读取所有技能数据。

**返回值**：所有技能数据的字典

**示例**：
```python
all_data = storage.get_all()
for skill_name, skill_data in all_data.items():
    print(f"{skill_name}: {skill_data['last_updated']}")
```

---

#### `list_skills(self) -> List[str]`

列出所有已存储的技能名称。

**返回值**：技能名称列表

**示例**：
```python
skills = storage.list_skills()
print(f"已存储的技能: {skills}")
```

---

#### `delete(self, skill_name: str) -> bool`

删除技能数据。

**参数**：
- `skill_name`: 技能名称

**返回值**：是否删除成功

**示例**：
```python
if storage.delete("old-skill"):
    print("删除成功")
else:
    print("技能不存在")
```

---

#### `clear(self)`

清空所有数据。

**示例**：
```python
storage.clear()
print("已清空所有数据")
```

---

#### `get_stats(self) -> Dict[str, Any]`

获取存储统计信息。

**返回值**：包含统计信息的字典

**示例**：
```python
stats = storage.get_stats()
print(f"技能总数: {stats['total_skills']}")
for skill_name, skill_stats in stats['skills'].items():
    print(f"{skill_name}: {skill_stats['logs_count']} 条日志")
```

## 数据格式

### 存储文件格式

技能管理者使用JSON格式存储所有数据：

```json
{
  "skill-name-1": {
    "config": {
      "key1": "value1",
      "key2": "value2"
    },
    "logs": [
      {
        "time": "2024-01-22 12:00:00",
        "level": "INFO",
        "message": "日志消息"
      }
    ],
    "last_updated": "2024-01-22 12:00:00"
  },
  "skill-name-2": {
    "config": {},
    "logs": [],
    "last_updated": "2024-01-22 12:10:00"
  }
}
```

### 配置数据格式

配置数据格式由调用技能自行定义，建议包含：

- **必要元数据**：创建时间、版本号、技能状态
- **业务配置**：部署模式、输出路径、访问方式等
- **用户手册位置**：便于其他技能引用

**示例**：
```python
{
    "deploy_mode": "simple",
    "output_path": "/workspace/output/observability.log",
    "access_method": "cat /workspace/output/observability.log",
    "manual_path": "/workspace/projects/dev-observability/SKILL.md",
    "timestamp": "2024-01-22 12:00:00"
}
```

### 日志数据格式

日志数据格式由调用技能自行定义，建议包含：

- **时间戳**：`time`字段
- **日志级别**：`level`字段（INFO、WARNING、ERROR等）
- **消息内容**：`message`字段
- **上下文信息**：根据需要添加其他字段

**示例**：
```python
[
    {
        "time": "2024-01-22 12:00:00",
        "level": "INFO",
        "message": "开始执行",
        "step": "initialization"
    },
    {
        "time": "2024-01-22 12:05:00",
        "level": "WARNING",
        "message": "发现警告",
        "details": "..."
    }
]
```

## 使用示例

### 示例1：技能集成技能管理者

```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

def my_skill_main():
    # 初始化存储
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # 1. 存储配置
    skill_config = {
        "mode": "production",
        "output_dir": "/workspace/output",
        "retry_count": 3
    }
    storage.save_config("my-awesome-skill", skill_config)

    # 2. 执行技能逻辑
    execution_logs = []

    try:
        # ... 执行逻辑 ...
        execution_logs.append({
            "time": "2024-01-22 10:00:00",
            "level": "INFO",
            "message": "开始执行"
        })

        # ... 更多逻辑 ...

        execution_logs.append({
            "time": "2024-01-22 10:05:00",
            "level": "INFO",
            "message": "执行完成"
        })

    except Exception as e:
        execution_logs.append({
            "time": "2024-01-22 10:03:00",
            "level": "ERROR",
            "message": f"执行失败: {str(e)}"
        })

    # 3. 存储日志
    storage.save_logs("my-awesome-skill", execution_logs, append=True)

if __name__ == '__main__':
    my_skill_main()
```

### 示例2：查询技能协作数据

```python
from skill_manager import SkillStorage

def analyze_skills():
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # 1. 列出所有技能
    skills = storage.list_skills()
    print(f"已存储的技能 ({len(skills)}):")
    for skill in skills:
        print(f"  - {skill}")

    # 2. 分析特定技能的配置
    dev_obs_config = storage.get_config("dev-observability")
    if dev_obs_config:
        print(f"\n可观测系统配置:")
        print(f"  部署模式: {dev_obs_config.get('deploy_mode')}")
        print(f"  输出路径: {dev_obs_config.get('output_path')}")

    # 3. 查看技能日志
    dev_obs_logs = storage.get_logs("dev-observability")
    if dev_obs_logs:
        print(f"\n最近5条日志:")
        for log in dev_obs_logs[-5:]:
            print(f"  [{log.get('time')}] {log.get('message')}")

if __name__ == '__main__':
    analyze_skills()
```

### 示例3：智能体分析存储数据

当智能体需要分析多个技能的协作情况时：

1. 读取所有技能数据
2. 分析技能间的配置关联
3. 识别共享的依赖或数据
4. 提供优化建议

```python
from skill_manager import SkillStorage

def analyze_collaboration():
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # 获取所有技能数据
    all_data = storage.get_all()

    # 分析输出路径关联
    output_paths = {}
    for skill_name, skill_data in all_data.items():
        config = skill_data.get("config", {})
        output_path = config.get("output_path")
        if output_path:
            if output_path not in output_paths:
                output_paths[output_path] = []
            output_paths[output_path].append(skill_name)

    # 检测共享输出路径
    print("技能协作分析:")
    for path, skills in output_paths.items():
        if len(skills) > 1:
            print(f"  共享输出路径: {path}")
            print(f"    涉及技能: {', '.join(skills)}")

if __name__ == '__main__':
    analyze_collaboration()
```

## 最佳实践

### 1. 技能命名规范
- 使用小写字母和连字符：`my-awesome-skill`
- 避免使用下划线或驼峰命名
- 保持命名简洁且有意义

### 2. 配置数据设计
- 包含必要的元数据（创建时间、版本号）
- 使用扁平的键值对结构
- 提供用户手册位置，便于其他技能引用
- 记录部署模式、输出路径、访问方式等关键信息

### 3. 日志数据设计
- 始终包含时间戳
- 使用标准日志级别（INFO、WARNING、ERROR）
- 提供足够的上下文信息
- 定期清理过期日志，避免存储文件过大

### 4. 增量更新
- 使用`append_logs=True`追加日志，避免覆盖历史数据
- 修改配置时先读取再合并，保留未修改的字段
- 定期检查`last_updated`时间戳，追踪数据变更

### 5. 存储路径管理
- 使用统一路径：`/workspace/projects/skill-data.json`
- 定期备份存储文件
- 监控存储文件大小，必要时清理

### 6. 错误处理
- 检查返回值是否为`None`
- 处理文件读写异常
- 提供有意义的错误提示

### 7. 性能优化
- 避免频繁调用`get_all()`，使用`get()`或`get_config()`
- 批量操作时减少磁盘I/O
- 日志量过大时考虑分片存储

### 8. 安全性
- 不在配置中存储敏感信息（密码、密钥等）
- 限制存储文件的访问权限
- 定期审计存储的内容

### 9. 智能体协作
- 智能体可以基于存储的数据发现技能协作机会
- 提供查询接口供智能体分析技能关系
- 利用存储数据生成协作报告

### 10. 技能组合
- 多个技能可以共享同一个存储文件
- 通过技能名区分不同技能的数据
- 智能体可以查询所有技能数据，发现优化点
