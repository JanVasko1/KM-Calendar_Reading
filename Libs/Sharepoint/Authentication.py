import sharepy
import json
import os

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

User_Name = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
Auth_Address = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Init_authentication() -> sharepy:
    try:
        s_aut = sharepy.connect(site=Auth_Address, username=User_Name)
        s_aut.save(filename=f"Operational\\SP_Auth.pkl")
    except Exception as Error:
        print(Error)
        s_aut = ""
        print("It is not possible to connect and save now, try later.")
    return s_aut

def Delete_Authentication() -> None:
    try:
        os.remove(filename=f"Operational\\SP_Auth.pkl")
    except:
        print("File is already deleted.")

def Authentication() -> sharepy:
    while True:
        # Authentication
        try:
            s_aut = sharepy.load(filename=f"Operational\\SP_Auth.pkl")
        except:
            s_aut = Init_authentication()

        # Check loop + check auth return value
        if s_aut == "":
            print("Not authenticated. Wrong password or try connect to Baracuda. ")
            Break = input(f"Do you want to stop loop? [Y/N]?")
            Break = Break.upper()
            if Break == "Y":
                break
            else:
                pass
        else:
            break
    
    return s_aut
