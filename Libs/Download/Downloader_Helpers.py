# Import Libraries
from datetime import datetime, timedelta
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]
Activity_Method = Settings["Event_Handler"]["Activity"]["Method"]
Project_Method = Settings["Event_Handler"]["Project"]["Method"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
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

def Project_handler(Project: str) -> str:
    if Project_Method == "Events":
        Multiple_Projects = Project.find("; ")
        if Multiple_Projects != -1:
            Project_list = Project.split("; ")
            Project = Project_list[0]
        else:
            pass
    else:
        Project = ""
    return Project
    
def Activity_handler(Body: str) -> str:
    if Activity_Method == "Events":
        Activity_occurence = Body.find("Activity: ")

        if Activity_occurence != -1:
            body_split = Body.split("Activity: ")
            Sub_body_split = str(body_split[1]).split("\r\n")
            Activity = Sub_body_split[0]
            Activity = Activity.rstrip(" ")
        else:
            Activity = ""   
    else:
        Activity = ""  
    return Activity

def Location_handler(Location: str) -> str:
    if Location != "":
        Location = Location.replace("Microsoft Teams Meeting; ", "")
        Location = Location.replace(" (Brno (Holandská 4))", "")
    else:
        pass
    return Location

def All_Day_Event_End_Handler(Events_downloaded: dict, Counter: int, Subject: str, Start_Date: str, End_Date: str, End_Date_dt: datetime, Start_Time: str, End_Time: str, Duration: int, Project: str, Activity: str, Recurring: bool, Busy_Status: str, Location: str, All_Day_Event: bool) -> list[dict, int]:
    if (All_Day_Event == True) and (End_Time == "00:00"):
        End_Date_dt = End_Date_dt - timedelta(days=1)
        End_Date = End_Date_dt.strftime(Date_format)
        End_Time = "23:59"

        Events_downloaded = Add_to_Events_dict(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)
        Counter += 1
    
    else:
        Events_downloaded = Add_to_Events_dict(Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)
        Counter += 1
    return Events_downloaded, Counter

def Add_to_Events_dict(Events_downloaded: dict, Counter: int, Subject: str, Start_Date: str, End_Date: str, Start_Time: str, End_Time: str, Duration: int, Project: str, Activity: str, Recurring: bool, Busy_Status: str, Location: str, All_Day_Event: bool) -> dict: 
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
    return Events_downloaded