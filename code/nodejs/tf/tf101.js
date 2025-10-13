const tf = require('@tensorflow/tfjs-node');

const t1 = tf.tensor([
    [1,2,3],
    [5,9,30],
    [1,2,3],
    [5,9,30]
]);
const t2 = tf.tensor([
    [4,8],
    [4,8],
    [4,8],
    [4,8] 
]);

console.log('t1');
t1.print();
console.log('sum of t1');
t1.sum().print();
console.log('sum of t1 along column axis ');
t1.sum(1).print();
console.log('sum of t1 along rows axis ');
t1.sum(0).print();
console.log('sum of t1 along column axis, keep orig rank ');
t1.sum(1,true).print();

// Error: Error in concat1D: rank of tensors[1] must be the same as the rank of the rest (1). 
// b/c try 2 concate 1 dim (sum) to 2 dim
//t1.sum(1).concat(t2).print();
console.log('t1 shape ',t1.shape);
console.log('t2 shape ',t2.shape);
//2 ways 2 solve. 1st. tell sum to preserve original dimensions and concat along y axis
t1.sum(1,true).concat(t2, 1).print();
//2nd way. better. expand dims to add y axis dim. 
console.log('t1 y axis sum before expand dim');
t1.sum(1).print();
console.log('t1 y axis sum after expand dim');
t1.sum(1).expandDims(1).print();
console.log('t1 y axis sum concat w/ t2 along y axis');
t1.sum(1).expandDims(1).concat(t2,1).print();