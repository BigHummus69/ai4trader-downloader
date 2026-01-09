import tkinter as tk
from tkinter import filedialog

###-----FILE WINDOW TESTING ------###

def exit_program():
    user_exit_input = input("Do you want to exit? Press Enter to confirm, and N to restart:")
    if user_exit_input == "":
        exit()
    elif user_exit_input.upper() == "N":
        select_directory()
    else:
        print("Invalid input. Please enter 'N' to restart or press Enter to exit.")
        exit_program()

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    user_directory_choice = input(   
        "\n"
        "Select Directory for Storing CSV Files? A few new folders will be created inside your selected directory, so make sure it's empty! Please answer "
        "Y for Yes, N for No: "
    )

    if user_directory_choice.upper() == 'Y':
        selected_dir = filedialog.askdirectory(title="Selected Directory for Storing CSV Files")
        print(selected_dir)
        exit_program()
    elif user_directory_choice.upper() == 'N':
        print("Directory selection cancelled by user.")
        exit_program()
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")
        select_directory()

select_directory()