#!/usr/bin/env python3
"""
可观测数据生成器
生成符合规范的可观测数据文件，避免大模型幻觉导致的格式错误

核心原则：示例数据仅提供最小骨架，不填充任何虚假的业务数据。
所有业务相关数据（任务、埋点、异常）应由智能体根据实际情况填写。

安全机制：如果目标文件已存在且非空，默认会报错并提示使用 --overwrite 参数，
防止意外覆盖已编辑的数据文件。

使用方法:
  生成最小数据集:
    python generate_observability_data.py --mode minimal --project-name "我的项目"

  强制覆盖已存在的文件:
    python generate_observability_data.py --mode minimal --project-name "我的项目" --overwrite
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta


def check_file_exists(file_path, overwrite=False):
    """检查文件是否存在并警告
    
    Args:
        file_path: 文件路径
        overwrite: 是否强制覆盖
        
    Returns:
        bool: 是否应该继续写入文件
    """
    if file_path.exists():
        file_size = file_path.stat().st_size
        if file_size > 10:  # 文件非空（大于10字节）
            if not overwrite:
                print(f"[ERROR] 文件已存在且非空: {file_path}")
                print(f"[INFO] 文件大小: {file_size} 字节")
                print(f"[INFO] 如果要覆盖，请使用 --overwrite 参数")
                print(f"[INFO] 例如: python generate_observability_data.py --overwrite")
                return False
            else:
                print(f"[WARNING] 文件已存在，将被覆盖: {file_path}")
        else:
            print(f"[INFO] 文件已存在但为空: {file_path}")
    return True


def generate_project_data(project_name, mode='minimal', iterations=1, custom_modules=None):
    """生成项目维度数据
    
    Args:
        project_name: 项目名称
        mode: 数据模式（minimal/complete）
        iterations: 迭代数量
        custom_modules: 自定义模块列表，格式为 [{"id": "MOD-001", "name": "模块名称"}, ...]
    """
    project_data = {
        "project_name": project_name,
        "current_iteration": "ITER-001"
    }

    if mode == 'minimal':
        # 最小数据集：1个迭代，无任务（由用户手动添加）
        project_data["iterations"] = [
            {
                "iteration_id": "ITER-001",
                "iteration_name": "第一次迭代",
                "status": "in_progress",
                "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "tasks": [],
                "modules": [
                    {
                        "module_id": "MOD-001",
                        "module_name": custom_modules[0]["name"] if custom_modules else "示例模块",
                        "expected_completion": 0.0
                    }
                ],
                "assumptions": []
            }
        ]
    else:
        # 完整示例：多个迭代，无任务（由用户手动添加）
        project_data["iterations"] = []
        for i in range(1, iterations + 1):
            iteration_id = f"ITER-{i:03d}"
            start_date = datetime.now() - timedelta(days=30 * (iterations - i))
            end_date = start_date + timedelta(days=30)

            # 根据迭代编号设置不同状态
            if i < iterations:
                status = "completed"
            elif i == iterations:
                status = "in_progress"
            else:
                status = "not_started"

            tasks = []  # 不生成示例任务，由用户手动添加

            # 为每个迭代分配模块
            # 优先使用自定义模块，否则使用默认模块列表
            if custom_modules:
                all_modules = custom_modules
            else:
                all_modules = [
                    {"id": "MOD-001", "name": "示例模块1"},
                    {"id": "MOD-002", "name": "示例模块2"},
                    {"id": "MOD-003", "name": "示例模块3"},
                    {"id": "MOD-004", "name": "示例模块4"},
                    {"id": "MOD-005", "name": "示例模块5"},
                    {"id": "MOD-006", "name": "示例模块6"}
                ]
            
            # 每个迭代涉及 1-2 个模块
            iter_modules = all_modules[(i-1)*2 % len(all_modules):(i-1)*2 % len(all_modules) + min(2, len(all_modules) - ((i-1)*2 % len(all_modules)))]
            modules = []
            for m in iter_modules:
                modules.append({
                    "module_id": m["id"],
                    "module_name": m["name"],
                    "expected_completion": 0.0
                })

            project_data["iterations"].append({
                "iteration_id": iteration_id,
                "iteration_name": f"第{i}次迭代",
                "status": status,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "tasks": tasks,
                "modules": modules,
                "assumptions": []
            })

    return project_data


def generate_app_data(app_name, mode='minimal', custom_modules=None):
    """生成应用维度数据
    
    Args:
        app_name: 应用名称
        mode: 数据模式（minimal/complete）
        custom_modules: 自定义模块列表，格式为 [{"id": "MOD-001", "name": "模块名称"}, ...]
    """
    app_data = {
        "app_name": app_name,
        "version": "1.0.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if mode == 'minimal':
        # 最小数据集：1个模块
        app_data["modules"] = [
            {
                "module_id": "MOD-001",
                "module_name": custom_modules[0]["name"] if custom_modules else "示例模块",
                "status": "in_progress",
                "owner": "待分配",
                "completion_rate": 0.0,
                "last_update": datetime.now().strftime("%Y-%m-%d"),
                "notes": "模块开发中"
            }
        ]
    else:
        # 完整示例：多个模块
        if custom_modules:
            module_names = [m["name"] for m in custom_modules]
        else:
            module_names = [
                "示例模块1",
                "示例模块2",
                "示例模块3",
                "示例模块4",
                "示例模块5",
                "示例模块6"
            ]
        app_data["modules"] = []
        for i, name in enumerate(module_names):
            app_data["modules"].append({
                "module_id": f"MOD-{i+1:03d}",
                "module_name": name,
                "status": "pending",
                "owner": "待分配",
                "completion_rate": 0.0,
                "last_update": datetime.now().strftime("%Y-%m-%d"),
                "notes": "待开发"
            })

    return app_data


def generate_test_data(mode='minimal', custom_modules=None):
    """生成测试维度数据
    
    Args:
        mode: 数据模式（minimal/complete）
        custom_modules: 自定义模块列表（未使用，保留以兼容接口）
    """
    test_data = {}

    if mode == 'minimal':
        # 最小数据集：1个测试套件框架（数据为0）
        test_data["test_suites"] = [
            {
                "suite_name": "单元测试",
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "coverage": 0.0,
                "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        test_data["tracing_points"] = []
        test_data["anomalies"] = []
    else:
        # 完整示例：多个测试套件框架（数据为0），由真实数据填充
        test_data["test_suites"] = [
            {
                "suite_name": "单元测试",
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "coverage": 0.0,
                "last_run": datetime.now().strftime("%Y-%m-%d 10:30:00")
            },
            {
                "suite_name": "集成测试",
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "coverage": 0.0,
                "last_run": datetime.now().strftime("%Y-%m-%d 09:15:00")
            },
            {
                "suite_name": "性能测试",
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "coverage": 0.0,
                "last_run": datetime.now().strftime("%Y-%m-%d 08:00:00")
            }
        ]
        # 埋点数据留空，由智能体根据实际监控数据填写
        test_data["tracing_points"] = []
        # 异常数据留空，由智能体根据实际监控数据填写
        test_data["anomalies"] = []

    return test_data


def main():
    parser = argparse.ArgumentParser(
        description='生成可观测数据文件',
        epilog='示例:\n'
               '  生成最小数据集: python generate_observability_data.py --mode minimal --project-name "我的项目"\n'
               '  生成完整示例: python generate_observability_data.py --mode complete --project-name "示例项目" --iterations 3',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--mode', choices=['minimal', 'complete'], default='minimal',
                       help='数据模式: minimal=最小数据集（快速开始）, complete=完整示例（包含所有字段）')
    parser.add_argument('--project-name', default='示例项目',
                       help='项目名称（默认: 示例项目）')
    parser.add_argument('--app-name', default='示例应用',
                       help='应用名称（默认: 示例应用）')
    parser.add_argument('--iterations', type=int, default=3,
                       help='迭代数量（仅 complete 模式，默认: 3）')
    parser.add_argument('--output-dir', default='.',
                       help='输出目录（默认: 当前目录）')
    parser.add_argument('--modules', default=None,
                       help='自定义模块列表（JSON格式: [{"id":"MOD-001","name":"模块1"},{"id":"MOD-002","name":"模块2"}]）')
    parser.add_argument('--overwrite', action='store_true',
                       help='强制覆盖已存在的文件（默认会报错）')

    args = parser.parse_args()

    # 解析自定义模块列表
    custom_modules = None
    if args.modules:
        try:
            custom_modules = json.loads(args.modules)
            print(f"[INFO] 使用自定义模块: {[m['name'] for m in custom_modules]}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] 模块列表JSON格式错误: {e}")
            exit(1)

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成数据
    print(f"\n[INFO] 生成模式: {args.mode}")
    print(f"[INFO] 项目名称: {args.project_name}")
    print(f"[INFO] 应用名称: {args.app_name}")

    project_data = generate_project_data(args.project_name, args.mode, args.iterations, custom_modules)
    app_data = generate_app_data(args.app_name, args.mode, custom_modules)
    test_data = generate_test_data(args.mode, custom_modules)

    # 写入文件
    project_file = output_dir / "project_data.json"
    app_file = output_dir / "app_status.json"
    test_file = output_dir / "test_metrics.json"

    # 检查文件是否存在
    for file_path in [project_file, app_file, test_file]:
        if not check_file_exists(file_path, args.overwrite):
            print(f"[ERROR] 检测到文件冲突，请检查后重试")
            exit(1)

    # 写入文件并验证格式
    files_to_write = [
        (project_file, project_data),
        (app_file, app_data),
        (test_file, test_data)
    ]

    for file_path, data in files_to_write:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 验证写入的文件格式是否正确
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"[OK] {file_path.name} 格式验证通过")
        except json.JSONDecodeError as e:
            print(f"[ERROR] {file_path.name} 格式错误: {e}")
            exit(1)

    print(f"\n[OK] 数据文件生成成功:")
    print(f"  - {project_file.absolute()}")
    print(f"  - {app_file.absolute()}")
    print(f"  - {test_file.absolute()}")

    print(f"\n[INFO] 下一步:")
    print(f"  1. 根据实际需求手动编辑数据文件，特别是任务列表")
    print(f"  2. 运行可观测界面:")
    print(f"     静态模式: python scripts/run_web_observability.py --mode static --project {project_file.name} --app {app_file.name} --test {test_file.name}")
    print(f"     Web 模式: python scripts/run_web_observability.py --mode web --project {project_file.name} --app {app_file.name} --test {test_file.name}")


if __name__ == '__main__':
    main()
