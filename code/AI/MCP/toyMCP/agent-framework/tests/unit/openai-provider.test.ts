import { jest, describe, it, expect, beforeEach } from '@jest/globals';
import { OpenAIProvider } from '../../src/openai-provider';

// Mock the OpenAI module
jest.mock('openai', () => {
  // Create a mock constructor that matches the OpenAI class structure
  const mockCreate = jest.fn();
  
  return {
    default: jest.fn().mockImplementation(() => ({
      chat: {
        completions: {
          create: mockCreate
        }
      }
    }))
  };
});

// Import the mocked module
import OpenAI from 'openai';

describe('OpenAIProvider', () => {
  let provider: OpenAIProvider;
  let mockCreateMethod: jest.Mock;
  
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Create an instance of the provider
    provider = new OpenAIProvider('test-api-key', 'gpt-4', true);
    
    // Get a reference to the mocked create method
    // TypeScript won't complain with this approach
    const mockInstance = (OpenAI as jest.MockedFunction<any>).mock.results[0].value;
    mockCreateMethod = mockInstance.chat.completions.create;
  });
  
  describe('complete', () => {
    it('should construct OpenAI client with correct API key', () => {
      expect(OpenAI).toHaveBeenCalledWith({
        apiKey: 'test-api-key'
      });
    });
    
    it('should call OpenAI API with correct parameters', async () => {
      // Setup mock response with type that works
      mockCreateMethod.mockResolvedValueOnce({
        choices: [
          {
            message: {
              content: '{"action": "add", "text": "Buy milk"}'
            }
          }
        ]
      });
      
      await provider.complete('Test prompt');
      
      expect(mockCreateMethod).toHaveBeenCalledWith({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are a helpful agent that manages a todo list.' },
          { role: 'user', content: 'Test prompt' }
        ],
        temperature: 0.2
      });
    });
    
    it('should return the message content from API response', async () => {
      // Setup mock response
      mockCreateMethod.mockResolvedValueOnce({
        choices: [
          {
            message: {
              content: '{"action": "add", "text": "Buy milk"}'
            }
          }
        ]
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('{"action": "add", "text": "Buy milk"}');
    });
    
    it('should handle empty response content gracefully', async () => {
      // Setup mock response with null content
      mockCreateMethod.mockResolvedValueOnce({
        choices: [
          {
            message: {
              content: null
            }
          }
        ]
      });
      
      const result = await provider.complete('Test prompt');
      
      expect(result).toBe('');
    });
    
    it('should handle API errors gracefully', async () => {
      // Setup mock API error
      mockCreateMethod.mockRejectedValueOnce(new Error('API rate limit exceeded'));
      
      await expect(provider.complete('Test prompt'))
        .rejects.toThrow('Failed to get completion: API rate limit exceeded');
    });
  });
}); 