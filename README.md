# Todo App with AI Chatbot 🤖

A modern Todo application with an integrated AI chatbot that understands natural language commands. Built with **FastAPI** (backend), **Next.js** (frontend), and deployable with **Docker** and **Kubernetes**.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Chatbot Commands](#chatbot-commands)
- [API Documentation](#api-documentation)
- [Docker Setup](#docker-setup)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Environment Variables](#environment-variables)
- [Development](#development)

---

## ✨ Features

### Todo Management
- ✅ Create, read, and delete todos
- ✅ In-memory SQLite database
- ✅ Clean, modern UI

### AI Chatbot
- 🤖 Natural language command processing
- 🤖 Understands context-aware commands
- 🤖 Friendly responses and error handling
- 🤖 Real-time conversation interface

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js       │         │   FastAPI       │
│   Frontend      │ ──────► │   Backend       │
│   (Port 3000)   │         │   (Port 8000)   │
│                 │         │                 │
│  - Chatbot UI   │         │  - /todos API   │
│  - Todo List    │         │  - /chat API    │
└─────────────────┘         └────────┬────────┘
                                     │
                                     ▼
                              ┌───────────────┐
                              │   SQLite DB   │
                              │  (In-memory)  │
                              └───────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker (optional, for containerized deployment)
- Helm (optional, for Kubernetes deployment)

### 1. Start the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python main.py
# Or using uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 2. Start the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## 💬 Chatbot Commands

The chatbot understands natural language commands. Here are the supported commands:

### 1. Add Todo

**Command:** `Add todo: <task>`

**Examples:**
```
Add todo: buy milk
Add todo: finish the report
Add todo: call John at 5 PM
```

**Response:**
```
✅ Todo added successfully! (ID: 1): buy milk
```

### 2. Show Todos

**Command:** `Show todos`

**Alternative commands:**
- `List todos`
- `Get todos`
- `My todos`

**Response:**
```
📋 Your todos:
  1. buy milk
  2. finish the report ✓
  3. call John at 5 PM
```

### 3. Delete Todo

**Command:** `Delete todo <id>`

**Examples:**
```
Delete todo 1
Delete todo: 2
```

**Response:**
```
✅ Todo 1 deleted successfully!
```

### 4. Greetings

**Commands:**
- `Hi`
- `Hello`
- `Hey`
- `Good morning`
- `Good afternoon`
- `Good evening`

**Response:**
```
👋 Hello! I'm your Todo Assistant. I can help you manage your todos. Try:
• 'Add todo: buy milk'
• 'Show todos'
• 'Delete todo 1'
```

### 5. Help

**Command:** `Help`

**Response:**
```
🤖 I'm your Todo Assistant! Here's what I can do:
• 'Add todo: <task>' - Add a new todo
• 'Show todos' - View all your todos
• 'Delete todo <id>' - Delete a todo by ID
• Say 'Hi' for a greeting
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Todo API with Chatbot is running!",
  "version": "1.0.0"
}
```

#### 2. Create Todo
```http
POST /todos
Content-Type: application/json

{
  "title": "buy milk"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "buy milk",
  "completed": false
}
```

#### 3. Get All Todos
```http
GET /todos
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "buy milk",
    "completed": false
  },
  {
    "id": 2,
    "title": "finish report",
    "completed": true
  }
]
```

#### 4. Delete Todo
```http
DELETE /todos/{id}
```

**Response:**
```json
{
  "message": "Todo 1 deleted successfully"
}
```

#### 5. Chat with Bot 🤖
```http
POST /chat
Content-Type: application/json

{
  "message": "Add todo: buy milk"
}
```

**Response:**
```json
{
  "response": "✅ Todo added successfully! (ID: 1): buy milk",
  "action": "add"
}
```

---

## 🐳 Docker Setup

### Build Docker Images

#### Backend
```bash
cd backend
docker build -t todo-chatbot-backend:latest .
```

#### Frontend
```bash
cd frontend
docker build -t todo-chatbot-frontend:latest .
```

### Run with Docker

#### Start Backend Container
```bash
docker run -d \
  --name todo-backend \
  -p 8000:8000 \
  -v todo-data:/app \
  todo-chatbot-backend:latest
```

#### Start Frontend Container
```bash
docker run -d \
  --name todo-frontend \
  --link todo-backend:backend \
  -p 3000:3000 \
  -e BACKEND_URL=http://backend:8000 \
  todo-chatbot-frontend:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - todo-data:/app
    environment:
      - DATABASE_URL=sqlite:///todos.db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend

volumes:
  todo-data:
```

Run with:
```bash
docker-compose up -d
```

---

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- Helm 3+

### Install with Helm

#### 1. Add Helm Repository (if applicable)
```bash
# Skip for local development
```

#### 2. Configure Values (Optional)
Edit `helm/todo-chatbot/values.yaml` to customize:
- Resource limits
- Environment variables
- Ingress settings
- Persistence options

#### 3. Install the Chart
```bash
cd helm

# Install with default values
helm install todo-chatbot ./todo-chatbot

# Install with custom values
helm install todo-chatbot ./todo-chatbot -f custom-values.yaml

# Install in a specific namespace
helm install todo-chatbot ./todo-chatbot -n todo-app
```

#### 4. Verify Installation
```bash
# Check pods
kubectl get pods -l app.kubernetes.io/name=todo-chatbot

# Check services
kubectl get svc -l app.kubernetes.io/name=todo-chatbot

# View logs
kubectl logs -l app.kubernetes.io/component=backend
kubectl logs -l app.kubernetes.io/component=frontend
```

#### 5. Access the Application

**Option 1: Port Forward**
```bash
# Forward frontend port
kubectl port-forward svc/todo-chatbot-frontend 3000:3000

# Forward backend port
kubectl port-forward svc/todo-chatbot-backend 8000:8000
```

**Option 2: Ingress**
Enable ingress in `values.yaml`:
```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: todo-chatbot.local
      paths:
        - path: /
          pathType: Prefix
```

Then access at: `http://todo-chatbot.local`

#### 6. Uninstall
```bash
helm uninstall todo-chatbot
```

---

## 🔧 Environment Variables

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///todos.db` | Database connection string |
| `API_PREFIX` | `/api` | API route prefix |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://localhost:8000` | Backend API URL |

---

## 👨‍💻 Development

### Backend Development

```bash
cd backend

# Install with dev dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API docs
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

---

## 📁 Project Structure

```
h-2-phase-4/
├── backend/
│   ├── main.py              # FastAPI application with chatbot
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend Docker configuration
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Main page component
│   │   │   ├── layout.tsx   # Root layout
│   │   │   └── globals.css  # Global styles
│   │   └── components/
│   │       ├── Chatbot.tsx  # Chatbot component
│   │       └── TodoList.tsx # Todo list component
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── Dockerfile           # Frontend Docker configuration
│
└── helm/
    └── todo-chatbot/
        ├── Chart.yaml       # Helm chart metadata
        ├── values.yaml      # Default configuration values
        └── templates/
            ├── backend.yaml     # Backend deployment & service
            ├── frontend.yaml    # Frontend deployment & service
            ├── pvc.yaml         # Persistent volume claim
            ├── ingress.yaml     # Ingress configuration
            └── _helpers.tpl     # Template helper functions
```

---

## 🎯 Chatbot Usage Examples

### Example 1: Complete Workflow

```
User: Hi
Bot: 👋 Hello! I'm your Todo Assistant...

User: Add todo: buy groceries
Bot: ✅ Todo added successfully! (ID: 1): buy groceries

User: Add todo: walk the dog
Bot: ✅ Todo added successfully! (ID: 2): walk the dog

User: Show todos
Bot: 📋 Your todos:
       1. buy groceries
       2. walk the dog

User: Delete todo 1
Bot: ✅ Todo 1 deleted successfully!

User: Show todos
Bot: 📋 Your todos:
       2. walk the dog
```

### Example 2: Error Handling

```
User: Delete todo 999
Bot: ❌ Todo with ID 999 not found.

User: Add todo:
Bot: 🤔 I'm not sure I understand. Try one of these commands...
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **Next.js** - React framework for production
- **SQLite** - Lightweight database
- **Kubernetes** - Container orchestration
- **Helm** - Kubernetes package manager

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the chatbot examples above

---

**Happy Todo Managing! 🎉**
