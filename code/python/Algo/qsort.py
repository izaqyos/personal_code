#!/usr/local/bin/python3

def partition(lst, low, high):
    i = low -1 #i is always of the last element smaller than pivot
    pivot = lst[high]

    for j in range(low,high):
        if lst[j] <= pivot:
            i=i+1 #we want to move lst[j] to lst[i] (the last element smaller than pivot)
            lst[i],lst[j] = lst[j], lst[i]

    lst[high],lst[i+1] = lst[i+1], lst[high]
    return i+1

def qsortHelper(lst, low, high):
    #print("===qsortHelper({},{},{})===".format(lst, low, high))
    if(low < high):
        pivotIndex = partition(lst, low, high)
        qsortHelper(lst,low, pivotIndex-1)
        qsortHelper(lst, pivotIndex+1, high)


def qsort(lst):
    qsortHelper(lst, 0, len(lst)-1)


def test():
    lists = [ [], [1], [2,1], [1,3,6,3,4,2], [9,4,2,6,4,0,1,5] ]
    for l in lists:
        print('pre sort {}'.format(l))
        qsort(l) 
        print('post sort {}'.format(l))

if __name__=="__main__":
    test()

