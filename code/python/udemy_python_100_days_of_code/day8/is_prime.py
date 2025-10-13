#Write your code below this line 👇

def prime_checker(number):
  import math
  if number == 1 or number ==2:
    return True
  for i in range(2, math.ceil(math.sqrt(number))):
    if number%i == 0:
      return False
  return True
  




#Write your code above this line 👆
    
#Do NOT change any of the code below👇
n = int(input("Check this number: "))
is_prime = prime_checker(number=n)
print(f"{n} is prime check {is_prime}")



