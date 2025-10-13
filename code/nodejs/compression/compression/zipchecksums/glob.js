const glob = require('glob'); // Import glob
const path = require("path");

const filePattern = '*.txt'; // Replace with your actual pattern

glob(filePattern, { cwd: path.resolve() }, (err, fileList) => {
  if (err) {
    console.error('Error finding files:', err);
    return;
  }

  console.log('Matching files:', fileList);
});

