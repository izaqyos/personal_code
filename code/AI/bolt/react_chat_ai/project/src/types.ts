export type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export type LLMProvider = 'anthropic' | 'openai' | 'gemini' | 'ollama';

export type AttachedDocument = {
  name: string;
  content: string;
};

export type APISettings = {
  openai: string;
  anthropic: string;
  gemini: string;
  ollamaUrl: string;
  ollamaModel: string;
};

export type OllamaModel = {
  name: string;
  modified_at: string;
  size: number;
};