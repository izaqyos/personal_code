console.log("Demo of nodejs globals");

console.log(" __filename = ", __filename);
console.log(" __dirname = ", __dirname);
console.log(" platform+arch = ", process.platform, process.arch);
console.log(" pid = ", process.pid);
console.log(" title = ", process.title);


console.log("setTimeout(cb,ms) triggers cb after ms...");

function echoMsg (argument) {
    console.log(argument.toString());
}

var to = setTimeout(echoMsg, 2000, "printed after 2 seconds");
var to1 = setTimeout(echoMsg, 2000, "printed after 2 seconds");

clearTimeout(to1);

setInterval(echoMsg, 1000, "Print after one second");

