var express = require('express');
var router = express.Router();

// middleware that is specific to this router
router.use(function timeLog (req, res, next) {
    console.log('Time: ', Date.now());
    next()
});
// define the home route
// /admin/
router.get('/', function (req, res) {
    res.send('admin home')
});
// define the profile route
// /admin/profile
router.get('/profile', function (req, res) {
    res.send('admin profile');
});

router.use('/watchers', require('./watchers-router'));

module.exports = router;



