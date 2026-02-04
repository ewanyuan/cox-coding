#!/usr/bin/env python3
"""
Unit Test: Static Web Page Generation by Agent Call Script

Test Objectives:
1. Using mock data
2. Simulating agent call script to generate static web pages
3. Verifying that the DOM element count corresponding to tasks in the first iteration of the generated webpage is not 0
4. Generated static web pages need to be saved for user verification
"""

import os
import json
import unittest
import tempfile
import shutil
import sys
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestStaticObservability(unittest.TestCase):
    """Test static observability functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        
        # Generate mock data
        self.generate_mock_data()
        
        # Output file path
        self.output_html = os.path.join(self.temp_dir, 'observability.html')
        
        # Also generate one in the tests folder for user convenience
        self.user_output_html = os.path.join(Path(__file__).parent, 'static_observability_test.html')
    
    def tearDown(self):
        """Clean up test environment"""
        # Delete temporary directory
        shutil.rmtree(self.temp_dir)
        # Keep user viewing file for convenient user verification
    
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
    
    def test_static_observability(self):
        """Test static observability functionality"""
        # Import necessary modules
        from cox.scripts.run_web_observability import ObservabilityData, generate_static_html
        
        # Create data manager
        data_manager = ObservabilityData(
            os.path.join(self.temp_dir, 'project_data.json'),
            os.path.join(self.temp_dir, 'app_status.json'),
            os.path.join(self.temp_dir, 'test_metrics.json')
        )
        
        # Simulate agent call script to generate static web page
        # Call generate_static_html function to generate HTML file with inline data
        generate_static_html(data_manager, self.output_html)
        
        # Also generate user viewable file
        generate_static_html(data_manager, self.user_output_html)
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.output_html), "Static web page file not generated")
        self.assertTrue(os.path.exists(self.user_output_html), "User viewable static web page file not generated")
        
        # Read generated HTML content
        with open(self.output_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verify file size greater than 0
        self.assertGreater(len(html_content), 0, "Static web page file is empty")
        
        # Verify HTML content contains necessary elements
        self.assertIn('Cox Observability Panel', html_content)
        
        # Verify data is inlined to HTML
        self.assertIn('staticData', html_content, "Data not inlined to HTML")
        self.assertIn('Test Project', html_content, "Project name not displayed")
        
        # Verify DOM element count corresponding to tasks in first iteration is not 0
        # Check if task list is included
        self.assertIn('task-list', html_content)
        
        # Check if task-related DOM structure is included
        # Check task card elements - this is the task item style in task list
        task_card_count = html_content.count('bg-zinc-900/40 rounded-lg border border-zinc-800/30')
        self.assertGreater(task_card_count, 0, "DOM element count for tasks in first iteration is 0")
        
        # More precise check: verify task data is inlined
        self.assertIn('TASK-001', html_content, "Task 1 not displayed in HTML")
        self.assertIn('TASK-002', html_content, "Task 2 not displayed in HTML")
        self.assertIn('Task 1', html_content, "Task 1 name not displayed in HTML")
        self.assertIn('Task 2', html_content, "Task 2 name not displayed in HTML")
        
        print(f"\nStatic web page generated:")
        print(f"- Temporary test file: {self.output_html}")
        print(f"- User verification file: {self.user_output_html}")
        print(f"\nPlease open {self.user_output_html} to verify web content.")
        print(f"\nVerification points:")
        print(f"1. Page title displays 'Test Project'")
        print(f"2. Iteration management area displays '2 Iterations'")
        print(f"3. First iteration contains 2 tasks: 'Task 1' and 'Task 2'")
        print(f"4. Task status displayed correctly (todo/in_progress)")

if __name__ == '__main__':
    unittest.main()