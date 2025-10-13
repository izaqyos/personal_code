class User{

        constructor (fname, lname){
                this.fname = fname;
                this.lname = lname;
        }

        getName()
        {
                return this.fname +" "+this.lname;
        }

        sleep(ms){
                return new Promise(resolve => setTimeout(resolve,ms));
        }

        async saveToDB()
        {
                console.log("sleeping...");
                await this.sleep(2000);
                console.log("woke up 2 sec later");
        }

        setName(fname,lname){
                this.fname = fname;
                this.lname = lname;
        }

        callSetThenGetName(){
                console.log("callSetThenGetName()");
                this.setName(this.fname, this.lname);
                this.saveToDB();
                this.getName();
        }
}


//module.exports = new User ("yosi","izaq");
module.exports = User ;

var sinon = require('sinon');
let user = new User("yosi","izaq");
var getNameSpy =  sinon.spy(user,"getName");

var i;
for (i=0;i<10;i++) user.getName();
console.log("user.getName() called %s times", getNameSpy.callCount);
//calling restore removes the spy. this is very important.
getNameSpy.restore();

user.saveToDB();

