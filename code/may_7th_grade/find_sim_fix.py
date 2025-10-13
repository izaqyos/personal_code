def find_fun():
  text=str(input("enter text "))
  char=str(input("enter char "))
  i=0
  fi = -1
  while (i<len(text)):
    if (text[i]==char):
        fi = i
    i+=1
  print("the index of the char you selected is:",fi)
find_fun()
