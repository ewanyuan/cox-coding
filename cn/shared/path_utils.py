#!/usr/bin/env python3
"""
路径工具模块

提供跨平台路径解析和常用路径操作
"""

import os
from pathlib import Path


def get_skill_root():
    """
    获取技能根目录

    动态检测脚本所在位置，返回技能根目录

    Returns:
        Path: 技能根目录路径对象
    """
    # 获取当前脚本所在目录的父目录（即技能根目录）
    # 例如：/workspace/projects/dev-observability/scripts/foo.py
    # 返回：/workspace/projects/dev-observability

    # 从调用栈获取脚本路径
    import inspect
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_globals.get('__file__')

    if caller_file:
        # 脚本所在目录的父目录即为技能根目录
        script_dir = Path(caller_file).resolve()
        skill_root = script_dir.parent
    else:
        # 如果无法获取调用者路径，使用当前工作目录
        skill_root = Path.cwd()

    return skill_root


def get_projects_root():
    """
    获取 projects 根目录（所有技能的父目录）

    Returns:
        Path: projects 根目录路径对象
    """
    skill_root = get_skill_root()
    projects_root = skill_root.parent
    return projects_root


def get_skill_manager_scripts():
    """
    获取 skill-manager 的 scripts 目录

    Returns:
        Path: skill-manager/scripts 目录路径对象
    """
    projects_root = get_projects_root()
    skill_manager_scripts = projects_root / "skill-manager" / "scripts"
    return skill_manager_scripts


def get_skill_data_path():
    """
    获取 skill-data.json 的路径

    Returns:
        Path: skill-data.json 路径对象
    """
    projects_root = get_projects_root()
    skill_data = projects_root / "skill-data.json"
    return skill_data


def get_skill_dir(skill_name):
    """
    获取指定技能的目录路径

    Args:
        skill_name: 技能名称

    Returns:
        Path: 技能目录路径对象
    """
    projects_root = get_projects_root()
    skill_dir = projects_root / skill_name
    return skill_dir


def get_skill_file(skill_name, file_path):
    """
    获取技能内文件的完整路径

    Args:
        skill_name: 技能名称
        file_path: 相对于技能根目录的文件路径（如 SKILL.md, scripts/foo.py）

    Returns:
        Path: 文件完整路径对象
    """
    skill_dir = get_skill_dir(skill_name)
    full_path = skill_dir / file_path
    return full_path


# 便捷的 str 表示（用于需要字符串的地方）
def get_skill_root_str():
    """返回技能根目录的字符串表示"""
    return str(get_skill_root())


def get_projects_root_str():
    """返回 projects 根目录的字符串表示"""
    return str(get_projects_root())


def get_skill_manager_scripts_str():
    """返回 skill-manager/scripts 的字符串表示"""
    return str(get_skill_manager_scripts())


def get_skill_data_path_str():
    """返回 skill-data.json 的字符串表示"""
    return str(get_skill_data_path())
