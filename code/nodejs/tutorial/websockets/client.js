const WebSocket = require('ws');

// Create a WebSocket connection to the server
const ws = new WebSocket('ws://localhost:8080');

// Event handler for connection established
ws.on('open', () => {
  console.log('Connected to WebSocket server');

  // Send a message to the server
  ws.send('Hello, server!');
});

// Event handler for receiving messages from the server
ws.on('message', (message) => {
  console.log('Received message:', message);
});

// Event handler for connection closed
ws.on('close', () => {
  console.log('Disconnected from WebSocket server');
});

