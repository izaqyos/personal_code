#!/usr/bin/env python3
"""
Day 3: Pandas Essentials - ANSWERS

Complete solutions for all Day 3 exercises.
"""

import pandas as pd
import numpy as np


def exercise_1_series_dataframe_creation():
    """Exercise 1: Create Series and DataFrames."""
    print("\n" + "="*60)
    print("Exercise 1: Series and DataFrame Creation - ANSWER")
    print("="*60)
    
    series_list = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
    print(f"Series from list:\n{series_list}\n")
    
    series_dict = pd.Series({'x': 1, 'y': 2, 'z': 3})
    print(f"Series from dict:\n{series_dict}\n")
    
    df_dict = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['NYC', 'LA', 'Chicago']
    })
    print(f"DataFrame from dict:\n{df_dict}\n")
    
    np.random.seed(42)
    array = np.random.randn(3, 4)
    df_array = pd.DataFrame(array, columns=['A', 'B', 'C', 'D'])
    print(f"DataFrame from array:\n{df_array}")


def exercise_2_data_selection():
    """Exercise 2: Select data from DataFrames."""
    print("\n" + "="*60)
    print("Exercise 2: Data Selection - ANSWER")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 75000, 55000, 70000],
        'department': ['HR', 'IT', 'IT', 'Sales', 'HR']
    })
    print(f"DataFrame:\n{df}\n")
    
    names = df['name']
    print(f"Names column:\n{names}\n")
    
    name_salary = df[['name', 'salary']]
    print(f"Name and salary:\n{name_salary}\n")
    
    rows_1_3 = df.iloc[1:4]
    print(f"Rows 1-3:\n{rows_1_3}\n")
    
    age_over_28 = df[df['age'] > 28]
    print(f"Age > 28:\n{age_over_28}\n")
    
    it_dept = df[df['department'] == 'IT']
    print(f"IT department:\n{it_dept}\n")
    
    high_earners = df.loc[df['salary'] >= 60000, ['name', 'salary']]
    print(f"High earners (>=60k):\n{high_earners}\n")
    
    loc_selection = df.loc[1:3, ['name', 'age']]
    print(f"Using .loc[1:3, ['name', 'age']]:\n{loc_selection}")


def exercise_3_data_manipulation():
    """Exercise 3: Add, modify, and delete columns."""
    print("\n" + "="*60)
    print("Exercise 3: Data Manipulation - ANSWER")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'salary': [50000, 60000, 75000, 55000]
    })
    print(f"Original:\n{df}\n")
    
    df['bonus'] = df['salary'] * 0.1
    print(f"Added bonus:\n{df}\n")
    
    df['senior'] = df['age'] >= 30
    print(f"Added senior:\n{df}\n")
    
    df = df.rename(columns={'salary': 'base_salary'})
    print(f"Renamed salary:\n{df}\n")
    
    df['total_comp'] = df['base_salary'] + df['bonus']
    print(f"Added total_comp:\n{df}\n")
    
    df = df.drop('bonus', axis=1)
    print(f"Dropped bonus:\n{df}\n")
    
    df = df.sort_values('age', ascending=False)
    print(f"Sorted by age desc:\n{df}\n")
    
    df = df.reset_index(drop=True)
    print(f"Reset index:\n{df}")


def exercise_4_groupby_aggregation():
    """Exercise 4: Group data and aggregate."""
    print("\n" + "="*60)
    print("Exercise 4: GroupBy and Aggregation - ANSWER")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
        'age': [25, 30, 35, 28, 32, 29],
        'salary': [50000, 60000, 75000, 55000, 70000, 58000],
        'department': ['HR', 'IT', 'IT', 'Sales', 'HR', 'Sales']
    })
    print(f"DataFrame:\n{df}\n")
    
    mean_salary = df.groupby('department')['salary'].mean()
    print(f"Mean salary by dept:\n{mean_salary}\n")
    
    emp_count = df.groupby('department').size()
    print(f"Employee count by dept:\n{emp_count}\n")
    
    multi_agg = df.groupby('department').agg({
        'salary': ['mean', 'min', 'max'],
        'age': 'mean'
    })
    print(f"Multiple aggregations:\n{multi_agg}\n")
    
    total_salary = df['salary'].sum()
    salary_pct = (df.groupby('department')['salary'].sum() / total_salary * 100).round(2)
    print(f"Salary percentage by dept:\n{salary_pct}\n")
    
    salary_range = df.groupby('department')['salary'].apply(lambda x: x.max() - x.min())
    print(f"Salary range by dept:\n{salary_range}")


def exercise_5_handling_missing_data():
    """Exercise 5: Handle missing data."""
    print("\n" + "="*60)
    print("Exercise 5: Handling Missing Data - ANSWER")
    print("="*60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, np.nan, 35, 28, np.nan],
        'salary': [50000, 60000, np.nan, 55000, 70000],
        'department': ['HR', 'IT', 'IT', np.nan, 'HR']
    })
    print(f"Original:\n{df}\n")
    
    missing_mask = df.isnull()
    print(f"Missing values mask:\n{missing_mask}\n")
    
    missing_count = df.isnull().sum()
    print(f"Missing count per column:\n{missing_count}\n")
    
    df_dropped = df.dropna()
    print(f"Dropped rows with NaN:\n{df_dropped}\n")
    
    df_copy = df.copy()
    df_copy['age'] = df_copy['age'].fillna(df_copy['age'].mean())
    print(f"Filled age with mean:\n{df_copy}\n")
    
    df_copy['department'] = df_copy['department'].fillna('Unknown')
    print(f"Filled department with 'Unknown':\n{df_copy}\n")
    
    df_ffill = df.copy()
    df_ffill['salary'] = df_ffill['salary'].ffill()
    print(f"Forward filled salary:\n{df_ffill}")


def exercise_6_merging_joining():
    """Exercise 6: Merge and join DataFrames."""
    print("\n" + "="*60)
    print("Exercise 6: Merging and Joining - ANSWER")
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
    
    print(f"Employees:\n{employees}\n")
    print(f"Departments:\n{departments}\n")
    
    inner_join = pd.merge(employees, departments, on='dept_id', how='inner')
    print(f"Inner join:\n{inner_join}\n")
    
    left_join = pd.merge(employees, departments, on='dept_id', how='left')
    print(f"Left join:\n{left_join}\n")
    
    outer_join = pd.merge(employees, departments, on='dept_id', how='outer')
    print(f"Outer join:\n{outer_join}\n")
    
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    
    vertical_concat = pd.concat([df1, df2], axis=0, ignore_index=True)
    print(f"Vertical concat:\n{vertical_concat}\n")
    
    horizontal_concat = pd.concat([df1, df2], axis=1)
    print(f"Horizontal concat:\n{horizontal_concat}")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 3: PANDAS ESSENTIALS - ANSWERS")
    print("="*60)
    
    exercise_1_series_dataframe_creation()
    exercise_2_data_selection()
    exercise_3_data_manipulation()
    exercise_4_groupby_aggregation()
    exercise_5_handling_missing_data()
    exercise_6_merging_joining()
    
    print("\n✓ All exercises completed!")


if __name__ == "__main__":
    main()
