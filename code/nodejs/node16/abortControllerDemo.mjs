import { setTimeout, setInterval, setImmediate} from 'timers/promises';

/*
long running promise 
note use of options argument to pass the abort signal in
also not check for aborted signal after firing the long time operation (simulated by setTimeout)
 */
const someLongRunningTask = async (delay, msg, options) => {
   const signal = {...options};
    console.log('got signal', signal);
   const res = await setTimeout(delay, msg);
    console.log('got signal 2 ', JSON.stringfy(signal, null, 4));
    if (signal.signal.aborted === true) {
        throw new Error('someLongRunningTask cancelled');
    }
   console.log(`waited ${delay}, ${msg}`);
};

console.log('Cancel promise using AbortController');

// straightforward, an AbortController for TO and Task promises
const cancelTO = new AbortController();
const cancelTask = new AbortController();

async function timeout1() {
    try {
        await setTimeout(1000, undefined, {signal: cancelTO.signal}); // note, setTimeout options argument passes cancelTO signal
        console.log('aborting task');
        cancelTask.abort(); // timeout1 cancels task after 1 second
        
    } catch (e) {
        /* handle error */
    }
}

async function task() {
    try {
        await someLongRunningTask(5000,  'long running task finished', {signal: cancelTask.signal}); //  note, setTimeout options argument passes cancelTask signal 
    }
    finally {
        cancelTO.abort(); // task cancels timeout1 
    }
    }

await Promise.race([timeout1(), task()]);
