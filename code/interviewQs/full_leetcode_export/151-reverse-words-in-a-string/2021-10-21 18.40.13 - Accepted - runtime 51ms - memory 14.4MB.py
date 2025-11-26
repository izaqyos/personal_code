class Solution:
    def reverseWords(self, s: str) -> str:
        # too easy. accepted. 32ms :) 
        #words = s.split()[::-1]
        #return " ".join(words)
        
        #low level work
        words = []
        word = []
        for c in s:
            if c == ' ':
                if word:
                    words.append("".join(word))
                    word = []
            else:
                word.append(c)
        if word:
            words.append("".join(word))
                
        return " ".join(words[::-1])
                
            