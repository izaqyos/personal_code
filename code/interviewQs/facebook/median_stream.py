import math
# Add any extra import statements you may need here
import heapq

# Add any helper functions you may need here


def findMedian(arr):
  # Write your code here
  if (len(arr) == 0):
    return arr
  
  smaller = [] #max heap. don't forget negate in out...
  bigger = [] #min heap
  
  median = 0
  medians=[]

  for n in arr:
    if n < median:
      if len(smaller) > len(bigger): #maintain max 1 size diff
        heapq.heappush(bigger, -1*heapq.heappop(smaller))
      heapq.heappush(smaller, -1*n)
    else:
      if len(bigger) > len(smaller): #maintain max 1 size diff
        heapq.heappush(smaller, -1*heapq.heappop(bigger))
      heapq.heappush(bigger, n)
      
    if (len(bigger) < len(smaller)):
      median = -1*smaller[0]
    elif (len(smaller) < len(bigger)):
      median = bigger[0]
    else:
      median = (bigger[0] + (-1*smaller[0]))  // 2
    
    medians.append(median)
    
    
  return medians      
      
      
  
  

	









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
  arr_1 = [5, 15, 1, 3]
  expected_1 = [5, 10, 5, 4]
  output_1 = findMedian(arr_1)
  check(expected_1, output_1)

  arr_2 = [2, 4, 7, 1, 5, 3]
  expected_2 = [2, 3, 4, 3, 4, 3]
  output_2 = findMedian(arr_2)
  check(expected_2, output_2)


  # Add your own test cases here
  
