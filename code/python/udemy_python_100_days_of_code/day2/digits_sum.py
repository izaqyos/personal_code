# 🚨 Don't change the code below 👇
two_digit_number = input("Type a two digit number: ")
# 🚨 Don't change the code above 👆

####################################
##specific solution
#digit1 = int(two_digit_number[0])
#digit2 = int(two_digit_number[1])
#print(digit1+digit2)
#Write your code below this line 👇
#general case solution
two_digit_number = int(two_digit_number)
total = 0
while two_digit_number:
    least_digit = two_digit_number%10
    total+=least_digit
    two_digit_number //= 10 

print(total)
