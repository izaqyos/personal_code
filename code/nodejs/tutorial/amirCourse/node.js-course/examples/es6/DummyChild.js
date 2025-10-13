let { Dummy } = require('./Dummy');

const PREFIX = "DummyChild_";

class DummyChild extends Dummy {
    foo() {
        return PREFIX + super.foo();
    }
    boo() {
        return this.foo() + "_wooo";
    }
}

let d = new DummyChild();
console.log("d.foo() ->", d.foo()); // > d.foo() -> DummyChild_boo
console.log("d.boo() ->", d.boo()); // > d.boo() -> DummyChild_boo_wooo