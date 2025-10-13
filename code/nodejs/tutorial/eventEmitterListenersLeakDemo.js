//Assume Logger is a module that emits errors
//var Logger = require('./Logger.js');


const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();
for (var i = 0; i < 11; i++) {
console.log('number of listeres: ' +EventEmitter.listenerCount(myEmitter, 'event'));
myEmitter.on('event', () => {
  console.log('an event occurred!');
});
}
myEmitter.emit('event');

//Note, to fix (node:85333) MaxListenersExceededWarning: Possible EventEmitter memory leak detected. 11 event listeners added. Use emitter.setMaxListeners() to increase limit
//remove the .on (register event listener)  from loop
