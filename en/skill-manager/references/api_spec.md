# Skill Manager API Specification

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core API](#core-api)
- [Data Format](#data-format)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Overview

Skill manager provides unified configuration and log storage services for other skills, supporting data sharing and collaboration between skills.

**Core Features**:
- Unified JSON format storage
- Concise Python API
- Supports incremental updates
- Flexible path configuration
- Complete query and management capabilities

**Design Philosophy**:
- Service-oriented: Passive service invoked by other skills
- Data-neutral: Doesn't limit configuration and log data formats
- Simple and easy-to-use: Provides intuitive API interface
- Scalable: Supports large numbers of skills and data

## Quick Start

### Installation and Import

```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

# Initialize storage instance
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")
```

### Basic Usage

```python
# Store configuration
storage.save_config("my-skill", {
    "mode": "production",
    "output_dir": "/workspace/output"
})

# Store logs
storage.save_logs("my-skill", [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "Start execution"}
])

# Read data
config = storage.get_config("my-skill")
logs = storage.get_logs("my-skill")
```

## Core API

### SkillStorage Class

#### `__init__(self, data_path: str = None)`

Initialize skill storage instance.

**Parameters**:
- `data_path`: Data file path, defaults to `/workspace/projects/skill-data.json`

**Example**:
```python
# Use default path
storage = SkillStorage()

# Use custom path
storage = SkillStorage(data_path="/custom/path/skill-data.json")
```

---

#### `save_config(self, skill_name: str, config: Dict[str, Any])`

Store skill configuration.

**Parameters**:
- `skill_name`: Skill name (recommended to use lowercase letters and hyphens)
- `config`: Configuration data (dictionary format)

**Example**:
```python
storage.save_config("my-skill", {
    "deploy_mode": "simple",
    "output_path": "/workspace/output/log.txt",
    "access_method": "cat /workspace/output/log.txt",
    "manual_path": "/workspace/projects/my-skill/SKILL.md",
    "timestamp": "2024-01-22 12:00:00"
})
```

**Note**: Each invocation overwrites that skill's configuration, to preserve partial configuration should read first then merge.

---

#### `save_logs(self, skill_name: str, logs: List[Dict[str, Any]], append: bool = True)`

Store skill logs.

**Parameters**:
- `skill_name`: Skill name
- `logs`: Log data (list format)
- `append`: Whether to append to existing logs, `True` for append, `False` for overwrite

**Example**:
```python
# Append logs
storage.save_logs("my-skill", [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "Start execution"},
    {"time": "2024-01-22 12:05:00", "level": "INFO", "message": "Execution completed"}
], append=True)

# Overwrite logs
storage.save_logs("my-skill", new_logs, append=False)
```

---

#### `save(self, skill_name: str, config: Dict[str, Any] = None, logs: List[Dict[str, Any]] = None, append_logs: bool = True)`

Simultaneously store skill configuration and logs.

**Parameters**:
- `skill_name`: Skill name
- `config`: Configuration data (optional)
- `logs`: Log data (optional)
- `append_logs`: Whether to append logs to existing logs

**Example**:
```python
storage.save(
    skill_name="my-skill",
    config={"mode": "production"},
    logs=[{"time": "2024-01-22 12:00:00", "message": "Start"}],
    append_logs=True
)
```

---

#### `get_config(self, skill_name: str) -> Optional[Dict[str, Any]]`

Read skill configuration.

**Parameters**:
- `skill_name`: Skill name

**Return Value**: Configuration data dictionary, returns `None` if skill doesn't exist

**Example**:
```python
config = storage.get_config("my-skill")
if config:
    print(f"Deployment mode: {config.get('deploy_mode')}")
else:
    print("Skill doesn't exist")
```

---

#### `get_logs(self, skill_name: str) -> Optional[List[Dict[str, Any]]]`

Read skill logs.

**Parameters**:
- `skill_name`: Skill name

**Return Value**: Log data list, returns `None` if skill doesn't exist

**Example**:
```python
logs = storage.get_logs("my-skill")
if logs:
    print(f"Total log count: {len(logs)}")
    print(f"Recent logs: {logs[-1]}")
```

---

#### `get(self, skill_name: str) -> Optional[Dict[str, Any]]`

Read all data for a skill (configuration and logs).

**Parameters**:
- `skill_name`: Skill name

**Return Value**: Dictionary containing `config`, `logs`, `last_updated`

**Example**:
```python
skill_data = storage.get("my-skill")
if skill_data:
    config = skill_data["config"]
    logs = skill_data["logs"]
    last_updated = skill_data["last_updated"]
```

---

#### `get_all(self) -> Dict[str, Any]`

Read all skills data.

**Return Value**: Dictionary of all skills data

**Example**:
```python
all_data = storage.get_all()
for skill_name, skill_data in all_data.items():
    print(f"{skill_name}: {skill_data['last_updated']}")
```

---

#### `list_skills(self) -> List[str]`

List names of all stored skills.

**Return Value**: List of skill names

**Example**:
```python
skills = storage.list_skills()
print(f"Stored skills: {skills}")
```

---

#### `delete(self, skill_name: str) -> bool`

Delete skill data.

**Parameters**:
- `skill_name`: Skill name

**Return Value**: Whether deletion was successful

**Example**:
```python
if storage.delete("old-skill"):
    print("Deletion successful")
else:
    print("Skill doesn't exist")
```

---

#### `clear(self)`

Clear all data.

**Example**:
```python
storage.clear()
print("All data cleared")
```

---

#### `get_stats(self) -> Dict[str, Any]`

Get storage statistics.

**Return Value**: Dictionary containing statistical information

**Example**:
```python
stats = storage.get_stats()
print(f"Total skills: {stats['total_skills']}")
for skill_name, skill_stats in stats['skills'].items():
    print(f"{skill_name}: {skill_stats['logs_count']} logs")
```

## Data Format

### Storage File Format

Skill manager uses JSON format to store all data:

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
        "message": "Log message"
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

### Configuration Data Format

Configuration data format defined by calling skills, recommended to include:

- **Necessary metadata**: Creation time, version number, skill status
- **Business configuration**: Deployment mode, output path, access method, etc.
- **User manual location**: Facilitates other skills to reference

**Example**:
```python
{
    "deploy_mode": "simple",
    "output_path": "/workspace/output/observability.log",
    "access_method": "cat /workspace/output/observability.log",
    "manual_path": "/workspace/projects/dev-observability/SKILL.md",
    "timestamp": "2024-01-22 12:00:00"
}
```

### Log Data Format

Log data format defined by calling skills, recommended to include:

- **Timestamp**: `time` field
- **Log level**: `level` field (INFO, WARNING, ERROR, etc.)
- **Message content**: `message` field
- **Context information**: Add other fields as needed

**Example**:
```python
[
    {
        "time": "2024-01-22 12:00:00",
        "level": "INFO",
        "message": "Start execution",
        "step": "initialization"
    },
    {
        "time": "2024-01-22 12:05:00",
        "level": "WARNING",
        "message": "Discovered warning",
        "details": "..."
    }
]
```

## Usage Examples

### Example 1: Skill Integrates Skill Manager

```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

def my_skill_main():
    # Initialize storage
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # 1. Store configuration
    skill_config = {
        "mode": "production",
        "output_dir": "/workspace/output",
        "retry_count": 3
    }
    storage.save_config("my-awesome-skill", skill_config)

    # 2. Execute skill logic
    execution_logs = []

    try:
        # ... execute logic ...
        execution_logs.append({
            "time": "2024-01-22 10:00:00",
            "level": "INFO",
            "message": "Start execution"
        })

        # ... more logic ...

        execution_logs.append({
            "time": "2024-01-22 10:05:00",
            "level": "INFO",
            "message": "Execution completed"
        })

    except Exception as e:
        execution_logs.append({
            "time": "2024-01-22 10:03:00",
            "level": "ERROR",
            "message": f"Execution failed: {str(e)}"
        })

    # 3. Store logs
    storage.save_logs("my-awesome-skill", execution_logs, append=True)

if __name__ == '__main__':
    my_skill_main()
```

### Example 2: Query Skill Collaboration Data

```python
from skill_manager import SkillStorage

def analyze_skills():
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # 1. List all skills
    skills = storage.list_skills()
    print(f"Stored skills ({len(skills)}):")
    for skill in skills:
        print(f"  - {skill}")

    # 2. Analyze specific skill's configuration
    dev_obs_config = storage.get_config("dev-observability")
    if dev_obs_config:
        print(f"\nObservability system configuration:")
        print(f"  Deployment mode: {dev_obs_config.get('deploy_mode')}")
        print(f"  Output path: {dev_obs_config.get('output_path')}")

    # 3. View skill logs
    dev_obs_logs = storage.get_logs("dev-observability")
    if dev_obs_logs:
        print(f"\nRecent 5 logs:")
        for log in dev_obs_logs[-5:]:
            print(f"  [{log.get('time')}] {log.get('message')}")

if __name__ == '__main__':
    analyze_skills()
```

### Example 3: Agent Analyzes Stored Data

When Agent needs to analyze multiple skills' collaboration:

1. Read all skills data
2. Analyze configuration correlations between skills
3. Identify shared dependencies or data
4. Provide optimization recommendations

```python
from skill_manager import SkillStorage

def analyze_collaboration():
    storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

    # Get all skills data
    all_data = storage.get_all()

    # Analyze output path correlations
    output_paths = {}
    for skill_name, skill_data in all_data.items():
        config = skill_data.get("config", {})
        output_path = config.get("output_path")
        if output_path:
            if output_path not in output_paths:
                output_paths[output_path] = []
            output_paths[output_path].append(skill_name)

    # Detect shared output paths
    print("Skill collaboration analysis:")
    for path, skills in output_paths.items():
        if len(skills) > 1:
            print(f"  Shared output path: {path}")
            print(f"    Involved skills: {', '.join(skills)}")

if __name__ == '__main__':
    analyze_collaboration()
```

## Best Practices

### 1. Skill Naming Convention
- Use lowercase letters and hyphens: `my-awesome-skill`
- Avoid underscores or camelCase
- Keep naming concise and meaningful

### 2. Configuration Data Design
- Include necessary metadata (creation time, version number)
- Use flat key-value pair structure
- Provide user manual location, facilitating other skills to reference
- Record deployment mode, output path, access method and other key information

### 3. Log Data Design
- Always include timestamps
- Use standard log levels (INFO, WARNING, ERROR)
- Provide sufficient context information
- Periodically clean expired logs, avoid storage file becoming too large

### 4. Incremental Updates
- Use `append_logs=True` to append logs, avoid overwriting historical data
- When modifying configuration, read first then merge, preserve unmodified fields
- Periodically check `last_updated` timestamp, track data changes

### 5. Storage Path Management
- Use unified path: `/workspace/projects/skill-data.json`
- Periodically backup storage files
- Monitor storage file size, clean when necessary

### 6. Error Handling
- Check if return value is `None`
- Handle file read/write exceptions
- Provide meaningful error prompts

### 7. Performance Optimization
- Avoid frequent calls to `get_all()`, use `get()` or `get_config()`
- Reduce disk I/O during batch operations
- Consider sharded storage when log volume too large

### 8. Security
- Don't store sensitive information in configuration (passwords, keys, etc.)
- Limit access permissions for storage files
- Regularly audit stored content

### 9. Agent Collaboration
- Agent can based on stored data discover skill collaboration opportunities
- Provide query interfaces for Agent to analyze skill relationships
- Utilize stored data to generate collaboration reports

### 10. Skill Combination
- Multiple skills can share same storage file
- Distinguish different skills' data by skill name
- Agent can query all skills data, discover optimization points
