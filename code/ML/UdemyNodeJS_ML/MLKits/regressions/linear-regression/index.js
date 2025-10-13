require('@tensorflow/tfjs-node'); //CPU tf, GPU only supported on linux
const tf = require('@tensorflow/tfjs'); //tensor flow node lib
const linearReg = require('./linear-regression');
const plot = require('node-remote-plot');

const loadCSV = require('../load-csv'); 
 const LinearRegression = require('./linear-regression');

let {features, labels, testFeatures, testLabels } = loadCSV('../data/cars.csv', {
    shuffle: true,
    splitTest: 50,
    dataColumns: ['horsepower', 'weight','displacement'],
    labelColumns: ['mpg']
});

console.log(features, labels);

const regression = new LinearRegression(features, labels, {
    learningRate: 0.1,
    iterations: 3, // for full regression (non batch) we require more iterations. around 100.
    batchSize: 10, // 1 - stochastic, >1 batch
});

regression.train();
const r2 = regression.test(testFeatures, testLabels);

// console.log('m: ', regression.m);
// console.log('b: ', regression.b);

//console.log('m: ', regression.weights.get(1,0));
//console.log('b: ',  regression.weights.get(0,0));

// //Plot MSEs
// plot({
//     x: regression.mses.reverse(),
//     xLabel: 'iteration #',
//     yLabel: 'Mean Square Root Error'
// });

//Plot MSEs vs b values
plot({
    x: regression.bhistory,
    y: regression.mses.reverse(),
    xLabel: 'Value of B',
    yLabel: 'Mean Square Root Error'
});

plot({
  x: regression.mses.reverse(),
  xLabel: 'Iteration #',
  yLabel: 'Mean Squared Error'
});

console.log('mses history', regression.mses);
console.log('r2', r2);

const predictions_tf = regression.predict([
    //horsepower, mpg, displacement. Order is very important!!
        [120, 2, 380],
    ]);
predictions_tf.print();
// console.log('test assignment');
// const ones = tf.ones([3,1]);
// console.log('ones ');
// ones.print();
// const onescp = ones;
// console.log('ones copy ');
// onescp.print();
