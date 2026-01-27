#!/usr/bin/env python3
"""
cox 技能调用 skill-manager 存储信息的辅助脚本

此脚本封装了对 skill-manager 的调用，简化了部署信息和问题追踪信息的存储。
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


def store_deployment_info(deploy_mode, config_details):
    """
    存储部署信息到 skill-manager

    Args:
        deploy_mode: 部署模式 (simple/web/prometheus)
        config_details: 配置字典，包含访问方式、路径等信息

    Returns:
        是否存储成功
    """
    try:
        storage = SkillStorage(data_path=get_skill_data_path_str())

        # 读取现有配置
        existing_config = storage.get_config("cox") or {}
        existing_logs = storage.get_logs("cox") or []

        # 更新配置
        existing_config["deploy_mode"] = deploy_mode
        existing_config.update(config_details)
        existing_config["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 追加日志
        log_message = f"{deploy_mode}方案部署完成"
        if deploy_mode == "simple":
            log_message += f"，日志文件: {config_details.get('output_path', 'unknown')}"
        elif deploy_mode == "web":
            log_message += f"，访问地址: {config_details.get('url', 'unknown')}"
        elif deploy_mode == "prometheus":
            log_message += f"，Prometheus: {config_details.get('prometheus_url', 'unknown')}, Grafana: {config_details.get('grafana_url', 'unknown')}"

        existing_logs.append({
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO",
            "message": log_message
        })

        # 保存
        storage.save("cox", config=existing_config, logs=existing_logs)

        return True, "部署信息已存储"

    except Exception as e:
        return False, f"存储失败: {str(e)}"


def store_issue_info(issue_id, description, affected_modules, complexity, occurrence_count):
    """
    存储问题追踪信息到 skill-manager

    Args:
        issue_id: 问题ID (如 ISSUE-001)
        description: 问题描述
        affected_modules: 受影响的模块列表
        complexity: 复杂度 (high/medium/low)
        occurrence_count: 出现次数

    Returns:
        是否存储成功
    """
    try:
        storage = SkillStorage(data_path=get_skill_data_path_str())

        # 读取现有配置
        existing_config = storage.get_config("cox") or {}
        existing_logs = storage.get_logs("cox") or []

        # 更新配置
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        existing_config["issue_id"] = issue_id
        existing_config["issue_description"] = description
        existing_config["affected_modules"] = affected_modules
        existing_config["complexity"] = complexity
        existing_config["occurrence_count"] = occurrence_count
        existing_config["last_updated"] = now

        # 追加日志
        existing_logs.append({
            "time": now,
            "level": "WARNING",
            "message": "检测到复杂/重复问题，已更新观测数据",
            "issue_id": issue_id
        })

        # 保存
        storage.save("cox", config=existing_config, logs=existing_logs)

        return True, f"问题 {issue_id} 信息已存储"

    except Exception as e:
        return False, f"存储失败: {str(e)}"


def main():
    import argparse

    parser = argparse.ArgumentParser(description='cox 存储信息到 skill-manager')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 存储部署信息
    deploy_parser = subparsers.add_parser('deploy', help='存储部署信息')
    deploy_parser.add_argument('--mode', required=True, choices=['simple', 'web', 'prometheus'],
                              help='部署模式')
    deploy_parser.add_argument('--config', required=True,
                              help='配置JSON字符串')

    # 存储问题信息
    issue_parser = subparsers.add_parser('issue', help='存储问题追踪信息')
    issue_parser.add_argument('--issue-id', required=True, help='问题ID')
    issue_parser.add_argument('--description', required=True, help='问题描述')
    issue_parser.add_argument('--modules', required=True, help='受影响模块，逗号分隔')
    issue_parser.add_argument('--complexity', required=True, choices=['high', 'medium', 'low'],
                              help='复杂度')
    issue_parser.add_argument('--count', type=int, required=True, help='出现次数')

    args = parser.parse_args()

    if args.command == 'deploy':
        config = json.loads(args.config)
        success, message = store_deployment_info(args.mode, config)
        if success:
            print(f"[OK] {message}")
            return 0
        else:
            print(f"[FAIL] {message}")
            return 1

    elif args.command == 'issue':
        modules = [m.strip() for m in args.modules.split(',')]
        success, message = store_issue_info(
            args.issue_id, args.description, modules,
            args.complexity, args.count
        )
        if success:
            print(f"[OK] {message}")
            return 0
        else:
            print(f"[FAIL] {message}")
            return 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
