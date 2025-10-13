
function someFunc(iterationNum){
        console.log('someFunc iteration # ', iterationNum);
}

const limit=100000;

////no problem here, all function calls fire after this TO expires
//for(i=0; i<limit; i++){
//    setTimeout(someFunc, 1000, i);
//}

for(i=0; i<limit; i++){
    setTimeout(someFunc, 1000+i*1, i);
}


