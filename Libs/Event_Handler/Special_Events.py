# Import Libraries
from pandas import DataFrame, Series, concat
from datetime import datetime

import Libs.Event_Handler.Parallel_Events as Parallel_Events
import Libs.Pandas_Functions as Pandas_Functions

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Counter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minutes
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Delete_Event_during_KM_Calendar(Dataframe: DataFrame, Event_Day: str, KM_Start_Time_dt: datetime, KM_End_Time_dt: datetime, Vacation_Index: int) -> None:
    mask1 = Dataframe["Start_Date"] == Event_Day
    mask2 = Dataframe["Start_Time"] >= KM_Start_Time_dt
    mask3 = Dataframe["Start_Time"] <= KM_End_Time_dt
    mask4 = Dataframe["End_Time"] >= KM_Start_Time_dt
    mask5 = Dataframe["End_Time"] <= KM_End_Time_dt
    To_Delete_df = DataFrame(Dataframe.loc[mask1 & mask2 & mask3 &mask4 & mask5])
    Event_Indexes = To_Delete_df.index.values.tolist() 
    Event_Indexes.remove(Vacation_Index)

    # Delete according to index
    for Event_index in Event_Indexes:
        Dataframe.drop(labels=[Event_index], axis=0, inplace=True)

def Days_Handler(Events: DataFrame) -> list:
    Days_List = Events["Start_Date"].tolist()
    Days_List = list(set(Days_List))
    Days_List.sort()
    return Days_List

def Subtract_Parallel_Events(Events: DataFrame, Event_Search_Text: str) -> DataFrame:
    # Should split conflict meetings if they are within Lunch
    Cumulated_Events = DataFrame()

    #Get Days details from Events
    Days_List = Days_Handler(Events)

    for Day in Days_List:
        mask1 = Events["Start_Date"] == Day
        Day_Events_df = DataFrame(Events.loc[mask1])
        Day_Events_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
        
        # Get Lunch Conflict
        Day_Events_df = Parallel_Events.Find_Conflict_in_DF(Check_DF=Day_Events_df)
        mask1 = Day_Events_df["Subject"] == Event_Search_Text
        Filtered_df = DataFrame(Day_Events_df.loc[mask1])

        # Test if there is Lunch within Day
        try:
            Conflict_list = Filtered_df.iloc[0]["Conflict_indexes"]
            Sub_Event_Start_Time = Filtered_df.iloc[0]["Start_Time"]
            Sub_Event_End_Time = Filtered_df.iloc[0]["End_Time"]
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
                Parallel_Events.Event_End_Cut(Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                
                # Event Start will be cut by SubEvent
                Parallel_Events.Event_Start_Cut(Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                
                # Event Start will be cut by SubEvent
                Parallel_Events.Event_Start_Cut_Lunch(Conflict_df=Day_Events_df, Event_Index=Conflict_index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)

                # SubEvent is inside totally of Event no borders
                Parallel_Events.Event_Middle_Cut(Conflict_df=Day_Events_df, Event_Index=Conflict_index, Data=Event_Series, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)

        Day_Events_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
        for row in Day_Events_df.iterrows():
            row_Series = Series(row[1])
            Event_Start_Time = row_Series["Start_Time"]
            Event_End_Time = row_Series["End_Time"]
            Day_Events_df.at[row[0], "Duration"] = Duration_Counter(Time1=Event_Start_Time, Time2=Event_End_Time)
        
        # Add to Cumulated
        Cumulated_Events = concat(objs=[Cumulated_Events, Day_Events_df], axis=0)
    Cumulated_Events.drop(labels=["Conflict", "Conflict_indexes", "Start_with_Event"], axis=1, inplace=True)

    return Cumulated_Events

def Day_handler(Settings: dict, Events: DataFrame, Details: dict) -> DataFrame:
    Vacation_Calendar = Settings["0"]["General"]["Calendar"]
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Time_format = Settings["0"]["General"]["Formats"]["Time"]

    for row in Events.iterrows():
        row_index = row[0]
        row_Series = Series(row[1])
        Event_Subject = row_Series["Subject"]
        Event_Day = row_Series["Start_Date"]
        Event_All_Day = row_Series["All_Day_Event"]

        Day_dt = datetime.strptime(Event_Day, Date_format)
        Day_WeekDay_name = Day_dt.strftime("%A")

        # Vacation - if found as "All day" substituted for real day hours
        Text_Found = Event_Subject.find(Details["Search_Text"])
        if Text_Found == -1:
            pass
        else:
            if Event_All_Day == True:
                # All Day
                KM_Start_Time = Vacation_Calendar[Day_WeekDay_name]["Vacation"]["Start_Time"]
                KM_End_Time = Vacation_Calendar[Day_WeekDay_name]["Vacation"]["End_Time"]

                # Change Event Start Time and End time according to calendar
                KM_Start_Time_dt = datetime.strptime(KM_Start_Time, Time_format)
                KM_End_Time_dt = datetime.strptime(KM_End_Time, Time_format)
                Events.at[row_index, "Start_Time"] = KM_Start_Time_dt
                Events.at[row_index, "End_Time"] = KM_End_Time_dt
                Events.at[row_index, "Duration"] = Duration_Counter(Time1=KM_Start_Time_dt, Time2=KM_End_Time_dt)

                # Delete all meetings of that day and within the Event time
                if Details["Delete_Events_w_KM_Calendar"] == True:
                    Delete_Event_during_KM_Calendar(Dataframe=Events, Event_Day=Event_Day, KM_Start_Time_dt=KM_Start_Time_dt, KM_End_Time_dt=KM_End_Time_dt, Vacation_Index=row_index)
                else:
                    pass
            else:
                # Part of the Day
                # Delete all meetings of that day and within the Event time
                if Details["Delete_Events_w_KM_Calendar"] == True:
                    Delete_Event_during_KM_Calendar(Dataframe=Events, Event_Day=Event_Day, KM_Start_Time_dt=KM_Start_Time_dt, KM_End_Time_dt=KM_End_Time_dt, Vacation_Index=row_index)
                else:
                    pass
    return Events

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
# Vacation
def Vacation(Settings: dict, Events: DataFrame) -> DataFrame:
    Vacation_Details = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]
    Vacation_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Use"]

    if Vacation_Enabled == True:
        Events = Day_handler(Settings=Settings, Events=Events, Details=Vacation_Details)
        return Events
    else:
        return Events

# SickDay
def SickDay(Settings: dict, Events: DataFrame) -> DataFrame:
    SickDay_Details = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]
    SickDay_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Use"]

    if SickDay_Enabled == True:
        Events = Day_handler(Settings=Settings, Events=Events, Details=SickDay_Details)
        return Events
    else:
        return Events

# Home Office
def HomeOffice(Settings: dict, Events: DataFrame):
    HomeOffice_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Use"]

    if HomeOffice_Enabled == True:
        return Events
    else:
        return Events

# Lunch
def Lunch(Settings: dict, Events: DataFrame) -> DataFrame:
    Lunch_Details = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]
    Lunch_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Use"]

    if Lunch_Enabled == True:
        Cumulated_Events = Subtract_Parallel_Events(Events=Events, Event_Search_Text = Lunch_Details["Search_Text"])
        return Cumulated_Events
    else:
        return Events

# Private
def Private(Settings: dict, Events: DataFrame) -> DataFrame:
    Private_Details = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]
    Private_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]["Use"]

    if Private_Enabled == True:
        if Private_Details["Method"] == "Split Parallel and delete":
            Cumulated_Events = Subtract_Parallel_Events(Events=Events, Event_Search_Text = Private_Details["Search_Text"])
            return Cumulated_Events
        elif Private_Details["Method"] == "Just delete Private":
            mask = Events["Subject"] == Private_Details["Search_Text"]
            Events_Subtracted = DataFrame(Events[~mask])
            return Events_Subtracted
        else:
            pass
    else:
        return Events
