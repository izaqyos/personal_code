
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

