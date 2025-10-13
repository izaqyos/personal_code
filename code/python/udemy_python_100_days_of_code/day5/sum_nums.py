#Write your code below this row 👇
#sum even numbers between 1-100, this is arith sequence 2,4,6 with 50 elems 
# so should be (an+a1)*(n/2) == 102*25 = 2550
#but here we practice range so only using range:
sumnums = 0
for i in range(2,101,2):
  sumnums+=i 

print(sumnums)

