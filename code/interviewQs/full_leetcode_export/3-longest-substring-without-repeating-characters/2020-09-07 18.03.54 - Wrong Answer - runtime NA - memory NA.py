class Solution:
    def lengthOfLongestSubstring(self, s):
        if len(s) < 2:
            return len(s)
        l=0
        h=1
        maxsize = 1
        ctoi = {} #character to last seen position
        ctoi[s[0]] = 0
        for i in range(1,len(s)):
        #    if c in str[l:h]: #the search in window is o(n) so overall o(n^2), can use dictionary of last seen pos for total o(n)
        # space is o(1) for naive, o(n) for dictionary
        #        lo=str.index[c]+1
        #        maxsize = max(maxsize, h-l)
        #    hi+=1
            if s[i] in ctoi:
                l = ctoi[s[i]] +1
                ctoi[s[i]] = i
                maxsize = max(maxsize, h-l+1)
            else:
                ctoi[s[i]] = i
            h+=1
        
        return max(maxsize, h-l)