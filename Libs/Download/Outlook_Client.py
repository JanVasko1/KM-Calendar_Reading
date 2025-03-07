# Import Libraries
from pandas import DataFrame as DataFrame
from datetime import datetime
import win32com.client
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Download.Downloader_Helpers as Downloader_Helpers

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Settings: dict, Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str) -> DataFrame:
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Time_format = Settings["0"]["General"]["Formats"]["Time"]
    BusyStatus_List = Defaults_Lists.Busy_Status_List()

    # Access Outlook and get the events from the calendar
    Outlook = win32com.client.Dispatch("Outlook.Application")
    ns = Outlook.GetNamespace("MAPI")

    appts = ns.GetDefaultFolder(9).Items
    appts.Sort("[Start]")
    appts.IncludeRecurrences = True

    # download Events within interval or those which thin day + Event which are bigger than interval, Event which starts before and finish in interval, and Events which Start within interval, but finish after interval
    appts = appts.Restrict(f"""
        ([Start] >= '{Filter_Start_Date}' AND [END] <= '{Filter_End_Date}') OR 
        ([Start] < '{Filter_Start_Date}' AND [END] > '{Filter_End_Date}') OR
        ([Start] < '{Filter_Start_Date}' AND [Start] < '{Filter_End_Date}' AND [END] >= '{Filter_Start_Date}' AND [END] <= '{Filter_End_Date}') OR
        ([Start] >= '{Filter_Start_Date}' AND [Start] <= '{Filter_End_Date}' AND [END] > '{Filter_Start_Date}' AND [END] > '{Filter_End_Date}')""")

    Events_downloaded = {}
    Counter = 0
    for indx, Event in enumerate(appts):
        Subject = str(Event.Subject)
        Start_Date_dt = datetime(year=Event.Start.year, month=Event.Start.month, day=Event.Start.day, hour=Event.Start.hour, minute=Event.Start.minute)
        Start_Date = Start_Date_dt.strftime(Date_format)
        Start_Time = Start_Date_dt.strftime(Time_format)
        End_Date_dt = datetime(year=Event.End.year, month=Event.End.month, day=Event.End.day, hour=Event.End.hour, minute=Event.End.minute)
        End_Date = End_Date_dt.strftime(Date_format)
        End_Time = End_Date_dt.strftime(Time_format)
        Duration = int(Event.duration)
        Project = str(Event.Categories)
        Recurring = Event.IsRecurring
        Busy_index = int(Event.BusyStatus)
        Busy_Status = BusyStatus_List[Busy_index]
        Location = str(Event.Location)
        All_Day_Event = Event.AllDayEvent
        Body = Event.Body

        # Project --> secure only one be used outlook can have 2: Use first one only
        Project = Downloader_Helpers.Project_handler(Settings=Settings, Project=Project)

        # Activity --> in the Body as predefined text
        Activity = Downloader_Helpers.Activity_handler(Settings=Settings, Body=Body)

        # Location --> Get only Meeting Room
        Location = Downloader_Helpers.Location_handler(Settings=Settings, Location=Location)

        # Update End_Date for all Day Event and split them to every day event
        Events_downloaded, Counter = Downloader_Helpers.All_Day_Event_End_Handler(Settings=Settings, Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, End_Date_dt=End_Date_dt, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)

    # Close Outlook
    Outlook.Quit()

    # Crop edge dates as they were added in previous step
    Events_Process = Downloader_Helpers.Crop_edge_days_Events(Settings=Settings, Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T

    return Events_Process_df
