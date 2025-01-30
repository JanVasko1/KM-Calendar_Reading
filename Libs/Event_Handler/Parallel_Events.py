# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
from pandas import DataFrame, Series
import pandas
from datetime import datetime

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

Parallel_Enabled = Settings["Event_Handler"]["Events"]["Parallel_Events"]["Use"]
Start_Method = Settings["Event_Handler"]["Events"]["Parallel_Events"]["Start_Method"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Counter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minutes
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Days_Handler(Events: DataFrame) -> list:
    Days_List = Events["Start_Date"].tolist()
    Days_List = list(set(Days_List))
    Days_List.sort()
    return Days_List

def Add_Start_END_Indexes(Checked_Event_Index: int, Event_Start_with_indexes: list, Event_Start_time: datetime, Checked_Event_Start_time: datetime):
    if Event_Start_time == Checked_Event_Start_time:
        Event_Start_with_indexes.append(Checked_Event_Index)
    else:
        pass

def Find_Conflict_in_DF(Check_DF: DataFrame) -> DataFrame:
    Check_DF["Conflict"] = False
    Check_DF["Conflict_indexes"] = ""
    Check_DF["Start_with_Event"] = ""

    # Define if there is Conflict in the meeting 
    for row in Check_DF.iterrows():
        Event_Series = pandas.Series(row[1])
        Event_Index = row[0]
        Event_Start_time = Event_Series["Start_Time"]
        Event_End_time = Event_Series["End_Time"]

        Event_Conflict = False
        Event_Conflict_indexes = []
        Event_Conflict_SBS_indexes = []
        Event_Start_with_indexes = []
        Event_End_with_indexes = []

        for row2 in Check_DF.iterrows():
            Checked_Event_Series = pandas.Series(row2[1])
            Checked_Event_Index = row2[0]
            Checked_Event_Start_time = Checked_Event_Series["Start_Time"]
            Checked_Event_End_time = Checked_Event_Series["End_Time"]  

            # Check if Event is overlapped by another event
            if Event_Index != Checked_Event_Index:
                # Checked_Event starts before/same but ends sooner (Group=1)
                if (Checked_Event_Start_time <= Event_Start_time) and (Checked_Event_Start_time < Event_End_time) and (Checked_Event_End_time > Event_Start_time) and (Checked_Event_End_time <= Event_End_time):
                    Event_Conflict = True
                    Event_Conflict_indexes.append(Checked_Event_Index)
                    Add_Start_END_Indexes(Checked_Event_Index=Checked_Event_Index, Event_Start_with_indexes=Event_Start_with_indexes, Event_Start_time=Event_Start_time, Checked_Event_Start_time=Checked_Event_Start_time)

                # Checked_Event ends before/same but start sooner (Group=2)
                elif (Checked_Event_Start_time >= Event_Start_time) and (Checked_Event_Start_time < Event_End_time) and (Checked_Event_End_time > Event_Start_time) and (Checked_Event_End_time >= Event_End_time):
                    Event_Conflict = True
                    Event_Conflict_indexes.append(Checked_Event_Index)
                    Add_Start_END_Indexes(Checked_Event_Index=Checked_Event_Index, Event_Start_with_indexes=Event_Start_with_indexes, Event_Start_time=Event_Start_time, Checked_Event_Start_time=Checked_Event_Start_time)

                # Checked_Event inside Event (Group=3)
                elif (Checked_Event_Start_time >= Event_Start_time) and (Checked_Event_Start_time < Event_End_time) and (Checked_Event_End_time > Event_Start_time) and (Checked_Event_End_time <= Event_End_time):
                    Event_Conflict = True
                    Event_Conflict_indexes.append(Checked_Event_Index)
                    Add_Start_END_Indexes(Checked_Event_Index=Checked_Event_Index, Event_Start_with_indexes=Event_Start_with_indexes, Event_Start_time=Event_Start_time, Checked_Event_Start_time=Checked_Event_Start_time)

                # Checked_Event overlap Event (Group=4)
                elif (Checked_Event_Start_time < Event_Start_time) and (Checked_Event_Start_time < Event_End_time) and (Checked_Event_End_time > Event_Start_time) and (Checked_Event_End_time > Event_End_time):
                    Event_Conflict = True
                    Event_Conflict_indexes.append(Checked_Event_Index)
                    Add_Start_END_Indexes(Checked_Event_Index=Checked_Event_Index, Event_Start_with_indexes=Event_Start_with_indexes, Event_Start_time=Event_Start_time, Checked_Event_Start_time=Checked_Event_Start_time)
                else:
                    pass
            else:
                pass

        # Make list unique values
        Event_Conflict_indexes = list(set(Event_Conflict_indexes))
        Event_Conflict_SBS_indexes = list(set(Event_Conflict_SBS_indexes))
        Event_Start_with_indexes = list(set(Event_Start_with_indexes))
        Event_End_with_indexes = list(set(Event_End_with_indexes))

        # Update values
        Check_DF.at[Event_Index, "Conflict"] = Event_Conflict
        Check_DF.at[Event_Index, "Conflict_indexes"] = Event_Conflict_indexes
        Check_DF.at[Event_Index, "Start_with_Event"] = Event_Start_with_indexes
        
    Check_DF = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Check_DF, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
    return Check_DF

def removing_elements(my_list: list, element) -> list:
   result = [i for i in my_list if i != element]
   return result

def Event_End_Cut(Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event End will be cut by SubEvent
    if (Event_Start_Time <= Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time <= Sub_Event_End_Time):
        Event_End_Time = Sub_Event_Start_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        return True
    else:
        return False

def Event_Start_Cut(Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event Start will be cut by SubEvent
    if (Event_Start_Time == Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time > Sub_Event_End_Time):
        Event_Start_Time = Sub_Event_End_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        return True
    else:
        return False
    
def Event_Start_Cut_Lunch(Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event Start will be cut by SubEvent -->just for Lunch event nothing else
    if (Event_Start_Time >= Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time >= Sub_Event_End_Time):
        Event_Start_Time = Sub_Event_End_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        return True
    else:
        return False

def Event_Half_Cut(Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event = SubEvent
    if (Event_Start_Time == Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time == Sub_Event_End_Time):
        Duration = Event_End_Time - Event_Start_Time
        Duration = Duration // 2
        Event_End_Time = Event_Start_Time + Duration
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        return True
    else:
        return False

def Event_Middle_Cut(Conflict_df: DataFrame, Event_Index: int, Data: Series, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # SubEvent is inside totally of Event no borders
    if (Event_Start_Time < Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time > Sub_Event_End_Time):
        # Event 1
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Sub_Event_Start_Time

        # Event 1
        Insert_Index = Conflict_df.shape[0]
        Conflict_df.loc[Insert_Index] = Data
        Conflict_df.at[Insert_Index, "Start_Time"] = Sub_Event_End_Time
        Conflict_df.at[Insert_Index, "End_Time"] = Event_End_Time
        
        Event_End_Time = Sub_Event_Start_Time
        return True
    else:
        return False

def Parallel_Events_Handler(Conflict_df: DataFrame) -> DataFrame:
    # Sort because of 3 and more same start events
    if Start_Method == "Use Shorter":
        Conflict_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Conflict_df, Columns_list=["Start_Date", "Start_Time", "Duration"], Accenting_list=[False, False, False]) 
    elif Start_Method == "Use Longer":
        Conflict_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Conflict_df, Columns_list=["Start_Date", "Start_Time", "Duration"], Accenting_list=[False, False, True]) 
    else:
        Conflict_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Conflict_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[False, False]) 

    Return = False
    for row in Conflict_df.iterrows():
        # Define current row as pandas Series
        row_Series = pandas.Series(row[1])
        Event_Index = row[0]
        Event_Start_Time = row_Series["Start_Time"]
        Event_End_Time = row_Series["End_Time"]
        Event_Duration = row_Series["Duration"]

        # Shorten current event if something is by subEvent
        for Sub_row in Conflict_df.iterrows():
            Sub_row_Series = pandas.Series(Sub_row[1])
            Sub_Event_Index = Sub_row[0]
            Sub_Event_Start_Time = Sub_row_Series["Start_Time"]
            Sub_Event_End_Time = Sub_row_Series["End_Time"]
            Sub_Event_Duration = Sub_row_Series["Duration"]

            # Split event
            if Event_Index != Sub_Event_Index:
                # Start_Method - defender
                if Event_Start_Time == Sub_Event_Start_Time:
                    if Start_Method == "Use Shorter":
                        # Check if Event Duration > Sub Event Duration
                        if Event_Duration >= Sub_Event_Duration:
                            pass
                        else:
                            continue
                    elif Start_Method == "Use Longer":
                        # Check if Event Duration < Sub Event Duration
                        if Event_Duration <= Sub_Event_Duration:
                            pass
                        else:
                            continue

                    else:
                        pass

                else:
                    pass

                # Event End will be cut by SubEvent
                if Return == False:
                    Return = Event_End_Cut(Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                else:
                    pass
                
                # Event Start will be cut by SubEvent
                if Return == False:
                    Return = Event_Start_Cut(Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                else:
                    pass
                
                # Event = SubEvent
                if Return == False:
                    Return = Event_Half_Cut(Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                else:
                    pass
            
                # SubEvent is inside totally of Event no borders
                if Return == False:
                    Return = Event_Middle_Cut(Conflict_df=Conflict_df, Event_Index=Event_Index, Data=row_Series, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                else:
                    pass

            if Return == True:
                # if one change is done then return to main Parallel handler to process again --> because it is better 
                print(Conflict_df)
                return Conflict_df
            else:
                pass
    return Conflict_df

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Parallel_Events(Events: DataFrame):
    if Parallel_Enabled == True:
        Cumulated_Events = pandas.DataFrame()
        #Get Days details from Events
        Days_List = Days_Handler(Events)

        for Day in Days_List:
            mask1 = Events["Start_Date"] == Day
            Day_Events_df = Events.loc[mask1]

            # Define Conflict within the day
            Day_Events_df = Find_Conflict_in_DF(Check_DF=Day_Events_df)

            # Add non-Conflict to Cumulated
            mask1 = Day_Events_df["Conflict"] == False
            Non_Conflict_df = Day_Events_df.loc[mask1]
            Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Non_Conflict_df], axis=0)
            
            # Splitting --> done only for Events within same Busy_Status_Priorities_List
            mask1 = Day_Events_df["Conflict"] == True
            Conflict_df = Day_Events_df.loc[mask1]

            if Conflict_df.empty:
                pass
            else:
                # ------------------------------ Event_Empty_Insert Handler ------------------------------ #
                Empty_Index_to_Del_list = []
                for row in Conflict_df.iterrows():
                    # Define current row as pandas Series
                    row_Series = pandas.Series(row[1])
                    Event_Index = row[0]
                    Event_Empty_Insert = row_Series["Event_Empty_Insert"]
                    if Event_Empty_Insert == True:
                        Event_Start_Time = row_Series["Start_Time"]
                        Event_End_Time = row_Series["End_Time"]
                        for sub_row in Conflict_df.iterrows():
                            # Define current row as pandas Series
                            Sub_row_Series = pandas.Series(sub_row[1])
                            Sub_Event_Index = sub_row[0]
                            Sub_Event_Start_Time = Sub_row_Series["Start_Time"]
                            Sub_Event_End_Time = Sub_row_Series["End_Time"]
                            if Event_Index != Sub_Event_Index:
                                if (Event_Start_Time >= Sub_Event_Start_Time) and (Event_End_Time <= Sub_Event_End_Time):
                                    # Delete Event inserted by Automation
                                    Empty_Index_to_Del_list.append(Event_Index)
                                    break
                                else:
                                    pass
                            else:
                                pass
                    else:
                        continue

                # Delete all rows 
                for Empty_Index_to_Del in Empty_Index_to_Del_list:
                    Conflict_df.drop(labels=[Empty_Index_to_Del], axis=0, inplace=True)

                # Update Conflict_df values
                for Empty_Index_to_Del in Empty_Index_to_Del_list:
                    for row in Conflict_df.iterrows():
                        # Define current row as pandas Series
                        row_Series = pandas.Series(row[1])
                        Event_Index = row[0]
                        Event_Conflict_indexes = row_Series["Conflict_indexes"]
                        Event_Start_with_Events = row_Series["Start_with_Event"]

                        # Conflict_indexes
                        Event_Conflict_Count = Event_Conflict_indexes.count(Empty_Index_to_Del)
                        if Event_Conflict_Count > 0:
                            Event_Conflict_indexes = removing_elements(my_list=Event_Conflict_indexes, element=Empty_Index_to_Del)
                            Conflict_df.at[Event_Index, "Conflict_indexes"] = Event_Conflict_indexes
                            if not Event_Conflict_indexes:
                                # Not an Conflict any more
                                Conflict_df.at[Event_Index, "Conflict"] = False
                            else:
                                pass
                        else:
                            pass
                            
                        # Start_with_Event
                        Event_Start_Count = Event_Start_with_Events.count(Empty_Index_to_Del)
                        if Event_Start_Count > 0:
                            Event_Start_with_Events = removing_elements(my_list=Event_Start_with_Events, element=Empty_Index_to_Del)
                            Conflict_df.at[Event_Index, "Start_with_Event"] = Event_Start_with_Events
                        else:
                            pass

                # ------------------------------ Conflict_df update after Function ------------------------------ #
                # Add non-Conflict to Cumulated --> might be changed as previous function change it
                mask1 = Conflict_df["Conflict"] == False
                Non_Conflict_df = Conflict_df.loc[mask1]
                Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Non_Conflict_df], axis=0)

                # Update Conflict_df
                mask1 = Conflict_df["Conflict"] == True
                Conflict_df = Conflict_df.loc[mask1]

                # ------------------------------ Parallel Events Handler ------------------------------ #
                while True:
                    if Conflict_df.empty:
                        break
                    else:
                        Conflict_df = Parallel_Events_Handler(Conflict_df=Conflict_df)
                                
                        # Duration change
                        Conflict_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Conflict_df, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 
                        for row in Conflict_df.iterrows():
                            row_Series = pandas.Series(row[1])
                            Event_Start_Time = row_Series["Start_Time"]
                            Event_End_Time = row_Series["End_Time"]
                            Conflict_df.at[row[0], "Duration"] = Duration_Counter(Time1=Event_Start_Time, Time2=Event_End_Time)

                        print(Conflict_df)
                        Conflict_df = Find_Conflict_in_DF(Check_DF=Conflict_df)
                        print(Conflict_df)

                        mask1 = Conflict_df["Conflict"] == False
                        Non_Conflict_df = Conflict_df.loc[mask1]
                        Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Non_Conflict_df], axis=0)

                        # Update Conflict_df
                        mask1 = Conflict_df["Conflict"] == True
                        Conflict_df = Conflict_df.loc[mask1]
                                    
            # Delete variables
            del Non_Conflict_df, Conflict_df, Day_Events_df

        # Delete helper columns
        Cumulated_Events.drop(labels=["Conflict", "Conflict_indexes", "Start_with_Event"], axis=1, inplace=True)

        # Get Rid of Duration = 0
        mask = Cumulated_Events["Duration"] == 0
        Cumulated_Events = Cumulated_Events[~mask]

        return Cumulated_Events

    else:
        return Events

