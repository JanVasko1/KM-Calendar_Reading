# Import Libraries
from pandas import DataFrame

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

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Time_format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Download_and_Process(Download_Date_Range_Source: str, Download_Data_Source: str, SP_Password: str|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None):
    # Download Events
    Events = Downloader.Download_Events(Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    # Process Events
    Events = Divide_Events.OverMidnight_Events(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Fill_Empty_Place.Fill_Events(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Fill_Empty_Place.Fill_Events_Coverage(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Location_Set.Location_Set(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Special_Events.Lunch(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Skip_Events.Skip_Events(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Parralel_Events.Parralel_Events(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = AutoFiller.AutoFiller(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Special_Events.Vacation(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Special_Events.HomeOffice(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    Events = Join_Events.Join_Events(Events=Events)
    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

    # Sumamry Dataframes
    Events = Summary.Generate_Summary(Events=Events)
