#!/usr/bin/env python3
"""
Day 3: Pandas Essentials

Pandas is the go-to library for data manipulation and analysis.
It provides:
- DataFrame: 2D labeled data structure (like Excel/SQL table)
- Series: 1D labeled array
- Powerful data cleaning, filtering, grouping, and aggregation
- Time series support
- CSV/Excel/SQL/JSON reading and writing

WHY PANDAS?
- Handle missing data elegantly
- Easy data alignment and reshaping
- Split-apply-combine operations (groupby)
- Merge/join datasets like SQL
- Built on NumPy for performance

INSTRUCTIONS:
1. Complete each exercise by filling in the TODO sections
2. Run the script to verify your solutions
3. Check day3_pandas_essentials_answers.py if stuck
"""

import pandas as pd
import numpy as np


def exercise_1_series_dataframe_creation():
    """
    Exercise 1: Create Series and DataFrames.
    
    TODO:
    1. Create a Series from a list [10, 20, 30, 40] with index ['a', 'b', 'c', 'd']
    2. Create a Series from a dictionary {'x': 1, 'y': 2, 'z': 3}
    3. Create a DataFrame from a dictionary:
       {'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['NYC', 'LA', 'Chicago']}
    4. Create a DataFrame from a NumPy array (3x4) with custom column names
    
    HINTS:
    - pd.Series(data, index=...)
    - pd.DataFrame(dict) or pd.DataFrame(array, columns=[...])
    """
    print("\n" + "="*60)
    print("Exercise 1: Series and DataFrame Creation")
    print("="*60)
    
    # TODO: Series from list with index
    series_list = None
    
    # TODO: Series from dictionary
    series_dict = None
    
    # TODO: DataFrame from dictionary
    df_dict = None
    
    # TODO: DataFrame from NumPy array
    np.random.seed(42)
    array = np.random.randn(3, 4)
    df_array = None  # Add columns: ['A', 'B', 'C', 'D']
    
    print("Exercise 1: Not implemented yet - fill in the TODOs!")


def exercise_2_data_selection():
    """
    Exercise 2: Select data from DataFrames.
    
    TODO:
    Given this DataFrame:
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [25, 30, 35, 28, 32],
            'salary': [50000, 60000, 75000, 55000, 70000],
            'department': ['HR', 'IT', 'IT', 'Sales', 'HR']
        })
    
    1. Select the 'name' column (returns Series)
    2. Select multiple columns: ['name', 'salary']
    3. Select rows 1-3 using iloc (integer location)
    4. Select rows where age > 28
    5. Select IT department employees
    6. Select name and salary where salary >= 60000
    7. Use .loc to select rows 1-3, columns 'name' and 'age'
    
    HINTS:
    - df['col'] or df.col for single column
    - df[['col1', 'col2']] for multiple columns
    - df.iloc[start:end] for integer-based
    - df.loc[condition] for label/boolean-based
    - df[df['col'] > value] for boolean filtering
    """
    print("\n" + "="*60)
    print("Exercise 2: Data Selection")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 75000, 55000, 70000],
        'department': ['HR', 'IT', 'IT', 'Sales', 'HR']
    })
    print(df)
    
    # TODO: Select 'name' column
    names = None
    
    # TODO: Select 'name' and 'salary' columns
    name_salary = None
    
    # TODO: Select rows 1-3 (indices 1, 2, 3)
    rows_1_3 = None
    
    # TODO: Filter where age > 28
    age_over_28 = None
    
    # TODO: Filter IT department
    it_dept = None
    
    # TODO: Name and salary where salary >= 60000
    high_earners = None
    
    # TODO: Use .loc for rows 1-3, columns 'name' and 'age'
    loc_selection = None
    
    print("Exercise 2: Not implemented yet - fill in the TODOs!")


def exercise_3_data_manipulation():
    """
    Exercise 3: Add, modify, and delete columns.
    
    TODO:
    1. Add a 'bonus' column = salary * 0.1
    2. Add a 'senior' column = True if age >= 30 else False
    3. Rename 'salary' to 'base_salary'
    4. Create 'total_comp' = base_salary + bonus
    5. Delete the 'bonus' column
    6. Sort by age descending
    7. Reset the index
    
    HINTS:
    - df['new_col'] = values
    - df['col'] = condition (returns boolean Series)
    - df.rename(columns={'old': 'new'})
    - df.drop('col', axis=1) or del df['col']
    - df.sort_values('col', ascending=False)
    - df.reset_index(drop=True)
    """
    print("\n" + "="*60)
    print("Exercise 3: Data Manipulation")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'salary': [50000, 60000, 75000, 55000]
    })
    print("Original:\n", df)
    
    # TODO: Add bonus column (salary * 0.1)
    # df['bonus'] = ...
    
    # TODO: Add senior column (age >= 30)
    # df['senior'] = ...
    
    # TODO: Rename salary to base_salary
    # df = df.rename(...)
    
    # TODO: Add total_comp = base_salary + bonus
    # df['total_comp'] = ...
    
    # TODO: Delete bonus column
    # df = df.drop(...)
    
    # TODO: Sort by age descending
    # df = df.sort_values(...)
    
    # TODO: Reset index
    # df = df.reset_index(...)
    
    print("Exercise 3: Not implemented yet - fill in the TODOs!")


def exercise_4_groupby_aggregation():
    """
    Exercise 4: Group data and aggregate.
    
    TODO:
    1. Group by department and calculate mean salary
    2. Group by department and get count of employees
    3. Group by department and get multiple aggregations:
       {'salary': ['mean', 'min', 'max'], 'age': 'mean'}
    4. Group by department and calculate total salary percentage
    5. Apply a custom function: calculate salary range (max - min)
    
    HINTS:
    - df.groupby('col').mean()
    - df.groupby('col').agg({'col': ['func1', 'func2']})
    - df.groupby('col')['col2'].sum()
    - df.groupby('col').apply(custom_func)
    """
    print("\n" + "="*60)
    print("Exercise 4: GroupBy and Aggregation")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
        'age': [25, 30, 35, 28, 32, 29],
        'salary': [50000, 60000, 75000, 55000, 70000, 58000],
        'department': ['HR', 'IT', 'IT', 'Sales', 'HR', 'Sales']
    })
    print(df)
    
    # TODO: Mean salary by department
    mean_salary = None
    
    # TODO: Employee count by department
    emp_count = None
    
    # TODO: Multiple aggregations
    multi_agg = None
    
    # TODO: Total salary by department as percentage of total
    # Hint: First get sum by dept, then divide by total sum * 100
    total_salary = df['salary'].sum()
    salary_pct = None
    
    # TODO: Salary range by department (max - min)
    # Hint: Use .apply() with a lambda or function
    salary_range = None
    
    print("Exercise 4: Not implemented yet - fill in the TODOs!")


def exercise_5_handling_missing_data():
    """
    Exercise 5: Handle missing data (NaN values).
    
    TODO:
    1. Check which values are missing (isnull)
    2. Count missing values per column
    3. Drop rows with any missing values
    4. Fill missing ages with the mean age
    5. Fill missing departments with 'Unknown'
    6. Use forward fill for missing salaries
    
    HINTS:
    - df.isnull() returns boolean DataFrame
    - df.isnull().sum() counts per column
    - df.dropna() removes rows with NaN
    - df.fillna(value) fills with value
    - df['col'].fillna(df['col'].mean())
    - df.fillna(method='ffill') for forward fill
    """
    print("\n" + "="*60)
    print("Exercise 5: Handling Missing Data")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, np.nan, 35, 28, np.nan],
        'salary': [50000, 60000, np.nan, 55000, 70000],
        'department': ['HR', 'IT', 'IT', np.nan, 'HR']
    })
    print("Original:\n", df)
    
    # TODO: Boolean mask of missing values
    missing_mask = None
    
    # TODO: Count missing per column
    missing_count = None
    
    # TODO: Drop rows with any NaN (create copy)
    df_dropped = None
    
    # TODO: Fill missing ages with mean
    df_copy = df.copy()
    # df_copy['age'] = ...
    
    # TODO: Fill missing departments with 'Unknown'
    # df_copy['department'] = ...
    
    # TODO: Forward fill missing salaries (create another copy)
    df_ffill = df.copy()
    # df_ffill['salary'] = ...
    
    print("Exercise 5: Not implemented yet - fill in the TODOs!")


def exercise_6_merging_joining():
    """
    Exercise 6: Merge and join DataFrames.
    
    TODO:
    1. Inner join employees and departments on 'dept_id'
    2. Left join to keep all employees
    3. Outer join to keep all rows from both
    4. Concatenate two DataFrames vertically
    5. Concatenate two DataFrames horizontally
    
    HINTS:
    - pd.merge(df1, df2, on='col', how='inner')
    - how: 'inner', 'left', 'right', 'outer'
    - pd.concat([df1, df2], axis=0) for vertical
    - pd.concat([df1, df2], axis=1) for horizontal
    """
    print("\n" + "="*60)
    print("Exercise 6: Merging and Joining")
    print("="*60)
    
    employees = pd.DataFrame({
        'emp_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'dept_id': [101, 102, 101, 103, 102]
    })
    
    departments = pd.DataFrame({
        'dept_id': [101, 102, 104],
        'dept_name': ['Engineering', 'Sales', 'Marketing']
    })
    
    print("Employees:\n", employees)
    print("\nDepartments:\n", departments)
    
    # TODO: Inner join (only matching dept_ids)
    inner_join = None
    
    # TODO: Left join (all employees, matching departments)
    left_join = None
    
    # TODO: Outer join (all from both)
    outer_join = None
    
    # Additional DataFrames for concat
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    
    # TODO: Concatenate vertically
    vertical_concat = None
    
    # TODO: Concatenate horizontally
    horizontal_concat = None
    
    print("Exercise 6: Not implemented yet - fill in the TODOs!")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 3: PANDAS ESSENTIALS")
    print("="*60)
    print("\nPandas is essential for data manipulation.")
    print("Complete each exercise by filling in the TODO sections.")
    
    exercise_1_series_dataframe_creation()
    exercise_2_data_selection()
    exercise_3_data_manipulation()
    exercise_4_groupby_aggregation()
    exercise_5_handling_missing_data()
    exercise_6_merging_joining()
    
    print("\n" + "="*60)
    print("Complete the TODOs and run again to verify!")
    print("="*60)


if __name__ == "__main__":
    main()
