# Deployment Solution Detailed Instructions

This document provides detailed configuration and usage instructions for three deployment solutions.

## Table of Contents
- [Simple Solution](#simple-solution-recommended-for-beginners)
- [Intermediate Solution](#intermediate-solution-recommended-for-small-teams)
- [Comprehensive Solution](#comprehensive-solution-not-currently-available)

---

## Simple Solution (Recommended for Beginners)

### Characteristics
- Generates structured logs only, no interface
- Zero dependencies, zero configuration, ready to use

### Use Cases
- Individual development
- Quick requirement validation
- No visualization needed

### Usage
```bash
python scripts/generate_observability_log.py --project project_data.json --app app_status.json --test test_metrics.json
```

### Invoke skill-manager After Deployment

**Method 1: Use Helper Script (Recommended)**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode simple \
  --config '{
    "output_path": "/workspace/projects/cox/output.log",
    "access_method": "cat /workspace/projects/cox/output.log",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**Method 2: Directly Invoke skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "simple",
    "output_path": "/workspace/projects/cox/output.log",
    "access_method": "cat /workspace/projects/cox/output.log",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "Simple solution deployment complete, log file: /workspace/projects/cox/output.log"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```

---

## Intermediate Solution (Recommended for Small Teams)

### Characteristics
- Provides local Web interface displaying observability data
- Lightweight, easy to deploy, real-time refresh

### Use Cases
- 5-10 person team development
- Need visualization interface

### Usage
```bash
python scripts/run_web_observability.py --project project_data.json --app app_status.json --test test_metrics.json
# Visit http://localhost:5000 to view interface
```

### Invoke skill-manager After Deployment

**Method 1: Use Helper Script (Recommended)**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode web \
  --config '{
    "url": "http://localhost:5000",
    "access_method": "Browser access http://localhost:5000",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**Method 2: Directly Invoke skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "web",
    "url": "http://localhost:5000",
    "access_method": "Browser access http://localhost:5000",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "Intermediate solution deployment complete, access URL: http://localhost:5000"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```

### Important Note
Intermediate solution also generates `observability.log` log file, format consistent with simple solution, facilitating access by other skills.

---

## Comprehensive Solution (Not Currently Available)

### Characteristics
- Use Prometheus+Grafana professional observability tools
- Docker deployment
- Standard technology stack, scalable, production-ready

### Use Cases
- Preparing to migrate to production environment
- Need professional monitoring capabilities

### Status
Not yet available, pending data integration and configuration solution completion.
