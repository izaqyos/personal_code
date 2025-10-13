var server = require('./server/index.js');
var port = process.env.PORT || 3000;

server.listen(port, function(){
        console.log("server running on port %d", port);
});







