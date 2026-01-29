#!/usr/bin/env python3
"""
分析测试指标数据，提取测试套件结果、埋点状态、异常列表等信息
"""

import json
import sys
import argparse
from typing import Dict, List, Any


class TestMetricsAnalyzer:
    """测试指标分析器"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.analysis = {
            "test_suite_results": {},
            "tracking_points": {},
            "exception_summary": {},
            "coverage_stats": {},
            "issues": []
        }
    
    def analyze(self) -> Dict[str, Any]:
        """分析测试指标数据"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 分析测试套件结果
            self._analyze_test_suite_results(data)
            
            # 分析埋点状态
            self._analyze_tracking_points(data)
            
            # 分析异常情况
            self._analyze_exceptions(data)
            
            # 分析覆盖率
            self._analyze_coverage(data)
            
            # 识别问题
            self._identify_issues(data)
            
            return self.analysis
            
        except FileNotFoundError:
            raise Exception(f"测试指标文件不存在: {self.input_file}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")
        except Exception as e:
            raise Exception(f"分析测试指标失败: {str(e)}")
    
    def _analyze_test_suite_results(self, data: Dict[str, Any]):
        """分析测试套件结果"""
        test_suites = data.get('test_suites', [])
        
        for suite in test_suites:
            suite_name = suite.get('name', 'unknown')
            total_tests = suite.get('total_tests', 0)
            passed_tests = suite.get('passed_tests', 0)
            failed_tests = suite.get('failed_tests', 0)
            skipped_tests = suite.get('skipped_tests', 0)
            
            self.analysis["test_suite_results"][suite_name] = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "skipped_tests": skipped_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "execution_time": suite.get('execution_time', 0)
            }
    
    def _analyze_tracking_points(self, data: Dict[str, Any]):
        """分析埋点状态"""
        tracking_points = data.get('tracking_points', [])
        
        total_points = len(tracking_points)
        active_points = len([tp for tp in tracking_points if tp.get('status', '').lower() == 'active'])
        inactive_points = total_points - active_points
        
        self.analysis["tracking_points"] = {
            "total_points": total_points,
            "active_points": active_points,
            "inactive_points": inactive_points,
            "details": tracking_points
        }
    
    def _analyze_exceptions(self, data: Dict[str, Any]):
        """分析异常情况"""
        exceptions = data.get('exceptions', [])
        
        # 按异常类型分组
        exception_types = {}
        for exc in exceptions:
            exc_type = exc.get('type', 'unknown')
            exception_types[exc_type] = exception_types.get(exc_type, 0) + 1
        
        self.analysis["exception_summary"] = {
            "total_exceptions": len(exceptions),
            "exception_types": exception_types,
            "details": exceptions
        }
    
    def _analyze_coverage(self, data: Dict[str, Any]):
        """分析测试覆盖率"""
        coverage = data.get('coverage', {})
        
        self.analysis["coverage_stats"] = {
            "line_coverage": coverage.get('line_coverage', 0),
            "branch_coverage": coverage.get('branch_coverage', 0),
            "function_coverage": coverage.get('function_coverage', 0),
            "statement_coverage": coverage.get('statement_coverage', 0)
        }
    
    def _identify_issues(self, data: Dict[str, Any]):
        """识别问题"""
        issues = []
        
        # 检查测试失败
        for suite_name, results in self.analysis["test_suite_results"].items():
            if results["failed_tests"] > 0:
                issues.append({
                    "type": "测试失败",
                    "description": f"测试套件 {suite_name} 有 {results['failed_tests']} 个测试失败",
                    "severity": "high"
                })
        
        # 检查埋点问题
        if self.analysis["tracking_points"].get("inactive_points", 0) > 0:
            issues.append({
                "type": "埋点未激活",
                "description": f"{self.analysis['tracking_points']['inactive_points']} 个埋点未激活",
                "severity": "medium"
            })
        
        # 检查异常数量
        if self.analysis["exception_summary"].get("total_exceptions", 0) > 0:
            issues.append({
                "type": "测试异常",
                "description": f"测试过程中发现 {self.analysis['exception_summary']['total_exceptions']} 个异常",
                "severity": "high"
            })
        
        # 检查覆盖率
        if self.analysis["coverage_stats"].get("line_coverage", 0) < 80:
            issues.append({
                "type": "覆盖率不足",
                "description": f"行覆盖率仅 {self.analysis['coverage_stats']['line_coverage']:.1f}%，低于80%",
                "severity": "medium"
            })
        
        self.analysis["issues"] = issues


def main():
    parser = argparse.ArgumentParser(description='分析测试指标数据')
    parser.add_argument('--input', required=True, help='测试指标JSON文件路径')
    parser.add_argument('--output', required=True, help='输出分析结果JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        analyzer = TestMetricsAnalyzer(args.input)
        analysis = analyzer.analyze()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"测试指标分析完成，输出文件: {args.output}")
        print(f"测试套件: {len(analysis['test_suite_results'])}")
        print(f"埋点数量: {analysis['tracking_points']['total_points']}")
        print(f"异常数量: {analysis['exception_summary']['total_exceptions']}")
        print(f"问题数量: {len(analysis['issues'])}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
