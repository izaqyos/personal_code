const http = require('http');
// keep the connection open
const agent = new http.Agent({ keepAlive: true });

module.exports = ({host, data = {}, path = '/', port = 80, method = 'POST', contentType = 'application/json'}) => {
    data = JSON.stringify(data);
    const headers = method === 'POST' ? {
        'Content-Type': contentType,
        'Content-Length': Buffer.byteLength(data)
    } : {};
    const ops = {
        hostname: host,
        port: port,
        path,
        method,
        headers
    };
    return request(ops, data);
};

function request(ops, postData) {
    return new Promise((resolve, reject) => {
        const req = http.request({
            ...ops,
            agent
        }, (res) => {
            const data = [];

            const {headers, statusCode} = res;
            console.log(`status: ${statusCode}, headers: ${JSON.stringify(headers)}`);

            res.on('data', (chunk) => {
                data.push(chunk);
            });

            res.on('end', () => {
                resolve(data.join(""));
            });
        });

        req.on('error', (e) => reject(e));

        req.write(postData);
        req.end();
    })
}