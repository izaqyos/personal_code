const {exec} = require("child_process");

exec('ls', (err, stdout, stderr) => {
    console.log(stdout);
    console.log(stderr);
    if (err) {
        console.log(`encountered error ${err}`);
    }
});
