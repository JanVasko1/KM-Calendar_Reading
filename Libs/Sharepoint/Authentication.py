# Import Libraries
import sharepy
import os
import Libs.Defaults_Lists as Defaults_Lists

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Auth_Email = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
Auth_Address = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Init_authentication(SP_Password: str|None) -> sharepy:
    try:
        s_aut = sharepy.connect(site=Auth_Address, username=Auth_Email, password=SP_Password)
        s_aut.save(filename=f"Operational\\SP_Auth.pkl")
    except Exception as Error:
        CTkMessagebox(title="Error", message="It is not possible to connect and save now, try later.", icon="cancel", fade_in_duration=1)
        s_aut = ""
    return s_aut

def Delete_Authentication() -> None:
    try:
        os.remove(filename=f"Operational\\SP_Auth.pkl")
    except:
        CTkMessagebox(title="Info", message="Sharepoint authentification file already deleted", icon="cancel", fade_in_duration=1)

def Authentication(SP_Password: str|None) -> sharepy:
    while True:
        # Authentication
        try:
            s_aut = sharepy.load(filename=f"Operational\\SP_Auth.pkl")
        except:
            s_aut = Init_authentication(SP_Password=SP_Password)

        # Check loop + check auth return value
        if s_aut == "":
            msg = CTkMessagebox(title="Break Loop", message="Not authenticated. Wrong password or try connect to Baracuda. Do you want to stop loop?", icon="question", option_1="No", option_2="Yes")
            Break = msg.get()
            
            Break = Break.upper()
            if Break == "Yes":
                break
            else:
                pass
        else:
            break
    
    return s_aut
