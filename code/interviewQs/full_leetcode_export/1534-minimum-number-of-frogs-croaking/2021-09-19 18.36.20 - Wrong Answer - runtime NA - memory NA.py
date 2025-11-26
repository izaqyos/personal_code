class Solution:

    def minNumberOfFrogs(self, croakOfFrogs: str) -> int:
        """
        idea, keep a list of frogs 
        each frog will be in state one of {c, r, o, a, k} after k back to silent
        if letter not in allowed=['c', 'r', 'o', 'a', 'k'] return -1
        else if letter can't be added to any frog return -1
        """
        allowed =['c', 'r', 'o', 'a', 'k'] 
        frogs = []
        for c in croakOfFrogs:
            if not c in allowed: # guarantedd not to happen, still I like to validate input 
                return -1
            else:
                character_allocated = False
                for i,frog in enumerate(frogs):
                    #print(frog, c, allowed[allowed.index(c)-1])
                    if c == 'c':
                        if frog == 'k':
                            #print(f"reset frog {i} to c")
                            frogs[i] = c
                            character_allocated = True
                    elif frog == allowed[allowed.index(c)-1]:
                        frogs[i] = c
                        character_allocated = True
                if not character_allocated:
                    #print("new frog needed")
                    if c == 'c': # we need a new frog
                        #print("add new frog at C")
                        frogs.append('c')
                    else: #illegal state. this character can't be croacked by any frog
                        return -1
        valid_frogs = [_ for _ in frogs if _[-1] == 'k']
        if valid_frogs:
            return len(valid_frogs)
        else:
            return -1
