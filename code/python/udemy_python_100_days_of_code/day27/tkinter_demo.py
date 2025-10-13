import tkinter

print("Demo of tkinter")
window = tkinter.Tk()
print("Setting title")
window.title("My First GUI Program")
window.minsize(width=500, height=300)

my_label = tkinter.Label(text="I am a label", font=("Arial", 24, "bold"))
my_label.pack()

print("Running mainloop")
window.mainloop()
