const { AsyncLocalStorage } = require('async_hooks');

const asyncLocalStorage = new AsyncLocalStorage();

function logWithRequestId(message) {
  const store = asyncLocalStorage.getStore();
  const requestId = store ? store.requestId : 'N/A';
  console.log(`[${requestId}] ${message}`);
}

function handleRequest(requestId) {
  asyncLocalStorage.run({ requestId }, () => { // Create a new context
    logWithRequestId('Starting request processing...');
    setTimeout(() => {
      logWithRequestId('Database query complete.');
      setTimeout(() => {
        logWithRequestId('Sending response.');
      }, 50);
    }, 100);
  });
}

handleRequest(123);
handleRequest(456);
