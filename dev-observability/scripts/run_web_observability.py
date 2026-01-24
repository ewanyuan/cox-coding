#!/usr/bin/env python3
"""
Modern Observability Web Dashboard (Premium UI)
基于 Flask 和 Tailwind CSS 构建的现代化可观测仪表板 - 支持中英文切换
"""

import json
import os
import sys
import io
import argparse
import time
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, jsonify

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

app = Flask(__name__)
data_manager = None

def get_dashboard_html():
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
                            <i data-lucide="list-todo" class="text-blue-400"></i> 
                            <span id="title-tasks">进行中的任务</span>
                        </h2>
                        <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-1 rounded" id="task-count">0 任务</span>
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

            <div class="glass-card rounded-2xl p-6 bg-orange-500/5 border-orange-500/20">
                <h2 class="text-lg font-bold flex items-center gap-2 mb-6 text-orange-400">
                    <i data-lucide="alert-octagon"></i> 
                    <span id="title-risks">风险告警</span>
                </h2>
                <div class="space-y-3" id="risk-list">
                    <!-- 动态内容 -->
                </div>
            </div>

            <div class="glass-card rounded-2xl p-6 lg:col-span-1">
                <h2 class="text-lg font-bold flex items-center gap-2 mb-6">
                    <i data-lucide="trending-up" class="text-green-400"></i> 
                    <span id="title-perf">性能趋势</span>
                </h2>
                <div id="performance-chart" class="h-48">
                    <canvas id="perf-canvas"></canvas>
                </div>
            </div>

            <div class="glass-card rounded-2xl p-6 lg:col-span-1">
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
                tasks: '进行中的任务',
                modules: '模块成熟度',
                coverage: '测试覆盖率',
                anomalies: '活跃异常',
                assumptions: '假设验证分析',
                risks: '风险告警',
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
                noRisks: '当前无活跃风险',
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
                    pending: '待定'
                }
            },
            en: {
                appTitle: 'Cox coding - Transparent & Smooth Interactive Experience',
                lastUpdate: 'LAST UPDATE',
                refresh: 'Refresh',
                tasks: 'Active Tasks',
                modules: 'Module Maturity',
                coverage: 'Test Coverage',
                anomalies: 'Active Anomalies',
                assumptions: 'Assumptions Analysis',
                risks: 'Risk Alerts',
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
                noRisks: 'No active risks',
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
                    pending: 'Pending'
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
            document.getElementById('title-risks').textContent = t.risks;
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
            'pending': { bg: 'bg-yellow-500/10', text: 'text-yellow-400' }
        };

        function getStatusBadge(status) {
            const key = status.toLowerCase();
            const cfg = statusConfig[key] || { bg: 'bg-zinc-800', text: 'text-zinc-400' };
            const label = translations[currentLang].status[key] || status;
            return `<span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${cfg.bg} ${cfg.text}">${label}</span>`;
        }

        async function refreshData() {
            const btnIcon = document.getElementById('refresh-icon');
            btnIcon.classList.add('animate-spin');
            
            try {
                const res = await fetch('/api/data');
                const data = await res.json();
                window.lastData = data;
                renderUI(data);
            } catch (e) {
                console.error("Refresh failed", e);
            } finally {
                setTimeout(() => btnIcon.classList.remove('animate-spin'), 600);
            }
        }

        function renderUI(data) {
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
            
            document.getElementById('top-metrics').innerHTML = `
                ${renderMetricCard(t.metricIterations, p.iterations.length, 'milestone', 'text-blue-400')}
                ${renderMetricCard(t.metricTasks, totalTasks, 'check-circle', 'text-emerald-400')}
                ${renderMetricCard(t.metricPassRate, passRate + '%', 'shield', 'text-amber-400')}
                ${renderMetricCard(t.metricAnomalies, test.anomalies.length, 'zap', 'text-red-400')}
            `;

            // 任务列表
            const allTasks = p.iterations.flatMap(i => i.tasks);
            document.getElementById('task-count').textContent = `${allTasks.length} ${t.metricTasks}`;
            document.getElementById('task-list').innerHTML = allTasks.slice(0, 5).map(task => `
                <div class="flex items-center justify-between p-4 bg-zinc-900/40 rounded-xl border border-zinc-800/50">
                    <div class="flex items-center gap-4">
                        <div class="w-1 h-8 rounded-full ${task.status === 'completed' || task.status === 'done' ? 'bg-emerald-500' : 'bg-blue-500'}"></div>
                        <div>
                            <p class="font-semibold text-sm">${task.task_name}</p>
                            <p class="text-xs text-zinc-500">${task.assignee || t.unassigned}</p>
                        </div>
                    </div>
                    <div>${getStatusBadge(task.status)}</div>
                </div>
            `).join('');

            // 模块成熟度
            document.getElementById('module-grid').innerHTML = a.modules.map(m => `
                <div class="p-4 bg-zinc-900/40 rounded-xl border border-zinc-800/50">
                    <div class="flex justify-between items-start mb-3">
                        <p class="font-bold text-sm text-zinc-200">${m.module_name}</p>
                        ${getStatusBadge(m.status)}
                    </div>
                    <div class="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-blue-500 h-full" style="width: ${(m.completion_rate || 0)*100}%"></div>
                    </div>
                    <p class="text-[10px] text-zinc-500 mt-2 font-mono uppercase">${((m.completion_rate || 0)*100).toFixed(0)}% ${t.completeSuffix}</p>
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

            // 假设分析
            const allAssumptions = p.iterations.flatMap(i => i.assumptions || []);
            document.getElementById('assumptions-list').innerHTML = allAssumptions.length
                ? allAssumptions.map(assump => `
                    <div class="p-3 bg-zinc-900/40 rounded-lg border border-zinc-800/50">
                        <p class="text-sm font-semibold text-zinc-200 mb-2">${assump.description}</p>
                        <div class="flex items-center justify-between">
                            ${getStatusBadge(assump.status)}
                            ${assump.validation_date ? `<span class="text-[10px] text-zinc-500">${assump.validation_date}</span>` : ''}
                        </div>
                    </div>
                `).join('')
                : `<p class="text-zinc-500 text-sm text-center py-4">${t.noAssumptions}</p>`;

            // 风险告警 (逻辑保持英文KEY但UI翻译)
            const risks = analyzeRisks(p, a, test);
            document.getElementById('risk-list').innerHTML = risks.length
                ? risks.map(risk => `
                    <div class="p-3 bg-orange-500/10 rounded-lg border border-orange-500/20">
                        <div class="flex items-center justify-between mb-2">
                            <span class="font-bold text-orange-400 text-sm">${risk.level}</span>
                            <span class="text-[10px] text-zinc-500 uppercase">${risk.category}</span>
                        </div>
                        <p class="text-xs text-zinc-300">${risk.message}</p>
                    </div>
                `).join('')
                : `<p class="text-zinc-500 text-sm text-center py-4">${t.noRisks}</p>`;

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
        }

        function analyzeRisks(project, app, test) {
            const risks = [];
            const currentIter = project.iterations.find(i => i.iteration_id === project.current_iteration);
            const isZh = currentLang === 'zh';

            project.iterations.forEach(iter => {
                if (iter.status === 'delayed') {
                    risks.push({
                        level: 'HIGH', category: isZh ? '排期' : 'Schedule',
                        message: isZh ? `迭代 ${iter.iteration_name} 已延期` : `Iteration ${iter.iteration_name} delayed`
                    });
                }
            });

            const blockedTasks = currentIter?.tasks.filter(t => t.status === 'blocked') || [];
            if (blockedTasks.length > 0) {
                risks.push({
                    level: 'MEDIUM', category: isZh ? '阻塞' : 'Blockers',
                    message: isZh ? `${blockedTasks.length} 个任务被阻塞` : `${blockedTasks.length} tasks blocked`
                });
            }

            const criticalAnomalies = test.anomalies.filter(a => a.severity === 'critical');
            if (criticalAnomalies.length > 0) {
                risks.push({
                    level: 'CRITICAL', category: isZh ? '质量' : 'Quality',
                    message: isZh ? `检测到 ${criticalAnomalies.length} 个严重异常` : `${criticalAnomalies.length} critical anomalies detected`
                });
            }

            return risks.slice(0, 5);
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

        // 初始化
        setLanguage('zh');
        refreshData();
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
    """

@app.route('/')
def index():
    return render_template_string(get_dashboard_html())

@app.route('/api/data')
def get_data():
    return jsonify(data_manager.get_all_data())

def main():
    global data_manager
    parser = argparse.ArgumentParser(description='Modern Observability Dash')
    parser.add_argument('--project', required=True, help='Project data path')
    parser.add_argument('--app', required=True, help='App data path')
    parser.add_argument('--test', required=True, help='Test metrics path')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    # 验证文件
    for f in [args.project, args.app, args.test]:
        if not os.path.exists(f):
            print(f"Error: {f} not found.")
            exit(1)

    data_manager = ObservabilityData(args.project, args.app, args.test)

    print(f"\n🚀 Cox coding-透明流畅的交互体验 已启动!")
    print(f"🔗 本地地址: http://{args.host}:{args.port}")
    print(f"📡 监控中: {len(data_manager.files)} 个数据源")
    
    app.run(host=args.host, port=args.port, debug=False, threaded=True)

if __name__ == '__main__':
    main()
