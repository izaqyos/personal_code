
// based on https://fireship.io/lessons/ts-decorators-by-example/
//

const msg = `
Class Decorator
A class decorator makes it possible to intercept the constructor of class. They are called when the class is declared, not when a new instance is instantiated.

Side note - one of the most powerful characteristics of a decoractor is its ability to reflect metadata, but the casual user will rarely need this feature. It is more suitable for use in frameworks, like the Angular Compiler for example, that need to to analyze the codebase to build the final app bundle.

Example
Real World Use Case: When a class is decorated you have to be careful with inheritence because its decendents will not inherit the decorators. Let’s freeze the class to prevent inheritence completely

compile like this: $ tsc --target ES5 --experimentalDecorators decorators101.ts
`;
console.log(msg);
@Frozen
class IceCream {}

function Frozen(constructor: Function) {
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

const msg2 = `
Property Decorator
All of the examples in this guide use *Decorator Factories*. This just means the decorator itself is wrapped in a function so we can pass custom arguments to it, i.e @Cool('stuff') Feel free to omit the outer function if you want to apply a decorator without arguments @Cool .
Property decorators can be extremly useful because they can listen to state changes on a class. To fully understand the next example, it helps to be familar with JavaScript PropertyDescriptors.

Example
Let’s override the flavor property to surround it in emojis. This allows us to set a regular string value, but run additional code on get/set as middleware, if you will.

`;

console.log(msg2);
export class IceCreamComponent {
  @Emoji()
  flavor = 'vanilla';
}


// Property Decorator
function Emoji() {
  return function(target: Object, key: string | symbol) {

    let val = target[key];

    const getter = () =>  {
        console.log('Emoji getter called');
        return val;
    };
    const setter = (next) => {
        console.log('Emoji setter called');
        console.log('updating flavor...');
        val = `🍦 ${next} 🍦`;
    };

    Object.defineProperty(target, key, {
      get: getter,
      set: setter,
      enumerable: true,
      configurable: true,
    });

  };
};

const flavor = new IceCreamComponent();
const flavor_get = flavor.flavor;
console.log(`flavor by get ${flavor_get} `);
flavor.flavor = 'coco';
console.log(`flavor after set ${flavor.flavor} `);
// will print 
// Emoji setter called
// updating flavor...
// Emoji getter called
// flavor by get 🍦 vanilla 🍦
// Emoji setter called
// updating flavor...
// Emoji getter called
// flavor after set 🍦 coco 🍦

const msg3 = `
Method Decorator
Method decoractors allow us override a method’s function, change its control flow, and execute additional code before/after it runs.

Example
The following decoractor will show a confirm message in the browser before executing the method. If the user clicks cancel, it will be bypassed. Notice how we have two decoractors stacked below - they will be applied from top to bottom.
        `;

export class IceCreamComponent2 {

  toppings = [];

  @Confirmable('Are you sure?')
  @Confirmable('Are you super, super sure? There is no going back!')
  addTopping(topping) {
    this.toppings.push(topping);
  }

}


// Method Decorator
function Confirmable(message: string) {
  console.log('in method factory');
  return function (target: Object, key: string | symbol, descriptor: PropertyDescriptor) {
    console.log('in decorator function');
    const original = descriptor.value;

      descriptor.value = function( ... args: any[]) {
          console.log('simulate allowed');
          const allow = 'yes';

          if (allow) {
            const result = original.apply(this, args);
            return result;
          } else {
            return null;
          }
    };

    return descriptor;
  };
}

const confirmIceCream = new IceCreamComponent2();
confirmIceCream.addTopping('vanilla');
