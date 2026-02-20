# Chatbot Debug Guide

## Overview

This guide provides comprehensive debugging strategies for the Todo Chatbot application.

## Common Issues

### 1. Chatbot Not Responding

**Symptoms**: Chat interface shows loading state indefinitely

**Debug Steps**:
1. Check backend server is running on port 8000
2. Verify CORS is enabled in `backend/main.py`
3. Check browser console for network errors
4. Test API directly: `curl http://localhost:8000/`

**Solution**:
```bash
# Check backend status
curl http://localhost:8000/

# Check CORS headers
curl -I http://localhost:8000/chat
```

### 2. Messages Not Persisting

**Symptoms**: Chat history resets on page refresh

**Debug Steps**:
1. Check if messages are stored in component state only
2. Verify database connection in `main.py`
3. Check SQLite file permissions

**Solution**:
```python
# In main.py, verify database initialization
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (...)
    """)
    conn.commit()
    conn.close()
```

### 3. Pattern Matching Issues

**Symptoms**: Chatbot doesn't recognize commands

**Debug Steps**:
1. Check regex patterns in `chat()` endpoint
2. Verify message is being lowercased
3. Test patterns individually

**Solution**:
```python
import re

# Test pattern matching
message = "Add todo: buy milk"
add_pattern = r"add todo[:\s]+(.+)"
match = re.match(add_pattern, message.lower())
print(match.group(1) if match else "No match")
```

### 4. Database Lock Errors

**Symptoms**: `sqlite3.OperationalError: database is locked`

**Debug Steps**:
1. Check for unclosed connections
2. Verify connection pooling
3. Check for concurrent writes

**Solution**:
```python
def get_db_connection():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    return conn
```

## Debug Tools

### 1. Logging

Add logging to backend:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/chat")
def chat(chat_request: ChatRequest):
    logger.debug(f"Received message: {chat_request.message}")
    # ... rest of code
```

### 2. Request/Response Inspection

```python
@app.post("/chat")
def chat(chat_request: ChatRequest):
    logger.debug(f"Request: {chat_request.dict()}")
    result = process_message(chat_request.message)
    logger.debug(f"Response: {result}")
    return result
```

### 3. Database Inspection

```bash
# Open SQLite database
sqlite3 todos.db

# Check tables
.tables

# View todos
SELECT * FROM todos;
```

## Testing Commands

### Test All Chatbot Commands

```bash
# Add todo
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add todo: test item"}'

# Show todos
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show todos"}'

# Delete todo
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Delete todo 1"}'

# Greeting
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Frontend Debug

### 1. Check Network Requests

Open DevTools → Network tab → Filter by "chat"

### 2. Check Console Errors

Open DevTools → Console → Look for errors

### 3. Check State

In React DevTools, inspect Chatbot component state

## Performance Debug

### 1. Slow Responses

- Check database query performance
- Verify network latency
- Check server resources

### 2. Memory Leaks

- Check for unclosed connections
- Monitor component unmounting
- Use browser memory profiler

## Error Codes Reference

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Endpoint not found | Check URL path |
| 500 | Server error | Check backend logs |
| CORS | Origin blocked | Enable CORS in backend |
| Timeout | Request timeout | Increase timeout or optimize |

## Contact

For issues, check:
- Backend logs
- Frontend console
- Network tab in DevTools
