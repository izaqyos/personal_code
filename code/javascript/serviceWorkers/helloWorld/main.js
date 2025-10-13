function getClickDemo() {
    document.getElementById("demo").innerHTML = "you clicked demo";
}

// create service worker
const worker = new Worker('task.js');

worker.addEventListener('message', msg => {
    console.log('service worker says: ', msg.data);
}, false);

//launch service worker
worker.postMessage("Hello service worker");
