class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        n = len(dominoes)
        domlist = list(dominoes)
        last='L'
        lpos=-1
        for i in range(n):
            if domlist[i] == 'R':
                if last == 'R':
                    for j in range(lpos+1,i):
                        domlist[j]='R'
                last = 'R'
                lpos=i
            if domlist[i] == 'L':
                if last == 'R':
                    diff=i-lpos-1
                    for j in range(lpos+1,lpos+(diff//2)+1):
                            domlist[j]='R'
                    for j in range(i-1, i-(diff//2)-1, -1):
                            
                            domlist[j]='L'
                else:
                    for j in range(lpos+1,i):
                        domlist[j]='L'
                last = 'L'
                lpos=i
        if last == 'R':
            for j in range(lpos+1,n):
                domlist[j] = 'R'
                
        return "".join(domlist)


        