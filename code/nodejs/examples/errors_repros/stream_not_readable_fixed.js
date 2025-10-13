/**
 * @file nodejs_stream_handling_fixed.js
 * @purpose Corrected version demonstrating the proper way to handle request bodies
 * after using body-parsing middleware like express.json().
 * @important Always use req.body after body-parsing middleware.
 */

const express = require('express');
const app = express();

// --- Middleware ---
// express.json(): Parses JSON bodies and makes them available on req.body.
// It consumes the request stream.
app.use(express.json());

// --- Route Definition (Corrected) ---
// Handles POST requests to the /data endpoint.
app.post('/data', (req, res, next) => { // 'next' is used for error handling
  try {
    // *** FIX START *** //

    // 1. REMOVED: The check for stream state (req.readable / req.readableEnded)
    //    and the explicit throwing of an error based on that check.
    //    This is no longer needed as we won't attempt to read the raw stream.

    // 2. REMOVED: The entire "Problematic Code Section" which incorrectly
    //    attempted to attach listeners (req.on('data'), req.on('end'), req.on('error'))
    //    to the request stream after it was already consumed by express.json().

    // 3. ADDED: Direct use of `req.body`.
    //    Middleware (express.json) has already processed the stream and
    //    made the parsed data available here. This is the correct approach.
    console.log('Using parsed body from middleware:', req.body);

    // Example: Send back the received data in the response
    res.status(200).json({
        message: "Data received successfully via req.body",
        receivedData: req.body // Use the data from req.body
    });

    // *** FIX END *** //
  } catch (error) {
    console.error("Caught exception in route handler:", error.message);
    // Pass the error to the Express error handling middleware
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