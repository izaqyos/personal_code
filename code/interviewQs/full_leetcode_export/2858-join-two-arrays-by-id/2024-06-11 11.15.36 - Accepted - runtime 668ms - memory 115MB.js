var join = function (arr1, arr2) {
  const ret = new Map(); //map id to merged object
  const arr1map = arr1.reduce((map, obj) => {
    const { id, ...rest } = obj;
    map.set(id, rest);
    return map;
  }, new Map());
  const arr2map = arr2.reduce((map, obj) => {
    const { id, ...rest } = obj;
    map.set(id, rest);
    return map;
  }, new Map());

  for (let i = 0; i < arr1.length; i++) {
    // only arr1 has it so push all it's array
    if (!arr2map.has(arr1[i].id)) {
      ret.set(arr1[i].id, arr1[i]);
      //console.log(
      //  `id ${arr1[i].id} exists in array arr1 only, setting ret map at id ${arr1[i].id} to ${arr1[i]} `
      //);
    } else {

      ret.set(arr1[i].id, {});
      for (const key in arr1[i]) {
        //console.log(
        //  `id ${
        //    arr1[i].id
        //  } exists in both array, merging from arr1 key ${key} with value ${JSON.stringify(
        //    arr1[i][key],
        //    null,
        //    4
        //  )} `
        //);
        ret.get(arr1[i].id)[key] = arr1[i][key];
        //console.log(ret);
      }

    }
  }
  // console.log("merged map after processing arr1");
  // console.log(ret);

  // now process arr2
  for (let i = 0; i < arr2.length; i++) {
    if (!arr1map.has(arr2[i].id)) {
      ret.set(arr2[i].id, arr2[i]);
    } else {
      for (const key in arr2[i]) {
        ret.get(arr2[i].id)[key] = arr2[i][key];
      }
    }
  }

  ret_as_array = Array.from(ret.values());
  return ret_as_array.sort((a, b) => a.id - b.id);
};