import { setTimeout, setInterval, setImmediate} from 'timers/promises';

const setTORes = await setTimeout(500, "setTimeout result :)");
console.log(setTORes);
const setImmediateRes = await setTimeout(500, "setImmediate result :)");
console.log(setImmediateRes);

const interval = 50;
for await (const startTime of setInterval(interval, Date.Now)) {
    const now = Date.now();
    console.log(now);
    if ((now-startTime) > 1000) {
        break;
    }
}
console.log(Date.now());
