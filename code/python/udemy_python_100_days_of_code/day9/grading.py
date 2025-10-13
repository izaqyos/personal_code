student_scores = {
  "Harry": 81,
  "Ron": 78,
  "Hermione": 99, 
  "Draco": 74,
  "Neville": 62,
}

# 🚨 Don't change the code above 👆

#TODO-1: Create an empty dictionary called student_grades.
grades = ["Outstanding", "Exceeds Expecations", "Acceptable", "Fail"]
student_grades={}

#TODO-2: Write your code below to add the grades to student_grades.👇
for k,v in student_scores.items():
  if v<= 70:
    student_grades[k]=grades[3]
  elif 71<=v<=80:
    student_grades[k]=grades[2]
  elif 81<=v<=90:
    student_grades[k]=grades[1]
  elif 91<=v<=100:
    student_grades[k]=grades[0]
  else:
    print(f"grade {v} is greater than 100")
    

# 🚨 Don't change the code below 👇
print(student_grades)






