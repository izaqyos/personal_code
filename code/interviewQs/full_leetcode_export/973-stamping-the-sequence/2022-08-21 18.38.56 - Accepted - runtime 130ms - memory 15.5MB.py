class Solution:
    def movesToStamp(self, stamp: str, target: str) -> List[int]:
        m,n = len(stamp), len(target) 
        ret = []
        possible_stamps = set()
        for i in range(m):
            for j in range(m-i):
                possible_stamps.add(i*'#'+stamp[i:m-j]+j*'#')

        desired_target='#'*n
        while target != desired_target:
            
            found = False
            for i in range(n-m+1, -1, -1):
                if target[i:i+m] in possible_stamps:
            
                    target = target[:i] +m*'#'+target[i+m:]
                    
                    ret.append(i)
                    found = True
            if not found:
                return []
        return ret[::-1]
