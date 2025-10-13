const url = 'https://jsonplaceholder.typicode.com/todos/1'
export async function getJsonFromUrl(url){
    console.log(`GET from ${url}`);
    const resp = await fetch(url);
    if (resp.ok) {
        const jsonData = await resp.json();
        console.log(`Got json ${JSON.stringify(jsonData, null, 4)} from ${url}`);
        //console.log(`Got json ${JSON.stringify(jsonData, null, ' ')} from ${url}`);
        //console.log(`Got json ${JSON.stringify(jsonData, null, "\t")} from ${url}`);
        return jsonData;
    }
    else {
        console.error(`Got error ${resp.status} ${resp.statusText}`);
        throw new Error(`Got error ${resp.status} ${resp.statusText}`);
    }
}


getJsonFromUrl(url);
// module.exports={ getJsonFromUrl};

