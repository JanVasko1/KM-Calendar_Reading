# Import Libraries
from pandas import DataFrame, Series, concat
import random
from datetime import datetime, timedelta

import Libs.GUI.Elements as Elements

from customtkinter import CTk

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Change(Date_format: str, Time_format: str, Start_Date: str, End_Date: str, Start_Time: str, End_Time: str) -> int:
    Start_Date_Time = f"""{Start_Date}_{Start_Time}"""
    End_Date_Time = f"""{End_Date}_{End_Time}"""
    Start_Date_Time_dt = datetime.strptime(Start_Date_Time, f"{Date_format}_{Time_format}")
    End_Date_Time_dt = datetime.strptime(End_Date_Time, f"{Date_format}_{Time_format}")
    if End_Date_Time_dt.minute == 59:
        End_Date_Time_dt = End_Date_Time_dt + timedelta(minutes=1)

    Duration_dt = End_Date_Time_dt - Start_Date_Time_dt

    Duration = (int(Duration_dt.total_seconds())) // 60
    return Duration

def Days_Handler(Date_format: str, Event_Start_Date: str, Event_End_Date: str) -> list:
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
def OverMidnight_Events(Settings: dict, Configuration: dict, window: CTk|None, Events: DataFrame):
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Time_format = Settings["0"]["General"]["Formats"]["Time"]


    # Handle Meetings which are for more days / over midnight --> splits them
    Event_Indexes = []
    for row in Events.iterrows():
        row_Series = Series(row[1])
        Event_Start_Date = row_Series["Start_Date"]
        Event_End_Date = row_Series["End_Date"]

        if Event_Start_Date != Event_End_Date:
            Days_List = Days_Handler(Date_format=Date_format, Event_Start_Date=Event_Start_Date, Event_End_Date=Event_End_Date)
            last_index = len(Days_List) - 1

            for Current_index, Current_day in enumerate(Days_List):
                row_Series_2 = row_Series.copy()
                # First Day
                if Current_index == 0:
                    row_Series_2["End_Date"] = Current_day
                    row_Series_2["End_Time"] = "23:59"
                    row_Series_2["Duration"] = Duration_Change(Date_format=Date_format, Time_format=Time_format, Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2

                # Middle Days
                elif Current_index > 0 and Current_index != last_index:
                    row_Series_2["Start_Date"] = Current_day
                    row_Series_2["End_Date"] = Current_day
                    row_Series_2["Start_Time"] = "00:00"
                    row_Series_2["End_Time"] = "23:59"
                    row_Series_2["Duration"] = Duration_Change(Date_format=Date_format, Time_format=Time_format, Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2

                # Last Day
                elif Current_index == last_index:
                    row_Series_2["Start_Date"] = Current_day
                    row_Series_2["Start_Time"] = "00:00"
                    row_Series_2["Duration"] = Duration_Change(Date_format=Date_format, Time_format=Time_format, Start_Date=row_Series_2["Start_Date"], End_Date=row_Series_2["End_Date"], Start_Time=row_Series_2["Start_Time"], End_Time=row_Series_2["End_Time"])
                    
                    Events.loc[Events.shape[0]] = row_Series_2
                
                # Should not happened
                else:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Divide_Events.py: This should not happened.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            # Add index to list of indexes to be deleted
            Event_Indexes.append(row[0])
        else:
            pass


    # Delete original line as it will be substituted by newly created lines
    for Event_index in Event_Indexes:
        Events.drop(labels=[Event_index], axis=0, inplace=True)
    return Events

def Empty_Split_Events(Settings: dict, Configuration: dict, window: CTk|None, Events: DataFrame):
    Events_Empty_Split_Enabled = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Use"]
    Split_duration = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Duration"]
    Split_Minimal_Time = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Minimal_Time"]
    Split_method = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Method"]

    def Find_Split_Events(Events: DataFrame) -> DataFrame:
        if (Events["Event_Empty_Insert"] == True) and (Events["Event_Empty_Method"] == "General") and (Events["Duration"] >= Split_duration):
            return True
        else:
            return False
        
    def Split_Event(Cumulated_Events: DataFrame, Row: Series) -> DataFrame:
        init_duration = Row["Duration"]
        if Split_method == "Equal Split":
            first_duration = init_duration // 2
            second_duration = init_duration - first_duration            
        elif Split_method == "Random Split":
            try:
                first_duration = random.randrange(start=Split_Minimal_Time, stop=(init_duration - Split_Minimal_Time), step=Split_Minimal_Time)
                second_duration = init_duration - first_duration        
            except:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Cannot perform split as minimal time is {Split_Minimal_Time} and split duration is {Split_duration}. You need to keep Split Duration > Minimal Time", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Not supported Split Empty Events method used.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        
        # First row
        insert_first_row = Row.copy()
        insert_first_row["Duration"] = first_duration        
        time_change = timedelta(minutes=first_duration) 
        insert_first_row["End_Time"] = insert_first_row["Start_Time"] + time_change 

        # Second Row
        insert_second_row = Row.copy()
        insert_second_row["Duration"] = second_duration
        insert_second_row["Start_Time"] = insert_first_row["End_Time"]

        # Recursive calls
        if first_duration >= Split_duration:
            Cumulated_Events = Split_Event(Cumulated_Events=Cumulated_Events, Row=insert_first_row)
        else:
            # Add to Cumulated Events list
            Cumulated_Events.loc[len(Cumulated_Events)] = insert_first_row.to_list()

        if second_duration >= Split_duration:
            Cumulated_Events = Split_Event(Cumulated_Events=Cumulated_Events, Row=insert_second_row)
        else:
            # Add to Cumulated Events list
            Cumulated_Events.loc[len(Cumulated_Events)] = insert_second_row.to_list()

        return Cumulated_Events

    if Events_Empty_Split_Enabled == True:
        Cumulated_Events = DataFrame()
        Events["Empty_Split"] = Events.apply(Find_Split_Events, axis = 1)

        # Define events to be splitted DF
        mask1 = Events["Empty_Split"] == True
        Events_to_Split_df = DataFrame(Events.loc[mask1])

        # Add non-Conflict to Cumulated
        mask1 = Events["Empty_Split"] == False
        Non_Split_df = DataFrame(Events.loc[mask1])
        Cumulated_Events = concat(objs=[Cumulated_Events, Non_Split_df], axis=0, ignore_index=True)

        if Events_to_Split_df.empty:
            pass
        else:
            for row in Events_to_Split_df.iterrows():
                row_Series = Series(row[1])
                Cumulated_Events = Split_Event(Cumulated_Events=Cumulated_Events, Row=row_Series)
        
        Cumulated_Events.drop(labels=["Empty_Split"], axis=1, inplace=True)
        return Cumulated_Events
    else:
        return Events
