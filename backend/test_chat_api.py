"""
Test Chat API for Todo Chatbot
===============================
Test suite specifically for the chat endpoint.

Usage:
    python test_chat_api.py

Test Coverage:
    - All chatbot commands
    - Response format validation
    - Action type verification
"""

import unittest
import json
from typing import Dict, Any, List, Optional


# ============================================
# Configuration
# ============================================

BACKEND_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"


# ============================================
# Test Helper Class
# ============================================

class ChatAPITester:
    """Helper class for chat API testing"""
    
    def __init__(self):
        self.session = None
        self.backend_available = False
        
    def setup(self):
        """Check if backend is available"""
        try:
            import requests
            response = requests.get(BACKEND_URL, timeout=5)
            self.backend_available = response.status_code == 200
        except:
            self.backend_available = False
    
    def send_message(self, message: str) -> Optional[Dict[str, Any]]:
        """Send message to chat API"""
        if not self.backend_available:
            return None
        
        try:
            import requests
            response = requests.post(
                CHAT_ENDPOINT,
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            return {
                "status_code": response.status_code,
                "data": response.json(),
            }
        except Exception as e:
            return {"error": str(e)}


# ============================================
# Test Cases
# ============================================

class TestChatAPI(unittest.TestCase):
    """Test chat API endpoint"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.tester = ChatAPITester()
        cls.tester.setup()
    
    def assert_valid_response(self, response: Optional[Dict[str, Any]], test_name: str):
        """Assert response is valid"""
        if response is None:
            self.skipTest(f"{test_name}: Backend not running")
        
        if "error" in response:
            self.fail(f"{test_name}: {response['error']}")
        
        self.assertEqual(response["status_code"], 200, f"{test_name}: HTTP status not 200")
        self.assertIn("data", response, f"{test_name}: No data in response")
        
        data = response["data"]
        self.assertIn("response", data, f"{test_name}: Missing 'response' field")
        self.assertIn("action", data, f"{test_name}: Missing 'action' field")
    
    def test_add_todo_basic(self):
        """Test basic add todo command"""
        response = self.tester.send_message("Add todo: buy milk")
        self.assert_valid_response(response, "Add Todo Basic")
        
        data = response["data"]
        self.assertEqual(data["action"], "add")
        self.assertIn("✅", data["response"])
        self.assertIn("added", data["response"].lower())
    
    def test_add_todo_variations(self):
        """Test add todo with different formats"""
        variations = [
            "Add todo: task 1",
            "add todo: task 2",
            "ADD TODO: task 3",
            "Add todo task 4",
        ]
        
        for variation in variations:
            with self.subTest(variation=variation):
                response = self.tester.send_message(variation)
                self.assert_valid_response(response, f"Add Todo Variation: {variation}")
                self.assertEqual(response["data"]["action"], "add")
    
    def test_show_todos(self):
        """Test show todos command"""
        response = self.tester.send_message("Show todos")
        self.assert_valid_response(response, "Show Todos")
        
        data = response["data"]
        self.assertEqual(data["action"], "show")
        self.assertIn("📋", data["response"])
    
    def test_show_todos_alternatives(self):
        """Test alternative show todos commands"""
        alternatives = [
            "List todos",
            "Get todos",
            "My todos",
        ]
        
        for alt in alternatives:
            with self.subTest(alternative=alt):
                response = self.tester.send_message(alt)
                self.assert_valid_response(response, f"Show Todos Alt: {alt}")
                self.assertEqual(response["data"]["action"], "show")
    
    def test_delete_todo(self):
        """Test delete todo command"""
        # First add a todo
        add_response = self.tester.send_message("Add todo: to delete")
        self.assert_valid_response(add_response, "Delete Setup")
        
        # Then delete it
        response = self.tester.send_message("Delete todo 1")
        self.assert_valid_response(response, "Delete Todo")
        
        data = response["data"]
        self.assertEqual(data["action"], "delete")
        self.assertIn("✅", data["response"])
    
    def test_delete_nonexistent(self):
        """Test deleting non-existent todo"""
        response = self.tester.send_message("Delete todo 9999")
        self.assert_valid_response(response, "Delete Non-existent")
        
        data = response["data"]
        self.assertEqual(data["action"], "delete")
        self.assertIn("❌", data["response"])
        self.assertIn("not found", data["response"].lower())
    
    def test_greetings(self):
        """Test greeting commands"""
        greetings = [
            "Hi",
            "Hello",
            "Hey",
            "Good morning",
        ]
        
        for greeting in greetings:
            with self.subTest(greeting=greeting):
                response = self.tester.send_message(greeting)
                self.assert_valid_response(response, f"Greeting: {greeting}")
                self.assertEqual(response["data"]["action"], "greeting")
                self.assertIn("👋", response["data"]["response"])
    
    def test_help_command(self):
        """Test help command"""
        response = self.tester.send_message("Help")
        self.assert_valid_response(response, "Help Command")
        
        data = response["data"]
        self.assertEqual(data["action"], "help")
        self.assertIn("🤖", data["response"])
    
    def test_unknown_command(self):
        """Test unknown command handling"""
        response = self.tester.send_message("Random gibberish xyz123")
        self.assert_valid_response(response, "Unknown Command")
        
        data = response["data"]
        self.assertEqual(data["action"], "unknown")
        self.assertIn("🤔", data["response"])
    
    def test_empty_message(self):
        """Test empty message handling"""
        response = self.tester.send_message("")
        self.assert_valid_response(response, "Empty Message")
        
        data = response["data"]
        self.assertEqual(data["action"], "unknown")
    
    def test_response_format_consistency(self):
        """Test response format consistency"""
        commands = [
            "Hi",
            "Add todo: test",
            "Show todos",
            "Help",
        ]
        
        for command in commands:
            with self.subTest(command=command):
                response = self.tester.send_message(command)
                self.assert_valid_response(response, f"Format: {command}")
                
                # Check response type
                self.assertIsInstance(response["data"]["response"], str)
                self.assertIsInstance(response["data"]["action"], str)
    
    def test_response_time(self):
        """Test response time"""
        import time
        
        start = time.time()
        response = self.tester.send_message("Hi")
        elapsed = time.time() - start
        
        if response and "error" not in response:
            # Response should be under 1 second
            self.assertLess(elapsed, 1.0, "Response time too slow")


class TestChatAPIValidation(unittest.TestCase):
    """Test chat API response validation"""
    
    def test_action_types(self):
        """Test all action types are valid"""
        valid_actions = {"add", "show", "delete", "greeting", "help", "unknown"}
        
        tester = ChatAPITester()
        tester.setup()
        
        if not tester.backend_available:
            self.skipTest("Backend not running")
        
        test_commands = [
            ("Add todo: test", "add"),
            ("Show todos", "show"),
            ("Hi", "greeting"),
            ("Help", "help"),
            ("Random", "unknown"),
        ]
        
        for command, expected_action in test_commands:
            with self.subTest(command=command):
                response = tester.send_message(command)
                if response and "error" not in response:
                    self.assertIn(response["data"]["action"], valid_actions)


# ============================================
# Test Runner
# ============================================

def run_tests():
    """Run all chat API tests"""
    print("\n" + "=" * 60)
    print("CHAT API TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestChatAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestChatAPIValidation))
    
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
