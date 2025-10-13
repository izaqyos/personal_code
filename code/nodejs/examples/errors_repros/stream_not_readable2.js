const express = require('express');
const app = express();

// Middleware that consumes the stream
app.use(express.json());

app.post('/data', (req, res, next) => { // Added 'next' for error handling
  try {
    // Log the state for demonstration purposes
    // Note: `readableEnded` might be undefined in very old Node versions, hence the nullish coalescing
    console.log(`Entering handler: req.readable = ${req.readable}, req.readableEnded = ${req.readableEnded ?? 'N/A'}`);

    // *** CHECK ADDED HERE ***
    // Check if the stream is already ended or not readable BEFORE attaching listeners.
    // This indicates it was likely consumed by middleware.
    if (req.readableEnded || !req.readable) {
      // Explicitly throw an error if the stream is already consumed.
      throw new Error('Stream is not readable or has already ended. Likely consumed by middleware.');
    }

    // --- Original problematic code remains below ---
    // --- This part will likely still not function correctly even if the check above passed
    // --- (which it shouldn't in this scenario after express.json),
    // --- but the goal was to add the explicit error throw.

    let rawData = '';
    console.log('Attempting to attach stream listeners (should ideally not reach here after check)');

    req.on('data', (chunk) => {
      console.log('Listener received data chunk (Problematic - should not happen)');
      rawData += chunk;
    });

    req.on('end', () => {
      console.log('Listener received end event (Problematic - should not happen)');
      console.log('Raw data attempt:', rawData);
      console.log('Parsed body:', req.body);
      // This likely won't be reached if the 'end' event doesn't fire
      res.json({ received: req.body });
    });

    req.on('error', (err) => {
      console.error("Stream 'error' event listener caught:", err);
      // Pass stream errors to the Express error handler
      next(err);
    });
    // --- End of original problematic code ---

  } catch (error) {
    // Catch the explicitly thrown error (or any other synchronous error)
    console.error("Caught exception in route handler:", error.message);
    // Pass the error to the Express error handling middleware
    next(error);
  }
});

// *** ADDED: Basic Express Error Handler ***
// This middleware catches errors passed via next()
app.use((err, req, res, next) => {
  console.error("Express error handler caught:", err.message);
  // Send a generic server error response
  res.status(500).json({
    error: 'Server Error',
    message: err.message // Include the specific error message
  });
});


app.listen(3001, () => console.log('Server running on port 3001'));
