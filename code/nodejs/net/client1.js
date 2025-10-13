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


let hrstart = process.hrtime();
const clients = net.connect({port: 2222}, () => {

    // 'connect' listener
    console.log('connected to server!');
    //clients.write('world!\r\n');

    hrstart = process.hrtime();
    ////send non binary
    clients.write(filedata+'\n\n\n');

    //send non binary 
    msg_len = Buffer.byteLength(filedata+3);
    
    ////send binary
    ////send_buf = Buffer.from(filedata, "utf-8");
    //send_buf = new Buffer( 4 + msg_len);
    //send_buf.writeUInt32BE(msg_len, 0);
    //send_buf.write(filedata+'\n\n\n', 4); 
    //console.log('sending data to server!');
    //clients.write(send_buf);
    
    console.log('data sent to server!');
});

//on data read from server
clients.on('data', (data) => {
  console.log('got data: %s\n', data.toString());
  
  hrend = process.hrtime(hrstart);
  console.log(`total time for full qky exposure_report is ${hrend[0]}sec, ${hrend[1]/1000000}ms`);

  //clients.write(filedata);
  clients.end();
});

//on tcp fin
clients.on('end', () => {
  console.log('disconnected from server');
});
