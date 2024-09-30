from pandas import DataFrame, Series
import pandas
import json
from datetime import datetime
from tqdm import tqdm

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

Divide_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Divide_Method"]
Start_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Start_Method"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Couter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minues
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Dataframe_sort(Dataframe: DataFrame, Sort: bool) -> None:
    # Sort DAtaframe and reindex 
    Dataframe.sort_values(by=["Start_Date", "Start_Time"], ascending=[Sort, Sort], axis=0, inplace = True)
    Dataframe.reset_index(inplace=True)
    Dataframe.drop(labels=["index"], inplace=True, axis=1)

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

def Find_Conflit_in_DF(Check_DF: DataFrame) -> DataFrame:
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

            # Check if Event is overlaped by another event
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
        
    Dataframe_sort(Dataframe=Check_DF, Sort=True) 
    return Check_DF

def removing_elements(my_list: list, element) -> list:
   result = [i for i in my_list if i != element]
   return result

def Event_End_Cut(Continue: bool, Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event End will be cut by SubEvent
    if (Event_Start_Time <= Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time <= Sub_Event_End_Time):
        Event_End_Time = Sub_Event_Start_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        
        Continue = True
        return Continue
    else:
        return Continue

def Event_Start_Cut(Continue: bool, Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event Start will be cut by SubEvent
    if (Event_Start_Time == Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time > Sub_Event_End_Time):
        Event_Start_Time = Sub_Event_End_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        
        Continue = True
        return Continue
    else:
        return Continue
    
def Event_Start_Cut_Lunch(Continue: bool, Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event Start will be cut by SubEvent -->just for Lunch event nothing else
    if (Event_Start_Time >= Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time >= Sub_Event_End_Time):
        Event_Start_Time = Sub_Event_End_Time
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        
        Continue = True
        return Continue
    else:
        return Continue

def Event_Half_Cut(Continue: bool, Conflict_df: DataFrame, Event_Index: int, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # Event = SubEvent
    if (Event_Start_Time == Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time == Sub_Event_End_Time):
        Duration = Event_End_Time - Event_Start_Time
        Duration = Duration // 2
        Event_End_Time = Event_Start_Time + Duration
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Event_End_Time
        
        Continue = True
        return Continue
    else:
        return Continue

def Event_Middle_Cut(Continue: bool, Conflict_df: DataFrame, Event_Index: int, Data: Series, Event_Start_Time: datetime, Event_End_Time: datetime, Sub_Event_Start_Time: datetime, Sub_Event_End_Time: datetime) -> bool:
    # SubEvent is inside totaly of Event no borders
    if (Event_Start_Time < Sub_Event_Start_Time) and (Event_Start_Time < Sub_Event_End_Time) and (Event_End_Time > Sub_Event_Start_Time) and (Event_End_Time > Sub_Event_End_Time):
        # Event 1
        Conflict_df.at[Event_Index, "Start_Time"] = Event_Start_Time
        Conflict_df.at[Event_Index, "End_Time"] = Sub_Event_Start_Time

        # Event 1
        Inser_Index = Conflict_df.shape[0]
        Conflict_df.loc[Inser_Index] = Data
        Conflict_df.at[Inser_Index, "Start_Time"] = Sub_Event_End_Time
        Conflict_df.at[Inser_Index, "End_Time"] = Event_End_Time
        
        Event_End_Time = Sub_Event_Start_Time
        Continue = True
        return Continue
    else:
        return Continue


def Parralel_Events_Handler(Conflict_df: DataFrame) -> DataFrame:
    Continue = True
    while Continue==True:
        Dataframe_sort(Dataframe=Conflict_df, Sort=False) 
        Continue = False
        for row in Conflict_df.iterrows():
            # Define current row as pandas Series
            row_Series = pandas.Series(row[1])
            Event_Index = row[0]
            Event_Start_Time = row_Series["Start_Time"]
            Event_End_Time = row_Series["End_Time"]

            # Shorten current event if something is by subEvent
            for Sub_row in Conflict_df.iterrows():
                Sub_row_Series = pandas.Series(Sub_row[1])
                Sub_Event_Index = Sub_row[0]
                Sub_Event_Start_Time = Sub_row_Series["Start_Time"]
                Sub_Event_End_Time = Sub_row_Series["End_Time"]

                # Split larger event
                if Event_Index != Sub_Event_Index:
                    # Event End will be cut by SubEvent
                    Continue = Event_End_Cut(Continue=Continue, Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                    
                    # Event Start will be cut by SubEvent
                    Continue = Event_Start_Cut(Continue=Continue, Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                    
                    # Event = SubEvent
                    Continue = Event_Half_Cut(Continue=Continue, Conflict_df=Conflict_df, Event_Index=Event_Index, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)
                
                    # SubEvent is inside totaly of Event no borders
                    Continue = Event_Middle_Cut(Continue=Continue, Conflict_df=Conflict_df, Event_Index=Event_Index, Data=row_Series, Event_Start_Time=Event_Start_Time, Event_End_Time=Event_End_Time, Sub_Event_Start_Time=Sub_Event_Start_Time, Sub_Event_End_Time=Sub_Event_End_Time)

    return Conflict_df

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Parralel_Events(Events: DataFrame):
    if Divide_Method == "Divide":
        Cumulated_Events = pandas.DataFrame()
        #Get Days details from Events
        Days_List = Days_Handler(Events)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Data_df_TQDM = tqdm(total=int(len(Days_List)),desc=f"{now}>> Parralel Meetings")
        for Day in Days_List:
            mask1 = Events["Start_Date"] == Day
            Day_Events_df = Events.loc[mask1]

            # Define Conflict within the day
            Day_Events_df = Find_Conflit_in_DF(Check_DF=Day_Events_df)

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
                    Event_Empty_Insert = row_Series["Event_Empty_Insert"]
                    Event_Index = row[0]
                    if Event_Empty_Insert == True:
                        Event_Start_Time = row_Series["Start_Time"]
                        Event_End_Time = row_Series["End_Time"]
                        for sub_row in Conflict_df.iterrows():
                            # Define current row as pandas Series
                            Sub_row_Series = pandas.Series(sub_row[1])
                            Sub_Event_Start_Time = Sub_row_Series["Start_Time"]
                            Sub_Event_End_Time = Sub_row_Series["End_Time"]
                            if (Event_Start_Time >= Sub_Event_Start_Time) and (Event_End_Time <= Sub_Event_End_Time):
                                # Delete Event inserted by Automation
                                Empty_Index_to_Del_list.append(Event_Index)
                                break
                            else:
                                pass
                    else:
                        continue

                # Delete all rows 
                for Empty_Index_to_Del in Empty_Index_to_Del_list:
                    Conflict_df.drop(labels=[Empty_Index_to_Del], axis=0, inplace=True)

                # Udpate Conflict_df values
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

                # ------------------------------ Parralel Events Handler ------------------------------ #
                if Conflict_df.empty:
                    pass
                else:
                    Conflict_df = Parralel_Events_Handler(Conflict_df=Conflict_df)
                            
                    # Duration change
                    Dataframe_sort(Dataframe=Conflict_df, Sort=True) 
                    for row in Conflict_df.iterrows():
                        row_Series = pandas.Series(row[1])
                        Event_Start_Time = row_Series["Start_Time"]
                        Event_End_Time = row_Series["End_Time"]
                        Conflict_df.at[row[0], "Duration"] = Duration_Couter(Time1=Event_Start_Time, Time2=Event_End_Time)
                    
                    # Add to Cumulated
                    Conflict_df.drop(Conflict_df[Conflict_df["Duration"] == 0].index, inplace = True)
                    Cumulated_Events = pandas.concat(objs=[Cumulated_Events, Conflict_df], axis=0)

            # Delete variables
            del Non_Conflict_df, Conflict_df, Day_Events_df

            Data_df_TQDM.update(1) 
        Data_df_TQDM.close()

        # Delete helper columns
        Cumulated_Events.drop(labels=["Conflict", "Conflict_indexes", "Start_with_Event"], axis=1, inplace=True)
        return Cumulated_Events
    elif Divide_Method == "Keep_Parralel":
        return Events
    else:
        return Events

