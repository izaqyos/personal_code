const Coin = require('../models/Coin.model');
const express = require('express');
// const app = express();
const CoinRouter = express.Router();

CoinRouter.route('/create').get( (req, res) => {
    res.render('create');
});

CoinRouter.route('/').get( (req, res) => {
    // 1st step return index.html
    // res.render('index');

    // 2nd step, after mongo and model are ready return coins list 
    Coin.find(  (errs, coins) => {
        if (errs) {
            console.log(`error producing coins list: ${errs}`);
        }
        else {
        }
        res.render('index', {coins: coins}); //note, that index.ejs will display the coins
    }
    );
});

CoinRouter.route('/edit/:id').get( (req, res) => {
    const id = req.params.id; // extract query (path) param id.
    Coin.findById(id, (err, coin) => {
        res.render('edit', {coin: coin});
    });
});

CoinRouter.route('/').post( (req, res) => {
    Coin.find( (err, coins) => {
        if (err) {
            console.log(err);
        } else {
            res.render('index', {coins: coins});
        }
    }
    );
});

CoinRouter.route('/post').post( (req, res) => {
    console.log('/post got body ', JSON.stringify(req.body, null, 4));
    const coin = new Coin(req.body);
    console.log('/post got coin ', JSON.stringify(coin, null, 4));
    coin.save().then( coin => {
        res.redirect('/coins');
    }).catch( err => {
        const msg = `Failed to save coin to DB due to error: ${err}`
        res.status(400).send(msg);
    });
});

CoinRouter.route('/update/:id').post( (req, res) => {
    console.log('Trying to update coin with id', req.params.id);
    Coin.findById(req.params.id, (err, coin) => {
        if (!coin) {
            // return next(new Error('Failed to find coin for update'));
            res.status(403).send('Failed to find coin for update');
        }
        else {
            coin.name = req.body.name;
            coin.price = req.body.price;
            coin.save().then( coin => {
                res.redirect('/coins');
            }).catch( err => {
                res.status(400).send(`Failed to update DB for coin ${coin.name}`);
            });;
        }

    });
});

CoinRouter.route('/delete/:id').get(function (req, res) {
  Coin.findByIdAndRemove({_id: req.params.id},
       function(err, coin){
        if(err) res.json(err);
        else res.redirect('/coins');
    });
});

module.exports = CoinRouter;

