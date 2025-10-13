
// readResponseInChunks('https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json');
// readResponseInChunks('https://jsonplaceholder.typicode.com/photos');

async function goFetch(url) {
    const resp = await fetch(url);
    const data = await resp.json();
    return data;
}
const readData = await goFetch('https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json');
console.log(readData);
