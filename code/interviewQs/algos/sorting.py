def heapsort(arr):
    """
    returns arr sorted list
    """
    import heapq
    hq = []
    for n in arr:
        heapq.heappush(hq, n)

    return [heapq.heappop(hq) for _ in arr ]

def qsort_partition(arr, l, h):
    if l<h:
        pivot = arr[h]
        lower_than_index = l
        for j in range(l,h):
            if arr[j] < pivot:
                arr[lower_than_index], arr[j] = arr[j], arr[lower_than_index]
                lower_than_index+=1

        arr[h], arr[lower_than_index] = arr[lower_than_index], arr[h]
        return lower_than_index

def qsortutil(arr, l, h):
    if l<h:
        partitionIndex = qsort_partition(arr, l, h)
        qsortutil(arr, l, partitionIndex-1)
        qsortutil(arr, partitionIndex+1,h)

def qsort(arr):
    qsortutil(arr, 0, len(arr)-1)

def merge(arr1, arr2): #merge 2 sorted arrays into one
    i,j = 0,0
    m,n = len(arr1), len(arr2)
    ret = []
    while i<m and j<n:
        if arr1[i] < arr2[j]:
            ret.append(arr1[i]) 
            i+=1
        else:
            ret.append(arr2[j]) 
            j+=1

    while j<n:
        ret.append(arr2[j])
        j+=1 
    while i<m:
        ret.append(arr1[i])
        i+=1
    return ret


def mergesortR(arr, l, h):
    if  l<=h:
        if h == l:
            return [arr[h]]
        elif h == l+1:
            if arr[h] < arr[l]:
                arr[h], arr[l] = arr[l], arr[h] 
            return arr[l:h+1]
        else:
            L = mergesortR(arr, l, (l+h)//2)
            H = mergesortR(arr, (l+h)//2 +1, h)
            R = merge(L,H)
            return R
    else:
        return [] 

def mergesort(arr):
    return mergesortR(arr, 0, len(arr)-1)

# practice
def nativeSort(arr):
    ret = arr[:]
    ret.sort()
    return ret

def heapsort1(arr):
    import heapq
    h = []
    for n in arr:
        heapq.heappush(h,n)
    return [heapq.heappop(h) for _ in arr]

def qsort(arr):
    def partition(arr, l, h):
        if l<h:
            pivot = arr[h]
            lower_than_index = l
            for i in range(l,h):
                if arr[i]<pivot:
                    arr[lower_than_index], arr[i] = arr[i],arr[lower_than_index] 
                    lower_than_index +=1
            arr[h], arr[lower_than_index] = arr[lower_than_index],arr[h] 
            return lower_than_index

    def qsortutil(arr, l, h):
        if l<h:
            partitionIndex = partition(arr, l , h)
            qsortutil(arr,l, partitionIndex-1) 
            qsortutil(arr,partitionIndex+1, h) 

    return qsortutil(arr, 0 , len(arr)-1)


# practice
def test():
    inputs = [
        [5,3,1,2],
        [15,34,14,2, 0 , 10]
    ]
    expected = [
        [1,2,3,5],
        [0, 2, 10 , 14, 15,34] 
    ]

    for inp, exp in zip(inputs, expected):
        hsorted = heapsort(inp)
        print('heapsort {} -> {}'.format( inp, hsorted))
        inpcpy = inp[:]
        qsort(inpcpy)
        print('quicksort {} -> {}'.format( inp, inpcpy))
        msorted = mergesort(inpcpy)
        print('mergesort {} -> {}'.format( inp, inpcpy))
        print('practice section')
        practice_native_sorted = nativeSort(inp)
        print('native python sort {} -> {}'.format(inp, practice_native_sorted))
        practice_heapsort = heapsort1(inp)
        print('native python sort {} -> {}'.format(inp, practice_heapsort))


if __name__ == "__main__":
    test()
