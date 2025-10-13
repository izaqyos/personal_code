const inventory = [
  { name: 'MacBook Pro', category: 'Electronics', price: 2500 },
  { name: 'Wireless Mouse', category: 'Electronics', price: 75 },
  { name: 'T-Shirt', category: 'Apparel', price: 25 },
  { name: 'Jeans', category: 'Apparel', price: 80 },
  { name: 'Node.js Explained', category: 'Books', price: 40 },
  { name: 'Coffee Mug', category: 'Kitchenware', price: 15 },
  { name: 'Mechanical Keyboard', category: 'Electronics', price: 200 }
];


const groupedByReduce = inventory.reduce((accumulator, product) => {
  const key = product.category;
  if (!accumulator[key]) {
    accumulator[key] = [];
  }
  accumulator[key].push(product);
  return accumulator;
}, {}); 
console.log('--- Grouped with reduce, more cumbersome syntax: ---');
console.log(groupedByReduce);

const groupedByObject = Object.groupBy(inventory, product => product.category);
console.log('\n--- Grouped with Object.groupBy: ---');
console.log(groupedByObject);
console.log('Prototype of result:', Object.getPrototypeOf(groupedByObject)); 

console.log('--- Iterating with Object.entries() ---');

for (const [category, products] of Object.entries(groupedByObject)) {
  console.log(`Category: ${category}`);
  // 'products' is the array of items for that category
  products.forEach(product => {
    console.log(`  - ${product.name} ($${product.price})`);
  });
}
