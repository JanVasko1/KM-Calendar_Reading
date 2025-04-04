# Import Libraries
import os
from glob import glob
from shutil import rmtree

from customtkinter import CTk

import Libs.GUI.Elements as Elements

# --------------------------------------------- Folders / Files --------------------------------------------- #
def Create_Folder(Configuration: dict, window: CTk|None, file_path: str) -> None:
    # Create Folder
    try: 
        os.makedirs(f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="File Manipulation", message=f"Not possible to create folder: {Error}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_Folder(Configuration: dict, window: CTk|None, file_path: str) -> None:
    # Create Folder
    try: 
        os.rmdir(path=f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="File Manipulation", message=f"Not possible to delete folder: {Error}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_Folders(Configuration: dict, window: CTk|None, file_path: str) -> None:
    try:
        rmtree(file_path)
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="File Manipulation", message=f"Not possible to delete folders: {Error}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_File(Configuration: dict, window: CTk|None, file_path: str) -> None:
    # Delete File
    try: 
        os.remove(path=f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="File Manipulation", message=f"Not possible to delete file: {Error}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_All_Files(Configuration: dict, window: CTk|None, file_path: str, include_hidden: bool) -> None:
    # Delete File
    try:
        files = glob(pathname=os.path.join(file_path, "*"), include_hidden=include_hidden)
        for file in files:
            os.remove(file)
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="File Manipulation", message=f"Not possible to delete all files: {Error}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Get_Downloads_File_Path(File_Name: str, File_postfix: str):
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    Destination_File = os.path.join(downloads_folder, os.path.basename(f"{File_Name}.{File_postfix}"))
    return Destination_File
