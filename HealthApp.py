import ttkbootstrap as ttk
from datetime import date


def save_to_file(filename):
    # get user input from entry widget
    user_input = entry.get()

    # get current date
    current_date = date.today().strftime('%d/%m/%Y')

    # write user input and current date to file
    with open(filename, 'a') as file:
        file.write(f'{current_date}: {user_input}\n')

    # clear the text box
    entry.delete(0, 'end')


def reset_file(filename):
    # delete everything from the file
    open(filename, 'w').close()
    
    
def save_on_key_press(event):
    # check if 'enter' key was pressed
    if event.keysym == 'Return':
        save_to_file("saved_data.txt")

# create main tkinter window
root = ttk.Window(themename = 'darkly')

# create title
title = ttk.Label(root, text='Enter text to save:', font = 'Calibri 16 bold')
title.pack(padx = 10, pady = 5)


# create input field 
input_frame = ttk.Frame(root)

entry = ttk.Entry(input_frame)
entry.pack(side = 'left', padx = 5, pady = 5)

save_button = ttk.Button(input_frame, text='Save', command = lambda: save_to_file("saved_data.txt"))
save_button.pack(side = 'left', padx = 5, pady = 5)

reset_button = ttk.Button(input_frame, text = 'Reset', command = lambda: reset_file("saved_data.txt"))
reset_button.pack(side = 'right', padx= 5, pady = 5)

input_frame.pack(padx= 5, pady = 5)


# bind 'enter' key to save_to_file function
entry.bind('<KeyPress>', save_on_key_press)

# start main loop
root.mainloop()
