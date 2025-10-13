const net = require('net')
const fs = require('fs')

const filename='exposure_report';
//const filename='businessapp.0212427E3EAE45D2A7648092A2F2FE88.json';

const filedata=fs.readFileSync(filename);
//NOTE:--> all the events of the socket are applicable here..in client...


// -----------------creating client using net.connect instead of custom socket-------

// server creation using net.connect --->
// u can also => write the below code in seperate js file
// open new node instance => and run it...


let times = 0;
let hrstart = process.hrtime();
const clients = net.connect({port: 2222}, () => {
 
  // 'connect' listener
  console.log('connected to server!');
  //clients.write('world!\r\n');
    
  hrstart = process.hrtime();
  clients.write(filedata + '\n\n\n');
    times++;
    
  //msg_len = Buffer.byteLength(filedata);
  //send_buf = Buffer.from(filedata, "utf-8");
  ////send_buf.write(filedata, 0);
  //clients.write(send_buf);
});

//on data read from server
clients.on('data', (data) => {
  console.log(data.toString());
  

  clients.write(filedata);
  times++;
  if (times === 500) {
      hrend = process.hrtime(hrstart);
      console.log(`total time for ${times} iterations is ${hrend[0]}sec, ${hrend[1]/1000000}ms`);
      clients.end();
  }
  //clients.end();
});

//on tcp fin
clients.on('end', () => {
  console.log('disconnected from server');
});
