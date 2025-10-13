function printmem() {
 let memprint='';
 memprint+='rss: '+process.memoryUsage().rss/(1024**2)+ 'MB\n';
 memprint+= 'heap total '+process.memoryUsage().heapTotal/(1024**2)+'MB\n';
 memprint+= 'heap used '+process.memoryUsage().heapUsed/(1024**2)+'MB\n';
 memprint+= 'external '+process.memoryUsage().exteral/(1024**2)+'MB\n';
 memprint+= 'buffers '+process.memoryUsage().arrayBuffers/(1024**2)+'MB\n';
 console.log(memprint);
 }
 printmem()
