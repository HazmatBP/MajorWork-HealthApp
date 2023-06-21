# Written by Harry McGrath for Year 12 SDD, 2023
#? this colour of comment denotes weird shit that still works for some reason

# Importing libraries
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import *
import json
import os


appRunning = True   # variable is always true while the app is running


def save_on_closing():
    global appRunning
    print("Closing the program...")

    # writes the contents of the steps dictionary to a .json file
    json.dump(steps_dict, open( "saved_data.json", "w" ))

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
    if date_choice == "select_date":
        # return date from selector
        return formatted_date
    else:
        # return todays date 
        return datetime.today().strftime('%Y%m%d')

def insert_missing_dates(dictionary):
    
    sort_dict_by_key(dictionary)
    
    new_dictionary = {}
    keys = list(dictionary.keys())

    if not keys:
        # If the dictionary is empty, return an empty dictionary
        print("returning empty dict")
        return new_dictionary
    
    # Get the start and end dates from the dictionary
    start_date = datetime.strptime(keys[0], '%Y%m%d')
    end_date = datetime.strptime(keys[-1], '%Y%m%d')
    current_date = start_date

    # Iterate through the dates between start_date and end_date (inclusive)
    while current_date <= end_date:
        # Format the current date as YYYYMMDD
        date_str = current_date.strftime('%Y%m%d')

        # Check if the date exists in the dictionary
        if date_str in dictionary:
            # If the date exists, copy the corresponding value to the new dictionary
            new_dictionary[date_str] = dictionary[date_str]
        else:
            # If the date is missing, assign 0 as the value in the new dictionary
            new_dictionary[date_str] = 0

        # Move to the next date
        current_date += timedelta(days=1)

    return new_dictionary

def save_with_date(entry_widget, dictionary):

    # get user input from entry widget
    user_input = entry_widget.get()

    if user_input.isnumeric(): #only saves the data if the input is a number.

        user_input = int(user_input)
        # get current date
        current_date = get_date()

        # If the date being written to is already in the dictionary, this if statement will add the new value to the existing value instead of overwriting it.
        if current_date in dictionary:
            existing_value = dictionary.get(current_date)
            new_value = existing_value + user_input

            dictionary.update({current_date: new_value})

        else:
            dictionary.update({current_date: user_input})

        entry_widget.delete(0, END) # clear the entry box
        
        dictionary = sort_dict_by_key(dictionary)
        
        dictionary = insert_missing_dates(dictionary)
        
        # update the output box
        update_output_with_dict(output_message, dictionary, "Steps")
        
        # update the daily goal meter
        update_meter(steps_goal_meter, dictionary)


def update_output_with_dict(text_widget, dictionary, value_type): 
    # value_type is the prefix added before the value in the output.
    # For example, value_type = "Pushups" will give a result like 19/02/2023 - Pushups: 35
    
    text_widget.configure(state= "normal") # "opens" the text widget so its contents can be edited
    
    text_widget.delete(1.0, END) # deletes any text currently in the widget
    
    final_string = f"" # final string to be inserted into the widget
    
    for i in dictionary:
        #? i is the key, dictionary[i] is the corresponding value

        date_obj = datetime.strptime(i, '%Y%m%d') # parses the key as a datetime object
        
        readable_date = date_obj.strftime('%d/%m/%Y') # converts the date formatting back into a string, with a nice readable format
        
        final_string += f"{readable_date} - {value_type}: {dictionary[i]} \n" # adds the entry to the final string, with some nice formatting
    
    text_widget.insert(1.0, final_string)
    
    text_widget.configure(state= "disabled") # "closes" the text widget so that the user cannot modify its contents 
    

def reset_day(dictionary):

    # replaces today's current value with 0
    current_date = get_date()
    dictionary.update({current_date: 0})


    # update the output box
    update_output_with_dict(output_message, dictionary, "Steps")
    
    # update the daily goal meter
    update_meter(steps_goal_meter, dictionary)
    

def clear_dict_confirm(dictionary, message):
    # Display a confirmation dialog box
    response = messagebox.askquestion("Confirmation", message)

    # Check the user's response
    if response == 'yes':
        # Reset the history
        dictionary.clear()
    
    sort_dict_by_key(dictionary)
    
    insert_missing_dates(dictionary)
    
    # update the output box
    update_output_with_dict(output_message, dictionary, "Steps")
    
    # update the daily goal meter
    update_meter(steps_goal_meter, dictionary)
    
def save_on_key_press(event):

    # check if 'enter' key was pressed
    if event.keysym == 'Return':
        save_with_date(steps_entry, steps_dict)



# create main tkinter window
app = ttk.Window(themename = 'darkly', title="Steps Counter App")

# Bind the on_closing function to the "WM_DELETE_WINDOW" event
app.protocol("WM_DELETE_WINDOW", save_on_closing)



# create title
title = ttk.Label(app, text='Steps Counter App', font = 'Calibri 16 bold')
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

#? Reason why lambda is used: ttk classes require a function with no inputs in the "command" parameter,
#? and the workaround to this is using lambda to turn functions that have inputs into temporary inputless functions

# create save button
save_button = ttk.Button(input_frame, text='Save', command = lambda : save_with_date(steps_entry, steps_dict))
save_button.pack(side = 'left', padx = 5, pady = 5)

# create clear history button
clear_history_button = ttk.Button(input_frame, text = 'Clear History', command = lambda: clear_dict_confirm(steps_dict, "Are you sure you want to clear your steps history?"))
clear_history_button.pack(side = 'right', padx= 5, pady = 5)

# create reset day button
reset_day_button = ttk.Button(input_frame, text = 'Reset Day', command = lambda: reset_day(steps_dict))
reset_day_button.pack(side = 'right', padx= 5, pady = 5)

input_frame.pack(padx= 5, pady = 5)

# bind 'enter' key to save_to_file function
steps_entry.bind('<KeyPress>', save_on_key_press)

# create steps goal frame
steps_goal_frame = ttk.Labelframe(app, text = "Daily Goal")


steps_goal_meter = ttk.Meter(
    steps_goal_frame, 
    subtext = "Steps",
    meterthickness = 25,
    amounttotal = 8000,
    stripethickness = 4,
    bootstyle= SUCCESS
    # todo: change this so it uses .config(), as this method doesn't let you change the amounttotal later
    )
steps_goal_meter.pack(padx= 5, pady = 5)

steps_goal_frame.pack(side = "right", padx= 5, pady = 5)

def set_meter_total(meter_widget, total):
    meter_widget.configure(amounttotal= total)

def update_meter(meter, dictionary):
    current_date = datetime.today().strftime('%Y%m%d') # get current date
    
    # if the current date has an entry in the dictionary, set the meter to that value, otherwise set it to 0 
    try:
        value = dictionary[current_date]
    except:
        value = 0
        
    meter.configure(amountused = value)

# create output frame

output_frame = ttk.Labelframe(app, text = "Stats Log")

# create output message
output_message = ttk.Text(output_frame, state= "disabled", height= 12.4)
output_message.pack(padx= 5, pady = 5)

output_frame.pack(side = "left", padx= 5, pady = 5)





# load dictionary from file 
steps_dict = load_json_to_dict("saved_data.json")

# update the steps goal meter so it doesn't display 0 at first
update_meter(steps_goal_meter, steps_dict)

update_output_with_dict(output_message, steps_dict, "Steps")

while appRunning:
    app.update()
app.destroy()



