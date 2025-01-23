import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import subprocess

# VARIABLES
# ---------
source_name = ""
source_name_exe = ""
file_path_exe = ""
file_path_iwad = ""
file_path_file = ""
script_result = ""

def submit_source():
    global source_name, source_name_exe
    try:
        user_input = simpledialog.askstring("Enter source port", "Insert source port name. If a Flatpak, write as named on Flathub (i.e.: flatpak run org.zdoom.GZDoom)")  # Get the source port name
        if user_input:  # Check if user input is not None
            # Split the input into components based on '/' 
            components = user_input.split('/')
            # Add quotes around components that contain spaces
            formatted_components = [f"'{component}'" if ' ' in component else component for component in components]
            # Join the components back together - so that the script finds the correct filepath
            formatted_path = '/'.join(formatted_components)
            print(f"You entered: {formatted_path}")
            source_name = formatted_path
        else:
            messagebox.showinfo("Information", "No input provided.")
    except Exception as e:
        messagebox.showinfo("Information", f"An error occurred: {e}")
        
def submit_source_exe():
    global source_name, source_name_exe, file_path_exe
    file_path_exe = filedialog.askopenfilename(title="Select a .exe file")
    if file_path_exe:  # Check if a file was selected
        # Format the path to handle spaces
        file_path_exe = format_path(file_path_exe)
        print(file_path_exe)

def format_path(path):
    # Split the input into components based on '/'
    components = path.split('/')
    # Add quotes around components that contain spaces
    formatted_components = [f"'{component}'" if ' ' in component else component for component in components]
    # Join the components back together
    return '/'.join(formatted_components)

def pick_iwad():  # Open the file picker dialog
    global file_path_iwad
    file_path_iwad = filedialog.askopenfilename(title="Select a IWAD file")
    if file_path_iwad:  # Check if a file was selected
        # Format the path to handle spaces
        file_path_iwad = " -iwad " + format_path(file_path_iwad)
        print(file_path_iwad)

def pick_file():  # Open the file picker dialog
    global file_path_file
    new_file_path = filedialog.askopenfilename(title="Select a mod file")
    if new_file_path:  # Check if a file was selected and append the new file path to the existing string
        # Format the new file path to handle spaces
        new_file_path = format_path(new_file_path)
        if file_path_file:  # If there's already a file path, append with a space
            file_path_file += " " + " -file " + new_file_path
        else:  # If it's the first file being added
            file_path_file = " -file " + new_file_path
        print(file_path_file)

def unite():
    global script_result, source_name, source_name_exe, file_path_exe
    if source_name == "":
        source_name = file_path_exe
        script_result = source_name + (file_path_iwad if file_path_iwad else "") + (file_path_file if file_path_file else "")
    script_result = source_name + (file_path_iwad if file_path_iwad else "") + (file_path_file if file_path_file else "")
    print(script_result)
    result.set(script_result)  # Update the StringVar to reflect the new result
    result_show.config(text=script_result)  # Update the label to show the new result
    
def save_to_file():
    global script_result
    if script_result:
        file_path = filedialog.asksaveasfilename(defaultextension=".sh", filetypes=[("shellscript", "*.sh"), ("Windows Batch file", "*bat"), ("All files", "*.*")])
        if file_path:  # Check if the user selected a file
            with open(file_path, 'w') as file:
                # Determine the default text based on the file extension
                if file_path.endswith('.sh'):
                    default_text = "#!/usr/bin/bash\n"
                    subprocess.run(['chmod', '+x', file_path], check=True)
                    print (f"{file_path} is now executable.")
                elif file_path.endswith('.bat'):
                    default_text = "@echo off\n"
            # Write the default text to the first line
                file.write(default_text)
                # Write the content of script_result
                file.write(script_result)
            messagebox.showinfo("Information", "File saved successfully.")
    else:
        messagebox.showinfo("Information", "No content to save.")
        
# ---

def about_info():
    tk.messagebox.showinfo(title='About doom-to-sh',
                           message="Program to create shellscripts and batch files for Doom modding. \n"
                                   "Version: 0.0.1 \n"
                                   "made by emexis \n"
                           )

# GUI
# ---
# Main window
root = tk.Tk()
root.title("doom-to-sh")

# Field to add the source port (GZDoom, Crispy, etc.) - Linux
source_entry_button = tk.Button(root, text="1 - Specify Source Port - Linux", command=submit_source)
source_entry_button.pack(pady=10)

# Button to add a .exe filepath instead - Windows
source_entry_exe_button = tk.Button(root, text="(Alt) Specify Source Port - .exe ", command=submit_source_exe)
source_entry_exe_button.pack(pady=10)

# Button to add WADs with -iwad flag
add_button_file = tk.Button(root, text="2 + Add IWAD file", command=pick_iwad)
add_button_file.pack(pady=10)

# Button to add files with -file flag
add_button_file = tk.Button(root, text="3 + Add mod files", command=pick_file)
add_button_file.pack(pady=10)

# Show result
update_result = tk.Button(root, text="Update Script", command=unite)
update_result.pack(pady=10)

result = tk.StringVar()
result.set("Result will be shown here")  # Initial message

result_show = tk.Label(root, textvariable=result, wraplength=300)
result_show.pack(pady=20)

# Save result to file button
save_button = tk.Button(root, text="Save to File", command=save_to_file)
save_button.pack(pady=10)

#
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=10, pady=10)

# about button
about_button = tk.Button(root, text='about', command=about_info)
about_button.pack(side='right', padx=10)

# Tkinter event loop
root.mainloop()
