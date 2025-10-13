import tkinter as tk

# Create the main application window
root = tk.Tk()

# Set the title of the window
root.title("Hello Tkinter")

# Create a label widget
label = tk.Label(root, text="Hello, World!")

# Pack the label into the window
label.pack()

# Run the application loop
root.mainloop()
