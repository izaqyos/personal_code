class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        Boyer-Moore Voting Algorithm BoyerMooreVoting(sequence):
  Input: A sequence (array, list, etc.) of elements called 'sequence'
  Output: The majority element in the sequence, if it exists; otherwise, an arbitrary element.

  // Initialization
  candidate = null  // Initialize a variable to store the potential majority element (candidate)
  count = 0         // Initialize a counter to 0

  // First Pass: Find a potential candidate
  For each element in sequence:
    If count == 0:
      candidate = element   // If the counter is 0, set the current element as the new candidate
      count = 1             // and set the counter to 1
    Else if element == candidate:
      count = count + 1   // If the current element is the same as the candidate, increment the counter
    Else:
      count = count - 1   // If the current element is different from the candidate, decrement the counter

  // Second Pass: Verify the candidate (Optional but recommended for correctness)
  count = 0
  For each element in sequence:
      If element == candidate:
          count = count + 1

  // Check if the candidate is the true majority element
  If count > (length of sequence) / 2:
    Return candidate
  Else:
    Return "No majority element found"  // Or return null, or raise an exception, depending on the desired behavior
  End If

End Algorithm
        """
        majority = None
        count = 0
        for num in nums:
            if count == 0:
                majority = num
                count = 1
            elif num == majority:
                count += 1
            else:
                count -= 1

        count = 0
        for num in nums:
            if num == majority:
                count += 1
        if count > len(nums)//2:
            return majority
        else:
            return None
