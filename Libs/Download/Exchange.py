# Import Libraries
from pandas import DataFrame as DataFrame
import requests
from datetime import datetime

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements as Elements
import Libs.Download.Downloader_Helpers as Downloader_Helpers

from customtkinter import CTk

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Exchange_Busy_Status_List = Defaults_Lists.Exchange_Busy_Status_List()
Busy_Status_List = Defaults_Lists.Busy_Status_List()

# Load OAuth2 info
Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Duration_Counter(Time1: datetime, Time2: datetime) -> int:
    # Count duration between 2 datetime in minuets
    Duration_dt = Time2 - Time1
    Duration = int(Duration_dt.total_seconds() // 60)
    return Duration

def Add_Events_downloaded(Settings: dict, Events_downloaded: dict, Events: dict, Counter: int) -> None:
    Exchange_DateTime_format = Settings["0"]["General"]["Formats"]["Exchange_DateTime"]
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Time_format = Settings["0"]["General"]["Formats"]["Time"]


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
        Project = Downloader_Helpers.Project_handler(Settings=Settings, Project=Project)

        # Activity --> in the Body as predefined text
        Activity = Downloader_Helpers.Activity_handler(Settings=Settings, Body=Body)

        # Location --> Get only Meeting Room
        Location = Downloader_Helpers.Location_handler(Settings=Settings, Location=Location)

        # Update End_Date for all Day Event and split them to every day event
        Events_downloaded, Counter = Downloader_Helpers.All_Day_Event_End_Handler(Settings=Settings, Events_downloaded=Events_downloaded, Counter=Counter, Subject=Subject, Start_Date=Start_Date, End_Date=End_Date, End_Date_dt=End_Date_dt, Start_Time=Start_Time, End_Time=End_Time, Duration=Duration, Project=Project, Activity=Activity, Recurring=Recurring, Busy_Status=Busy_Status, Location=Location, All_Day_Event=All_Day_Event)

    return Counter

def Exchange_OAuth(Settings: dict, Configuration: dict, window: CTk|None, Exchange_Password: str) -> str:
    User_Email = Settings["0"]["General"]["User"]["Email"]

    if not client_id:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No client_id found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    if not client_secret:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No client_secret found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    if not tenant_id:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No tenant_id found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    # OAuth2 authentication at KM Azure
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "username": User_Email,
        "password": Exchange_Password}
    response = requests.post(url=url, data=payload)
    tokens = response.json()
    access_token = tokens["access_token"]

    return access_token

def Exchange_OAuth_Test() -> str:
    try:
        # OAuth2 authentication at KM Azure
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"}
        response = requests.post(url=url, data=payload)
        if (response.status_code >= 200) and (response.status_code < 300):
            return True
        else:
            return False
    except:
        return False

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Settings: dict, Configuration: dict, window: CTk|None, Input_Start_Date_dt: datetime, Input_End_Date_dt: datetime, Filter_Start_Date: str, Filter_End_Date: str, Exchange_Password: str) -> DataFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]

    # OAuth2 Access
    access_token = Exchange_OAuth(Settings=Settings, Configuration=Configuration, window=window, Exchange_Password=Exchange_Password)

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
    events_url = f"https://graph.microsoft.com/v1.0/users/{User_Email}/calendar/calendarView"
    events_response = requests.get(url=events_url, headers=headers, params=params)

    Counter = 0 
    if events_response.status_code == 200:
        # Init page 
        Events = events_response.json()
        Counter = Add_Events_downloaded(Settings=Settings, Events_downloaded=Events_downloaded, Events=Events, Counter=Counter) 

        # Check if there are more pages of results 
        while '@odata.nextLink' in Events:
            next_link = Events['@odata.nextLink']
            response = requests.get(next_link, headers=headers) 
            if response.status_code == 200: 
                Events = response.json()
                Counter = Add_Events_downloaded(Settings=Settings, Events_downloaded=Events_downloaded, Events=Events, Counter=Counter)       
    elif events_response.status_code == 503:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Not possible to download from Exchange (Response Code: {events_response.status_code}), Exchange is temporary unavailable, try few moments later.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Events_downloaded = {}
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Not possible to download from Exchange (Response Code: {events_response.status_code}), will try to download from Outlook Classic Client.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Events_downloaded = {}

    # Crop edge dates as they were added in previous step
    Events_Process = Downloader_Helpers.Crop_edge_days_Events(Settings=Settings, Events_downloaded=Events_downloaded, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt)
    Events_Process_df = DataFrame(data=Events_Process, columns=list(Events_Process.keys()))
    Events_Process_df = Events_Process_df.T
    return Events_Process_df

def Get_All_Projects(access_token: str, username: str) -> dict:
    headers_get = {
        "Authorization": f"Bearer {access_token}"}
    
    # Get all categories
    Cat_list_url = f"https://graph.microsoft.com/v1.0/users/{username}/outlook/masterCategories"
    All_Cat_response = requests.get(url=Cat_list_url, headers=headers_get)

    if All_Cat_response.status_code == 200 or All_Cat_response.status_code == 201:
        Exchange_Categories = All_Cat_response.json().get("value", {})
        Exchange_Categories_dict = {index: value for index, value in enumerate(Exchange_Categories)}
        return Exchange_Categories_dict, True
    else:
        return {}, False

def Create_Project(access_token: str, username: str, Preset_Active_color: str, project: str) -> bool:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"}
    
    body = {
        "color": f"{Preset_Active_color}",
        "displayName": f"{project}"}
    
    category_url = f"https://graph.microsoft.com/v1.0/users/{username}/outlook/masterCategories"
    category_response = requests.post(url=category_url, headers=headers, json=body)

    if category_response.status_code == 200 or category_response.status_code == 201:
        return True
    else:
        return False

def Delete_Projects(access_token: str, username: str, category_id: str) -> bool:
    headers_del = {
        "Authorization": f"Bearer {access_token}"}

    delete_url = f"https://graph.microsoft.com/v1.0/users/{username}/outlook/masterCategories/{category_id}"
    delete_response = requests.delete(url=delete_url, headers=headers_del)

    if delete_response.status_code == 200 or delete_response.status_code == 201:
        return True
    else:
        return False

def Change_Project_Color(access_token: str, username: str, category_id: str, Color: str) -> bool:
    headers_update = {
        "Authorization": f"Bearer {access_token}"}
    
    body = {
        "color": f"{Color}"}

    update_url = f"https://graph.microsoft.com/v1.0/users/{username}/outlook/masterCategories/{category_id}"
    update_response = requests.delete(url=update_url, headers=headers_update, json=body)

    if update_response.status_code == 200 or update_response.status_code == 201:
        return True
    else:
        return False

def Push_Project(Settings: dict, Configuration: dict, window: CTk|None, Exchange_Password: str) -> None:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    access_token = Exchange_OAuth(Settings=Settings, Configuration=Configuration, window=window, Exchange_Password=Exchange_Password)

    # Get list of Projects
    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")

    # Preset Color
    Category_Active_Color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Active_Color"]
    Category_Non_Active_Color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Non_Active_Color"]
    Preset_Active_color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Color_preset_map"][f"{Category_Active_Color}"]
    Preset_Non_Active_color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Color_preset_map"][f"{Category_Non_Active_Color}"]

    # Exchange Categories --> Projects
    Exchange_Categories_dict, Can_Continue = Get_All_Projects(access_token=access_token, username=User_Email)
    Exchange_Categories_Names_list = Defaults_Lists.List_from_Dict(Exchange_Categories_dict, Key_Argument="displayName")

    if Can_Continue == True:
        # Check missing in Exchange
        Exchange_Missing_list = Defaults_Lists.List_missing_values(Source_list=Exchange_Categories_Names_list, Compare_list=Project_List)
        for project in Exchange_Missing_list:
            Created_Flag = Create_Project(access_token=access_token, username=User_Email, Preset_Active_color=Preset_Active_color, project=project)
            if Created_Flag == True:
                pass
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"""It was not possible to crate "{project}" as Category on Exchange, please create it manually.""", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # Check for surplus in Exchange
        Exchange_Surplus_list = Defaults_Lists.List_missing_values(Source_list=Project_List, Compare_list=Exchange_Categories_Names_list)
        if len(Exchange_Surplus_list) > 0:
            for project in Exchange_Surplus_list:
                # Find Category ID
                for key, value in Exchange_Categories_dict.items():
                    if value["displayName"] == project:
                        category_id = value["id"]
                        # Date check
                        response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"This step will delete project from Exchange Categories which will also delete it from all of your Events where it was used?\n\n Project: {project}", icon="question", fade_in_duration=1, GUI_Level_ID=1, option_1="Delete", option_2="Keep", option_3="Change color")
                        if response == "Delete":
                            Deleted_Flag = Delete_Projects(access_token=access_token, username=User_Email, category_id=category_id)
                            if Deleted_Flag == True:
                                pass
                            else:
                                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"""It was not possible to delete "{project}" from Category on Exchange, please delete it manually.""", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                        elif response == "Change color":
                            Update_Flag = Change_Project_Color(access_token=access_token, username=User_Email, category_id=category_id, Color=Preset_Non_Active_color)
                            if Update_Flag == True:
                                pass
                            else:
                                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"""It was not possible to change color for "{project}" from Category on Exchange, please update it manually.""", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                        elif response == "Keep":
                            break
                        else:
                            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Delete Categories on Exchange stopped by user.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    else:
                        pass
        else:
            pass         
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="No client_id found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Push_Activity(Settings: dict, Configuration: dict, window: CTk|None, Exchange_Password: str) -> None:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    access_token = Exchange_OAuth(Settings=Settings, Configuration=Configuration, window=window, Exchange_Password=Exchange_Password)

    # Get list of Projects
    Activity_List = Settings["0"]["Event_Handler"]["Activity"]["Activity_List"]

    # TODO --> Push_Activity
    pass