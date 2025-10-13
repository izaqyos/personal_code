module.exports = (val) => {
    return new Promise((resolve) => {
        setTimeout(() => resolve(val));
    })
};