import Libs.Event_Handler.Parralel_Events as Parralel_Events
from pandas import DataFrame
import pandas
from datetime import datetime
from tqdm import tqdm
import json

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

Vacation_Calendar = Settings["General"]["Calendar"]
Vacation_Details = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]
Lunch_Details = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Couter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minues
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Delete_Event_during_Vacation_Day(Dataframe: DataFrame, Event_Day: str, Vacation_Start_Time_dt: datetime, Vacation_End_Time_dt: datetime, Vacation_Index: int) -> None:
    mask1 = Dataframe["Start_Date"] == Event_Day
    mask2 = Dataframe["Start_Time"] >= Vacation_Start_Time_dt
    mask3 = Dataframe["Start_Time"] <= Vacation_End_Time_dt
    mask4 = Dataframe["End_Time"] >= Vacation_Start_Time_dt
    mask5 = Dataframe["End_Time"] <= Vacation_End_Time_dt
    To_Delete_df = Dataframe.loc[mask1 & mask2 & mask3 &mask4 & mask5]
    Event_Indexes = To_Delete_df.index.values.tolist() 
    Event_Indexes.remove(Vacation_Index)

    # Delete according to indexex
    for Event_index in Event_Indexes:
        Dataframe.drop(labels=[Event_index], axis=0, inplace=True)

def Days_Handler(Events: DataFrame) -> list:
    Days_List = Events["Start_Date"].tolist()
    Days_List = list(set(Days_List))
    Days_List.sort()
    return Days_List

def Dataframe_sort(Dataframe: DataFrame, Sort: bool) -> None:
    # Sort DAtaframe and reindex 
    Dataframe.sort_values(by=["Start_Date", "Start_Time"], ascending=[Sort, Sort], axis=0, inplace = True)
    Dataframe.reset_index(inplace=True)
    Dataframe.drop(labels=["index"], inplace=True, axis=1)

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
# Vacation
def Vacation(Events: DataFrame):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(Events.shape[0]),desc=f"{now}>> Special Events - Vacation")
    for row in Events.iterrows():
        row_index = row[0]
        row_Series = pandas.Series(row[1])
        Event_Subject = row_Series["Subject"]
        Event_Day = row_Series["Start_Date"]
        Event_All_Day = row_Series["All_Day_Event"]

        Day_dt = datetime.strptime(Event_Day, Date_format)
        Day_WeekDay_name = Day_dt.strftime("%A")

        # Vacation - if found as "All day" substituted for real day hours
        Vacation_Found = Event_Subject.find(Vacation_Details["Search_Text"])
        if Vacation_Found == -1:
            pass
        else:
            # All Day
            if Event_All_Day == True:
                Calendar_Start_Time = Vacation_Calendar[Day_WeekDay_name]["Vacation"]["Start_Time"]
                Calendar_End_Time = Vacation_Calendar[Day_WeekDay_name]["Vacation"]["End_Time"]

                # Change Event Start Time and End time according to calendar
                Vacation_Start_Time_dt = datetime.strptime(Calendar_Start_Time, Time_format)
                Vacation_End_Time_dt = datetime.strptime(Calendar_End_Time, Time_format)
                Events.at[row_index, "Start_Time"] = Vacation_Start_Time_dt
                Events.at[row_index, "End_Time"] = Vacation_End_Time_dt
                Events.at[row_index, "Duration"] = Duration_Couter(Time1=Vacation_Start_Time_dt, Time2=Vacation_End_Time_dt)

                # Delete all meetings of that day and within the Event time
                Delete_Event_during_Vacation_Day(Dataframe=Events, Event_Day=Event_Day, Vacation_Start_Time_dt=Vacation_Start_Time_dt, Vacation_End_Time_dt=Vacation_End_Time_dt, Vacation_Index=row_index)
            else:
                # Delete all meetings of that day and within the Event time
                Delete_Event_during_Vacation_Day(Dataframe=Events, Event_Day=Event_Day, Vacation_Start_Time_dt=Vacation_Start_Time_dt, Vacation_End_Time_dt=Vacation_End_Time_dt, Vacation_Index=row_index)

        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    return Events

# Home Office
def HomeOffice(Events: DataFrame):
    # Možná ani nebude potřeba, pokud se nemá měnit lookace
    return Events

# Lunch
def Lunch(Events: DataFrame):
    # Should split conflict meetings if they are within Lunch
    Cumulated_Events = pandas.DataFrame()

    #Get Days details from Events
    Days_List = Days_Handler(Events)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(len(Days_List)),desc=f"{now}>> Special Events - Lunch")
    for Day in Days_List:
        mask1 = Events["Start_Date"] == Day
        Day_Events_df = Events.loc[mask1]
        Dataframe_sort(Dataframe=Day_Events_df, Sort=True) 
        
        # Get Lunch Conflict
        Day_Events_df = Parralel_Events.Find_Conflit_in_DF(Check_DF=Day_Events_df)
        mask1 = Day_Events_df["Subject"] == Lunch_Details["Search_Text"]
        Lunch_df = Day_Events_df.loc[mask1]

        # Test if there is Lunch within Day
        try:
            Conflict_list = Lunch_df.iloc[0]["Conflict_indexes"]
            Sub_Event_Start_Time = Lunch_df.iloc[0]["Start_Time"]
            Sub_Event_End_Time = Lunch_df.iloc[0]["End_Time"]
        except:
            Conflict_list = []

        if not Conflict_list:
            pass
        else:
            for Conflict_index in Conflict_list:
                # Find Event in Day_Events_df
                Event_Series = Day_Events_df.iloc[Conflict_index]
                Event_Start_Time = Event_Series["Start_Time"]
                Event_End_Time = Event_Series["End_Time"]

                # ------------ Split Event ------------ #
                # Event End will be cut by SubEvent
                Parralel_Events.Event_End_Cut(Continue=False, Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                
                # Event Start will be cut by SubEvent
                Parralel_Events.Event_Start_Cut(Continue=False, Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                
                # Event Start will be cut by SubEvent
                Parralel_Events.Event_Start_Cut_Lunch(Continue=False, Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)

                # SubEvent is inside totaly of Event no borders
                Parralel_Events.Event_Middle_Cut(Continue=False, Conflict_df=Day_Events_df, Event_Index=Conflict_index, Data=Event_Series, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)

        Dataframe_sort(Dataframe=Day_Events_df, Sort=True) 
        for row in Day_Events_df.iterrows():
            row_Series = pandas.Series(row[1])
            Event_Start_Time = row_Series["Start_Time"]
            Event_End_Time = row_Series["End_Time"]
            Day_Events_df.at[row[0], "Duration"] = Duration_Couter(Time1=Event_Start_Time, Time2=Event_End_Time)
        
        # Add to Cumulated
        Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Day_Events_df], axis=0)
        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()
    Cumulated_Events.drop(labels=["Conflict", "Conflict_indexes", "Start_with_Event"], axis=1, inplace=True)
    return Cumulated_Events
