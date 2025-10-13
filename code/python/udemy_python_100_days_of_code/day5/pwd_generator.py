#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

total_chars = nr_letters+nr_symbols+nr_numbers
if total_chars <4:
  print(f"{nr_letters} is too short.")
  exit(0)
#Eazy Level - Order not randomised:
#e.g. 4 letter, 2 symbol, 2 number = JduE&!91


#Hard Level - Order of characters randomised:
#e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P

all_chars=[]
if nr_letters:
  all_chars.append([letters,nr_letters])
if nr_numbers:
  all_chars.append([numbers,nr_numbers])
if nr_symbols:
  all_chars.append([symbols,nr_symbols])
  
pwd=''

for i in range(total_chars):
  which_class=random.randint(0, len(all_chars)-1)
  letter=all_chars[which_class][0][random.randint(0,len(all_chars[which_class][0])-1)]
  all_chars[which_class][1]-=1
  if all_chars[which_class][1] == 0: #if it reached 0 we satisfied user requirement and we remove it from pool of candidate chars
    all_chars=all_chars[:which_class]+all_chars[which_class+1:]
  pwd+=letter

print(pwd)
  

