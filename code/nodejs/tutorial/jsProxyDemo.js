//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy
// https://medium.com/dailyjs/how-to-use-javascript-proxies-for-fun-and-profit-365579d4a9f8
//

console.log('simple get proxy example.');

const wrapFunc = obj => {
        return new Proxy(obj, {
                get(target, propertyKey){
                        console.log(`trapped get call for "${propertyKey}"`);
                        return target[propertyKey];
                }
        });
}

const myobj = {msg: 'hello js proxy'};

const wrappedObj = wrapFunc(myobj);
console.log('accessing myobj getter. ', wrappedObj.msg);


//An SDK for an API with 20 lines of code
//As I said, you can intercept method calls for methods that… don’t even exist. When somebody calls a method on a proxied object the get handler will be called and then you can return a dynamically generated function. You don’t have to touch the proxied object if you don’t need to.
//
//With that idea in mind, you can parse the method being invoked and dynamically implement its functionality in runtime! For example we could have a proxy that when invoked with api.getUsers() it could make a GET /users in an API. With this convention we can go further and api.postItems({ name: ‘Item name' }) would call POST /items with the first parameter as request body.
console.log('get proxy that generates a function that selects http method and makes the call .');

const {METHODS} = require('http')

console.log('http methods: %s', JSON.stringify({METHODS}, null, 4));

const api = new Proxy({}, 
        {
                get(target, propertyKey){
                        const method = METHODS.find( method => 
                                propertyKey.startsWith(method.toLowerCase()))
                        if (!method) return;

                        const path = 
                                '/' +
                                propertyKey 
                                .substring(method.length) //remove method prefix
                                .replace(/([a-z])([A-Z])/g, '$1/$2') //getUser -> get/user
                                .replace(/\$/g, '/$/') // $ -> /$/
                                .toLowerCase()

                        return (...args) => {
                                const finalPath = path.replace(/\$/g, () => args.shift()) // /$/ -> /arg1/
                                const queryOrBody = args.shift() || {}
                                // You could use fetch here
                                // return fetch(finalPath, { method, body: queryOrBody })
                                console.log(method, finalPath, queryOrBody)
                        }
                }
        })


// GET /
api.get()
// GET /users
api.getUsers()
// GET /users/1234/likes
api.getUsers$Likes('1234')
// GET /users/1234/likes?page=2
api.getUsers$Likes('1234', { page: 2 })
// POST /items with body
api.postItems({ name: 'Item name' })
// api.foobar is not a function
api.foobar()
