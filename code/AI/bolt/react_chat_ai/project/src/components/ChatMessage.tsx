import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  return (
    <div className={`flex gap-3 ${message.role === 'assistant' ? 'bg-gray-50' : ''} p-4 rounded-lg`}>
      <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-200">
        {message.role === 'assistant' ? (
          <Bot className="w-5 h-5 text-gray-700" />
        ) : (
          <User className="w-5 h-5 text-gray-700" />
        )}
      </div>
      <div className="flex-1">
        <ReactMarkdown className="prose max-w-none">
          {message.content}
        </ReactMarkdown>
      </div>
    </div>
  );
};