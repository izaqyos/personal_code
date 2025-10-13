import { jest, describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import axios from 'axios';
import { MCPAgent, LLMProvider } from '../../src/agent';

// Mock axios
jest.mock('axios');
const mockAxios = axios as jest.Mocked<typeof axios>;

// Create a mock LLM provider
class MockLLMProvider implements LLMProvider {
  public promptsReceived: string[] = [];
  public responsesToReturn: string[] = [];
  
  constructor(responses: string[] = []) {
    this.responsesToReturn = responses;
  }
  
  async complete(prompt: string): Promise<string> {
    this.promptsReceived.push(prompt);
    // Return the next response or empty string
    return this.responsesToReturn.shift() || '{}';
  }
}

describe('MCPAgent', () => {
  let agent: MCPAgent;
  let mockLLM: MockLLMProvider;
  
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    
    // Create mock LLM provider with predefined responses
    mockLLM = new MockLLMProvider();
    
    // Create agent instance
    agent = new MCPAgent('http://localhost:3000', mockLLM, true);
  });
  
  describe('authenticate', () => {
    it('should authenticate successfully and store token', async () => {
      // Mock successful authentication response
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      
      const result = await agent.authenticate('testuser', 'password');
      
      expect(result).toBe(true);
      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://localhost:3000/auth/login',
        { username: 'testuser', password: 'password' }
      );
    });
    
    it('should handle authentication failure', async () => {
      // Mock failed authentication
      mockAxios.post.mockRejectedValueOnce(new Error('Authentication failed'));
      
      const result = await agent.authenticate('baduser', 'wrongpassword');
      
      expect(result).toBe(false);
      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://localhost:3000/auth/login',
        { username: 'baduser', password: 'wrongpassword' }
      );
    });
  });
  
  describe('executeRPC', () => {
    it('should throw error if not authenticated', async () => {
      await expect(agent.executeRPC('todo.list')).rejects.toThrow('Not authenticated');
    });
    
    it('should execute RPC call with correct parameters', async () => {
      // First authenticate
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      await agent.authenticate('testuser', 'password');
      
      // Then mock RPC response
      mockAxios.post.mockResolvedValueOnce({ 
        data: { 
          jsonrpc: '2.0',
          id: 'test-id',
          result: { success: true } 
        } 
      });
      
      const result = await agent.executeRPC('todo.add', { text: 'Buy milk' });
      
      expect(result).toEqual({
        jsonrpc: '2.0',
        id: 'test-id',
        result: { success: true }
      });
      
      // Check second axios call (first was authentication)
      expect(mockAxios.post).toHaveBeenCalledTimes(2);
      
      // Verify the second call has correct parameters
      const secondCallArgs = mockAxios.post.mock.calls[1];
      // Type assertion for the mock call arguments
      const [url, data, config] = secondCallArgs as [string, any, any];
      expect(url).toBe('http://localhost:3000/rpc');
      expect(data.method).toBe('todo.add');
      expect(data.params).toEqual({ text: 'Buy milk' });
      expect(data.jsonrpc).toBe('2.0');
      expect(config?.headers?.Authorization).toBe('Bearer test-token-123');
    });
    
    it('should handle RPC call errors', async () => {
      // Authenticate
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      await agent.authenticate('testuser', 'password');
      
      // Mock RPC error
      mockAxios.post.mockRejectedValueOnce(new Error('RPC error'));
      
      await expect(agent.executeRPC('todo.add', { text: 'Buy milk' }))
        .rejects.toThrow('RPC error');
    });
  });
  
  describe('listTasks', () => {
    beforeEach(async () => {
      // Authenticate for all tests in this describe block
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      await agent.authenticate('testuser', 'password');
    });
    
    it('should format tasks list correctly', async () => {
      // Mock todo.list response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: [
            { id: 1, text: 'Buy milk', created_at: '2023-01-01T12:00:00Z' },
            { id: 2, text: 'Walk dog', created_at: '2023-01-02T12:00:00Z' }
          ]
        }
      });
      
      const result = await agent.listTasks();
      
      expect(result).toContain('Current tasks:');
      expect(result).toContain('[1] Buy milk');
      expect(result).toContain('[2] Walk dog');
    });
    
    it('should handle empty task list', async () => {
      mockAxios.post.mockResolvedValueOnce({
        data: { result: [] }
      });
      
      const result = await agent.listTasks();
      
      expect(result).toBe('No tasks found');
    });
    
    it('should handle errors when listing tasks', async () => {
      mockAxios.post.mockRejectedValueOnce(new Error('Network error'));
      
      const result = await agent.listTasks();
      
      expect(result).toContain('Failed to list tasks: Network error');
    });
  });
  
  describe('removeTask', () => {
    beforeEach(async () => {
      // Authenticate for all tests in this describe block
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      await agent.authenticate('testuser', 'password');
    });
    
    it('should remove task by ID', async () => {
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: { id: 1, text: 'Buy milk' }
        }
      });
      
      const result = await agent.removeTask(1);
      
      expect(result).toBe('Removed task: Buy milk');
      
      // Verify correct parameters were sent
      const callArgs = mockAxios.post.mock.calls[1]; // Second call after auth
      const [url, data] = callArgs as [string, any];
      expect(data.method).toBe('todo.remove');
      expect(data.params).toEqual({ id: 1 });
    });
    
    it('should handle errors when removing tasks', async () => {
      mockAxios.post.mockRejectedValueOnce(new Error('Task not found'));
      
      const result = await agent.removeTask(999);
      
      expect(result).toContain('Failed to remove task: Task not found');
    });
  });
  
  describe('executeTask', () => {
    beforeEach(async () => {
      // Authenticate for all tests in this describe block
      mockAxios.post.mockResolvedValueOnce({ 
        data: { token: 'test-token-123' } 
      });
      await agent.authenticate('testuser', 'password');
    });
    
    it('should add a task correctly', async () => {
      // Set up LLM to return "add" action
      mockLLM.responsesToReturn = [
        JSON.stringify({
          action: 'add',
          text: 'Buy milk',
          reasoning: 'This is a new todo item'
        })
      ];
      
      // Mock the add RPC response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: { id: 1, text: 'Buy milk' }
        }
      });
      
      const result = await agent.executeTask('add milk to my shopping list');
      
      expect(result).toContain('Added task: Buy milk');
      expect(mockLLM.promptsReceived.length).toBe(1);
      expect(mockLLM.promptsReceived[0]).toContain('You need to decide what to do with this task');
    });
    
    it('should list tasks correctly', async () => {
      // Set up LLM to return "list" action
      mockLLM.responsesToReturn = [
        JSON.stringify({
          action: 'list',
          reasoning: 'User wants to see current tasks'
        })
      ];
      
      // Mock the list RPC response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: [
            { id: 1, text: 'Buy milk', created_at: '2023-01-01T12:00:00Z' }
          ]
        }
      });
      
      const result = await agent.executeTask('show me my tasks');
      
      expect(result).toContain('Current tasks:');
      expect(result).toContain('[1] Buy milk');
    });
    
    it('should remove a task when ID is known', async () => {
      // Set up LLM to return "remove" action with ID
      mockLLM.responsesToReturn = [
        JSON.stringify({
          action: 'remove',
          id: 1,
          reasoning: 'User wants to remove this task'
        })
      ];
      
      // Mock the remove RPC response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: { id: 1, text: 'Buy milk' }
        }
      });
      
      const result = await agent.executeTask('remove the milk task');
      
      expect(result).toBe('Removed task: Buy milk');
    });
    
    it('should find and remove a task when ID is unknown', async () => {
      // Set up LLM to return "remove" action without ID
      mockLLM.responsesToReturn = [
        JSON.stringify({
          action: 'remove',
          reasoning: 'User wants to remove a task but didn\'t specify which one'
        }),
        // Second response for task selection
        '1'
      ];
      
      // Mock the list RPC response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: [
            { id: 1, text: 'Buy milk', created_at: '2023-01-01T12:00:00Z' },
            { id: 2, text: 'Walk dog', created_at: '2023-01-02T12:00:00Z' }
          ]
        }
      });
      
      // Mock the remove RPC response
      mockAxios.post.mockResolvedValueOnce({
        data: {
          result: { id: 1, text: 'Buy milk' }
        }
      });
      
      const result = await agent.executeTask('remove the milk task');
      
      expect(result).toContain('Removed task: Buy milk');
      expect(mockLLM.promptsReceived.length).toBe(2);
      expect(mockLLM.promptsReceived[1]).toContain('User wants to remove this task');
    });
    
    it('should handle invalid LLM response', async () => {
      // Set up LLM to return invalid JSON
      mockLLM.responsesToReturn = ['not a valid json'];
      
      const result = await agent.executeTask('do something');
      
      expect(result).toContain('Failed to process task');
    });
  });
}); 