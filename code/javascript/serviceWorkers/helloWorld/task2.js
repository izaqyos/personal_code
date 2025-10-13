self.addEventListener('message', evt => {
    const data = evt.data;
    switch (data.cmd) {
        case 'start':
            self.postMessage('Worker started '+data.msg);
            break;
        case 'stop':
            self.postMessage('Worker stopped '+data.msg + ' buttons will stop working');
            // 2nd way to stop worker. by calling self.close() from within the worker
            self.close();
            break;
        default:
            self.postMessage('got an unknown cmd ' + data.msg);
    }
}, false)