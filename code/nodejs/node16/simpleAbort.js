let controller = new AbortController();
let signal = controller.signal;

signal.addEventListener('abort', () => console.log('operation aborted'));

console.log('signal.aborted before abort', signal.aborted);
controller.abort();
console.log('signal.aborted after abort', signal.aborted);
