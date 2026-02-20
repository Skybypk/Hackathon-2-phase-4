# Qwen Code Configuration

## Project Overview

This is **Phase 4** of the Q4 Hackathon - Todo App with AI Chatbot.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14 (React 18, TypeScript)
- **Database**: SQLite (in-memory/file-based)
- **Deployment**: Docker, Kubernetes (Helm)

## Project Structure

```
h-2-phase-4/
├── backend/           # FastAPI backend with chatbot
├── frontend/          # Next.js frontend
├── helm/              # Kubernetes Helm charts
├── .specify/          # Specifications
├── docer/             # Docker configurations
├── history/           # Development history
├── specs/             # Technical specifications
└── .qwen/             # Qwen configuration
```

## Development Commands

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Chatbot Commands

The chatbot supports natural language commands:

| Command | Example |
|---------|---------|
| Add todo | `Add todo: buy milk` |
| Show todos | `Show todos` |
| Delete todo | `Delete todo 1` |
| Greeting | `Hi`, `Hello`, `Hey` |
| Help | `Help` |

## API Endpoints

- `GET /` - Health check
- `POST /todos` - Create todo
- `GET /todos` - List todos
- `DELETE /todos/{id}` - Delete todo
- `POST /chat` - Chat with bot

## Docker

```bash
# Build backend
docker build -t todo-chatbot-backend:latest ./backend

# Build frontend
docker build -t todo-chatbot-frontend:latest ./frontend
```

## Kubernetes

```bash
# Install with Helm
helm install todo-chatbot ./helm/todo-chatbot

# Uninstall
helm uninstall todo-chatbot
```

## Environment Variables

### Backend
- `DATABASE_URL`: SQLite connection string
- `API_PREFIX`: API route prefix
- `CORS_ORIGINS`: Allowed origins

### Frontend
- `BACKEND_URL`: Backend API URL

## Version

- **Phase**: 4
- **App Version**: 1.0.0
- **Last Updated**: 2026-02-18
