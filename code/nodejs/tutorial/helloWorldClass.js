class HelloWorld{
    constructor(msg){
            this.msg = msg;
    }

    printHelloWorld()
        {
                console.log(this.msg);
                return this.msg;
        }
}

module.exports = new HelloWorld ("Hello World. This is a demo of basic nodejs");


