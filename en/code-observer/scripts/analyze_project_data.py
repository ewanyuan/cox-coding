#!/usr/bin/env python3
"""
分析项目迭代和任务数据，提取项目进度、任务状态等信息
"""

import json
import sys
import argparse
from typing import Dict, List, Any


class ProjectDataAnalyzer:
    """项目数据分析器"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.analysis = {
            "project_info": {},
            "iteration_progress": {},
            "task_summary": {},
            "assumptions": [],
            "risks": []
        }
    
    def analyze(self) -> Dict[str, Any]:
        """分析项目数据"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 分析项目基本信息
            self._analyze_project_info(data)
            
            # 分析迭代进度
            self._analyze_iteration_progress(data)
            
            # 分析任务状态
            self._analyze_task_summary(data)
            
            # 提取开发假设
            self._extract_assumptions(data)
            
            # 识别风险
            self._identify_risks(data)
            
            return self.analysis
            
        except FileNotFoundError:
            raise Exception(f"项目数据文件不存在: {self.input_file}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")
        except Exception as e:
            raise Exception(f"分析项目数据失败: {str(e)}")
    
    def _analyze_project_info(self, data: Dict[str, Any]):
        """分析项目基本信息"""
        self.analysis["project_info"] = {
            "project_name": data.get('project_name', 'unknown'),
            "total_iterations": len(data.get('iterations', [])),
            "total_tasks": 0
        }
        
        # 统计总任务数
        for iteration in data.get('iterations', []):
            self.analysis["project_info"]["total_tasks"] += len(iteration.get('tasks', []))
    
    def _analyze_iteration_progress(self, data: Dict[str, Any]):
        """分析迭代进度"""
        iterations = data.get('iterations', [])
        
        for iteration in iterations:
            iteration_name = iteration.get('name', 'unknown')
            tasks = iteration.get('tasks', [])
            
            if not tasks:
                continue
            
            completed_tasks = len([t for t in tasks if t.get('status', '').lower() in ['completed', 'done']])
            
            self.analysis["iteration_progress"][iteration_name] = {
                "total_tasks": len(tasks),
                "completed_tasks": completed_tasks,
                "completion_rate": (completed_tasks / len(tasks)) * 100 if tasks else 0,
                "status": iteration.get('status', 'unknown')
            }
    
    def _analyze_task_summary(self, data: Dict[str, Any]):
        """分析任务状态汇总"""
        all_tasks = []
        
        for iteration in data.get('iterations', []):
            all_tasks.extend(iteration.get('tasks', []))
        
        if not all_tasks:
            return
        
        status_counts = {}
        for task in all_tasks:
            status = task.get('status', 'unknown').lower()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        self.analysis["task_summary"] = {
            "total_tasks": len(all_tasks),
            "status_distribution": status_counts,
            "completed_tasks": status_counts.get('completed', 0) + status_counts.get('done', 0),
            "pending_tasks": status_counts.get('pending', 0) + status_counts.get('todo', 0),
            "in_progress_tasks": status_counts.get('in_progress', 0) + status_counts.get('doing', 0)
        }
    
    def _extract_assumptions(self, data: Dict[str, Any]):
        """提取开发假设"""
        assumptions = data.get('assumptions', [])
        
        if isinstance(assumptions, list):
            self.analysis["assumptions"] = assumptions
        elif isinstance(assumptions, str):
            self.analysis["assumptions"] = [assumptions]
    
    def _identify_risks(self, data: Dict[str, Any]):
        """识别风险"""
        risks = []
        
        # 检查迭代进度风险
        for iteration_name, progress in self.analysis["iteration_progress"].items():
            if progress["completion_rate"] < 50 and progress["status"].lower() in ['in_progress', 'active']:
                risks.append({
                    "type": "进度风险",
                    "description": f"迭代 {iteration_name} 完成率仅 {progress['completion_rate']:.1f}%",
                    "severity": "medium"
                })
        
        # 检查任务堆积风险
        if self.analysis.get("task_summary", {}).get("pending_tasks", 0) > 10:
            risks.append({
                "type": "任务堆积",
                "description": f"待处理任务过多: {self.analysis['task_summary']['pending_tasks']} 个",
                "severity": "high"
            })
        
        self.analysis["risks"] = risks


def main():
    parser = argparse.ArgumentParser(description='分析项目迭代和任务数据')
    parser.add_argument('--input', required=True, help='项目数据JSON文件路径')
    parser.add_argument('--output', required=True, help='输出分析结果JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        analyzer = ProjectDataAnalyzer(args.input)
        analysis = analyzer.analyze()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"项目数据分析完成，输出文件: {args.output}")
        print(f"迭代数量: {analysis['project_info']['total_iterations']}")
        print(f"总任务数: {analysis['project_info']['total_tasks']}")
        print(f"风险数量: {len(analysis['risks'])}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
