# Import Libraries
from pandas import DataFrame as DataFrame
from dotenv import load_dotenv
import requests
from datetime import datetime
import Libs.Download.Outlook_Client as Outlook_Client
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Download.Downloader_Helpers as Downloader_Helpers

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]
Exchange_DateTime_format = Settings["General"]["Formats"]["Exchange_DateTime"]
Exchange_Busy_Status_List = Defaults_Lists.Exchange_Busy_Status_List()
Busy_Status_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Counter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minuets
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Add_Events_downloaded(Events_downloaded: dict, Events: dict, Counter: int) -> None:
    for Event in Events["value"]:
        Subject = str(Event["subject"])
        Start_Date_correction = str(Event["start"]["dateTime"])
        Start_Date_correction = Start_Date_correction.split(sep=".")
        Start_Date_dt = datetime.strptime(Start_Date_correction[0], Exchange_DateTime_format)
        Start_Date = Start_Date_dt.strftime(Date_format)
        Start_Time = Start_Date_dt.strftime(Time_format)
        End_Date_correction = str(Event["end"]["dateTime"])
        End_Date_correction = End_Date_correction.split(sep=".")
        End_Date_dt = datetime.strptime(End_Date_correction[0], Exchange_DateTime_format)
        End_Date = End_Date_dt.strftime(Date_format)
        End_Time = End_Date_dt.strftime(Time_format)
        Duration = Duration_Counter(Time1=Start_Date_dt, Time2=End_Date_dt)
        Project_list = Event["categories"]
        if len(Project_list) == 0:
            Project = ""
        else:
            Project = "; ".join(Project_list)
        Recurring = Event["recurrence"]
        if not Recurring:
            Recurring = False
        else:
            Recurring = True
        Busy_Status = Event["showAs"]
        Busy_index = Exchange_Busy_Status_List.index(Busy_Status)
        Busy_Status = Busy_Status_List[Busy_index]
        Location = Event["location"]["displayName"]
        All_Day_Event = Event["isAllDay"]
        Body = Event["bodyPreview"]

        # Project --> secure only one be used outlook can have 2: Use first one only
        Project = Downloader_Helpers.Project_handler(Project=Project)

        # Activity --> in the Body as predefined text
        Activity = Downloader_Helpers.Activity_handler(Body=Body)

        # Location --> Get only Meeting Room
        Location = Downloader_Helpers.Location_handler(Location=Location)

        # Update End_Date for all Day Event and split them to every day event
        Events_downloaded, Counter = Downloader_Helpers.All_Day_Event_End_Handler(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, End_Date_dt=End_Date_dt, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)

    return Counter

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str, Exchange_Password: str) -> DataFrame:
    import getpass
    # Load OAuth2 info
    client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
    username = Settings["General"]["Downloader"]["Outlook"]["Calendar"]

    if not client_id:
        CTkMessagebox(title="Error", message=f"No client_id found. Check your .env file.", icon="cancel", fade_in_duration=1)
        raise ValueError()
    if not client_secret:
        CTkMessagebox(title="Error", message=f"No client_secret found. Check your .env file.", icon="cancel", fade_in_duration=1)
        raise ValueError()
    if not tenant_id:
        CTkMessagebox(title="Error", message=f"No tenant_id found. Check your .env file.", icon="cancel", fade_in_duration=1)
        raise ValueError()

    # OAuth2 authentication at KM Azure
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "username": username,
        "password": Exchange_Password}
    response = requests.post(url=url, data=payload)
    tokens = response.json()
    access_token = tokens["access_token"]

    # Update filters
    Filter_Start_Date = Filter_Start_Date + "T00:00:00Z"
    Filter_End_Date = Filter_End_Date + "T23:59:59Z"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": 'outlook.timezone="Europe/Paris"'}

    params = {
        "startDateTime": Filter_Start_Date,
        "endDateTime": Filter_End_Date,
        "$orderby": f"start/dateTime desc",
        "$top": 1000,
        "$count": "true",
        "$select": "subject, start, end, categories, recurrence, showAs, location, isAllDay, bodyPreview"}

    Events_downloaded = {}
    events_url = f"https://graph.microsoft.com/v1.0/users/{username}/calendar/calendarView"
    events_response = requests.get(url=events_url, headers=headers, params=params)

    Counter = 0 
    if response.status_code == 200:
        # Init page 
        Events = events_response.json()
        Counter = Add_Events_downloaded(Events_downloaded=Events_downloaded, Events=Events, Counter=Counter) 

        # Check if there are more pages of results 
        while '@odata.nextLink' in Events:
            next_link = Events['@odata.nextLink']
            response = requests.get(next_link, headers=headers) 
            if response.status_code == 200: 
                Events = response.json()
                Counter = Add_Events_downloaded(Events_downloaded=Events_downloaded, Events=Events, Counter=Counter)       
    else:
        CTkMessagebox(title="Info", message=f"Not possible to download from Exchange (Response Code: {response.status_code}), will try to download from Outlook Classic Client.", fade_in_duration=1)
        Events_downloaded = {}
        Events_Process_df = Outlook_Client.Download_Events(Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Filter_Start_Date=Filter_Start_Date, Filter_End_Date=Filter_End_Date) 

    # Crop edge dates as they were added in previous step
    Events_Process = Downloader_Helpers.Crop_edge_days_Events(Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Date_format=Date_format)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T
    return Events_Process_df
