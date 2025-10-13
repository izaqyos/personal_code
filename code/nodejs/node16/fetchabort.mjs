import fetch from 'node-fetch';

const delay = process.argv[2] ?? 10000;
console.log('got delay argument', delay);
const url1 = 'https://www.brainyquote.com/quote_of_the_day';
async function demo_fetch_abort(abortDelay, url) {
    const controller = new AbortController();
    setTimeout( () => controller.abort(), abortDelay);
    console.log('fetch from ', url);
    try {
        let resp = await fetch(url, {signal: controller.signal});
        const text = await resp.text();
        const lines = text.split('\n');
        //console.log(typeof text);
        console.log( lines.find( elem => elem.includes('twitter:description') ) );
    } catch (e) {
        if (e.name === 'AbortError') {
            console.log('fetch was aborted');
        }
        else {
            console.log(`got error ${e}`);
        }
        /* handle error */
    }
}

console.log('Demo aborting fetch using node 16 AbortController. First run abort fetch if longer than 1 sec (expect success)');
demo_fetch_abort(delay, url1);
// console.log('Demo aborting fetch using node 16 AbortController. Second run abort fetch if longer than 10ms (expect abort), will print before first :) ');
// demo_fetch_abort(10);
