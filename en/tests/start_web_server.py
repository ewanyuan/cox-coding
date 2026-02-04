#!/usr/bin/env python3
"""
Start Web Server for Test Verification

Automatically find available port and start Web server
"""

import os
import sys
import socket
import time
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cox.scripts.run_web_observability import app, ObservabilityData

def find_available_port(start_port=5001, max_attempts=100):
    """Find available port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise Exception(f"Unable to find available port in range {start_port}-{start_port + max_attempts}")

def main():
    # Find available port
    port = find_available_port()
    
    # Use data files in current directory
    data_manager = ObservabilityData(
        'project_data.json',
        'app_status.json',
        'test_data.json'
    )
    
    # Set global data_manager
    import cox.scripts.run_web_observability
    cox.scripts.run_web_observability.data_manager = data_manager
    
    print(f"\n{'='*60}")
    print(f"Web server started successfully")
    print(f"{'='*60}")
    print(f"\nAccess address: http://127.0.0.1:{port}")
    print(f"\nPress Ctrl+C to stop server")
    print(f"\nServer will keep running, you can access and verify in browser anytime")
    print(f"{'='*60}\n")
    
    # Start server
    app.run(
        host='127.0.0.1',
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False
    )

if __name__ == '__main__':
    main()