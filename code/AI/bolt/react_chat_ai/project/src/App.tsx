import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2, Settings } from 'lucide-react';
import { ChatMessage } from './components/ChatMessage';
import { FileUpload } from './components/FileUpload';
import { SettingsModal } from './components/SettingsModal';
import { Message, LLMProvider, AttachedDocument, APISettings } from './types';
import { sendMessage } from './services/llm';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [provider, setProvider] = useState<LLMProvider>('openai');
  const [attachedDocs, setAttachedDocs] = useState<AttachedDocument[]>([]);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [apiSettings, setApiSettings] = useState<APISettings>(() => {
    const saved = localStorage.getItem('apiSettings');
    return saved ? JSON.parse(saved) : {
      openai: '',
      anthropic: '',
      gemini: '',
      ollamaUrl: 'http://localhost:11434',
      ollamaModel: ''
    };
  });
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (file: File) => {
    const text = await file.text();
    setAttachedDocs(prev => [...prev, { name: file.name, content: text }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setError(null);
    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage(input, provider, apiSettings, attachedDocs);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
    } catch (error) {
      console.error('Error:', error);
      setError(error instanceof Error ? error.message : 'An error occurred');
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '❌ Error: ' + (error instanceof Error ? error.message : 'Failed to get response')
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveSettings = (settings: APISettings) => {
    setApiSettings(settings);
    localStorage.setItem('apiSettings', JSON.stringify(settings));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gray-800 p-4 flex items-center gap-2">
            <Bot className="w-6 h-6 text-white" />
            <h1 className="text-xl font-semibold text-white">AI Chat Assistant</h1>
            <div className="ml-auto flex items-center gap-2">
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value as LLMProvider)}
                className="bg-gray-700 text-white rounded px-3 py-1"
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="gemini">Gemini</option>
                <option value="ollama">Ollama</option>
              </select>
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="p-2 text-white hover:bg-gray-700 rounded-lg"
                title="API Settings"
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="h-[500px] overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
            {isLoading && (
              <div className="flex items-center gap-2 text-gray-500">
                <Loader2 className="w-5 h-5 animate-spin" />
                Thinking...
              </div>
            )}
            {error && (
              <div className="text-red-500 text-sm p-2 bg-red-50 rounded">
                {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* File Upload */}
          <div className="p-4 border-t">
            <FileUpload onFileUpload={handleFileUpload} />
            {attachedDocs.length > 0 && (
              <div className="mt-2">
                <p className="text-sm text-gray-600">
                  Attached documents: {attachedDocs.map(doc => doc.name).join(', ')}
                </p>
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </div>
          </form>
        </div>
      </div>

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        settings={apiSettings}
        onSave={handleSaveSettings}
      />
    </div>
  );
}

export default App;