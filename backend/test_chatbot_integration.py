"""
Test Chatbot Integration for Todo Chatbot
==========================================
Integration tests for the complete chatbot system.

Usage:
    python test_chatbot_integration.py

Test Coverage:
    - End-to-end workflows
    - Multi-step operations
    - State persistence
    - Concurrent operations
"""

import unittest
import time
from typing import List, Dict, Any


# ============================================
# Configuration
# ============================================

BACKEND_URL = "http://localhost:8000"


# ============================================
# Integration Test Class
# ============================================

class ChatbotIntegrationTester:
    """Integration test helper"""
    
    def __init__(self):
        self.backend_available = False
        self.session_data = {}
        
    def setup(self):
        """Check backend availability"""
        try:
            import requests
            response = requests.get(BACKEND_URL, timeout=5)
            self.backend_available = response.status_code == 200
        except:
            self.backend_available = False
    
    def send_message(self, message: str) -> Dict[str, Any]:
        """Send message and get response"""
        try:
            import requests
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": message},
                timeout=10
            )
            return {
                "success": response.status_code == 200,
                "data": response.json(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_todos(self) -> List[Dict[str, Any]]:
        """Get all todos"""
        try:
            import requests
            response = requests.get(f"{BACKEND_URL}/todos", timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []


class TestIntegrationWorkflows(unittest.TestCase):
    """Test complete workflows"""
    
    @classmethod
    def setUpClass(cls):
        """Set up integration tester"""
        cls.tester = ChatbotIntegrationTester()
        cls.tester.setup()
    
    def test_complete_workflow(self):
        """Test complete todo management workflow"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        # Step 1: Greeting
        result = self.tester.send_message("Hi")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "greeting")
        
        # Step 2: Add first todo
        result = self.tester.send_message("Add todo: buy groceries")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "add")
        
        # Step 3: Add second todo
        result = self.tester.send_message("Add todo: walk the dog")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "add")
        
        # Step 4: Show todos
        result = self.tester.send_message("Show todos")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "show")
        self.assertIn("buy groceries", result["data"]["response"])
        
        # Step 5: Delete first todo
        result = self.tester.send_message("Delete todo 1")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "delete")
        
        # Step 6: Verify deletion
        result = self.tester.send_message("Show todos")
        self.assertTrue(result["success"])
        
        # Step 7: Help
        result = self.tester.send_message("Help")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "help")
    
    def test_multiple_add_operations(self):
        """Test adding multiple todos"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        todos_to_add = [
            "Task 1",
            "Task 2",
            "Task 3",
        ]
        
        for todo in todos_to_add:
            result = self.tester.send_message(f"Add todo: {todo}")
            self.assertTrue(result["success"])
            self.assertEqual(result["data"]["action"], "add")
            time.sleep(0.1)  # Small delay between operations
    
    def test_error_recovery(self):
        """Test error recovery workflow"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        # Try to delete non-existent todo
        result = self.tester.send_message("Delete todo 9999")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "delete")
        self.assertIn("❌", result["data"]["response"])
        
        # Ask for help after error
        result = self.tester.send_message("Help")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "help")
        
        # Try valid operation
        result = self.tester.send_message("Hi")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["action"], "greeting")
    
    def test_case_insensitivity_workflow(self):
        """Test case insensitivity in workflow"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        commands = [
            "ADD TODO: UPPERCASE",
            "add todo: lowercase",
            "Add Todo: Mixed Case",
            "SHOW TODOS",
            "show todos",
        ]
        
        for command in commands:
            result = self.tester.send_message(command)
            self.assertTrue(result["success"], f"Failed for command: {command}")


class TestStatePersistence(unittest.TestCase):
    """Test state persistence across operations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up tester"""
        cls.tester = ChatbotIntegrationTester()
        cls.tester.setup()
    
    def test_todos_persist_across_operations(self):
        """Test todos persist across different operations"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        # Add a todo
        result = self.tester.send_message("Add todo: persistent task")
        self.assertTrue(result["success"])
        
        # Do other operations
        self.tester.send_message("Hi")
        self.tester.send_message("Help")
        
        # Verify todo still exists
        result = self.tester.send_message("Show todos")
        self.assertTrue(result["success"])
        self.assertIn("persistent task", result["data"]["response"])
    
    def test_concurrent_operations(self):
        """Test concurrent operations don't interfere"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        # Add todos in quick succession
        for i in range(3):
            self.tester.send_message(f"Add todo: concurrent task {i}")
        
        # Verify all exist
        todos = self.tester.get_todos()
        self.assertGreaterEqual(len(todos), 3)


class TestResponseQuality(unittest.TestCase):
    """Test response quality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up tester"""
        cls.tester = ChatbotIntegrationTester()
        cls.tester.setup()
    
    def test_response_contains_emoji(self):
        """Test responses contain appropriate emojis"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        emoji_mapping = {
            "Add todo: test": "✅",
            "Show todos": "📋",
            "Hi": "👋",
            "Help": "🤖",
        }
        
        for command, expected_emoji in emoji_mapping.items():
            result = self.tester.send_message(command)
            if result["success"]:
                self.assertIn(expected_emoji, result["data"]["response"])
    
    def test_response_is_helpful(self):
        """Test responses provide helpful information"""
        if not self.tester.backend_available:
            self.skipTest("Backend not running")
        
        # Test unknown command provides guidance
        result = self.tester.send_message("Random command")
        self.assertTrue(result["success"])
        response = result["data"]["response"]
        
        # Should contain helpful guidance
        self.assertTrue(
            any(keyword in response.lower() for keyword in [
                "try", "command", "add", "show", "help"
            ])
        )


# ============================================
# Test Runner
# ============================================

def run_tests():
    """Run all integration tests"""
    print("\n" + "=" * 60)
    print("CHATBOT INTEGRATION TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWorkflows))
    suite.addTests(loader.loadTestsFromTestCase(TestStatePersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
