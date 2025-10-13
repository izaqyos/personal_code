require('@tensorflow/tfjs-node'); //CPU tf, GPU only supported on linux
const tf = require('@tensorflow/tfjs'); //tensor flow node lib

const loadCSV = require('./load-csv');

function knn(features, labels, predPoint, k)  {
    //use moments to get statistics of tensor. 0 to take along X axis
    const {mean, variance} = tf.moments(features, 0); 

    const scaledPrediction = predPoint.sub(mean).div(variance.pow(0.5));

    return features
    .sub(mean)              // scale
    .div(variance.pow(0.5)) // to std deviation
    .sub(scaledPrediction) // [ [/\X , /\Y] , [], ..., ]
    .pow(2) // [... [ /\X^2 , /\Y^2  ] ]
    .sum(1) // sum on y axis 
    .pow(0.5) //  (/\X^2 + /\Y^2) )^0.5  , pythogrian distance
    .expandDims(1) // we need 2 concat with labels which is 2d #labels,1 ranks. so we change [#features] shape
    // to [#features,1] shape
    .concat( labels, 1) // concat on y axis
    .unstack() // convert the tensor to array of arrays for sorting
    .sort( (a,b) => a.get(0) > b.get(0) ? 1 : -1 ) // a/b[0] - distance
    .slice(0,k) // top k
    .reduce( (acc, elem) => acc + elem.get(1) , 0) / k // use reduce 2 calc sum then average
    
}
let {features, labels, testFeatures, testLabels } = loadCSV('kc_house_data.csv', {
    shuffle: true,
    splitTest: 10,
    dataColumns: ['lat', 'long',, 'sqft_living', 'sqft_lot'],
    labelColumns: ['price']

});

// console.log(testFeatures);
// console.log(testLabels);

//convert to tensors
features = tf.tensor(features)
labels = tf.tensor(labels)

testFeatures.forEach( (element, i) => {
const result = knn( features, labels, tf.tensor(element), 10)
console.log('guess ', i, result, testLabels[i][0]); 
const err =  ((result - testLabels[i][0]) / testLabels[i][0])*(-100);
console.log('error ', i, err);
});