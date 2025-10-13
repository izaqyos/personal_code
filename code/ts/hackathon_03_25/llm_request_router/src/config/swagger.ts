import swaggerJsdoc from 'swagger-jsdoc';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Content Design Time Assistant API',
      version: '1.0.0',
      description: 'API documentation for the Content Design Time Assistant',
      contact: {
        name: 'API Support',
        url: 'http://localhost:3001',
      },
    },
    servers: [
      {
        url: 'http://localhost:3001',
        description: 'Development server',
      },
    ],
    components: {
      schemas: {
        UserPromptRequest: {
          type: 'object',
          required: ['text'],
          properties: {
            text: {
              type: 'string',
              description: 'The prompt text to send to the assistant',
              example: 'How do I add a content provider?',
            },
          },
        },
        UserPromptResponse: {
          type: 'object',
          properties: {
            response: {
              type: 'string',
              description: "The assistant's response to the prompt",
            },
            requestType: {
              type: 'string',
              description: 'The classified type of the request',
              enum: ['action', 'help', 'unknown'],
            },
            actionType: {
              type: 'string',
              description: 'The specific action type (if request is an action)',
              enum: [
                'add_content_provider',
                'remove_content_provider',
                'update_content_provider',
                'delete_content_provider',
              ],
              nullable: true,
            },
            error: {
              type: 'string',
              description: 'Error message if an error occurred',
              nullable: true,
            },
          },
        },
      },
    },
  },
  apis: ['./src/routes/*.ts'], // Path to the API routes
};

export const specs = swaggerJsdoc(options); 