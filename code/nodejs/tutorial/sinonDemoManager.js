user = require('./sinonDemo.js');

class Manager{
        constructor(name){
                this.name =name;
        }

        hireNewEmployee( user)
        {
            console.log("hireNewEmployee()");
            user.callSetThenGetName();
        }
}

module.exports = Manager ;
