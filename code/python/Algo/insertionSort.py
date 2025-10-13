#!/usr/local/bin/python3


def insertionSort(lst):
    """
Pseudo:

i ← 1
while i < length(A)
    j ← i
    while j > 0 and A[j-1] > A[j]
        swap A[j] and A[j-1]
        j ← j - 1
    end while
    i ← i + 1
end while


Insertion sort iterates, consuming one input element each repetition, and growing a sorted output list. At each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list, and inserts it there. It repeats until no input elements remain.
Sorting is typically done in-place, by iterating up the array, growing the sorted list behind it. At each array-position, it checks the value there against the largest value in the sorted list (which happens to be next to it, in the previous array-position checked). If larger, it leaves the element in place and moves to the next. If smaller, it finds the correct position within the sorted list, shifts all the larger values up to make a space, and inserts into that correct position.
The resulting array after k iterations has the property where the first k + 1 entries are sorted ("+1" because the first entry is skipped). In each iteration the first remaining entry of the input is removed, and inserted into the result at the correct position, thus extending the result:
    """

    i = 1 #i always points 1 past sorted part of array
    while i<len(lst):
        j = i
        while (j>0) and (lst[j] < lst[j-1]): #find the right spot for lst[i] on
                                             # sorted subarray lst[0]-lst[i-1]
            lst[j], lst[j-1] = lst[j-1], lst[j]
            j = j-1
        i = i+1



def testInsertionSort():
    lists = [ [], [1], [2,1], [1,3,6,3,4,2], [9,4,2,6,4,0,1,5] ]
    for l in lists:
        print('pre sort {}'.format(l))
        insertionSort(l) 
        print('post sort {}'.format(l))

if __name__=="__main__":
    testInsertionSort()

