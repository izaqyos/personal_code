import math
# Add any extra import statements you may need here


class TreeNode: 
  def __init__(self,key): 
    self.left = None
    self.right = None
    self.val = key 

# Add any helper functions you may need here


def visible_nodes(root):
  # Write your code here
  # Visible nodes # is same as max tree depth. so we can do DFS recursively
  # Non recursive, keep 2 stacks the normal DFS one and a 2nd, path stack. When top of both stacks is same
  # means we r at a leave so update depth to max(depth, len(path))
  
  #recursion
  def max_depth_r(root):

    if root == None:
      return 0
    else:
      return max( max_depth_r(root.left), max_depth_r(root.right)) +1
    
  #no recursion
  from collections import deque
  def max_depth(root):
    depth = 0
    dfs_stack = deque()
    path = deque()
    dfs_stack.append(root)
    while len(dfs_stack) > 0:
      cur = dfs_stack[-1]
      if len(path) > 0 and (path[-1] == cur):
        if depth < len(path):
          depth = len(path)
        dfs_stack.pop()
        path.pop()
      else:
        path.append(cur)
        if cur.right != None:
          dfs_stack.append(cur.right)
        if cur.left != None:
          dfs_stack.append(cur.left)
    return depth
      
    
  
  #return max_depth_r(root)
  return max_depth(root)
  










# These are the tests we use to determine if the solution is correct.
# You can add your own at the bottom, but they are otherwise not editable!

def printInteger(n):
  print('[', n, ']', sep='', end='')

test_case_number = 1

def check(expected, output):
  global test_case_number
  result = False
  if expected == output:
    result = True
  rightTick = '\u2713'
  wrongTick = '\u2717'
  if result:
    print(rightTick, 'Test #', test_case_number, sep='')
  else:
    print(wrongTick, 'Test #', test_case_number, ': Expected ', sep='', end='')
    printInteger(expected)
    print(' Your output: ', end='')
    printInteger(output)
    print()
  test_case_number += 1

if __name__ == "__main__":
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  expected_1 = 4
  output_1 = visible_nodes(root_1)
  check(expected_1, output_1)

  root_2 = TreeNode(10)
  root_2.left = TreeNode(8)
  root_2.right = TreeNode(15)
  root_2.left.left = TreeNode(4)
  root_2.left.left.right = TreeNode(5)
  root_2.left.left.right.right = TreeNode(6)
  root_2.right.left =TreeNode(14)
  root_2.right.right = TreeNode(16)

  expected_2 = 5
  output_2 = visible_nodes(root_2)
  check(expected_2, output_2)

  # Add your own test cases here
  
