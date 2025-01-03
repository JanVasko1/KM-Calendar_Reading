# Import Libraries
import Libs.Download.Downloader as Downloader

import Libs.Event_Handler.Fill_Empty_Place as Fill_Empty_Place
import Libs.Event_Handler.Divide_Events as Divide_Events
import Libs.Event_Handler.Location_Set as Location_Set
import Libs.Event_Handler.Skip_Events as Skip_Events
import Libs.Event_Handler.Parralel_Events as Parralel_Events
import Libs.Event_Handler.AutoFiller as AutoFiller
import Libs.Event_Handler.Special_Events as Special_Events
import Libs.Event_Handler.Join_Events as Join_Events
import Libs.Summary as Summary
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTkProgressBar, CTk, CTkLabel
from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Time_format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Local Function ---------------------------------------------------------- #
def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Lable: str) -> None:
    Progress_Bar.step()
    Progress_text.configure(text=f"{Lable}")
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Lable: str) -> None:
    Progress_Bar.set(value=0)
    Progress_text.configure(text=f"{Lable}")
    window.update_idletasks()

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Download_and_Process(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: str, Download_Data_Source: str, SP_Password: str|None, SP_Whole_Period:bool|None, SP_End_Date_Max_Today_Var: bool|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None):
    # Download Events 
    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Downloading") 
    Events, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Input_Start_Date_dt, Input_End_Date_dt, Download_canceled = Downloader.Download_Events(Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Password=SP_Password, SP_Whole_Period=SP_Whole_Period, SP_End_Date_Max_Today_Var=SP_End_Date_Max_Today_Var, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    
    if Download_canceled == False:
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Process Events
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Overniight Events") 
        Events = Divide_Events.OverMidnight_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Too long Empty Events") 
        Events = Divide_Events.Too_Long_Empty_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Fill Empty") 
        Events = Fill_Empty_Place.Fill_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Fill Empty Coverage") 
        Events = Fill_Empty_Place.Fill_Events_Coverage(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Location set") 
        Events = Location_Set.Location_Set(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Lunch") 
        Events = Special_Events.Lunch(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Skip Events") 
        Events = Skip_Events.Skip_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Parralel Events") 
        Events = Parralel_Events.Parralel_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="AutoFilling") 
        Events = AutoFiller.AutoFiller(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Vacation") 
        Events = Special_Events.Vacation(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="HomeOffice") 
        Events = Special_Events.HomeOffice(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Joining Events") 
        Events = Join_Events.Join_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Sumamry Dataframes
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Summary") 
        Events = Summary.Generate_Summary(Events=Events, Report_Period_Active_Days=Report_Period_Active_Days, Report_Period_Start=Report_Period_Start, Report_Period_End=Report_Period_End, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt)
        Progress_Bar.set(value=1)

        CTkMessagebox(title="Success", message="Sucessfully downloaded and processed.", icon="check", option_1="Thanks", fade_in_duration=1)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Lable="Canceled") 