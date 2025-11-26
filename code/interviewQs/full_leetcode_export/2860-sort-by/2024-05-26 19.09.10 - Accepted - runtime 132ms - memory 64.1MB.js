var sortBy = function(arr, fn) {
    // cheese 
    // return arr.sort((a, b) => fn(a) - fn(b));

    // implement inplace quicksort of arr
    if (arr.length <= 1) {
        return arr;
    }

    const quicksort = (arr, left = 0, right = arr.length-1) => {
       if (left < right) {
        const pivotIndex = partition(arr, left, right);
        quicksort(arr, left, pivotIndex - 1);
        quicksort(arr, pivotIndex + 1, right);
       }
    }
    const partition = (arr, left, right) => {
        const pivot = arr[right];

        let i = left - 1;
        for (let j = left; j < right; j++) {
            if (fn(arr[j]) < fn(pivot)) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, right);
        return i + 1;
    } 

    function swap (arr, i, j) {
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }

    quicksort(arr);
    return arr;
};