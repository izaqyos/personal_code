const net = require('net')
const fs = require('fs')

//const filename='exposure_report';
const filename='businessapp.0212427E3EAE45D2A7648092A2F2FE88.json';

const filedata=fs.readFileSync(filename);
//NOTE:--> all the events of the socket are applicable here..in client...


// -----------------creating client using net.connect instead of custom socket-------

// server creation using net.connect --->
// u can also => write the below code in seperate js file
// open new node instance => and run it...


const clients = net.connect({port: 2222}, () => {
  // 'connect' listener
  console.log('connected to server!');
  //clients.write('world!\r\n');
  msg_len = Buffer.byteLength(filedata);
  send_buf = Buffer.from(filedata, "utf-8");
  //send_buf.write(filedata, 0);
  clients.write(send_buf);
});

//on data read from server
clients.on('data', (data) => {
  console.log(data.toString());
  clients.end();
});

//on tcp fin
clients.on('end', () => {
  console.log('disconnected from server');
});
