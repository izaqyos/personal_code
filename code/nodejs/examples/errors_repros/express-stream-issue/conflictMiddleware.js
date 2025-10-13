// conflictMiddleware.js
const rawBody = require('raw-body');

const conflictMiddleware = async (req, res, next) => {
    console.log('[ConflictMiddleware] Attempting to read stream...');
    try {
        // Attempt to read the stream. This uses the 'req' object which might
        // point to the original stream (error case) or the replaced stream (fixed case).
        const buffer = await rawBody(req, {
            limit: '1mb' // Set a limit
            // No length needed if reading from the replaced PassThrough stream in the fixed case
        });
        console.log(`[ConflictMiddleware] Successfully read stream (${buffer.length} bytes).`);
        // Store the buffer read by this middleware for potential verification
        req.conflictReadBuffer = buffer;
        next(); // Proceed if read was successful
    } catch (error) {
        console.error('[ConflictMiddleware] Failed to read stream:', error.message);
        // Check for errors indicating the stream was already consumed or ended
        if (error.message.includes('already ended') ||
            error.message.includes('not readable') ||
            error.code === 'ERR_STREAM_PREMATURE_CLOSE' || // Another possible error
            error.type === 'stream.destroyed' // raw-body might throw this
           ) {
            console.error('[ConflictMiddleware] Stream conflict detected!');
            // Simulate the error observed from Dynatrace
            return res.status(500).send('Internal Server Error: Stream conflict (simulated)');
        }
        // Pass other unexpected errors
        next(error);
    }
};

module.exports = conflictMiddleware;
