#!/usr/bin/env python3
"""
Unit Test: Interactive Web Page Generation by Agent Call Script

Test Objectives:
1. Using mock data
2. Simulating agent call script to generate interactive web pages
3. Verifying that the DOM element count corresponding to tasks in the first iteration of the generated webpage is not 0
4. Automatically find available port and start Web server for testing
"""

import os
import json
import unittest
import tempfile
import shutil
import sys
import socket
import threading
import time
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cox.scripts.run_web_observability import app, ObservabilityData

class TestWebObservability(unittest.TestCase):
    """Test web observability functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        
        # Generate mock data
        self.generate_mock_data()
        
        # Initialize Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Global data_manager setup
        import cox.scripts.run_web_observability
        cox.scripts.run_web_observability.data_manager = ObservabilityData(
            os.path.join(self.temp_dir, 'project_data.json'),
            os.path.join(self.temp_dir, 'app_status.json'),
            os.path.join(self.temp_dir, 'test_metrics.json')
        )
        
        # Find available port
        self.test_port = self.find_available_port()
        self.server_thread = None
    
    def tearDown(self):
        """Clean up test environment"""
        # Don't automatically stop server, let user manually stop
        # Stop Web server
        # if self.server_thread and self.server_thread.is_alive():
        #     self.server_thread.join(timeout=1)
        
        # Delete temporary directory
        # shutil.rmtree(self.temp_dir)
        print(f"\nTemporary directory kept at: {self.temp_dir}")
        print(f"Please manually delete temporary directory or press Ctrl+C to stop server")
    
    def find_available_port(self, start_port=5001, max_attempts=100):
        """Find available port"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        raise Exception(f"Unable to find available port in range {start_port}-{start_port + max_attempts}")
    
    def generate_mock_data(self):
        """Generate mock data"""
        # Project data - containing iterations and tasks
        project_data = {
            "project_name": "Test Project",
            "current_iteration": "ITER-001",
            "iterations": [
                {
                    "iteration_id": "ITER-001",
                    "iteration_name": "First Iteration",
                    "start_date": "2026-02-01",
                    "end_date": "2026-02-15",
                    "status": "in_progress",
                    "modules": [],
                    "tasks": [
                        {
                            "task_id": "TASK-001",
                            "task_name": "Task 1",
                            "status": "todo",
                            "priority": "high"
                        },
                        {
                            "task_id": "TASK-002",
                            "task_name": "Task 2",
                            "status": "in_progress",
                            "priority": "medium"
                        }
                    ],
                    "assumptions": []
                },
                {
                    "iteration_id": "ITER-002",
                    "iteration_name": "Second Iteration",
                    "start_date": "2026-02-16",
                    "end_date": "2026-03-01",
                    "status": "todo",
                    "modules": [],
                    "tasks": [],
                    "assumptions": []
                }
            ],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # Application status data
        app_status = {
            "app_name": "Test App",
            "version": "1.0.0",
            "modules": [
                {
                    "module_id": "MOD-001",
                    "module_name": "Module 1",
                    "status": "confirmed",
                    "completion_rate": 1.0,
                    "issue_description": ""
                }
            ],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # Test metrics data
        test_metrics = {
            "test_suites": [],
            "anomalies": [],
            "performance_history": [],
            "last_updated": "2026-02-04 08:00:00"
        }
        
        # Write files
        with open(os.path.join(self.temp_dir, 'project_data.json'), 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(self.temp_dir, 'app_status.json'), 'w', encoding='utf-8') as f:
            json.dump(app_status, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(self.temp_dir, 'test_metrics.json'), 'w', encoding='utf-8') as f:
            json.dump(test_metrics, f, ensure_ascii=False, indent=2)
    
    def test_web_observability(self):
        """Test web observability functionality"""
        # Start Web server
        self.start_web_server()
        
        # Simulate agent call script (access through Flask test client)
        response = self.client.get('/')
        
        # Verify response status code
        self.assertEqual(response.status_code, 200)
        
        # Get response content
        html_content = response.data.decode('utf-8')
        
        # Verify HTML content contains necessary elements
        self.assertIn('Cox coding-Transparent and smooth interactive experience', html_content)
        
        # Verify DOM element count corresponding to tasks in first iteration is not 0
        # Find DOM elements related to tasks
        # Check if task list is included
        self.assertIn('task-list', html_content)
        
        # Check if task items are included
        # Since our mock data has 2 tasks in first iteration, it should contain task-related DOM elements
        # Check task-related DOM structure
        # Check task card elements
        task_card_count = html_content.count('bg-zinc-900/40 rounded-lg border border-zinc-800/30')
        self.assertGreater(task_card_count, 0, "DOM element count for tasks in first iteration is 0")
        
        # Check task status elements
        task_status_count = html_content.count('task status')
        # Even if task status doesn't appear directly, we should at least have task cards
        if task_status_count == 0:
            # As alternative check, ensure there are task-related contents
            self.assertGreater(task_card_count, 0, "DOM element count for tasks in first iteration is 0")
        
        # Check API data
        api_response = self.client.get('/api/data')
        self.assertEqual(api_response.status_code, 200)
        
        api_data = api_response.json
        self.assertIn('project', api_data)
        self.assertIn('iterations', api_data['project'])
        self.assertEqual(len(api_data['project']['iterations']), 2)
        self.assertEqual(len(api_data['project']['iterations'][0]['tasks']), 2)
        
        print(f"\nWeb server started on port {self.test_port}")
        print(f"Please visit http://127.0.0.1:{self.test_port} to view webpage")
        print(f"Server will keep running for 60 seconds for your verification...")
        print(f"After verification, press Ctrl+C to stop server")
        
        # Keep server running for 60 seconds for user verification
        time.sleep(60)
    
    def start_web_server(self):
        """Start Web server in background"""
        import cox.scripts.run_web_observability
        
        def run_server():
            cox.scripts.run_web_observability.server = app.run(
                host='127.0.0.1',
                port=self.test_port,
                debug=False,
                threaded=True,
                use_reloader=False
            )
        
        # Use non-daemon thread, so server continues running when main thread sleeps
        self.server_thread = threading.Thread(target=run_server, daemon=False)
        self.server_thread.start()
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()