import sharepy
import json
import os

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

User_Name = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
Auth_Path = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Aut_parh"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Init_authentication() -> sharepy:
    try:
        s_aut = sharepy.connect("https://connectkonicaminolta.sharepoint.com", username=User_Name)
        s_aut.save(filename=f"{Auth_Path}ssp-session.pkl")
    except Exception as Error:
        print(Error)
        s_aut = ""
        print("It is not possible to connect and save now, try later.")
    return s_aut

def Delete_Authentication():
    try:
        os.remove(filename=f"{Auth_Path}ssp-session.pkl")
    except:
        print("File is already deleted.")