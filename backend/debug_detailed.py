"""
Debug Detailed Script for Todo Chatbot
=======================================
This script provides detailed debugging information for the Todo Chatbot application.

Usage:
    python debug_detailed.py

Features:
    - Database connection testing
    - API endpoint testing
    - Pattern matching validation
    - Response format verification
"""

import sqlite3
import re
import json
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime


# ============================================
# Configuration
# ============================================

DATABASE_PATH = "todos.db"
BACKEND_URL = "http://localhost:8000"


# ============================================
# Color Output for Terminal
# ============================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


# ============================================
# Database Debugging
# ============================================

def test_database_connection() -> bool:
    """Test database connection"""
    print_header("DATABASE CONNECTION TEST")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        print_success(f"Connected to database: {DATABASE_PATH}")
        
        # Check if todos table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='todos'
        """)
        table = cursor.fetchone()
        
        if table:
            print_success("Table 'todos' exists")
            
            # Get table schema
            cursor.execute("PRAGMA table_info(todos)")
            columns = cursor.fetchall()
            print_info("Table schema:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM todos")
            count = cursor.fetchone()[0]
            print_info(f"Total todos in database: {count}")
            
            # Show sample records
            if count > 0:
                cursor.execute("SELECT * FROM todos LIMIT 5")
                records = cursor.fetchall()
                print_info("Sample records:")
                for record in records:
                    print(f"  ID: {record[0]}, Title: {record[1]}, Completed: {record[2]}")
        else:
            print_warning("Table 'todos' does not exist")
            
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print_error(f"Database error: {e}")
        return False


# ============================================
# Pattern Matching Debugging
# ============================================

def test_pattern_matching():
    """Test chatbot pattern matching"""
    print_header("PATTERN MATCHING TEST")
    
    patterns = {
        "add todo": r"add todo[:\s]+(.+)",
        "delete todo": r"delete todo[:\s]+(\d+)",
        "show todos": ["show todos", "list todos", "get todos", "my todos"],
        "greetings": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"],
    }
    
    test_messages = [
        "Add todo: buy milk",
        "add todo: finish report",
        "ADD TODO: call john",
        "Delete todo 1",
        "delete todo: 2",
        "Show todos",
        "list todos",
        "get todos",
        "my todos",
        "Hi",
        "hello",
        "Hey",
        "Good morning",
        "Random message",
    ]
    
    for message in test_messages:
        msg_lower = message.lower()
        matched = False
        
        # Test add todo pattern
        match = re.match(patterns["add todo"], msg_lower)
        if match:
            print_success(f"'{message}' → ADD TODO: '{match.group(1)}'")
            matched = True
            continue
        
        # Test delete todo pattern
        match = re.match(patterns["delete todo"], msg_lower)
        if match:
            print_success(f"'{message}' → DELETE TODO: ID {match.group(1)}")
            matched = True
            continue
        
        # Test show todos
        if msg_lower in patterns["show todos"]:
            print_success(f"'{message}' → SHOW TODOS")
            matched = True
            continue
        
        # Test greetings
        if msg_lower in patterns["greetings"]:
            print_success(f"'{message}' → GREETING")
            matched = True
            continue
        
        # No match
        if not matched:
            print_warning(f"'{message}' → NO MATCH (unknown)")


# ============================================
# API Endpoint Testing
# ============================================

def test_api_endpoints():
    """Test API endpoints"""
    print_header("API ENDPOINT TEST")
    
    try:
        import requests
    except ImportError:
        print_error("requests library not installed. Run: pip install requests")
        return
    
    endpoints = [
        ("GET", "/", "Health Check"),
        ("GET", "/todos", "Get Todos"),
        ("POST", "/chat", "Chat Endpoint"),
    ]
    
    for method, path, description in endpoints:
        try:
            url = f"{BACKEND_URL}{path}"
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json={"message": "test"}, timeout=5)
            
            status = f"{response.status_code}"
            if response.status_code == 200:
                print_success(f"{method} {path} ({description}) - {status}")
            else:
                print_warning(f"{method} {path} ({description}) - {status}")
                
        except requests.exceptions.ConnectionError:
            print_error(f"{method} {path} ({description}) - Backend not running")
        except requests.exceptions.Timeout:
            print_error(f"{method} {path} ({description}) - Timeout")
        except Exception as e:
            print_error(f"{method} {path} ({description}) - {e}")


# ============================================
# Response Format Validation
# ============================================

def validate_response_format():
    """Validate chatbot response format"""
    print_header("RESPONSE FORMAT VALIDATION")
    
    try:
        import requests
        
        test_cases = [
            {"message": "Add todo: test item", "expected_action": "add"},
            {"message": "Show todos", "expected_action": "show"},
            {"message": "Delete todo 1", "expected_action": "delete"},
            {"message": "Hello", "expected_action": "greeting"},
            {"message": "Help", "expected_action": "help"},
            {"message": "Random text", "expected_action": "unknown"},
        ]
        
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": test_case["message"]},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    has_response = "response" in data
                    has_action = "action" in data
                    action_matches = data.get("action") == test_case["expected_action"]
                    
                    if has_response and has_action:
                        if action_matches:
                            print_success(f"'{test_case['message']}' → Valid format (action: {data['action']})")
                        else:
                            print_warning(f"'{test_case['message']}' → Wrong action: expected {test_case['expected_action']}, got {data['action']}")
                    else:
                        print_error(f"'{test_case['message']}' → Missing fields (response: {has_response}, action: {has_action})")
                else:
                    print_error(f"'{test_case['message']}' → HTTP {response.status_code}")
                    
            except Exception as e:
                print_error(f"'{test_case['message']}' → {e}")
                
    except ImportError:
        print_error("requests library not installed")
    except Exception as e:
        print_error(f"Validation error: {e}")


# ============================================
# Performance Testing
# ============================================

def test_performance():
    """Test API performance"""
    print_header("PERFORMANCE TEST")
    
    try:
        import requests
        import time
        
        iterations = 10
        times = []
        
        print_info(f"Running {iterations} requests...")
        
        for i in range(iterations):
            start = time.time()
            response = requests.get(f"{BACKEND_URL}/", timeout=5)
            end = time.time()
            
            if response.status_code == 200:
                times.append(end - start)
        
        if times:
            avg_time = sum(times) / len(times) * 1000  # Convert to ms
            min_time = min(times) * 1000
            max_time = max(times) * 1000
            
            print_success(f"Average response time: {avg_time:.2f}ms")
            print_info(f"Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")
            
            if avg_time < 100:
                print_success("Performance is excellent!")
            elif avg_time < 500:
                print_info("Performance is good")
            else:
                print_warning("Performance may need optimization")
        else:
            print_error("No successful requests")
            
    except ImportError:
        print_error("requests library not installed")
    except Exception as e:
        print_error(f"Performance test error: {e}")


# ============================================
# Main Execution
# ============================================

def main():
    """Main debug function"""
    print_header("TODO CHATBOT DEBUG REPORT")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Database: {DATABASE_PATH}")
    print(f"Backend URL: {BACKEND_URL}")
    
    # Run all tests
    test_database_connection()
    test_pattern_matching()
    test_api_endpoints()
    validate_response_format()
    test_performance()
    
    print_header("DEBUG COMPLETE")


if __name__ == "__main__":
    main()
