# 🚨 Don't change the code below 👇
year = int(input("Which year do you want to check? "))
# 🚨 Don't change the code above 👆

#Write your code below this line 👇
"""
This is how you work out whether if a particular year is a leap year.

on every year that is evenly divisible by 4 

**except** every year that is evenly divisible by 100 

**unless** the year is also evenly divisible by 400
"""

msg= "eap year."
if year%4:
    print("Not l"+msg)
else:
    if year%100:
        print("L"+msg)
    else:
        if year%400:
            print("Not l"+msg)
        else:
            print("L"+msg)




