/**
 * @file nodejs_stream_handling_example.js
 * @purpose Demonstrates handling of request streams in Express.js, specifically
 * how middleware like express.json() consumes the stream, preventing
 * subsequent reads. Shows how to detect this and handle the error.
 * @important Middleware order is crucial. Body parsers must come before route
 * handlers that need the parsed body.
 * @important Always use req.body to access parsed data after middleware,
 * not the raw stream.
 *
 * @usage
 * 1. Run this file using `node nodejs_stream_handling_example.js`.
 * 2. Send a POST request with 'Content-Type: application/json' and a JSON body
 * to http://localhost:3001/data (e.g., using curl).
 * 3. Observe the server logs and the HTTP 500 error response returned to the client,
 * indicating the stream was already consumed.
 */

const express = require('express');
const app = express();

// --- Middleware ---
// express.json(): Parses incoming requests with JSON payloads.
// CRITICAL: This middleware reads and consumes the *entire* request stream
// to make the parsed data available as `req.body`.
app.use(express.json());

// --- Route Definition ---
// Handles POST requests to the /data endpoint.
app.post('/data', (req, res, next) => { // 'next' is used to pass errors to the error handler
  try {
    // Log the initial state of the request stream upon entering the handler.
    // After express.json(), `req.readable` should be false and `req.readableEnded` should be true.
    console.log(`Entering handler: req.readable = ${req.readable}, req.readableEnded = ${req.readableEnded ?? 'N/A'}`);

    // --- Stream State Check ---
    // Verify if the stream is still readable or has already ended.
    // If either is true, it signifies that middleware has already processed the stream.
    if (!req.readable || req.readableEnded) {
      const errorMessage = 'Request stream is not readable or has ended. Likely consumed by middleware.';
      console.error("Error:", errorMessage);
      // Throw an error to stop processing and trigger the error handler.
      throw new Error(errorMessage);
    }

    // --- Problematic Code Section ---
    // The following code attempts to read the raw request stream manually.
    // IMPORTANT: This section will NOT execute correctly because `express.json()`
    // has already consumed the stream. The `data` and `end` events will not
    // be emitted for these listeners attached *after* consumption.
    // This block is kept purely for illustrative purposes of what *not* to do.
    console.log('Attempting to attach stream listeners (should not happen)');
    let rawData = '';
    req.on('data', (chunk) => {
      // This listener will likely never receive any data.
      console.log('Listener received data chunk (Problematic - should not happen)');
      rawData += chunk;
    });

    req.on('end', () => {
      // This listener will likely never be called.
      console.log('Listener received end event (Problematic - should not happen)');
      console.log('Raw data attempt:', rawData); // Will likely be empty
      // The response logic here is unreachable in this scenario.
      res.json({ received: req.body });
    });

    req.on('error', (streamError) => {
      // Handles potential errors emitted directly by the stream object itself.
      console.error("Stream 'error' event listener caught:", streamError);
      // Pass the stream error to the Express error handling middleware.
      next(streamError);
    });
    // --- End of Problematic Code Section ---

  } catch (error) {
    // Catches synchronous errors, including the one explicitly thrown above.
    console.error("Caught exception in route handler:", error.message);
    // Pass the caught error to the Express error handling middleware.
    next(error);
  }
});

// --- Express Error Handling Middleware ---
// This middleware specifically handles errors passed via `next(error)`.
// It must have four arguments (err, req, res, next) to be recognized by Express.
app.use((err, req, res, next) => {
  console.error("Express error handler caught:", err.message);
  // Send a standardized HTTP 500 Internal Server Error response.
  res.status(500).json({
    error: 'Server Error',
    message: err.message // Include the error message for client debugging.
  });
});

// --- Server Initialization ---
// Start the Express server, making it listen for connections on port 3001.
app.listen(3001, () => console.log('Server running on port 3001'));
