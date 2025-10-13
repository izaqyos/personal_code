// TODO:
// - use the official driver (https://github.com/NodeRedis/node_redis)
// - wrap client with promises (hint: bluebird in npm)
// - load a mock version of redis in case redis is not available
//    if redis is up - URL would be on env parameter (REDIS_URL)
//    hint: redis-mock in npm

// module.exports = client;
var redis = require('redis');

class mockClient{

        constructor(){
        }

        get(){
        }

        set(){
        }

        on(){
        }
}

let client;
if (! process.env.REDIS_URL ){
        client = new mockClient();
}
else {
    redis.createClient();
}
// client.on('error', function(err){
//   console.log('Something went wrong ', err)
// });
// client.set('my test key', 'my test value', redis.print);
// client.get('my test key', function(error, result) {
//   if (error) throw error;
//   console.log('GET result ->', result)
// });
