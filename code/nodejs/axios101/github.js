
const ax = require('axios')
const url = 'https://api.github.com/users/izaqyos';

async function getgitdata() {
    const config = {
        method: 'get',
        url: url,
        headers: {
            'User-Agent': 'Yosi Console'
        }
    };
    const resp = await ax(config);
    console.log(`followers ${resp.data.followers}, location ${resp.data.location}`);
}

getgitdata()

