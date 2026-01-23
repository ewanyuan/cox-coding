#!/usr/bin/env python3
"""
可观测日志生成器（简单方案）
生成结构化的可观测日志，可在终端查看或使用工具分析
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


class ObservabilityLogGenerator:
    """可观测日志生成器"""

    def __init__(self, project_data, app_data, test_data):
        self.project_data = project_data
        self.app_data = app_data
        self.test_data = test_data
        self.lines = []

    def add_line(self, prefix, content):
        """添加日志行"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.lines.append(f"[{timestamp}] {prefix} {content}")

    def generate_project_section(self):
        """生成项目维度日志"""
        self.add_line("=" * 70, "")
        self.add_line("PROJECT", f"项目名称: {self.project_data['project_name']}")
        self.add_line("PROJECT", f"当前迭代: {self.project_data['current_iteration']}")
        self.add_line("PROJECT", "")

        for iteration in self.project_data['iterations']:
            self.add_line("PROJECT", f"迭代: {iteration['iteration_name']} ({iteration['iteration_id']})")
            self.add_line("PROJECT", f"  状态: {iteration['status']}")
            if 'start_date' in iteration:
                self.add_line("PROJECT", f"  时间: {iteration['start_date']} ~ {iteration.get('end_date', '进行中')}")

            # 任务统计
            status_count = {}
            for task in iteration['tasks']:
                status = task['status']
                status_count[status] = status_count.get(status, 0) + 1

            self.add_line("PROJECT", f"  任务统计: {dict(status_count)}")

            # 任务列表
            self.add_line("PROJECT", f"  任务列表:")
            for task in iteration['tasks']:
                task_info = f"    - {task['task_name']} ({task['status']})"
                if 'assignee' in task:
                    task_info += f" [{task['assignee']}]"
                self.add_line("PROJECT", task_info)

            # 假设列表
            if iteration.get('assumptions'):
                self.add_line("PROJECT", f"  假设列表:")
                for assumption in iteration['assumptions']:
                    assumption_info = f"    - {assumption['description']} ({assumption['status']})"
                    self.add_line("PROJECT", assumption_info)

            self.add_line("PROJECT", "")

    def generate_app_section(self):
        """生成应用维度日志"""
        self.add_line("=" * 70, "")
        self.add_line("APP", f"应用名称: {self.app_data['app_name']}")
        self.add_line("APP", f"版本: {self.app_data.get('version', 'N/A')}")
        self.add_line("APP", f"最后更新: {self.app_data['last_updated']}")
        self.add_line("APP", "")

        # 模块状态统计
        status_count = {}
        for module in self.app_data['modules']:
            status = module['status']
            status_count[status] = status_count.get(status, 0) + 1
        self.add_line("APP", f"模块状态统计: {dict(status_count)}")
        self.add_line("APP", "")

        # 模块列表
        self.add_line("APP", f"模块列表:")
        for module in self.app_data['modules']:
            module_info = f"  - {module['module_name']}"
            module_info += f" [{module['status']}]"
            if 'completion_rate' in module:
                module_info += f" (完成率: {module['completion_rate']*100:.1f}%)"
            if 'owner' in module:
                module_info += f" [负责人: {module['owner']}]"
            self.add_line("APP", module_info)
            if 'notes' in module:
                self.add_line("APP", f"    备注: {module['notes']}")

        self.add_line("APP", "")

    def generate_test_section(self):
        """生成测试维度日志"""
        self.add_line("=" * 70, "")
        self.add_line("TEST", f"最后更新: {self.test_data['last_updated']}")
        self.add_line("TEST", "")

        # 测试套件
        self.add_line("TEST", f"测试套件:")
        for suite in self.test_data['test_suites']:
            pass_rate = (suite['passed_tests'] / suite['total_tests'] * 100) if suite['total_tests'] > 0 else 0
            suite_info = f"  - {suite['suite_name']}"
            suite_info += f" (总计: {suite['total_tests']}, 通过: {suite['passed_tests']}, 失败: {suite['failed_tests']}, 跳过: {suite['skipped_tests']})"
            suite_info += f" [通过率: {pass_rate:.1f}%]"
            if 'coverage' in suite:
                suite_info += f" [覆盖率: {suite['coverage']*100:.1f}%]"
            self.add_line("TEST", suite_info)
            self.add_line("TEST", f"    最后运行: {suite['last_run']}")

        self.add_line("TEST", "")

        # 埋点状态
        self.add_line("TEST", f"埋点状态:")
        status_count = {}
        for point in self.test_data['tracing_points']:
            status = point['status']
            status_count[status] = status_count.get(status, 0) + 1
        self.add_line("TEST", f"  统计: {dict(status_count)}")

        for point in self.test_data['tracing_points']:
            point_info = f"  - {point['module']}: {point['location']}"
            point_info += f" [{point['metric_type']}, {point['status']}]"
            self.add_line("TEST", point_info)

        self.add_line("TEST", "")

        # 异常分析
        if self.test_data['anomalies']:
            self.add_line("TEST", f"异常分析:")
            severity_count = {}
            for anomaly in self.test_data['anomalies']:
                severity = anomaly['severity']
                severity_count[severity] = severity_count.get(severity, 0) + 1
            self.add_line("TEST", f"  统计: {dict(severity_count)}")

            for anomaly in self.test_data['anomalies']:
                anomaly_info = f"  - [{anomaly['severity']}] {anomaly['description']}"
                anomaly_info += f" ({anomaly['type']}, {anomaly['status']})"
                self.add_line("TEST", anomaly_info)
                self.add_line("TEST", f"    发生次数: {anomaly['occurrence_count']}")
                self.add_line("TEST", f"    时间范围: {anomaly['first_occurred']} ~ {anomaly['last_occurred']}")
        else:
            self.add_line("TEST", f"异常分析: 无异常")

        self.add_line("TEST", "")

    def generate_summary(self):
        """生成摘要"""
        self.add_line("=" * 70, "")
        self.add_line("SUMMARY", "可观测摘要")

        # 项目摘要
        total_iterations = len(self.project_data['iterations'])
        total_tasks = sum(len(iteration['tasks']) for iteration in self.project_data['iterations'])
        self.add_line("SUMMARY", f"  项目: {self.project_data['project_name']} - {total_iterations}个迭代, {total_tasks}个任务")

        # 应用摘要
        total_modules = len(self.app_data['modules'])
        avg_completion = sum(m.get('completion_rate', 0) for m in self.app_data['modules']) / total_modules if total_modules > 0 else 0
        self.add_line("SUMMARY", f"  应用: {self.app_data['app_name']} - {total_modules}个模块, 平均完成率: {avg_completion*100:.1f}%")

        # 测试摘要
        total_tests = sum(suite['total_tests'] for suite in self.test_data['test_suites'])
        total_passed = sum(suite['passed_tests'] for suite in self.test_data['test_suites'])
        total_anomalies = len(self.test_data['anomalies'])
        test_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        self.add_line("SUMMARY", f"  测试: {total_tests}个测试用例, 通过率: {test_pass_rate:.1f}%, 异常数: {total_anomalies}")

        self.add_line("=", "=" * 70)

    def generate(self):
        """生成完整日志"""
        self.add_line("", "")
        self.add_line("", "开发阶段可观测日志")
        self.add_line("", "")

        self.generate_project_section()
        self.generate_app_section()
        self.generate_test_section()
        self.generate_summary()

        return '\n'.join(self.lines)

    def print_and_save(self, output_file):
        """打印并保存日志"""
        log_content = self.generate()

        # 输出到终端
        print(log_content)

        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(log_content)

        print(f"\n日志已保存到: {output_file}")


def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON格式错误: {file_path}")
        print(f"详情: {e}")
        exit(1)


def main():
    parser = argparse.ArgumentParser(description='可观测日志生成器（简单方案）')
    parser.add_argument('--project', required=True, help='项目数据文件路径')
    parser.add_argument('--app', required=True, help='应用状态文件路径')
    parser.add_argument('--test', required=True, help='测试指标文件路径')
    parser.add_argument('--output', default='observability.log', help='输出日志文件路径')

    args = parser.parse_args()

    # 加载数据文件
    print("加载数据文件...")
    project_data = load_json_file(args.project)
    app_data = load_json_file(args.app)
    test_data = load_json_file(args.test)

    # 生成日志
    print("生成可观测日志...")
    print("-" * 70)
    generator = ObservabilityLogGenerator(project_data, app_data, test_data)
    generator.print_and_save(args.output)

    print("\n日志生成完成!")
    print("\n提示: 可以使用以下命令分析日志:")
    print(f"  cat {args.output}")
    print(f"  grep 'PROJECT:' {args.output}")
    print(f"  grep 'APP:' {args.output}")
    print(f"  grep 'ANOMALY:' {args.output}")


if __name__ == '__main__':
    main()
