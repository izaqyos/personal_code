import { jest, describe, it, expect, beforeEach } from '@jest/globals';
import axios from 'axios';
import { OllamaProvider } from '../../src/ollama-provider';

// Mock axios
jest.mock('axios');
const mockAxios = axios as jest.Mocked<typeof axios>;

describe('OllamaProvider', () => {
  let provider: OllamaProvider;
  
  beforeEach(() => {
    jest.clearAllMocks();
    provider = new OllamaProvider('test-model', 'http://test-ollama:11434', true);
  });
  
  describe('complete', () => {
    it('should send correct parameters to Ollama API', async () => {
      // Mock successful response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          response: '{"action": "add", "text": "Buy milk"}'
        }
      });
      
      await provider.complete('Test prompt');
      
      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://test-ollama:11434/api/generate',
        {
          model: 'test-model',
          prompt: 'Test prompt',
          stream: false
        }
      );
    });
    
    it('should return the raw response from Ollama', async () => {
      // Mock response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          response: '{"action": "add", "text": "Buy milk"}'
        }
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('{"action": "add", "text": "Buy milk"}');
    });
    
    it('should extract valid JSON from response with thinking tags', async () => {
      // Mock response with thinking tags
      mockAxios.post.mockResolvedValueOnce({
        data: {
          response: `<think>
          Let me analyze what to do here...
          I think I need to add a task
          </think>
          {"action": "add", "text": "Buy milk"}`
        }
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('{"action": "add", "text": "Buy milk"}');
    });
    
    it('should extract JSON from response with comments', async () => {
      // Mock response with comments
      mockAxios.post.mockResolvedValueOnce({
        data: {
          response: `// First let me think about this
          /* 
           * This is a multi-line comment
           * explaining my reasoning
           */
          {"action": "add", "text": "Buy milk"}`
        }
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('{"action": "add", "text": "Buy milk"}');
    });
    
    it('should extract valid JSON object when surrounded by text', async () => {
      // Mock response with JSON surrounded by text
      mockAxios.post.mockResolvedValueOnce({
        data: {
          response: `I think we should add a new task to the list.
          {"action": "add", "text": "Buy milk"}
          This will ensure we don't forget to buy milk.`
        }
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('{"action": "add", "text": "Buy milk"}');
    });
    
    it('should handle API errors gracefully', async () => {
      // Mock API error
      mockAxios.post.mockRejectedValueOnce(new Error('API connection failed'));
      
      await expect(provider.complete('Test prompt'))
        .rejects.toThrow('Failed to get completion: API connection failed');
    });
  });
}); 