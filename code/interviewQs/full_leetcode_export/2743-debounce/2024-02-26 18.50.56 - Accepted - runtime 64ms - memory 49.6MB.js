var debounce = function(fn, t) {

    console.log("debounce called");
    let timeStarted = undefined;
    let timer = undefined;
    let executed = false;

    return function(...args) {
        //console.log(`debounce generated function called with fn=${fn}, t=${t}`); 

        if (timer && !executed) {
            const ctime = new Date();
            console.log(`debounce generated function called after ${ctime-timeStarted} millisecond, debounce time ${t}  `);
            if (ctime-timeStarted < t) {
                console.log("cancel timer");
                //cancel timer
                clearTimeout(timer);

                //reschedule timeout
                executed = false;
                timer = setTimeout( () => { executed = true; fn(...args)}, t);
                timeStarted = new Date(); 
                //console.log(`debounce generated function setting TO callback at ${timeStarted}, delay ${t} `);
            } // else do nothing, let timer keep running
        } else {
            console.log(`debounce generated function called first time, executed=${executed}, timer=${timer}`);
            executed = false;
            timer = setTimeout(() => { executed = true; fn(...args)}, t);
            timeStarted = new Date(); 
            //console.log(`debounce generated function setting TO callback at ${timeStarted}, delay ${t} `);
        }
    }
};
