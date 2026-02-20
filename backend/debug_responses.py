"""
Debug Responses Script for Todo Chatbot
========================================
This script helps debug and validate chatbot responses.

Usage:
    python debug_responses.py

Features:
    - Test all chatbot commands
    - Validate response formats
    - Check response times
    - Log detailed response information
"""

import json
import time
from typing import Dict, Any, List
from datetime import datetime


# ============================================
# Configuration
# ============================================

BACKEND_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"


# ============================================
# Test Cases
# ============================================

TEST_CASES: List[Dict[str, Any]] = [
    {
        "name": "Add Todo - Standard",
        "message": "Add todo: buy milk",
        "expected_action": "add",
        "expected_keywords": ["✅", "added", "ID"],
    },
    {
        "name": "Add Todo - Colon Format",
        "message": "Add todo: finish report",
        "expected_action": "add",
        "expected_keywords": ["✅", "added", "ID"],
    },
    {
        "name": "Add Todo - Space Format",
        "message": "Add todo call john",
        "expected_action": "add",
        "expected_keywords": ["✅", "added", "ID"],
    },
    {
        "name": "Show Todos - Standard",
        "message": "Show todos",
        "expected_action": "show",
        "expected_keywords": ["📋", "todos"],
    },
    {
        "name": "Show Todos - Alternative",
        "message": "List todos",
        "expected_action": "show",
        "expected_keywords": ["📋", "todos"],
    },
    {
        "name": "Show Todos - Get",
        "message": "Get todos",
        "expected_action": "show",
        "expected_keywords": ["📋", "todos"],
    },
    {
        "name": "Show Todos - My",
        "message": "My todos",
        "expected_action": "show",
        "expected_keywords": ["📋", "todos"],
    },
    {
        "name": "Delete Todo - Standard",
        "message": "Delete todo 1",
        "expected_action": "delete",
        "expected_keywords": ["✅", "deleted"],
    },
    {
        "name": "Delete Todo - Colon Format",
        "message": "Delete todo: 2",
        "expected_action": "delete",
        "expected_keywords": ["✅", "deleted"],
    },
    {
        "name": "Greeting - Hi",
        "message": "Hi",
        "expected_action": "greeting",
        "expected_keywords": ["👋", "Hello"],
    },
    {
        "name": "Greeting - Hello",
        "message": "Hello",
        "expected_action": "greeting",
        "expected_keywords": ["👋", "Hello"],
    },
    {
        "name": "Greeting - Hey",
        "message": "Hey",
        "expected_action": "greeting",
        "expected_keywords": ["👋", "Hello"],
    },
    {
        "name": "Greeting - Good Morning",
        "message": "Good morning",
        "expected_action": "greeting",
        "expected_keywords": ["👋", "Hello"],
    },
    {
        "name": "Help Command",
        "message": "Help",
        "expected_action": "help",
        "expected_keywords": ["🤖", "Todo Assistant"],
    },
    {
        "name": "Unknown Command",
        "message": "Random text here",
        "expected_action": "unknown",
        "expected_keywords": ["🤔", "not sure"],
    },
    {
        "name": "Empty Message",
        "message": "",
        "expected_action": "unknown",
        "expected_keywords": ["🤔", "not sure"],
    },
    {
        "name": "Case Insensitive - ADD TODO",
        "message": "ADD TODO: URGENT TASK",
        "expected_action": "add",
        "expected_keywords": ["✅", "added"],
    },
    {
        "name": "Case Insensitive - SHOW TODOS",
        "message": "SHOW TODOS",
        "expected_action": "show",
        "expected_keywords": ["📋"],
    },
]


# ============================================
# Response Debugger
# ============================================

class ResponseDebugger:
    """Debug chatbot responses"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def send_request(self, message: str) -> Dict[str, Any]:
        """Send request to chatbot API"""
        try:
            import requests
            
            start_time = time.time()
            response = requests.post(
                CHAT_ENDPOINT,
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            end_time = time.time()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json(),
                "response_time": (end_time - start_time) * 1000,  # ms
                "error": None,
            }
            
        except ImportError:
            return {
                "success": False,
                "status_code": None,
                "data": None,
                "response_time": 0,
                "error": "requests library not installed",
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "status_code": None,
                "data": None,
                "response_time": 0,
                "error": "Backend not running",
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "status_code": None,
                "data": None,
                "response_time": 0,
                "error": "Request timeout",
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "data": None,
                "response_time": 0,
                "error": str(e),
            }
    
    def validate_response(self, result: Dict[str, Any], test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response against expected values"""
        validation = {
            "passed": True,
            "errors": [],
            "warnings": [],
        }
        
        # Check if request was successful
        if not result["success"]:
            validation["passed"] = False
            validation["errors"].append(f"Request failed: {result['error']}")
            return validation
        
        # Check status code
        if result["status_code"] != 200:
            validation["passed"] = False
            validation["errors"].append(f"HTTP status: {result['status_code']}")
            return validation
        
        # Check response format
        data = result["data"]
        if "response" not in data:
            validation["passed"] = False
            validation["errors"].append("Missing 'response' field")
        
        if "action" not in data:
            validation["passed"] = False
            validation["errors"].append("Missing 'action' field")
        
        # Check action matches
        if data.get("action") != test_case["expected_action"]:
            validation["passed"] = False
            validation["errors"].append(
                f"Action mismatch: expected '{test_case['expected_action']}', got '{data.get('action')}'"
            )
        
        # Check expected keywords
        response_text = data.get("response", "").lower()
        for keyword in test_case["expected_keywords"]:
            if keyword.lower() not in response_text:
                validation["warnings"].append(f"Expected keyword not found: {keyword}")
        
        return validation
    
    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case"""
        result = self.send_request(test_case["message"])
        validation = self.validate_response(result, test_case)
        
        test_result = {
            "name": test_case["name"],
            "message": test_case["message"],
            "expected_action": test_case["expected_action"],
            "result": result,
            "validation": validation,
            "passed": validation["passed"],
        }
        
        self.total_tests += 1
        if validation["passed"]:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        return test_result
    
    def print_result(self, test_result: Dict[str, Any]):
        """Print test result"""
        status = "✓ PASS" if test_result["passed"] else "✗ FAIL"
        color = "\033[92m" if test_result["passed"] else "\033[91m"
        reset = "\033[0m"
        
        print(f"\n{color}{status}{reset} - {test_result['name']}")
        print(f"  Message: {test_result['message']}")
        
        if test_result["result"]["success"]:
            print(f"  Response Time: {test_result['result']['response_time']:.2f}ms")
            if test_result["result"]["data"]:
                print(f"  Action: {test_result['result']['data'].get('action', 'N/A')}")
                response = test_result["result"]["data"].get("response", "")
                if len(response) > 80:
                    response = response[:80] + "..."
                print(f"  Response: {response}")
        
        if test_result["validation"]["errors"]:
            print(f"  Errors: {', '.join(test_result['validation']['errors'])}")
        
        if test_result["validation"]["warnings"]:
            print(f"  Warnings: {', '.join(test_result['validation']['warnings'])}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests:  {self.total_tests}")
        print(f"Passed:       {self.passed_tests} ({self.passed_tests/self.total_tests*100:.1f}%)")
        print(f"Failed:       {self.failed_tests} ({self.failed_tests/self.total_tests*100:.1f}%)")
        print("=" * 60)


# ============================================
# Main Execution
# ============================================

def main():
    """Main debug function"""
    print("=" * 60)
    print("CHATBOT RESPONSE DEBUGGER")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Cases: {len(TEST_CASES)}")
    
    debugger = ResponseDebugger()
    
    for test_case in TEST_CASES:
        result = debugger.run_test(test_case)
        debugger.print_result(result)
    
    debugger.print_summary()
    
    # Save results to file
    results_file = f"debug_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "backend_url": BACKEND_URL,
                "total_tests": debugger.total_tests,
                "passed_tests": debugger.passed_tests,
                "failed_tests": debugger.failed_tests,
                "results": debugger.results,
            }, f, indent=2)
        print(f"\nResults saved to: {results_file}")
    except Exception as e:
        print(f"\nError saving results: {e}")


if __name__ == "__main__":
    main()
