#!/usr/bin/env python3
"""
技能管理者 - 技能配置和日志存储服务

为其他技能提供统一的配置和日志存储能力，支持技能间数据共享和协作。
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class SkillStorage:
    """
    技能存储类

    提供技能配置和日志的存储、读取、管理功能。
    """

    def __init__(self, data_path: str = None):
        """
        初始化技能存储

        Args:
            data_path: 数据文件路径，默认为 /workspace/projects/skill-data.json
        """
        if data_path is None:
            data_path = "/workspace/projects/skill-data.json"

        self.data_path = data_path
        self._ensure_data_file()

    def _ensure_data_file(self):
        """确保数据文件存在"""
        data_dir = os.path.dirname(self.data_path)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)

        if not os.path.exists(self.data_path):
            self._save_data({})

    def _load_data(self) -> Dict[str, Any]:
        """加载所有数据"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self, data: Dict[str, Any]):
        """保存所有数据"""
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_config(self, skill_name: str, config: Dict[str, Any]):
        """
        存储技能配置

        Args:
            skill_name: 技能名称
            config: 配置数据（字典格式）
        """
        data = self._load_data()

        if skill_name not in data:
            data[skill_name] = {
                "config": {},
                "logs": [],
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        data[skill_name]["config"] = config
        data[skill_name]["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._save_data(data)

    def save_logs(self, skill_name: str, logs: List[Dict[str, Any]], append: bool = True):
        """
        存储技能日志

        Args:
            skill_name: 技能名称
            logs: 日志数据（列表格式）
            append: 是否追加到现有日志，True为追加，False为覆盖
        """
        data = self._load_data()

        if skill_name not in data:
            data[skill_name] = {
                "config": {},
                "logs": [],
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        if append:
            data[skill_name]["logs"].extend(logs)
        else:
            data[skill_name]["logs"] = logs

        data[skill_name]["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._save_data(data)

    def save(self, skill_name: str, config: Dict[str, Any] = None,
             logs: List[Dict[str, Any]] = None, append_logs: bool = True):
        """
        同时存储技能配置和日志

        Args:
            skill_name: 技能名称
            config: 配置数据（可选）
            logs: 日志数据（可选）
            append_logs: 日志是否追加到现有日志
        """
        data = self._load_data()

        if skill_name not in data:
            data[skill_name] = {
                "config": {},
                "logs": [],
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        if config is not None:
            data[skill_name]["config"] = config

        if logs is not None:
            if append_logs:
                data[skill_name]["logs"].extend(logs)
            else:
                data[skill_name]["logs"] = logs

        data[skill_name]["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._save_data(data)

    def get_config(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        读取技能配置

        Args:
            skill_name: 技能名称

        Returns:
            配置数据字典，如果技能不存在则返回None
        """
        data = self._load_data()

        if skill_name not in data:
            return None

        return data[skill_name].get("config")

    def get_logs(self, skill_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        读取技能日志

        Args:
            skill_name: 技能名称

        Returns:
            日志数据列表，如果技能不存在则返回None
        """
        data = self._load_data()

        if skill_name not in data:
            return None

        return data[skill_name].get("logs")

    def get(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        读取技能的所有数据（配置和日志）

        Args:
            skill_name: 技能名称

        Returns:
            包含config和logs的字典，如果技能不存在则返回None
        """
        data = self._load_data()

        if skill_name not in data:
            return None

        return {
            "config": data[skill_name].get("config"),
            "logs": data[skill_name].get("logs"),
            "last_updated": data[skill_name].get("last_updated")
        }

    def get_all(self) -> Dict[str, Any]:
        """
        读取所有技能数据

        Returns:
            所有技能数据的字典
        """
        return self._load_data()

    def list_skills(self) -> List[str]:
        """
        列出所有已存储的技能名称

        Returns:
            技能名称列表
        """
        data = self._load_data()
        return list(data.keys())

    def delete(self, skill_name: str) -> bool:
        """
        删除技能数据

        Args:
            skill_name: 技能名称

        Returns:
            是否删除成功
        """
        data = self._load_data()

        if skill_name not in data:
            return False

        del data[skill_name]
        self._save_data(data)
        return True

    def clear(self):
        """清空所有数据"""
        self._save_data({})

    def get_stats(self) -> Dict[str, Any]:
        """
        获取存储统计信息

        Returns:
            包含统计信息的字典
        """
        data = self._load_data()

        stats = {
            "total_skills": len(data),
            "skills": {}
        }

        for skill_name, skill_data in data.items():
            stats["skills"][skill_name] = {
                "config_size": len(str(skill_data.get("config", {}))),
                "logs_count": len(skill_data.get("logs", [])),
                "last_updated": skill_data.get("last_updated")
            }

        return stats


def main():
    """命令行接口（用于测试）"""
    import argparse

    parser = argparse.ArgumentParser(description='技能管理者 - 技能配置和日志存储服务')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 列出所有技能
    list_parser = subparsers.add_parser('list', help='列出所有已存储的技能')

    # 读取技能数据
    get_parser = subparsers.add_parser('get', help='读取技能数据')
    get_parser.add_argument('skill_name', help='技能名称')

    # 删除技能
    delete_parser = subparsers.add_parser('delete', help='删除技能数据')
    delete_parser.add_argument('skill_name', help='技能名称')

    # 统计信息
    stats_parser = subparsers.add_parser('stats', help='显示统计信息')

    args = parser.parse_args()

    storage = SkillStorage()

    if args.command == 'list':
        skills = storage.list_skills()
        print(f"已存储的技能 ({len(skills)}):")
        for skill in skills:
            print(f"  - {skill}")

    elif args.command == 'get':
        skill_data = storage.get(args.skill_name)
        if skill_data:
            print(f"技能: {args.skill_name}")
            print(f"配置: {json.dumps(skill_data['config'], ensure_ascii=False, indent=2)}")
            print(f"日志条数: {len(skill_data['logs'])}")
            print(f"最后更新: {skill_data['last_updated']}")
        else:
            print(f"错误: 技能 '{args.skill_name}' 不存在")

    elif args.command == 'delete':
        if storage.delete(args.skill_name):
            print(f"已删除技能: {args.skill_name}")
        else:
            print(f"错误: 技能 '{args.skill_name}' 不存在")

    elif args.command == 'stats':
        stats = storage.get_stats()
        print(f"存储统计:")
        print(f"  技能总数: {stats['total_skills']}")
        print(f"\n技能详情:")
        for skill_name, skill_stats in stats['skills'].items():
            print(f"  {skill_name}:")
            print(f"    配置大小: {skill_stats['config_size']} 字符")
            print(f"    日志条数: {skill_stats['logs_count']}")
            print(f"    最后更新: {skill_stats['last_updated']}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
