let times=1000000000;
console.log('measure 1G assignments');

let hrstart = process.hrtime();
let flag = false;
for (i=0; i<times; i++){
    flag = true;
}
let hrend = process.hrtime(hrstart);

console.log('1G assignments execution time: %ds %dms', hrend[0], hrend[1]/1000000);

console.log('measure 10k comparisons and conditioned assignments');
hrstart = process.hrtime();
flag = false;
for (i=0; i<times; i++){
    if (!flag) flag = true;
}
hrend = process.hrtime(hrstart);

console.log('1G comparisons and conditioned assignments execution time: %ds %dms', hrend[0], hrend[1]/1000000);

var start = new Date()
let hrstart1 = process.hrtime()
var simulateTime = 5

setTimeout(function(argument) {
  // execution time simulated with setTimeout function
  var end = new Date() - start,
    hrend = process.hrtime(hrstart1)

  console.info('Execution time: %dms', end)
  console.info('Execution time (hr): %ds %dms', hrend[0], hrend[1] / 1000000)
}, simulateTime)

class ttlMap {
    constructor(repeats) {
        this.repeats = repeats;
        this.amap = new Map()
    }

    countSeconds() {
        let start = new Date();
        console.log('count seconds. start', start);
        let end;
        for (let i = 0; i < this.repeats ; i++) {
            setTimeout( () => {
                end = new Date() - start;
                start = new Date();
                console.log('counted '+(i+1)+' seconds using Date() diff in seconds'+(end/1000))

            }, 1000)
        }
    }

    set(k,v) {
        const now = Date.now();
        this.amap.set(k, [v, now])
        console.log('set '+k+' => '+v+' at time '+now);
    }

    get(k) {
        if (! this.amap.has(k) ) {
            console.log('entry '+k+' does not exist');
            return;
        }
        const now = Date.now();
        const [v, createTime] = this.amap.get(k);
        const elapsed = (now-createTime)/1000; 
        console.log('get '+k+' => '+v+' at time '+now+', lifetime is '+elapsed+' seconds');
        if (elapsed < 2)
        {
            return v
        }
        else {
            console.log(k+' has expired');
            this.amap.delete(k);
        }
    }
}

const ttl = new ttlMap(10);
ttl.countSeconds();
ttl.set('a', 1);
ttl.set('b', 2);
ttl.set('c', 3);
ttl.set('d', 4);
setTimeout(() => {
    console.log('wait a few seconds');
    console.log('value of a: ', ttl.get('a'));
    console.log('value of b: ', ttl.get('b'));
}, 2000);
setTimeout(() => {
    console.log('wait a few seconds');
    console.log('value of c: ', ttl.get('c'));
    console.log('value of d: ', ttl.get('d'));
}, 1000);

setTimeout(() => {
    console.log('end demo');
}, 20000);
