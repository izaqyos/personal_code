//type WorkerCallback = (err: any, result?: any) => any;
//
//export function runWorker(path: string, cb: WorkerCallback,
//        WorkerData: object | null = null) {
//        const worker = new Worker(path, {WorkerData});
//
//        worker.on('message', cb.bind(null, null);
//        worker.on('error', cb);
//
//        worker.on('exit', (exitCode) => {
//                if (exitCode === 0) {
//                        return null;
//                }
//
//                return cb(new Error(`worker thread stopped. code ${exitCode}`));
//        });
//
//        return worker;

const {Worker, isMainThread, workerData} = require('worker_threads');

let currentVal = 0;
let intervals = [100, 1000, 500];

function counter(id, i){
        console.log("[", id, "]", i);
        return i;
}

if (isMainThread){
        console.log("main thread");
        for (let i=0; i<2; i++) {
                //create two worker threads. pass i to them on workerData
                let wt = new Worker(__filename, {workerData: i}); // threads code require absolute path to .js file
        }

        //Also, print every 500ms main thread counter
    setInterval((a) => currentVal = counter(a, currentVal+1), intervals[2], "MainThread");
} else {

        console.log("Worker thread");
        setInterval((a) => currentVal = counter(a, currentVal+1), intervals[workerData],workerData); //pass workerData to setInterval CB (as param a) , workerData is the index from the main thread loop

}


