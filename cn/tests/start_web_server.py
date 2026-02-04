#!/usr/bin/env python3
"""
启动Web服务器供测试验证

自动查找可用端口并启动Web服务器
"""

import os
import sys
import socket
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from cox.scripts.run_web_observability import app, ObservabilityData

def find_available_port(start_port=5001, max_attempts=100):
    """查找可用的端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise Exception(f"无法在 {start_port}-{start_port + max_attempts} 范围内找到可用端口")

def main():
    # 查找可用端口
    port = find_available_port()
    
    # 使用当前目录的数据文件
    data_manager = ObservabilityData(
        'project_data.json',
        'app_status.json',
        'test_data.json'
    )
    
    # 设置全局data_manager
    import cox.scripts.run_web_observability
    cox.scripts.run_web_observability.data_manager = data_manager
    
    print(f"\n{'='*60}")
    print(f"Web服务器启动成功")
    print(f"{'='*60}")
    print(f"\n访问地址: http://127.0.0.1:{port}")
    print(f"\n按 Ctrl+C 停止服务器")
    print(f"\n服务器将保持运行，您可以随时在浏览器中访问验证")
    print(f"{'='*60}\n")
    
    # 启动服务器
    app.run(
        host='127.0.0.1',
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False
    )

if __name__ == '__main__':
    main()