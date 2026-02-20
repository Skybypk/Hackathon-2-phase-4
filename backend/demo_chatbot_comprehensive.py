"""
Demo Chatbot Comprehensive
===========================
A comprehensive demonstration of the Todo Chatbot functionality.

Usage:
    python demo_chatbot_comprehensive.py

Features:
    - Interactive chatbot demo
    - All command demonstrations
    - Error handling examples
    - Performance metrics
"""

import json
import time
from typing import Optional, Dict, Any
from datetime import datetime


# ============================================
# Configuration
# ============================================

BACKEND_URL = "http://localhost:8000"


# ============================================
# Chatbot Demo Class
# ============================================

class ChatbotDemo:
    """Comprehensive chatbot demonstration"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_history = []
        self.stats = {
            "commands_sent": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "total_time": 0,
        }
        
    def send_message(self, message: str) -> Optional[Dict[str, Any]]:
        """Send message to chatbot and get response"""
        try:
            import requests
            
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            end_time = time.time()
            
            self.stats["commands_sent"] += 1
            self.stats["total_time"] += (end_time - start_time)
            
            if response.status_code == 200:
                self.stats["successful_responses"] += 1
                data = response.json()
                return {
                    "success": True,
                    "data": data,
                    "response_time": (end_time - start_time) * 1000,
                }
            else:
                self.stats["failed_responses"] += 1
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response_time": (end_time - start_time) * 1000,
                }
                
        except ImportError:
            return {"success": False, "error": "requests library not installed"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Backend not running. Start with: python main.py"}
        except Exception as e:
            self.stats["failed_responses"] += 1
            return {"success": False, "error": str(e)}
    
    def print_response(self, result: Dict[str, Any], user_message: str):
        """Print formatted response"""
        print("\n" + "-" * 60)
        print(f"You: {user_message}")
        
        if result["success"]:
            data = result["data"]
            print(f"Bot: {data.get('response', 'No response')}")
            print(f"Action: {data.get('action', 'unknown')}")
            print(f"Response Time: {result['response_time']:.2f}ms")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print("-" * 60)
    
    def demo_basic_commands(self):
        """Demonstrate basic commands"""
        print("\n" + "=" * 60)
        print("BASIC COMMANDS DEMO")
        print("=" * 60)
        
        commands = [
            "Hi",
            "Add todo: buy groceries",
            "Add todo: walk the dog",
            "Add todo: finish the report",
            "Show todos",
            "Delete todo 1",
            "Show todos",
            "Help",
        ]
        
        for command in commands:
            result = self.send_message(command)
            self.print_response(result, command)
            time.sleep(0.5)
    
    def demo_error_handling(self):
        """Demonstrate error handling"""
        print("\n" + "=" * 60)
        print("ERROR HANDLING DEMO")
        print("=" * 60)
        
        commands = [
            "Delete todo 9999",  # Non-existent ID
            "",  # Empty message
            "Random gibberish",  # Unknown command
            "Add todo: ",  # Empty todo
        ]
        
        for command in commands:
            result = self.send_message(command)
            self.print_response(result, command)
            time.sleep(0.5)
    
    def demo_case_insensitivity(self):
        """Demonstrate case insensitivity"""
        print("\n" + "=" * 60)
        print("CASE INSENSITIVITY DEMO")
        print("=" * 60)
        
        commands = [
            "ADD TODO: UPPERCASE TASK",
            "add todo: lowercase task",
            "Add Todo: Mixed Case Task",
            "SHOW TODOS",
            "show todos",
            "Show Todos",
        ]
        
        for command in commands:
            result = self.send_message(command)
            self.print_response(result, command)
            time.sleep(0.5)
    
    def demo_alternative_commands(self):
        """Demonstrate alternative command formats"""
        print("\n" + "=" * 60)
        print("ALTERNATIVE COMMANDS DEMO")
        print("=" * 60)
        
        commands = [
            "List todos",
            "Get todos",
            "My todos",
            "Delete todo: 2",
            "Delete todo 3",
        ]
        
        for command in commands:
            result = self.send_message(command)
            self.print_response(result, command)
            time.sleep(0.5)
    
    def demo_greetings(self):
        """Demonstrate greeting responses"""
        print("\n" + "=" * 60)
        print("GREETINGS DEMO")
        print("=" * 60)
        
        greetings = [
            "Hi",
            "Hello",
            "Hey",
            "Good morning",
            "Good afternoon",
            "Good evening",
        ]
        
        for greeting in greetings:
            result = self.send_message(greeting)
            self.print_response(result, greeting)
            time.sleep(0.5)
    
    def print_stats(self):
        """Print session statistics"""
        print("\n" + "=" * 60)
        print("SESSION STATISTICS")
        print("=" * 60)
        print(f"Session ID: {self.session_id}")
        print(f"Commands Sent: {self.stats['commands_sent']}")
        print(f"Successful Responses: {self.stats['successful_responses']}")
        print(f"Failed Responses: {self.stats['failed_responses']}")
        
        if self.stats['commands_sent'] > 0:
            success_rate = (self.stats['successful_responses'] / self.stats['commands_sent']) * 100
            avg_time = (self.stats['total_time'] / self.stats['commands_sent']) * 1000
            print(f"Success Rate: {success_rate:.1f}%")
            print(f"Average Response Time: {avg_time:.2f}ms")
        
        print("=" * 60)
    
    def save_conversation(self):
        """Save conversation history to file"""
        filename = f"conversation_{self.session_id}.json"
        try:
            with open(filename, "w") as f:
                json.dump({
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "stats": self.stats,
                    "conversation": self.conversation_history,
                }, f, indent=2)
            print(f"\nConversation saved to: {filename}")
        except Exception as e:
            print(f"\nError saving conversation: {e}")
    
    def run_full_demo(self):
        """Run complete demonstration"""
        print("\n" + "=" * 60)
        print("TODO CHATBOT COMPREHENSIVE DEMO")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Backend URL: {BACKEND_URL}")
        
        # Check backend connection
        print("\nChecking backend connection...")
        result = self.send_message("Hi")
        if not result["success"]:
            print(f"Error: {result['error']}")
            print("\nPlease start the backend server:")
            print("  cd backend")
            print("  python main.py")
            return
        
        print("Backend connected successfully!")
        
        # Run demos
        self.demo_basic_commands()
        self.demo_error_handling()
        self.demo_case_insensitivity()
        self.demo_alternative_commands()
        self.demo_greetings()
        
        # Print statistics
        self.print_stats()
        
        # Save conversation
        self.save_conversation()
        
        print("\nDemo completed successfully!")


# ============================================
# Interactive Mode
# ============================================

def interactive_mode():
    """Run interactive chatbot session"""
    print("\n" + "=" * 60)
    print("INTERACTIVE CHATBOT MODE")
    print("=" * 60)
    print("Type your messages below. Type 'quit' to exit.\n")
    print("Available commands:")
    print("  - Add todo: <task>")
    print("  - Show todos / List todos / Get todos")
    print("  - Delete todo <id>")
    print("  - Hi / Hello / Hey")
    print("  - Help")
    print("=" * 60 + "\n")
    
    demo = ChatbotDemo()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\nGoodbye! 👋")
                demo.print_stats()
                break
            
            if not user_input:
                continue
            
            result = demo.send_message(user_input)
            demo.print_response(result, user_input)
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye! 👋")
            demo.print_stats()
            break
        except Exception as e:
            print(f"\nError: {e}")


# ============================================
# Main Execution
# ============================================

def main():
    """Main function"""
    print("\nTODO CHATBOT COMPREHENSIVE DEMO")
    print("=" * 60)
    print("\nSelect mode:")
    print("  1. Full Demo (automated)")
    print("  2. Interactive Mode")
    print("  3. Quick Test")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        demo = ChatbotDemo()
        demo.run_full_demo()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        demo = ChatbotDemo()
        print("\nRunning quick test...")
        test_commands = ["Hi", "Add todo: test task", "Show todos"]
        for cmd in test_commands:
            result = demo.send_message(cmd)
            demo.print_response(result, cmd)
        demo.print_stats()
    else:
        print("Invalid choice. Running quick test...")
        demo = ChatbotDemo()
        demo.run_full_demo()


if __name__ == "__main__":
    main()
