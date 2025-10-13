import tkinter as tk
from tkinter import ttk

def show_message():
    """Displays a message in the label when the button is clicked."""
    label.config(text="Button clicked!")

# Create main window
root = tk.Tk()
root.title("Tkinter Widget Demo")

# --- Labels ---
label = tk.Label(root, text="This is a label.")
label.pack(pady=10)

# --- Buttons ---
button = tk.Button(root, text="Click Me", command=show_message)
button.pack()

# --- Entry ---
entry = tk.Entry(root)
entry.pack(pady=10)

# --- Text ---
text = tk.Text(root, height=5, width=30)
text.pack()

# --- Listbox ---
listbox = tk.Listbox(root)
listbox.insert(1, "Item 1")
listbox.insert(2, "Item 2")
listbox.insert(3, "Item 3")
listbox.pack(pady=10)

# --- Radiobuttons ---
radio_var = tk.StringVar(value="Option 1")
radio1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value="Option 1")
radio2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value="Option 2")
radio1.pack()
radio2.pack()

# --- Checkbutton ---
check_var = tk.BooleanVar()
checkbutton = tk.Checkbutton(root, text="Check me", variable=check_var)
checkbutton.pack(pady=10)

# --- Scale ---
scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
scale.pack()

# --- Progressbar ---
progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progressbar.pack(pady=10)

# --- Combobox ---
combo = ttk.Combobox(root, values=["Choice 1", "Choice 2", "Choice 3"])
combo.pack()

# --- Spinbox ---
spinbox = tk.Spinbox(root, from_=0, to=10)
spinbox.pack(pady=10)

# --- Menu ---
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open")
filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# --- Canvas ---
canvas = tk.Canvas(root, width=200, height=100)
canvas.create_rectangle(50, 25, 150, 75, fill="blue")
canvas.pack(pady=10)

# Run the main loop
root.mainloop()
