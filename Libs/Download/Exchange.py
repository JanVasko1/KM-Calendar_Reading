# Import Libraries
import json
from pandas import DataFrame as DataFrame
from datetime import datetime
from tqdm import tqdm
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Download.Downloader_Helpers as Downloader_Helpers
from exchangelib import Credentials, Account

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str) -> DataFrame:

    # Replace with your actual email and password
    credentials = Credentials("Jan.Vasko@konicaminolta.eu", "1x810fklL...")
    account = Account("Jan.Vasko@konicaminolta.eu", credentials=credentials, autodiscover=True)
    appts = account.inbox.all().order_by('-datetime_received')[:10]      # Fiktivní promněná pro testování pouze 

    for item in appts:
        print(item.subject, item.sender, item.datetime_received)

    # Access Outlook and get the events from the calendar

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
        Events_downloaded, Counter = Downloader_Helpers.All_Day_Event_End_Handler(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)

        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    # Crop edge dates as they were added in previous step
    Events_Process = Downloader_Helpers.Crop_edge_days_Events(Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Date_format=Date_format)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T
    return Events_Process_df
