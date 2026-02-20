/**
 * TodoList Component
 * ===================
 * Displays all todos with an extraordinary, professional UI.
 * Features vibrant gradient colors, smooth animations, glassmorphism effects,
 * and horizontal layout covering 70% of screen width.
 */

'use client';

import React, { useState, useEffect } from 'react';

// Type definition for Todo item
interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

// Backend API URL from environment variable
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Vibrant color gradients for todo items
const todoGradients = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
  'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
];

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, []);

  /**
   * Fetch all todos from API
   */
  const fetchTodos = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/todos`);
      if (!response.ok) throw new Error('Failed to fetch todos');
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  /**
   * Add a new todo
   */
  const addTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim() || isLoading) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTodo.trim() }),
      });

      if (!response.ok) throw new Error('Failed to add todo');

      await fetchTodos();
      setNewTodo('');
    } catch (error) {
      console.error('Error adding todo:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Delete a todo by ID
   */
  const deleteTodo = async (id: number) => {
    try {
      const response = await fetch(`${BACKEND_URL}/todos/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete todo');

      await fetchTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  // Get gradient color based on todo ID
  const getTodoGradient = (id: number) => {
    return todoGradients[(id - 1) % todoGradients.length];
  };

  return (
    <div>
      <h2>📝 My Todo List</h2>

      {/* Enhanced Stats Bar */}
      {todos.length > 0 && (
        <div className="stats-bar-enhanced">
          <div className="stat-card stat-total">
            <div className="stat-icon">📊</div>
            <div className="stat-value">{todos.length}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
          <div className="stat-card stat-completed">
            <div className="stat-icon">✅</div>
            <div className="stat-value">{todos.filter(t => t.completed).length}</div>
            <div className="stat-label">Completed</div>
          </div>
          <div className="stat-card stat-pending">
            <div className="stat-icon">⏳</div>
            <div className="stat-value">{todos.filter(t => !t.completed).length}</div>
            <div className="stat-label">Pending</div>
          </div>
          <div className="stat-card stat-progress">
            <div className="stat-icon">📈</div>
            <div className="stat-value">
              {todos.length > 0 ? Math.round((todos.filter(t => t.completed).length / todos.length) * 100) : 0}%
            </div>
            <div className="stat-label">Progress</div>
          </div>
        </div>
      )}

      {/* Add Todo Form */}
      <form onSubmit={addTodo} className="todo-form">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="✨ What amazing task will you accomplish today?"
          className="todo-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary btn-add"
          disabled={isLoading || !newTodo.trim()}
        >
          <span>🚀</span> Add Task
        </button>
      </form>

      {/* Todo List Display */}
      {todos.length === 0 ? (
        <div className="empty-state-premium">
          <div className="empty-state-icon">📋</div>
          <h3 className="empty-state-title">No tasks yet!</h3>
          <p className="empty-state-description">
            Start by adding your first task above or use the AI chatbot assistant
          </p>
          <div className="empty-state-suggestions">
            <span className="suggestion-badge">💼 Work tasks</span>
            <span className="suggestion-badge">🏠 Personal goals</span>
            <span className="suggestion-badge">📚 Learning objectives</span>
          </div>
        </div>
      ) : (
        <ul className="todo-list-horizontal">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className="todo-card-horizontal"
              style={{
                background: getTodoGradient(todo.id),
                opacity: todo.completed ? 0.7 : 1,
                transform: todo.completed ? 'scale(0.98)' : 'scale(1)',
              }}
            >
              <div className="todo-card-content">
                <div className="todo-card-id">#{todo.id}</div>
                <div className="todo-card-text">
                  <span className={`todo-title ${todo.completed ? 'completed' : ''}`}>
                    {todo.completed && '✅ '}
                    {todo.title}
                  </span>
                </div>
              </div>
              <div className="todo-card-actions">
                <button
                  onClick={() => deleteTodo(todo.id)}
                  className="btn-delete-card"
                  title="Delete this task"
                >
                  🗑️
                </button>
              </div>
              <div className="todo-card-glow"></div>
            </li>
          ))}
        </ul>
      )}

      {/* Quick Tips */}
      <div className="tip-box-premium">
        <div className="tip-icon">💡</div>
        <div className="tip-content">
          <p className="tip-title">Pro Tip</p>
          <p className="tip-description">
            Use the AI chatbot assistant to manage your todos with natural language commands!
          </p>
          <div className="tip-examples">
            <code>"Add todo: buy groceries"</code>
            <code>"Show todos"</code>
            <code>"Delete todo 1"</code>
          </div>
        </div>
      </div>

      {/* Inline Styles for Enhanced Components */}
      <style dangerouslySetInnerHTML={{ __html: `
        /* Enhanced Stats Bar */
        .stats-bar-enhanced {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          margin-bottom: 24px;
          padding: 8px;
        }

        .stat-card {
          padding: 20px 16px;
          border-radius: 16px;
          text-align: center;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
          backdrop-filter: blur(10px);
        }

        .stat-card::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
          opacity: 0;
          transition: opacity 0.3s ease;
        }

        .stat-card:hover::before {
          opacity: 1;
        }

        .stat-card:hover {
          transform: translateY(-8px);
        }

        .stat-total {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        }

        .stat-completed {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
        }

        .stat-pending {
          background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
          box-shadow: 0 8px 32px rgba(249, 115, 22, 0.4);
        }

        .stat-progress {
          background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
          box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        }

        .stat-icon {
          font-size: 28px;
          margin-bottom: 8px;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }

        .stat-value {
          font-size: 36px;
          font-weight: 800;
          color: white;
          text-shadow: 0 2px 8px rgba(0,0,0,0.2);
          margin-bottom: 4px;
        }

        .stat-label {
          font-size: 11px;
          color: rgba(255, 255, 255, 0.9);
          text-transform: uppercase;
          letter-spacing: 1.2px;
          font-weight: 600;
        }

        /* Enhanced Todo Form */
        .todo-form {
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
          padding: 28px;
          border-radius: 20px;
          border: 2px solid rgba(102, 126, 234, 0.3);
          box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
          margin-bottom: 32px;
        }

        .todo-input {
          padding: 20px 28px;
          border: 2px solid rgba(102, 126, 234, 0.4);
          border-radius: 16px;
          font-size: 16px;
          background: rgba(255, 255, 255, 0.95);
          color: #1e293b;
          font-weight: 600;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .todo-input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.2);
          transform: scale(1.02);
          background: white;
        }

        .btn-add {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
          padding: 20px 36px;
          font-size: 16px;
          box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
        }

        .btn-add:hover {
          box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
          transform: translateY(-6px);
        }

        /* Empty State Premium */
        .empty-state-premium {
          text-align: center;
          padding: 80px 40px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
          border-radius: 24px;
          border: 3px dashed rgba(102, 126, 234, 0.4);
          position: relative;
          overflow: hidden;
        }

        .empty-state-premium::before {
          content: "";
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
          animation: pulse 4s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 0.5; }
          50% { transform: scale(1.1); opacity: 0.8; }
        }

        .empty-state-icon {
          font-size: 80px;
          margin-bottom: 24px;
          position: relative;
          z-index: 1;
          animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-15px); }
        }

        .empty-state-title {
          font-size: 28px;
          font-weight: 700;
          color: #f8fafc;
          margin-bottom: 12px;
          position: relative;
          z-index: 1;
        }

        .empty-state-description {
          color: #94a3b8;
          font-size: 16px;
          margin-bottom: 24px;
          position: relative;
          z-index: 1;
        }

        .empty-state-suggestions {
          display: flex;
          gap: 12px;
          justify-content: center;
          flex-wrap: wrap;
          position: relative;
          z-index: 1;
        }

        .suggestion-badge {
          background: rgba(102, 126, 234, 0.2);
          padding: 10px 20px;
          border-radius: 20px;
          font-size: 14px;
          color: #cbd5e1;
          border: 1px solid rgba(102, 126, 234, 0.3);
          transition: all 0.3s ease;
        }

        .suggestion-badge:hover {
          background: rgba(102, 126, 234, 0.3);
          transform: scale(1.05);
        }

        /* Horizontal Todo List */
        .todo-list-horizontal {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
          padding: 8px;
          list-style: none;
          max-height: none;
          overflow: visible;
        }

        .todo-card-horizontal {
          flex: 1 1 calc(33.333% - 20px);
          min-width: 280px;
          max-width: 450px;
          padding: 24px 28px;
          border-radius: 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        }

        .todo-card-horizontal::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.05) 100%);
          opacity: 0;
          transition: opacity 0.4s ease;
        }

        .todo-card-horizontal:hover::before {
          opacity: 1;
        }

        .todo-card-horizontal:hover {
          transform: translateY(-10px) scale(1.03);
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }

        .todo-card-content {
          display: flex;
          align-items: center;
          gap: 16px;
          flex: 1;
          position: relative;
          z-index: 1;
        }

        .todo-card-id {
          background: rgba(255, 255, 255, 0.25);
          padding: 8px 14px;
          border-radius: 12px;
          font-size: 14px;
          font-weight: 700;
          color: white;
          backdrop-filter: blur(10px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .todo-card-text {
          flex: 1;
        }

        .todo-title {
          font-size: 18px;
          font-weight: 600;
          color: white;
          text-shadow: 0 2px 8px rgba(0,0,0,0.2);
          transition: all 0.3s ease;
        }

        .todo-title.completed {
          text-decoration: line-through;
          opacity: 0.7;
        }

        .todo-card-actions {
          position: relative;
          z-index: 1;
        }

        .btn-delete-card {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          padding: 12px 16px;
          border-radius: 12px;
          font-size: 20px;
          cursor: pointer;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .btn-delete-card:hover {
          background: rgba(239, 68, 68, 0.8);
          transform: scale(1.15) rotate(10deg);
          box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
        }

        .todo-card-glow {
          position: absolute;
          bottom: -50%;
          right: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
          opacity: 0;
          transition: opacity 0.4s ease;
        }

        .todo-card-horizontal:hover .todo-card-glow {
          opacity: 1;
        }

        /* Tip Box Premium */
        .tip-box-premium {
          margin-top: 32px;
          padding: 24px 28px;
          background: linear-gradient(135deg, rgba(6, 214, 255, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
          border-radius: 20px;
          border: 2px solid rgba(6, 214, 255, 0.3);
          display: flex;
          gap: 20px;
          align-items: flex-start;
          box-shadow: 0 8px 32px rgba(6, 214, 255, 0.2);
        }

        .tip-icon {
          font-size: 32px;
          flex-shrink: 0;
          animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
          0%, 100% { filter: drop-shadow(0 0 8px rgba(6, 214, 255, 0.5)); }
          50% { filter: drop-shadow(0 0 20px rgba(6, 214, 255, 0.8)); }
        }

        .tip-content {
          flex: 1;
        }

        .tip-title {
          font-size: 16px;
          font-weight: 700;
          color: #00d9ff;
          margin-bottom: 8px;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .tip-description {
          font-size: 14px;
          color: #cbd5e1;
          margin-bottom: 12px;
          line-height: 1.6;
        }

        .tip-examples {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
        }

        .tip-examples code {
          background: rgba(6, 214, 255, 0.2);
          padding: 8px 14px;
          border-radius: 8px;
          color: #00d9ff;
          font-family: "Consolas", monospace;
          font-size: 13px;
          border: 1px solid rgba(6, 214, 255, 0.3);
          transition: all 0.3s ease;
        }

        .tip-examples code:hover {
          background: rgba(6, 214, 255, 0.3);
          transform: scale(1.05);
        }

        /* Responsive */
        @media (max-width: 1024px) {
          .stats-bar-enhanced {
            grid-template-columns: repeat(2, 1fr);
          }

          .todo-card-horizontal {
            flex: 1 1 calc(50% - 20px);
          }
        }

        @media (max-width: 640px) {
          .stats-bar-enhanced {
            grid-template-columns: 1fr;
          }

          .todo-card-horizontal {
            flex: 1 1 100%;
          }

          .tip-box-premium {
            flex-direction: column;
          }
        }
      `}} />
    </div>
  );
}
