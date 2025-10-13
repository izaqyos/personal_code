console.log("Event handling demo started");

// import events
var events = require('events');


//create eventEmitter
var eventEmitter = new events.EventEmitter();

//bind an event + event handler
//eventEmitter.on('eventName', eventHandler);
//
//emit event
//eventEmitter.emit('eventName');
//

//create event handler
var connectionHandler = function connected()  {

        console.log("connectionHandler called for successful connection");

        eventEmitter.emit('data_received');
}

//bind successful connection event to its event handler
eventEmitter.on('connection', connectionHandler);

eventEmitter.on('data_received', function () {
     console.log("anonymous data_received CB function called");
});

//fire the successful connection event
eventEmitter.emit('connection');

// listener #1
var listner1 = function listner1() {
   console.log('listner1 executed.');
}

// listener #2
var listner2 = function listner2() {
  console.log('listner2 executed.');
}

// Bind the connection event with the listner1 function
eventEmitter.addListener('connection', listner1);

// Bind the connection event with the listner2 function
eventEmitter.on('connection', listner2);

var eventListeners = require('events').EventEmitter.listenerCount
   (eventEmitter,'connection');
console.log(eventListeners + " Listner(s) listening to connection event");

// Fire the connection event 
eventEmitter.emit('connection');

// Remove the binding of listner1 function
eventEmitter.removeListener('connection', listner1);
console.log("Listner1 will not listen now.");

// Fire the connection event 
eventEmitter.emit('connection');

eventListeners = require('events').EventEmitter.listenerCount(eventEmitter,'connection');
console.log(eventListeners + " Listner(s) listening to connection event");

console.log("Program Ended.");

console.log("Event handling demo ended");

