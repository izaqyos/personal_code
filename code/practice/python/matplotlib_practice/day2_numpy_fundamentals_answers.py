#!/usr/bin/env python3
"""
Day 2: NumPy Fundamentals - ANSWERS

Complete solutions for all Day 2 exercises.
"""

import numpy as np


def exercise_1_array_creation():
    """Exercise 1: Create arrays in different ways."""
    print("\n" + "="*60)
    print("Exercise 1: Array Creation - ANSWER")
    print("="*60)
    
    arr_from_list = np.array([1, 2, 3, 4, 5])
    zeros_matrix = np.zeros((3, 3))
    ones_array = np.ones(10)
    range_array = np.arange(10)
    linspace_array = np.linspace(0, 1, 5)
    identity = np.eye(3)
    random_array = np.random.rand(2, 3)
    
    print(f"From list: {arr_from_list}")
    print(f"Zeros:\n{zeros_matrix}")
    print(f"Ones: {ones_array}")
    print(f"Range: {range_array}")
    print(f"Linspace: {linspace_array}")
    print(f"Identity:\n{identity}")
    print(f"Random:\n{random_array}")


def exercise_2_array_properties():
    """Exercise 2: Explore array properties and reshaping."""
    print("\n" + "="*60)
    print("Exercise 2: Array Properties - ANSWER")
    print("="*60)
    
    arr = np.arange(12)
    print(f"Original: {arr}")
    print(f"Shape: {arr.shape}")
    print(f"Dtype: {arr.dtype}")
    print(f"Ndim: {arr.ndim}")
    
    arr_3x4 = arr.reshape((3, 4))
    print(f"\nReshaped to 3x4:\n{arr_3x4}")
    
    arr_3d = arr.reshape((2, 2, 3))
    print(f"\nReshaped to 2x2x3:\n{arr_3d}")
    
    arr_flat = arr_3d.flatten()
    print(f"\nFlattened: {arr_flat}")
    
    arr_transposed = arr_3x4.T
    print(f"\nTransposed (4x3):\n{arr_transposed}")


def exercise_3_indexing_slicing():
    """Exercise 3: Indexing and slicing arrays."""
    print("\n" + "="*60)
    print("Exercise 3: Indexing and Slicing - ANSWER")
    print("="*60)
    
    arr = np.arange(25).reshape((5, 5))
    print(f"Array:\n{arr}")
    
    element = arr[2, 3]
    print(f"\nElement at (2,3): {element}")
    
    third_row = arr[2, :]
    print(f"Third row: {third_row}")
    
    second_col = arr[:, 1]
    print(f"Second column: {second_col}")
    
    subarray = arr[1:3, 2:4]
    print(f"Subarray (rows 1-2, cols 2-3):\n{subarray}")
    
    every_other = arr[0, ::2]
    print(f"Every other from first row: {every_other}")
    
    reversed_arr = arr[::-1, ::-1]
    print(f"Reversed:\n{reversed_arr}")


def exercise_4_vectorized_operations():
    """Exercise 4: Perform vectorized operations."""
    print("\n" + "="*60)
    print("Exercise 4: Vectorized Operations - ANSWER")
    print("="*60)
    
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])
    
    print(f"a = {a}")
    print(f"b = {b}")
    
    sum_ab = a + b
    print(f"\na + b = {sum_ab}")
    
    prod_ab = a * b
    print(f"a * b = {prod_ab}")
    
    a_squared = a ** 2
    print(f"a² = {a_squared}")
    
    b_sqrt = np.sqrt(b)
    print(f"√b = {b_sqrt}")
    
    dot_product = np.dot(a, b)
    print(f"a · b = {dot_product}")
    
    mask = a > 2
    print(f"\nMask (a > 2): {mask}")
    
    a_filtered = a[mask]
    print(f"Filtered a: {a_filtered}")


def exercise_5_aggregation_functions():
    """Exercise 5: Use aggregation functions."""
    print("\n" + "="*60)
    print("Exercise 5: Aggregation Functions - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    arr = np.random.rand(4, 3)
    print(f"Array:\n{arr}")
    
    print(f"\nSum: {arr.sum():.4f}")
    print(f"Mean: {arr.mean():.4f}")
    print(f"Std: {arr.std():.4f}")
    print(f"Min: {arr.min():.4f}")
    print(f"Max: {arr.max():.4f}")
    
    row_sums = arr.sum(axis=1)
    print(f"\nRow sums: {row_sums}")
    
    col_means = arr.mean(axis=0)
    print(f"Column means: {col_means}")
    
    max_index = arr.argmax()
    print(f"Index of max: {max_index}")
    print(f"(row, col) of max: {np.unravel_index(max_index, arr.shape)}")
    
    cumsum_rows = np.cumsum(arr, axis=1)
    print(f"\nCumulative sum along rows:\n{cumsum_rows}")


def exercise_6_broadcasting():
    """Exercise 6: Understand broadcasting rules."""
    print("\n" + "="*60)
    print("Exercise 6: Broadcasting - ANSWER")
    print("="*60)
    
    arr = np.ones((3, 4))
    print(f"Original (3x4):\n{arr}")
    
    row_vector = np.array([1, 2, 3, 4])
    row_addition = arr + row_vector
    print(f"\nAdd [1,2,3,4] to each row:\n{row_addition}")
    
    col_vector = np.array([[10], [20], [30]])
    col_addition = arr + col_vector
    print(f"\nAdd [[10],[20],[30]] to each column:\n{col_addition}")
    
    outer = np.outer([1, 2, 3], [1, 2, 3, 4])
    print(f"\nOuter product:\n{outer}")
    
    np.random.seed(42)
    data = np.random.randn(5, 3)
    print(f"\nOriginal data:\n{data}")
    print(f"Column means: {data.mean(axis=0)}")
    
    normalized = data - data.mean(axis=0)
    print(f"\nNormalized:\n{normalized}")
    print(f"New column means (≈0): {normalized.mean(axis=0)}")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 2: NUMPY FUNDAMENTALS - ANSWERS")
    print("="*60)
    
    exercise_1_array_creation()
    exercise_2_array_properties()
    exercise_3_indexing_slicing()
    exercise_4_vectorized_operations()
    exercise_5_aggregation_functions()
    exercise_6_broadcasting()
    
    print("\n✓ All exercises completed!")


if __name__ == "__main__":
    main()
