#!/usr/bin/env python3
"""
优化任务管理脚本

提供优化任务的增删改查功能，用于维护 skill-evolution-driver 的优化任务清单。
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加 shared 到路径，导入 path_utils
shared_dir = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_dir))
from path_utils import get_skill_manager_scripts_str, get_skill_data_path_str

# 添加 skill-manager 脚本路径
sys.path.insert(0, get_skill_manager_scripts_str())
from skill_manager import SkillStorage


def create_task(skill_name, optimization_type, description, status='pending'):
    """
    创建新的优化任务

    Args:
        skill_name: 技能名称
        optimization_type: 优化类型
        description: 任务描述
        status: 任务状态（pending/feasible/not_feasible/in-progress/completed/failed）

    Returns:
        任务字典
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        "task_id": f"OPT-{now.replace(' ', '').replace('-', '').replace(':', '')}",
        "skill_name": skill_name,
        "optimization_type": optimization_type,
        "description": description,
        "status": status,
        "feasibility": "pending",
        "backup_path": "",
        "old_version": "",
        "new_version": "",
        "test_result": "",
        "notes": "",
        "created_at": now,
        "updated_at": now
    }


def add_task(task):
    """
    添加优化任务到 skill-evolution-driver

    Args:
        task: 任务字典

    Returns:
        是否成功
    """
    storage = SkillStorage(data_path=get_skill_data_path_str())

    # 读取现有配置
    config = storage.get_config('skill-evolution-driver') or {}

    # 获取或初始化任务列表
    tasks = config.get('optimization_tasks', [])

    # 检查是否已存在相同任务
    for existing_task in tasks:
        if (existing_task.get('skill_name') == task['skill_name'] and
            existing_task.get('description') == task['description']):
            return False, "任务已存在"

    # 添加任务
    tasks.append(task)
    config['optimization_tasks'] = tasks
    config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 保存
    storage.save_config('skill-evolution-driver', config)

    return True, f"任务 {task['task_id']} 已添加"


def update_task_status(task_id, status, notes=None, **kwargs):
    """
    更新任务状态

    Args:
        task_id: 任务ID
        status: 新状态
        notes: 备注
        **kwargs: 其他要更新的字段

    Returns:
        是否成功
    """
    storage = SkillStorage(data_path=get_skill_data_path_str())

    # 读取现有配置
    config = storage.get_config('skill-evolution-driver')
    if not config or 'optimization_tasks' not in config:
        return False, "任务列表不存在"

    tasks = config['optimization_tasks']

    # 查找任务
    task_found = False
    for task in tasks:
        if task.get('task_id') == task_id:
            task['status'] = status
            task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if notes is not None:
                task['notes'] = notes

            # 更新其他字段
            for key, value in kwargs.items():
                task[key] = value

            task_found = True
            break

    if not task_found:
        return False, f"任务 {task_id} 不存在"

    # 保存
    config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    storage.save_config('skill-evolution-driver', config)

    return True, f"任务 {task_id} 状态已更新为 {status}"


def list_tasks(status=None, skill_name=None):
    """
    列出优化任务

    Args:
        status: 按状态过滤（可选）
        skill_name: 按技能名称过滤（可选）

    Returns:
        任务列表
    """
    storage = SkillStorage(data_path=get_skill_data_path_str())

    # 读取现有配置
    config = storage.get_config('skill-evolution-driver')
    if not config or 'optimization_tasks' not in config:
        return []

    tasks = config['optimization_tasks']

    # 过滤
    filtered = tasks
    if status:
        filtered = [t for t in filtered if t.get('status') == status]
    if skill_name:
        filtered = [t for t in filtered if t.get('skill_name') == skill_name]

    return filtered


def main():
    import argparse

    parser = argparse.ArgumentParser(description='优化任务管理')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 添加任务
    add_parser = subparsers.add_parser('add', help='添加优化任务')
    add_parser.add_argument('--skill-name', required=True, help='技能名称')
    add_parser.add_argument('--type', required=True, help='优化类型')
    add_parser.add_argument('--description', required=True, help='任务描述')
    add_parser.add_argument('--status', default='pending', help='任务状态')

    # 更新任务状态
    update_parser = subparsers.add_parser('update', help='更新任务状态')
    update_parser.add_argument('--task-id', required=True, help='任务ID')
    update_parser.add_argument('--status', required=True, help='新状态')
    update_parser.add_argument('--notes', help='备注')
    update_parser.add_argument('--backup-path', help='备份路径')
    update_parser.add_argument('--old-version', help='旧版本')
    update_parser.add_argument('--new-version', help='新版本')
    update_parser.add_argument('--test-result', help='测试结果')

    # 列出任务
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', help='按状态过滤')
    list_parser.add_argument('--skill-name', help='按技能名称过滤')

    args = parser.parse_args()

    if args.command == 'add':
        task = create_task(
            args.skill_name,
            args.type,
            args.description,
            args.status
        )
        success, message = add_task(task)
        if success:
            print(f"[OK] {message}")
            return 0
        else:
            print(f"[FAIL] {message}")
            return 1

    elif args.command == 'update':
        kwargs = {}
        if args.backup_path:
            kwargs['backup_path'] = args.backup_path
        if args.old_version:
            kwargs['old_version'] = args.old_version
        if args.new_version:
            kwargs['new_version'] = args.new_version
        if args.test_result:
            kwargs['test_result'] = args.test_result

        success, message = update_task_status(
            args.task_id,
            args.status,
            args.notes,
            **kwargs
        )
        if success:
            print(f"[OK] {message}")
            return 0
        else:
            print(f"[FAIL] {message}")
            return 1

    elif args.command == 'list':
        tasks = list_tasks(args.status, args.skill_name)

        if not tasks:
            print("没有找到任务")
            return 0

        print(f"找到 {len(tasks)} 个任务:\n")
        for task in tasks:
            print(f"任务ID: {task.get('task_id')}")
            print(f"  技能: {task.get('skill_name')}")
            print(f"  类型: {task.get('optimization_type')}")
            print(f"  描述: {task.get('description')}")
            print(f"  状态: {task.get('status')}")
            print(f"  创建时间: {task.get('created_at')}")
            print(f"  更新时间: {task.get('updated_at')}")
            if task.get('notes'):
                print(f"  备注: {task.get('notes')}")
            print()

        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
