# Testing Guide for Agent Framework

This document provides information on how to run and maintain tests for the agent-framework.

## Test Coverage

The testing suite covers the following components:

1. **MCPAgent** - Main agent class for communicating with the MCP server
2. **LLM Providers** - OpenAI and Ollama providers
3. **Integration Tests** - End-to-end tests with a running MCP server

## Running Tests

### Prerequisites

- Node.js and npm installed
- For integration tests:
  - MCP server running at http://localhost:3000 (or specified by MCP_SERVER_URL)
  - For Ollama tests: Local Ollama server running at http://localhost:11434 (or specified by OLLAMA_API_URL)
  - For OpenAI tests: Valid OpenAI API key set in the OPENAI_API_KEY environment variable

### Environment Setup

Create a `.env` file in the agent-framework directory based on the `.env-example` file:

```
MCP_SERVER_URL=http://localhost:3000
MCP_USERNAME=username
MCP_PASSWORD=password
OPENAI_API_KEY=your_openai_key
OLLAMA_API_URL=http://localhost:11434
DEBUG_MODE=true
```

### Commands

Run all tests:
```
npm test
```

Run unit tests only:
```
npm test -- --testPathPattern=unit
```

Run integration tests:
```
npm test -- --testPathPattern=integration --env RUN_INTEGRATION_TESTS=true
```

Generate test coverage report:
```
npm run test:coverage
```

## Test Structure

### Unit Tests

Unit tests are located in `tests/unit` and use Jest mocks to isolate components:

- `agent.test.ts` - Tests for the MCPAgent class
- `ollama-provider.test.ts` - Tests for Ollama API integration
- `openai-provider.test.ts` - Tests for OpenAI API integration

### Integration Tests

Integration tests in `tests/integration` verify end-to-end functionality:

- `agent-mcp-integration.test.ts` - Tests agent interaction with a live MCP server

## Writing New Tests

### Adding Unit Tests

1. Create a new file in `tests/unit` directory
2. Import necessary modules and use Jest mocks for dependencies
3. Follow the AAA pattern (Arrange, Act, Assert) for test structure

Example:
```typescript
import { jest, describe, it, expect } from '@jest/globals';
import { YourComponent } from '../../src/your-component';

jest.mock('dependency');

describe('YourComponent', () => {
  it('should perform specific action', () => {
    // Arrange
    const component = new YourComponent();
    
    // Act
    const result = component.method();
    
    // Assert
    expect(result).toBe(expectedValue);
  });
});
```

### Adding Integration Tests

1. Create a new file in `tests/integration` directory
2. Use the `describeIntegration` helper to make tests skippable
3. Set up test data before tests and clean up after tests

## Maintaining Tests

- Run tests before committing changes
- Keep test coverage high (aim for >80% statement coverage)
- Update tests when changing functionality
- Fix flaky tests promptly 