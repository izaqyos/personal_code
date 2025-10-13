//[i500695@C02X632CJGH6:2019-01-01 20:46:56:~/Desktop/work/code/nodejs/tutorial:]500$ node switchStringDemo.js
//process.env.REGION=undefined
//[i500695@C02X632CJGH6:2019-01-01 20:47:05:~/Desktop/work/code/nodejs/tutorial:]501$ export REGION=url
//[i500695@C02X632CJGH6:2019-01-01 20:47:21:~/Desktop/work/code/nodejs/tutorial:]502$ node switchStringDemo.js
//url detected. process.env.REGION=url
//[i500695@C02X632CJGH6:2019-01-01 20:47:23:~/Desktop/work/code/nodejs/tutorial:]503$ export REGION=json
//[i500695@C02X632CJGH6:2019-01-01 20:47:29:~/Desktop/work/code/nodejs/tutorial:]504$ node switchStringDemo.js
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
