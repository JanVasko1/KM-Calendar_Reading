# Import Libraries
from pandas import DataFrame as DataFrame
from datetime import datetime
from tqdm import tqdm
import win32com.client
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Download.Downloader_Helpers as Downloader_Helpers

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]
Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]

BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str) -> DataFrame:
    # Access Outlook and get the events from the calendar
    Outlook = win32com.client.Dispatch("Outlook.Application")
    ns = Outlook.GetNamespace("MAPI")

    # get only mentioned Account
    account_name = Email
    account = None
    for acc in ns.Folders:
        if acc.Name == account_name:
            account = acc
            break

    #! Dodělat --> připojit se pouze k jednomu Account

    appts = ns.GetDefaultFolder(9).Items
    appts.Sort("[Start]")
    appts.IncludeRecurrences = True

    # download Events within interval or thoes which thin day + Event which are bigger than interval, Event which starts before and finish in interval, and Events which Start within interval, but finish after interval
    appts = appts.Restrict(f"""
        ([Start] >= '{Filter_Start_Date}' AND [END] <= '{Filter_End_Date}') OR 
        ([Start] < '{Filter_Start_Date}' AND [END] > '{Filter_End_Date}') OR
        ([Start] < '{Filter_Start_Date}' AND [Start] < '{Filter_End_Date}' AND [END] >= '{Filter_Start_Date}' AND [END] <= '{Filter_End_Date}') OR
        ([Start] >= '{Filter_Start_Date}' AND [Start] <= '{Filter_End_Date}' AND [END] > '{Filter_Start_Date}' AND [END] > '{Filter_End_Date}')""")

    Events_downloaded = {}
    Counter = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(len(appts)),desc=f"{now}>> Downloader")
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
        Busyindex = int(Event.BusyStatus)
        Busy_Status = BusyStatus_List[Busyindex]
        Location = str(Event.Location)
        All_Day_Event = Event.AllDayEvent
        Body = Event.Body

        # Project --> secure only one be used outlook can have 2: Use first one only
        Project = Downloader_Helpers.Project_handler(Project=Project)

        # Activity --> in the Body as predefined text
        Activity = Downloader_Helpers.Activity_handler(Body=Body)

        # Location --> Get only Meeting Room
        Location = Downloader_Helpers.Location_handler(Location=Location)

        # Udpate End_Date for all Day Event and split them to every day event
        Events_downloaded, Counter = Downloader_Helpers.All_Day_Event_End_Handler(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, End_Date_dt=End_Date_dt, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)

        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    # Close Outlook
    Outlook.Quit()

    # Crop edge dates as they were added in previous step
    Events_Process = Downloader_Helpers.Crop_edge_days_Events(Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Date_format=Date_format)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T
    return Events_Process_df
