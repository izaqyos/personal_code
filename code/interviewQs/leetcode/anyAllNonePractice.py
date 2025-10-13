""" 
practice any all none 
"""
from typing import List, Set, Dict, Tuple, Optional

class listsContainer:

    def init_indices(self, numbers: List[int], index: int):
        if numbers:
            for n in numbers:
                self.indexNum(n, index)
        else: 
            # we need to keep track of indices of empty lists to add to none result (algorithm uses dictionary and relies on at least one value)
           self.emptyLists.add(index)

    def __init__(self, numbers: List[List[int]]):
        self.numbers:List[List[int]] = []
        self.nums2indices: Dict(int, Set[int]) = dict()
        self.emptyLists = set()
        for i,n in enumerate(numbers):
            # self.numbers.append(n) #ref copy
            self.numbers.append(n[:]) #shallow copy
            self.init_indices(n,i)


    def indexNum(self, number: int, index: int):
        if number in self.nums2indices:
            self.nums2indices[number].add(index)
        else:
            self.nums2indices[number] = {index};

    def printMe(self):
        print("listsContainer sub lists are:")
        for n in self.numbers:
            print(n)
        print(f"listsContainer indices: {self.nums2indices}")

    def all(self, nums: List[int]):
        """
        return set of indices of all lists that contain all of the numbers in nums
        """
        ret_set =  {_ for _ in range(len(self.numbers))}
        for n in nums:
            ret_set = ret_set.intersection(self.nums2indices[n])
        return ret_set

    def any(self, nums: List[int]):
        """
        return set of indices of all lists that contain any of the numbers in nums
        """
        ret_set = set()
        for n in nums:
            ret_set = ret_set.union(self.nums2indices[n])
        return ret_set

    #todo, cont. w/ none 
    def none(self, nums: List[int]):
        """
        return set of indices of all lists that contain none of the numbers in nums
        """
        ret_set = set()
        for aset in self.nums2indices.values():
            ret_set =  ret_set.union(aset)
        for n in nums:
            ret_set = ret_set - self.nums2indices[n]
        print(f"none set before empty lists {ret_set}")
        ret_set = ret_set.union(self.emptyLists)
        return ret_set



def test():
    l1 = [_ for _ in range(9)]
    l2 = [_ for _ in range(5)]
    l3 = [_ for _ in range(3)]
    l4 = [_ for _ in range(3,8)]
    l5 = []
    l6 = [12]
    inputs = [l1,l2,l3,l4,l5,l6]
    lc = listsContainer(inputs)
    lc.printMe()
    any1 = lc.any([12,5])
    print(f"any of [12,5] is {any1}")
    none1 = lc.none([12,5,4])
    print(f"none of [12,5, 4] is {none1}")
    all1 = lc.all([1,2])
    print(f"all of [1,2] is {all1}")
    all2 = lc.all([12])
    print(f"all of [12] is {all2}")
    all3 = lc.all([1, 12])
    print(f"all of [1, 12] is {all3}")

def main():
    test()

if __name__ == "__main__":
    main()
