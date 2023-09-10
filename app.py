import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os
import sys

# Determine the file path in PyInstaller environment
if getattr(sys, 'frozen', False):
    # If the code is run by PyInstaller
    script_dir = sys._MEIPASS
else:
    # If the code is run directly from Python
    script_dir = os.path.dirname(__file__)

def check_base_scs(folder_path):
    base_scs_path = os.path.join(folder_path, "base.scs")
    
    if os.path.exists(base_scs_path):
        return True
    else:
        return False

def update_app():
    destination_folder = folder_var.get()
    
    if not destination_folder:
        messagebox.showerror('Error', 'Please select the right game folder containing the game with the base.scs file!')
        return
    
    source_folder = os.path.join(script_dir, "dlcs")
    
    # Use a Text widget to display progress messages
    text_widget.config(state='normal')  # Enable editing
    text_widget.delete(1.0, 'end')  # Clear previous messages

    def log_message(message):
        # Add messages to the text area
        text_widget.insert('end', message + '\n')
        text_widget.see('end')
        text_widget.update_idletasks()

    if check_base_scs(destination_folder):
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            
            # Check if the source is a directory
            if os.path.isdir(source_file):
                # Copy directory
                log_message(f'Copying directory: {source_file}')
                if os.path.exists(destination_file):
                    # If the destination directory already exists, copy only missing or updated files
                    for root, dirs, files in os.walk(source_file):
                        rel_root = os.path.relpath(root, source_folder)
                        dest_root = os.path.join(destination_folder, rel_root)
                        
                        if not os.path.exists(dest_root):
                            os.makedirs(dest_root)
                        
                        for file in files:
                            src_file = os.path.join(root, file)
                            dest_file = os.path.join(dest_root, file)
                            
                            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                                shutil.copy2(src_file, dest_file)
                else:
                    shutil.copytree(source_file, destination_file)
            else:
                # Copy file
                log_message(f'Copying file: {source_file}')
                if os.path.exists(destination_file):
                    if os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                        shutil.copy2(source_file, destination_file)
                else:
                    shutil.copy(source_file, destination_file)
            
        log_message('The DLCs have been installed successfully!')
    else:
        log_message('Please select the right game folder containing the game with the base.scs file!')
        return

root = tk.Tk()
root.title('Mosbymods.de - ETS2 DLC Updater to v1.48.1.6')
root.geometry('350x320')  # Set the window size
# Set window icon
icon_path = os.path.join(script_dir, 'icon.ico')
root.iconbitmap(icon_path)

# Folder Selector and Browse button
folder_frame = ttk.Frame(root)
folder_frame.pack(pady=20)
folder_label = ttk.Label(folder_frame, text='Select the game folder:')
folder_label.pack(side='left', padx=(0, 10))
folder_var = tk.StringVar()
folder_entry = ttk.Entry(folder_frame, textvariable=folder_var)
folder_entry.pack(side='left')

folder_button_icon_path = os.path.join(script_dir, 'browseicon.png')
folder_button_icon = tk.PhotoImage(file=folder_button_icon_path)
folder_button_icon = folder_button_icon.subsample(25)

folder_button = ttk.Button(folder_frame, text='Browse', image=folder_button_icon, compound='left',
                           command=lambda: folder_var.set(filedialog.askdirectory()))
folder_button.image = folder_button_icon
folder_button.pack(side='left', padx=(10, 0))

# Update button
update_button = ttk.Button(root, text='Install', command=update_app)
update_button.pack(pady=(0, 20))

# Create a text area for messages
text_widget = tk.Text(root, wrap='word', width=40, height=10, state='disabled')
text_widget.pack(padx=10, pady=10)

root.mainloop()
