
def find_fun():
  text=str(input("enter text "))
  t_f=  False
  char=str(input("enter char "))
  I=0
  while (I==len(text)):
    if (text[I]==char):
      t_f=True            
    I+=1
  print("the index of the char you selected is:",(I-1))
find_fun()
