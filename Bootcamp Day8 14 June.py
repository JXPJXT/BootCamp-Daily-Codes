# Create a Tkinter window with a Text widget that allows users to enter and edit text. 

import tkinter as tk
from tkinter import messagebox

def show_text_content():
    content = text_widget.get("1.0", tk.END)  # Get all the text from the widget
    messagebox.showinfo("Text Content", content)

root = tk.Tk()
root.title("Text Widget Example")

# Create a Text widget
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(pady=20)

# Create a Button to display the content of the text widget
show_button = tk.Button(root, text="Show Text", command=show_text_content)
show_button.pack(pady=20)

root.mainloop()

# Create a Tkinter window with a Listbox widget displaying a list of items.

import tkinter as tk
from tkinter import messagebox

def show_selected_item():
    selected_item = listbox.get(listbox.curselection()[0])  # Get the selected item
    messagebox.showinfo("Selected Item", selected_item)

root = tk.Tk()
root.title("Listbox Example")

# Create a Listbox widget and populate it with items
listbox = tk.Listbox(root, height=6, width=20)
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
for item in items:
    listbox.insert(tk.END, item)
listbox.pack(pady=20)

# Create a Button to display the selected item
show_button = tk.Button(root, text="Show Selected", command=show_selected_item)
show_button.pack(pady=20)

root.mainloop()

# Create a Tkinter window with a Spinbox widget allowing users to select a number

import tkinter as tk
from tkinter import messagebox

def show_spinbox_value():
    value = spinbox.get()  # Get the selected value from the spinbox
    messagebox.showinfo("Selected Value", value)

root = tk.Tk()
root.title("Spinbox Example")

# Create a Spinbox widget
spinbox = tk.Spinbox(root, from_=1, to=10, width=5)
spinbox.pack(pady=20)

# Create a Button to display the selected value
show_button = tk.Button(root, text="Show Value", command=show_spinbox_value)
show_button.pack(pady=20)

root.mainloop()

# Create a Tkinter window with a ComboBox widget displaying a dropdown list of options.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def show_combobox_selection():
    selected_option = combobox.get()  # Get the selected option from the ComboBox
    messagebox.showinfo("Selected Option", selected_option)

root = tk.Tk()
root.title("Combobox Example")

# Create a ComboBox widget with options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
combobox = ttk.Combobox(root, values=options, width=20)
combobox.pack(pady=20)

# Create a Button to display the selected option
show_button = tk.Button(root, text="Show Selection", command=show_combobox_selection)
show_button.pack(pady=20)

root.mainloop()

