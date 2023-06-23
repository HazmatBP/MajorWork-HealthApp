# Written by Harry McGrath for Year 12 SDD, 2023
#? this colour of comment denotes unintuitive snippets of code that need extra explanation

# Importing libraries
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import *
import json
import os

# Importing matplotlib stuff
import matplotlib
matplotlib.use('TkAgg') # tells matplotlib to use the backend built for tkinter

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

appRunning = True   # variable is always true while the app is running

#* DEFINING FUNCTIONS

def save_on_closing():
    global appRunning
    global steps_dict
    global steps_goal
    
    print("Closing the program...")
    
    steps_dict = insert_missing_dates(steps_dict) # adds missing dates to the dict before it gets saved
    
    json_data = {
        "steps_dict" : steps_dict,
        "steps_goal" : steps_goal
    }
    
    # writes the contents of the steps dictionary to a .json file
    json.dump(json_data, open( "saved_data.json", "w" ))

    # closes the window
    appRunning = False


def load_json_data(file_path):
    if os.path.exists(file_path):
        # Check if the file is empty
        if os.stat(file_path).st_size == 0:
            # Create new JSON file with an empty dictionary if file is empty
            output_data = {"steps_dict": {}, "steps_goal": 8000} #? 8000 is used as the default steps goal value 
            with open(file_path, "w") as file:
                json.dump(output_data, file)
        else:
            # Load data from existing non-empty JSON file
            with open(file_path) as file:
                output_data = json.load(file)
    else:
        # Create new JSON file with an empty dictionary and variable
        output_data = {"steps_dict": {}, "steps_goal": 8000} #? 8000 is used as the default steps goal value 
        with open(file_path, "w") as file:
            json.dump(output_data, file)

    return output_data["steps_dict"], output_data["steps_goal"]


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
        
        entry_widget.configure(bootstyle="primary") # changes the entry widget colour to the "primary" colour, to show that the input is correct
        
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
        update_meter(steps_meter, dictionary)
    else:
        entry_widget.configure(bootstyle="danger") # changes the entry widget colour to red, to show that the input is incorrect
        
    return dictionary

def update_output_with_dict(text_widget, dictionary, value_type): 
    # value_type is the prefix added before the value in the output.
    # For example, value_type = "Pushups" will give a result like 19/02/2023 - Pushups: 35
    
    text_widget.configure(state = NORMAL) # "opens" the text widget so its contents can be edited
    
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
    update_meter(steps_meter, dictionary)
    

def clear_dict_confirm(dictionary, message):
    # Display a confirmation dialog box
    response = messagebox.askquestion("Confirmation", message)

    # Check the user's response
    if response == 'yes':
        # Reset the history
        dictionary.clear()
    
  
    # update the output box
    update_output_with_dict(output_message, dictionary, "Steps")
    
    # update the daily goal meter
    update_meter(steps_meter, dictionary)
    
def save_on_key_press(event):

    # check if 'enter' key was pressed
    if event.keysym == 'Return':
        save_with_date(steps_entry, steps_dict)


def update_meter(meter, dictionary):
    current_date = datetime.today().strftime('%Y%m%d') # get current date
    
    # if the current date has an entry in the dictionary, set the meter to that value, otherwise set it to 0 
    try:
        value = dictionary[current_date]
    except:
        value = 0
        
    meter.configure(amountused = value)

def set_meter_total(meter_widget, total, total_prefix_string):
    global steps_goal
    
    meter_widget.configure(amounttotal= total)
    edit_step_goal_text.configure(text= f"{total_prefix_string} {total}")
    steps_goal = total
    


def steps_goal_popup():
    global popup

    def confirm_action():
        
        input_value = popup_entry.get()

        set_meter_total(steps_meter, input_value, "Steps Goal: ")
        # Close the popup window after executing the desired action
        popup.destroy()

    def cancel_action():
        # Function to be executed when the Cancel button is clicked
        
        # Close the popup window without taking any action
        popup.destroy()

    popup = ttk.Toplevel(app)
    popup.geometry("250x150")
    popup.title("Edit Steps Goal")

    popup_title = ttk.Label(popup, text="Edit Steps Goal:", font='Calibri 16 bold', bootstyle=SUCCESS)
    popup_title.pack(pady="10")

    popup_entry = ttk.Entry(popup)
    popup_entry.pack(pady=10)

    buttons_frame = ttk.Frame(popup)

    cancel_button = ttk.Button(buttons_frame, text="Cancel", bootstyle=SUCCESS, command=cancel_action)
    cancel_button.pack(side=LEFT, padx=10, pady=5)

    confirm_button = ttk.Button(buttons_frame, text="Confirm", bootstyle=SUCCESS, command=confirm_action)
    confirm_button.pack(side=RIGHT, padx=10, pady=5)

    buttons_frame.pack()
    
    popup.grab_set()
    popup.lift()


#* CREATING WIDGETS

# create main tkinter window
app = ttk.Window(themename = 'darkly', title="Steps Counter App")

# Bind the on_closing function to the "WM_DELETE_WINDOW" event
app.protocol("WM_DELETE_WINDOW", save_on_closing)



# create title
title = ttk.Label(app, text='Steps Counter App', font = 'Calibri 16 bold')
title.pack(padx = 10, pady = 5)

# create date selector frame
date_frame = ttk.Labelframe(app, text= "Date Selection")

# create date radiobutton
date_radio_var = ttk.StringVar()

date_radio_button1 = ttk.Radiobutton(date_frame, text="Current Date", variable = date_radio_var, value="current_date")
date_radio_button2 = ttk.Radiobutton(date_frame, text="Select Date:", variable = date_radio_var, value="select_date")

date_radio_button1.pack(side=LEFT, padx = 5, pady = 5)
date_radio_button2.pack(side=LEFT, padx = 5, pady = 5)

date_frame.pack(side=TOP)

# create date selector
date_selector = ttk.DateEntry(date_frame)
date_selector.pack(side = RIGHT, padx = 5, pady = 5)

# create tabs notebook
notebook = ttk.Notebook(app)
notebook.pack(padx = 10, pady = 10,)

logging_tab = ttk.Frame(notebook, width=400, height=280)

graph_tab = ttk.Frame(notebook, width=400, height=280)

logging_tab.pack(fill='both', expand=True)
graph_tab.pack(fill='both', expand=True)

notebook.add(logging_tab, text='Exercise Logging')
notebook.add(graph_tab, text='Statistics View')



# create input frame
input_frame = ttk.Labelframe(logging_tab, text = "Steps Recorder")

# create entry field
steps_entry = ttk.Entry(input_frame)
steps_entry.pack(side = LEFT, padx = 5, pady = 5)

#? Reason why lambda is used: ttk classes require a function with no inputs in the "command" parameter,
#? and the workaround to this is using lambda to turn functions that have inputs into temporary inputless functions

# create save button
save_button = ttk.Button(input_frame, text='Save', command = lambda : save_with_date(steps_entry, steps_dict), bootstyle=SUCCESS)
save_button.pack(side = LEFT, padx = 5, pady = 5)

# create clear history button
clear_history_button = ttk.Button(input_frame, text = 'Clear History', command = lambda: clear_dict_confirm(steps_dict, "Are you sure you want to clear your steps history?"), bootstyle=SUCCESS)
clear_history_button.pack(side = RIGHT, padx= 5, pady = 5)

# create reset day button
reset_day_button = ttk.Button(input_frame, text = 'Reset Day', command = lambda: reset_day(steps_dict), bootstyle=SUCCESS)
reset_day_button.pack(side = RIGHT, padx= 5, pady = 5)

input_frame.pack(padx= 5, pady = 5)

# bind 'enter' key to save_to_file function
steps_entry.bind('<KeyPress>', save_on_key_press)

# create steps goal frame
steps_meter_frame = ttk.Labelframe(logging_tab, text = "Daily Goal")

# create steps goal meter
steps_meter = ttk.Meter(
    steps_meter_frame, 
    subtext = "Steps",
    meterthickness = 25,
    amounttotal = 666, # if the total is actually 666 upon loading the window, Harry's probably messed something up
    stripethickness = 4,
    bootstyle= SUCCESS,
    metersize= 210,
    textfont="Helvetica 20 bold",
    subtextfont="bold"
    )

steps_meter.pack(padx= 5, pady = 5)




# steps goal editor section 
steps_goal_editor_frame = ttk.Frame(steps_meter_frame) # creates an invisible frame so that the edit goal text and button can be placed properly

# set steps goal value
steps_goal = 8000 

edit_step_goal_text = ttk.Label(steps_goal_editor_frame, text= f"Steps Goal: {steps_goal}", font="helvetica 10 bold")
edit_step_goal_text.pack(side = LEFT, padx= 5, pady = 5)

edit_step_goal_button = ttk.Button(steps_goal_editor_frame, text = "Edit Goal", bootstyle = SUCCESS, command = steps_goal_popup)
edit_step_goal_button.pack(side = RIGHT, padx= 5, pady = 5)

steps_goal_editor_frame.pack(padx= 5, pady = 5)
steps_meter_frame.pack(side = RIGHT, padx= 5, pady = 5)


# create output frame

output_frame = ttk.Labelframe(logging_tab, text = "Steps Log")

# create output message
output_message = ttk.Text(output_frame, state= DISABLED, height= 12.5, font = "Calibri 12")
output_message.pack(padx= 5, pady = 5)

output_frame.pack(side = LEFT, padx= 5, pady = 5)



# create a figure
figure = Figure(figsize=(6, 4), dpi=100)

canvas = FigureCanvasTkAgg(figure, graph_tab)

canvas.draw()
canvas.get_tk_widget().pack()


#* RUNTIME SETUP

# load values from file 
steps_dict, steps_goal = load_json_data("saved_data.json")

# Set the initial steps meter total value to be the steps_goal loaded from the .json file
set_meter_total(steps_meter, steps_goal, "Steps Goal: ")

# update the steps goal meter so it doesn't display 0 at first
update_meter(steps_meter, steps_dict)

# update the output box so it loads the info from the dictionary
update_output_with_dict(output_message, steps_dict, "Steps")


date_radio_var.set("current_date") # this makes the "current date" option in the date selector be selected by default

while appRunning:
    app.update()
app.destroy()



