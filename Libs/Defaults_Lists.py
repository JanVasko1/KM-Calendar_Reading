# Import Libraries
from pandas import DataFrame
import json

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