var buf = new Buffer(10); 
console.log("buf= ",buf);


var buf1 = new Buffer([1,2,3,4]); 
console.log("buf1= ",buf1);

var buf2 = new Buffer(256); 
wlen = buf2.write("writing to buffer");
console.log("wrote "+wlen+" bytes to buf2. content(hex)= ",buf2);
console.log("readable content= "+buf2.toString('utf8',0, wlen));

buf = new Buffer(26);
for (var i = 0 ; i < 26 ; i++) {
  buf[i] = i + 97;
}

console.log( buf.toString('ascii'));       // outputs: abcdefghijklmnopqrstuvwxyz
console.log( buf.toString('ascii',0,5));   // outputs: abcde
console.log( buf.toString('utf8',0,5));    // outputs: abcde
console.log( buf.toString(undefined,0,5)); // encoding defaults to 'utf8', outputs abcde




var buf = new Buffer('Simply Easy Learning');
var json = buf.toJSON(buf);

console.log(json);


var buffer1 = new Buffer('TutorialsPoint ');
var buffer2 = new Buffer('Simply Easy Learning');
var buffer3 = Buffer.concat([buffer1,buffer2]);
console.log("buffer3 content: " + buffer3.toString());

var buffera = new Buffer('ABC');
var bufferb = new Buffer('ABCD');
var result = buffera.compare(buffer2);

if(result < 0) {
   console.log(buffera +" comes before " + bufferb);
}else if(result == 0){
   console.log(buffera +" is same as " + bufferb);
}else {
   console.log(buffera +" comes after " + bufferb);
}

var bufferc = new Buffer('ABC');

//copy a buffer
var bufferd = new Buffer(3);
bufferc.copy(bufferd);
console.log("bufferd content: " + bufferd.toString());

var buffere = new Buffer('TutorialsPoint');

//slicing a buffer
var bufferf = bufferd.slice(0,9);
console.log("bufferf content: " + bufferf.toString());


var bufferg = new Buffer('TutorialsPoint');

//length of the buffer
console.log("buffer length: " + bufferg.length);


