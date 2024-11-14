# Import Libraries
import json
from pandas import DataFrame as DataFrame
from datetime import datetime, timedelta
from tqdm import tqdm
import win32com.client
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]

BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Add_to_Events_dict(Events_downloaded: dict, Counter: int, Subject: str, Start_Date: str, End_Date: str, Start_Time: str, End_Time: str, Duration: int, Project: str, Activity: str, Recurring: bool, Busy_Status: str, Location: str, All_Day_Event: bool) -> None: 
    Events_downloaded[Counter] = {
        "Subject": Subject, 
        "Start_Date": Start_Date, 
        "End_Date": End_Date,
        "Start_Time": Start_Time, 
        "End_Time": End_Time,
        "Duration": Duration,
        "Project": Project,
        "Activity": Activity,
        "Recurring": Recurring,
        "Busy_Status": Busy_Status,
        "Meeting_Room": Location,
        "All_Day_Event": All_Day_Event,
        "Event_Empty_Insert": False,
        "Event_Empty_Method": "",
        "Within_Working_Hours": False,
        "Location": "Office"}

def Duration_Change(Events_downloaded: dict, key:int, value: dict) -> None:
    Start_Date_Time = f"""{value["Start_Date"]}_{value["Start_Time"]}"""
    End_Date_Time = f"""{value["End_Date"]}_{value["End_Time"]}"""
    Start_Date_Time_dt = datetime.strptime(Start_Date_Time, f"{Date_format}_{Time_format}")
    End_Date_Time_dt = datetime.strptime(End_Date_Time, f"{Date_format}_{Time_format}")
    if End_Date_Time_dt.minute == 59:
        End_Date_Time_dt = End_Date_Time_dt + timedelta(minutes=1)

    Duration_dt = End_Date_Time_dt - Start_Date_Time_dt

    Duration = (int(Duration_dt.total_seconds())) // 60
    Events_downloaded[key]["Duration"] = Duration

def Crop_edge_days_Events(Events_downloaded: dict, Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Date_format: str) -> dict:
    Events_Process = {}
    Counter = 0
    for key, value in Events_downloaded.items():
        Event_Start_Date_dt = datetime.strptime(value["Start_Date"], Date_format)
        Event_End_Date_dt = datetime.strptime(value["End_Date"], Date_format)

        # Event within Input Dates interval
        if (Event_Start_Date_dt >= Input_Start_Date_dt) and (Event_Start_Date_dt <= Input_End_Date_dt) and (Event_End_Date_dt >= Input_Start_Date_dt) and (Event_End_Date_dt <= Input_End_Date_dt):
            Events_Process[Counter] = value
            Counter += 1

        # Event Crossing Input Start Date
        elif (Event_Start_Date_dt < Input_Start_Date_dt) and (Event_Start_Date_dt < Input_End_Date_dt) and (Event_End_Date_dt >= Input_Start_Date_dt) and (Event_End_Date_dt <= Input_End_Date_dt):
            # Modify Start_Date and Start_Time
            Event_Start_Date = Input_Start_Date_dt.strftime(Date_format)
            Event_Start_Time = "00:00"
            Events_downloaded[key]["Start_Date"] = Event_Start_Date
            Events_downloaded[key]["Start_Time"] = Event_Start_Time
            Duration_Change(Events_downloaded=Events_downloaded, key=key, value=value) 

            Events_Process[Counter] = value
            Counter += 1
    
        # Event Crossing Input End Date
        elif (Event_Start_Date_dt >= Input_Start_Date_dt) and (Event_Start_Date_dt <= Input_End_Date_dt) and (Event_End_Date_dt >= Input_Start_Date_dt) and (Event_End_Date_dt > Input_End_Date_dt):
            # Modify End_Date and End_Time
            Event_End_Date = Input_End_Date_dt.strftime(Date_format)
            Event_End_Time = "23:59"
            Events_downloaded[key]["End_Date"] = Event_End_Date
            Events_downloaded[key]["End_Time"] = Event_End_Time
            Duration_Change(Events_downloaded=Events_downloaded, key=key, value=value) 

            Events_Process[Counter] = value
            Counter += 1

        # Event Crossing both Input Start/End Date 
        elif (Event_Start_Date_dt < Input_Start_Date_dt) and (Event_Start_Date_dt < Input_End_Date_dt) and (Event_End_Date_dt > Input_Start_Date_dt) and (Event_End_Date_dt > Input_End_Date_dt):
            # Modify Start_Date and Start_Time
            Event_Start_Date = Input_Start_Date_dt.strftime(Date_format)
            Event_Start_Time = "00:00"
            Events_downloaded[key]["Start_Date"] = Event_Start_Date
            Events_downloaded[key]["Start_Time"] = Event_Start_Time

            # Modify End_Date and End_Time
            Event_End_Date = Input_End_Date_dt.strftime(Date_format)
            Event_End_Time = "23:59"
            Events_downloaded[key]["End_Date"] = Event_End_Date
            Events_downloaded[key]["End_Time"] = Event_End_Time
            Duration_Change(Events_downloaded=Events_downloaded, key=key, value=value) 

            Events_Process[Counter] = value
            Counter += 1

        # Events totaly outside the Input Date interval
        else:
            continue

    return Events_Process

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str) -> DataFrame:
    #! Dodělat --> co udělat když se nepodaří stáhnout zatím jsem tu nechal Outlook !!!!!
    # Access Outlook and get the events from the calendar
    Outlook = win32com.client.Dispatch("Outlook.Application")
    ns = Outlook.GetNamespace("MAPI")
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
        Multiple_Projects = Project.find("; ")
        if Multiple_Projects != -1:
            Project_list = Project.split("; ")
            Project = Project_list[0]
        else:
            pass

        # Activity --> in the Body as predefined text
        Activity = ""
        Activity_occurence = Body.find("Activity: ")

        if Activity_occurence != -1:
            body_split = Body.split("Activity: ")
            Sub_body_split = str(body_split[1]).split("\r\n")
            Activity = Sub_body_split[0]
            Activity = Activity.rstrip(" ")
        else:
            pass     

        # Location --> Get only Meeting Room
        if Location != "":
            Location = Location.replace("Microsoft Teams Meeting; ", "")
            Location = Location.replace(" (Brno (Holandská 4))", "")
        else:
            pass

        # Udpate End_Date for all Day Event and split them to every day event
        if (All_Day_Event == True) and (End_Time == "00:00"):
            End_Date_dt = End_Date_dt - timedelta(days=1)
            End_Date = End_Date_dt.strftime(Date_format)
            End_Time = "23:59"

            Add_to_Events_dict(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)
            Counter += 1
        
        else:
            Add_to_Events_dict(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)
            Counter += 1

        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()

    # Close Outlook
    Outlook.Quit()

    # Crop edge dates as they were added in previous step
    Events_Process = Crop_edge_days_Events(Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Date_format=Date_format)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T
    return Events_Process_df
