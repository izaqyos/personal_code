var express = require('express');
var db = require('../db');
var router = express.Router();

router.get('/', function(req, res, next) {
    db.singleQuery('SELECT * FROM Student')
        .then(function (result) {
            res.status(200).send(result.rows);
        }, next);
});

router.post('/', function (req, res, next) {
    db.singleQuery('INSERT INTO Student VALUES($1, $2, $3)',
        [req.body.id, req.body.name, req.body.rollnumber])

        .then(function (result) {
            res.status(200).send();
        }, next);
});

router.get('/:id', function (req, res, next) {
    db.singleQuery('SELECT * FROM Student WHERE id=$1', [req.params.id])
        .then(function (result) {
            res.status(200).send(result.rows[0]);
        }, next);
});

router.put('/:id', function (req, res, next) {
    db.singleQuery('UPDATE Student SET name=$2, rollnumber=$3 WHERE id=$1',
        [req.params.id, req.body.name, req.body.rollnumber])

        .then(function (result) {
            res.status(200).send();
        }, next);
});

router.delete('/:id', function (req, res, next) {
    db.singleQuery('DELETE FROM Student WHERE id=$1', [req.params.id])
        .then(function (result) {
            res.status(200).send(result.rows[0]);
        }, next);
});

module.exports = router;
