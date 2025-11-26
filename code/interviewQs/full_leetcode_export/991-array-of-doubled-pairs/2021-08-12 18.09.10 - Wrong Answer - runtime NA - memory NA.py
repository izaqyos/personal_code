class Solution:
    def canReorderDoubled(self, arr: List[int]) -> bool:
        ncount = dict()
        total = len(arr)
        for n in arr:
            if n in ncount:
                ncount[n]+=1
            else:
                ncount[n] = 1


        for k in sorted(ncount.keys()):
            if k == 0: #special case, 0, 2*0 same key
                total -=ncount[k]
                ncount[k] = 0
                continue
            if ncount[k]>0: 
                if 2*k in ncount and ncount[2*k]>0:
                    matched = min(ncount[k], ncount[2*k])
                    total -= matched
                    ncount[k] -=matched
                    ncount[2*k] -=matched
        return total == 0
