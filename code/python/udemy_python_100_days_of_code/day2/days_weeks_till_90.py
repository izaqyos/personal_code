# 🚨 Don't change the code below 👇
age = input("What is your current age? ")
# 🚨 Don't change the code above 👆

#Write your code below this line 👇




# https://waitbutwhy.com/2014/05/life-weeks.html 
days_year = 365
weeks_year = 52
months_year = 12
target_age = 90
age = int(age)
#age = int(input("what is your current age? "))
age_diff_years = target_age-age
if age_diff_years<0:
    print("age must be smaller than or equal to 90")
    exit(0)
msg = f"You have {age_diff_years*days_year} days, {age_diff_years*weeks_year} weeks, and {age_diff_years*months_year} months left."
print(msg)
