//async  function f(){
//        return 1;
//}

//f().then( res => console.log("promise returned %s", res));
//console.log("waiting on async promise. val=%s", f().then());
//
//
function createPromise(){
  return new Promise((resolve, reject) => {
    setTimeout(() => resolve("done!"), 1000)
  });
}

async function f1() {

        let result;
        try{
  result = await createPromise(); // wait till the promise resolves (*), await can only be used in an async function. Its better than using .then() w/ success function
        }
        catch (err){
                console.log("promise rejected %s",err);
        }

  console.log("result=%s", result); // "done!"
        return result;
}

async function f2() {
    return 2;
}

async function f3() {
    console.log(f2());  
    console.log(await f2());  
}

console.log("1");
f3();
f1().then(res => console.log("res=%s",res));

