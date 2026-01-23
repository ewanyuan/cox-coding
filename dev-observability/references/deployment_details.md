# 部署方案详细说明

本文档提供三种部署方案的详细配置和使用说明。

## 目录
- [简单方案](#简单方案推荐初学者)
- [中等方案](#中等方案推荐小团队)
- [全面方案](#全面方案暂不提供)

---

## 简单方案（推荐初学者）

### 特点
- 仅生成结构化日志，无界面
- 零依赖、零配置、即用即走

### 适用场景
- 个人开发
- 快速验证需求
- 不需要可视化展示

### 使用方式
```bash
python scripts/generate_observability_log.py --project project_data.json --app app_status.json --test test_metrics.json
```

### 部署后调用skill-manager

**方式一：使用辅助脚本（推荐）**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode simple \
  --config '{
    "output_path": "/workspace/projects/dev-observability/output.log",
    "access_method": "cat /workspace/projects/dev-observability/output.log",
    "manual_path": "/workspace/projects/dev-observability/SKILL.md"
  }'
```

**方式二：直接调用 skill-manager API**
```python
import sys
sys.path.insert(0, '/workspace/projects/skill-manager/scripts')
from skill_manager import SkillStorage

storage = SkillStorage(data_path="/workspace/projects/skill-data.json")

skill_config = {
    "deploy_mode": "simple",
    "output_path": "/workspace/projects/dev-observability/output.log",
    "access_method": "cat /workspace/projects/dev-observability/output.log",
    "manual_path": "/workspace/projects/dev-observability/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "简单方案部署完成，日志文件: /workspace/projects/dev-observability/output.log"
}]

storage.save("dev-observability", config=skill_config, logs=execution_logs)
```

---

## 中等方案（推荐小团队）

### 特点
- 提供本地Web界面展示可观测数据
- 轻量级、易部署、实时刷新

### 适用场景
- 5-10人团队开发
- 需要可视化界面

### 使用方式
```bash
python scripts/run_web_observability.py --project project_data.json --app app_status.json --test test_metrics.json
# 访问 http://localhost:5000 查看界面
```

### 部署后调用skill-manager

**方式一：使用辅助脚本（推荐）**
```bash
python scripts/store_to_skill_manager.py deploy \
  --mode web \
  --config '{
    "url": "http://localhost:5000",
    "access_method": "浏览器访问 http://localhost:5000",
    "manual_path": "/workspace/projects/dev-observability/SKILL.md"
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
    "manual_path": "/workspace/projects/dev-observability/SKILL.md"
}

execution_logs = [{
    "time": "2024-01-22 12:00:00",
    "level": "INFO",
    "message": "中等方案部署完成，访问地址: http://localhost:5000"
}]

storage.save("dev-observability", config=skill_config, logs=execution_logs)
```

### 重要说明
中等方案也会生成 `observability.log` 日志文件，与简单方案格式保持一致，方便其他技能访问。

---

## 全面方案（暂不提供）

### 特点
- 使用Prometheus+Grafana专业可观测工具
- Docker部署
- 标准技术栈、可扩展、生产就绪

### 适用场景
- 准备迁移到生产环境
- 需要专业监控能力

### 状态
暂不开放，待完善数据对接和配置方案后上线。
