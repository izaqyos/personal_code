const obj = {
    oldItems: [
        {
            id: "ab2341ba",
            title: "My Item",
        }
    ],
    newItems: [
        {
            id: "cc4423aa",
            title: "My New Item",
        }
    ],
    id: "dc1462a7",
    count: 3
};

const process = (myObj) => {
    // TODO:
    // return an object with changes:
    //  - merge data.newItems with data.oldItems
    //  - put merged array in new property called "items"
};

console.log("before:", obj);
const afterProcess = process(obj);
console.log("after:", afterProcess);