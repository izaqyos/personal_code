"""
Queue Removals
You're given a list of n integers arr, which represent elements in a queue (in order from front to back). You're also given an integer x, and must perform x iterations of the following 3-step process:
Pop x elements from the front of queue (or, if it contains fewer than x elements, pop all of them)
Of the elements that were popped, find the one with the largest value (if there are multiple such elements, take the one which had been popped the earliest), and remove it
For each one of the remaining elements that were popped (in the order they had been popped), decrement its value by 1 if it's positive (otherwise, if its value is 0, then it's left unchanged), and then push it back onto the queue
Compute a list of x integers output, the ith of which is the 1-based index in the original array of the element which had been removed in step 2 during the ith iteration.
Signature
int[] findPositions(int[] arr, int x)
Input
x is in the range [1, 316].
n is in the range [x, x*x].
Each value arr[i] is in the range [1, x].
Output
Return a list of x integers output, as described above.
Example
n = 6
arr = [1, 2, 2, 3, 4, 5]
x = 5
output = [5, 6, 4, 1, 2]
The initial queue is [1, 2, 2, 3, 4, 5] (from front to back).
In the first iteration, the first 5 elements are popped off the queue, leaving just [5]. Of the popped elements, the largest one is the 4, which was at index 5 in the original array. The remaining elements are then decremented and pushed back onto the queue, whose contents are then [5, 0, 1, 1, 2].
In the second iteration, all 5 elements are popped off the queue. The largest one is the 5, which was at index 6 in the original array. The remaining elements are then decremented (aside from the 0) and pushed back onto the queue, whose contents are then [0, 0, 0, 1].
In the third iteration, all 4 elements are popped off the queue. The largest one is the 1, which had the initial value of 3 at index 4 in the original array. The remaining elements are pushed back onto the queue, whose contents are then [0, 0, 0].
In the fourth iteration, all 3 elements are popped off the queue. Since they all have an equal value, we remove the one that was popped first, which had the initial value of 1 at index 1 in the original array. The remaining elements are pushed backed onto the queue, whose contents are then [0, 0].
In the final iteration, both elements are popped off the queue. We remove the one that was popped first, which had the initial value of 2 at index 2 in the original array.
"""
import math
# Add any extra import statements you may need here


# Add any helper functions you may need here


def findPositions(arr, x):
  # Write your code here
  print('arr {}, x {}'.format(arr, x))
  from collections import deque
  q = deque()
  for i in range(len(arr)):
    q.append( [arr.pop(0), i] )

  print('q', q)
  
  ret=[]
  for i in range(x):
      poped = [ q.popleft() for i in range(x) if len(q) > 0 ]
      print('poped: ', poped)
      mx = poped[0]
      mxi = 0
      for j in range(1, len(poped)):
        if poped[j][0] > mx[0]:
          mx = poped[j]
          mxi = j
      print('max of poped {}, orig index {}'.format(poped[mxi][0], poped[mxi][1]))
      ret.append(poped[mxi][1]+1)
      poped.pop(mxi)
      for k in range(len(poped)):
        n = poped.pop(0)
        if n[0] > 0:
            n[0]-=1
        q.append(n)
      
  return ret
  

	









# These are the tests we use to determine if the solution is correct.
# You can add your own at the bottom, but they are otherwise not editable!

def printInteger(n):
  print('[', n, ']', sep='', end='')

def printIntegerList(array):
  size = len(array)
  print('[', end='')
  for i in range(size):
    if i != 0:
      print(', ', end='')
    print(array[i], end='')
  print(']', end='')

test_case_number = 1

def check(expected, output):
  global test_case_number
  expected_size = len(expected)
  output_size = len(output)
  result = True
  if expected_size != output_size:
    result = False
  for i in range(min(expected_size, output_size)):
    result &= (output[i] == expected[i])
  rightTick = '\u2713'
  wrongTick = '\u2717'
  if result:
    print(rightTick, 'Test #', test_case_number, sep='')
  else:
    print(wrongTick, 'Test #', test_case_number, ': Expected ', sep='', end='')
    printIntegerList(expected)
    print(' Your output: ', end='')
    printIntegerList(output)
    print()
  test_case_number += 1

if __name__ == "__main__":
  n_1 = 6
  x_1 = 5
  arr_1 = [1, 2, 2, 3, 4, 5]
  expected_1 = [5, 6, 4, 1, 2]
  output_1 = findPositions(arr_1, x_1)
  check(expected_1, output_1)

  n_2 = 13
  x_2 = 4
  arr_2 = [2, 4, 2, 4, 3, 1, 2, 2, 3, 4, 3, 4, 4]
  expected_2 = [2, 5, 10, 13]
  output_2 = findPositions(arr_2, x_2)
  check(expected_2, output_2)


  # Add your own test cases here
