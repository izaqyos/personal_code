
class Shape {
    constructor (id, x, y) {
        this.id = id;
        this.move(x, y);
    }
    move (x, y) {
        this.x = x;
        this.y = y;
    }
}
// inheritance
class Circle extends Shape {
    constructor (id, x, y, radius) {
        super(id, x, y);
        this.radius = radius;
    }
}


///////// ES5 /////////

/*

    var Shape = function (id, x, y) {
        this.id = id;
        this.move(x, y);
    };
    Shape.prototype.move = function (x, y) {
        this.x = x;
        this.y = y;
    };

    // inheritance
    var Circle = function (id, x, y, radius) {
        Shape.call(this, id, x, y);
        this.radius = radius;
    };
    Circle.prototype = Object.create(Shape.prototype);
    Circle.prototype.constructor = Circle;

*/


// species pattern

class MyArray extends Array {
    // Overwrite species to the parent Array constructor
    static get [Symbol.species]() { return Array; }
}
let a = new MyArray(1,2,3);
console.log(a instanceof Array); // true
console.log(a instanceof MyArray); // true
console.log(Array.isArray(a));   // true

let mapped = a.map(x => x * x); // map() returns default constructor
console.log(mapped instanceof MyArray); // false
console.log(mapped instanceof Array);   // true