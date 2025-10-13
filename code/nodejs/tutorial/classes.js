class DemoClass{

        constructor(name){
                this.name = name;
        }

        printMe(){
                console.log("name is %s",this.name);
                console.log("undefined member: %s", this.undef);
                if (!this.undef) {
                        console.log("this.undef is undefined");
                }
                else{
                        console.log("this.undef is defined");
                }
        }
}

function test1(){
    demoC = new DemoClass('demo');
    demoC.printMe();
}

test1()
