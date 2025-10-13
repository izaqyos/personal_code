let uuid = require('uuid/v1');
let uuidvalidate = require('uuid-validate');

module.exports=  () => {
        uuidv1 = uuid();
//console.log("Generated uuid: %s", uuidv1 );
        if (uuidvalidate(uuidv1)) {
                //console.log("it is a valid version %s uuid ", uuidvalidate.version(uuidv1));
        }
        else{
                //console.log("it is not valid");
        }
        return uuidv1;

};

let genUUIDv1 = module.exports;

uuid1 = genUUIDv1();
console.log(uuid1);
