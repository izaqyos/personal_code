var pg = require("pg");
var Q = require('q');

var config = require('./config.json').postgres;
config.max = 10; // connection pool size
config.idleTimeoutMillis = 30000; // how long a client is allowed to remain idle before being closed

var pool = new pg.Pool(config);

var db = module.exports = {
    getConnection: function () {
        console.log("asking for connection...");
        return Q.Promise(function (resolve, reject) {
            pool.connect(function(err, client, done) {
                if(err){
                    console.error("Could not get connection:", err);
                    return reject(err);
                }
                resolve({
                    client: client,
                    done: done
                });
            });
        });
    },
    singleQuery: function (query, params) {
        return db.getConnection()
            .then(_query.bind(null, query, params));
    }
};

function _query(query, params, con) {
    return Q.Promise(function (resolve, reject) {
        con.client.query(query, params || [], function (err, result) {
            con.done(); // closing the connection;
            if (err) {
                return reject(err);
            }
            resolve(result);
        });
    });
}