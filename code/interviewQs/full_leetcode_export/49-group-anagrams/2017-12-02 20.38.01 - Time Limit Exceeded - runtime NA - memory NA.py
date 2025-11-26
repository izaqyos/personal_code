class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        
        words = dict()
        
        for word in strs:
            w = tuple(sorted(word,key=string.lower))
            print w
            if w in words.keys():
                words[w].append(word)
            else:
                words[w]=[word]
                
            ret = words.values()
           
        return ret
            
                
        
            
        