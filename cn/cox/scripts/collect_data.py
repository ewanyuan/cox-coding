#!/usr/bin/env python3
"""
可观测数据采集工具
用于验证和导出可观测数据
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


class DataValidator:
    """数据格式验证器"""

    # 枚举值定义
    ITERATION_STATUS = ['not_started', 'in_progress', 'completed', 'delayed']
    TASK_STATUS = ['todo', 'in_progress', 'review', 'done', 'blocked']
    TASK_PRIORITY = ['low', 'medium', 'high', 'critical']
    ASSUMPTION_STATUS = ['pending', 'validated', 'invalidated']
    MODULE_STATUS = ['pending', 'developed', 'confirmed', 'optimized']
    TRACING_METRIC_TYPE = ['counter', 'gauge', 'histogram', 'summary']
    TRACING_STATUS = ['active', 'inactive', 'deprecated']
    ANOMALY_TYPE = ['performance', 'functional', 'integration', 'security']
    ANOMALY_SEVERITY = ['low', 'medium', 'high', 'critical']
    ANOMALY_STATUS = ['open', 'investigating', 'resolved', 'ignored']

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_date_format(self, date_str, allow_none=True):
        """验证日期格式"""
        if date_str is None and allow_none:
            return True

        if date_str is None:
            self.errors.append("日期字段不能为空")
            return False

        try:
            # 尝试解析两种格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
            if ' ' in date_str:
                datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            else:
                datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            self.errors.append(f"日期格式错误: {date_str}，应为 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS")
            return False

    def validate_project_data(self, data):
        """验证项目数据格式"""
        if not isinstance(data, dict):
            self.errors.append("project_data.json 必须是 JSON 对象")
            return False

        # 必填字段
        required_fields = ['project_name', 'current_iteration', 'iterations']
        for field in required_fields:
            if field not in data:
                self.errors.append(f"project_data.json 缺少必填字段: {field}")

        # 验证迭代列表
        if 'iterations' in data:
            if not isinstance(data['iterations'], list):
                self.errors.append("iterations 必须是数组")
            else:
                for iteration in data['iterations']:
                    self._validate_iteration(iteration)

        return len(self.errors) == 0

    def _validate_iteration(self, iteration):
        """验证迭代数据"""
        required_fields = ['iteration_id', 'iteration_name', 'status', 'tasks', 'assumptions']
        for field in required_fields:
            if field not in iteration:
                self.errors.append(f"迭代缺少必填字段: {field}")

        # 验证状态枚举
        if 'status' in iteration and iteration['status'] not in self.ITERATION_STATUS:
            self.errors.append(
                f"迭代状态 '{iteration['status']}' 无效，允许的值: {self.ITERATION_STATUS}"
            )

        # 验证日期
        if 'start_date' in iteration:
            self.validate_date_format(iteration['start_date'])
        if 'end_date' in iteration:
            self.validate_date_format(iteration['end_date'])

        # 验证任务列表
        if 'tasks' in iteration:
            if not isinstance(iteration['tasks'], list):
                self.errors.append("tasks 必须是数组")
            else:
                for task in iteration['tasks']:
                    self._validate_task(task)

        # 验证假设列表
        if 'assumptions' in iteration:
            if not isinstance(iteration['assumptions'], list):
                self.errors.append("assumptions 必须是数组")
            else:
                for assumption in iteration['assumptions']:
                    self._validate_assumption(assumption)

    def _validate_task(self, task):
        """验证任务数据"""
        required_fields = ['task_id', 'task_name', 'status']
        for field in required_fields:
            if field not in task:
                self.errors.append(f"任务缺少必填字段: {field}")

        # 验证状态枚举
        if 'status' in task and task['status'] not in self.TASK_STATUS:
            self.errors.append(
                f"任务状态 '{task['status']}' 无效，允许的值: {self.TASK_STATUS}"
            )

        # 验证优先级枚举
        if 'priority' in task and task['priority'] not in self.TASK_PRIORITY:
            self.errors.append(
                f"任务优先级 '{task['priority']}' 无效，允许的值: {self.TASK_PRIORITY}"
            )

    def _validate_assumption(self, assumption):
        """验证假设数据"""
        required_fields = ['assumption_id', 'description', 'status']
        for field in required_fields:
            if field not in assumption:
                self.errors.append(f"假设缺少必填字段: {field}")

        # 验证状态枚举
        if 'status' in assumption and assumption['status'] not in self.ASSUMPTION_STATUS:
            self.errors.append(
                f"假设状态 '{assumption['status']}' 无效，允许的值: {self.ASSUMPTION_STATUS}"
            )

        # 验证日期
        if 'validation_date' in assumption:
            self.validate_date_format(assumption['validation_date'])

    def validate_app_status(self, data):
        """验证应用状态数据格式"""
        if not isinstance(data, dict):
            self.errors.append("app_status.json 必须是 JSON 对象")
            return False

        # 必填字段
        required_fields = ['app_name', 'last_updated', 'modules']
        for field in required_fields:
            if field not in data:
                self.errors.append(f"app_status.json 缺少必填字段: {field}")

        # 验证日期
        if 'last_updated' in data:
            self.validate_date_format(data['last_updated'], allow_none=False)

        # 验证模块列表
        if 'modules' in data:
            if not isinstance(data['modules'], list):
                self.errors.append("modules 必须是数组")
            else:
                for module in data['modules']:
                    self._validate_module(module)

        return len(self.errors) == 0

    def _validate_module(self, module):
        """验证模块数据"""
        required_fields = ['module_name', 'status']
        for field in required_fields:
            if field not in module:
                self.errors.append(f"模块缺少必填字段: {field}")

        # 验证状态枚举
        if 'status' in module and module['status'] not in self.MODULE_STATUS:
            self.errors.append(
                f"模块状态 '{module['status']}' 无效，允许的值: {self.MODULE_STATUS}"
            )

        # 验证完成率
        if 'completion_rate' in module:
            if not isinstance(module['completion_rate'], (int, float)):
                self.errors.append("completion_rate 必须是数字")
            elif not (0.0 <= module['completion_rate'] <= 1.0):
                self.errors.append(
                    f"completion_rate 值 {module['completion_rate']} 超出范围 [0.0, 1.0]"
                )

        # 验证日期
        if 'last_update' in module:
            self.validate_date_format(module['last_update'])

    def validate_test_metrics(self, data):
        """验证测试指标数据格式"""
        if not isinstance(data, dict):
            self.errors.append("test_metrics.json 必须是 JSON 对象")
            return False

        # 必填字段
        required_fields = ['last_updated', 'test_suites', 'tracing_points', 'anomalies']
        for field in required_fields:
            if field not in data:
                self.errors.append(f"test_metrics.json 缺少必填字段: {field}")

        # 验证日期
        if 'last_updated' in data:
            self.validate_date_format(data['last_updated'], allow_none=False)

        # 验证测试套件列表
        if 'test_suites' in data:
            if not isinstance(data['test_suites'], list):
                self.errors.append("test_suites 必须是数组")
            else:
                for suite in data['test_suites']:
                    self._validate_test_suite(suite)

        # 验证埋点列表
        if 'tracing_points' in data:
            if not isinstance(data['tracing_points'], list):
                self.errors.append("tracing_points 必须是数组")
            else:
                for point in data['tracing_points']:
                    self._validate_tracing_point(point)

        # 验证异常列表
        if 'anomalies' in data:
            if not isinstance(data['anomalies'], list):
                self.errors.append("anomalies 必须是数组")
            else:
                for anomaly in data['anomalies']:
                    self._validate_anomaly(anomaly)

        return len(self.errors) == 0

    def _validate_test_suite(self, suite):
        """验证测试套件数据"""
        required_fields = ['suite_name', 'total_tests', 'passed_tests', 'failed_tests',
                          'skipped_tests', 'last_run']
        for field in required_fields:
            if field not in suite:
                self.errors.append(f"测试套件缺少必填字段: {field}")

        # 验证数值关系
        if all(k in suite for k in ['total_tests', 'passed_tests', 'failed_tests', 'skipped_tests']):
            total = suite['total_tests']
            if suite['passed_tests'] > total:
                self.errors.append("passed_tests 不能大于 total_tests")
            if suite['failed_tests'] > total:
                self.errors.append("failed_tests 不能大于 total_tests")
            if suite['skipped_tests'] > total:
                self.errors.append("skipped_tests 不能大于 total_tests")

        # 验证覆盖率
        if 'coverage' in suite:
            if not isinstance(suite['coverage'], (int, float)):
                self.errors.append("coverage 必须是数字")
            elif not (0.0 <= suite['coverage'] <= 1.0):
                self.errors.append(f"coverage 值 {suite['coverage']} 超出范围 [0.0, 1.0]")

        # 验证日期
        if 'last_run' in suite:
            self.validate_date_format(suite['last_run'])

    def _validate_tracing_point(self, point):
        """验证埋点数据"""
        required_fields = ['point_id', 'module', 'location', 'metric_type', 'status',
                          'last_verified']
        for field in required_fields:
            if field not in point:
                self.errors.append(f"埋点缺少必填字段: {field}")

        # 验证指标类型枚举
        if 'metric_type' in point and point['metric_type'] not in self.TRACING_METRIC_TYPE:
            self.errors.append(
                f"埋点指标类型 '{point['metric_type']}' 无效，允许的值: {self.TRACING_METRIC_TYPE}"
            )

        # 验证状态枚举
        if 'status' in point and point['status'] not in self.TRACING_STATUS:
            self.errors.append(
                f"埋点状态 '{point['status']}' 无效，允许的值: {self.TRACING_STATUS}"
            )

        # 验证日期
        if 'last_verified' in point:
            self.validate_date_format(point['last_verified'])

    def _validate_anomaly(self, anomaly):
        """验证异常数据"""
        required_fields = ['anomaly_id', 'type', 'severity', 'description',
                          'first_occurred', 'last_occurred', 'occurrence_count', 'status']
        for field in required_fields:
            if field not in anomaly:
                self.errors.append(f"异常缺少必填字段: {field}")

        # 验证异常类型枚举
        if 'type' in anomaly and anomaly['type'] not in self.ANOMALY_TYPE:
            self.errors.append(
                f"异常类型 '{anomaly['type']}' 无效，允许的值: {self.ANOMALY_TYPE}"
            )

        # 验证严重程度枚举
        if 'severity' in anomaly and anomaly['severity'] not in self.ANOMALY_SEVERITY:
            self.errors.append(
                f"异常严重程度 '{anomaly['severity']}' 无效，允许的值: {self.ANOMALY_SEVERITY}"
            )

        # 验证状态枚举
        if 'status' in anomaly and anomaly['status'] not in self.ANOMALY_STATUS:
            self.errors.append(
                f"异常处理状态 '{anomaly['status']}' 无效，允许的值: {self.ANOMALY_STATUS}"
            )

        # 验证日期
        if 'first_occurred' in anomaly:
            self.validate_date_format(anomaly['first_occurred'])
        if 'last_occurred' in anomaly:
            self.validate_date_format(anomaly['last_occurred'])


def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON格式错误: {file_path}")
        print(f"详情: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='可观测数据采集工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 验证命令
    validate_parser = subparsers.add_parser('validate', help='验证数据格式')
    validate_parser.add_argument('--project', required=True, help='项目数据文件')
    validate_parser.add_argument('--app', required=True, help='应用状态文件')
    validate_parser.add_argument('--test', required=True, help='测试指标文件')

    # 导出Prometheus指标命令
    export_parser = subparsers.add_parser('export-prometheus', help='导出Prometheus指标格式')
    export_parser.add_argument('--project', required=True, help='项目数据文件')
    export_parser.add_argument('--app', required=True, help='应用状态文件')
    export_parser.add_argument('--test', required=True, help='测试指标文件')
    export_parser.add_argument('--output', default='metrics.prom', help='输出文件')

    args = parser.parse_args()

    if args.command == 'validate':
        validator = DataValidator()

        # 加载数据文件
        project_data = load_json_file(args.project)
        app_data = load_json_file(args.app)
        test_data = load_json_file(args.test)

        # 验证数据
        print("验证数据格式...")
        print("-" * 50)

        print("验证 project_data.json...")
        if validator.validate_project_data(project_data):
            print("[OK] project_data.json 验证通过")
        else:
            print("[FAIL] project_data.json 验证失败")
            for error in validator.errors:
                print(f"  - {error}")

        print("-" * 50)

        # 重置错误列表
        validator.errors = []

        print("验证 app_status.json...")
        if validator.validate_app_status(app_data):
            print("[OK] app_status.json 验证通过")
        else:
            print("[FAIL] app_status.json 验证失败")
            for error in validator.errors:
                print(f"  - {error}")

        print("-" * 50)

        validator.errors = []

        print("验证 test_metrics.json...")
        if validator.validate_test_metrics(test_data):
            print("[OK] test_metrics.json 验证通过")
        else:
            print("[FAIL] test_metrics.json 验证失败")
            for error in validator.errors:
                print(f"  - {error}")

        print("-" * 50)

    elif args.command == 'export-prometheus':
        # 加载数据文件
        project_data = load_json_file(args.project)
        app_data = load_json_file(args.app)
        test_data = load_json_file(args.test)

        # 验证数据
        validator = DataValidator()
        if not (validator.validate_project_data(project_data) and
                validator.validate_app_status(app_data) and
                validator.validate_test_metrics(test_data)):
            print("错误: 数据格式验证失败，无法导出")
            sys.exit(1)

        # 导出Prometheus指标
        print(f"导出Prometheus指标到 {args.output}...")
        with open(args.output, 'w', encoding='utf-8') as f:
            # 项目指标
            f.write("# Project Metrics\n")
            project_name = project_data["project_name"]
            current_iteration = project_data["current_iteration"]
            f.write('project_iterations_total{{project_name="{project_name}"}} {count}\n'.format(
                project_name=project_name, count=len(project_data["iterations"])))
            f.write('project_current_iteration{{project_name="{project_name}",iteration="{iteration}"}} 1\n'.format(
                project_name=project_name, iteration=current_iteration))

            # 任务统计
            for iteration in project_data['iterations']:
                iteration_id = iteration['iteration_id']
                for task in iteration['tasks']:
                    task_name = task["task_name"]
                    task_status = task["status"]
                f.write('task_status{{project_name="{project_name}",iteration="{iteration_id}",task="{task_name}",status="{task_status}"}} 1\n'.format(
                    project_name=project_name, iteration_id=iteration_id, task_name=task_name, task_status=task_status))

            # 应用模块指标
            f.write("\n# App Metrics\n")
            app_name = app_data["app_name"]
            for module in app_data['modules']:
                module_name = module["module_name"]
                module_status = module["status"]
                f.write('module_completion_rate{{app_name="{app_name}",module="{module_name}"}} {rate}\n'.format(
                    app_name=app_name, module_name=module_name, rate=module["completion_rate"]))
                f.write('module_status{{app_name="{app_name}",module="{module_name}",status="{module_status}"}} 1\n'.format(
                    app_name=app_name, module_name=module_name, module_status=module_status))

            # 测试指标
            f.write("\n# Test Metrics\n")
            for suite in test_data['test_suites']:
                suite_name = suite["suite_name"]
                f.write('test_total{{suite_name="{suite_name}"}} {total}\n'.format(
                    suite_name=suite_name, total=suite["total_tests"]))
                f.write('test_passed{{suite_name="{suite_name}"}} {passed}\n'.format(
                    suite_name=suite_name, passed=suite["passed_tests"]))
                f.write('test_failed{{suite_name="{suite_name}"}} {failed}\n'.format(
                    suite_name=suite_name, failed=suite["failed_tests"]))
                f.write('test_skipped{{suite_name="{suite_name}"}} {skipped}\n'.format(
                    suite_name=suite_name, skipped=suite["skipped_tests"]))
                f.write('test_coverage{{suite_name="{suite_name}"}} {coverage}\n'.format(
                    suite_name=suite_name, coverage=suite["coverage"]))

        print("[OK] 导出完成")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
