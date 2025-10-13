// Import the required modules
const WebSocket = import('ws');

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

// Event handler for new connections
wss.on('connection', (ws) => {
  console.log('New client connected');

  // Event handler for receiving messages from the client
  ws.on('message', (message) => {
    console.log('Received message:', message);

    // Send a response back to the client
    ws.send('Server received: ' + message);
  });

  // Event handler for client disconnection
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

