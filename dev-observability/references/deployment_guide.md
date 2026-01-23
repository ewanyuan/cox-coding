# 可观测系统部署指南

## 目录
- [环境准备](#环境准备)
- [简单方案部署](#简单方案部署)
- [中等方案部署](#中等方案部署)
- [全面方案部署](#全面方案部署)
- [方案迁移](#方案迁移)
- [常见问题](#常见问题)

## 环境准备

### 基础环境要求
- Python 3.7+
- pip包管理工具

### 简单方案环境
无需额外依赖，Python标准库即可

### 中等方案环境
安装Flask依赖：
```bash
pip install flask>=2.0.0
```

### 全面方案环境
- Docker 20.10+
- Docker Compose 2.0+
- 至少2GB可用内存

## 简单方案部署

### 部署步骤

1. **准备数据文件**
   按照数据格式规范创建三个JSON文件：
   - `project_data.json`
   - `app_status.json`
   - `test_metrics.json`

2. **生成可观测日志**
   ```bash
   python scripts/generate_observability_log.py \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json
   ```

3. **查看日志输出**
   脚本会在终端输出格式化的可观测信息，同时生成日志文件 `observability.log`

4. **分析日志**
   ```bash
   # 查看完整日志
   cat observability.log

   # 过滤特定维度
   grep "PROJECT:" observability.log
   grep "APP:" observability.log
   grep "TEST:" observability.log

   # 查看异常信息
   grep "ANOMALY:" observability.log
   ```

### 参数说明
- `--project`：项目数据文件路径（必填）
- `--app`：应用状态文件路径（必填）
- `--test`：测试指标文件路径（必填）
- `--output`：输出日志文件路径（可选，默认：observability.log）

### 优势
- 零配置，即用即走
- 无需网络服务，适合本地开发
- 可结合grep、awk等工具进行定制化分析

### 局限性
- 无可视化界面
- 不支持多用户访问
- 无历史数据对比

## 中等方案部署

### 部署步骤

1. **准备数据文件**
   同简单方案，创建三个JSON数据文件

2. **安装依赖**
   ```bash
   pip install flask>=2.0.0
   ```

3. **启动Web服务**
   ```bash
   python scripts/run_web_observability.py \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json \
     --port 5000
   ```

4. **访问Web界面**
   在浏览器中打开 `http://localhost:5000`

5. **自动刷新**
   Web界面支持自动刷新（默认每30秒），无需手动重新加载页面

### 参数说明
- `--project`：项目数据文件路径（必填）
- `--app`：应用状态文件路径（必填）
- `--test`：测试指标文件路径（必填）
- `--port`：Web服务端口（可选，默认：5000）
- `--refresh-interval`：自动刷新间隔秒数（可选，默认：30）

### Web界面功能
1. **项目概览**：展示迭代列表、任务统计、假设状态
2. **应用状态**：展示模块列表、完成率、状态分布
3. **测试监控**：展示测试套件结果、埋点状态、异常列表
4. **实时刷新**：自动检测数据文件变化并刷新界面
5. **过滤筛选**：支持按状态、优先级等条件筛选

### 高级配置
修改服务监听地址：
```bash
python scripts/run_web_observability.py \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 0.0.0.0 \
  --port 5000
```

这样其他设备可以通过 `http://<服务器IP>:5000` 访问

### 优势
- 可视化界面，直观易懂
- 支持多用户访问
- 实时数据刷新
- 部署简单，维护成本低

### 局限性
- 无历史数据存储
- 无告警机制
- 扩展性有限

## 全面方案部署

### 部署步骤

1. **准备环境**
   ```bash
   # 检查Docker版本
   docker --version

   # 检查Docker Compose版本
   docker-compose --version
   ```

2. **准备数据文件**
   同其他方案，创建三个JSON数据文件

3. **配置Prometheus**
   编辑 `assets/docker_compose/prometheus.yml`，添加数据采集配置：
   ```yaml
   scrape_configs:
     - job_name: 'observability'
       static_configs:
         - targets: ['localhost:8080']
       scrape_interval: 30s
   ```

4. **启动服务**
   ```bash
   cd assets/docker_compose
   docker-compose up -d
   ```

5. **访问服务**
   - Prometheus：http://localhost:9090
   - Grafana：http://localhost:3000（默认账号：admin/admin）

6. **配置Grafana**
   - 登录Grafana后，添加Prometheus数据源
   - 导入预置仪表板（位于 `assets/docker_compose/grafana/dashboards/`）
   - 开始监控可观测数据

### 数据转换脚本
将JSON数据转换为Prometheus指标格式：

```bash
python scripts/collect_data.py export-prometheus \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output metrics.prom
```

然后让Prometheus采集该指标文件。

### Docker Compose服务说明

| 服务名称 | 端口 | 说明 |
|---------|------|------|
| prometheus | 9090 | 指标采集和存储 |
| grafana | 3000 | 可视化仪表板 |
| pushgateway | 9091 | 临时指标推送（可选） |

### 优势
- 专业级监控能力
- 支持历史数据存储和查询
- 丰富的告警规则
- 可扩展到生产环境
- 标准技术栈，社区成熟

### 局限性
- 部署复杂度较高
- 需要较多系统资源
- 学习曲线较陡

## 方案迁移

### 简单 -> 中等
迁移步骤：
1. 数据文件通用，无需修改
2. 安装Flask依赖
3. 启动Web服务
4. 访问Web界面验证

### 中等 -> 全面
迁移步骤：
1. 准备Docker环境
2. 使用数据转换脚本生成Prometheus指标
3. 配置Prometheus和Grafana
4. 验证数据正确性
5. 逐步切换到新系统

### 全面 -> 中等/简单
如需降级：
1. 保留原始JSON数据文件
2. 直接使用中等或简单方案的脚本
3. 清理Docker容器和镜像

## 常见问题

### 简单方案相关问题

**Q：日志文件太大如何处理？**
A：可以定期清理或使用日志轮转工具，如 `logrotate`。

**Q：如何筛选特定迭代的数据？**
A：使用 `grep` 过滤：`grep "ITERATION-ID" observability.log`

### 中等方案相关问题

**Q：Web界面无法访问？**
A：检查端口是否被占用，尝试修改 `--port` 参数；检查防火墙设置。

**Q：数据更新后界面不刷新？**
A：确认数据文件保存成功，等待自动刷新周期（默认30秒），或手动刷新浏览器页面。

**Q：如何让其他团队成员访问？**
A：使用 `--host 0.0.0.0` 参数，并确保网络可访问。

### 全面方案相关问题

**Q：Docker容器启动失败？**
A：检查端口占用、Docker资源限制、查看容器日志：`docker-compose logs <service_name>`

**Q：Grafana无法连接Prometheus？**
A：检查数据源配置中的URL是否正确（通常是 `http://prometheus:9090`）

**Q：如何自定义Grafana仪表板？**
A：在Grafana界面中创建新仪表板，或编辑预置仪表板，满足特定需求。

### 数据相关问题

**Q：数据格式验证失败？**
A：使用 `scripts/collect_data.py validate` 命令检查具体错误信息，参考数据格式规范修正。

**Q：如何从现有系统导入数据？**
A：编写转换脚本，将现有系统数据转换为符合规范的JSON格式。

**Q：数据文件如何版本控制？**
A：建议将数据文件纳入Git版本控制，方便追踪历史变更。

## 最佳实践

1. **选择合适的方案**：根据团队规模和需求选择部署方案
2. **定期更新数据**：建立数据更新机制，保持可观测数据新鲜度
3. **持续优化**：根据使用反馈，不断调整监控指标和界面展示
4. **文档维护**：及时更新数据文件和配置文档，保持信息同步
5. **备份重要数据**：定期备份JSON数据文件，防止意外丢失
6. **安全性考虑**：生产环境使用时，注意设置访问控制和数据加密
