Array.prototype.groupBy = function(fn) {
    let ret = {};
    for (let index = 0; index < this.length; index++) {
        let key = fn(this[index]);
        if (ret[key] === undefined) {
            ret[key] = [];
        }
        ret[key].push(this[index]);
    }
    return ret;
};