var example = /** @class */ (function () {
    function example(a, b) {
        this.a = a;
        this.b = b;
    }
    return example;
}());
var ex = new example('class', ' to json');
console.log(JSON.stringify(ex, null, 4));
