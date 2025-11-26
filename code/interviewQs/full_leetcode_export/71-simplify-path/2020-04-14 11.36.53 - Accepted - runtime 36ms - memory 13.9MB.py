from collections import deque

class Solution:
    def __init__(self):
        self.q = deque()

    def handle_dir(self, dir):
        if len(dir) == 0: 
            return

        if dir == '.':
            return
        elif dir == '..':
            if len(self.q) > 0:
                self.q.pop()
        else:
            self.q.append(dir)

    def finalize(self):
        """
        use dirs in stack to reconstruct path. if it weren't for deque o(1) popleft would have 
        used a 2nd stack to reverse order of dirs so root pops first etc. 
        """
        path = '/'
        while len(self.q) > 0:
            path+= self.q.popleft()
            if (len(self.q) > 0):
                path+='/'

        return path

    def simplifyPath(self, path):
        """
        rules, remove ending / if any
        scan path, consume patterns between / , 
        if pattern is . - noop
        if pattern is .. - pop stack if not empty
        if pattern is a word - push to stack
        if pattern is empty set ending / as starting / for next check
        """
        index = 0
        length = len(path)
        if path[-1] == '/':
            length-=1

        lslash = False
        left_slash = 0
        right_slash = 0
        while index < length:
            c = path[index]
            if c == '/':
                if lslash:
                    right_slash = index
                    self.handle_dir(path[left_slash+1: right_slash])
                    left_slash = index
                    lslash = True
                else:
                    lslash = True
                    left_slash = index
            index+=1

        if left_slash < length: #save call handle dir with empty dir 
            self.handle_dir(path[left_slash+1: length])

        return self.finalize()