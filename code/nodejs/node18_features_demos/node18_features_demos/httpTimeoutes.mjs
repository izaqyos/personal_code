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
$ node --version
v19.5.0*
 $ node httpTimeoutes.mjs
headersTimeout= 60000
requestTimeout= 300000
 */
