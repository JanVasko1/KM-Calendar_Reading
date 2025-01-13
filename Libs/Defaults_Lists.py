# Import Libraries
from pandas import DataFrame
from dotenv import load_dotenv
import json
import os

from CTkMessagebox import CTkMessagebox

def Load_Settings() -> dict:
    File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
    Settings = json.load(fp=File)
    File.close()
    return Settings

def Load_Configuration() -> dict:
    File = open(file=f"Libs\\GUI\\Configuration.json", mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Load_Figures(Theme:str) -> dict:
    File = open(file=f"Libs\\GUI\\Figure_settings_{Theme}.json", mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Busy_Status_List() -> list[str]:
    Busy_Stuses = ["Free", "Tentative", "Busy", "Out of Office", "Working elsewhere"]
    return Busy_Stuses

def Exchange_Busy_Status_List() -> list[str]:
    Busy_Stuses = ["free", "tentative", "busy", "oof", "workingElsewhere", "unknown"]
    return Busy_Stuses

def Busy_Status_Priorities_List() -> list[str]:
    # Smaller Index = Higher priority
    Busy_Stuses_Priorities = ["Busy", "Working elsewhere", "Tentative", "Free", "Out of Office"]
    return Busy_Stuses_Priorities

def Dataframe_sort(Sort_Dataframe: DataFrame, Columns_list: list, Accenting_list: list) -> None:
    # Sort Dataframe and reindex 
    Sort_Dataframe.sort_values(by=Columns_list, ascending=Accenting_list, axis=0, inplace = True)
    Sort_Dataframe.reset_index(inplace=True)
    Sort_Dataframe.drop(labels=["index"], inplace=True, axis=1)
    return Sort_Dataframe

def Load_Exchange_env() -> list[str, str, str]:
    load_dotenv(dotenv_path=f"Libs\\Download\\Exchange.env")
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    tenant_id = os.getenv("tenant_id")
    return client_id, client_secret, tenant_id

def Information_Update_Settings(File_Name: str, JSON_path: list, Information: int|str|list|dict) -> None:
    def update_value(File_dict: dict, JSON_path: list, Information: int|str|list|dict) -> None:
        # Must be in local function !!!!
        for key in JSON_path[:-1]:
            File_dict = File_dict[key]
        File_dict[JSON_path[-1]] = Information

    try:
        # Load File
        if File_Name == "Settings":
            File_dict = Load_Settings()
        elif File_Name == "Configuration":
            File_dict = Load_Configuration()
        else:
            pass

        # Update values
        update_value(File_dict=File_dict, JSON_path=JSON_path, Information=Information)
        
        # Save in Settings.json
        if File_Name == "Settings":
            with open(f"Libs\\Settings.json", mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=File_dict, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        elif File_Name == "Configuration":
            with open(f"Libs\\GUI\\Configuration.json", mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=File_dict, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        else:
            pass
            
    except Exception as Error:
        CTkMessagebox(title="Error", message=f"Not possible to udpate {Information} into Field: {JSON_path} of {File_Name}", icon="cancel", fade_in_duration=1)

def Delete_File(file_path: str) -> None:
    # Delete File before generation
    try: 
        os.remove(path=f"{file_path}")
    except:
        pass