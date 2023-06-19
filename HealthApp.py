# Written by Harry McGrath for Year 12 SDD, 2023
#? this colour of comment denotes weird shit that still works for some reason


import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import *
import json
import os


appRunning = True   # variable is always true while the app is running


def save_on_closing():
    global appRunning
    print("Closing the program...")

    # writes the contents of the steps dictionary to a .json file
    json.dump(steps_dict, open( "saved_data.json", 'w' ))

    # closes the window
    appRunning = False


def load_json_to_dict(file_path):
    if os.path.exists(file_path):
        # Check if the file is empty
        if os.stat(file_path).st_size == 0:
            # Create new JSON file with an empty dictionary
            output_dict = {}
            with open(file_path, "w") as file:
                json.dump(output_dict, file)
        else:
            # Load data from existing non-empty JSON file
            with open(file_path) as file:
                output_dict = json.load(file)
    else:
        # Create new JSON file with an empty dictionary
        output_dict = {}
        with open(file_path, "w") as file:
            json.dump(output_dict, file)

    return output_dict


def sort_dict_by_key(dictionary):
    keys = list(dictionary.keys()) # makes a list of all the keys in the dictionary
    keys.sort() # sorts said list of keys
    
    new_dict = {}
    for key in keys:
        new_dict[key] = dictionary[key] 
        # goes through the old dict and puts all their values in the correct positions in the new dict
        
    return new_dict

def get_date():

    selected_date = date_selector.entry.get()   #? weird internal object magic, is basically just get_date() except it actually works

    # Parse the input string as a datetime object
    date_obj = datetime.strptime(selected_date, '%d/%m/%Y')

    # Format the datetime object as "YYYYMMDD" string   #? this uses this horribly unreadable date formatting for easy dictionary sorting later
    formatted_date = date_obj.strftime('%Y%m%d')

    # check which radio button is selected
    date_choice = date_radio_var.get()

    # return either the date from the selector or todays date depending on radiobutton choice
    if date_choice == "current_date":
        # return date from selector
        print("selected date chosen") #! test print statements
        return formatted_date
    else:
        # return todays date 
        print("today's date chosen") #! test print statements
        return datetime.today().strftime('%Y%m%d')

def save_with_date(entry_widget, dictionary):

    # get user input from entry widget
    user_input = entry_widget.get()

    if user_input.isnumeric(): #only saves the data if the input is a number.

        user_input = int(user_input)
        #print(user_input) #todo dev print statement
        # get current date
        current_date = get_date()

        # If the date being written to is already in the dictionary, this if statement will add the new value to the existing value instead of overwriting it.
        if current_date in dictionary:
            existing_value = dictionary.get(current_date)
            new_value = existing_value + user_input

            dictionary.update({current_date: new_value})

        else:
            dictionary.update({current_date: user_input})

        #print(dictionary) #todo dev print statement

        entry_widget.delete(0, END) # clear the entry box


def update_widget_with_dict(text_widget, dictionary, value_type): 
    # value_type is the prefix added before the value in the output.
    # For example, value_type = "Pushups" will give a result like 19/02/2023 - Pushups: 35
    
    dictionary = sort_dict_by_key(dictionary) 
    
    text_widget.configure(state= "normal") # "opens" the text widget so its contents can be edited
    
    text_widget.delete(1.0, END) # deletes any text currently in the widget
    
    final_string = f"" # final string to be inserted into the widget
    
    for i in dictionary:
        #todo  i is the key, dictionary[i] is the corresponding value

        date_obj = datetime.strptime(i, '%Y%m%d') # parses the key as a datetime object
        
        readable_date = date_obj.strftime('%d/%m/%Y') # converts the date formatting back into a string, with a nice readable format
        
        final_string += f"{readable_date} - {value_type}: {dictionary[i]} \n" # adds the entry to the final string, with some nice formatting
    
    text_widget.insert(1.0, final_string)
    
    text_widget.configure(state= "disabled") # "closes" the text widget so that the user cannot modify its contents 
    #! needs finishing
    

def reset_day(dictionary):

    # replaces today's current value with 0
    current_date = get_date()
    dictionary.update({current_date: 0})
    #print(dictionary) #todo dev print statement

def save_on_key_press(event):

    # check if 'enter' key was pressed
    if event.keysym == 'Return':
        save_with_date(steps_entry, steps_dict)



# create main tkinter window
app = ttk.Window(themename = 'darkly')

# Bind the on_closing function to the "WM_DELETE_WINDOW" event
app.protocol("WM_DELETE_WINDOW", save_on_closing)



# create title
title = ttk.Label(app, text='Health App', font = 'Calibri 16 bold')
title.pack(padx = 10, pady = 5)

# create input frame
input_frame = ttk.Labelframe(app, text = "Steps Recorder")

# create date radiobutton
date_radio_var = ttk.StringVar()

date_radio_button1 = ttk.Radiobutton(input_frame, text="Current Date", variable = date_radio_var, value="current_date")
date_radio_button2 = ttk.Radiobutton(input_frame, text="Select Date:", variable = date_radio_var, value="select_date")

date_radio_button1.pack(padx = 5, pady = 5)
date_radio_button2.pack(padx = 5, pady = 5)

# create date selector
date_selector = ttk.DateEntry(input_frame)
date_selector.pack(side = 'left', padx = 5, pady = 5)

# create entry field
steps_entry = ttk.Entry(input_frame)
steps_entry.pack(side = 'left', padx = 5, pady = 5)

# create save button
save_button = ttk.Button(input_frame, text='Save', command = lambda : save_with_date(steps_entry, steps_dict))
save_button.pack(side = 'left', padx = 5, pady = 5)

# create reset button
reset_button = ttk.Button(input_frame, text = 'Reset Day', command = lambda: reset_day(steps_dict))
reset_button.pack(side = 'right', padx= 5, pady = 5)


input_frame.pack(padx= 5, pady = 5)

# bind 'enter' key to save_to_file function
steps_entry.bind('<KeyPress>', save_on_key_press)

# create output field
output_frame = ttk.Labelframe(app, text = "Stats Output")

output_message = ttk.Text(output_frame, state= "disabled")
output_message.pack(padx= 5, pady = 5)

output_frame.pack(padx= 5, pady = 5)




# load dictionary from file before anything else happens
steps_dict = load_json_to_dict("saved_data.json")

# Run app
while appRunning:
    app.update()
    update_widget_with_dict(output_message, steps_dict, "Steps")
app.destroy()





