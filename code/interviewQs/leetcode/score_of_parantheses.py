class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        total = 0
        from collections import deque
        st = deque()
        for c in s:
            if c == '(':
                st.append(total) #save total so far
                total = 0 #since we start a new (  seq processing (DFS) reset total
            else:
                ttotal = st.pop() #restore total so far
                total = ttotal + max(2*total, 1) # add to total so far the max of 1 for () or two times total for (A) where A is valid parenthes
        return total
                
                
 
        

# fails on "(()(()))" naive approach will not work. require recursion
# todo, implement recursion Solution
