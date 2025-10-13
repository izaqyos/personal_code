const RoomManager = require("./RoomManager");

const manager = new RoomManager();

manager.on("create", function (room) {
    console.log('New room was created:', room);
});

manager.on("create", function (room) {
    console.log(room, 'was created...');
});

manager.createRoom({id: "dummy-room"});