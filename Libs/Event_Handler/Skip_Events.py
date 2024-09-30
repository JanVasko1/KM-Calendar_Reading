from pandas import DataFrame
import pandas
import json
from datetime import datetime
from tqdm import tqdm

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Day_Start_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
Day_End_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]
Skip_Events_list = Settings["Event_Handler"]["Events"]["Skip"]
Skip_Events_list.append(Day_Start_Subject)
Skip_Events_list.append(Day_End_Subject)

Columns = ["Subject", 
        "Start_Date", 
        "End_Date",
        "Start_Time", 
        "End_Time",
        "Duration",
        "Project",
        "Activity",
        "Recurring",
        "Busy_Status",
        "Meeting_Room",
        "All_Day_Event",
        "Event_Empty_Insert",
        "Within_Working_Hours",
        "Location"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Skip_Events(Events: DataFrame):
    Cumulated_Events = pandas.DataFrame(columns=Columns)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(Events.shape[0]),desc=f"{now}>> Skip Events")
    for row in Events.iterrows():
        # Define current row as pandas Series
        row_Series = pandas.Series(row[1])
        Event_Subject = row_Series["Subject"]

        for Skip in Skip_Events_list:
            Part_Found = Event_Subject.find(Skip)

            if Part_Found == -1:
                pass
            else:
                break

        if Part_Found == -1:
            Cumulated_Events.loc[Cumulated_Events.shape[0]] = row_Series
        else:
            pass
        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    return Cumulated_Events
