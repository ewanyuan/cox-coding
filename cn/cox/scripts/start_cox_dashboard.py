#!/usr/bin/env python3
"""
COX Dashboard 一键启动脚本
提供最简单的方式启动COX可观测面板

使用方法:
  python start_cox_dashboard.py           # 自动检测并启动
  python start_cox_dashboard.py --web     # 启动Web交互模式
  python start_cox_dashboard.py --static  # 生成静态HTML
  python start_cox_dashboard.py --init    # 初始化示例数据
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 尝试导入 Flask
try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    from run_web_observability import ObservabilityData, generate_static_html
    from generate_observability_data import generate_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from run_web_observability import ObservabilityData, generate_static_html
    from generate_observability_data import generate_data


# 默认数据文件名
DEFAULT_FILES = {
    'project': 'project_data.json',
    'app': 'app_status.json',
    'test': 'test_data.json'
}


def check_files_exist():
    """检查数据文件是否存在"""
    missing = []
    for key, filename in DEFAULT_FILES.items():
        if not os.path.exists(filename):
            missing.append(filename)
    return missing


def generate_sample_data(project_name="我的项目", app_name="我的应用"):
    """生成示例数据文件"""
    print("\n[INFO] 正在生成示例数据...")
    
    try:
        # 使用 generate_observability_data 生成数据
        data = generate_data(
            mode='minimal',
            project_name=project_name,
            app_name=app_name
        )
        
        # 保存项目数据
        with open(DEFAULT_FILES['project'], 'w', encoding='utf-8') as f:
            json.dump(data['project'], f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已生成: {DEFAULT_FILES['project']}")
        
        # 保存应用状态
        with open(DEFAULT_FILES['app'], 'w', encoding='utf-8') as f:
            json.dump(data['app'], f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已生成: {DEFAULT_FILES['app']}")
        
        # 保存测试数据
        test_data = {
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "test_suites": [],
            "tracing_points": [],
            "anomalies": [],
            "performance_history": []
        }
        with open(DEFAULT_FILES['test'], 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已生成: {DEFAULT_FILES['test']}")
        
        print("[INFO] 示例数据生成完成！\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] 生成示例数据失败: {e}")
        print("[INFO] 将尝试创建最小化的数据文件...")
        
        # 备选方案：创建最小化数据
        try:
            create_minimal_data()
            return True
        except:
            return False


def create_minimal_data():
    """创建最小化数据（备选方案）"""
    # 项目数据
    project_data = {
        "project_name": "示例项目",
        "current_iteration": "ITER-001",
        "iterations": [
            {
                "iteration_id": "ITER-001",
                "iteration_name": "第一个迭代",
                "status": "in_progress",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "tasks": [],
                "modules": [],
                "assumptions": []
            }
        ]
    }
    
    # 应用状态
    app_data = {
        "app_name": "示例应用",
        "version": "v1.0.0",
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "modules": []
    }
    
    # 测试数据
    test_data = {
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "test_suites": [],
        "tracing_points": [],
        "anomalies": [],
        "performance_history": []
    }
    
    # 保存文件
    with open(DEFAULT_FILES['project'], 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 已生成: {DEFAULT_FILES['project']}")
    
    with open(DEFAULT_FILES['app'], 'w', encoding='utf-8') as f:
        json.dump(app_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 已生成: {DEFAULT_FILES['app']}")
    
    with open(DEFAULT_FILES['test'], 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 已生成: {DEFAULT_FILES['test']}")


def show_welcome():
    """显示欢迎信息"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   COX Dashboard - 一键启动                                    ║
║   为您的AI编程体验保驾护航                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def show_help():
    """显示帮助信息"""
    print("""
使用方式:
  python start_cox_dashboard.py           自动检测并启动Web模式
  python start_cox_dashboard.py --web     启动Web交互模式（推荐）
  python start_cox_dashboard.py --static  生成静态HTML文件
  python start_cox_dashboard.py --init    初始化示例数据
  python start_cox_dashboard.py -h        显示此帮助信息

启动后:
  - Web模式: 访问 http://localhost:5000 查看交互面板
  - 静态模式: 生成 observability.html，用浏览器打开

注意:
  - Web模式需要安装Flask: pip install flask
  - 如果数据文件不存在，将自动生成示例数据
    """)


def run_web_mode():
    """启动Web交互模式"""
    print("\n[INFO] 启动 Web 交互模式...")
    
    if not FLASK_AVAILABLE:
        print("\n[ERROR] Web模式需要Flask，但未检测到安装")
        print("[INFO] 请先安装Flask: pip install flask")
        print("[INFO] 或者使用静态模式: python start_cox_dashboard.py --static")
        return
    
    # 检查数据文件
    missing = check_files_exist()
    if missing:
        print(f"\n[WARNING] 缺少数据文件: {', '.join(missing)}")
        if not generate_sample_data():
            print("[ERROR] 无法创建示例数据")
            return
    
    # 导入并启动
    try:
        from run_web_observability import data_manager, app
        print("\n[INFO] COX Dashboard 已启动！")
        print("[INFO] 访问地址: http://localhost:5000")
        print("[INFO] 按 Ctrl+C 停止服务\n")
        print("-" * 50)
        
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
        
    except Exception as e:
        print(f"\n[ERROR] 启动失败: {e}")
        print("[INFO] 请尝试手动启动:")
        print("  python -m cox.scripts.run_web_observability --mode web")
        print("  --project project_data.json --app app_status.json --test test_data.json")


def run_static_mode():
    """生成静态HTML"""
    print("\n[INFO] 生成静态HTML文件...")
    
    # 检查数据文件
    missing = check_files_exist()
    if missing:
        print(f"\n[WARNING] 缺少数据文件: {', '.join(missing)}")
        if not generate_sample_data():
            print("[ERROR] 无法创建示例数据")
            return
    
    # 生成静态HTML
    try:
        from run_web_observability import get_static_html_template
        
        output_file = 'observability.html'
        
        # 读取现有数据文件
        data = {}
        for key, filename in DEFAULT_FILES.items():
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data[key] = json.load(f)
                print(f"  ✓ 已读取: {filename}")
            except FileNotFoundError:
                print(f"  ✗ 文件不存在: {filename}")
                data[key] = {}
            except json.JSONDecodeError:
                print(f"  ✗ JSON格式错误: {filename}")
                data[key] = {}
        
        # 生成内联数据的HTML
        inline_data_js = f"""
    // 静态模式：数据已内联到 HTML 中
    const staticData = {{
        project: {json.dumps(data.get('project', {}), ensure_ascii=False)},
        app: {json.dumps(data.get('app', {}), ensure_ascii=False)},
        test: {json.dumps(data.get('test', {}), ensure_ascii=False)},
        last_updated: new Date().toLocaleTimeString('zh-CN', {{hour: '2-digit', minute: '2-digit', second: '2-digit'}})
    }};
    // 标记为静态模式
    window.isStaticMode = true;
"""
        
        # 获取静态HTML模板并替换
        html_template = get_static_html_template()
        html_content = html_template.replace(
            '// {{STATIC_DATA_PLACEHOLDER}}',
            inline_data_js
        )
        
        # 将 renderUI 调用改为使用 staticData
        html_content = html_content.replace(
            'function renderUI(data) {',
            'function renderUI(data) {{\n            if (window.isStaticMode && typeof staticData !== "undefined") {{\n                data = staticData;\n            }}'
        )
        
        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n[SUCCESS] 静态HTML已生成: {output_file}")
        print("[INFO] 可以直接用浏览器打开查看")
        print("[INFO] 数据已内联到HTML文件中，无需额外的JSON文件\n")
        
    except Exception as e:
        print(f"\n[ERROR] 生成失败: {e}")
        print("[INFO] 请尝试手动生成:")
        print("  python -m cox.scripts.run_web_observability --mode static")
        print("  --project project_data.json --app app_status.json --test test_data.json")


def main():
    """主函数"""
    show_welcome()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='COX Dashboard 一键启动脚本',
        add_help=False
    )
    
    parser.add_argument('--web', action='store_true', help='启动Web交互模式')
    parser.add_argument('--static', action='store_true', help='生成静态HTML')
    parser.add_argument('--init', action='store_true', help='初始化示例数据')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')
    
    args = parser.parse_args()
    
    # 显示帮助
    if args.help:
        show_help()
        return
    
    # 初始化数据
    if args.init:
        generate_sample_data()
        return
    
    # 自动检测模式
    if args.web:
        run_web_mode()
    elif args.static:
        run_static_mode()
    else:
        # 默认启动Web模式（如果Flask可用）
        if FLASK_AVAILABLE:
            print("[INFO] 检测到Flask可用，将启动Web交互模式")
            print("[INFO] 使用 --static 参数可以生成静态HTML")
            print("")
            run_web_mode()
        else:
            print("[INFO] Flask未安装，将生成静态HTML")
            print("[INFO] 使用 --web 参数可以安装Flask后启动Web模式")
            print("")
            run_static_mode()


if __name__ == '__main__':
    main()
