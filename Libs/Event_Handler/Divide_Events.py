from pandas import DataFrame
import pandas
import json
from datetime import datetime, timedelta
from tqdm import tqdm

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Change(Start_Date: str, End_Date: str, Start_Time: str, End_Time: str) -> int:
    Start_Date_Time = f"""{Start_Date}_{Start_Time}"""
    End_Date_Time = f"""{End_Date}_{End_Time}"""
    Start_Date_Time_dt = datetime.strptime(Start_Date_Time, f"{Date_format}_{Time_format}")
    End_Date_Time_dt = datetime.strptime(End_Date_Time, f"{Date_format}_{Time_format}")
    if End_Date_Time_dt.minute == 59:
        End_Date_Time_dt = End_Date_Time_dt + timedelta(minutes=1)

    Duration_dt = End_Date_Time_dt - Start_Date_Time_dt

    Duration = (int(Duration_dt.total_seconds())) // 60
    return Duration

def Days_Handler(Event_Start_Date: str, Event_End_Date: str) -> list:
    Event_Start_Date_dt = datetime.strptime(Event_Start_Date, Date_format)
    Event_End_Date_dt = datetime.strptime(Event_End_Date, Date_format)
    Days_dt = Event_End_Date_dt - Event_Start_Date_dt
    Days_no = int(Days_dt.total_seconds()) // 60 // 60 // 24
    Days_List = []
    for counter in range(0, Days_no + 1):
        Date_converted_dt = Event_Start_Date_dt + timedelta(days=counter)
        Date_import = Date_converted_dt.strftime(Date_format)
        Days_List.append(Date_import)
    Days_List.sort()
    return Days_List

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def OverMidnight_Events(Events: DataFrame):
    # Handle Meetings wchich are for more days / over midnight --> splits them
    Event_Indexes = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(Events.shape[0]),desc=f"{now}>> Overnight Events")
    for row in Events.iterrows():
        row_Series = pandas.Series(row[1])
        Event_Start_Date = row_Series["Start_Date"]
        Event_End_Date = row_Series["End_Date"]

        if Event_Start_Date != Event_End_Date:
            Days_List = Days_Handler(Event_Start_Date, Event_End_Date)
            last_index = len(Days_List) - 1

            for Current_index, Current_day in enumerate(Days_List):
                row_Series_2 = row_Series.copy()
                # First Day
                if Current_index == 0:
                    row_Series_2["End_Date"] = Current_day
                    row_Series_2["End_Time"] = "23:59"
                    row_Series_2["Duration"] = Duration_Change(Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2

                # Middle Days
                elif Current_index > 0 and Current_index != last_index:
                    row_Series_2["Start_Date"] = Current_day
                    row_Series_2["End_Date"] = Current_day
                    row_Series_2["Start_Time"] = "00:00"
                    row_Series_2["End_Time"] = "23:59"
                    row_Series_2["Duration"] = Duration_Change(Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2

                # Last Day
                elif Current_index == last_index:
                    row_Series_2["Start_Date"] = Current_day
                    row_Series_2["Start_Time"] = "00:00"
                    row_Series_2["Duration"] = Duration_Change(Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2
                
                # Should not happened
                else:
                    print(f"Divide_Events.py: This should happened.")

            # Add index to list of indexes to be deleted
            Event_Indexes.append(row[0])
        else:
            pass

        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    # Delete original line as it will be substituted by newly created lines
    for Event_index in Event_Indexes:
        Events.drop(labels=[Event_index], axis=0, inplace=True)
    return Events