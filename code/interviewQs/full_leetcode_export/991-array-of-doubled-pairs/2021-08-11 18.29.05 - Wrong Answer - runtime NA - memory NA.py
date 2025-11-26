class Solution:
    def canReorderDoubled(self, arr: List[int]) -> bool:
        n2index = dict()
        for i,n in enumerate(arr):
            if n in n2index:
                n2index[n].append(i)
            else:
                n2index[n] = [i]
          
        #print(n2index)
        for k,v in n2index.items():
            #print(k,v, k*2, k//2 )
            if not v: #this number was already matched
                continue
            match = False
            if 2*k in n2index:
                idxs = n2index[2*k]
                if idxs:
                    match = True
                    idxs.pop()
                    
            elif k//2 in n2index and k%2==0: #we need % check since // operator rounds
                idxs = n2index[k//2]
                if idxs:
                    match = True
                    idxs.pop()
                    
            else:
                return False
            if match:
                v.pop()
            else:
                return False
        for v in n2index.values(): #after all nums are matched all index lists must be empty
            if v:
                return False
        return True
                
                    