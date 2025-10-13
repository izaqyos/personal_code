const { EventEmitter } = require('events');

class RoomManager extends EventEmitter{
    constructor() {
        super();
        this.rooms = [];
    }
    createRoom(room) {
        this.rooms.push(room);
        process.nextTick(() => {
            this.emit("create", room);
        });
    }
    getRoom(i) {
        return this.rooms[i];
    }
}

module.exports = RoomManager;