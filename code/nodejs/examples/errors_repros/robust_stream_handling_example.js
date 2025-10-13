/**
 * @file robust_app_example.js
 * @purpose Demonstrates a robust Express.js application structure resilient
 * to stream consumption errors by correctly using middleware and
 * implementing comprehensive error handling.
 * @see nodejs_stream_strategies_doc for underlying principles.
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3002; // Use environment variable or default

// --- Core Middleware Setup ---

// It's good practice to have logging/request ID middleware run first (not shown for brevity).

// Resilience Strategy #1: Standardize Middleware Order
// Place body parsers relatively early, after essential middleware like logging, CORS, etc.
// These consume the stream and populate `req.body`.
app.use(express.json({ limit: '1mb' })); // Parse JSON bodies, add size limit
app.use(express.urlencoded({ extended: true, limit: '1mb' })); // Parse URL-encoded bodies

// --- API Routes ---

// Example route demonstrating correct body handling and error catching
app.post('/api/items', (req, res, next) => {
  // Using try...catch within the handler for synchronous errors
  try {
    // Resilience Strategy #2: Prioritize req.body / Parsed Data
    // We directly use req.body, assuming express.json() or urlencoded() ran successfully.
    // We DO NOT attempt to access the raw req stream here.
    const newItemData = req.body;

    console.log('Received item data via req.body:', newItemData);

    // --- Example: Basic Validation ---
    if (!newItemData || !newItemData.name || !newItemData.value) {
      // Example of a synchronous error (Bad Request)
      // We create an error object and pass it to the global error handler via next()
      const validationError = new Error('Missing required fields: name and value.');
      validationError.status = 400; // Add a status code for the error handler
      return next(validationError); // Use return to stop execution here
    }

    // --- Example: Processing Logic ---
    // (In a real app, interact with a database, etc.)
    const createdItem = {
      id: Date.now(), // Simple ID generation for example
      ...newItemData,
      createdAt: new Date().toISOString()
    };

    // Send successful response
    res.status(201).json({
        message: "Item created successfully",
        item: createdItem
    });

  } catch (error) {
    // Catch any unexpected synchronous errors during validation or processing
    console.error(`Unexpected error in POST /api/items handler: ${error.message}`);
    // Pass the error to the global Express error handler
    // Ensure it has a status code or the global handler assigns one
    error.status = error.status || 500;
    next(error);
  }
});

// --- Catch-All for 404 Not Found ---
// If no route above matched, this middleware will run
app.use((req, res, next) => {
  const error = new Error(`Not Found - ${req.originalUrl}`);
  error.status = 404;
  next(error); // Pass the 404 error to the global error handler
});


// --- Global Error Handling Middleware ---
// Resilience Strategy #4: Implement Robust Global Error Handling
// This MUST be the last middleware defined.
// It catches all errors passed by `next(error)`.
// Note the specific 4-argument signature (err, req, res, next).
app.use((err, req, res, next) => {
  // Log the error (in a real app, use a proper logger like Winston or Pino)
  // Include request ID if available
  console.error(`Global Error Handler Caught: ${err.message}`, {
      status: err.status || 500,
      stack: err.stack, // Include stack trace for debugging
      // requestUrl: req.originalUrl, // Optional: log request context
      // requestMethod: req.method, // Optional: log request context
  });

  // Determine status code: use error's status or default to 500
  const statusCode = err.status || 500;

  // Send a generic error response to the client
  // Avoid sending detailed error messages or stack traces in production
  res.status(statusCode).json({
    error: 'Server Error',
    // Optionally include message in non-production environments
    // message: process.env.NODE_ENV !== 'production' ? err.message : undefined
    message: `An internal server error occurred.` // More generic message
  });
});


// --- Server Initialization ---
app.listen(PORT, () => {
  console.log(`Robust server listening on port ${PORT}`);
});

