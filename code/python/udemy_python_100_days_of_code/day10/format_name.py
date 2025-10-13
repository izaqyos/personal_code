def format_name(fname, lname):
  retname= fname+" "+lname
  return retname.title()

def main():
  names = [('yosi', 'izaq'), ('guy', 'hanan')]
  expected = ['Yosi Izaq', 'Guy Hanan']
  res=[]
  for name in names:
    print(f"formatting {name}")
    res.append(format_name(name[0], name[1]))
  for exp, res in zip(expected, res):
    print(f"formated name is {res}")
    assert(exp == res)

main()

