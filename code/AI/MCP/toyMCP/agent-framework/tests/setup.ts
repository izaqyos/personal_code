import { jest, beforeAll, afterAll } from '@jest/globals';

// Mock environment variables
process.env.MCP_SERVER_URL = 'http://localhost:3000';
process.env.MCP_USERNAME = 'test_user';
process.env.MCP_PASSWORD = 'test_password';
process.env.OPENAI_API_KEY = 'test_openai_key';
process.env.OLLAMA_API_URL = 'http://localhost:11434';
process.env.DEBUG_MODE = 'true';

// Set test timeout
jest.setTimeout(10000); // 10 second timeout for all tests

// Global beforeAll and afterAll hooks can be added here
beforeAll(() => {
  // Setup code that runs before all tests
  console.log('Starting agent-framework tests...');
});

afterAll(() => {
  // Cleanup code that runs after all tests
  console.log('Completed agent-framework tests.');
}); 