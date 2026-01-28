#!/usr/bin/env python3
"""
检查 skill-manager 中的技能优化机会

此脚本扫描 skill-manager 存储的数据，识别需要优化的技能和待处理的优化任务。
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# 添加 shared 到路径，导入 path_utils
shared_dir = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_dir))
from path_utils import get_skill_manager_scripts_str, get_skill_data_path_str, get_skill_dir

# 添加 skill-manager 脚本路径
sys.path.insert(0, get_skill_manager_scripts_str())
from skill_manager import SkillStorage


def check_missing_fields(storage, skill_name, completed_tasks=None):
    """
    检查技能配置中是否缺少必要字段

    Args:
        storage: SkillStorage 实例
        skill_name: 技能名称
        completed_tasks: 已完成的优化任务列表（用于过滤）

    Returns:
        缺失字段列表
    """
    config = storage.get_config(skill_name)
    if not config:
        return []

    missing = []

    # 检查是否有 version 字段
    if 'version' not in config:
        # 检查是否有已完成的 version 字段优化任务
        version_task_completed = False
        if completed_tasks:
            for task in completed_tasks:
                if (task.get('skill_name') == skill_name and
                    task.get('status') == 'completed' and
                    'version' in task.get('description', '').lower()):
                    version_task_completed = True
                    break

        if not version_task_completed:
            missing.append('version')

    # 检查是否有 deploy_mode 字段（针对 dev-observability）
    if skill_name == 'dev-observability' and 'deploy_mode' not in config:
        # 检查是否有已完成的 deploy_mode 字段优化任务
        deploy_mode_task_completed = False
        if completed_tasks:
            for task in completed_tasks:
                if (task.get('skill_name') == skill_name and
                    task.get('status') == 'completed' and
                    'deploy_mode' in task.get('description', '').lower()):
                    deploy_mode_task_completed = True
                    break

        if not deploy_mode_task_completed:
            missing.append('deploy_mode')

    # 检查是否有 manual_path 字段
    if 'manual_path' not in config:
        # 检查是否有已完成的 manual_path 字段优化任务
        manual_path_task_completed = False
        if completed_tasks:
            for task in completed_tasks:
                if (task.get('skill_name') == skill_name and
                    task.get('status') == 'completed' and
                    'manual_path' in task.get('description', '').lower()):
                    manual_path_task_completed = True
                    break

        if not manual_path_task_completed:
            missing.append('manual_path')

    return missing


def check_pending_optimization_tasks(storage):
    """
    检查是否有待处理的优化任务

    Args:
        storage: SkillStorage 实例

    Returns:
        待处理任务列表
    """
    config = storage.get_config('skill-evolution-driver')
    if not config:
        return []

    # 检查是否有优化任务配置
    if 'optimization_tasks' not in config:
        return []

    tasks = config['optimization_tasks']
    pending_tasks = [task for task in tasks if task.get('status') == 'pending']

    return pending_tasks


def check_error_logs(storage, skill_name, completed_tasks=None):
    """
    检查技能日志中是否有错误或警告

    Args:
        storage: SkillStorage 实例
        skill_name: 技能名称
        completed_tasks: 已完成的优化任务列表（用于过滤）

    Returns:
        错误日志列表
    """
    logs = storage.get_logs(skill_name)
    if not logs:
        return []

    error_logs = [
        log for log in logs
        if log.get('level') in ['ERROR', 'WARNING', 'CRITICAL']
    ]

    # 如果有已完成的错误日志优化任务，过滤相关错误
    if completed_tasks and error_logs:
        filtered_logs = []
        for log in error_logs:
            is_filtered = False
            for task in completed_tasks:
                if (task.get('skill_name') == skill_name and
                    task.get('status') == 'completed' and
                    'error' in task.get('description', '').lower()):
                    # 检查错误日志的时间是否在任务完成之后
                    task_updated = task.get('updated_at', '')
                    if task_updated and log.get('time', '') <= task_updated:
                        is_filtered = True
                        break

            if not is_filtered:
                filtered_logs.append(log)

        return filtered_logs

    return error_logs


def check_skill_directory_issues(skill_name, completed_tasks=None):
    """
    检查技能目录是否存在问题

    Args:
        skill_name: 技能名称
        completed_tasks: 已完成的优化任务列表（用于过滤）

    Returns:
        问题列表
    """
    issues = []
    skill_dir = get_skill_dir(skill_name)

    if not skill_dir.exists():
        issues.append(f'技能目录不存在: {skill_dir}')
        return issues

    # 检查 SKILL.md 是否存在
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        # 检查是否有已完成的 SKILL.md 缺失优化任务
        skill_md_task_completed = False
        if completed_tasks:
            for task in completed_tasks:
                if (task.get('skill_name') == skill_name and
                    task.get('status') == 'completed' and
                    'skill.md' in task.get('description', '').lower()):
                    skill_md_task_completed = True
                    break

        if not skill_md_task_completed:
            issues.append('缺少 SKILL.md 文件')
        return issues

    # 检查 SKILL.md 格式
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查 YAML 前言区
        if not content.startswith('---'):
            # 检查是否有已完成的 YAML 前言区优化任务
            yaml_task_completed = False
            if completed_tasks:
                for task in completed_tasks:
                    if (task.get('skill_name') == skill_name and
                        task.get('status') == 'completed' and
                        'yaml' in task.get('description', '').lower()):
                        yaml_task_completed = True
                        break

            if not yaml_task_completed:
                issues.append('SKILL.md 缺少 YAML 前言区')
        else:
            # 检查 name 和 description 字段
            yaml_end = content.find('---', 3)
            yaml_content = content[3:yaml_end]

            missing_fields = []
            if 'name:' not in yaml_content:
                # 检查是否有已完成的 name 字段优化任务
                name_task_completed = False
                if completed_tasks:
                    for task in completed_tasks:
                        if (task.get('skill_name') == skill_name and
                            task.get('status') == 'completed' and
                            'name' in task.get('description', '').lower()):
                            name_task_completed = True
                            break
                if not name_task_completed:
                    missing_fields.append('name')

            if 'description:' not in yaml_content:
                # 检查是否有已完成的 description 字段优化任务
                desc_task_completed = False
                if completed_tasks:
                    for task in completed_tasks:
                        if (task.get('skill_name') == skill_name and
                            task.get('status') == 'completed' and
                            'description' in task.get('description', '').lower()):
                            desc_task_completed = True
                            break
                if not desc_task_completed:
                    missing_fields.append('description')

            if missing_fields:
                issues.append(f'YAML 前言区缺少字段: {", ".join(missing_fields)}')

    except Exception as e:
        issues.append(f'无法读取 SKILL.md: {str(e)}')

    # 检查必需目录
    for required_dir in ['scripts', 'references', 'assets']:
        if not (skill_dir / required_dir).exists():
            # 检查是否有已完成的目录优化任务
            dir_task_completed = False
            if completed_tasks:
                for task in completed_tasks:
                    if (task.get('skill_name') == skill_name and
                        task.get('status') == 'completed' and
                        required_dir in task.get('description', '').lower()):
                        dir_task_completed = True
                        break

            if not dir_task_completed:
                issues.append(f'缺少 {required_dir} 目录')

    return issues


def main():
    import argparse

    parser = argparse.ArgumentParser(description='检查技能优化机会')
    parser.add_argument('--skill-name', help='指定检查的技能名称，不指定则检查所有技能')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='输出格式')
    args = parser.parse_args()

    # 初始化存储
    storage = SkillStorage(data_path=get_skill_data_path_str())

    # 获取所有技能或指定技能
    if args.skill_name:
        skills_to_check = [args.skill_name]
    else:
        skills_to_check = storage.list_skills()

    results = []

    # 获取已完成的优化任务（用于过滤重复问题）
    config = storage.get_config('skill-evolution-driver')
    completed_tasks = []
    if config and 'optimization_tasks' in config:
        completed_tasks = [
            task for task in config['optimization_tasks']
            if task.get('status') == 'completed'
        ]

    # 检查待处理的优化任务
    pending_tasks = check_pending_optimization_tasks(storage)
    if pending_tasks:
        results.append({
            'type': 'pending_task',
            'skill': 'skill-evolution-driver',
            'description': f'有 {len(pending_tasks)} 个待处理的优化任务',
            'details': pending_tasks
        })

    # 检查每个技能
    for skill_name in skills_to_check:
        skill_issues = []

        # 跳过 skill-evolution-driver 本身
        if skill_name == 'skill-evolution-driver':
            continue

        # 1. 检查缺失字段（过滤已完成的任务）
        missing_fields = check_missing_fields(storage, skill_name, completed_tasks)
        if missing_fields:
            skill_issues.append({
                'type': 'missing_fields',
                'description': f'缺少必要字段: {", ".join(missing_fields)}'
            })

        # 2. 检查错误日志（过滤已完成的任务）
        error_logs = check_error_logs(storage, skill_name, completed_tasks)
        if error_logs:
            skill_issues.append({
                'type': 'error_logs',
                'description': f'有 {len(error_logs)} 条错误日志',
                'count': len(error_logs)
            })

        # 3. 检查技能目录问题（过滤已完成的任务）
        dir_issues = check_skill_directory_issues(skill_name, completed_tasks)
        if dir_issues:
            skill_issues.append({
                'type': 'directory_issues',
                'description': '技能目录存在问题',
                'issues': dir_issues
            })

        if skill_issues:
            results.append({
                'skill': skill_name,
                'issues': skill_issues
            })

    # 输出结果
    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("[OK] 未发现需要优化的技能")
            return 0

        print("检测到以下优化机会：\n")

        for result in results:
            if result.get('type') == 'pending_task':
                print(f"【待处理任务】")
                print(f"  技能: {result['skill']}")
                print(f"  描述: {result['description']}")
                print()

            else:
                skill_name = result['skill']
                print(f"【{skill_name}】")

                for issue in result['issues']:
                    print(f"  - {issue['description']}")
                    if issue.get('type') == 'directory_issues' and 'issues' in issue:
                        for detail in issue['issues']:
                            print(f"    • {detail}")

                print()

        print("建议：调用 skill-evolution-driver 进行优化")

    return 0 if not results else 1


if __name__ == "__main__":
    sys.exit(main())
