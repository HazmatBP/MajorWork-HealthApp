import ttkbootstrap as ttk
from datetime import *


def save_with_date(filename, entry_widget):
    # get user input from entry widget
    user_input = entry_widget.get()
    print(user_input)
    # get current date
    current_date = datetime.now().strftime('%d%m%Y')

    # write user input and current date to file
    with open(filename, 'a') as file:
        file.write(f'{current_date}-{user_input}\n')
        
    entry_widget.delete(0, "end")


def read_dateinfo_from_file(file_path):
    date_dict = {}
    
    with open(file_path, "r") as file:
        lines = file.readlines()
        split_line = [] # temporary array used to split the datestamp and value into seperate values  
        
        for i in range(len(lines)):
            split_line = lines[i].split("-") 
            date_dict.update({split_line[0], split_line[1]}) # adds a key:value pair to the dictionary, with the datestamp as the key and the value as the value
            
    file_path.close()  
    return date_dict

    
def reset_file(filename):
    # delete everything from the file
    open(filename, 'w').close()
    
    
def save_on_key_press(event):
    # check if 'enter' key was pressed
    if event.keysym == 'Return':
        save_with_date("saved_data.txt", entry)

# create main tkinter window
app = ttk.Window(themename = 'darkly')

# create title
title = ttk.Label(app, text='Enter text to save:', font = 'Calibri 16 bold')
title.pack(padx = 10, pady = 5)


# create input field 
input_frame = ttk.Labelframe(app, text = "Input")

entry = ttk.Entry(input_frame)
entry.pack(side = 'left', padx = 5, pady = 5)


save_button = ttk.Button(input_frame, text='Save', command = lambda : (save_with_date("saved_data.txt", entry.get(), entry)))

save_button.pack(side = 'left', padx = 5, pady = 5)

reset_button = ttk.Button(input_frame, text = 'Reset', command = lambda: reset_file("saved_data.txt"))
reset_button.pack(side = 'right', padx= 5, pady = 5)

input_frame.pack(padx= 5, pady = 5)

# bind 'enter' key to save_to_file function
entry.bind('<KeyPress>', save_on_key_press)




# create output field
output_frame = ttk.Labelframe(app, text = "Stats Output")

output_message = ttk.Text(output_frame, state = 'disabled')
output_message.pack(padx= 5, pady = 5)

output_frame.pack(padx= 5, pady = 5)

# start main loop
app.mainloop()
