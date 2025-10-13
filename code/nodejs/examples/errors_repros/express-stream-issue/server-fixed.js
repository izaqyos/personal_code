// server-fixed.js
const express = require('express');
const bufferRawBodyMiddleware = require('./bufferRawBodyMiddleware');
const conflictMiddleware = require('./conflictMiddleware');

const app = express();
const port = 3002; // Use a different port

// 1. bufferRawBodyMiddleware runs first, reads the stream, and replaces req methods
app.use(bufferRawBodyMiddleware);

// 2. express.json() runs second, reads from the *replaced* (buffered) stream
app.use(express.json());

// 3. conflictMiddleware runs third, also reads from the *replaced* (buffered) stream
app.use(conflictMiddleware);

// Endpoint
app.post('/test', (req, res) => {
    console.log(' Received request.');
     if (res.headersSent) {
        console.log(' Response already sent by middleware.');
        return;
    }
    console.log(' Parsed Body:', req.body);

    // Optional: Verify the conflict middleware also got the same data
    let conflictReadMatches = false;
    if (req.rawBody && req.conflictReadBuffer) {
        conflictReadMatches = req.rawBody.equals(req.conflictReadBuffer);
        console.log(` Conflict middleware read matches original buffer: ${conflictReadMatches}`);
    }

    res.status(200).json({
        message: 'Success (Fixed Server)',
        receivedBody: req.body,
        conflictReadMatches: conflictReadMatches // Include verification in response
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
    console.log(`Fixed server listening on port ${port}`);
});

module.exports = server; // Export for testing
