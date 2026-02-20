/**
 * Main Page Component
 * ====================
 * The home page of the Todo App with Chatbot.
 * Displays Todo List covering 70% of screen horizontally.
 * Chatbot appears as a floating widget at bottom-right.
 */

import TodoList from '@/components/TodoList';
import Chatbot from '@/components/Chatbot';
import './globals.css';

export default function Home() {
  return (
    <main>
      {/* Header Banner */}
      <div className="header-banner">
        <h1>✨ Todo App with AI Chatbot</h1>
        <p>Manage your tasks with natural language commands</p>
      </div>

      <div className="container">
        {/* Main Panel: Todo List (70% width) */}
        <div className="todo-section">
          <div className="card todo-card">
            <TodoList />
          </div>
        </div>
      </div>

      {/* Floating Chatbot at Bottom Right */}
      <Chatbot />
    </main>
  );
}
