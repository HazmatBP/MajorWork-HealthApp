import tkinter as tk
from datetime import date

def save_to_file():
    # get user input from entry widget
    user_input = entry.get()

    # get current date
    current_date = date.today().strftime("%d/%m/%Y")

    # write user input and current date to file
    with open('saved_data.txt', 'a') as file:
        file.write(f"{current_date}: {user_input}\n")

    # clear the text box
    entry.delete(0, 'end')

def on_key_press(event):
    # check if "enter" key was pressed
    if event.keysym == 'Return':
        save_to_file()

# create main tkinter window
root = tk.Tk()

# create input entry box and label
label = tk.Label(root, text='Enter text to save:')
label.pack()
entry = tk.Entry(root)
entry.pack()

# create save button
button = tk.Button(root, text='Save', command=save_to_file)
button.pack()

# bind "enter" key to save_to_file function
entry.bind('<KeyPress>', on_key_press)

# start main loop
root.mainloop()
