import readchar
print("Welcome to the Health App!  \nPress any key to start:")
key = readchar.readkey()

if key:
    print("""What do you want to do?
Press 1 to add new activity:
Press 2 to view stats:
Press 3 to exit:\n""")
    
else:
    exit()