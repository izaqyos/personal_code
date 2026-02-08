#!/usr/bin/env python3
"""
Day 2: NumPy Fundamentals

NumPy (Numerical Python) is the foundation for scientific computing in Python.
It provides:
- N-dimensional arrays (ndarray) - fast, memory-efficient containers
- Broadcasting - operations between arrays of different shapes
- Vectorized operations - apply operations to entire arrays at once
- Linear algebra, random numbers, Fourier transforms, and more

WHY NUMPY?
- Python lists are slow for numerical operations
- NumPy arrays are stored in contiguous memory (cache-friendly)
- Operations are implemented in C (100x faster than Python loops)
- Essential for ML, data science, image processing, simulations

INSTRUCTIONS:
1. Complete each exercise by filling in the TODO sections
2. Run the script to verify your solutions
3. Check day2_numpy_fundamentals_answers.py if stuck
"""

import numpy as np


def exercise_1_array_creation():
    """
    Exercise 1: Create arrays in different ways.
    
    TODO:
    1. Create a 1D array from a Python list [1, 2, 3, 4, 5]
    2. Create a 2D array (3x3 matrix) of zeros
    3. Create a 1D array of 10 ones
    4. Create an array from 0 to 9 (use np.arange)
    5. Create an array of 5 evenly spaced values from 0 to 1 (use np.linspace)
    6. Create a 3x3 identity matrix (use np.eye)
    7. Create a 2x3 array of random values between 0 and 1
    
    HINTS:
    - np.array([...]) for list conversion
    - np.zeros((rows, cols)) for zeros
    - np.ones(n) for ones
    - np.arange(start, stop) like range()
    - np.linspace(start, stop, num_points)
    - np.eye(n) for identity matrix
    - np.random.rand(rows, cols) for random
    """
    print("\n" + "="*60)
    print("Exercise 1: Array Creation")
    print("="*60)
    
    # TODO: Create array from list
    arr_from_list = None
    
    # TODO: Create 3x3 matrix of zeros
    zeros_matrix = None
    
    # TODO: Create array of 10 ones
    ones_array = None
    
    # TODO: Create array [0, 1, 2, ..., 9]
    range_array = None
    
    # TODO: Create 5 evenly spaced values from 0 to 1
    linspace_array = None
    
    # TODO: Create 3x3 identity matrix
    identity = None
    
    # TODO: Create 2x3 random array
    random_array = None
    
    # Verification (uncomment after implementing)
    # print(f"From list: {arr_from_list}")
    # print(f"Zeros:\n{zeros_matrix}")
    # print(f"Ones: {ones_array}")
    # print(f"Range: {range_array}")
    # print(f"Linspace: {linspace_array}")
    # print(f"Identity:\n{identity}")
    # print(f"Random:\n{random_array}")
    
    print("Exercise 1: Not implemented yet - fill in the TODOs!")


def exercise_2_array_properties():
    """
    Exercise 2: Explore array properties and reshaping.
    
    TODO:
    1. Create an array of 12 elements (0 to 11)
    2. Print its shape, dtype, and ndim
    3. Reshape it to 3x4
    4. Reshape it to 2x2x3 (3D)
    5. Flatten it back to 1D
    6. Transpose the 3x4 array
    
    HINTS:
    - arr.shape, arr.dtype, arr.ndim for properties
    - arr.reshape((rows, cols))
    - arr.flatten() or arr.ravel()
    - arr.T for transpose
    """
    print("\n" + "="*60)
    print("Exercise 2: Array Properties")
    print("="*60)
    
    # TODO: Create array 0-11
    arr = None
    
    # TODO: Print shape, dtype, ndim
    # print(f"Shape: {arr.shape}")
    # print(f"Dtype: {arr.dtype}")
    # print(f"Ndim: {arr.ndim}")
    
    # TODO: Reshape to 3x4
    arr_3x4 = None
    
    # TODO: Reshape to 2x2x3
    arr_3d = None
    
    # TODO: Flatten back to 1D
    arr_flat = None
    
    # TODO: Transpose 3x4 to 4x3
    arr_transposed = None
    
    print("Exercise 2: Not implemented yet - fill in the TODOs!")


def exercise_3_indexing_slicing():
    """
    Exercise 3: Indexing and slicing arrays.
    
    TODO:
    1. Create a 5x5 array with values 0-24
    2. Get the element at row 2, column 3
    3. Get the entire third row
    4. Get the entire second column
    5. Get a 2x2 subarray from rows 1-2, columns 2-3
    6. Get every other element from the first row
    7. Reverse the array along both axes
    
    HINTS:
    - arr[row, col] for single element
    - arr[row, :] for entire row
    - arr[:, col] for entire column
    - arr[r1:r2, c1:c2] for subarray
    - arr[::2] for every other element
    - arr[::-1, ::-1] for reversing
    """
    print("\n" + "="*60)
    print("Exercise 3: Indexing and Slicing")
    print("="*60)
    
    # TODO: Create 5x5 array (0-24 reshaped)
    arr = None
    
    # TODO: Element at (2, 3)
    element = None
    
    # TODO: Third row (index 2)
    third_row = None
    
    # TODO: Second column (index 1)
    second_col = None
    
    # TODO: 2x2 subarray (rows 1-2, cols 2-3)
    subarray = None
    
    # TODO: Every other element from first row
    every_other = None
    
    # TODO: Reversed array
    reversed_arr = None
    
    print("Exercise 3: Not implemented yet - fill in the TODOs!")


def exercise_4_vectorized_operations():
    """
    Exercise 4: Perform vectorized operations (no loops!).
    
    TODO:
    1. Create arrays a = [1, 2, 3, 4, 5] and b = [10, 20, 30, 40, 50]
    2. Add them element-wise
    3. Multiply them element-wise
    4. Square all elements in a
    5. Calculate sqrt of all elements in b
    6. Calculate the dot product of a and b
    7. Create a boolean mask where a > 2
    8. Use the mask to filter a
    
    HINTS:
    - a + b, a * b for element-wise operations
    - a ** 2 for power
    - np.sqrt(b) for square root
    - np.dot(a, b) or a @ b for dot product
    - a > 2 creates boolean array
    - a[mask] filters using boolean array
    """
    print("\n" + "="*60)
    print("Exercise 4: Vectorized Operations")
    print("="*60)
    
    # TODO: Create arrays
    a = None
    b = None
    
    # TODO: Element-wise addition
    sum_ab = None
    
    # TODO: Element-wise multiplication
    prod_ab = None
    
    # TODO: Square of a
    a_squared = None
    
    # TODO: Square root of b
    b_sqrt = None
    
    # TODO: Dot product
    dot_product = None
    
    # TODO: Boolean mask where a > 2
    mask = None
    
    # TODO: Filtered array
    a_filtered = None
    
    print("Exercise 4: Not implemented yet - fill in the TODOs!")


def exercise_5_aggregation_functions():
    """
    Exercise 5: Use aggregation functions.
    
    TODO:
    1. Create a 4x3 random array (use seed=42 for reproducibility)
    2. Calculate: sum, mean, std, min, max of entire array
    3. Calculate sum along rows (axis=1)
    4. Calculate mean along columns (axis=0)
    5. Find index of maximum value (use argmax)
    6. Calculate cumulative sum along rows
    
    HINTS:
    - np.random.seed(42) for reproducibility
    - arr.sum(), arr.mean(), arr.std(), arr.min(), arr.max()
    - arr.sum(axis=1) for row-wise
    - arr.sum(axis=0) for column-wise
    - arr.argmax() for index of max
    - np.cumsum(arr, axis=1) for cumulative sum
    """
    print("\n" + "="*60)
    print("Exercise 5: Aggregation Functions")
    print("="*60)
    
    np.random.seed(42)
    
    # TODO: Create 4x3 random array
    arr = None
    
    # TODO: Calculate statistics
    total = None
    mean_val = None
    std_val = None
    min_val = None
    max_val = None
    
    # TODO: Sum along rows
    row_sums = None
    
    # TODO: Mean along columns
    col_means = None
    
    # TODO: Index of maximum
    max_index = None
    
    # TODO: Cumulative sum along rows
    cumsum_rows = None
    
    print("Exercise 5: Not implemented yet - fill in the TODOs!")


def exercise_6_broadcasting():
    """
    Exercise 6: Understand broadcasting rules.
    
    Broadcasting allows operations on arrays of different shapes.
    Rules:
    1. Arrays are compared from trailing dimensions
    2. Dimensions are compatible if equal or one is 1
    3. Smaller array is "broadcast" to match larger
    
    TODO:
    1. Create a 3x4 array of ones
    2. Add a 1D array [1, 2, 3, 4] to each row (broadcasts across rows)
    3. Add a column vector [[10], [20], [30]] to each column
    4. Create a 3x4 array from outer product of [1,2,3] and [1,2,3,4]
    5. Normalize each column to have mean 0 (subtract column means)
    
    HINTS:
    - Row vector: shape (4,) broadcasts to (3, 4)
    - Column vector: shape (3, 1) broadcasts to (3, 4)
    - np.outer(a, b) for outer product
    - arr - arr.mean(axis=0) for column normalization
    """
    print("\n" + "="*60)
    print("Exercise 6: Broadcasting")
    print("="*60)
    
    # TODO: Create 3x4 ones
    arr = None
    
    # TODO: Add [1,2,3,4] to each row
    row_addition = None
    
    # TODO: Add [[10],[20],[30]] to each column
    col_vector = None  # Shape (3, 1)
    col_addition = None
    
    # TODO: Outer product
    outer = None
    
    # TODO: Normalize columns
    np.random.seed(42)
    data = np.random.randn(5, 3)  # 5 rows, 3 columns
    normalized = None  # Each column should have mean ≈ 0
    
    print("Exercise 6: Not implemented yet - fill in the TODOs!")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 2: NUMPY FUNDAMENTALS")
    print("="*60)
    print("\nNumPy is the foundation for numerical computing in Python.")
    print("Complete each exercise by filling in the TODO sections.")
    
    exercise_1_array_creation()
    exercise_2_array_properties()
    exercise_3_indexing_slicing()
    exercise_4_vectorized_operations()
    exercise_5_aggregation_functions()
    exercise_6_broadcasting()
    
    print("\n" + "="*60)
    print("Complete the TODOs and run again to verify!")
    print("="*60)


if __name__ == "__main__":
    main()
