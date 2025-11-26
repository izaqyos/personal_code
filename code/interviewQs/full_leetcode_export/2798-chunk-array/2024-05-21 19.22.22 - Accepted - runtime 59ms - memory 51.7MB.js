/**
 * @param {Array} arr
 * @param {number} size
 * @return {Array}
 */
var chunk = function(arr, size) {
    const ret = []
    let chunk = [];
    for (let index = 0; index < arr.length; index++) {
        if (chunk.length < size) {
            chunk.push(arr[index]);
        } else {
            ret.push(chunk);
            chunk = [arr[index]];
        }
    }
    if (chunk.length > 0) {
        ret.push(chunk);
    }
    return ret;
};