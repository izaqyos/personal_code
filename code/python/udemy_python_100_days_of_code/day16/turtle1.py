from turtle import Turtle, Screen

t1 = Turtle()
t1.shape('turtle')
t1.color("DarkBlue")  #see https://rgbcolorpicker.com/
print(t1)

scr = Screen()
scr.canvheight = 800
scr.canvwidth = 600
t1.forward(500)
scr.exitonclick()

from prettytable import PrettyTable
pt = PrettyTable()
pt.field_names=["Pokemon Name", "Type"]
pt.add_row(["Pikachu", "Electric"])
pt.add_row(["Squirtale", "Water"])
pt.add_row(["Charmandar", "Fire"])
pt.align = "l"
print(pt)
