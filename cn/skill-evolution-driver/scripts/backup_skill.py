#!/usr/bin/env python3
"""
技能备份工具
备份整个skill目录为.skill文件
"""

import os
import sys
import shutil
import zipfile
import argparse
from datetime import datetime
import json


def validate_skill(skill_dir):
    """
    验证技能格式

    Args:
        skill_dir: 技能目录路径

    Returns:
        (is_valid, errors): (是否有效, 错误列表)
    """
    errors = []

    # 检查目录存在
    if not os.path.exists(skill_dir):
        errors.append(f"技能目录不存在: {skill_dir}")
        return False, errors

    # 检查SKILL.md存在
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.exists(skill_md_path):
        errors.append(f"SKILL.md不存在: {skill_md_path}")

    # 检查前言区格式
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            errors.append("SKILL.md前言区格式错误：必须以---开头")
        else:
            # 提取前言区
            parts = content.split('---')
            if len(parts) < 3:
                errors.append("SKILL.md前言区格式错误：前言区必须以---结尾")
            else:
                yaml_content = parts[1]
                if not yaml_content.strip():
                    errors.append("SKILL.md前言区为空")
    except Exception as e:
        errors.append(f"读取SKILL.md失败: {str(e)}")

    # 检查目录结构
    required_dirs = ['scripts', 'references', 'assets']
    for dir_name in required_dirs:
        dir_path = os.path.join(skill_dir, dir_name)
        if not os.path.exists(dir_path):
            # 这些目录是可选的，所以只是警告
            pass

    # 检查脚本语法
    scripts_dir = os.path.join(skill_dir, 'scripts')
    if os.path.exists(scripts_dir):
        for filename in os.listdir(scripts_dir):
            if filename.endswith('.py'):
                script_path = os.path.join(scripts_dir, filename)
                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    compile(code, script_path, 'exec')
                except SyntaxError as e:
                    errors.append(f"脚本语法错误 {filename}: {str(e)}")

    return len(errors) == 0, errors


def backup_skill(skill_dir, output_dir=None):
    """
    备份技能目录为.skill文件

    Args:
        skill_dir: 技能目录路径
        output_dir: 输出目录，默认为技能所在目录

    Returns:
        backup_path: 备份文件路径
    """
    # 获取技能名
    skill_name = os.path.basename(os.path.normpath(skill_dir))

    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.dirname(skill_dir)

    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_filename = f"{skill_name}.backup.{timestamp}.skill"
    backup_path = os.path.join(output_dir, backup_filename)

    # 创建ZIP文件
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历skill目录
        for root, dirs, files in os.walk(skill_dir):
            # 跳过缓存和临时目录
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.pytest_cache', 'node_modules', '.DS_Store']]

            for file in files:
                # 跳过缓存和临时文件
                if file.endswith(('.pyc', '.pyo', '.pyd', '.DS_Store')):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_dir)
                zipf.write(file_path, arcname)

    return backup_path


def main():
    parser = argparse.ArgumentParser(description='技能备份工具')
    parser.add_argument('--skill-dir', required=True, help='技能目录路径')
    parser.add_argument('--output-dir', help='输出目录（默认为技能所在目录）')
    parser.add_argument('--validate-only', action='store_true', help='仅验证，不备份')

    args = parser.parse_args()

    # 规范化路径
    skill_dir = os.path.normpath(args.skill_dir)

    # 验证技能
    is_valid, errors = validate_skill(skill_dir)

    if not is_valid:
        print("[FAIL] 技能验证失败")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("[OK] 技能验证通过")

    if args.validate_only:
        return

    # 备份技能
    try:
        backup_path = backup_skill(skill_dir, args.output_dir)
        print(f"[OK] 技能备份成功")
        print(f"  备份文件: {backup_path}")
    except Exception as e:
        print(f"[FAIL] 备份失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
