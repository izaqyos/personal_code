self.addEventListener('message', evt => {
    self.postMessage(evt.data);
}, false)