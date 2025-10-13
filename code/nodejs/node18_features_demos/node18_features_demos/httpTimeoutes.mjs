import express from 'express';
import path, {dirname} from 'path';
import {fileURLToPath} from 'url';

const app = express();
const __dirname = dirname(fileURLToPath(import.meta.url));
app.use(express.static(path.join(__dirname, 'index.html')));

app.get('/*', (req, res) => {
    setTimeout( () => res.sendFile(path.join(__dirname, './index.html')), 2000);
});

const server = app.listen(8080);
console.log('headersTimeout=', server.headersTimeout);
console.log('requestTimeout=', server.requestTimeout);

/*
 node 19 defaults, 1 and 5 min
[i500695@WYLQRXL9LQ:2023-02-01 16:56:28:~/work/code/nodejs/node18:]2005$ node --version
v19.5.0*
 [i500695@WYLQRXL9LQ:2023-02-01 16:55:54:~/work/code/nodejs/node18:]2005$ node httpTimeoutes.mjs
headersTimeout= 60000
requestTimeout= 300000
 */
