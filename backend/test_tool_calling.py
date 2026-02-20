"""
Test Tool Calling for Todo Chatbot
===================================
Test tool/function calling capabilities of the chatbot.

Usage:
    python test_tool_calling.py

Test Coverage:
    - Function mapping
    - Parameter extraction
    - Tool execution
    - Error handling
"""

import unittest
import re
from typing import Dict, Any, List, Optional, Callable


# ============================================
# Tool Definitions
# ============================================

class TodoTools:
    """Todo management tools"""
    
    def __init__(self):
        self.todos = []
        self.next_id = 1
    
    def add_todo(self, title: str) -> Dict[str, Any]:
        """Add a new todo"""
        todo = {
            "id": self.next_id,
            "title": title,
            "completed": False
        }
        self.todos.append(todo)
        self.next_id += 1
        
        return {
            "success": True,
            "id": todo["id"],
            "title": todo["title"],
            "message": f"✅ Todo added successfully! (ID: {todo['id']}): {todo['title']}"
        }
    
    def show_todos(self) -> Dict[str, Any]:
        """Show all todos"""
        if not self.todos:
            return {
                "success": True,
                "message": "📋 You have no todos yet. Add one by saying: 'Add todo: buy milk'"
            }
        
        todo_list = "\n".join([
            f"  {t['id']}. {t['title']} {'✓' if t['completed'] else ''}"
            for t in self.todos
        ])
        
        return {
            "success": True,
            "message": f"📋 Your todos:\n{todo_list}"
        }
    
    def delete_todo(self, todo_id: int) -> Dict[str, Any]:
        """Delete a todo by ID"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                self.todos.pop(i)
                return {
                    "success": True,
                    "message": f"✅ Todo {todo_id} deleted successfully!"
                }
        
        return {
            "success": False,
            "message": f"❌ Todo with ID {todo_id} not found."
        }


# ============================================
# Pattern Matchers
# ============================================

class PatternMatchers:
    """Pattern matching utilities"""
    
    @staticmethod
    def match_add_todo(message: str) -> Optional[str]:
        """Match add todo command"""
        pattern = r"add todo[:\s]+(.+)"
        match = re.match(pattern, message.lower())
        return match.group(1).strip() if match else None
    
    @staticmethod
    def match_delete_todo(message: str) -> Optional[int]:
        """Match delete todo command"""
        pattern = r"delete todo[:\s]+(\d+)"
        match = re.match(pattern, message.lower())
        return int(match.group(1)) if match else None
    
    @staticmethod
    def match_show_todos(message: str) -> bool:
        """Match show todos command"""
        patterns = ["show todos", "list todos", "get todos", "my todos"]
        return message.lower() in patterns
    
    @staticmethod
    def match_greeting(message: str) -> bool:
        """Match greeting"""
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        return message.lower() in greetings
    
    @staticmethod
    def match_help(message: str) -> bool:
        """Match help command"""
        return "help" in message.lower()


# ============================================
# Tool Executor
# ============================================

class ToolExecutor:
    """Execute tools based on matched patterns"""
    
    def __init__(self):
        self.tools = TodoTools()
        self.matchers = PatternMatchers()
    
    def execute(self, message: str) -> Dict[str, Any]:
        """Execute appropriate tool based on message"""
        message = message.strip()
        
        # Try add todo
        todo_title = self.matchers.match_add_todo(message)
        if todo_title:
            return self.tools.add_todo(todo_title)
        
        # Try delete todo
        todo_id = self.matchers.match_delete_todo(message)
        if todo_id is not None:
            return self.tools.delete_todo(todo_id)
        
        # Try show todos
        if self.matchers.match_show_todos(message):
            return self.tools.show_todos()
        
        # Try greeting
        if self.matchers.match_greeting(message):
            return {
                "success": True,
                "message": "👋 Hello! I'm your Todo Assistant. I can help you manage your todos. Try:\n"
                           "• 'Add todo: buy milk'\n"
                           "• 'Show todos'\n"
                           "• 'Delete todo 1'"
            }
        
        # Try help
        if self.matchers.match_help(message):
            return {
                "success": True,
                "message": "🤖 I'm your Todo Assistant! Here's what I can do:\n"
                           "• 'Add todo: <task>' - Add a new todo\n"
                           "• 'Show todos' - View all your todos\n"
                           "• 'Delete todo <id>' - Delete a todo by ID\n"
                           "• Say 'Hi' for a greeting"
            }
        
        # Unknown command
        return {
            "success": False,
            "message": "🤔 I'm not sure I understand. Try one of these commands:\n"
                       "• 'Add todo: buy milk'\n"
                       "• 'Show todos'\n"
                       "• 'Delete todo 1'\n"
                       "• Or just say 'Hi'!"
        }


# ============================================
# Test Cases
# ============================================

class TestToolCalling(unittest.TestCase):
    """Test tool calling functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.executor = ToolExecutor()
    
    def test_add_todo_tool(self):
        """Test add todo tool execution"""
        result = self.executor.execute("Add todo: buy milk")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["title"], "buy milk")
        self.assertIn("✅", result["message"])
    
    def test_show_todos_tool(self):
        """Test show todos tool execution"""
        # Add a todo first
        self.executor.execute("Add todo: test task")
        
        # Show todos
        result = self.executor.execute("Show todos")
        
        self.assertTrue(result["success"])
        self.assertIn("📋", result["message"])
        self.assertIn("test task", result["message"])
    
    def test_delete_todo_tool(self):
        """Test delete todo tool execution"""
        # Add a todo
        self.executor.execute("Add todo: to delete")
        
        # Delete it
        result = self.executor.execute("Delete todo 1")
        
        self.assertTrue(result["success"])
        self.assertIn("✅", result["message"])
    
    def test_delete_nonexistent_tool(self):
        """Test delete non-existent todo"""
        result = self.executor.execute("Delete todo 999")
        
        self.assertFalse(result["success"])
        self.assertIn("❌", result["message"])
        self.assertIn("not found", result["message"].lower())
    
    def test_greeting_tool(self):
        """Test greeting tool execution"""
        result = self.executor.execute("Hi")
        
        self.assertTrue(result["success"])
        self.assertIn("👋", result["message"])
    
    def test_help_tool(self):
        """Test help tool execution"""
        result = self.executor.execute("Help")
        
        self.assertTrue(result["success"])
        self.assertIn("🤖", result["message"])
    
    def test_unknown_command_tool(self):
        """Test unknown command handling"""
        result = self.executor.execute("Random command xyz")
        
        self.assertFalse(result["success"])
        self.assertIn("🤔", result["message"])


class TestPatternMatching(unittest.TestCase):
    """Test pattern matching"""
    
    def test_add_todo_patterns(self):
        """Test add todo pattern matching"""
        patterns = [
            "Add todo: buy milk",
            "add todo: finish report",
            "ADD TODO: call john",
            "Add todo walk the dog",
        ]
        
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                result = PatternMatchers.match_add_todo(pattern)
                self.assertIsNotNone(result)
    
    def test_delete_todo_patterns(self):
        """Test delete todo pattern matching"""
        patterns = [
            ("Delete todo 1", 1),
            ("delete todo: 2", 2),
            ("DELETE TODO: 999", 999),
        ]
        
        for pattern, expected_id in patterns:
            with self.subTest(pattern=pattern):
                result = PatternMatchers.match_delete_todo(pattern)
                self.assertEqual(result, expected_id)
    
    def test_show_todos_patterns(self):
        """Test show todos pattern matching"""
        patterns = [
            "Show todos",
            "List todos",
            "Get todos",
            "My todos",
        ]
        
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                result = PatternMatchers.match_show_todos(pattern)
                self.assertTrue(result)
    
    def test_greeting_patterns(self):
        """Test greeting pattern matching"""
        patterns = [
            "Hi",
            "Hello",
            "Hey",
            "Good morning",
        ]
        
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                result = PatternMatchers.match_greeting(pattern)
                self.assertTrue(result)


class TestToolState(unittest.TestCase):
    """Test tool state management"""
    
    def test_state_persistence(self):
        """Test state persists across operations"""
        executor = ToolExecutor()
        
        # Add todo
        executor.execute("Add todo: persistent task")
        
        # Do other operations
        executor.execute("Hi")
        executor.execute("Help")
        
        # Verify todo still exists
        result = executor.execute("Show todos")
        self.assertIn("persistent task", result["message"])
    
    def test_multiple_todos(self):
        """Test multiple todos management"""
        executor = ToolExecutor()
        
        # Add multiple todos
        for i in range(5):
            executor.execute(f"Add todo: task {i}")
        
        # Verify all exist
        result = executor.execute("Show todos")
        for i in range(5):
            self.assertIn(f"task {i}", result["message"])


# ============================================
# Test Runner
# ============================================

def run_tests():
    """Run all tool calling tests"""
    print("\n" + "=" * 60)
    print("TOOL CALLING TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestToolCalling))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternMatching))
    suite.addTests(loader.loadTestsFromTestCase(TestToolState))
    
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
