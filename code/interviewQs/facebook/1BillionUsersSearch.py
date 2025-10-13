"""
1 Billion Users
We have N different apps with different user growth rates. At a given time t, measured in days, the number of users using an app is g^t (for simplicity we'll allow fractional users), where g is the growth rate for that app. These apps will all be launched at the same time and no user ever uses more than one of the apps.
After how many full days will we have 1 billion total users across the N apps?
Signature
int getBillionUsersDay(float[] growthRates)
Input
1.0 < growthRate < 2.0 for all growth rates
1 <= N <= 1,000
Output
Return the number of full days it will take before we have a total of 1 billion users across all N apps.
Example 1
growthRates = [1.5]
output = 52
Example 2
growthRates = [1.1, 1.2, 1.3]
output = 79
Example 3
growthRates = [1.01, 1.02]
output = 1047
"""

import math
# Add any extra import statements you may need here


# Add any helper functions you may need here


def getBillionUsersDay(growthRates):
  # Write your code here
  def numusers(growthRates, t):
    nusers = [ pow(gr, t) for gr in growthRates]
    return sum(nusers)

  target = pow(10,9)
  gh = 50
  while numusers(growthRates, gh) < target:
    gh *=2

  gl = 0

  while gl < gh:
    if gl == gh-1:
      return gh
    guess = (gl+gh)//2
    nu = numusers(growthRates, guess)
    if nu == target:
      return guess
    elif nu > target:
      gh = guess
      #gl = gl + (guess-gl)//2
    else:
      gl = gl + (gh-gl)//2
















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
  test_1 = [1.1, 1.2, 1.3]
  expected_1 = 79
  output_1 = getBillionUsersDay(test_1)
  check(expected_1, output_1)

  test_2 = [1.01, 1.02]
  expected_2 = 1047
  output_2 = getBillionUsersDay(test_2)
  check(expected_2, output_2)

  # Add your own test cases here


