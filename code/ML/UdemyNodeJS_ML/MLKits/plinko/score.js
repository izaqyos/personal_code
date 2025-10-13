const outputs = [];

function onScoreUpdate(dropPosition, bounciness, size, bucketLabel) {
  // Ran every time a balls drops into a bucket
  outputs.push([dropPosition, bounciness, size, bucketLabel]);

  // console.log(outputs);
}

//// single feature distance
//const dist = (point, predictionPoint) => Math.abs(point - predictionPoint);

// multi feature distance, euclydan/pythogroian distance 
// const dist = (features, prediction) => ( (features[0] - prediction[0])**2 + 
//   (features[1] - prediction[1])**2 +(features[2] - prediction[2])**2)**0.5;
// same using lodash
const dist = (pt1, pt2) => {
  _.chain(pt1)
    .zip(pt2)
    .map(([p1, p2]) => (p1 - p2) ** 2)
    .sum()
    .value() ** 0.5
};

function runAnalysis() {
  console.log('runAnalysis');



  //pre refactor
  // let correct = 0;
  // _.range(1, 15).forEach(k => {
  //   testSet.forEach(element => {
  //     const bucket = knn(trainSet, element[0], k);

  //     if (bucket === element[3]) correct++;
  //     console.log('Predicting ball dropped from %d to fall into bucket %d. actual bucket %d', element[0], bucket, element[3]);
  //   });
  //   console.log('correct %d times. accuracy %f', correct, correct / testSetSize);

  // })

  // //post refactor, but w/o feature selection
  // const testSetSize = 50;
  // const [testSet, trainSet] = splitDatasets(normalize(outputs, 3), testSetSize);
  // _.range(1, 20).forEach(k => { //k from 1 to 19
  //   const accuracy = _.chain(testSet)
  //     .filter(test => knn(trainSet, _.initial(test), k) === test[3])
  //     //.tap( x => console.log('#test w/ correct prediction %d, %s', x.length, JSON.stringify(x)))
  //     .size()
  //     .divide(testSetSize)
  //     .value();
  //   console.log('knn k=%d correct accuracy %f', k, accuracy);


  //with feature selection
  _.range(0, 3).forEach(featureIndex => {
    const testSetSize = 50;
    const dataSelectedFeature= outputs.map( r => [ r[featureIndex] , r[r.length-1]]);
    const [testSet, trainSet] = splitDatasets(normalize(dataSelectedFeature, 1), testSetSize);

    _.range(1, 20).forEach(k => { //k from 1 to 19
      const accuracy = _.chain(testSet)
        .filter(test => knn(trainSet, _.initial(test), k) === _.last(test))
        .size()
        .divide(testSetSize)
        .value();
      console.log('knn. feature=%d, k=%d, correct accuracy %f', featureIndex, k, accuracy); 
    }); 
  })
}

function knn(data, predictionPoint, k) {
      // KNN impl
      //console.log('knn data %s', JSON.stringify(data));
      //console.log('knn, predictionPoint=%s, k %d', predictionPoint, k);

      //predictionPoint has just features. no labels.
      return _.chain(data)
        .map(row => {
          return [dist(_.initial(row), predictionPoint),
          _.last(row)
          ] //produce array [distance, bucket]
        })
        .sortBy(row => row[0]) //sort by distance
        .slice(0, k) //take K neighbors
        .countBy(row => row[1]) //produce {bucket#: frequency} object
        .toPairs() //converts {k:v} obj to [[k1,v1],...[Kn,Vn]] array
        .sortBy(row => row[1]) // sort by frequency 
        .last() //take highest freq array [bucket, freq]
        .first() // bucket (as string since countBy converts to str)
        .parseInt() //convert to int
        .value(); //execute chain
    }

function splitDatasets(data, testCount) {
      const shuff = _.shuffle(data); //shuffle is required, otherwise we risk getting different localized data clusters 
      // in training vs. test sets (like training only has drop positions 0-200 and test 200-300)

      const testSet = _.slice(shuff, 0, testCount);
      const trainSet = _.slice(shuff, testCount);
      return [testSet, trainSet];
    }

function normalize(data, featuresCount) {
      const clonedData = _.cloneDeep(data);
      for (let i = 0; i < featuresCount; i++) {
        const clonedDataColumn = clonedData.map(row => row[i]);
        const min = _.min(clonedDataColumn);
        const max = _.max(clonedDataColumn);

        for (let j = 0; j < clonedData.length; j++) {
          clonedData[j][i] = (clonedData[j][i] - min) / (max - min);
        }
      }

      return clonedData;
    }
