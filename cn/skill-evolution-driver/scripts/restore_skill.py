#!/usr/bin/env python3
"""
技能还原工具
从备份文件还原技能目录
"""

import os
import sys
import shutil
import zipfile
import argparse
import tempfile


def restore_skill(backup_file, skill_dir):
    """
    从备份文件还原技能目录

    Args:
        backup_file: 备份文件路径（.skill文件）
        skill_dir: 技能目录路径
    """
    # 检查备份文件存在
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"备份文件不存在: {backup_file}")

    # 如果技能目录存在，先删除
    if os.path.exists(skill_dir):
        shutil.rmtree(skill_dir)

    # 解压备份文件到临时目录
    temp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(temp_dir)

        # 将解压的内容移动到目标目录
        # ZIP文件中应该包含skill目录的内容
        extracted_items = os.listdir(temp_dir)
        if len(extracted_items) == 1:
            # 如果ZIP只包含一个目录，直接移动它
            shutil.move(os.path.join(temp_dir, extracted_items[0]), skill_dir)
        else:
            # 如果ZIP包含多个文件/目录，将temp_dir重命名为skill_dir
            shutil.move(temp_dir, skill_dir)
            temp_dir = None
    finally:
        # 清理临时目录（如果没有被移动）
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def main():
    parser = argparse.ArgumentParser(description='技能还原工具')
    parser.add_argument('--backup-file', required=True, help='备份文件路径')
    parser.add_argument('--skill-dir', required=True, help='技能目录路径')

    args = parser.parse_args()

    # 规范化路径
    backup_file = os.path.normpath(args.backup_file)
    skill_dir = os.path.normpath(args.skill_dir)

    # 还原技能
    try:
        restore_skill(backup_file, skill_dir)
        print(f"[OK] 技能还原成功")
        print(f"  备份文件: {backup_file}")
        print(f"  技能目录: {skill_dir}")
    except Exception as e:
        print(f"[FAIL] 还原失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
