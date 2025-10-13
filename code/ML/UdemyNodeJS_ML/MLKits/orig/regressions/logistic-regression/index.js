require('@tensorflow/tfjs-node');
const tf = require('@tensorflow/tfjs');
const loadCSV = require('../load-csv');
const LogisticRegression = require('./logistic-regression');

let { features, labels, testFeatures, testLabels } = loadCSV('../data/cars.csv', {
  shuffle: true,
  splitTest: 50, // 50 rows for tests
  dataColumns: ['horsepower', 'displacement', 'weight'],
  labelColumns: ['passedemissions'],
  converters: {
      passedemissions: val => { // each value of passedemissions column is passed to the labda. which performs labed encoding
      return val === 'TRUE' ? 1 : 0 // TRUE string to 1, else 0 
    }
  }
});

const regression = new LogisticRegression(features, labels, {
    learningRate: 0.5,
    iterations: 100,
    batchSize: 50,
    decisionBoundary: 0.6
});
regression.train();

console.log('Predict a car we know has failed and a car that passed...');
regression.predict([
    [130, 307, 1.75],
    [88, 97, 1.065],
]).print();
console.log('note 0.23 and 0.94 values. means 23%,94% chance to pass test. If we set descion boundry to 0.5 thats one fail and one pass');

console.log('tested accuracy', regression.test(testFeatures, testLabels));
// console.log(labels); // verify labels are encoded

