let n = 1;
gotosearch: while (true) {
    n+=1;
    for (let index = 2; index <= Math.sqrt(n); index++){
       if (n%index == 0) {
           continue gotosearch;
       } 
       postMessage(n);
    }
}