var compactObject = function(obj) {

    function compactDFSRecursion(obj, newObj) {
        if (Array.isArray(obj)) {
            //console.log("handling as array, using newObj", newObj);
            // handle as array
            for (const val of obj) {
                //console.log("handling val", val);
                if (Boolean(val)) {
                    //console.log("handle non falsy val", val);
                    if (Array.isArray(val) ) {
                        //console.log("val type is array");
                        const compact_val = compactDFSRecursion(val, []);
                        //console.log("Adding to array compact val of type array ", compact_val);
                        newObj.push(compact_val);
                    } else if (typeof val === 'object') {
                        //console.log("val type is object");
                        const compact_val = compactDFSRecursion(val, {});
                        //console.log("Adding to array compact val of type object ", compact_val);
                        newObj.push(compact_val);
                    } else {
                        //console.log("Adding to array val", val);
                        newObj.push(val);
                    }
                }
            }
        } else if (typeof obj === 'object') {
            //handle as object
            //console.log("handling as object");
            for (const key in obj) {
                //console.log("handling key", key);
                if (Boolean(obj[key])) {
                    //console.log("handle non falsy key", key, "value", obj[key]);
                    if (Array.isArray(obj[key])) {
                        newObj[key] = compactDFSRecursion(obj[key], []);

                    } else if (typeof obj[key] === 'object'){
                        newObj[key] = compactDFSRecursion(obj[key], {});
                    } else {
                        newObj[key] = obj[key];
                    }
                }
            }
        }
        else {
            //console.log("Type is not an array or object")
        }
        return newObj;
    };

    if  (Array.isArray(obj)) {
        //console.log("Type is array", obj);
        return compactDFSRecursion(obj, []);
    } else if (typeof obj === 'object') {
        //console.log("Type is object", obj);
        return compactDFSRecursion(obj, {});
    }
};