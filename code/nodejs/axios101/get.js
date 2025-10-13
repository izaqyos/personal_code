const ax = require('axios')

const url = 'http://ynet.co.il';
ax.get(url).then(resp => {
    console.log('get response status:',resp.status);
});

async function aget() {
    const resp = await ax.get(url);
    console.log('async/await got response status:',resp.status);
}

async function aget_header() {
    const config = {
        method: 'get',
        url: url,
        headers: {
            'User-Agent': 'Yosi Console'
        }
    };
    const resp = await ax(config);
    console.log('got response with custom header:',resp.request._header);
}

aget();
aget_header();

