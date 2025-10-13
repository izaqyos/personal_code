"""
   list of vectors , list of lists
    v1 = [10,7, 12]
    v2 = [12, 15, 17, 4]
    v3 = [10,20,30,40]

    # vectors,  M  sum off all |Vi| i from 0 to len() -1
    data

    operations.
    all(vec) : # return all vectors containing
    all([10,12]) -> v1 (all vectors containing all input nums)
Idea . Build dict of num to ver indices set for all num in all vectors.
Then use it.
For all. Intersection of all sets of num in input (if num not in dictionary return empty set)
For any. union of all sets of num in input
For none.  call any. Then do set of all indices - (difference) any_set

    any([10,30]) -> 0,2 indexes


    none(v) -> return all vecors not containg none of nums in v
    none(10,7) -> return index 1
    ret = set()
    for n in in:
        for st in d




all complexit
all(iv) len(iv) = n
num of vectors = k
len(sum all vec lengths) = m



"""



from collections import defaultdict
class vecOps:
    def __init__(self, lists):
        """
        dictionary
        10: {0,2}
        7: {0}
        12: {0,1}
        """
        self.lists=lists
        self.nums2ListsDict= defaultdict(set)
        for i,lst in enumerate(lists):
            for n in lst:
                self.nums2ListsDict[n].add(i)
    
    def __str__(self):
        repr_str = "vecOps vectors:\n"
        repr_str += str(self.lists)
        repr_str += '\n'
        repr_str += "Numbers to vector indices dictionary:\n"
        repr_str += str(self.nums2ListsDict)
        return repr_str

    def any(self, iv):
       ret = set()
       
       #remove dupes in input
       ivset = set()
       for n in iv:
           ivset.add(n)
       
       for n in ivset:
           if n in self.nums2ListsDict:
               nset = self.nums2ListsDict[n]
               ret|=nset #ret.union(nset)
           #else: #if input number is not in vectors its containing set is empty so ret|{} is same as doing nothing
           #    return set()
       
       return ret

    def none(self, iv):
       anyset = self.any(iv)
       #allset = set.union(*self.nums2ListsDict.values()) #1 way 2 get all set. but much better:
       allset = {i for i in range(len(self.lists))}
       return allset-anyset
       


    def all(self, iv):
       ret = set()
       
       #remove dupes in input
       ivset = set()
       for n in iv:
           ivset.add(n)
       
       for n in ivset:
           if n in self.nums2ListsDict:
               nset = self.nums2ListsDict[n]
               if len(ret) == 0:
                   ret = nset
               else:
                   ret&=nset #ret.intersection(nset)
           else:
               return set()
       
       return ret

def test():
    lists=[ 
        [10,7, 12, 30],
    [12, 15, 17, 4],
    [10,20,30,40],
]

    ops = vecOps(lists)
    print("Testing vecOps instance: ", ops)

    ivs = [ [10, 30], [], [15], [3] ]
    expected = [ {0,2}, set(), {1}, set()]
    for inp,exp in zip(ivs, expected):
        res = ops.all(inp)
        print('all({})={}'.format(inp,res))
        assert(res == exp)
    
    any_ivs = [ [10, 12, 20], [], [15, 40], [3] ]
    any_expected = [ {0,1,2}, set(), {1,2}, set()]
    for inp,exp in zip(any_ivs, any_expected):
        res = ops.any(inp)
        print('any({})={}'.format(inp,res))
        assert(res == exp)

    none_ivs = [ [10, 12, 20], [], [15, 40], [3] ]
    none_expected = [ set(), {0,1,2}, {0}, {0,1,2}]
    for inp,exp in zip(none_ivs, none_expected):
        res = ops.none(inp)
        print('none({})={}'.format(inp,res))
        assert(res == exp)

if __name__ == "__main__":
    test()
