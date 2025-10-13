console.log("Demo of js getters and setters");
const myobject = {
    innerPropertyPrivate: 0,
    get innerProperty() {
        console.log('intercepted get access to inner property'); 
        return this.innerPropertyPrivate;
    },
    set innerProperty(newval) {
        console.log('intercepted set access to inner property');
        this.innerPropertyPrivate = newval;
    }
}

console.log(myobject.innerProperty);
myobject.innerProperty = "hello setters";
console.log(myobject.innerProperty);

console.log("create a readonly propery by defining only getter");

const myro_object = {
    innerPropertyPrivate: 0,
    get innerProperty() {
        console.log('intercepted get access to inner readonly property '); 
        return this.innerPropertyPrivate;
    }
}
console.log(myro_object.innerProperty);

