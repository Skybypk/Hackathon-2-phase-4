"""
FastAPI Backend with Todo API and AI Chatbot
=============================================
This is the main application file containing:
- Todo CRUD operations (Create, Read, Delete)
- Chatbot endpoint that understands natural language commands
- In-memory SQLite database for persistence
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import re

# Initialize FastAPI app
app = FastAPI(
    title="Todo API with Chatbot",
    description="A simple Todo API with AI Chatbot integration",
    version="1.0.0"
)

# Enable CORS for frontend communication
# This allows the Next.js frontend to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ============================================
# Database Setup (SQLite - In-Memory)
# ============================================

def get_db_connection():
    """Create a database connection with row factory for dict-like access"""
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = get_db_connection()
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

# Initialize database on startup
init_db()

# ============================================
# Pydantic Models (Request/Response Schemas)
# ============================================

class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    title: str

class Todo(BaseModel):
    """Schema for a todo item"""
    id: int
    title: str
    completed: bool = False

class ChatRequest(BaseModel):
    """Schema for chatbot requests"""
    message: str

class ChatResponse(BaseModel):
    """Schema for chatbot responses"""
    response: str
    action: str  # e.g., "add", "show", "delete", "greeting", "unknown"

# ============================================
# Todo API Endpoints
# ============================================

@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    return {"message": "Todo API with Chatbot is running!", "version": "1.0.0"}

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    """
    Create a new todo item
    
    Request body:
    - title: The todo text
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, completed) VALUES (?, ?)",
        (todo.title, False)
    )
    conn.commit()
    todo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    new_todo = cursor.fetchone()
    conn.close()
    
    return dict(new_todo)

@app.get("/todos", response_model=List[Todo])
def get_todos():
    """
    Get all todo items
    
    Returns a list of all todos with their ID, title, and completion status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    conn.close()
    
    return [dict(todo) for todo in todos]

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """
    Delete a todo item by ID
    
    Returns success message if deleted, error if todo not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if todo exists
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Delete the todo
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"Todo {todo_id} deleted successfully"}

# ============================================
# Chatbot Endpoint
# ============================================

@app.post("/chat", response_model=ChatResponse)
def chat(chat_request: ChatRequest):
    """
    Chatbot endpoint that understands natural language commands
    
    Supported commands:
    - "add todo: <text>" - Creates a new todo
    - "show todos" - Lists all todos
    - "delete todo <id>" - Deletes a todo by ID
    - Greetings - Returns friendly response
    - Other messages - Returns helpful guidance
    """
    message = chat_request.message.lower().strip()
    
    # Pattern 1: Add Todo - "add todo: buy milk"
    add_pattern = r"add todo[:\s]+(.+)"
    match = re.match(add_pattern, message)
    if match:
        todo_title = match.group(1).strip()
        # Call the create_todo function internally
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            (todo_title, False)
        )
        conn.commit()
        todo_id = cursor.lastrowid
        conn.close()
        return ChatResponse(
            response=f"✅ Todo added successfully! (ID: {todo_id}): {todo_title}",
            action="add"
        )
    
    # Pattern 2: Show Todos - "show todos"
    if message in ["show todos", "list todos", "get todos", "my todos"]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        conn.close()
        
        if not todos:
            return ChatResponse(
                response="📋 You have no todos yet. Add one by saying: 'Add todo: buy milk'",
                action="show"
            )
        
        todo_list = "\n".join([f"  {t['id']}. {t['title']} {'✓' if t['completed'] else ''}" for t in todos])
        return ChatResponse(
            response=f"📋 Your todos:\n{todo_list}",
            action="show"
        )
    
    # Pattern 3: Delete Todo - "delete todo 1"
    delete_pattern = r"delete todo[:\s]+(\d+)"
    match = re.match(delete_pattern, message)
    if match:
        todo_id = int(match.group(1))
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        
        if not todo:
            conn.close()
            return ChatResponse(
                response=f"❌ Todo with ID {todo_id} not found.",
                action="delete"
            )
        
        # Delete the todo
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
        
        return ChatResponse(
            response=f"✅ Todo {todo_id} deleted successfully!",
            action="delete"
        )
    
    # Pattern 4: Greetings
    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if message in greetings:
        return ChatResponse(
            response="👋 Hello! I'm your Todo Assistant. I can help you manage your todos. Try:\n"
                     "• 'Add todo: buy milk'\n"
                     "• 'Show todos'\n"
                     "• 'Delete todo 1'",
            action="greeting"
        )
    
    # Pattern 5: Help request
    if "help" in message:
        return ChatResponse(
            response="🤖 I'm your Todo Assistant! Here's what I can do:\n"
                     "• 'Add todo: <task>' - Add a new todo\n"
                     "• 'Show todos' - View all your todos\n"
                     "• 'Delete todo <id>' - Delete a todo by ID\n"
                     "• Say 'Hi' for a greeting",
            action="help"
        )
    
    # Pattern 6: Unknown command - provide helpful response
    return ChatResponse(
        response="🤔 I'm not sure I understand. Try one of these commands:\n"
                 "• 'Add todo: buy milk'\n"
                 "• 'Show todos'\n"
                 "• 'Delete todo 1'\n"
                 "• Or just say 'Hi'!",
        action="unknown"
    )

# ============================================
# Run the application
# ============================================

if __name__ == "__main__":
    import uvicorn
    # Run on 0.0.0.0 to make it accessible from outside Docker container
    uvicorn.run(app, host="0.0.0.0", port=8000)
