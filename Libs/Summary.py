from pandas import DataFrame
import pandas
import json

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Personnel_number = Settings["General"]["Person"]["Code"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Dataframe_sort(Dataframe: DataFrame) -> None:
    # Sort Dataframe and reindex 
    Dataframe.sort_values(by=["Date", "Start Time"], ascending=[True, True], axis=0, inplace = True)
    Dataframe.reset_index(inplace=True)
    Dataframe.drop(labels=["index"], inplace=True, axis=1)

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Generate_Summary(Events: DataFrame) -> DataFrame:
    #Update Events Dataframe
    Events["Personnel number"] = Personnel_number
    Events["Start_Time"] = Events["Start_Time"].astype(str)
    Events["End_Time"] = Events["End_Time"].astype(str)
    Events[["Start_Date_Del", "Start_Time"]] = Events["Start_Time"].str.split(" ", expand=True)
    Events[["End_Date_Del", "End_Time"]] = Events["End_Time"].str.split(" ", expand=True)
    Events["Start_Time"] = Events["Start_Time"].map(lambda x: x[:])
    Events["End_Time"] = Events["End_Time"].map(lambda x: x[:])
    Events.drop(labels=["End_Date", "Recurring", "Meeting_Room", "All_Day_Event", "Event_Empty_Insert", "Within_Working_Hours", "Start_Date_Del", "End_Date_Del"], axis=1, inplace=True)
    Events.rename(columns={"Start_Date": "Date", "Project": "Network Description", "Subject": "Activity description", "Start_Time": "Start Time", "End_Time": "End Time", "": ""}, inplace=True)
    Events = Events[["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location", "Duration", "Busy_Status"]]

    #! Doděalt
    # ------------------------------ Total Duration ------------------------------ #
    # ------------------- Total Duration ------------------- #
    # Cumulated duration for all selected period

    # ------------- Total Duration per Project ------------- #
    # Cumulated duration for all selected period and splited by project

    # ------------- Total Duration per activity ------------ #
    # Cumulated duration for all selected period and splited by Activity

    # ----------------------------- Average Duration ----------------------------- #
    # ------------------- Average Duration ------------------- #
    # Average duration for all selected period

    # ------------- Average Duration per Project ------------- #
    # Average duration for all selected period and splited by Project 

    # ------------- Average Duration per activity ------------ #
    # Average duration for all selected period and splited by Activity

    # ------------------------- Week day average Duration ------------------------ #
    # ------------------- Average Duration ------------------- #
    # Average duration for all selected period per WeekDay

    # ------------- Average Duration per Project ------------- #
    # Average duration for all selected period and splited by Project per WeekDay

    # ------------- Average Duration per activity ------------ #
    # Average duration for all selected period and splited by Activity per WeekDay


    # Prepare Dataframe for import --> delete all nont needed columns
    Dataframe_sort(Dataframe=Events) 
    pandas.set_option('display.max_rows', None)
    Events.drop(labels=["Duration", "Busy_Status"], axis=1, inplace=True)
    Events.to_csv(path_or_buf="TimeSheets.csv", index=False, sep=";", header=True)
    print("\nProcessed Data from Calendar:")
    print(Events)
    return Events