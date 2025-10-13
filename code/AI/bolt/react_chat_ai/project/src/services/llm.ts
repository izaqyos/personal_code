import { APISettings, LLMProvider, AttachedDocument, OllamaModel } from '../types';
import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { GoogleGenerativeAI } from '@google/generative-ai';

export async function sendMessage(
  message: string,
  provider: LLMProvider,
  apiSettings: APISettings,
  attachedDocs: AttachedDocument[]
): Promise<string> {
  const context = attachedDocs.length > 0
    ? `\nContext from attached documents:\n${attachedDocs.map(doc => `${doc.name}:\n${doc.content}`).join('\n\n')}`
    : '';

  const prompt = context ? `${context}\n\nUser message: ${message}` : message;

  switch (provider) {
    case 'openai':
      return callOpenAI(prompt, apiSettings.openai);
    case 'anthropic':
      return callAnthropic(prompt, apiSettings.anthropic);
    case 'gemini':
      return callGemini(prompt, apiSettings.gemini);
    case 'ollama':
      return callOllama(prompt, apiSettings.ollamaUrl, apiSettings.ollamaModel);
    default:
      throw new Error(`Unsupported provider: ${provider}`);
  }
}

async function callOpenAI(prompt: string, apiKey: string): Promise<string> {
  if (!apiKey) throw new Error('OpenAI API key not configured');

  const openai = new OpenAI({ apiKey });
  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
  });

  return response.choices[0]?.message?.content || 'No response generated';
}

async function callAnthropic(prompt: string, apiKey: string): Promise<string> {
  if (!apiKey) throw new Error('Anthropic API key not configured');

  const anthropic = new Anthropic({ apiKey });
  const response = await anthropic.messages.create({
    model: 'claude-3-opus-20240229',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
  });

  return response.content[0].text;
}

async function callGemini(prompt: string, apiKey: string): Promise<string> {
  if (!apiKey) throw new Error('Gemini API key not configured');

  const genAI = new GoogleGenerativeAI(apiKey);
  const model = genAI.getGenerativeModel({ model: 'gemini-pro' });
  const result = await model.generateContent(prompt);
  const response = await result.response;
  return response.text();
}

async function callOllama(prompt: string, url: string, model: string): Promise<string> {
  if (!url) throw new Error('Ollama URL not configured');
  if (!model) throw new Error('Ollama model not selected');

  const response = await fetch(`${url}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ],
      stream: false,
    }),
  });

  if (!response.ok) {
    throw new Error(`Ollama API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.message.content;
}

export async function fetchOllamaModels(url: string): Promise<OllamaModel[]> {
  if (!url) throw new Error('Ollama URL not configured');

  const response = await fetch(`${url}/api/tags`);
  if (!response.ok) {
    throw new Error(`Failed to fetch Ollama models: ${response.statusText}`);
  }

  const data = await response.json();
  return data.models;
}