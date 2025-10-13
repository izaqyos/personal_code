// server-error.js
const express = require('express');
const conflictMiddleware = require('./conflictMiddleware');

const app = express();
const port = 3001; // Use a different port

// 1. express.json() runs first and consumes the stream
app.use(express.json());

// 2. conflictMiddleware runs second and tries to read the *already consumed* stream - like oneagent dynatrace jj
app.use(conflictMiddleware);

// Endpoint that should ideally receive the parsed body
app.post('/test', (req, res) => {
    console.log(' Received request.');
    // This part might not even be reached if conflictMiddleware sends a 500 error
    if (res.headersSent) {
        console.log(' Response already sent by middleware.');
        return;
    }
    console.log(' Parsed Body:', req.body);
    res.status(200).json({
        message: 'Success (Error Server)',
        receivedBody: req.body
    });
});

// Basic error handler
app.use((err, req, res, next) => {
  console.error("[Global Error Handler] Error:", err.message);
  if (!res.headersSent) {
    res.status(err.status || 500).send('Something broke!');
  }
});


const server = app.listen(port, () => {
    console.log(`Error server listening on port ${port}`);
});

module.exports = server; // Export for testing
