module.exports = function (app) {
    app.use('/', require('./index-route'));
    app.use('/users', require('./users'));
    app.use('/students', require('./students'));
};
