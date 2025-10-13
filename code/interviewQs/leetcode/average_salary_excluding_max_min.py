"""
Average Salary Excluding the Minimum and Maximum Salary
You are given an array of unique integers salary where salary[i] is the salary of the ith employee.

Return the average salary of employees excluding the minimum and maximum salary. Answers within 10^-5 of the actual answer will be accepted.

 

Example 1:

Input: salary = [4000,3000,1000,2000]
Output: 2500.00000
Explanation: Minimum salary and maximum salary are 1000 and 4000 respectively.
Average salary excluding minimum and maximum salary is (2000+3000) / 2 = 2500
Example 2:

Input: salary = [1000,2000,3000]
Output: 2000.00000
Explanation: Minimum salary and maximum salary are 1000 and 3000 respectively.
Average salary excluding minimum and maximum salary is (2000) / 1 = 2000
 

Constraints:

3 <= salary.length <= 100
1000 <= salary[i] <= 10^6
All the integers of salary are unique.
"""

class Solution:
    def average(self, salary: List[int]) -> float:
        if len(salary) < 3:
            return 0
        n = len(salary)
        min_salary, max_salary = float('inf'), float('-inf')
        total = 0
        for s in salary:
            if s<min_salary:
                min_salary = s
            if s>max_salary:
                max_salary = s
            total += s
        total -= min_salary+max_salary
        return total/(n-2)


