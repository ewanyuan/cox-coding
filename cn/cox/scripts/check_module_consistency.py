#!/usr/bin/env python3
"""
模块一致性检查脚本
验证 project_data.json 和 app_status.json 中的模块信息是否一致
"""

import json
import sys
from pathlib import Path


def check_module_consistency(project_file='project_data.json', app_file='app_status.json'):
    """检查模块一致性
    
    Args:
        project_file: project_data.json 文件路径
        app_file: app_status.json 文件路径
    
    Returns:
        bool: 如果一致返回 True，否则返回 False
    """
    # 检查文件是否存在
    if not Path(project_file).exists():
        print(f"[ERROR] 文件不存在: {project_file}")
        return False
    
    if not Path(app_file).exists():
        print(f"[ERROR] 文件不存在: {app_file}")
        return False
    
    # 读取文件
    try:
        with open(project_file, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] {project_file} 格式错误: {e}")
        return False
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            app_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] {app_file} 格式错误: {e}")
        return False
    
    # 提取模块信息
    project_modules = {}
    for iteration in project_data.get('iterations', []):
        for module in iteration.get('modules', []):
            module_id = module['module_id']
            module_name = module['module_name']
            if module_id in project_modules:
                if project_modules[module_id] != module_name:
                    print(f"[WARNING] project_data.json 中模块 ID 重复，名称不一致: {module_id}")
            else:
                project_modules[module_id] = module_name
    
    app_modules = {}
    for module in app_data.get('modules', []):
        module_id = module['module_id']
        module_name = module['module_name']
        app_modules[module_id] = module_name
    
    # 检查一致性
    print("\n[INFO] 检查模块一致性...")
    print(f"  - project_data.json 中的模块: {len(project_modules)} 个")
    print(f"  - app_status.json 中的模块: {len(app_modules)} 个")
    
    # 检查项目数据中是否包含 app_status 中不存在的模块
    missing_in_app = set(project_modules.keys()) - set(app_modules.keys())
    if missing_in_app:
        print(f"\n[ERROR] 以下模块在 project_data.json 中存在，但在 app_status.json 中缺失:")
        for module_id in sorted(missing_in_app):
            print(f"  - {module_id}: {project_modules[module_id]}")
    
    # 检查 app_status 中是否包含项目数据中不存在的模块
    missing_in_project = set(app_modules.keys()) - set(project_modules.keys())
    if missing_in_project:
        print(f"\n[WARNING] 以下模块在 app_status.json 中存在，但在 project_data.json 中缺失:")
        for module_id in sorted(missing_in_project):
            print(f"  - {module_id}: {app_modules[module_id]}")
    
    # 检查模块名称是否一致
    common_modules = set(project_modules.keys()) & set(app_modules.keys())
    inconsistent = []
    for module_id in common_modules:
        if project_modules[module_id] != app_modules[module_id]:
            inconsistent.append(module_id)
    
    if inconsistent:
        print(f"\n[ERROR] 以下模块的名称在两个文件中不一致:")
        for module_id in sorted(inconsistent):
            print(f"  - {module_id}:")
            print(f"    project_data.json: {project_modules[module_id]}")
            print(f"    app_status.json: {app_modules[module_id]}")
    
    # 汇总结果
    if missing_in_app or missing_in_project or inconsistent:
        print(f"\n[RESULT] ❌ 模块不一致")
        return False
    else:
        print(f"\n[RESULT] ✅ 模块一致")
        print(f"\n模块列表:")
        for module_id in sorted(project_modules.keys()):
            print(f"  - {module_id}: {project_modules[module_id]}")
        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='检查 project_data.json 和 app_status.json 中的模块一致性',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--project', default='project_data.json',
                       help='project_data.json 文件路径（默认: project_data.json）')
    parser.add_argument('--app', default='app_status.json',
                       help='app_status.json 文件路径（默认: app_status.json）')
    
    args = parser.parse_args()
    
    # 执行检查
    result = check_module_consistency(args.project, args.app)
    
    # 返回退出码
    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
