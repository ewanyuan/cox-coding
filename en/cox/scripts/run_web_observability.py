#!/usr/bin/env python3
"""
Modern Observability Dashboard (Static & Web Modes)
现代化可观测仪表板 - 支持静态生成和 Web 交互两种模式

使用方法:
  静态模式（无需 Flask）: python run_web_observability.py --mode static --project ... --app ... --test ... --output observability.html
  Web 模式（需要 Flask）: python run_web_observability.py --mode web --project ... --app ... --test ...
"""

import json
import os
import sys
import io
import argparse
import time
from pathlib import Path
from datetime import datetime

# 尝试导入 Flask，如果失败则提示用户
try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# 修复 Windows 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ObservabilityData:
    """可观测数据管理 (已优化)"""
    def __init__(self, project_file, app_file, test_file):
        self.files = {
            'project': project_file,
            'app': app_file,
            'test': test_file
        }
        self.last_modified = {}
        self._cache = {}

    def load_if_changed(self):
        changed = False
        for name, path in self.files.items():
            try:
                mtime = os.path.getmtime(path)
                if name not in self.last_modified or mtime > self.last_modified[name]:
                    self.last_modified[name] = mtime
                    with open(path, 'r', encoding='utf-8') as f:
                        self._cache[name] = json.load(f)
                    changed = True
            except Exception as e:
                print(f"Error loading {path}: {e}")
        return changed

    def get_all_data(self):
        self.load_if_changed()
        return {
            'project': self._cache.get('project', {}),
            'app': self._cache.get('app', {}),
            'test': self._cache.get('test', {}),
            'last_updated': datetime.now().strftime('%H:%M:%S')
        }


# 全局变量
data_manager = None
app = None

# Flask 应用和路由（仅 Web 模式使用）
if FLASK_AVAILABLE:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template_string(get_dashboard_html('web'))

    @app.route('/api/data')
    def get_data():
        return jsonify(data_manager.get_all_data())

    @app.route('/api/update/module', methods=['POST'])
    def update_module_status():
        """更新模块状态和问题描述（仅交互模式）"""
        try:
            data = request.json
            module_name = data.get('module_name')
            new_status = data.get('status')
            issue_description = data.get('issue_description', '')
            
            # 读取 app_status.json
            with open(data_manager.files['app'], 'r', encoding='utf-8') as f:
                app_data = json.load(f)
            
            # 更新模块状态
            for module in app_data['modules']:
                if module['module_name'] == module_name:
                    module['status'] = new_status
                    if new_status == 'has_issue':
                        module['issue_description'] = issue_description
                    else:
                        module['issue_description'] = ''
                    break
            
            # 更新 last_updated
            app_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 写回文件
            with open(data_manager.files['app'], 'w', encoding='utf-8') as f:
                json.dump(app_data, f, ensure_ascii=False, indent=2)
            
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/api/update/assumption', methods=['POST'])
    def update_assumption_status():
        """更新假设状态（仅交互模式）"""
        try:
            import base64
            data = request.json
            assumption_id = data.get('assumption_id')
            new_status = data.get('status')

            # 读取 project_data.json
            with open(data_manager.files['project'], 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            # 更新假设状态
            for iteration in project_data['iterations']:
                for assumption in iteration.get('assumptions', []):
                    # 优先使用 assumption_id 匹配，如果没有则尝试解码 base64 并匹配 hypothesis/description/assumption_text
                    match_found = False

                    if 'assumption_id' in assumption and assumption['assumption_id'] == assumption_id:
                        match_found = True
                    else:
                        # 尝试解码 base64 并匹配假设内容
                        try:
                            decoded_id = base64.b64decode(assumption_id).decode('utf-8')
                            hypothesis_content = assumption.get('hypothesis') or assumption.get('description') or assumption.get('assumption_text')
                            if hypothesis_content == decoded_id:
                                match_found = True
                        except:
                            pass

                    if match_found:
                        assumption['status'] = new_status
                        if new_status == 'validated':
                            assumption['validation_date'] = datetime.now().strftime('%Y-%m-%d')
                        else:
                            assumption['validation_date'] = None
                        break

            # 写回文件
            with open(data_manager.files['project'], 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)

            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

def get_dashboard_html(mode='static'):
    """现代化 UI 模板 - 采用 Tailwind CSS 和 Lucid Icons (中文默认 & 语言切换)"""
    return """
<!DOCTYPE html>
<html lang="zh-CN" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cox coding-透明流畅的交互体验</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', 'Noto Sans SC', sans-serif;
            background-color: #09090b;
            color: #fafafa;
        }
        .glass-card {
            background: rgba(24, 24, 27, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(39, 39, 42, 1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            border-color: rgba(63, 63, 70, 1);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }
        .gradient-text {
            background: linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #09090b; }
        ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 10px; }
        .hidden { display: none; }
    </style>
</head>
<body class="p-6 lg:p-10">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-6">
            <div>
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-blue-600 rounded-lg">
                        <i data-lucide="activity" class="w-6 h-6 text-white"></i>
                    </div>
                    <h1 class="text-3xl font-bold tracking-tight text-white" id="app-title">Cox coding-透明流畅的交互体验</h1>
                </div>
                <p class="text-zinc-400 font-medium" id="project-info">正在获取项目状态...</p>
            </div>
            
            <div class="flex items-center gap-4">
                <!-- 语言切换 -->
                <div class="flex bg-zinc-900/80 rounded-lg p-1 border border-zinc-800">
                    <button onclick="setLanguage('zh')" id="lang-zh" class="px-3 py-1.5 rounded-md text-xs font-bold transition-all bg-blue-600 text-white">中文</button>
                    <button onclick="setLanguage('en')" id="lang-en" class="px-3 py-1.5 rounded-md text-xs font-bold transition-all text-zinc-500 hover:text-white">EN</button>
                </div>

                <div class="flex items-center gap-4 bg-zinc-900/50 p-2 rounded-xl border border-zinc-800">
                    <div class="px-4 py-2 border-r border-zinc-800">
                        <p class="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-1" id="label-last-update">最后更新</p>
                        <p class="text-sm font-mono text-emerald-400" id="last-updated">00:00:00</p>
                    </div>
                    <button onclick="refreshData()" class="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg font-semibold hover:bg-zinc-200 transition-colors">
                        <i data-lucide="refresh-cw" class="w-4 h-4" id="refresh-icon"></i>
                        <span id="btn-refresh">刷新</span>
                    </button>
                </div>
            </div>
        </header>

        <!-- Top Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10" id="top-metrics">
            <!-- 动态内容 -->
        </div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Left Column: Tasks & Progress -->
            <div class="lg:col-span-8 space-y-6">
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-lg font-bold flex items-center gap-2">
                            <i data-lucide="git-merge" class="text-blue-400"></i> 
                            <span id="title-tasks">迭代管理</span>
                        </h2>
                        <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-1 rounded" id="task-count">0 迭代</span>
                    </div>
                    <div class="space-y-3" id="task-list">
                        <!-- 动态内容 -->
                    </div>
                </div>

                <div class="glass-card rounded-2xl p-6">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                        <i data-lucide="layers" class="text-emerald-400"></i> 
                        <span id="title-modules">模块成熟度</span>
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="module-grid">
                        <!-- 动态内容 -->
                    </div>
                </div>
            </div>

            <!-- Right Column: Tests & Anomalies -->
            <div class="lg:col-span-4 space-y-6">
                <div class="glass-card rounded-2xl p-6 border-l-4 border-l-amber-500">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                        <i data-lucide="shield-check" class="text-amber-500"></i> 
                        <span id="title-coverage">测试覆盖率</span>
                    </h2>
                    <div class="space-y-6" id="test-suites">
                        <!-- 动态内容 -->
                    </div>
                </div>

                <div class="glass-card rounded-2xl p-6 bg-red-500/5 border-red-500/20">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-4 text-red-400">
                        <i data-lucide="alert-triangle"></i> 
                        <span id="title-anomalies">活跃异常</span>
                    </h2>
                    <div class="space-y-3" id="anomaly-list">
                        <!-- 动态内容 -->
                    </div>
                </div>
            </div>
        </div>

        <!-- New Features Section -->
        <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="glass-card rounded-2xl p-6">
                <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                    <i data-lucide="lightbulb" class="text-yellow-400"></i> 
                    <span id="title-assumptions">假设验证分析</span>
                </h2>
                <div class="space-y-3" id="assumptions-list">
                    <!-- 动态内容 -->
                </div>
            </div>

            <div class="glass-card rounded-2xl p-6 lg:col-span-1" id="performance-section">
                <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                    <i data-lucide="trending-up" class="text-green-400"></i> 
                    <span id="title-perf">性能趋势</span>
                </h2>
                <div id="performance-chart" class="h-48">
                    <canvas id="perf-canvas"></canvas>
                </div>
            </div>

            <div class="glass-card rounded-2xl p-6 lg:col-span-1" id="team-section">
                <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                    <i data-lucide="users" class="text-purple-400"></i> 
                    <span id="title-team">团队概览</span>
                </h2>
                <div class="space-y-4" id="team-list">
                    <!-- 动态内容 -->
                </div>
            </div>
        </div>
    </div>

    <script>
        // 语言字典
        const translations = {
            zh: {
                appTitle: 'Cox coding-透明流畅的交互体验',
                lastUpdate: '最后更新',
                refresh: '刷新',
                iterations: '迭代管理',
                modules: '模块成熟度',
                coverage: '测试覆盖率',
                anomalies: '活跃异常',
                assumptions: '假设验证分析',
                perf: '性能趋势',
                team: '团队概览',
                metricIterations: '迭代周期',
                metricTasks: '任务总数',
                metricPassRate: '测试通过率',
                metricAnomalies: '系统异常',
                unassigned: '未分配',
                completeSuffix: '完成',
                healthy: '系统状态良好',
                noAssumptions: '暂无跟踪的假设',
                noTeam: '暂无团队数据',
                noPerf: '无可用性能数据',
                status: {
                    completed: '已完成',
                    done: '已完成',
                    in_progress: '进行中',
                    todo: '待处理',
                    not_started: '未开始',
                    delayed: '延期',
                    critical: '紧急',
                    validated: '已验证',
                    invalidated: '已失效',
                    pending: '待定',
                    confirmed: '待确认',
                    optimized: '完美',
                    has_issue: '有问题',
                    unverifiable: '无法验证',
                    confirmed_true: '这是真的',
                    confirmed_false: '这是假的',
                    uncertain: '我不确定'
                }
            },
            en: {
                appTitle: 'Cox coding - Transparent & Smooth Interactive Experience',
                lastUpdate: 'LAST UPDATE',
                refresh: 'Refresh',
                iterations: 'Iterations',
                modules: 'Module Maturity',
                coverage: 'Test Coverage',
                anomalies: 'Active Anomalies',
                assumptions: 'Assumptions Analysis',
                perf: 'Performance Trends',
                team: 'Team Overview',
                metricIterations: 'Iterations',
                metricTasks: 'Total Tasks',
                metricPassRate: 'Test Pass Rate',
                metricAnomalies: 'Anomalies',
                unassigned: 'Unassigned',
                completeSuffix: 'Complete',
                healthy: 'System Healthy',
                noAssumptions: 'No assumptions tracked',
                noTeam: 'No team data available',
                noPerf: 'No performance data available',
                status: {
                    completed: 'Done',
                    done: 'Done',
                    in_progress: 'In Progress',
                    todo: 'Pending',
                    not_started: 'Pending',
                    delayed: 'Delayed',
                    critical: 'Critical',
                    validated: 'Validated',
                    invalidated: 'Invalid',
                    pending: 'Pending',
                    confirmed: 'Confirmed',
                    optimized: 'Perfect',
                    has_issue: 'Has Issue',
                    unverifiable: 'Unverifiable',
                    confirmed_true: 'Confirmed True',
                    confirmed_false: 'Confirmed False',
                    uncertain: 'Uncertain'
                }
            }
        };

        let currentLang = 'zh';

        function setLanguage(lang) {
            currentLang = lang;
            
            // 更新按钮样式
            const btnZh = document.getElementById('lang-zh');
            const btnEn = document.getElementById('lang-en');
            if(lang === 'zh') {
                btnZh.className = "px-3 py-1.5 rounded-md text-xs font-bold transition-all bg-blue-600 text-white";
                btnEn.className = "px-3 py-1.5 rounded-md text-xs font-bold transition-all text-zinc-500 hover:text-white";
                document.documentElement.lang = "zh-CN";
            } else {
                btnEn.className = "px-3 py-1.5 rounded-md text-xs font-bold transition-all bg-blue-600 text-white";
                btnZh.className = "px-3 py-1.5 rounded-md text-xs font-bold transition-all text-zinc-500 hover:text-white";
                document.documentElement.lang = "en";
            }

            // 更新静态文本
            const t = translations[lang];
            document.getElementById('app-title').textContent = t.appTitle;
            document.getElementById('label-last-update').textContent = t.lastUpdate;
            document.getElementById('btn-refresh').textContent = t.refresh;
            document.getElementById('title-tasks').textContent = t.tasks;
            document.getElementById('title-modules').textContent = t.modules;
            document.getElementById('title-coverage').textContent = t.coverage;
            document.getElementById('title-anomalies').textContent = t.anomalies;
            document.getElementById('title-assumptions').textContent = t.assumptions;
            document.getElementById('title-perf').textContent = t.perf;
            document.getElementById('title-team').textContent = t.team;

            // 重新渲染UI
            if(window.lastData) renderUI(window.lastData);
        }

        const statusConfig = {
            'completed': { bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
            'done': { bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
            'in_progress': { bg: 'bg-blue-500/10', text: 'text-blue-400' },
            'todo': { bg: 'bg-zinc-800', text: 'text-zinc-400' },
            'not_started': { bg: 'bg-zinc-800', text: 'text-zinc-400' },
            'delayed': { bg: 'bg-red-500/10', text: 'text-red-400' },
            'critical': { bg: 'bg-red-500', text: 'text-white' },
            'validated': { bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
            'invalidated': { bg: 'bg-red-500/10', text: 'text-red-400' },
            'pending': { bg: 'bg-yellow-500/10', text: 'text-yellow-400' },
            'confirmed': { bg: 'bg-blue-500/10', text: 'text-blue-400' },
            'optimized': { bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
            'has_issue': { bg: 'bg-red-500/10', text: 'text-red-400' },
            'unverifiable': { bg: 'bg-zinc-700', text: 'text-zinc-400' },
            'confirmed_true': { bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
            'confirmed_false': { bg: 'bg-red-500/10', text: 'text-red-400' },
            'uncertain': { bg: 'bg-yellow-500/10', text: 'text-yellow-400' }
        };

        // Priority 和 Risk Level 翻译配置
        const priorityLabels = {
            'zh': { 'critical': '紧急', 'high': '高', 'medium': '中', 'low': '低' },
            'en': { 'critical': 'Critical', 'high': 'High', 'medium': 'Medium', 'low': 'Low' }
        };
        
        const riskLabels = {
            'zh': { 'high': '大风险', 'low': '小风险' },
            'en': { 'high': 'High Risk', 'low': 'Low Risk' }
        };
        
        function getPriorityLabel(priority) {
            return priorityLabels[currentLang][priority] || priority;
        }
        
        function getRiskLabel(risk) {
            return riskLabels[currentLang][risk] || risk;
        }

                function getStatusBadge(status) {
            const key = status.toLowerCase();
            const cfg = statusConfig[key] || { bg: 'bg-zinc-800', text: 'text-zinc-400' };
            const label = translations[currentLang].status[key] || status;
            return `<span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${cfg.bg} ${cfg.text}">${label}</span>`;
        }

        // 迭代折叠状态管理
        let collapsedIterations = new Set();

        function toggleIteration(iterationId) {
            if (collapsedIterations.has(iterationId)) {
                collapsedIterations.delete(iterationId);
            } else {
                collapsedIterations.add(iterationId);
            }
            // 重新渲染 UI
            if(window.lastData) renderUI(window.lastData);
        }

        async function refreshData() {
            const btnIcon = document.getElementById('refresh-icon');
            if(btnIcon) btnIcon.classList.add('animate-spin');
            
            try {
                // Web 交互模式：从 Flask API 读取数据
                const response = await fetch('/api/data');
                const data = await response.json();
                window.lastData = data;
                renderUI(data);
            } catch (e) {
                console.error("Refresh failed", e);
            } finally {
                if(btnIcon) setTimeout(() => btnIcon.classList.remove('animate-spin'), 600);
            }
        }

        function renderUI(data) {
            try {
                const t = translations[currentLang];
                document.getElementById('last-updated').textContent = data.last_updated;
                const p = data.project;
                const a = data.app;
                const test = data.test;

                // 项目信息
                document.getElementById('project-info').textContent = `${p.project_name} • v${a.version || '1.0'}`;

                // 指标卡片
                const totalTasks = p.iterations.reduce((sum, iter) => sum + iter.tasks.length, 0);
                const passRate = test.test_suites.length ? (test.test_suites.reduce((s, x) => s + (x.passed_tests/x.total_tests), 0) / test.test_suites.length * 100).toFixed(0) : 0;
                const passRateDisplay = isNaN(parseFloat(passRate)) ? '暂未开放' : passRate + '%';
            
            document.getElementById('top-metrics').innerHTML = `
                ${renderMetricCard(t.metricIterations, p.iterations.length, 'milestone', 'text-blue-400')}
                ${renderMetricCard(t.metricTasks, totalTasks, 'check-circle', 'text-emerald-400')}
                ${renderMetricCard(t.metricPassRate, passRateDisplay, 'shield', 'text-amber-400')}
                ${renderMetricCard(t.metricAnomalies, test.anomalies.length, 'zap', 'text-red-400')}
            `;

            // 迭代列表（按迭代分组显示任务）
            document.getElementById('task-count').textContent = `${p.iterations.length} ${t.metricIterations}`;
            document.getElementById('task-list').innerHTML = p.iterations.map(iter => {
                const completedTasks = iter.tasks.filter(t => t.status === 'completed' || t.status === 'done').length;
                const progress = iter.tasks.length > 0 ? (completedTasks / iter.tasks.length * 100).toFixed(0) : 0;
                const isCurrent = iter.iteration_id === p.current_iteration;
                const isCollapsed = !isCurrent && collapsedIterations.has(iter.iteration_id);
                
                return `
                    <div class="bg-zinc-900/40 rounded-xl border ${isCurrent ? 'border-blue-500/30 bg-blue-500/5' : 'border-zinc-800/50'} overflow-hidden">
                        <!-- 迭代头部（可点击切换折叠/展开） -->
                        <div class="p-4 border-b border-zinc-800/50 cursor-pointer hover:bg-zinc-800/30 transition-colors" onclick="toggleIteration('${iter.iteration_id}')">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-3">
                                    ${isCurrent ? '<span class="text-xs bg-blue-500 text-white px-2 py-0.5 rounded font-medium">当前</span>' : ''}
                                    <i data-lucide="${isCollapsed ? 'chevron-right' : 'chevron-down'}" class="w-4 h-4 text-zinc-500 transition-transform"></i>
                                    <h3 class="font-bold text-base text-zinc-200">${iter.iteration_name}</h3>
                                </div>
                                ${getStatusBadge(iter.status)}
                            </div>
                            <div class="flex items-center gap-4 text-xs text-zinc-500">
                                <span><i data-lucide="calendar" class="w-3 h-3 inline mr-1"></i>${iter.start_date || '-'} ~ ${iter.end_date || '-'}</span>
                                <span><i data-lucide="hash" class="w-3 h-3 inline mr-1"></i>${iter.iteration_id}</span>
                            </div>
                        </div>
                        
                        <!-- 迭代进度和任务列表（折叠时隐藏） -->
                        <div class="${isCollapsed ? 'hidden' : ''}">
                            <!-- 迭代进度 -->
                            <div class="px-4 py-3 bg-zinc-900/20">
                                <div class="flex items-center justify-between text-xs mb-1">
                                    <span class="text-zinc-400">任务进度</span>
                                    <span class="text-zinc-300">${completedTasks}/${iter.tasks.length} 已完成 (${progress}%)</span>
                                </div>
                                <div class="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-gradient-to-r from-blue-500 to-emerald-500 h-full transition-all duration-500" style="width: ${progress}%"></div>
                                </div>
                            </div>
                            
                            <!-- 任务列表 -->
                            <div class="p-4 space-y-2">
                                ${iter.tasks.length > 0 ? iter.tasks.map(task => `
                                    <div class="flex items-center justify-between p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/30 hover:border-zinc-700/50 transition-colors">
                                        <div class="flex items-center gap-3">
                                            <div class="w-1.5 h-6 rounded-full ${task.status === 'completed' || task.status === 'done' ? 'bg-emerald-500' : task.status === 'in_progress' ? 'bg-blue-500' : 'bg-zinc-600'}"></div>
                                            <div class="flex-1">
                                                <p class="font-medium text-sm text-zinc-200">${task.task_name}</p>
                                                <div class="flex items-center gap-3 mt-1 text-xs text-zinc-500">
                                                    <span>${task.task_id}</span>
                                                    ${task.assignee ? `<span><i data-lucide="user" class="w-3 h-3 inline mr-1"></i>${task.assignee}</span>` : ''}
                                                    ${task.priority ? `<span class="px-1.5 py-0.5 rounded ${task.priority === 'high' || task.priority === 'critical' ? 'bg-red-500/10 text-red-400' : 'bg-zinc-700/50 text-zinc-400'}">${getPriorityLabel(task.priority)}</span>` : ''}
                                                    ${task.risk_level ? `<span class="px-1.5 py-0.5 rounded ${task.risk_level === 'high' ? 'bg-orange-500/10 text-orange-400' : 'bg-emerald-500/10 text-emerald-400'}">${getRiskLabel(task.risk_level)}</span>` : ''}
                                                </div>
                                            </div>
                                        </div>
                                        ${getStatusBadge(task.status)}
                                    </div>
                                `).join('') : '<p class="text-sm text-zinc-500 text-center py-4">尚未详细计划</p>'}
                            </div>
                        </div>
                        </div>
                        
                        <!-- 涉及的模块（折叠时也显示） -->
                        ${iter.modules && iter.modules.length > 0 ? `
                            <div class="px-4 py-3 border-t border-zinc-800/50">
                                <div class="flex items-center gap-2 text-xs text-zinc-500 mb-2">
                                    <i data-lucide="layers" class="w-3 h-3"></i>
                                    <span>涉及的模块 (${iter.modules.length})</span>
                                </div>
                                <div class="flex flex-wrap gap-2">
                                    ${iter.modules.map(mod => `
                                        <div class="px-3 py-1.5 bg-zinc-900/60 rounded-lg border border-zinc-800/50">
                                            <p class="text-xs font-medium text-zinc-300">${mod.module_name}</p>
                                            <p class="text-[10px] text-zinc-500 mt-0.5">预期完成率: ${(mod.expected_completion * 100).toFixed(0)}%</p>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                        
                        <!-- 开发假设（折叠时也显示） -->
                        ${iter.assumptions && iter.assumptions.length > 0 ? `
                            <div class="px-4 py-3 border-t border-zinc-800/50">
                                <div class="flex items-center gap-2 text-xs text-zinc-500 mb-2">
                                    <i data-lucide="lightbulb" class="w-3 h-3"></i>
                                    <span>开发假设 (${iter.assumptions.length})</span>
                                </div>
                                ${iter.assumptions.slice(0, 2).map(assump => {
                                    let status = assump.status;
                                    if (!status && assump.validated !== undefined) {
                                        status = assump.validated === true ? 'validated' : 'pending';
                                    }
                                    return `<div class="text-xs text-zinc-400 mb-1">
                                        <span class="${status === 'validated' ? 'text-emerald-400' : status === 'invalidated' ? 'text-red-400' : 'text-amber-400'}">●</span>
                                        ${assump.hypothesis || assump.description || assump.assumption_text || '无描述'}
                                    </div>`;
                                }).join('')}
                                ${iter.assumptions.length > 2 ? `<p class="text-xs text-zinc-500">...还有 ${iter.assumptions.length - 2} 个假设</p>` : ''}
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');

            // 模块成熟度（交互模式：只显示已宣称开发好的模块，支持状态更新）
            const developedModules = a.modules.filter(m => 
                m.status === 'confirmed' || 
                m.status === 'optimized' || 
                m.status === 'has_issue'
            );
            
            document.getElementById('module-grid').innerHTML = developedModules.map(m => `
                <div class="p-4 bg-zinc-900/40 rounded-xl border border-zinc-800/50" data-module="${m.module_name}">
                    <div class="flex justify-between items-start mb-3">
                        <p class="font-bold text-sm text-zinc-200">${m.module_name}</p>
                        ${renderModuleStatusSelect(m)}
                    </div>
                    <div class="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-blue-500 h-full" style="width: ${(m.completion_rate || 0)*100}%"></div>
                    </div>
                    <p class="text-[10px] text-zinc-500 mt-2 font-mono uppercase">${((m.completion_rate || 0)*100).toFixed(0)}% ${t.completeSuffix}</p>
                    ${m.status === 'has_issue' && m.issue_description ? `
                        <div class="mt-3 p-2 bg-red-500/10 rounded-lg border border-red-500/20">
                            <p class="text-xs text-red-400">问题描述：${m.issue_description}</p>
                        </div>
                    ` : ''}
                    ${window.showIssueInput === m.module_name ? `
                        <div class="mt-3">
                            <textarea id="issue-input-${m.module_name}" class="w-full p-2 bg-zinc-800 border border-zinc-700 rounded-lg text-xs text-zinc-200" rows="2" placeholder="请描述问题..."></textarea>
                            <button onclick="submitModuleIssue('${m.module_name}')" class="mt-2 px-3 py-1 bg-red-500 text-white text-xs rounded-lg hover:bg-red-600">提交问题</button>
                            <button onclick="cancelModuleIssue('${m.module_name}')" class="mt-2 ml-2 px-3 py-1 bg-zinc-700 text-zinc-300 text-xs rounded-lg hover:bg-zinc-600">取消</button>
                        </div>
                    ` : ''}
                </div>
            `).join('');

            // 测试套件
            document.getElementById('test-suites').innerHTML = test.test_suites.map(s => `
                <div>
                    <div class="flex justify-between text-sm mb-2 font-semibold">
                        <span>${s.suite_name}</span>
                        <span class="text-emerald-400">${(s.passed_tests/s.total_tests*100).toFixed(0)}%</span>
                    </div>
                    <div class="flex gap-1 h-2">
                        <div class="bg-emerald-500 rounded-l-sm" style="flex: ${s.passed_tests}"></div>
                        <div class="bg-red-500" style="flex: ${s.failed_tests}"></div>
                        <div class="bg-zinc-700 rounded-r-sm" style="flex: ${s.skipped_tests}"></div>
                    </div>
                </div>
            `).join('');

            // 异常
            document.getElementById('anomaly-list').innerHTML = test.anomalies.length
                ? test.anomalies.map(anom => `
                    <div class="p-3 bg-red-500/10 rounded-lg border border-red-500/20 text-xs">
                        <p class="font-bold text-red-400 mb-1 flex items-center justify-between">
                            ${anom.type}
                            <span class="opacity-50 font-normal">${anom.last_occurred.split(' ')[1]}</span>
                        </p>
                        <p class="text-zinc-400 line-clamp-1">${anom.description}</p>
                    </div>
                `).join('')
                : `<p class="text-zinc-500 text-sm text-center py-4">${t.healthy}</p>`;

            // 假设分析（交互模式：支持状态更新）
            const allAssumptions = p.iterations.flatMap(i => i.assumptions || []);
            document.getElementById('assumptions-list').innerHTML = allAssumptions.length
                ? allAssumptions.map(assump => `
                    <div class="p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/50">
                        <p class="text-sm font-semibold text-zinc-200 mb-2">${assump.hypothesis || assump.description || assump.assumption_text || '无描述'}</p>
                        <div class="flex items-center justify-between">
                            ${renderAssumptionStatusSelect(assump)}
                            ${assump.validation_date ? `<span class="text-[10px] text-zinc-500">${assump.validation_date}</span>` : ''}
                        </div>
                    </div>
                `).join('')
                : `<p class="text-zinc-500 text-sm text-center py-4">${t.noAssumptions}</p>`;

            // 性能趋势
            if (test.performance_history && test.performance_history.length > 0) {
                renderPerformanceChart(test.performance_history);
            } else {
                document.getElementById('performance-chart').innerHTML = `<p class="text-zinc-500 text-sm text-center py-8">${t.noPerf}</p>`;
            }

            // 团队概览
            const teamStats = analyzeTeamData(p, a);
            document.getElementById('team-list').innerHTML = Object.keys(teamStats).length
                ? Object.entries(teamStats).map(([member, stats]) => `
                    <div class="flex items-center justify-between p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/50">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">
                                <span class="text-sm font-bold text-purple-400">${member.charAt(0).toUpperCase()}</span>
                            </div>
                            <div>
                                <p class="text-sm font-semibold text-zinc-200">${member}</p>
                                <p class="text-[10px] text-zinc-500">${stats.tasks} tasks • ${stats.modules} modules</p>
                            </div>
                        </div>
                        <div class="text-right">
                            <p class="text-lg font-bold text-purple-400">${stats.completion}%</p>
                            <p class="text-[10px] text-zinc-500 uppercase">${t.completeSuffix}</p>
                        </div>
                    </div>
                `).join('')
                : `<p class="text-zinc-500 text-sm text-center py-4">${t.noTeam}</p>`;

            lucide.createIcons();
            
            // 根据数据情况隐藏无数据链路的板块（通过 CSS）
            // 测试覆盖率板块：所有套件的 total_tests 都为 0 时隐藏
            const hasRealTestData = test.test_suites.some(s => s.total_tests > 0);
            const coverageSection = document.querySelector('.border-l-amber-500');
            if(coverageSection) {
                if(!hasRealTestData) {
                    coverageSection.classList.add('hidden');
                } else {
                    coverageSection.classList.remove('hidden');
                }
            }
            
            // 团队概览板块：owner 通常为"待分配"时隐藏
            const hasRealTeamData = a.modules.some(m => m.owner && m.owner !== '待分配');
            const teamSection = document.getElementById('team-section');
            if(teamSection) {
                if(!hasRealTeamData) {
                    teamSection.classList.add('hidden');
                } else {
                    teamSection.classList.remove('hidden');
                }
            }
            
            // 性能趋势板块：无 performance_history 数据时隐藏
            const hasRealPerfData = test.performance_history && test.performance_history.length > 0;
            const perfSection = document.getElementById('performance-section');
            if(perfSection) {
                if(!hasRealPerfData) {
                    perfSection.classList.add('hidden');
                } else {
                    perfSection.classList.remove('hidden');
                }
            }
            
            } catch (e) {
                console.error("Render UI failed:", e);
                console.error("Data:", data);
            }
        }

        function analyzeTeamData(project, app) {
            const teamStats = {};
            project.iterations.forEach(iter => {
                iter.tasks.forEach(task => {
                    if (task.assignee) {
                        if (!teamStats[task.assignee]) teamStats[task.assignee] = { tasks: 0, modules: 0, completed: 0, total: 0 };
                        teamStats[task.assignee].tasks++;
                        teamStats[task.assignee].total++;
                        if (['done', 'completed'].includes(task.status.toLowerCase())) teamStats[task.assignee].completed++;
                    }
                });
            });
            app.modules.forEach(m => {
                if (m.owner) {
                    if (!teamStats[m.owner]) teamStats[m.owner] = { tasks: 0, modules: 0, completed: 0, total: 0 };
                    teamStats[m.owner].modules++;
                }
            });
            Object.keys(teamStats).forEach(member => {
                const s = teamStats[member];
                s.completion = s.total > 0 ? Math.round((s.completed / s.total) * 100) : 0;
            });
            return teamStats;
        }

        function renderPerformanceChart(perfHistory) {
            const canvas = document.getElementById('perf-canvas');
            if(!canvas) return;
            const ctx = canvas.getContext('2d');
            canvas.width = canvas.parentElement.offsetWidth;
            canvas.height = canvas.parentElement.offsetHeight;

            const metricName = perfHistory[0].metrics[0].name;
            const data = perfHistory.map(h => h.metrics[0].response_time);
            const labels = perfHistory.map(h => h.timestamp.split(' ')[1]);

            const padding = 40;
            const chartWidth = canvas.width - padding * 2;
            const chartHeight = canvas.height - padding * 2;
            const maxVal = Math.max(...data) * 1.2;
            const minVal = 0;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = '#27272a';
            ctx.lineWidth = 1;
            for (let i = 0; i <= 4; i++) {
                const y = padding + (chartHeight / 4) * i;
                ctx.beginPath(); ctx.moveTo(padding, y); ctx.lineTo(canvas.width - padding, y); ctx.stroke();
            }

            ctx.strokeStyle = '#22c55e';
            ctx.lineWidth = 2;
            ctx.beginPath();
            data.forEach((val, i) => {
                const x = padding + (chartWidth / (data.length - 1)) * i;
                const y = padding + chartHeight - ((val - minVal) / (maxVal - minVal)) * chartHeight;
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            });
            ctx.stroke();

            ctx.fillStyle = '#22c55e';
            data.forEach((val, i) => {
                const x = padding + (chartWidth / (data.length - 1)) * i;
                const y = padding + chartHeight - ((val - minVal) / (maxVal - minVal)) * chartHeight;
                ctx.beginPath(); ctx.arc(x, y, 4, 0, Math.PI * 2); ctx.fill();
            });

            ctx.fillStyle = '#71717a';
            ctx.font = '10px monospace';
            ctx.textAlign = 'center';
            labels.forEach((label, i) => {
                if (i % Math.ceil(labels.length / 5) === 0) {
                    const x = padding + (chartWidth / (labels.length - 1)) * i;
                    ctx.fillText(label, x, canvas.height - 10);
                }
            });
        }

        function renderMetricCard(label, value, icon, iconColor) {
            return `
                <div class="glass-card rounded-2xl p-5 flex items-center gap-5">
                    <div class="p-3 bg-zinc-900 rounded-xl">
                        <i data-lucide="${icon}" class="w-6 h-6 ${iconColor}"></i>
                    </div>
                    <div>
                        <p class="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-1">${label}</p>
                        <p class="text-2xl font-bold text-white">${value}</p>
                    </div>
                </div>
            `;
        }

        // 模块状态选择器（Web 交互模式）
        function renderModuleStatusSelect(module) {
            const isZh = currentLang === 'zh';
            const statusOptions = [
                { value: 'confirmed', label: isZh ? '待确认' : 'Confirmed' },
                { value: 'optimized', label: isZh ? '完美' : 'Perfect' },
                { value: 'has_issue', label: isZh ? '有问题' : 'Has Issue' }
            ];
            
            return `
                <select onchange="updateModuleStatus('${module.module_name}', this.value)" 
                        class="text-xs px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-zinc-300 focus:border-blue-500 focus:outline-none">
                    ${statusOptions.map(opt => 
                        `<option value="${opt.value}" ${module.status === opt.value ? 'selected' : ''}>${opt.label}</option>`
                    ).join('')}
                </select>
                ${module.status === 'has_issue' ? `
                    <button onclick="showModuleIssueInput('${module.module_name}')" 
                            class="ml-2 text-xs text-red-400 hover:text-red-300">
                        <i data-lucide="edit" class="w-3 h-3 inline"></i>
                    </button>
                ` : ''}
            `;
        }

        // 假设状态选择器（Web 交互模式）
        function renderAssumptionStatusSelect(assumption) {
            const isZh = currentLang === 'zh';
            const statusOptions = [
                { value: 'pending', label: isZh ? '待验证' : 'Pending' },
                { value: 'validated', label: isZh ? '已验证' : 'Validated' },
                { value: 'unverifiable', label: isZh ? '无法验证' : 'Unverifiable' },
                { value: 'confirmed_true', label: isZh ? '这是真的' : 'Confirmed True' },
                { value: 'confirmed_false', label: isZh ? '这是假的' : 'Confirmed False' },
                { value: 'uncertain', label: isZh ? '我不确定' : 'Uncertain' }
            ];

            // 使用 assumption_id，如果没有则使用 hypothesis 的 base64 编码作为临时 ID
            const assumptionId = assumption.assumption_id || btoa(assumption.hypothesis || assumption.description || assumption.assumption_text || '');

            return `
                <select onchange="updateAssumptionStatus('${assumptionId}', this.value)"
                        class="text-xs px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-zinc-300 focus:border-blue-500 focus:outline-none">
                    ${statusOptions.map(opt =>
                        `<option value="${opt.value}" ${assumption.status === opt.value ? 'selected' : ''}>${opt.label}</option>`
                    ).join('')}
                </select>
            `;
        }

        // 全局变量：控制问题输入框的显示
        window.showIssueInput = null;

        // 显示模块问题描述输入框
        function showModuleIssueInput(moduleName) {
            window.showIssueInput = moduleName;
            refreshData();
        }

        // 取消问题描述输入
        function cancelModuleIssue(moduleName) {
            window.showIssueInput = null;
            refreshData();
        }

        // 提交模块问题
        function submitModuleIssue(moduleName) {
            const input = document.getElementById(`issue-input-${moduleName}`);
            const issueDescription = input ? input.value : '';
            
            fetch('/api/update/module', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    module_name: moduleName,
                    status: 'has_issue',
                    issue_description: issueDescription
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.showIssueInput = null;
                    refreshData();
                } else {
                    alert('更新失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(err => {
                console.error('Error updating module:', err);
                alert('更新失败，请检查网络连接');
            });
        }

        // 更新模块状态
        function updateModuleStatus(moduleName, newStatus) {
            const issueDescription = newStatus === 'has_issue' ? '' : '';
            
            fetch('/api/update/module', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    module_name: moduleName,
                    status: newStatus,
                    issue_description: issueDescription
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    refreshData();
                } else {
                    alert('更新失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(err => {
                console.error('Error updating module:', err);
                alert('更新失败，请检查网络连接');
            });
        }

        // 更新假设状态
        function updateAssumptionStatus(assumptionId, newStatus) {
            fetch('/api/update/assumption', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    assumption_id: assumptionId,
                    status: newStatus
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    refreshData();
                } else {
                    alert('更新失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(err => {
                console.error('Error updating assumption:', err);
                alert('更新失败，请检查网络连接');
            });
        }

        // 初始化
        setLanguage('zh');
        refreshData();
    </script>
</body>
</html>
    """


def get_static_html_template():
    """获取静态 HTML 模板（简化版，移除交互功能）"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cox 可观测性面板 - 静态模式</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        body {
            background: linear-gradient(135deg, #09090b 0%, #18181b 50%, #09090b 100%);
            min-height: 100vh;
        }
        .glass-card {
            background: rgba(39, 39, 42, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(63, 63, 70, 0.3);
        }
        .animate-spin {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="text-zinc-100 antialiased p-4 lg:p-8">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="mb-8 flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent" id="app-title">Cox 可观测性面板</h1>
                <p class="text-sm text-zinc-500 mt-1" id="project-info">正在加载...</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="px-4 py-2 bg-zinc-900/80 rounded-lg border border-zinc-800">
                    <p class="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-1">最后更新</p>
                    <p class="text-sm font-mono text-emerald-400" id="last-updated">--:--:--</p>
                </div>
                <button onclick="refreshData()" class="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg font-semibold hover:bg-zinc-200 transition-colors">
                    <i data-lucide="refresh-cw" class="w-4 h-4" id="refresh-icon"></i>
                    <span>刷新</span>
                </button>
            </div>
        </header>

        <!-- Top Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10" id="top-metrics"></div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Left Column -->
            <div class="lg:col-span-8 space-y-6">
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-lg font-bold flex items-center gap-2">
                            <i data-lucide="git-merge" class="text-blue-400"></i> 迭代管理
                        </h2>
                        <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-1 rounded" id="task-count">0 迭代</span>
                    </div>
                    <div class="space-y-3" id="task-list"></div>
                </div>

                <div class="glass-card rounded-2xl p-6">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                        <i data-lucide="layers" class="text-emerald-400"></i> 模块成熟度
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="module-grid"></div>
                </div>
            </div>

            <!-- Right Column -->
            <div class="lg:col-span-4 space-y-6">
                <div class="glass-card rounded-2xl p-6">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                        <i data-lucide="lightbulb" class="text-yellow-400"></i> 假设验证
                    </h2>
                    <div class="space-y-3" id="assumptions-list"></div>
                </div>

                <div class="glass-card rounded-2xl p-6 bg-red-500/5 border-red-500/20">
                    <h2 class="text-lg font-bold flex items-center gap-2 mb-4 text-red-400">
                        <i data-lucide="alert-triangle"></i> 活跃异常
                    </h2>
                    <div class="space-y-3" id="anomaly-list"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const statusConfig = {
            'completed': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: '已完成' },
            'done': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: '已完成' },
            'in_progress': { bg: 'bg-blue-500/10', text: 'text-blue-400', label: '进行中' },
            'todo': { bg: 'bg-zinc-800', text: 'text-zinc-400', label: '待处理' },
            'not_started': { bg: 'bg-zinc-800', text: 'text-zinc-400', label: '未开始' },
            'delayed': { bg: 'bg-red-500/10', text: 'text-red-400', label: '延期' },
            'critical': { bg: 'bg-red-500', text: 'text-white', label: '紧急' },
            'validated': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: '已验证' },
            'invalidated': { bg: 'bg-red-500/10', text: 'text-red-400', label: '已失效' },
            'pending': { bg: 'bg-yellow-500/10', text: 'text-yellow-400', label: '待定' },
            'confirmed': { bg: 'bg-blue-500/10', text: 'text-blue-400', label: '待确认' },
            'optimized': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: '完美' },
            'has_issue': { bg: 'bg-red-500/10', text: 'text-red-400', label: '有问题' }
        };

        // Priority 和 Risk Level 翻译配置
        const priorityLabels = {
            'zh': { 'critical': '紧急', 'high': '高', 'medium': '中', 'low': '低' },
            'en': { 'critical': 'Critical', 'high': 'High', 'medium': 'Medium', 'low': 'Low' }
        };
        
        const riskLabels = {
            'zh': { 'high': '大风险', 'low': '小风险' },
            'en': { 'high': 'High Risk', 'low': 'Low Risk' }
        };
        
        function getPriorityLabel(priority) {
            return priorityLabels[currentLang][priority] || priority;
        }
        
        function getRiskLabel(risk) {
            return riskLabels[currentLang][risk] || risk;
        }

                function getStatusBadge(status) {
            const key = status ? status.toLowerCase() : 'pending';
            const cfg = statusConfig[key] || { bg: 'bg-zinc-800', text: 'text-zinc-400', label: status || '未知' };
            return `<span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${cfg.bg} ${cfg.text}">${cfg.label}</span>`;
        }

        let collapsedIterations = new Set();

        function toggleIteration(iterationId) {
            if (collapsedIterations.has(iterationId)) {
                collapsedIterations.delete(iterationId);
            } else {
                collapsedIterations.add(iterationId);
            }
            if(window.lastData) renderUI(window.lastData);
        }

        async function refreshData() {
            const btnIcon = document.getElementById('refresh-icon');
            if(btnIcon) btnIcon.classList.add('animate-spin');
            try {
                if(window.lastData) renderUI(window.lastData);
            } catch (e) {
                console.error("Refresh failed", e);
            } finally {
                if(btnIcon) setTimeout(() => btnIcon.classList.remove('animate-spin'), 600);
            }
        }

        function renderUI(data) {
            try {
                const t = translations;
                document.getElementById('last-updated').textContent = data.last_updated;
                const p = data.project;
                const a = data.app;
                const test = data.test;

                document.getElementById('project-info').textContent = `${p.project_name} • v${a.version || '1.0'}`;

                const totalTasks = p.iterations.reduce((sum, iter) => sum + iter.tasks.length, 0);
                document.getElementById('top-metrics').innerHTML = `
                    ${renderMetricCard('迭代周期', p.iterations.length, 'milestone', 'text-blue-400')}
                    ${renderMetricCard('任务总数', totalTasks, 'check-circle', 'text-emerald-400')}
                    ${renderMetricCard('系统异常', test.anomalies.length, 'zap', 'text-red-400')}
                `;

                document.getElementById('task-count').textContent = `${p.iterations.length} 迭代`;
                document.getElementById('task-list').innerHTML = p.iterations.map(iter => {
                    const completedTasks = iter.tasks.filter(t => t.status === 'completed' || t.status === 'done').length;
                    const progress = iter.tasks.length > 0 ? (completedTasks / iter.tasks.length * 100).toFixed(0) : 0;
                    const isCurrent = iter.iteration_id === p.current_iteration;
                    const isCollapsed = !isCurrent && collapsedIterations.has(iter.iteration_id);
                    
                    return `
                        <div class="bg-zinc-900/40 rounded-xl border ${isCurrent ? 'border-blue-500/30 bg-blue-500/5' : 'border-zinc-800/50'} overflow-hidden">
                            <div class="p-4 border-b border-zinc-800/50 cursor-pointer hover:bg-zinc-800/30 transition-colors" onclick="toggleIteration('${iter.iteration_id}')">
                                <div class="flex items-center justify-between mb-2">
                                    <div class="flex items-center gap-3">
                                        ${isCurrent ? '<span class="text-xs bg-blue-500 text-white px-2 py-0.5 rounded font-medium">当前</span>' : ''}
                                        <i data-lucide="${isCollapsed ? 'chevron-right' : 'chevron-down'}" class="w-4 h-4 text-zinc-500 transition-transform"></i>
                                        <h3 class="font-bold text-base text-zinc-200">${iter.iteration_name}</h3>
                                    </div>
                                    ${getStatusBadge(iter.status)}
                                </div>
                                <div class="flex items-center gap-4 text-xs text-zinc-500">
                                    <span><i data-lucide="calendar" class="w-3 h-3 inline mr-1"></i>${iter.start_date || '-'} ~ ${iter.end_date || '-'}</span>
                                </div>
                            </div>
                            <div class="${isCollapsed ? 'hidden' : ''}">
                                <div class="px-4 py-3 bg-zinc-900/20">
                                    <div class="flex items-center justify-between text-xs mb-1">
                                        <span class="text-zinc-400">任务进度</span>
                                        <span class="text-zinc-300">${completedTasks}/${iter.tasks.length} 已完成 (${progress}%)</span>
                                    </div>
                                    <div class="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                                        <div class="bg-gradient-to-r from-blue-500 to-emerald-500 h-full transition-all duration-500" style="width: ${progress}%"></div>
                                    </div>
                                </div>
                                <div class="p-4 space-y-2">
                                    ${iter.tasks.length > 0 ? iter.tasks.map(task => `
                                        <div class="flex items-center justify-between p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/30">
                                            <div class="flex items-center gap-3">
                                                <div class="w-1.5 h-6 rounded-full ${task.status === 'completed' || task.status === 'done' ? 'bg-emerald-500' : task.status === 'in_progress' ? 'bg-blue-500' : 'bg-zinc-600'}"></div>
                                                <div>
                                                    <p class="font-medium text-sm text-zinc-200">${task.task_name}</p>
                                                    <div class="flex items-center gap-3 mt-1 text-xs text-zinc-500">
                                                        <span>${task.task_id}</span>
                                                        ${task.assignee ? `<span><i data-lucide="user" class="w-3 h-3 inline mr-1"></i>${task.assignee}</span>` : ''}
                                                        ${task.priority ? `<span class="px-1.5 py-0.5 rounded ${task.priority === 'high' || task.priority === 'critical' ? 'bg-red-500/10 text-red-400' : 'bg-zinc-700/50 text-zinc-400'}">${getPriorityLabel(task.priority)}</span>` : ''}
                                                        ${task.risk_level ? `<span class="px-1.5 py-0.5 rounded ${task.risk_level === 'high' ? 'bg-orange-500/10 text-orange-400' : 'bg-emerald-500/10 text-emerald-400'}">${task.risk_level}</span>` : ''}
                                                    </div>
                                                </div>
                                            </div>
                                            ${getStatusBadge(task.status)}
                                        </div>
                                    `).join('') : '<p class="text-sm text-zinc-500 text-center py-4">尚未详细计划</p>'}
                                </div>
                            </div>
                            ${iter.assumptions && iter.assumptions.length > 0 ? `
                                <div class="px-4 py-3 border-t border-zinc-800/50">
                                    <div class="flex items-center gap-2 text-xs text-zinc-500 mb-2">
                                        <i data-lucide="lightbulb" class="w-3 h-3"></i>
                                        <span>开发假设 (${iter.assumptions.length})</span>
                                    </div>
                                    ${iter.assumptions.slice(0, 2).map(assump => {
                                        let status = assump.status;
                                        if (!status && assump.validated !== undefined) {
                                            status = assump.validated === true ? 'validated' : 'pending';
                                        }
                                        return `<div class="text-xs text-zinc-400 mb-1">
                                            <span class="${status === 'validated' ? 'text-emerald-400' : status === 'invalidated' ? 'text-red-400' : 'text-amber-400'}">●</span>
                                            ${assump.hypothesis || assump.description || assump.assumption_text || '无描述'}
                                        </div>`;
                                    }).join('')}
                                    ${iter.assumptions.length > 2 ? `<p class="text-xs text-zinc-500">...还有 ${iter.assumptions.length - 2} 个假设</p>` : ''}
                                </div>
                            ` : ''}
                        </div>
                    `;
                }).join('');

                const developedModules = a.modules.filter(m => 
                    m.status === 'confirmed' || 
                    m.status === 'optimized' || 
                    m.status === 'has_issue'
                );
                document.getElementById('module-grid').innerHTML = developedModules.map(m => `
                    <div class="p-4 bg-zinc-900/40 rounded-xl border border-zinc-800/50">
                        <div class="flex justify-between items-start mb-3">
                            <p class="font-bold text-sm text-zinc-200">${m.module_name}</p>
                            ${getStatusBadge(m.status)}
                        </div>
                        <div class="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                            <div class="bg-blue-500 h-full" style="width: ${(m.completion_rate || 0)*100}%"></div>
                        </div>
                        <p class="text-[10px] text-zinc-500 mt-2 font-mono uppercase">${((m.completion_rate || 0)*100).toFixed(0)}% 完成</p>
                        ${m.status === 'has_issue' && m.issue_description ? `
                            <div class="mt-3 p-2 bg-red-500/10 rounded-lg border border-red-500/20">
                                <p class="text-xs text-red-400">问题描述：${m.issue_description}</p>
                            </div>
                        ` : ''}
                    </div>
                `).join('') || '<p class="text-sm text-zinc-500 text-center py-4">暂无已开发的模块</p>';

                const allAssumptions = p.iterations.flatMap(i => i.assumptions || []);
                document.getElementById('assumptions-list').innerHTML = allAssumptions.length
                    ? allAssumptions.map(assump => `
                        <div class="p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/50">
                            <p class="text-sm font-semibold text-zinc-200 mb-2">${assump.hypothesis || assump.description || assump.assumption_text || '无描述'}</p>
                            <div class="flex items-center justify-between">
                                ${getStatusBadge(assump.status)}
                                ${assump.validation_date ? `<span class="text-[10px] text-zinc-500">${assump.validation_date}</span>` : ''}
                            </div>
                        </div>
                    `).join('')
                    : '<p class="text-zinc-500 text-sm text-center py-4">暂无跟踪的假设</p>';

                document.getElementById('anomaly-list').innerHTML = test.anomalies.length
                    ? test.anomalies.map(anom => `
                        <div class="p-3 bg-red-500/10 rounded-lg border border-red-500/20 text-xs">
                            <p class="font-bold text-red-400 mb-1">${anom.type}</p>
                            <p class="text-zinc-400 line-clamp-1">${anom.description}</p>
                        </div>
                    `).join('')
                    : '<p class="text-zinc-500 text-sm text-center py-4">系统状态良好</p>';

                lucide.createIcons();
            } catch (e) {
                console.error("Render failed:", e);
                console.error("Data:", data);
            }
        }

        function renderMetricCard(label, value, icon, iconColor) {
            return `
                <div class="glass-card rounded-2xl p-5 flex items-center gap-5">
                    <div class="p-3 bg-zinc-900 rounded-xl">
                        <i data-lucide="${icon}" class="w-6 h-6 ${iconColor}"></i>
                    </div>
                    <div>
                        <p class="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-1">${label}</p>
                        <p class="text-2xl font-bold text-white">${value}</p>
                    </div>
                </div>
            `;
        }

        const translations = {
            appTitle: 'Cox 可观测性面板',
            lastUpdate: '最后更新',
            refresh: '刷新'
        };

        // 静态模式固定中文，不需要 setLanguage 函数
        refreshData();
    </script>
</body>
</html>
    """


def generate_static_html(data_manager, output_file):
    """生成静态 HTML 文件
    
    静态模式：将所有数据内联到 HTML 文件中，避免 CORS 问题
    优势：
    - 一个 HTML 文件即可运行，不需要额外的 JSON 文件
    - 完全避免浏览器的 CORS 限制
    - 用户体验好，直接打开 HTML 即可查看
    - 静态模式只提供纯展示功能，不包含交互元素
    """
    # 1. 读取所有数据文件
    data = {}
    for key, src_path in data_manager.files.items():
        src_file = Path(src_path)
        if src_file.exists():
            with open(src_file, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)
            print(f"[INFO] 已读取数据文件: {src_file.name}")
        else:
            print(f"[WARNING] 数据文件不存在: {src_path}")
            data[key] = {}
    
    # 2. 准备内联数据 JavaScript 代码
    inline_data_js = f"""
    // 静态模式：数据已内联到 HTML 中
    const staticData = {{
        project: {json.dumps(data['project'], ensure_ascii=False)},
        app: {json.dumps(data['app'], ensure_ascii=False)},
        test: {json.dumps(data['test'], ensure_ascii=False)},
        last_updated: new Date().toLocaleTimeString('zh-CN', {{hour: '2-digit', minute: '2-digit', second: '2-digit'}})
    }};
    
    // 刷新数据（静态模式直接使用内联数据，不支持实时刷新）
    async function refreshData() {{
        const btnIcon = document.getElementById('refresh-icon');
        if(btnIcon) btnIcon.classList.add('animate-spin');
        
        try {{
            // 静态模式：使用内联数据
            window.lastData = staticData;
            renderUI(staticData);
        }} catch (e) {{
            console.error("Render failed", e);
        }} finally {{
            if(btnIcon) setTimeout(() => btnIcon.classList.remove('animate-spin'), 600);
        }}
    }}
    
    // 禁用自动刷新（静态模式无法实时更新数据）
    // setInterval(refreshData, 30000);
    """
    
    # 3. 获取静态 HTML 模板（简化版，不含交互功能）
    html_template = get_static_html_template()
    
    # 4. 插入内联数据到 HTML 中
    # 在 refreshData(); 之前插入 staticData 变量定义
    marker = "refreshData();"
    if marker in html_template:
        html_template = html_template.replace(marker, inline_data_js + "\n        " + marker)
    
    # 5. 写入 HTML 文件
    output_file_path = Path(output_file)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"\n[OK] 静态 HTML 已生成: {output_file_path.absolute()}")
    print(f"[INFO] 可以直接用浏览器打开查看")
    print(f"[INFO] 数据已内联到 HTML 文件中，无需额外的 JSON 文件")
    print(f"[INFO] 静态模式只提供展示功能，不包含交互元素")
    
    return str(output_file_path.absolute())


def main():
    global data_manager
    
    parser = argparse.ArgumentParser(
        description='Modern Observability Dashboard - 静态/Web 两种模式',
        epilog='示例:\n  静态模式: python run_web_observability.py --mode static --project project.json --app app.json --test test.json --output observability.html\n  Web 模式: python run_web_observability.py --mode web --project project.json --app app.json --test test.json',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--project', required=True, help='项目数据文件路径')
    parser.add_argument('--app', required=True, help='应用状态文件路径')
    parser.add_argument('--test', required=True, help='测试指标文件路径')
    parser.add_argument('--mode', choices=['static', 'web'], default='static',
                       help='运行模式: static=生成静态HTML（无需Flask）, web=启动Web服务器（需要Flask）')
    parser.add_argument('--output', default='observability.html',
                       help='静态模式下的输出文件路径（默认: observability.html）')
    parser.add_argument('--host', default='127.0.0.1', help='Web 模式下的服务器地址')
    parser.add_argument('--port', type=int, default=5000, help='Web 模式下的服务器端口')
    
    args = parser.parse_args()

    # 验证文件
    for f in [args.project, args.app, args.test]:
        if not os.path.exists(f):
            print(f"[ERROR] 文件不存在: {f}")
            exit(1)

    data_manager = ObservabilityData(args.project, args.app, args.test)

    if args.mode == 'static':
        # 静态模式：生成静态 HTML
        print("\n[INFO] 运行模式: 静态生成")
        print("[INFO] 正在生成静态 HTML 文件...")
        generate_static_html(data_manager, args.output)
        
    elif args.mode == 'web':
        # Web 模式：启动 Flask 服务器
        if not FLASK_AVAILABLE:
            print("\n[ERROR] Web 模式需要 Flask，但未检测到 Flask 安装")
            print("[INFO] 请先安装 Flask: pip install flask")
            print("[INFO] 或者使用静态模式: --mode static")
            exit(1)
        
        print("\n[INFO] 运行模式: Web 交互")
        print(f"[INFO] 本地地址: http://{args.host}:{args.port}")
        print(f"[INFO] 监控中: {len(data_manager.files)} 个数据源")
        print("[INFO] 按 Ctrl+C 停止服务器\n")
        
        app.run(host=args.host, port=args.port, debug=False, threaded=True)

if __name__ == '__main__':
    main()