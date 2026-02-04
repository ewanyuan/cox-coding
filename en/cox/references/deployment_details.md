# Deployment Solution Details

This document provides detailed configuration and usage instructions for three deployment solutions.

## Table of Contents
- [Static Web Solution](#static-web-solution)
- [Interactive Web Solution](#interactive-web-solution-recommended)
- [Comprehensive Solution](#comprehensive-solution-not-available-yet)

---

## Static Web Solution

- **Features**: Generates static HTML files, data embedded in HTML, no additional JSON files required
- **Applicable Scenarios**: Restricted environments (such as online sandbox environments), quick requirement validation
- **Usage Threshold**: No additional dependencies required (no need to install Flask)
- **Usage Method**: Call `scripts/run_web_observability.py --mode static`, generates `observability.html` file
- **Refresh Method**: Click refresh button to re-render data (static mode does not support auto-refresh)

### Calling skill-manager after deployment

**Method One: Using auxiliary script (recommended)**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode static \
  --config '{
    "output_path": "/workspace/projects/cox/observability.html",
    "access_method": "Open generated observability.html file",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**Method Two: Directly calling skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "static",
    "output_path": "/workspace/projects/cox/observability.html",
    "access_method": "Open generated observability.html file",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "Static web solution deployed successfully, HTML file: /workspace/projects/cox/observability.html"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```

---

## Interactive Web Solution (Recommended)

- **Features**: Provides local web interface, supports real-time data refresh (every 30 seconds), supports interaction
- **Applicable Scenarios**: Real-time monitoring required
- **Usage Threshold**: Requires Flask installation (`pip install flask`)
- **Usage Method**: Call `scripts/run_web_observability.py --mode web`, access http://localhost:5000

### Calling skill-manager after deployment

**Method One: Using auxiliary script (recommended)**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode web \
  --config '{
    "url": "http://localhost:5000",
    "access_method": "Access http://localhost:5000 via browser",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**Method Two: Directly calling skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "web",
    "url": "http://localhost:5000",
    "access_method": "Access http://localhost:5000 via browser",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "Interactive web solution deployed successfully, access address: http://localhost:5000"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```


---

## Comprehensive Solution (Not Available Yet)

- Features: Professional observability tools using Prometheus + Grafana, Docker deployment
- Applicable Scenarios: Preparing to migrate to production environment, requiring professional monitoring capabilities
- Status: Not open yet, will be launched after improving data integration and configuration schemes.