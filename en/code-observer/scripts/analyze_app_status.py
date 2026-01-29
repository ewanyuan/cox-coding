#!/usr/bin/env python3
"""
分析应用模块状态数据，提取模块状态、完成率等信息
"""

import json
import sys
import argparse
from typing import Dict, List, Any


class AppStatusAnalyzer:
    """应用状态分析器"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.analysis = {
            "module_status": {},
            "completion_stats": {},
            "owner_summary": {},
            "issues": []
        }
    
    def analyze(self) -> Dict[str, Any]:
        """分析应用状态数据"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 分析模块状态
            self._analyze_module_status(data)
            
            # 分析完成率统计
            self._analyze_completion_stats(data)
            
            # 分析负责人汇总
            self._analyze_owner_summary(data)
            
            # 识别问题模块
            self._identify_issues(data)
            
            return self.analysis
            
        except FileNotFoundError:
            raise Exception(f"应用状态文件不存在: {self.input_file}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")
        except Exception as e:
            raise Exception(f"分析应用状态失败: {str(e)}")
    
    def _analyze_module_status(self, data: List[Dict[str, Any]]):
        """分析模块状态"""
        for module in data:
            module_name = module.get('module_name', 'unknown')
            status = module.get('status', 'unknown')
            
            self.analysis["module_status"][module_name] = {
                "status": status,
                "completion_rate": module.get('completion_rate', 0),
                "owner": module.get('owner', 'unknown'),
                "description": module.get('description', '')
            }
    
    def _analyze_completion_stats(self, data: List[Dict[str, Any]]):
        """分析完成率统计"""
        completion_rates = [m.get('completion_rate', 0) for m in data]
        
        if completion_rates:
            self.analysis["completion_stats"] = {
                "avg_completion_rate": sum(completion_rates) / len(completion_rates),
                "max_completion_rate": max(completion_rates),
                "min_completion_rate": min(completion_rates),
                "completed_modules": len([m for m in data if m.get('completion_rate', 0) >= 100]),
                "in_progress_modules": len([m for m in data if 0 < m.get('completion_rate', 0) < 100]),
                "not_started_modules": len([m for m in data if m.get('completion_rate', 0) == 0])
            }
    
    def _analyze_owner_summary(self, data: List[Dict[str, Any]]):
        """分析负责人汇总"""
        owner_data = {}
        
        for module in data:
            owner = module.get('owner', 'unknown')
            completion_rate = module.get('completion_rate', 0)
            
            if owner not in owner_data:
                owner_data[owner] = {
                    "modules": [],
                    "total_completion_rate": 0,
                    "module_count": 0
                }
            
            owner_data[owner]["modules"].append(module.get('module_name', 'unknown'))
            owner_data[owner]["total_completion_rate"] += completion_rate
            owner_data[owner]["module_count"] += 1
        
        # 计算平均完成率
        for owner, stats in owner_data.items():
            stats["avg_completion_rate"] = stats["total_completion_rate"] / stats["module_count"]
        
        self.analysis["owner_summary"] = owner_data
    
    def _identify_issues(self, data: List[Dict[str, Any]]):
        """识别问题模块"""
        for module in data:
            issues = []
            
            # 完成率低
            if module.get('completion_rate', 0) < 50:
                issues.append("完成率低于50%")
            
            # 状态异常
            status = module.get('status', '').lower()
            if status in ['failed', 'error', 'blocked']:
                issues.append(f"状态异常: {status}")
            
            # 缺少负责人
            if not module.get('owner'):
                issues.append("缺少负责人")
            
            if issues:
                self.analysis["issues"].append({
                    "module_name": module.get('module_name', 'unknown'),
                    "issues": issues
                })


def main():
    parser = argparse.ArgumentParser(description='分析应用模块状态数据')
    parser.add_argument('--input', required=True, help='应用状态JSON文件路径')
    parser.add_argument('--output', required=True, help='输出分析结果JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        analyzer = AppStatusAnalyzer(args.input)
        analysis = analyzer.analyze()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"应用状态分析完成，输出文件: {args.output}")
        print(f"模块数量: {len(analysis['module_status'])}")
        print(f"问题模块: {len(analysis['issues'])}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
