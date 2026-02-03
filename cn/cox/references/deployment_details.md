# 部署方案详细说明

本文档提供三种部署方案的详细配置和使用说明。

## 目录
- [静态网页方案](#静态网页方案)
- [交互网页方案](#交互网页方案推荐)
- [全面方案](#全面方案暂不提供)

---

## 静态网页方案

- **特点**：生成静态 HTML 文件，数据内联到 HTML 中，无需额外的 JSON 文件
- **适用场景**：受限环境（如在线沙盒环境）、快速验证需求
- **使用门槛**：无需任何额外依赖（不需要安装 Flask）
- **使用方式**：调用 `scripts/run_web_observability.py --mode static`，生成 `observability.html` 文件
- **刷新方式**：点击刷新按钮重新渲染数据（静态模式不支持自动刷新）

### 部署后调用skill-manager

**方式一：使用辅助脚本（推荐）**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode static \
  --config '{
    "output_path": "/workspace/projects/cox/observability.html",
    "access_method": "打开生成的 observability.html 文件",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**方式二：直接调用 skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "static",
    "output_path": "/workspace/projects/cox/observability.html",
    "access_method": "打开生成的 observability.html 文件",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "静态网页方案部署完成，HTML文件: /workspace/projects/cox/observability.html"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```

---

## 交互网页方案（推荐）

- **特点**：提供本地 Web 界面，支持实时数据刷新（每 30 秒），支持交互
- **适用场景**：需要实时监控
- **使用门槛**：需要安装 Flask（`pip install flask`）
- **使用方式**：调用 `scripts/run_web_observability.py --mode web`，访问 http://localhost:5000

### 部署后调用skill-manager

**方式一：使用辅助脚本（推荐）**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode web \
  --config '{
    "url": "http://localhost:5000",
    "access_method": "浏览器访问 http://localhost:5000",
    "manual_path": "/workspace/projects/cox/SKILL.md"
  }'
```

**方式二：直接调用 skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "web",
    "url": "http://localhost:5000",
    "access_method": "浏览器访问 http://localhost:5000",
    "manual_path": "/workspace/projects/cox/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "交互网页方案部署完成，访问地址: http://localhost:5000"
}]

storage.save("cox", config=skill_config, logs=execution_logs)
```


---

## 全面方案（暂不提供）

- 特点：使用 Prometheus + Grafana 专业可观测工具，Docker 部署
- 适用场景：准备迁移到生产环境、需要专业监控能力
- 状态：暂不开放，待完善数据对接和配置方案后上线。
