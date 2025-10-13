
console.log('ES6 Map TS demo')
console.log('Map is similar to Object. but they are not the same. Map supports any type key, iteration, size, and is more optimized')
console.log('Careful not to use Map as Object. so use has/get/set, not [] !!')
let contacts = new Map()
contacts.set('Jessie', {phone: "213-555-1234", address: "123 N 1st Ave"})
contacts.has('Jessie') // true
contacts.get('Hilary') // undefined
contacts.set('Hilary', {phone: "617-555-4321", address: "321 S 2nd St"})
contacts.get('Jessie') // {phone: "213-555-1234", address: "123 N 1st Ave"}
contacts.delete('Raymond') // false
contacts.delete('Jessie') // true
console.log(contacts.size) // 1


console.log('Using a map...')
let aMap = new Map();
let Kstr = 'key string';
let Kobj = {};
let KFunc = function() {};

aMap.set(Kstr, 'str key value');
aMap.set(Kobj, 'Object key value');
aMap.set(KFunc, 'Function key value');

console.log('size', aMap.size);

console.log(aMap.get(Kstr));
console.log(aMap.get(Kobj));
console.log(aMap.get(KFunc));
aMap.get('a string')    // "value associated with 'a string'"
// because keyString === 'a string'
aMap.get({})            // undefined, because keyObj !== {}
aMap.get(function() {}) // undefined, because keyFunc !== function () {}


console.log('Use enum type as map key');
enum colors {
    red = 'red',
    green = 'green',
    blue = 'blue',
}

let colorsMap: Map<colors, number> = new Map<colors, number>();
colorsMap.set(colors.red, 2);
// colorsMap.set('green', 3); // will fail, Argument of type '"green"' is not assignable to parameter of type 'colors'
console.log('colors: ', colorsMap);

let deepMap: Map<string, Map<string, string>> = new Map<string, Map<string, string>>();
let submap1: Map<string, string> = new Map<string, string>();
submap1.set('k1', 'v1');
deepMap.set('submap1', submap1);
console.log('deep map print: ', deepMap);

