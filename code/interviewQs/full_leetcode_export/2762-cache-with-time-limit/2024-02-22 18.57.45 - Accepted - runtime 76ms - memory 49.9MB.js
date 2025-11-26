var TimeLimitedCache = function() {
    this.kv_ttl_map = new Map(); // value contains, createdAt, duration and original value array
};

/** 
 * @param {number} key
 * @param {number} value
 * @param {number} duration time until expiration in ms
 * @return {boolean} if un-expired key already existed
 */
TimeLimitedCache.prototype.set = function(key, value, duration) {
    let retval = false;
    let now = new Date(); 
    console.log(`set() params ${[key, value, duration]}`);

    if (this.kv_ttl_map.has(key)) {
        console.log(`set() ${key} exists`);
        [val, ctime, dur] = this.kv_ttl_map.get(key);
        if ((now-ctime) < dur) {
            retval = true;
        } else retval = false;
    }
    console.log(`set() setting key value to ${[value, now, duration]}`);
    this.kv_ttl_map.set(key,[value, now, duration]);
    if (this.kv_ttl_map.has(key)) {
        console.log(`set() now ${key} exists in map`);
    }
    return retval;
};

/** 
 * @param {number} key
 * @return {number} value associated with key
 */
TimeLimitedCache.prototype.get = function(key) {
    console.log(`get() ${key}`);
    if (this.kv_ttl_map.has(key)) {
        console.log(`get() ${key} exists in map`);
        let now = new Date(); 
        [val, ctime, dur] = this.kv_ttl_map.get(key);
        console.log(`get() ${key} value is ${[val, ctime, dur]}, now is ${now},  elapsed time is ${(now-ctime)}`);
        if ((now-ctime) < dur) {
            console.log(`get() ${key} is valid, returning ${val}`);
            return  val;
        }
    } 
    return -1;
};

/** 
 * @return {number} count of non-expired keys
 */
TimeLimitedCache.prototype.count = function() {
    let count = 0;
    for (const [k,v] of this.kv_ttl_map) {
        let now = new Date(); 
        [val, ctime, dur] = this.kv_ttl_map.get(k);
        if ((now-ctime) < dur) {
            count++;
        }

    }
    return count;
};
