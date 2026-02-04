#!/usr/bin/env python3
"""
单元测试：智能体调用脚本生成交互网页

测试目标：
1. 使用模拟数据
2. 模拟智能体调用脚本生成交互网页
3. 验证网页的第一个迭代的任务对应的DOM元素数量不为0
4. 自动查找可用端口并启动Web服务器供测试
"""

import os
import json
import unittest
import tempfile
import shutil
import sys
import socket
import threading
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from cox.scripts.run_web_observability import app, ObservabilityData

class TestWebObservability(unittest.TestCase):
    """测试web可观测性功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 生成模拟数据
        self.generate_mock_data()
        
        # 初始化Flask测试客户端
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # 全局data_manager设置
        import cox.scripts.run_web_observability
        cox.scripts.run_web_observability.data_manager = ObservabilityData(
            os.path.join(self.temp_dir, 'project_data.json'),
            os.path.join(self.temp_dir, 'app_status.json'),
            os.path.join(self.temp_dir, 'test_metrics.json')
        )
        
        # 查找可用端口
        self.test_port = self.find_available_port()
        self.server_thread = None
    
    def tearDown(self):
        """清理测试环境"""
        # 不自动停止服务器，让用户手动停止
        # 停止Web服务器
        # if self.server_thread and self.server_thread.is_alive():
        #     self.server_thread.join(timeout=1)
        
        # 删除临时目录
        # shutil.rmtree(self.temp_dir)
        print(f"\n临时目录保留在: {self.temp_dir}")
        print(f"请手动删除临时目录或按 Ctrl+C 停止服务器")
    
    def find_available_port(self, start_port=5001, max_attempts=100):
        """查找可用的端口"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        raise Exception(f"无法在 {start_port}-{start_port + max_attempts} 范围内找到可用端口")
    
    def generate_mock_data(self):
        """生成模拟数据"""
        # 项目数据 - 包含迭代和任务
        project_data = {
            "project_name": "测试项目",
            "current_iteration": "ITER-001",
            "iterations": [
                {
                    "iteration_id": "ITER-001",
                    "iteration_name": "第一个迭代",
                    "start_date": "2026-02-01",
                    "end_date": "2026-02-15",
                    "status": "in_progress",
                    "modules": [],
                    "tasks": [
                        {
                            "task_id": "TASK-001",
                            "task_name": "任务1",
                            "status": "todo",
                            "priority": "high"
                        },
                        {
                            "task_id": "TASK-002",
                            "task_name": "任务2",
                            "status": "in_progress",
                            "priority": "medium"
                        }
                    ],
                    "assumptions": []
                },
                {
                    "iteration_id": "ITER-002",
                    "iteration_name": "第二个迭代",
                    "start_date": "2026-02-16",
                    "end_date": "2026-03-01",
                    "status": "todo",
                    "modules": [],
                    "tasks": [],
                    "assumptions": []
                }
            ],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # 应用状态数据
        app_status = {
            "app_name": "测试应用",
            "version": "1.0.0",
            "modules": [
                {
                    "module_id": "MOD-001",
                    "module_name": "模块1",
                    "status": "confirmed",
                    "completion_rate": 1.0,
                    "issue_description": ""
                }
            ],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # 测试指标数据
        test_metrics = {
            "test_suites": [],
            "anomalies": [],
            "performance_history": [],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # 写入文件
        with open(os.path.join(self.temp_dir, 'project_data.json'), 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(self.temp_dir, 'app_status.json'), 'w', encoding='utf-8') as f:
            json.dump(app_status, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(self.temp_dir, 'test_metrics.json'), 'w', encoding='utf-8') as f:
            json.dump(test_metrics, f, ensure_ascii=False, indent=2)
    
    def test_web_observability(self):
        """测试web可观测性功能"""
        # 启动Web服务器
        self.start_web_server()
        
        # 模拟智能体调用脚本（通过Flask测试客户端访问）
        response = self.client.get('/')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
        
        # 获取响应内容
        html_content = response.data.decode('utf-8')
        
        # 验证HTML内容包含必要的元素
        self.assertIn('Cox coding-透明流畅的交互体验', html_content)
        
        # 验证第一个迭代的任务对应的DOM元素数量不为0
        # 查找任务相关的DOM元素
        # 检查是否包含任务列表
        self.assertIn('task-list', html_content)
        
        # 检查是否包含任务项
        # 由于我们的模拟数据中第一个迭代有2个任务，应该包含任务相关的DOM元素
        # 检查任务相关的DOM结构
        # 检查任务卡片元素
        task_card_count = html_content.count('bg-zinc-900/40 rounded-lg border border-zinc-800/30')
        self.assertGreater(task_card_count, 0, "第一个迭代的任务对应的DOM元素数量为0")
        
        # 检查任务状态元素
        task_status_count = html_content.count('task status')
        # 即使task status不直接出现，我们也应该至少有任务卡片
        if task_status_count == 0:
            # 作为备选检查，确保有任务相关的内容
            self.assertGreater(task_card_count, 0, "第一个迭代的任务对应的DOM元素数量为0")
        
        # 检查API数据
        api_response = self.client.get('/api/data')
        self.assertEqual(api_response.status_code, 200)
        
        api_data = api_response.json
        self.assertIn('project', api_data)
        self.assertIn('iterations', api_data['project'])
        self.assertEqual(len(api_data['project']['iterations']), 2)
        self.assertEqual(len(api_data['project']['iterations'][0]['tasks']), 2)
        
        print(f"\nWeb服务器已启动在端口 {self.test_port}")
        print(f"请访问 http://127.0.0.1:{self.test_port} 查看网页")
        print(f"服务器将保持运行60秒供您验证...")
        print(f"验证完成后按 Ctrl+C 停止服务器")
        
        # 保持服务器运行60秒供用户验证
        time.sleep(60)
    
    def start_web_server(self):
        """在后台启动Web服务器"""
        import cox.scripts.run_web_observability
        
        def run_server():
            cox.scripts.run_web_observability.server = app.run(
                host='127.0.0.1',
                port=self.test_port,
                debug=False,
                threaded=True,
                use_reloader=False
            )
        
        # 使用非daemon线程，这样主线程sleep时服务器会继续运行
        self.server_thread = threading.Thread(target=run_server, daemon=False)
        self.server_thread.start()
        
        # 等待服务器启动
        print("等待服务器启动...")
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()
