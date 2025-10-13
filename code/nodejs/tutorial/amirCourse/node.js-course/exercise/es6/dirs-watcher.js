let EventEmitter = require('events').EventEmitter;
let fs = require('fs');

class DirsWatcher extends EventEmitter {
    constructor (...args) {
        super(...args);
        this._watchers = {}; // holds all active _watchers
    }

    start(dir) {
        // TODO: watch the given directory (file change) and fire 'change' event
    }

    stop(dir) {
        // TODO: stop watching
    }

    /**
     *
     * @private
     * @param e {Event}
     * @returns {*}
     */
    _fireEvent(e) {
        return e && this.emit(e.name, e.data);
    }
}

class Event {
    constructor(name, data) {
        this.name = name;
        this.data = data;
    }
}

module.exports.DirsWatcher = DirsWatcher;
module.exports.Event = Event;