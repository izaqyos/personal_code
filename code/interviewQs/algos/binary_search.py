def bsearch(A, l, h, n):
    """
    binary search. A is sorted. l low index, h high indes, n number
    """
    if h>=len(A):
        h=len(A)
    if l<0:
        l=0
    
    while l<h:
        mid = (l+h)//2
        if A[mid] == n:
            return mid
        elif A[mid] > n:
            h = mid
        else:
            l = mid+1
    
    return -1

# practice
def bsearch1(A, t):
    l,h = 0, len(A)
    if h == -1: #empty array return -1, not found
        return h
    while l<h:
        m=(l+h)//2
        if A[m]>t:
            h=m #note we could decrease m by 1 but in case m=0 it would yield illegal address
        elif A[m]<t:
            l=m+1 # note we increase l by 1 as l is at least smaller than h by 1 
        else:
            return m
    return -1

# practice
def test():
    inputs = [ ([0, 6, 9, 20, 100, 103], [-2,0, 6, 10, 105, 20, 100, 103, 2])] #(A, [list of nums to find])
    expected = [ -1, 0, 1, -1, -1, 3, 4, 5, -1]
    for inp in inputs:
        (A, nums) = inp
        print('binary searches on', A)
        for n,e in zip(nums,expected):
            index = bsearch(A, 0, len(A), n)
            print('n={} index is {}'.format(n, index))
            assert(index == e )

        print('practice binary searches on', A)
        for n,e in zip(nums,expected):
            index = bsearch1(A, n)
            print('n={} index is {}'.format(n, index))
            assert(index == e )

if __name__ == "__main__":
    test()
