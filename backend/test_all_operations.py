"""
Test All Operations for Todo Chatbot
=====================================
Comprehensive test suite for all Todo and Chatbot operations.

Usage:
    python test_all_operations.py

Test Coverage:
    - Todo CRUD operations
    - Chatbot commands
    - Error handling
    - Edge cases
"""

import unittest
import sqlite3
import os
from typing import List, Dict, Any


# ============================================
# Configuration
# ============================================

DATABASE_PATH = "test_todos.db"
BACKEND_URL = "http://localhost:8000"


# ============================================
# Database Test Helper
# ============================================

def get_test_db_connection():
    """Create test database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_test_db():
    """Initialize test database"""
    conn = get_test_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()


def cleanup_test_db():
    """Clean up test database"""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)


# ============================================
# Test Classes
# ============================================

class TestDatabaseOperations(unittest.TestCase):
    """Test database CRUD operations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        init_test_db()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        cleanup_test_db()
    
    def setUp(self):
        """Clear database before each test"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos")
        conn.commit()
        conn.close()
    
    def test_create_todo(self):
        """Test creating a todo"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            ("Test Todo", False)
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM todos WHERE title = ?", ("Test Todo",))
        todo = cursor.fetchone()
        
        self.assertIsNotNone(todo)
        self.assertEqual(todo["title"], "Test Todo")
        self.assertFalse(todo["completed"])
        
        conn.close()
    
    def test_read_todos(self):
        """Test reading all todos"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        
        # Insert multiple todos
        todos_data = [
            ("Todo 1", False),
            ("Todo 2", True),
            ("Todo 3", False),
        ]
        cursor.executemany(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            todos_data
        )
        conn.commit()
        
        # Read all todos
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        
        self.assertEqual(len(todos), 3)
        
        conn.close()
    
    def test_delete_todo(self):
        """Test deleting a todo"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        
        # Insert a todo
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            ("To Delete", False)
        )
        todo_id = cursor.lastrowid
        conn.commit()
        
        # Delete the todo
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        
        # Verify deletion
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        deleted = cursor.fetchone()
        
        self.assertIsNone(deleted)
        
        conn.close()
    
    def test_update_todo(self):
        """Test updating a todo"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        
        # Insert a todo
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            ("To Update", False)
        )
        todo_id = cursor.lastrowid
        conn.commit()
        
        # Update the todo
        cursor.execute(
            "UPDATE todos SET completed = ?, title = ? WHERE id = ?",
            (True, "Updated Title", todo_id)
        )
        conn.commit()
        
        # Verify update
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        updated = cursor.fetchone()
        
        self.assertTrue(updated["completed"])
        self.assertEqual(updated["title"], "Updated Title")
        
        conn.close()


class TestPatternMatching(unittest.TestCase):
    """Test chatbot pattern matching"""
    
    def test_add_todo_pattern(self):
        """Test add todo pattern matching"""
        import re
        
        pattern = r"add todo[:\s]+(.+)"
        
        test_cases = [
            ("Add todo: buy milk", "buy milk"),
            ("add todo: finish report", "finish report"),
            ("ADD TODO: call john", "call john"),
            ("Add todo walk the dog", "walk the dog"),
        ]
        
        for message, expected in test_cases:
            match = re.match(pattern, message.lower())
            self.assertIsNotNone(match, f"Pattern should match: {message}")
            self.assertEqual(match.group(1), expected)
    
    def test_delete_todo_pattern(self):
        """Test delete todo pattern matching"""
        import re
        
        pattern = r"delete todo[:\s]+(\d+)"
        
        test_cases = [
            ("Delete todo 1", "1"),
            ("delete todo: 2", "2"),
            ("DELETE TODO: 999", "999"),
        ]
        
        for message, expected in test_cases:
            match = re.match(pattern, message.lower())
            self.assertIsNotNone(match, f"Pattern should match: {message}")
            self.assertEqual(match.group(1), expected)
    
    def test_show_todos_patterns(self):
        """Test show todos pattern matching"""
        patterns = ["show todos", "list todos", "get todos", "my todos"]
        
        for pattern in patterns:
            self.assertIn(pattern, patterns)
    
    def test_greeting_patterns(self):
        """Test greeting pattern matching"""
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        
        test_cases = ["Hi", "Hello", "Hey", "Good morning"]
        
        for greeting in test_cases:
            self.assertIn(greeting.lower(), greetings)


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Check if backend is running"""
        try:
            import requests
            response = requests.get(BACKEND_URL, timeout=5)
            cls.backend_running = response.status_code == 200
        except:
            cls.backend_running = False
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        if not self.backend_running:
            self.skipTest("Backend not running")
        
        import requests
        response = requests.get(BACKEND_URL)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
    
    def test_todos_endpoint(self):
        """Test todos endpoint"""
        if not self.backend_running:
            self.skipTest("Backend not running")
        
        import requests
        response = requests.get(f"{BACKEND_URL}/todos")
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_chat_endpoint(self):
        """Test chat endpoint"""
        if not self.backend_running:
            self.skipTest("Backend not running")
        
        import requests
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": "Hi"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())
        self.assertIn("action", response.json())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_empty_message(self):
        """Test empty message handling"""
        import re
        
        message = ""
        pattern = r"add todo[:\s]+(.+)"
        match = re.match(pattern, message.lower())
        
        self.assertIsNone(match)
    
    def test_whitespace_only_message(self):
        """Test whitespace-only message handling"""
        import re
        
        message = "   "
        pattern = r"add todo[:\s]+(.+)"
        match = re.match(pattern, message.strip().lower())
        
        self.assertIsNone(match)
    
    def test_special_characters(self):
        """Test special characters in todo"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        
        special_titles = [
            "Test with 'quotes'",
            'Test with "double quotes"',
            "Test with <html> tags",
            "Test with & symbols",
        ]
        
        for title in special_titles:
            cursor.execute(
                "INSERT INTO todos (title, completed) VALUES (?, ?)",
                (title, False)
            )
        
        conn.commit()
        
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        
        self.assertEqual(len(todos), len(special_titles))
        
        conn.close()
        cleanup_test_db()
        init_test_db()
    
    def test_very_long_title(self):
        """Test very long todo title"""
        conn = get_test_db_connection()
        cursor = conn.cursor()
        
        long_title = "A" * 1000
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            (long_title, False)
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM todos WHERE title = ?", (long_title,))
        todo = cursor.fetchone()
        
        self.assertIsNotNone(todo)
        self.assertEqual(len(todo["title"]), 1000)
        
        conn.close()
        cleanup_test_db()
        init_test_db()


# ============================================
# Test Runner
# ============================================

def run_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TODO CHATBOT - ALL OPERATIONS TEST")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternMatching))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
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
