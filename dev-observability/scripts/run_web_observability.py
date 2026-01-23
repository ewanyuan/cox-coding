#!/usr/bin/env python3
"""
可观测Web服务器（中等方案）
提供本地Web界面展示可观测数据
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import time


class ObservabilityData:
    """可观测数据管理"""

    def __init__(self, project_file, app_file, test_file):
        self.project_file = project_file
        self.app_file = app_file
        self.test_file = test_file
        self.last_modified = {}
        self._cache = {}

    def load_if_changed(self):
        """如果文件已修改则重新加载"""
        files = {
            'project': self.project_file,
            'app': self.app_file,
            'test': self.test_file
        }

        changed = False
        for name, path in files.items():
            try:
                mtime = os.path.getmtime(path)
                if name not in self.last_modified or mtime > self.last_modified[name]:
                    self.last_modified[name] = mtime
                    with open(path, 'r', encoding='utf-8') as f:
                        self._cache[name] = json.load(f)
                    changed = True
            except Exception as e:
                print(f"加载文件 {path} 失败: {e}")

        return changed

    def get_project_data(self):
        """获取项目数据"""
        if 'project' not in self._cache:
            self.load_if_changed()
        return self._cache.get('project', {})

    def get_app_data(self):
        """获取应用数据"""
        if 'app' not in self._cache:
            self.load_if_changed()
        return self._cache.get('app', {})

    def get_test_data(self):
        """获取测试数据"""
        if 'test' not in self._cache:
            self.load_if_changed()
        return self._cache.get('test', {})

    def get_all_data(self):
        """获取所有数据"""
        self.load_if_changed()
        return {
            'project': self.get_project_data(),
            'app': self.get_app_data(),
            'test': self.get_test_data(),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


# 创建Flask应用
app = Flask(__name__)

# 全局数据管理器
data_manager = None


def get_dashboard_html():
    """获取仪表板HTML模板"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>开发阶段可观测系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
                         'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .auto-refresh {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 15px;
            font-size: 0.9em;
        }

        .content {
            padding: 30px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }

        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }

        .info-item {
            margin-bottom: 10px;
            padding: 8px;
            background: white;
            border-radius: 5px;
        }

        .info-label {
            font-weight: bold;
            color: #555;
            margin-right: 8px;
        }

        .info-value {
            color: #333;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
        }

        .status-not_started { background: #e9ecef; color: #6c757d; }
        .status-in_progress { background: #cce5ff; color: #004085; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-delayed { background: #f8d7da; color: #721c24; }

        .status-pending { background: #fff3cd; color: #856404; }
        .status-developed { background: #cce5ff; color: #004085; }
        .status-confirmed { background: #d4edda; color: #155724; }
        .status-optimized { background: #d1ecf1; color: #0c5460; }

        .priority-low { background: #d4edda; color: #155724; }
        .priority-medium { background: #fff3cd; color: #856404; }
        .priority-high { background: #f8d7da; color: #721c24; }
        .priority-critical { background: #dc3545; color: white; }

        .table-container {
            overflow-x: auto;
            margin-top: 15px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 5px;
            overflow: hidden;
        }

        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .progress-bar {
            background: #e9ecef;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }

        .progress-text {
            text-align: center;
            font-size: 0.85em;
            color: white;
            line-height: 20px;
        }

        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        .anomaly-card {
            border-left-color: #dc3545;
        }

        .severity-low { background: #d4edda; color: #155724; }
        .severity-medium { background: #fff3cd; color: #856404; }
        .severity-high { background: #f8d7da; color: #721c24; }
        .severity-critical { background: #dc3545; color: white; }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .refresh-btn {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            margin-left: 15px;
            transition: all 0.3s ease;
        }

        .refresh-btn:hover {
            background: #667eea;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>开发阶段可观测系统</h1>
            <p id="project-name">加载中...</p>
            <div class="auto-refresh">
                最后更新: <span id="last-updated">-</span>
                <button class="refresh-btn" onclick="refreshData()">立即刷新</button>
                <span style="margin-left: 10px;">(每30秒自动刷新)</span>
            </div>
        </div>

        <div class="content">
            <!-- 摘要统计 -->
            <div class="section">
                <h2 class="section-title">项目摘要</h2>
                <div class="summary-stats" id="summary-stats">
                    <div class="loading">加载中...</div>
                </div>
            </div>

            <!-- 项目维度 -->
            <div class="section">
                <h2 class="section-title">项目维度</h2>
                <div class="card-grid" id="project-section">
                    <div class="loading">加载中...</div>
                </div>
            </div>

            <!-- 应用维度 -->
            <div class="section">
                <h2 class="section-title">应用维度</h2>
                <div class="card-grid" id="app-section">
                    <div class="loading">加载中...</div>
                </div>
            </div>

            <!-- 测试维度 -->
            <div class="section">
                <h2 class="section-title">测试维度</h2>
                <div class="card-grid" id="test-section">
                    <div class="loading">加载中...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function getStatusClass(status) {
            const statusMap = {
                'not_started': 'status-not_started',
                'in_progress': 'status-in_progress',
                'completed': 'status-completed',
                'delayed': 'status-delayed',
                'pending': 'status-pending',
                'developed': 'status-developed',
                'confirmed': 'status-confirmed',
                'optimized': 'status-optimized'
            };
            return statusMap[status] || '';
        }

        function getPriorityClass(priority) {
            const priorityMap = {
                'low': 'priority-low',
                'medium': 'priority-medium',
                'high': 'priority-high',
                'critical': 'priority-critical'
            };
            return priorityMap[priority] || '';
        }

        function getSeverityClass(severity) {
            const severityMap = {
                'low': 'severity-low',
                'medium': 'severity-medium',
                'high': 'severity-high',
                'critical': 'severity-critical'
            };
            return severityMap[severity] || '';
        }

        function renderSummary(data) {
            const project = data.project;
            const app = data.app;
            const test = data.test;

            const totalIterations = project.iterations.length;
            const totalTasks = project.iterations.reduce((sum, iter) => sum + iter.tasks.length, 0);
            const totalModules = app.modules.length;
            const avgCompletion = app.modules.reduce((sum, m) => sum + (m.completion_rate || 0), 0) / totalModules * 100;
            const totalTests = test.test_suites.reduce((sum, s) => sum + s.total_tests, 0);
            const totalPassed = test.test_suites.reduce((sum, s) => sum + s.passed_tests, 0);
            const testPassRate = totalTests > 0 ? (totalPassed / totalTests * 100).toFixed(1) : 0;
            const totalAnomalies = test.anomalies.length;

            document.getElementById('project-name').textContent = `${project.project_name} - ${app.app_name}`;
            document.getElementById('summary-stats').innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${totalIterations}</div>
                    <div class="stat-label">迭代总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${totalTasks}</div>
                    <div class="stat-label">任务总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${totalModules}</div>
                    <div class="stat-label">模块总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${avgCompletion.toFixed(1)}%</div>
                    <div class="stat-label">平均完成率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${testPassRate}%</div>
                    <div class="stat-label">测试通过率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${totalAnomalies}</div>
                    <div class="stat-label">异常总数</div>
                </div>
            `;
        }

        function renderProjectSection(project) {
            const iterations = project.iterations.map(iter => {
                const taskStatus = {};
                iter.tasks.forEach(task => {
                    taskStatus[task.status] = (taskStatus[task.status] || 0) + 1;
                });

                const tasksHtml = iter.tasks.map(task => `
                    <div class="info-item">
                        <div><span class="info-label">任务:</span><span class="info-value">${task.task_name}</span></div>
                        <div style="margin-top: 5px;">
                            <span class="status-badge ${getStatusClass(task.status)}">${task.status}</span>
                            ${task.priority ? `<span class="status-badge ${getPriorityClass(task.priority)}" style="margin-left: 5px;">${task.priority}</span>` : ''}
                            ${task.assignee ? `<span class="info-label" style="margin-left: 10px;">负责人: ${task.assignee}</span>` : ''}
                        </div>
                    </div>
                `).join('');

                const assumptionsHtml = iter.assumptions && iter.assumptions.length > 0 ? `
                    <div style="margin-top: 15px;">
                        <h4 style="margin-bottom: 10px;">开发假设</h4>
                        ${iter.assumptions.map(assump => `
                            <div class="info-item">
                                <div><span class="info-label">假设:</span><span class="info-value">${assump.description}</span></div>
                                <div style="margin-top: 5px;">
                                    <span class="status-badge ${getStatusClass(assump.status)}">${assump.status}</span>
                                    ${assump.validation_date ? `<span class="info-label" style="margin-left: 10px;">验证日期: ${assump.validation_date}</span>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '';

                return `
                    <div class="card">
                        <h3>${iter.iteration_name}</h3>
                        <div class="info-item">
                            <span class="info-label">迭代ID:</span><span class="info-value">${iter.iteration_id}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">状态:</span>
                            <span class="status-badge ${getStatusClass(iter.status)}">${iter.status}</span>
                        </div>
                        ${iter.start_date ? `
                            <div class="info-item">
                                <span class="info-label">时间:</span>
                                <span class="info-value">${iter.start_date} ~ ${iter.end_date || '进行中'}</span>
                            </div>
                        ` : ''}
                        <div class="info-item">
                            <span class="info-label">任务统计:</span>
                            <span class="info-value">${JSON.stringify(taskStatus)}</span>
                        </div>
                        <div style="margin-top: 15px;">
                            <h4 style="margin-bottom: 10px;">任务列表 (${iter.tasks.length})</h4>
                            ${tasksHtml}
                        </div>
                        ${assumptionsHtml}
                    </div>
                `;
            }).join('');

            document.getElementById('project-section').innerHTML = iterations;
        }

        function renderAppSection(app) {
            const moduleStats = {};
            app.modules.forEach(m => {
                moduleStats[m.status] = (moduleStats[m.status] || 0) + 1;
            });

            const modulesHtml = app.modules.map(m => `
                <div class="card">
                    <h3>${m.module_name}</h3>
                    <div class="info-item">
                        <span class="info-label">状态:</span>
                        <span class="status-badge ${getStatusClass(m.status)}">${m.status}</span>
                    </div>
                    ${m.owner ? `
                        <div class="info-item">
                            <span class="info-label">负责人:</span><span class="info-value">${m.owner}</span>
                        </div>
                    ` : ''}
                    <div class="info-item">
                        <span class="info-label">完成率:</span>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${(m.completion_rate || 0) * 100}%">
                                <span class="progress-text">${((m.completion_rate || 0) * 100).toFixed(1)}%</span>
                            </div>
                        </div>
                    </div>
                    ${m.last_update ? `
                        <div class="info-item">
                            <span class="info-label">最后更新:</span><span class="info-value">${m.last_update}</span>
                        </div>
                    ` : ''}
                    ${m.notes ? `
                        <div class="info-item">
                            <span class="info-label">备注:</span><span class="info-value">${m.notes}</span>
                        </div>
                    ` : ''}
                </div>
            `).join('');

            const statsHtml = `
                <div class="card">
                    <h3>模块状态统计</h3>
                    ${Object.entries(moduleStats).map(([status, count]) => `
                        <div class="info-item">
                            <span class="status-badge ${getStatusClass(status)}">${status}</span>
                            <span class="info-value" style="margin-left: 10px;">${count} 个模块</span>
                        </div>
                    `).join('')}
                </div>
            `;

            document.getElementById('app-section').innerHTML = statsHtml + modulesHtml;
        }

        function renderTestSection(test) {
            const suitesHtml = test.test_suites.map(suite => {
                const passRate = suite.total_tests > 0 ? (suite.passed_tests / suite.total_tests * 100).toFixed(1) : 0;
                return `
                    <div class="card">
                        <h3>${suite.suite_name}</h3>
                        <div class="info-item">
                            <span class="info-label">总计:</span><span class="info-value">${suite.total_tests}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">通过:</span><span class="info-value">${suite.passed_tests}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">失败:</span><span class="info-value">${suite.failed_tests}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">跳过:</span><span class="info-value">${suite.skipped_tests}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">通过率:</span><span class="info-value">${passRate}%</span>
                        </div>
                        ${suite.coverage !== undefined ? `
                            <div class="info-item">
                                <span class="info-label">覆盖率:</span><span class="info-value">${(suite.coverage * 100).toFixed(1)}%</span>
                            </div>
                        ` : ''}
                        <div class="info-item">
                            <span class="info-label">最后运行:</span><span class="info-value">${suite.last_run}</span>
                        </div>
                    </div>
                `;
            }).join('');

            const tracingPointsHtml = `
                <div class="card">
                    <h3>埋点状态</h3>
                    ${test.tracing_points.map(p => `
                        <div class="info-item">
                            <div><span class="info-label">模块:</span><span class="info-value">${p.module}</span></div>
                            <div><span class="info-label">位置:</span><span class="info-value">${p.location}</span></div>
                            <div style="margin-top: 5px;">
                                <span class="status-badge ${getStatusClass(p.status)}">${p.status}</span>
                                <span class="status-badge" style="margin-left: 5px;">${p.metric_type}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            const anomaliesHtml = test.anomalies.length > 0 ? `
                <div class="card anomaly-card">
                    <h3>异常列表 (${test.anomalies.length})</h3>
                    ${test.anomalies.map(a => `
                        <div class="info-item">
                            <div><span class="info-label">类型:</span><span class="info-value">${a.type}</span></div>
                            <div><span class="info-label">描述:</span><span class="info-value">${a.description}</span></div>
                            <div style="margin-top: 5px;">
                                <span class="status-badge ${getSeverityClass(a.severity)}">${a.severity}</span>
                                <span class="status-badge ${getStatusClass(a.status)}" style="margin-left: 5px;">${a.status}</span>
                            </div>
                            <div><span class="info-label">发生次数:</span><span class="info-value">${a.occurrence_count}</span></div>
                            <div><span class="info-label">时间:</span><span class="info-value">${a.first_occurred} ~ ${a.last_occurred}</span></div>
                        </div>
                    `).join('')}
                </div>
            ` : `
                <div class="card">
                    <h3>异常列表</h3>
                    <div class="info-item">
                        <span class="info-value">无异常</span>
                    </div>
                </div>
            `;

            document.getElementById('test-section').innerHTML = suitesHtml + tracingPointsHtml + anomaliesHtml;
        }

        function refreshData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('last-updated').textContent = data.last_updated;
                    renderSummary(data);
                    renderProjectSection(data.project);
                    renderAppSection(data.app);
                    renderTestSection(data.test);
                })
                .catch(error => {
                    console.error('加载数据失败:', error);
                });
        }

        // 初始加载
        refreshData();

        // 自动刷新（30秒）
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
    """


@app.route('/')
def index():
    """首页"""
    return render_template_string(get_dashboard_html())


@app.route('/api/data')
def get_data():
    """获取可观测数据API"""
    return jsonify(data_manager.get_all_data())


def main():
    global data_manager

    parser = argparse.ArgumentParser(description='可观测Web服务器（中等方案）')
    parser.add_argument('--project', required=True, help='项目数据文件路径')
    parser.add_argument('--app', required=True, help='应用状态文件路径')
    parser.add_argument('--test', required=True, help='测试指标文件路径')
    parser.add_argument('--output', default='observability.log', help='可观测日志文件路径（与简单方案保持一致）')
    parser.add_argument('--host', default='127.0.0.1', help='服务器地址')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口')

    args = parser.parse_args()

    # 验证文件存在
    for file_path in [args.project, args.app, args.test]:
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在: {file_path}")
            exit(1)

    # 初始化数据管理器
    data_manager = ObservabilityData(args.project, args.app, args.test)

    # 生成初始的可观测日志（与简单方案格式保持一致）
    def generate_observability_log():
        """生成可观测日志"""
        data = data_manager.get_all_data()

        log_content = f"""{'='*80}
开发阶段可观测日志
{'='*80}
生成时间: {data['last_updated']}
部署方案: 中等方案（Web界面）

{'='*80}
一、项目维度
{'='*80}

当前迭代: {data['project'].get('current_iteration', 'N/A')}
迭代状态: {data['project'].get('status', 'N/A')}
开始时间: {data['project'].get('start_date', 'N/A')}
结束时间: {data['project'].get('end_date', 'N/A')}

任务统计:
"""
        tasks = data['project'].get('tasks', [])
        todo_count = len([t for t in tasks if t.get('status') == 'todo'])
        in_progress_count = len([t for t in tasks if t.get('status') == 'in-progress'])
        completed_count = len([t for t in tasks if t.get('status') == 'completed'])

        log_content += f"  待办: {todo_count}\n"
        log_content += f"  进行中: {in_progress_count}\n"
        log_content += f"  已完成: {completed_count}\n\n"

        assumptions = data['project'].get('assumptions', [])
        log_content += f"开发假设: {len(assumptions)} 个\n"
        for assump in assumptions[:5]:
            log_content += f"  - {assump.get('assumption_id', 'N/A')}: {assump.get('description', 'N/A')}\n"
        log_content += "\n"

        log_content += f"""
{'='*80}
二、应用维度
{'='*80}

模块总数: {len(data['app'].get('modules', []))}
"""

        for module in data['app'].get('modules', [])[:10]:
            log_content += f"\n模块: {module.get('name', 'N/A')}\n"
            log_content += f"  状态: {module.get('status', 'N/A')}\n"
            log_content += f"  描述: {module.get('description', 'N/A')}\n"
            log_content += f"  最后更新: {module.get('last_updated', 'N/A')}\n"

        log_content += f"""
{'='*80}
三、测试维度
{'='*80}

测试覆盖:
"""
        coverage = data['test'].get('test_coverage', {})
        log_content += f"  总测试数: {coverage.get('total_tests', 0)}\n"
        log_content += f"  通过数: {coverage.get('passed', 0)}\n"
        log_content += f"  失败数: {coverage.get('failed', 0)}\n"
        log_content += f"  通过率: {coverage.get('pass_rate', 0):.1f}%\n\n"

        anomalies = data['test'].get('anomalies', [])
        log_content += f"异常检测: {len(anomalies)} 条\n"
        for anomaly in anomalies[:5]:
            log_content += f"  - {anomaly.get('type', 'N/A')}: {anomaly.get('description', 'N/A')}\n"

        log_content += f"""
{'='*80}
四、访问信息
{'='*80}

Web界面访问: http://{args.host}:{args.port}
日志文件路径: {os.path.abspath(args.output)}
自动刷新: 是（每30秒）
"""

        return log_content

    # 初始生成日志
    print(f"生成可观测日志: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(generate_observability_log())

    # 定期更新日志
    import threading

    def update_log_periodically():
        """定期更新日志"""
        while True:
            time.sleep(30)  # 每30秒更新一次
            try:
                if data_manager.load_if_changed():
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(generate_observability_log())
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 可观测日志已更新")
            except Exception as e:
                print(f"更新日志失败: {e}")

    # 启动日志更新线程
    log_thread = threading.Thread(target=update_log_periodically, daemon=True)
    log_thread.start()

    # 启动服务器
    print(f"启动可观测Web服务器...")
    print(f"项目数据: {args.project}")
    print(f"应用数据: {args.app}")
    print(f"测试数据: {args.test}")
    print(f"可观测日志: {args.output}")
    print(f"访问地址: http://{args.host}:{args.port}")
    print(f"按 Ctrl+C 停止服务器")

    app.run(host=args.host, port=args.port, debug=False, threaded=True)


if __name__ == '__main__':
    main()
