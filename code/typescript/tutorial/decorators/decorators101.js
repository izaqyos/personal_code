"use strict";
// based on https://fireship.io/lessons/ts-decorators-by-example/
//
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
var msg = "\nClass Decorator\nA class decorator makes it possible to intercept the constructor of class. They are called when the class is declared, not when a new instance is instantiated.\n\nSide note - one of the most powerful characteristics of a decoractor is its ability to reflect metadata, but the casual user will rarely need this feature. It is more suitable for use in frameworks, like the Angular Compiler for example, that need to to analyze the codebase to build the final app bundle.\n\nExample\nReal World Use Case: When a class is decorated you have to be careful with inheritence because its decendents will not inherit the decorators. Let\u2019s freeze the class to prevent inheritence completely\n\ncompile like this: $ tsc --target ES5 --experimentalDecorators decorators101.ts\n";
console.log(msg);
var IceCream = /** @class */ (function () {
    function IceCream() {
    }
    IceCream = __decorate([
        Frozen
    ], IceCream);
    return IceCream;
}());
function Frozen(constructor) {
    Object.freeze(constructor);
    Object.freeze(constructor.prototype);
}
console.log(Object.isFrozen(IceCream)); // true
// class FroYo extends IceCream {} // error, cannont be extended
// let froyo = new FroYo();
// would fail like this 
// /Users/i500695/work/code/typescript/tutorial/decorators/decorators101.js:13
//         function __() { this.constructor = d; }
//                                          ^
// 
// TypeError: Cannot assign to read only property 'constructor' of object '#<IceCream>'
//     at new __ (/Users/i500695/work/code/typescript/tutorial/decorators/decorators101.js:13:42)
//     at __extends (/Users/i500695/work/code/typescript/tutorial/decorators/decorators101.js:14:84)
//     at /Users/i500695/work/code/typescript/tutorial/decorators/decorators101.js:40:5
//     at Object.<anonymous> (/Users/i500695/work/code/typescript/tutorial/decorators/decorators101.js:45:2)
//     at Module._compile (internal/modules/cjs/loader.js:956:30)
//     at Object.Module._extensions..js (internal/modules/cjs/loader.js:973:10)
//     at Module.load (internal/modules/cjs/loader.js:812:32)
//     at Function.Module._load (internal/modules/cjs/loader.js:724:14)
//     at Function.Module.runMain (internal/modules/cjs/loader.js:1025:10)
//     at internal/main/run_main_module.js:17:11
var msg2 = "\nProperty Decorator\nAll of the examples in this guide use *Decorator Factories*. This just means the decorator itself is wrapped in a function so we can pass custom arguments to it, i.e @Cool('stuff') Feel free to omit the outer function if you want to apply a decorator without arguments @Cool .\nProperty decorators can be extremly useful because they can listen to state changes on a class. To fully understand the next example, it helps to be familar with JavaScript PropertyDescriptors.\n\nExample\nLet\u2019s override the flavor property to surround it in emojis. This allows us to set a regular string value, but run additional code on get/set as middleware, if you will.\n\n";
console.log(msg2);
var IceCreamComponent = /** @class */ (function () {
    function IceCreamComponent() {
        this.flavor = 'vanilla';
    }
    __decorate([
        Emoji()
    ], IceCreamComponent.prototype, "flavor", void 0);
    return IceCreamComponent;
}());
exports.IceCreamComponent = IceCreamComponent;
// Property Decorator
function Emoji() {
    return function (target, key) {
        var val = target[key];
        var getter = function () {
            console.log('Emoji getter called');
            return val;
        };
        var setter = function (next) {
            console.log('Emoji setter called');
            console.log('updating flavor...');
            val = "\uD83C\uDF66 " + next + " \uD83C\uDF66";
        };
        Object.defineProperty(target, key, {
            get: getter,
            set: setter,
            enumerable: true,
            configurable: true,
        });
    };
}
;
var flavor = new IceCreamComponent();
var flavor_get = flavor.flavor;
console.log("flavor by get " + flavor_get + " ");
flavor.flavor = 'coco';
console.log("flavor after set " + flavor.flavor + " ");
// will print 
// Emoji setter called
// updating flavor...
// Emoji getter called
// flavor by get 🍦 vanilla 🍦
// Emoji setter called
// updating flavor...
// Emoji getter called
// flavor after set 🍦 coco 🍦
var msg3 = "\nMethod Decorator\nMethod decoractors allow us override a method\u2019s function, change its control flow, and execute additional code before/after it runs.\n\nExample\nThe following decoractor will show a confirm message in the browser before executing the method. If the user clicks cancel, it will be bypassed. Notice how we have two decoractors stacked below - they will be applied from top to bottom.\n        ";
var IceCreamComponent2 = /** @class */ (function () {
    function IceCreamComponent2() {
        this.toppings = [];
    }
    IceCreamComponent2.prototype.addTopping = function (topping) {
        this.toppings.push(topping);
    };
    __decorate([
        Confirmable('Are you sure?'),
        Confirmable('Are you super, super sure? There is no going back!')
    ], IceCreamComponent2.prototype, "addTopping", null);
    return IceCreamComponent2;
}());
exports.IceCreamComponent2 = IceCreamComponent2;
// Method Decorator
function Confirmable(message) {
    console.log('in method factory');
    return function (target, key, descriptor) {
        console.log('in decorator function');
        var original = descriptor.value;
        descriptor.value = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            console.log('simulate allowed');
            var allow = 'yes';
            if (allow) {
                var result = original.apply(this, args);
                return result;
            }
            else {
                return null;
            }
        };
        return descriptor;
    };
}
var confirmIceCream = new IceCreamComponent2();
confirmIceCream.addTopping('vanilla');
