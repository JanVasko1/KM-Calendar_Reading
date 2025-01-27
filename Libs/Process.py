# Import Libraries
import Libs.Download.Downloader as Downloader

import Libs.Event_Handler.Fill_Empty_Place as Fill_Empty_Place
import Libs.Event_Handler.Divide_Events as Divide_Events
import Libs.Event_Handler.Location_Set as Location_Set
import Libs.Event_Handler.Skip_Events as Skip_Events
import Libs.Event_Handler.Parallel_Events as Parallel_Events
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
def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Label: str) -> None:
    Progress_Bar.step()
    Progress_text.configure(text="                                                        ")
    window.update_idletasks()
    Progress_text.configure(text=f"{Label}")
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Label: str, value: int) -> None:
    Progress_Bar.set(value=value)
    Progress_text.configure(text="                                                        ")
    window.update_idletasks()
    Progress_text.configure(text=f"{Label}")
    window.update_idletasks()

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Download_and_Process(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: str, Download_Data_Source: str, SP_Date_From_Method: str, SP_Date_To_Method: str, SP_Man_Date_To: str, SP_Password: str|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None):
    # Download Events 
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    Events, Events_Registered_df, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Download_canceled = Downloader.Download_Events(Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Date_From_Method=SP_Date_From_Method, SP_Date_To_Method=SP_Date_To_Method, SP_Man_Date_To=SP_Man_Date_To, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    
    if Download_canceled == False:
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Process Events
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Overnight Events") 
        Events = Divide_Events.OverMidnight_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty") 
        Events = Fill_Empty_Place.Fill_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Too long Empty Events") 
        Events = Divide_Events.Empty_Split_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty Coverage") 
        Events = Fill_Empty_Place.Fill_Events_Coverage(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True])

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Location set") 
        Events = Location_Set.Location_Set(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Lunch") 
        Events = Special_Events.Lunch(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Skip Events") 
        Events = Skip_Events.Skip_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Parallel Events") 
        Events = Parallel_Events.Parallel_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="AutoFilling") 
        Events = AutoFiller.AutoFiller(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Auto Activity Corrections") 
        Events = AutoFiller.Auto_Activity_Corrections(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Vacation") 
        Events = Special_Events.Vacation(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="HomeOffice") 
        Events = Special_Events.HomeOffice(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Joining Events") 
        Events = Join_Events.Join_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Summary Dataframe
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
        Events = Summary.Generate_Summary(Events=Events, Events_Registered_df=Events_Registered_df, Report_Period_Active_Days=Report_Period_Active_Days, Report_Period_Start=Report_Period_Start, Report_Period_End=Report_Period_End)

        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Done", value=1) 
        CTkMessagebox(title="Success", message="Successfully downloaded and processed.", icon="check", option_1="Thanks", fade_in_duration=1)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Canceled", value=0) 