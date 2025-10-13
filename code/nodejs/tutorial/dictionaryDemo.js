//ES5 JS

var dict = {};

var func1 = function(){
        console.log('func1 called');
}

var func2 = function(){
        console.log('func2 called');
}

//function as value
dict['func1'] = func1;
dict['func2'] = func2;

//function as key
dict[func1] = 'This is func1 value';
dict[func2] = 'This is func2 value';

Object.keys(dict).forEach(function (key, index){
        console.log('dictionary key ', key);
        console.log('dictionary index ', index);
        console.log('dictionary value ', dict[key]);
        if (typeof dict[key] === 'function'){
                console.log('encounter a function value. running it');
                dict[key]();
        }
});
