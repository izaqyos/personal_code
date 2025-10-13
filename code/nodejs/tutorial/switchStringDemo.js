//$ node switchStringDemo.js
//process.env.REGION=undefined
//$ export REGION=url
//$ node switchStringDemo.js
//url detected. process.env.REGION=url
//$ export REGION=json
//$ node switchStringDemo.js
//json detected. process.env.REGION=json     
let region = process.env.REGION;

switch (region){

        case "url":
                console.log("url detected. process.env.REGION=%s",region);
                break;
        case "json":
                console.log("json detected. process.env.REGION=%s",region);
                break;
        default:
                console.log("process.env.REGION=%s",region);
                break;

}
