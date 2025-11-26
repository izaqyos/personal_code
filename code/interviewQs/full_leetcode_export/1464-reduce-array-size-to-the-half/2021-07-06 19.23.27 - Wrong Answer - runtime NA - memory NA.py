class Solution:
    def minSetSize(self, arr: List[int]) -> int:
        if not arr:
            return []
        if len(arr)<3:
            return [arr[0]]
        
        char_freqs_sorted=[]
        char_freqs = {}
        ret=[]
        for n in arr:
            if n in char_freqs:
                char_freqs[n]+=1
            else:
                char_freqs[n]=1
        
        import heapq
        for k,v in char_freqs.items():
            heapq.heappush(char_freqs_sorted, (-v, k))
        
        size=len(arr)
        nsize=size
        while nsize>(size//2):
            freq,n = heapq.heappop(char_freqs_sorted)
            nsize+=freq #for max heap I saved the negative so I actually subsrtact
            ret.append(n)
        return len(ret)
            
            
        
        
        
        