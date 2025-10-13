const ax = require('axios')
const http = require('http');
const fs = require('fs');
const path = require('path');
const file='aa'
bigfileurl20mb='http://ipv4.download.thinkbroadband.com:8080/20MB.zip'
bigfileurl80mb='http://ipv4.download.thinkbroadband.com:8080/50MB.zip';
bigfileurl200mb='http://ipv4.download.thinkbroadband.com:8080/200MB.zip';
bigfilehost='ipv4.download.thinkbroadband.com';
// const maxsize = 2048;
const maxsize = 25*1024*1024;

url = 'http://localhost'+'/'+file;
// const url = 'http://localhost';

function getMaxSizeLim(url) {
    console.log('axios url', url);
    const config = {
        method: 'get',
        url: url,
        maxContentLength: maxsize, // response
        // maxBodyLength: maxsize, // request
        headers: {
            'User-Agent': 'Yosi Console',
            'maxContentLength': maxsize,
        }
    };
    ax(config).then(resp => {
        console.log(url+'download finished');
    })
    .catch (err => {
        console.log(url+'got error '+ err.message);
    });
}


function getMaxSizeLimAsStream(url) {
    console.log('axios url response as stream', url);
    const config = {
        method: 'get',
        url: url,
        // port: 8080,
        maxContentLength: maxsize, // response
        maxBodyLength: maxsize, // request
        responseType: 'stream',
        headers: {
            'User-Agent': 'Yosi Console',
            'maxContentLength': maxsize,
        }
    };
    ax(config).then(resp => {
        const fname = path.basename(url)
        resp.data.pipe(fs.createWriteStream(fname));
    })
        .catch (err => {
            console.log('HTTP get error', err.message);
        });
}

function getUsingRequests(url) {

    console.log('request url', url);
        const fname = path.basename(url)
    const opts = {
        method: 'GET',
        url: url,
        encoding: null,
        // hostname: bigfilehost,
        // path: path.basename(url),
    };
    const req = http.request(opts, resp => {
        console.log('get response status', resp.statusCode);
        console.log('get response length', resp.headers['content-length']);
        const file = fs.createWriteStream(fname);
        let size = 0;
        resp.on('data', data => {
            size+=data.length;
            if (size > maxsize) {
                console.log(`size ${size} exceeds limit ${maxsize}`);
                resp.abort(); //aborting response closes the stream
                fs.unlink(fname);
            }

        }).pipe(file);
        file.on('finish', () => {
            console.log('finished writing file');
            file.close();
        })
        // let data='';
        // resp.on('data', chunk => {
        //     data += chunk;
        // });
    });

    req.on('end', ()  => {
        console.log('end getting data. total length', data.length);
    });
    req.on('error', err  => {
        console.log('got error', err);
    });

    // req.write(data);
       req.end();

}

getMaxSizeLim(bigfileurl20mb);
getMaxSizeLim(bigfileurl80mb);
getMaxSizeLim(bigfileurl200mb);

// takes a long time so commented out
// getMaxSizeLimAsStream(bigfileurl20mb);
// getMaxSizeLimAsStream(bigfileurl80mb);
// getMaxSizeLimAsStream(bigfileurl200mb);
