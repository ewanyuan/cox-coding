#!/usr/bin/env python3
"""
版本号更新工具
更新SKILL.md中的version字段
"""

import os
import sys
import re
import argparse
from datetime import datetime


def get_current_version(skill_md_path):
    """
    获取当前版本号

    Args:
        skill_md_path: SKILL.md文件路径

    Returns:
        version: 当前版本号，如果没有则为None
    """
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 version: v1.0.0 格式
    match = re.search(r'version:\s*(v\d+\.\d+\.\d+)', content)
    if match:
        return match.group(1)

    return None


def increment_version(version, version_type):
    """
    增加版本号

    Args:
        version: 当前版本号，如 v1.0.0
        version_type: 版本类型（patch/minor/major）

    Returns:
        new_version: 新版本号
    """
    # 移除v前缀
    version = version.lstrip('v')
    parts = version.split('.')

    major = int(parts[0])
    minor = int(parts[1])
    patch = int(parts[2])

    if version_type == 'patch':
        patch += 1
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"不支持的版本类型: {version_type}")

    return f"v{major}.{minor}.{patch}"


def update_version(skill_md_path, version_type='patch'):
    """
    更新SKILL.md中的版本号

    Args:
        skill_md_path: SKILL.md文件路径
        version_type: 版本类型（patch/minor/major）

    Returns:
        old_version: 旧版本号
        new_version: 新版本号
    """
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取当前版本号
    old_version = get_current_version(skill_md_path)

    if old_version is None:
        # 如果没有版本号，设置为初始版本
        old_version = None
        new_version = "v1.0.0"
    else:
        # 增加版本号
        new_version = increment_version(old_version, version_type)

    # 更新或添加版本号
    if old_version is None:
        # 在name字段后添加version字段
        content = re.sub(
            r'(name:\s+[^\n]+)',
            rf'\1\nversion: {new_version}',
            content
        )
    else:
        # 更新现有版本号
        content = re.sub(
            rf'version:\s*{re.escape(old_version)}',
            f'version: {new_version}',
            content
        )

    # 写回文件
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return old_version, new_version


def main():
    parser = argparse.ArgumentParser(description='版本号更新工具')
    parser.add_argument('--skill-dir', required=True, help='技能目录路径')
    parser.add_argument('--type', default='patch',
                       choices=['patch', 'minor', 'major'],
                       help='版本类型（patch/minor/major）')
    parser.add_argument('--version', help='直接设置版本号')

    args = parser.parse_args()

    # 规范化路径
    skill_dir = os.path.normpath(args.skill_dir)
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')

    # 检查SKILL.md存在
    if not os.path.exists(skill_md_path):
        print(f"[FAIL] SKILL.md不存在: {skill_md_path}")
        sys.exit(1)

    try:
        if args.version:
            # 直接设置版本号
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            old_version = get_current_version(skill_md_path)

            if old_version is None:
                # 添加版本号
                content = re.sub(
                    r'(name:\s+[^\n]+)',
                    rf'\1\nversion: {args.version}',
                    content
                )
            else:
                # 更新版本号
                content = re.sub(
                    rf'version:\s*{re.escape(old_version)}',
                    f'version: {args.version}',
                    content
                )

            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)

            new_version = args.version
        else:
            # 增加版本号
            old_version, new_version = update_version(skill_md_path, args.type)

        if old_version:
            print(f"[OK] 版本号更新成功")
            print(f"  旧版本: {old_version}")
            print(f"  新版本: {new_version}")
        else:
            print(f"[OK] 版本号添加成功")
            print(f"  版本: {new_version}")
    except Exception as e:
        print(f"[FAIL] 更新失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
