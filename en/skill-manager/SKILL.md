---
name: skill-manager
description: Provides unified configuration and log storage service for other skills, supporting data sharing and collaboration between skills
dependency: {}
---

# Skill Manager

## Task Objectives
- This Skill is used to: Provide other skills with unified configuration and log storage capabilities
- Capabilities include:
  1. Store skill configuration information
  2. Store skill execution logs
  3. Query configurations and logs by skill name
  4. Manage all skills' stored data
- Trigger Conditions: Actively invoked by other skills when needing to store or read data

## Usage Scenarios

### Scenario 1: Skill Stores Its Own Configuration
When skills need to persist configuration information, invoke skill manager to store:

```python
from skill_manager import SkillStorage

# Create storage instance
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# Store configuration
config = {
    "deploy_mode": "simple",
    "output_path": "/path/to/output.log",
    "timestamp": "2024-01-22 12:00:00"
}
storage.save_config("my-skill", config)
```

### Scenario 2: Skill Stores Execution Logs
When skills need to record execution logs, invoke skill manager to store:

```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

logs = [
    {"time": "2024-01-22 12:00:00", "level": "INFO", "message": "Start execution"},
    {"time": "2024-01-22 12:05:00", "level": "INFO", "message": "Execution completed"}
]
storage.save_logs("my-skill", logs)
```

### Scenario 3: Skill Reads Other Skills' Data
When skills need to access other skills' configurations or logs:

```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# Read other skill's configuration
other_config = storage.get_config("other-skill")

# Read other skill's logs
other_logs = storage.get_logs("other-skill")
```

## Core Functionality Description

### Agent-Processable Functions
- API usage consultation: Explain how to use various functions of skill manager
- Data format recommendations: Recommend appropriate data structures based on storage needs
- Data analysis: Analyze stored configurations and logs, discover patterns or issues
- Storage management: View all stored skills, clean expired data

### Script-Implemented Functions
- **SkillStorage class**: Complete storage and read API, see [scripts/skill_manager.py](scripts/skill_manager.py)
  - `save_config(skill_name, config)`: Store skill configuration
  - `save_logs(skill_name, logs)`: Store skill logs
  - `save(skill_name, config, logs)`: Simultaneously store configuration and logs
  - `get_config(skill_name)`: Read skill configuration
  - `get_logs(skill_name)`: Read skill logs
  - `get_all()`: Read all skills data
  - `list_skills()`: List all stored skills
  - `delete(skill_name)`: Delete skill data

## Data Storage Format

Skill manager uses unified JSON format to store data:

```json
{
  "skill-name-1": {
    "config": {
      "key1": "value1",
      "key2": "value2"
    },
    "logs": [
      {"time": "2024-01-22 12:00:00", "message": "Log 1"},
      {"time": "2024-01-22 12:05:00", "message": "Log 2"}
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

## Resource Index
- **Core Module**: See [scripts/skill_manager.py](scripts/skill_manager.py) (SkillStorage class complete implementation)
- **API Specification**: See [references/api_spec.md](references/api_spec.md) (Detailed API documentation and usage examples)

## Precautions
- Skill manager is a service-oriented Skill, doesn't run actively, invoked by other skills
- Storage path recommended to use `/workspace/projects/skill-data.json` for unified management
- Configuration and log data formats defined by calling skills, skill manager only responsible for storage
- Each storage updates `last_updated` timestamp
- Supports incremental updates, won't overwrite existing configurations or logs (unless explicitly specified to overwrite)

## Best Practices
- Use consistent naming convention for skill names (such as lowercase letters with hyphens)
- Configuration data recommended to include necessary metadata (such as creation time, version number, etc.)
- Log data recommended to include timestamps and log levels
- Periodically clean unused skill data, avoid storage file becoming too large
- Read configuration at skill startup, record logs during execution
- Agent can assist in querying and analyzing stored data, discovering skill collaboration opportunities

## Usage Examples

### Example 1: Skill Integrates Skill Manager
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

# Initialize storage
storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# Store skill configuration
skill_config = {
    "mode": "production",
    "output_dir": "/workspace/output",
    "retry_count": 3
}
storage.save_config("my-awesome-skill", skill_config)

# Record execution logs
execution_logs = [
    {"time": "2024-01-22 10:00:00", "level": "INFO", "message": "Start execution"},
    {"time": "2024-01-22 10:00:05", "level": "INFO", "message": "Load configuration"},
    {"time": "2024-01-22 10:00:10", "level": "INFO", "message": "Execution completed"}
]
storage.save_logs("my-awesome-skill", execution_logs)
```

### Example 2: Query Skill Collaboration Data
```python
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

# View all stored skills
all_skills = storage.list_skills()
print(f"Stored skills: {all_skills}")

# Read specific skill's configuration
config = storage.get_config("dev-observability")
print(f"Configuration: {config}")

# Read specific skill's logs
logs = storage.get_logs("dev-observability")
print(f"Recent logs: {logs[-5:]}")
```

### Example 3: Agent Analyzes Stored Data
When Agent needs to analyze multiple skills' collaboration:

1. Read all skills data
2. Analyze configuration correlations between skills
3. Identify shared dependencies or data
4. Provide optimization recommendations

Agent can based on stored data, discover potential issues and optimization opportunities in skill combinations.
