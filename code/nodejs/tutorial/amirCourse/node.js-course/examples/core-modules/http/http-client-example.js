const httpRequest = require('./my-http-client');

async function run() {
    const res = await httpRequest({host: "localhost", port: 8001, data: {"my":"dummy", "da": "ta"}});
    console.log(`res: ${res}`);
    return res;
}

run().then(() => console.log("done!"));
