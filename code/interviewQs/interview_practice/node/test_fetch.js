console.log("Demo modern fetch function (node 18+)")

async function testFetch() {
    try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon/ditto');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.log(error);
    }
}


async function myFetchTester_Unknown() {
    try {
        const resp = await fetch('https://pokeapi.co/api/v2/pokemon/unknown');
        if (resp.ok) {
            const data = await resp.json();
            console.log(data);
        } else {
            console.log(`Got error: ${resp.status}, msg: ${resp.statusText}`)
        }
    } catch (err) {
        console.log(err);
    }
}

function runTests() {

    testFetch();
    myFetchTester_Unknown();
}

runTests();