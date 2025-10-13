import { jest, describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import axios from 'axios';
import { MCPAgent } from '../../src/agent';
import { OllamaProvider } from '../../src/ollama-provider';

// Skip these tests if not running integration tests
const shouldRunIntegrationTests = process.env.RUN_INTEGRATION_TESTS === 'true';
const describeIntegration = shouldRunIntegrationTests ? describe : describe.skip;

describeIntegration('MCPAgent Integration with MCP Server', () => {
  let agent: MCPAgent;
  let ollamaProvider: OllamaProvider;
  const MCP_SERVER_URL = process.env.MCP_SERVER_URL || 'http://localhost:3000';
  const MCP_USERNAME = process.env.MCP_USERNAME || 'test_user';
  const MCP_PASSWORD = process.env.MCP_PASSWORD || 'test_password';
  
  beforeAll(async () => {
    // Check if MCP server is running
    try {
      await axios.get(`${MCP_SERVER_URL}/health`);
      console.log(`MCP server at ${MCP_SERVER_URL} is available`);
    } catch (error) {
      console.error(`MCP server at ${MCP_SERVER_URL} is not available, skipping integration tests`);
      return;
    }
    
    // Create a real Ollama provider for integration tests
    ollamaProvider = new OllamaProvider('llama3', process.env.OLLAMA_API_URL, true);
    
    // Create agent
    agent = new MCPAgent(MCP_SERVER_URL, ollamaProvider, true);
    
    // Authenticate with the MCP server
    const authResult = await agent.authenticate(MCP_USERNAME, MCP_PASSWORD);
    if (!authResult) {
      throw new Error('Authentication failed, cannot continue integration tests');
    }
    
    console.log('Successfully authenticated with MCP server');
    
    // Clean up any existing tasks for clean test environment
    await cleanupTasks();
  });
  
  afterAll(async () => {
    // Clean up any tasks created during tests
    await cleanupTasks();
  });
  
  // Helper function to clean up tasks
  async function cleanupTasks() {
    if (!agent) return;
    
    try {
      const response = await agent.executeRPC('todo.list');
      const tasks = response.result || [];
      
      for (const task of tasks) {
        await agent.executeRPC('todo.remove', { id: task.id });
        console.log(`Removed task: ${task.text}`);
      }
    } catch (error) {
      console.error('Error during task cleanup:', error);
    }
  }
  
  it('should add a task via natural language', async () => {
    // Execute a task to add a new item
    const result = await agent.executeTask('add buy milk to my shopping list');
    
    // Verify task was added
    expect(result).toContain('Added task');
    expect(result).toContain('milk');
    
    // Verify task exists in list
    const listResponse = await agent.executeRPC('todo.list');
    const tasks = listResponse.result;
    
    expect(tasks.length).toBeGreaterThan(0);
    const addedTask = tasks.find((t: any) => t.text.toLowerCase().includes('milk'));
    expect(addedTask).toBeTruthy();
  });
  
  it('should list tasks', async () => {
    // Add a task first to ensure there's something to list
    await agent.executeRPC('todo.add', { text: 'Test task for listing' });
    
    // Execute the list task
    const result = await agent.executeTask('show me my tasks');
    
    // Verify list contains tasks
    expect(result).toContain('Current tasks:');
    expect(result).toContain('Test task for listing');
  });
  
  it('should remove a task', async () => {
    // Add a task first
    const addResponse = await agent.executeRPC('todo.add', { text: 'Remove this task test' });
    const taskId = addResponse.result.id;
    
    // Execute remove task
    const result = await agent.executeTask('remove the task about removing');
    
    // Verify removal was successful
    expect(result).toContain('Removed task');
    
    // Verify task is no longer in list
    const listResponse = await agent.executeRPC('todo.list');
    const tasks = listResponse.result;
    const removedTask = tasks.find((t: any) => t.id === taskId);
    expect(removedTask).toBeUndefined();
  });
}); 