import Libs.Download.Downloader as Downloader

import Libs.Event_Handler.Fill_Empty_Place as Fill_Empty_Place
import Libs.Event_Handler.Divide_Events as Divide_Events
import Libs.Event_Handler.Location_Set as Location_Set
import Libs.Event_Handler.Skip_Events as Skip_Events
import Libs.Event_Handler.Parralel_Events as Parralel_Events
import Libs.Event_Handler.AutoFiller as AutoFiller
import Libs.Event_Handler.Special_Events as Special_Events
import Libs.Summary as Summary
import Libs.Sharepoint.Sharepoint as Sharepoint

from pandas import DataFrame
import json

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Time_format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Dataframe_sort(Dataframe: DataFrame) -> None:
    # Sort Dataframe and reindex 
    Dataframe.sort_values(by=["Start_Date", "Start_Time"], ascending=[True, True], axis=0, inplace = True)
    Dataframe.reset_index(inplace=True)
    Dataframe.drop(labels=["index"], inplace=True, axis=1)

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
while True:
    # Download Events
    Events = Downloader.Download_Events()
    Dataframe_sort(Dataframe=Events) 

    # Process Events
    Events = Divide_Events.OverMidnight_Events(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Fill_Empty_Place.Fill_Events(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Location_Set.Location_Set(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Special_Events.Lunch(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Skip_Events.Skip_Events(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Parralel_Events.Parralel_Events(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = AutoFiller.AutoFiller(Events=Events)
    Dataframe_sort(Dataframe=Events) 
  
    Events = Special_Events.Vacation(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    Events = Special_Events.HomeOffice(Events=Events)
    Dataframe_sort(Dataframe=Events) 

    # Sumamry Dataframes
    Events = Summary.Generate_Summary(Events=Events)

    # Las querstion
    Correct = input(f"\n Do you want to auto upload to Sharepoit? [Y/N]?")
    Correct = Correct.upper()
    if Correct == "Y":
        # Uploader
        Sharepoint.Upload(Events=Events)
        break
    else:
        print("Nothing be uploaded automaticaly.")
        break

