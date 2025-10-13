// Initialize the Image Classifier method with MobileNet. A callback needs to be passed.
let classifier;

// A variable to hold the image we want to classify
let img;
let images = [];

document.getElementById("image").addEventListener("change", setup);

function preload() {
  console.log('Loading classifier');
  classifier = ml5.imageClassifier('MobileNet');
  img_bird = loadImage('images/bird.png');
  img_monkey = loadImage('images/imgbin-monkey.jpg');
  img_zebra = loadImage('images/Zebra.png');
  img_lion = loadImage('images/lion.png');
  img_whale = loadImage('images/whale.png');
  images.push(img_bird);
  images.push(img_monkey);
  images.push(img_zebra);
  images.push(img_lion);
  images.push(img_whale);
}

function setup() {
  removeElements();
  createCanvas(800, 800);
  chosenImg = document.getElementById("image").selectedIndex;

  console.log('Classifying image...');
  classifier.classify(images[chosenImg], gotResult);
  image(images[chosenImg], 0, 0);
}

// A function to run when we get any errors and the results
function gotResult(error, results) {
  // Display error in the console
  if (error) {
    console.error(error);
  } else {
    // The results are in an array ordered by confidence.
    console.log('classified label, confidence: ', results[0].label, results[0].confidence);
    createDiv(`Label: ${results[0].label}`);
    createDiv(`Confidence: ${nf(results[0].confidence, 0, 2)}`);
  }
}
