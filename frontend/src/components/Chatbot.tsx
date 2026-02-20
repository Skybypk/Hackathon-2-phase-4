/**
 * Chatbot Component
 * ==================
 * An extraordinary AI chat interface with vibrant gradient colors,
 * smooth animations, glassmorphism effects, and modern design.
 * Positioned at bottom-right with enhanced visual appeal.
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

// Type definitions for message structure
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

// Backend API URL from environment variable
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export default function Chatbot() {
  // State management
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "👋 Hi! I'm your AI Todo Assistant.\n\nI can help you manage your tasks with simple commands!\n\n✨ Try these:\n• 'Add todo: buy milk'\n• 'Show todos'\n• 'Delete todo 1'",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Ref for auto-scrolling to bottom of chat
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  /**
   * Send message to chatbot API
   * @param message - The user's message
   */
  const sendMessage = async (message: string) => {
    try {
      setIsLoading(true);

      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from chatbot');
      }

      const data = await response.json();

      // Add bot response to messages
      const botMessage: Message = {
        id: Date.now(),
        text: data.response,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      // Handle error
      const errorMessage: Message = {
        id: Date.now(),
        text: '❌ Oops! Something went wrong.\n\nPlease make sure the backend server is running on port 8000.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle form submission
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now(),
      text: input.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    // Send to chatbot
    sendMessage(input.trim());

    // Clear input
    setInput('');
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className="chatbot-floating-btn-premium"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window-premium">
          {/* Header */}
          <div className="chat-header-premium">
            <div className="chat-header-content">
              <div className="chat-avatar">🤖</div>
              <div className="chat-title-container">
                <h3 className="chat-title">AI Assistant</h3>
                <span className="chat-status">
                  <span className="status-dot"></span>
                  {isLoading ? 'Typing...' : 'Online'}
                </span>
              </div>
            </div>
            <button
              className="chat-close-btn"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages Area */}
          <div className="chat-messages-premium">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message-premium message-${message.sender}`}
              >
                <div className="message-avatar">
                  {message.sender === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-body">
                  <div className="message-sender-name">
                    {message.sender === 'user' ? 'You' : 'AI Assistant'}
                  </div>
                  <div className="message-content-premium">
                    {message.text}
                  </div>
                  <div className="message-time">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="message-premium message-bot">
                <div className="message-avatar">🤖</div>
                <div className="message-body">
                  <div className="message-sender-name">AI Assistant</div>
                  <div className="message-content-premium loading-message">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Auto-scroll anchor */}
            <div ref={messagesEndRef} />
          </div>

          {/* Command Examples */}
          <div className="command-examples-premium">
            <span className="examples-label">⚡ Quick Commands:</span>
            <div className="examples-list">
              <button
                className="example-chip"
                onClick={() => setInput('Add todo: buy milk')}
              >
                ➕ Add todo
              </button>
              <button
                className="example-chip"
                onClick={() => setInput('Show todos')}
              >
                📋 Show todos
              </button>
              <button
                className="example-chip"
                onClick={() => setInput('Delete todo 1')}
              >
                🗑️ Delete
              </button>
            </div>
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="chat-form-premium">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="💬 Type a command..."
              className="chat-input-premium"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="btn-send-premium"
              disabled={isLoading || !input.trim()}
            >
              <span className="send-icon">🚀</span>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
