# Import Libraries
from sharepy import SharePointSession, connect, load
import os

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements as Elements

from customtkinter import CTk

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Init_authentication(Settings: dict, Configuration: dict, window: CTk|None, SP_Password: str|None) -> SharePointSession:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    Auth_Address = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]

    try:
        s_aut = connect(site=Auth_Address, username=User_Email, password=SP_Password)
        s_aut.save(filename=Data_Functions.Absolute_path(relative_path=f"Operational\\SP_Auth.pkl"))
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="It is not possible to connect and save now, try later.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        s_aut = ""
    return s_aut

def Delete_Authentication(Configuration: dict, window: CTk|None) -> None:
    try:
        os.remove(filename=Data_Functions.Absolute_path(relative_path=f"Operational\\SP_Auth.pkl"))
    except:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Sharepoint authentication file already deleted", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Authentication(Settings: dict, Configuration: dict, window: CTk|None, SP_Password: str|None) -> SharePointSession:
    while True:
        # Authentication
        try:
            s_aut = load(filename=Data_Functions.Absolute_path(relative_path=f"Operational\\SP_Auth.pkl"))
        except:
            s_aut = Init_authentication(Settings=Settings, Configuration=Configuration, window=window, SP_Password=SP_Password)

        # Check loop + check auth return value
        if s_aut == "":
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message="Not authenticated. Wrong password or try connect to Baracuda. Do you want to stop loop?", icon="question", option_1="No", option_2="Yes", fade_in_duration=1, GUI_Level_ID=1)
            
            response = response.upper()
            if response == "Yes":
                break
            else:
                pass
        else:
            break
    
    return s_aut
