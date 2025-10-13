import WebSocketServer from 'ws';
import http from 'http';

const server = http.createServer();
// Create a WebSocket server
const wss = new WebSocketServer({server});

const port = 8000;
server.listen(port, () => {
    console.log(`WebSocket server listening on port ${port}`);

});
// // Event handler for new connections
// wss.on('connection', (ws) => {
//   console.log('New client connected');
// 
//   // Event handler for receiving messages from the client
//   ws.on('message', (message) => {
//     console.log('Received message:', message);
// 
//     // Send a response back to the client
//     ws.send('Server received: ' + message);
//   });
// 
//   // Event handler for client disconnection
//   ws.on('close', () => {
//     console.log('Client disconnected');
//   });
// });

