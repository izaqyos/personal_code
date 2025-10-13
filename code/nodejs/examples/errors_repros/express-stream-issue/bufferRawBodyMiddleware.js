const { PassThrough } = require('stream');
const getRawBody = require('raw-body');
const contentType = require('content-type');

async function bufferRawBodyMiddleware(req, res, next) {
  const length = req.headers['content-length'];
  const encoding = req.headers['transfer-encoding'];
  const type = req.headers['content-type'];

  const hasBody = length || encoding;
  // Ensure we haven't already buffered and the stream is initially readable
  const shouldBuffer = hasBody && !req.rawBody && !req.body && !req._body && req.readable;

  if (!shouldBuffer) {
    return next();
  }

  let charset = 'utf-8';
  try {
    if (type) {
      charset = contentType.parse(req).parameters.charset || 'utf-8';
    }
  } catch (e) {
    console.warn('Could not parse content-type for charset, defaulting to utf-8:', type);
  }

  try {
    console.log('[BufferMiddleware] Buffering raw body...');
    const bodyBuffer = await getRawBody(req, {
      length: length ? parseInt(length, 10) : undefined,
      limit: '1mb',
      encoding: charset
    });

    req.rawBody = bodyBuffer; // Store the definitive buffer
    console.log(`[BufferMiddleware] Raw body buffered (${bodyBuffer.length} bytes).`);

    let consumerStream = null; // Holds the stream for the *current* consumer

    // Function to get a stream for the current consumer, creating it if necessary
    const ensureConsumerStream = () => {
      // If the current consumer stream is ended, destroyed, or doesn't exist, create a new one.
      if (!consumerStream || consumerStream.readableEnded || consumerStream.destroyed) {
        console.log('[BufferMiddleware] Creating new PassThrough stream for consumer.');
        consumerStream = new PassThrough();
        consumerStream.end(req.rawBody); // Load the buffer into the new stream

        // Auto-nullify when this stream finishes so the *next* consumer gets a fresh one.
        const nullifyStream = () => {
          console.log('[BufferMiddleware] Consumer stream finished. Nullifying.');
          consumerStream = null;
        };
        consumerStream.once('end', nullifyStream);
        consumerStream.once('close', nullifyStream);
        consumerStream.once('error', nullifyStream); // Also nullify on error
      }
      return consumerStream;
    };

    // Patch the necessary stream methods
    // NOTE: This assumes middleware primarily use .on, .pipe, .read to consume.
    // If they inspect properties like .readable, this might still be imperfect.
    req.on = (...args) => {
      const stream = ensureConsumerStream();
      // console.log(`[BufferMiddleware Patch] req.on('${args[0]}')`);
      return stream.on(...args);
    };
    req.pipe = (...args) => {
      const stream = ensureConsumerStream();
      // console.log(`[BufferMiddleware Patch] req.pipe()`);
      return stream.pipe(...args);
    };
    req.read = (...args) => {
      const stream = ensureConsumerStream();
      // console.log(`[BufferMiddleware Patch] req.read()`);
      return stream.read(...args);
    };
    req.pause = (...args) => {
      const stream = ensureConsumerStream();
      return stream.pause(...args);
    };
    req.resume = (...args) => {
      const stream = ensureConsumerStream();
      return stream.resume(...args);
    };
    req.isPaused = (...args) => {
      // Use the current consumer stream if it exists, otherwise report as not paused
      return consumerStream ? consumerStream.isPaused(...args) : false;
    };
    req.setEncoding = (...args) => {
      const stream = ensureConsumerStream();
      return stream.setEncoding(...args);
    };
    req.destroy = (...args) => {
      // Destroy the current consumer stream if it exists
      if (consumerStream) {
        return consumerStream.destroy(...args);
      }
    };
    // Add other methods as needed, forwarding to ensureConsumerStream()

    console.log('[BufferMiddleware] Original request stream methods replaced by stream factory.');
    next();

  } catch (err) {
    console.error('[BufferMiddleware] Error buffering raw body:', err.message);
    // Handle specific errors like entity too large if needed
    if (err.type === 'entity.too.large') {
      return res.status(413).send('Payload Too Large');
    }
    next(err);
  }
}

module.exports = bufferRawBodyMiddleware;