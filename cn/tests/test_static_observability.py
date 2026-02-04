#!/usr/bin/env python3
"""
单元测试：智能体调用脚本生成静态网页

测试目标：
1. 使用模拟数据
2. 模拟智能体调用脚本生成静态网页
3. 验证网页的第一个迭代的任务对应的DOM元素数量不为0
4. 生成的静态网页要保存下来，用户需要打开验证
"""

import os
import json
import unittest
import tempfile
import shutil
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestStaticObservability(unittest.TestCase):
    """测试静态可观测性功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 生成模拟数据
        self.generate_mock_data()
        
        # 输出文件路径
        self.output_html = os.path.join(self.temp_dir, 'observability.html')
        
        # 也在tests文件夹生成一个，方便用户查看
        self.user_output_html = os.path.join(Path(__file__).parent, 'static_observability_test.html')
    
    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
        # 保留用户查看的文件，方便用户验证
    
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
    
    def test_static_observability(self):
        """测试静态可观测性功能"""
        # 导入必要的模块
        from cox.scripts.run_web_observability import ObservabilityData, generate_static_html
        
        # 创建数据管理器
        data_manager = ObservabilityData(
            os.path.join(self.temp_dir, 'project_data.json'),
            os.path.join(self.temp_dir, 'app_status.json'),
            os.path.join(self.temp_dir, 'test_metrics.json')
        )
        
        # 模拟智能体调用脚本生成静态网页
        # 调用generate_static_html函数生成包含内联数据的HTML文件
        generate_static_html(data_manager, self.output_html)
        
        # 同时生成用户可查看的文件
        generate_static_html(data_manager, self.user_output_html)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(self.output_html), "静态网页文件未生成")
        self.assertTrue(os.path.exists(self.user_output_html), "用户查看的静态网页文件未生成")
        
        # 读取生成的HTML内容
        with open(self.output_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 验证文件大小大于0
        self.assertGreater(len(html_content), 0, "静态网页文件为空")
        
        # 验证HTML内容包含必要的元素
        self.assertIn('Cox 可观测性面板', html_content)
        
        # 验证数据已内联到HTML中
        self.assertIn('staticData', html_content, "数据未内联到HTML中")
        self.assertIn('测试项目', html_content, "项目名称未显示")
        
        # 验证第一个迭代的任务对应的DOM元素数量不为0
        # 检查是否包含任务列表
        self.assertIn('task-list', html_content)
        
        # 检查是否包含任务相关的DOM结构
        # 检查任务卡片元素 - 这是任务列表中的任务项样式
        task_card_count = html_content.count('bg-zinc-900/40 rounded-lg border border-zinc-800/30')
        self.assertGreater(task_card_count, 0, "第一个迭代的任务对应的DOM元素数量为0")
        
        # 更精确的检查：验证任务数据已内联
        self.assertIn('TASK-001', html_content, "任务1未在HTML中显示")
        self.assertIn('TASK-002', html_content, "任务2未在HTML中显示")
        self.assertIn('任务1', html_content, "任务1名称未在HTML中显示")
        self.assertIn('任务2', html_content, "任务2名称未在HTML中显示")
        
        print(f"\n静态网页已生成：")
        print(f"- 临时测试文件：{self.output_html}")
        print(f"- 用户验证文件：{self.user_output_html}")
        print(f"\n请打开 {self.user_output_html} 验证网页内容。")
        print(f"\n验证要点：")
        print(f"1. 页面标题显示'测试项目'")
        print(f"2. 迭代管理区域显示'2 迭代'")
        print(f"3. 第一个迭代包含2个任务：'任务1'和'任务2'")
        print(f"4. 任务状态正确显示（todo/in_progress）")

if __name__ == '__main__':
    unittest.main()
