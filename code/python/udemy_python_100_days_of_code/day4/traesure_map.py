# 🚨 Don't change the code below 👇
row1 = ["⬜️","️⬜️","️⬜️"]
row2 = ["⬜️","⬜️","️⬜️"]
row3 = ["⬜️️","⬜️️","⬜️️"]
map = [row1, row2, row3]
print(f"{row1}\n{row2}\n{row3}")
position = input("Where do you want to put the treasure? ")
print(position)
# 🚨 Don't change the code above 👆

#Write your code below this row 👇
def is_valid_digit(length, digit):
    return 0 < digit <= length
        

digit1 = int(position[0])
digit2 = int(position[1])
if is_valid_digit(len(row1), digit1) and is_valid_digit(len(map), digit2):
    #print(f"{digit2-1}{digit1-1}")
    map[digit2-1][digit1-1] = 'X'
else:
    print(f"you chose {digit1}, {digit2} - please select digit in range 1-{len(map)}")



#Write your code above this row 👆

# 🚨 Don't change the code below 👇
print(f"{row1}\n{row2}\n{row3}")

