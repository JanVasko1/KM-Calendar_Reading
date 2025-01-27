# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
from pandas import DataFrame
import pandas
from datetime import datetime
import operator
import json
import random
import warnings
warnings.filterwarnings('ignore')

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

Day_Start_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
Day_End_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Get_General_Event(Settings: json, Gen_Event_Counter: int) -> str:
    Random_Num = random.randrange(start=0, stop=Gen_Event_Counter, step=1)
    General_Empty_Project = Settings["Event_Handler"]["Events"]["Empty"]["General"][f"{Random_Num}"]["Project"]
    General_Empty_Activity = Settings["Event_Handler"]["Events"]["Empty"]["General"][f"{Random_Num}"]["Activity"]
    General_Empty_Description = Settings["Event_Handler"]["Events"]["Empty"]["General"][f"{Random_Num}"]["Description"]
    return General_Empty_Project, General_Empty_Activity, General_Empty_Description

def Dataframe_timedelta_to_minutes(Timedelta) -> int:
    interval = Timedelta.value // 1_000
    minutes = interval // 60_000_000
    return minutes

def Delete_Pre_SubEvents(Differences_to_Start_list: list, Differences_to_End_list: list, Sub_event_DF_Index_list: list) -> None:
    # delete zero difference from Differences_list and connected record form Sub_event_DF_Index_list
    Index_to_Del = []

    # Check if end of event is before start of Sub Event
    for index, value in enumerate(Differences_to_Start_list):
        if value < 0:
            if Differences_to_End_list[index] <= 0:
                Index_to_Del.append(index)
            elif Differences_to_End_list[index] > 0:
                Differences_to_Start_list[index] = 0
            else:
                pass
        else:
            pass

    for index in sorted(Index_to_Del, reverse=True):
        Differences_to_Start_list.pop(index)
        Differences_to_End_list.pop(index)
        Sub_event_DF_Index_list.pop(index)

def Convert_time_delta_to_int(Differences_list: list) -> None:
    for index, value in enumerate(Differences_list):
        minutes = Dataframe_timedelta_to_minutes(value)
        Differences_list[index] = minutes

def Find_Close_Sub_Event(Day_Events_df: DataFrame, General_Empty_df: DataFrame, Day: str, Start_Time: str|datetime, Differences_to_Start_list: list, Differences_to_End_list: list, Sub_event_DF_Index_list: list, General_Empty_Project: str, General_Empty_Activity: str, General_Empty_Description: str) -> None:
    Delete_Pre_SubEvents(Differences_to_Start_list=Differences_to_Start_list, Differences_to_End_list=Differences_to_End_list, Sub_event_DF_Index_list=Sub_event_DF_Index_list)

    if not Differences_to_Start_list:
        pass
    else:
        Duration = min(Differences_to_Start_list)
        if Duration == 0:
            pass
        else:
            # Find End_Time for inserted event as Start_Time of next closest event
            Duration_Index = Differences_to_Start_list.index(Duration)
            DF_Index = Sub_event_DF_Index_list[Duration_Index]
            End_Time = General_Empty_df.iloc[DF_Index]["Start_Time"]
            Dataframe_add_line(Dataframe=Day_Events_df, Subject=General_Empty_Description, Start_Date=Day, End_Date=Day, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=General_Empty_Project, Activity=General_Empty_Activity, Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="General", Within_Working_Hours=True, Location="Office")
            # Must add  also to General_Empty because inserted line might be updated by different line calculation and newly create line would miss and cause double insert
            Dataframe_add_line(Dataframe=General_Empty_df, Subject=General_Empty_Description, Start_Date=Day, End_Date=Day, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=General_Empty_Project, Activity=General_Empty_Activity, Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="General", Within_Working_Hours=True, Location="Office")
   
def Define_Event_within_Working_Hours(Dataframe: DataFrame, Day_Start_Time_dt: datetime, Day_End_Time_dt: datetime) -> None:
    # Marks row which are at least with some part of event within working hours
    for row in Dataframe.iterrows():
        row_Series = pandas.Series(row[1])
        Event_Start_time = row_Series["Start_Time"]
        Event_End_time = row_Series["End_Time"]

        if (Event_Start_time < Day_Start_Time_dt) and (Event_End_time <= Day_Start_Time_dt) and (Event_Start_time < Day_End_Time_dt) and (Event_End_time <= Day_End_Time_dt):
            pass
        elif (Event_Start_time < Day_Start_Time_dt) and (Event_End_time > Day_Start_Time_dt) and (Event_Start_time < Day_End_Time_dt) and (Event_End_time < Day_End_Time_dt):
            Dataframe.at[row[0], "Within_Working_Hours"] = True
        elif (Event_Start_time >= Day_Start_Time_dt) and (Event_End_time > Day_Start_Time_dt) and (Event_Start_time < Day_End_Time_dt) and (Event_End_time <= Day_End_Time_dt):
            Dataframe.at[row[0], "Within_Working_Hours"] = True
        elif (Event_Start_time >= Day_Start_Time_dt) and (Event_End_time > Day_Start_Time_dt) and (Event_Start_time < Day_End_Time_dt) and (Event_End_time >= Day_End_Time_dt):
            Dataframe.at[row[0], "Within_Working_Hours"] = True
        elif (Event_Start_time >= Day_Start_Time_dt) and (Event_End_time > Day_Start_Time_dt) and (Event_Start_time >= Day_End_Time_dt) and (Event_End_time > Day_End_Time_dt):
            pass
        else:
            continue

def Duration_Counter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minutes
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Dataframe_add_line(Dataframe: DataFrame, Subject: str, Start_Date: str|datetime, End_Date: str|datetime, Start_Time: str|datetime, End_Time: str|datetime, Duration: int, Project: str, Activity: str, Recurring: bool, Busy_Status: str, Meeting_Room: str, All_Day_Event: bool, Event_Empty_Insert: bool, Event_Empty_Method: str, Within_Working_Hours: bool, Location: str) -> None:
    # Add record to Dataframe
    Dataframe.loc[Dataframe.shape[0]] = [Subject, Start_Date, End_Date, Start_Time, End_Time, Duration, Project, Activity, Recurring, Busy_Status, Meeting_Room, All_Day_Event, Event_Empty_Insert, Event_Empty_Method, Within_Working_Hours, Location] 

def Days_Handler(Events: DataFrame) -> list:
    Days_List = Events["Start_Date"].tolist()
    Days_List = list(set(Days_List))
    Days_List.sort()
    return Days_List

def Get_Day_Start_End_Time(Day_Events_df: DataFrame, Day: str):
    Day_Start_Series = Day_Events_df[Day_Events_df["Subject"] == str(Day_Start_Subject)]
    Day_End_Series = Day_Events_df[Day_Events_df["Subject"] == str(Day_End_Subject)]
    try:
        Day_Start_Time = Day_Start_Series.iloc[0]["Start_Time"]
        Day_End_Time = Day_End_Series.iloc[0]["End_Time"]
    except:
        Day_Start_Time = None
        Day_End_Time = None
    return Day_Start_Time, Day_End_Time

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Fill_Events(Events: DataFrame) -> DataFrame:
    Cumulated_Events = pandas.DataFrame()
    Events_Empty_Scheduled = Settings["Event_Handler"]["Events"]["Empty"]["Scheduled"]
    Gen_Event_Counter = int(len(Settings["Event_Handler"]["Events"]["Empty"]["General"]))
    
    # Get Days details from Events
    Days_List = Days_Handler(Events)

    for Day in Days_List:
        mask1 = Events["Start_Date"] == Day
        Day_Events_df = Events.loc[mask1]

        # Sorting
        Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
        
        Day_Start_Time, Day_End_Time = Get_Day_Start_End_Time(Day_Events_df=Day_Events_df, Day=Day)
        if Day_Start_Time == None or Day_End_Time == None:
            # Do not make input to the day when day does not have Work Start / Work End Time
            Day_Events_df["Start_Time"] = pandas.to_datetime(Day_Events_df["Start_Time"], format=Time_format)
            Day_Events_df["End_Time"] = pandas.to_datetime(Day_Events_df["End_Time"], format=Time_format)
            Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Day_Events_df], axis=0)
            continue
        else:
            Day_Start_Time_dt = datetime.strptime(Day_Start_Time, Time_format)
            Day_End_Time_dt = datetime.strptime(Day_End_Time, Time_format)
            Day_dt = datetime.strptime(Day, Date_format)
            Day_WeekDay = Day_dt.weekday() + 1

            #! Insert Scheduled  - between Day_Start_Time, Day_End_Time
            for item in Events_Empty_Scheduled.items():
                Schedule_Event_Start_Time_dt = datetime.strptime(item[1]["Start"], Time_format)
                Schedule_Event_End_Time_dt = datetime.strptime(item[1]["End"], Time_format)
                Schedule_WeekDays = item[1]["Day of Week"]

                # Scheduled event must be within Weeks Days selected
                if Day_WeekDay in Schedule_WeekDays:
                    # Scheduled event must be within the day working time at leas partially
                    if Schedule_Event_Start_Time_dt > Day_End_Time_dt:
                        continue
                    elif Schedule_Event_End_Time_dt < Day_Start_Time_dt:
                        continue
                    else:
                        # Check how Schedule meeting is within Working Hours for that day
                        if (Schedule_Event_Start_Time_dt >= Day_Start_Time_dt) and (Schedule_Event_End_Time_dt <= Day_End_Time_dt):
                            Duration = Duration_Counter(Time1=Schedule_Event_Start_Time_dt, Time2=Schedule_Event_End_Time_dt)
                            Dataframe_add_line(Dataframe=Day_Events_df, Subject=item[1]["Description"], Start_Date=Day, End_Date=Day, Start_Time=item[1]["Start"], End_Time=item[1]["End"], Duration=Duration, Project=item[1]["Project"], Activity=item[1]["Activity"], Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="Scheduled", Within_Working_Hours=False, Location="Office")
                        elif (Schedule_Event_Start_Time_dt >= Day_Start_Time_dt) and (Schedule_Event_End_Time_dt >= Day_End_Time_dt):
                            Duration = Duration_Counter(Time1=Schedule_Event_Start_Time_dt, Time2=Day_End_Time_dt)
                            Dataframe_add_line(Dataframe=Day_Events_df, Subject=item[1]["Description"], Start_Date=Day, End_Date=Day, Start_Time=item[1]["Start"], End_Time=Day_End_Time, Duration=Duration, Project=item[1]["Project"], Activity=item[1]["Activity"], Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="Scheduled", Within_Working_Hours=False, Location="Office")
                        elif (Schedule_Event_Start_Time_dt <= Day_Start_Time_dt) and (Schedule_Event_End_Time_dt <= Day_End_Time_dt):
                            Duration = Duration_Counter(Time1=Day_Start_Time_dt, Time2=Schedule_Event_End_Time_dt)
                            Dataframe_add_line(Dataframe=Day_Events_df, Subject=item[1]["Description"], Start_Date=Day, End_Date=Day, Start_Time=Day_Start_Time, End_Time=item[1]["End"], Duration=Duration, Project=item[1]["Project"], Activity=item[1]["Activity"], Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="Scheduled", Within_Working_Hours=False, Location="Office")
                        elif (Schedule_Event_Start_Time_dt <= Day_Start_Time_dt) and (Schedule_Event_End_Time_dt >= Day_End_Time_dt):
                            Duration = Duration_Counter(Time1=Day_Start_Time_dt, Time2=Day_End_Time_dt)
                            Dataframe_add_line(Dataframe=Day_Events_df, Subject=item[1]["Description"], Start_Date=Day, End_Date=Day, Start_Time=Day_Start_Time, End_Time=Day_End_Time, Duration=Duration, Project=item[1]["Project"], Activity=item[1]["Activity"], Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="Scheduled", Within_Working_Hours=False, Location="Office")
                        else:
                            pass
                else:
                    pass

            # Sorting
            Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            
            #! Insert General - only between Day_Start_Time, Day_End_Time
            Day_Events_df["Start_Time"] = pandas.to_datetime(Day_Events_df["Start_Time"], format=Time_format)
            Day_Events_df["End_Time"] = pandas.to_datetime(Day_Events_df["End_Time"], format=Time_format)
            Define_Event_within_Working_Hours(Dataframe=Day_Events_df, Day_Start_Time_dt=Day_Start_Time_dt, Day_End_Time_dt=Day_End_Time_dt)
            mask1 = Day_Events_df["Within_Working_Hours"] == True
            mask2 = Day_Events_df["All_Day_Event"] == False
            mask3 = Day_Events_df["Subject"] != Day_Start_Subject
            mask4 = Day_Events_df["Subject"] != Day_End_Subject
            General_Empty_df = Day_Events_df.loc[mask1 & mask2 & mask3 & mask4]

            # Fill between events
            General_Empty_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=General_Empty_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            for row in General_Empty_df.iterrows():
                # Define current row as pandas Series
                row_Series = pandas.Series(row[1])
                Event_End_time = row_Series["End_Time"]

                # Select Randomly from General Empty 
                General_Empty_Project, General_Empty_Activity, General_Empty_Description = Get_General_Event(Settings=Settings, Gen_Event_Counter=Gen_Event_Counter)

                # main loop
                Differences_to_Start_list = []
                Differences_to_End_list = []
                Sub_event_DF_Index_list = [] 
                for row_sub in General_Empty_df.iterrows():
                    Sub_row_Series = pandas.Series(row_sub[1])
                    Sub_Event_Start_time = Sub_row_Series["Start_Time"]
                    Sub_Event_End_time = Sub_row_Series["End_Time"]

                    # Do not compare same event to each other
                    if row[0] != row_sub[0]:
                        Difference_to_Star = Sub_Event_Start_time - Event_End_time
                        Difference_to_end = Sub_Event_End_time - Event_End_time
                        Differences_to_Start_list.append(Difference_to_Star)
                        Differences_to_End_list.append(Difference_to_end)
                        Sub_event_DF_Index_list.append(row_sub[0])
                    else:
                        pass
                    
                Convert_time_delta_to_int(Differences_list=Differences_to_Start_list)
                Convert_time_delta_to_int(Differences_list=Differences_to_End_list)
                Find_Close_Sub_Event(Day_Events_df=Day_Events_df, General_Empty_df=General_Empty_df, Day=Day, Start_Time=Event_End_time, Differences_to_Start_list=Differences_to_Start_list, Differences_to_End_list=Differences_to_End_list, Sub_event_DF_Index_list=Sub_event_DF_Index_list, General_Empty_Project=General_Empty_Project, General_Empty_Activity=General_Empty_Activity, General_Empty_Description=General_Empty_Description)
                Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            del General_Empty_df

            # Fill start of the day if needed
            Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            mask1 = Day_Events_df["Subject"] != Day_Start_Subject
            mask2 = Day_Events_df["Subject"] != Day_End_Subject
            mask3 = Day_Events_df["Within_Working_Hours"] == True
            General_Empty_df = Day_Events_df.loc[mask1 & mask2 & mask3]

            Event_Over = False
            Events_Start_Times_list = []
            for row in General_Empty_df.iterrows():
                # Define current row as pandas Series
                row_Series = pandas.Series(row[1])
                Event_Start_time = row_Series["Start_Time"]
                Event_End_time = row_Series["End_Time"]
                Events_Start_Times_list.append(Event_Start_time)

                # check if there is event over Day start
                if (Event_Start_time == Day_Start_Time_dt) or ((Event_Start_time < Day_Start_Time_dt) and (Event_End_time > Day_Start_Time_dt)):
                    Event_Over = True
                else:
                    continue
            
            if Event_Over == False:
                Difference_to_Star = []
                # Select Randomly from General Empty 
                General_Empty_Project, General_Empty_Activity, General_Empty_Description = Get_General_Event(Settings=Settings, Gen_Event_Counter=Gen_Event_Counter)

                for time in Events_Start_Times_list:
                    Difference = time - Day_Start_Time_dt
                    Difference_to_Star.append(Difference)
                Convert_time_delta_to_int(Differences_list=Difference_to_Star)
                Min_Duration = min(Difference_to_Star)
                Min_Duration_Index = Difference_to_Star.index(Min_Duration)
                End_Time = Events_Start_Times_list[Min_Duration_Index]
                Dataframe_add_line(Dataframe=Day_Events_df, Subject=General_Empty_Description, Start_Date=Day, End_Date=Day, Start_Time=Day_Start_Time_dt, End_Time=End_Time, Duration=Min_Duration, Project=General_Empty_Project, Activity=General_Empty_Activity, Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="General", Within_Working_Hours=True, Location="Office")
            elif Event_Over == True:
                pass
            else:
                pass
            del General_Empty_df

            # Fill end of the day if needed
            Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            mask1 = Day_Events_df["Subject"] != Day_Start_Subject
            mask2 = Day_Events_df["Subject"] != Day_End_Subject
            mask3 = Day_Events_df["Within_Working_Hours"] == True
            General_Empty_df = Day_Events_df.loc[mask1 & mask2 & mask3]

            Event_Over = False
            Events_End_Times_list = []
            for row in General_Empty_df.iterrows():
                # Define current row as pandas Series
                row_Series = pandas.Series(row[1])
                Event_Start_time = row_Series["Start_Time"]
                Event_End_time = row_Series["End_Time"]
                Events_End_Times_list.append(Event_End_time)

                # check if there is event over Day start
                if (Event_End_time == Day_End_Time_dt) or ((Event_Start_time < Day_End_Time_dt) and (Event_End_time > Day_End_Time_dt)):
                    Event_Over = True
                else:
                    continue
            
            if Event_Over == False:
                Difference_to_End = []
                # Select Randomly from General Empty 
                General_Empty_Project, General_Empty_Activity, General_Empty_Description = Get_General_Event(Settings=Settings, Gen_Event_Counter=Gen_Event_Counter)

                for time in Events_End_Times_list:
                    Difference = Day_End_Time_dt - time
                    Difference_to_End.append(Difference)
                Convert_time_delta_to_int(Differences_list=Difference_to_End)
                Min_Duration = min(Difference_to_End)
                Min_Duration_Index = Difference_to_End.index(Min_Duration)
                Start_Time = Events_End_Times_list[Min_Duration_Index]
                Dataframe_add_line(Dataframe=Day_Events_df, Subject=General_Empty_Description, Start_Date=Day, End_Date=Day, Start_Time=Start_Time, End_Time=Day_End_Time_dt, Duration=Min_Duration, Project=General_Empty_Project, Activity=General_Empty_Activity, Recurring=False, Busy_Status="Busy", Meeting_Room="", All_Day_Event=False, Event_Empty_Insert=True, Event_Empty_Method="General", Within_Working_Hours=True, Location="Office")
            elif Event_Over == True:
                pass
            else:
                pass
            del General_Empty_df
            
            # Add to cumulated Dataframe
            Day_Events_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Day_Events_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
            Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Day_Events_df], axis=0)
            del Day_Events_df

    return Cumulated_Events

def Fill_Events_Coverage(Events: DataFrame) -> DataFrame:
    # Get Coverage for setup event 2 list 
    Fill_Event_desc_list = []
    Fill_Event_project_list = []
    Fill_Event_activity_list = []
    Fill_Event_cover_list = []
    Fill_Event_counted_duration_list = []
    Fill_Event_actual_duration_list = []
    Fill_Events_dict = Settings["Event_Handler"]["Events"]["Empty"]["General"]
    Fill_Events_Keys = list(Fill_Events_dict.keys())

    for key in Fill_Events_Keys:
        Fill_Event_desc_list.append(Fill_Events_dict[key]["Description"])
        Fill_Event_project_list.append(Fill_Events_dict[key]["Project"])
        Fill_Event_activity_list.append(Fill_Events_dict[key]["Activity"])
        Fill_Event_cover_list.append(Fill_Events_dict[key]["Coverage Percentage"])

    # Check if Coverage is 100%
    if sum(Fill_Event_cover_list) == 100:
        # Get only Fill Events --> Dataframe preparation
        mask = Events["Event_Empty_Insert"] == True
        Fill_Empty_Df = Events[mask]
        Duration_Total = sum(Fill_Empty_Df["Duration"])

        mask = Fill_Empty_Df["Event_Empty_Method"] == "Scheduled"
        Scheduled_df = Fill_Empty_Df[mask]

        mask = Fill_Empty_Df["Event_Empty_Method"] == "General"
        General_df = Fill_Empty_Df[mask]
        del Fill_Empty_Df

        # Count Minutes per Coverage from Duration Total
        for key in Fill_Events_Keys:
            Key_List_index = Fill_Events_Keys.index(key)
            Current_Coverage = Fill_Event_cover_list[Key_List_index]
            Current_Coverage_Dur = int(round(Duration_Total * (Current_Coverage / 100), 0))
            Fill_Event_counted_duration_list.append(Current_Coverage_Dur)
            Fill_Event_actual_duration_list.append(0)
        Fill_Event_duration_Total = sum(Fill_Event_counted_duration_list)
        Difference = Duration_Total - Fill_Event_duration_Total
        Fill_Event_Max_duration = max(Fill_Event_counted_duration_list)
        Fill_Event_Max_duration_index = Fill_Event_counted_duration_list.index(Fill_Event_Max_duration)
        Fill_Event_counted_duration_list[Fill_Event_Max_duration_index] = Fill_Event_Max_duration + Difference

        # Schedules -- keep as planned
        for row_schedule in Scheduled_df.iterrows():
            Scheduled_Description = row_schedule[1]["Subject"]
            Scheduled_Duration = row_schedule[1]["Duration"]

            # Get index of Fill_Event_desc_list --> to be able put correctly to Fill_Event_actual_duration_list
            Current_Fill_Index = Fill_Event_desc_list.index(Scheduled_Description)

            # Add to proper actual Fill_Event_actual_duration_list
            Fill_Event_actual_duration_list[Current_Fill_Index] = Fill_Event_actual_duration_list[Current_Fill_Index] + Scheduled_Duration

        # General -- recalculate according to coverage
        while True:
            # Check if any data available
            if General_df.empty:
                break
            else:
                pass

            # Find maximal Duration in the DF + list of index containing this maximal duration
            Max_General_Duration = max(General_df["Duration"])
            mask = General_df["Duration"] == Max_General_Duration
            General_Sub_df = General_df[mask]

            # Random choice from list of index
            while True:
                # Check if any data available
                if General_Sub_df.empty:
                    break
                else:
                    pass

                # Random select index
                General_Sub_Index_list = list(General_Sub_df.index.values)
                Change_Row_Index = random.choice(General_Sub_Index_list)

                # Find the Fill Event with maximal difference between "Fill_Event_counted_duration_list" and "Fill_Event_actual_duration_list" --> where the number is positive (not to overshoot)
                Fill_Event_difference_duration_list = list(map(operator.sub, Fill_Event_counted_duration_list, Fill_Event_actual_duration_list))
                for i in range(len(Fill_Event_difference_duration_list)):
                    if Fill_Event_difference_duration_list[i] < 0:
                        Fill_Event_difference_duration_list[i] = 0
                    else:
                        pass
                Max_Diff_Duration = max(Fill_Event_difference_duration_list)
                Current_Fill_Index = Fill_Event_difference_duration_list.index(Max_Diff_Duration)

                # Events change
                Events.at[Change_Row_Index, "Subject"] = Fill_Event_desc_list[Current_Fill_Index]
                Events.at[Change_Row_Index, "Project"] = Fill_Event_project_list[Current_Fill_Index]
                Events.at[Change_Row_Index, "Activity"] = Fill_Event_activity_list[Current_Fill_Index]

                # Delete from DFs
                General_df = General_df.drop(Change_Row_Index)
                General_Sub_df = General_Sub_df.drop(Change_Row_Index)

                # Add to proper actual Fill_Event_actual_duration_list
                Fill_Event_actual_duration_list[Current_Fill_Index] = Fill_Event_actual_duration_list[Current_Fill_Index] + Max_General_Duration

        return Events
    else:
        CTkMessagebox(title="Error", message="Sum of all Coverage is not 100%, please re-setup them in Setup / Events - Empty/Scheduler.", icon="cancel", fade_in_duration=1)
        return Events