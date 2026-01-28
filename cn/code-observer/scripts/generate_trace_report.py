#!/usr/bin/env python3
"""
整合多维数据，生成全流程可视化追踪报告
"""

import json
import sys
import argparse
from typing import Dict, Any, Optional
from datetime import datetime


class TraceReportGenerator:
    """追踪报告生成器"""
    
    def __init__(self):
        self.logs_data = None
        self.metrics_data = None
        self.app_status = None
        self.project_data = None
        self.test_metrics = None
    
    def generate(self, args) -> str:
        """生成追踪报告"""
        # 加载数据
        if args.logs:
            self.logs_data = self._load_json(args.logs)
        if args.metrics:
            self.metrics_data = self._load_json(args.metrics)
        if args.app_status:
            self.app_status = self._load_json(args.app_status)
        if args.project_data:
            self.project_data = self._load_json(args.project_data)
        if args.test_metrics:
            self.test_metrics = self._load_json(args.test_metrics)
        
        # 生成报告
        report = self._build_report()
        
        # 写入文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def _load_json(self, filepath: str) -> Dict[str, Any]:
        """加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: 加载文件 {filepath} 失败: {str(e)}", file=sys.stderr)
            return None
    
    def _build_report(self) -> str:
        """构建报告"""
        report_lines = []
        
        # 报告标题
        report_lines.append("# 代码级观测追踪报告")
        report_lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 1. 执行路径追踪
        report_lines.append(self._generate_execution_trace_section())
        
        # 2. 性能指标分析
        report_lines.append(self._generate_performance_metrics_section())
        
        # 3. 异常追踪分析
        report_lines.append(self._generate_error_analysis_section())
        
        # 4. 跨维度关联分析
        report_lines.append(self._generate_cross_dimension_analysis_section())
        
        # 5. 问题总结
        report_lines.append(self._generate_issue_summary_section())
        
        return "\n".join(report_lines)
    
    def _generate_execution_trace_section(self) -> str:
        """生成执行追踪部分"""
        lines = []
        lines.append("## 1. 执行路径追踪")
        lines.append("")
        
        if not self.logs_data:
            lines.append("*无日志数据*")
            lines.append("")
            return "\n".join(lines)
        
        execution_paths = self.logs_data.get("execution_paths", [])
        function_calls = self.logs_data.get("function_calls", [])
        
        lines.append(f"**执行路径总数**: {len(execution_paths)}")
        lines.append(f"**函数调用次数**: {len(function_calls)}")
        lines.append("")
        
        # 执行路径时间轴
        if execution_paths:
            lines.append("### 执行路径时间轴")
            lines.append("")
            lines.append("| 时间戳 | 级别 | 消息 |")
            lines.append("|--------|------|------|")
            
            for path in execution_paths[:20]:  # 限制显示数量
                timestamp = path.get("timestamp", "")[:19]  # 截取到秒
                level = path.get("level", "")
                message = path.get("message", "")[:50]
                lines.append(f"| {timestamp} | {level} | {message}... |")
            
            lines.append("")
        
        # 函数调用链
        if function_calls:
            lines.append("### 函数调用链")
            lines.append("")
            lines.append("| 时间戳 | 函数名 | 耗时(ms) | 级别 |")
            lines.append("|--------|--------|----------|------|")
            
            # 按耗时排序
            sorted_calls = sorted(function_calls, key=lambda x: x.get("duration_ms", 0), reverse=True)
            
            for call in sorted_calls[:15]:  # 限制显示数量
                timestamp = call.get("timestamp", "")[:19]
                function = call.get("function", "")
                duration = call.get("duration_ms", 0)
                level = call.get("level", "")
                lines.append(f"| {timestamp} | {function} | {duration:.2f} | {level} |")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_performance_metrics_section(self) -> str:
        """生成性能指标部分"""
        lines = []
        lines.append("## 2. 性能指标分析")
        lines.append("")
        
        if self.logs_data:
            summary = self.logs_data.get("summary", {})
            lines.append("### 日志性能统计")
            lines.append("")
            lines.append(f"- **平均耗时**: {summary.get('avg_duration_ms', 0):.2f} ms")
            lines.append(f"- **最大耗时**: {summary.get('max_duration_ms', 0):.2f} ms")
            lines.append(f"- **函数调用总数**: {summary.get('total_function_calls', 0)}")
            lines.append("")
        
        if self.metrics_data:
            lines.append("### Prometheus指标")
            lines.append("")
            gauge_count = len(self.metrics_data.get("gauge_metrics", []))
            counter_count = len(self.metrics_data.get("counter_metrics", []))
            lines.append(f"- **Gauge指标**: {gauge_count}")
            lines.append(f"- **Counter指标**: {counter_count}")
            lines.append("")
            
            # 显示高耗时指标
            gauge_metrics = self.metrics_data.get("gauge_metrics", [])
            if gauge_metrics:
                lines.append("### 高耗时操作")
                lines.append("")
                lines.append("| 指标名称 | 标签 | 值 |")
                lines.append("|----------|------|-----|")
                
                sorted_metrics = sorted(gauge_metrics, key=lambda x: x.get("value", 0), reverse=True)
                
                for metric in sorted_metrics[:10]:
                    name = metric.get("name", "")
                    labels = ", ".join([f"{k}={v}" for k, v in metric.get("labels", {}).items()])
                    value = metric.get("value", 0)
                    lines.append(f"| {name} | {labels} | {value:.2f} |")
                
                lines.append("")
        
        if not self.logs_data and not self.metrics_data:
            lines.append("*无性能数据*")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_error_analysis_section(self) -> str:
        """生成异常分析部分"""
        lines = []
        lines.append("## 3. 异常追踪分析")
        lines.append("")
        
        if not self.logs_data:
            lines.append("*无日志数据*")
            lines.append("")
            return "\n".join(lines)
        
        exceptions = self.logs_data.get("exceptions", [])
        
        lines.append(f"**异常总数**: {len(exceptions)}")
        lines.append("")
        
        if exceptions:
            lines.append("### 异常列表")
            lines.append("")
            lines.append("| 时间戳 | 级别 | 异常类型 | 异常消息 |")
            lines.append("|--------|------|----------|----------|")
            
            for exc in exceptions[:15]:  # 限制显示数量
                timestamp = exc.get("timestamp", "")[:19]
                level = exc.get("level", "")
                exc_type = exc.get("exception_type", "")
                exc_message = exc.get("exception_message", "")[:40]
                lines.append(f"| {timestamp} | {level} | {exc_type} | {exc_message}... |")
            
            lines.append("")
            
            # 异常类型统计
            exc_type_counts = {}
            for exc in exceptions:
                exc_type = exc.get("exception_type", "Unknown")
                exc_type_counts[exc_type] = exc_type_counts.get(exc_type, 0) + 1
            
            if exc_type_counts:
                lines.append("### 异常类型分布")
                lines.append("")
                for exc_type, count in sorted(exc_type_counts.items(), key=lambda x: x[1], reverse=True):
                    lines.append(f"- **{exc_type}**: {count} 次")
                lines.append("")
        
        else:
            lines.append("*无异常记录*")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_cross_dimension_analysis_section(self) -> str:
        """生成跨维度关联分析部分"""
        lines = []
        lines.append("## 4. 跨维度关联分析")
        lines.append("")
        
        # 应用状态关联
        if self.app_status:
            lines.append("### 应用模块状态")
            lines.append("")
            module_status = self.app_status.get("module_status", {})
            
            for module_name, status in list(module_status.items())[:10]:
                status_str = status.get("status", "")
                completion = status.get("completion_rate", 0)
                owner = status.get("owner", "unknown")
                lines.append(f"- **{module_name}**: {status_str} (完成率: {completion}%, 负责人: {owner})")
            
            lines.append("")
        
        # 项目进度关联
        if self.project_data:
            lines.append("### 项目迭代进度")
            lines.append("")
            iteration_progress = self.project_data.get("iteration_progress", {})
            
            for iter_name, progress in list(iteration_progress.items())[:10]:
                completion_rate = progress.get("completion_rate", 0)
                status = progress.get("status", "")
                lines.append(f"- **{iter_name}**: {status} (完成率: {completion_rate:.1f}%)")
            
            lines.append("")
        
        # 测试指标关联
        if self.test_metrics:
            lines.append("### 测试指标")
            lines.append("")
            test_results = self.test_metrics.get("test_suite_results", {})
            
            for suite_name, results in list(test_results.items())[:10]:
                passed = results.get("passed_tests", 0)
                total = results.get("total_tests", 0)
                success_rate = results.get("success_rate", 0)
                lines.append(f"- **{suite_name}**: {passed}/{total} 通过 (成功率: {success_rate:.1f}%)")
            
            lines.append("")
        
        if not self.app_status and not self.project_data and not self.test_metrics:
            lines.append("*无跨维度数据*")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_issue_summary_section(self) -> str:
        """生成问题总结部分"""
        lines = []
        lines.append("## 5. 问题总结")
        lines.append("")
        
        issues = []
        
        # 从日志数据中提取问题
        if self.logs_data:
            exceptions = self.logs_data.get("exceptions", [])
            if exceptions:
                issues.append({
                    "category": "日志异常",
                    "count": len(exceptions),
                    "details": f"发现 {len(exceptions)} 个异常记录"
                })
            
            function_calls = self.logs_data.get("function_calls", [])
            high_duration_calls = [fc for fc in function_calls if fc.get("duration_ms", 0) > 1000]
            if high_duration_calls:
                issues.append({
                    "category": "性能瓶颈",
                    "count": len(high_duration_calls),
                    "details": f"发现 {len(high_duration_calls)} 个耗时超过1秒的函数调用"
                })
        
        # 从应用状态中提取问题
        if self.app_status:
            app_issues = self.app_status.get("issues", [])
            if app_issues:
                issues.append({
                    "category": "应用模块问题",
                    "count": len(app_issues),
                    "details": f"发现 {len(app_issues)} 个模块问题"
                })
        
        # 从项目数据中提取问题
        if self.project_data:
            project_risks = self.project_data.get("risks", [])
            if project_risks:
                issues.append({
                    "category": "项目风险",
                    "count": len(project_risks),
                    "details": f"识别 {len(project_risks)} 个项目风险"
                })
        
        # 从测试指标中提取问题
        if self.test_metrics:
            test_issues = self.test_metrics.get("issues", [])
            if test_issues:
                issues.append({
                    "category": "测试问题",
                    "count": len(test_issues),
                    "details": f"发现 {len(test_issues)} 个测试相关问题"
                })
        
        if issues:
            lines.append("### 问题汇总")
            lines.append("")
            lines.append("| 类别 | 数量 | 详情 |")
            lines.append("|------|------|------|")
            
            for issue in issues:
                category = issue.get("category", "")
                count = issue.get("count", 0)
                details = issue.get("details", "")
                lines.append(f"| {category} | {count} | {details} |")
            
            lines.append("")
        else:
            lines.append("*未发现明显问题*")
            lines.append("")
        
        # 生成建议
        lines.append("### 建议")
        lines.append("")
        
        if not self.logs_data:
            lines.append("- 请提供日志数据以进行执行路径分析")
        else:
            lines.append("- 建议优先处理异常追踪部分的异常问题")
            lines.append("- 建议优化高耗时的函数调用")
        
        if not self.metrics_data:
            lines.append("- 建议提供Prometheus指标数据以进行深度性能分析")
        
        lines.append("- 建议定期进行全流程追踪，及时发现性能瓶颈和异常")
        lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='生成全流程可视化追踪报告')
    parser.add_argument('--logs', help='解析后的日志数据JSON文件路径')
    parser.add_argument('--metrics', help='解析后的Prometheus指标JSON文件路径')
    parser.add_argument('--app-status', help='应用状态分析结果JSON文件路径')
    parser.add_argument('--project-data', help='项目数据分析结果JSON文件路径')
    parser.add_argument('--test-metrics', help='测试指标分析结果JSON文件路径')
    parser.add_argument('--output', required=True, help='输出追踪报告MD文件路径')
    
    args = parser.parse_args()
    
    try:
        generator = TraceReportGenerator()
        generator.generate(args)
        
        print(f"追踪报告生成完成，输出文件: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
