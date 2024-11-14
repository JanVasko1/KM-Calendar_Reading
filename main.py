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
import Libs.Sharepoint.Sharepoint as Sharepoint
import Libs.Defaults_Lists as Defaults_Lists

from pandas import DataFrame
import json

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Time_format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
# Download Events
Events = Downloader.Download_Events()
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

# Las querstion
Correct = input(f"\n Do you want to auto upload to Sharepoit? [Y/N]?")
Correct = Correct.upper()
if Correct == "Y":
    # Uploader
    Sharepoint.Upload(Events=Events)
else:
    print("Nothing be uploaded automaticaly.")
