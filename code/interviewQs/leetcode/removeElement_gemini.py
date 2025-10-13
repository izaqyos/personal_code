def removeElement(nums, val):
    """
    Removes all occurrences of val in nums in-place and returns the number of elements not equal to val.

    Args:
      nums: The input integer array.
      val: The integer value to remove.

    Returns:
      The number of elements in nums that are not equal to val (k).
    """
    k = 0  # Initialize the counter for elements not equal to val
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]  # Overwrite elements at the beginning with non-val elements
            k += 1
    return k


# Test Cases
def test_removeElement():
    test_cases = [
        {
            "nums": [3, 2, 2, 3],
            "val": 3,
            "expected_k": 2,
            "expected_nums": [2, 2]
        },
        {
            "nums": [0, 1, 2, 2, 3, 0, 4, 2],
            "val": 2,
            "expected_k": 5,
            "expected_nums": [0, 1, 3, 0, 4]
        },
        {
            "nums": [3, 3],
            "val": 3,
            "expected_k": 0,
            "expected_nums": []
        },
        {
            "nums": [],
            "val": 0,
            "expected_k": 0,
            "expected_nums": []
        },
        {
            "nums": [4,5],
            "val": 5,
            "expected_k": 1,
            "expected_nums": [4]
        }
    ]

    for case in test_cases:
        nums_copy = case["nums"].copy()  # Create a copy to avoid modifying the original list
        k = removeElement(nums_copy, case["val"])

        assert k == case["expected_k"], f"Expected k={case['expected_k']}, but got k={k}"
        
        # Check if the first k elements are correct
        assert nums_copy[:k] == sorted(case["expected_nums"]), f"Expected nums[:k]={sorted(case['expected_nums'])}, but got nums[:k]={nums_copy[:k]}"
        
        print(f"Test case passed: {case}")

test_removeElement()


