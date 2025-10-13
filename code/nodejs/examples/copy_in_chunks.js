function copyInChunks(sourceArr, targetArr, chunkSize) {
  let startIndex = 0;
  while (startIndex < sourceArr.length) {
    const chunk = sourceArr.slice(startIndex, startIndex + chunkSize);
    targetArr.push(...chunk); // Spread operator for efficient element addition
    startIndex += chunkSize;
  }
}

const sourceArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const targetArr = [];
const chunkSize = 3;

copyInChunks(sourceArr, targetArr, chunkSize);
console.log(targetArr); // Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

