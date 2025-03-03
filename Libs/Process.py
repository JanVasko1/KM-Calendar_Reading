# Import Libraries
from pandas import DataFrame, concat, read_csv

import Libs.Download.Downloader as Downloader
import Libs.Sharepoint.Authentication as Authentication
import Libs.Sharepoint.Sharepoint as Sharepoint
import Libs.GUI.Elements as Elements

import Libs.Event_Handler.Fill_Empty_Place as Fill_Empty_Place
import Libs.Event_Handler.Divide_Events as Divide_Events
import Libs.Event_Handler.Location_Set as Location_Set
import Libs.Event_Handler.Skip_Events as Skip_Events
import Libs.Event_Handler.Parallel_Events as Parallel_Events
import Libs.Event_Handler.AutoFiller as AutoFiller
import Libs.Event_Handler.Special_Events as Special_Events
import Libs.Event_Handler.Join_Events as Join_Events
import Libs.Summary as Summary

import Libs.Pandas_Functions as Pandas_Functions
import Libs.Data_Functions as Data_Functions
import Libs.File_Manipulation as File_Manipulation
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTkProgressBar, CTk, CTkLabel

# ---------------------------------------------------------- Local Function ---------------------------------------------------------- #
def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Label: str) -> None:
    Progress_Bar.step()
    Progress_text.configure(text="                                                        ")
    window.update_idletasks()
    Progress_text.configure(text=f"{Label}")
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Label: str, value: int) -> None:
    Progress_Bar.set(value=value)
    Progress_text.configure(text="                                                        ")
    window.update_idletasks()
    Progress_text.configure(text=f"{Label}")
    window.update_idletasks()

def Events_Summary_Save(Settings: dict, Events_df: DataFrame, Events_Registered_df: DataFrame) -> DataFrame:
    Sharepoint_Time_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Time"]
    Sharepoint_Time_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Time1"]
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]
    User_ID = Settings["0"]["General"]["User"]["Code"]

    # Delete File before generation
    File_Manipulation.Delete_File(file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\Downloads\\Events.csv"))

    # Calculation
    Events_df["Personnel number"] = User_ID
    Events_df.drop(labels=["End_Date", "Recurring", "Meeting_Room", "All_Day_Event", "Event_Empty_Insert", "Within_Working_Hours", "Duration", "Busy_Status"], axis=1, inplace=True)
    Events_df.rename(columns={"Start_Date": "Date", "Project": "Network Description", "Subject": "Activity description", "Start_Time": "Start Time", "End_Time": "End Time", "": ""}, inplace=True)
    Events_df = Events_df[["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]]
    # Time
    try:
        Events_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format)
        Events_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_df, Column="End Time", Covert_Format=Sharepoint_Time_Format)
    except:
        Events_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format1)
        Events_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_df, Column="End Time", Covert_Format=Sharepoint_Time_Format1)
    Events_df["Start Time"] = Events_df["Start Time"].dt.strftime(Time_Format)
    Events_df["End Time"] = Events_df["End Time"].dt.strftime(Time_Format)

    # Save only new values --> what is registered should not be available as new data
    Events_df.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\Downloads\\Events.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")

    # Cumulate with Event Registered
    Cumulated_Events = concat(objs=[Events_df, Events_Registered_df], axis=0)
    Cumulated_Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Cumulated_Events, Columns_list=["Date", "Start Time"], Accenting_list=[True, True]) 

    return Cumulated_Events


# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Download_and_Process(Settings: dict, Configuration: dict, window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: str, Download_Data_Source: str, SP_Date_From_Method: str, SP_Date_To_Method: str, SP_Man_Date_To: str, SP_Password: str|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None) -> None:
    Progress_Bar.configure(determinate_speed = round(number=50 / 17, ndigits=3))
    
    # ----------------------- Download Events ----------------------- #
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    Events, Events_Registered_df, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Download_canceled = Downloader.Download_Events(Settings=Settings, Configuration=Configuration, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Date_From_Method=SP_Date_From_Method, SP_Date_To_Method=SP_Date_To_Method, SP_Man_Date_To=SP_Man_Date_To, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    
    if Download_canceled == False:
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # ----------------------- Process Events ----------------------- #
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Overnight Events") 
        Events = Divide_Events.OverMidnight_Events(Settings=Settings, Configuration=Configuration, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Skip Events") 
        Events = Skip_Events.Skip_Events(Settings=Settings, Events=Events, Type="Regular")
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty") 
        Events = Fill_Empty_Place.Fill_Events(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Too long Empty Events") 
        Events = Divide_Events.Empty_Split_Events(Settings=Settings, Configuration=Configuration, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty Coverage") 
        Events = Fill_Empty_Place.Fill_Events_Coverage(Settings=Settings, Configuration=Configuration, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True])

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Location set") 
        Events = Location_Set.Location_Set(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Lunch") 
        Events = Special_Events.Lunch(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Private") 
        Events = Special_Events.Private(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Skip Events") 
        Events = Skip_Events.Skip_Events(Settings=Settings, Events=Events, Type="Special")
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Parallel Events") 
        Events = Parallel_Events.Parallel_Events(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="AutoFilling") 
        Events = AutoFiller.AutoFiller(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Auto Activity Corrections") 
        Events = AutoFiller.Auto_Activity_Corrections(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Vacation") 
        Events = Special_Events.Vacation(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Sick Day") 
        Events = Special_Events.SickDay(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="HomeOffice") 
        Events = Special_Events.HomeOffice(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Joining Events") 
        Events = Join_Events.Join_Events(Settings=Settings, Events=Events)
        Events = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Cumulated_Events = Events_Summary_Save(Settings=Settings, Events_df=Events, Events_Registered_df=Events_Registered_df)

        # ----------------------- Summary Dataframe ----------------------- #
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
        Summary.Generate_Summary(Settings=Settings, Configuration=Configuration, Calculation_source="Current", Events=Cumulated_Events,  Report_Period_Active_Days=Report_Period_Active_Days, Report_Period_Start=Report_Period_Start, Report_Period_End=Report_Period_End, Team_Member_ID=None)

        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Done", value=1) 
        Elements.Get_MessageBox(Configuration=Configuration, title="Success", message=f"Successfully downloaded and processed new data.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Canceled", value=0) 

def Pre_Periods_Download_and_Process(Settings: dict, Configuration: dict, window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, SP_Password: str, Download_Periods: list) -> None:
    User_ID = Settings["0"]["General"]["User"]["Code"]
    SP_Team = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
    SP_Link_History = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["History_Links"][f"{SP_Team}"]
    Sharepoint_Date_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Date"]
    Sharepoint_Date_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Date1"]
    Sharepoint_Date_Format2 = Settings["0"]["General"]["Formats"]["Sharepoint_Date2"]
    Sharepoint_Time_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Time"]
    Sharepoint_Time_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Time1"]
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]

    Events_History_df = DataFrame()

    # Delete previous files 
    File_Manipulation.Delete_All_Files(file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\History\\"), include_hidden=True)

    # Progress bar
    Download_Periods_Count = len(Download_Periods)
    Progress_Bar.configure(determinate_speed = round(number=50 / (Download_Periods_Count), ndigits=3))      # Counts only with downloads as Summary set it to 1

    # ----------------------- Download Events ----------------------- #
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    s_aut = Authentication.Authentication(Settings=Settings, Configuration=Configuration, SP_Password=SP_Password)
    for period in Download_Periods:
        History_Year = str(period[0])
        History_month = f"0{period[1]}" if period[1] < 10 else str(period[1])
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label=f"Download: {History_Year} - {History_month}") 
        
        # Download
        SP_Link_Updated = SP_Link_History.replace("____", History_Year)
        SP_Link_Updated = SP_Link_Updated.replace("__", History_month)

        History_Name = f"{History_Year}_{History_month}"
        Downloaded = Sharepoint.Download_Excel(Settings=Settings, s_aut=s_aut, SP_Link=SP_Link_Updated, Type="History", Name=History_Name)

        if Downloaded == True:
            try:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpent", Type="History", Name=History_Name)
            except:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpend", Type="History", Name=History_Name)
            Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
            data_boundary = Table_list[0][1]
            data_boundary = data_boundary.replace("O", "J")
            Events_Month_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

            mask1 = Events_Month_df["Personnel number"] == User_ID
            mask2 = Events_Month_df["Activity description"] != "User included in TimeSpent"
            Events_Month_df = Events_Month_df[mask1 & mask2]
            Events_History_df = concat(objs=[Events_History_df, Events_Month_df], axis=0)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Cannot download history period {History_Year}-{History_month} from Sharepoint.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    
    # Dates/Time correct
    # Date
    try:
        Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="Date", Covert_Format=Sharepoint_Date_Format)
    except:
        try:
            Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="Date", Covert_Format=Sharepoint_Date_Format1)
        except:
            Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="Date", Covert_Format=Sharepoint_Date_Format2)
    Events_History_df["Date"] = Events_History_df["Date"].dt.strftime(Date_Format)

    # Time
    try:
        Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format)
        Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="End Time", Covert_Format=Sharepoint_Time_Format)
    except:
        Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format1)
        Events_History_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_History_df, Column="End Time", Covert_Format=Sharepoint_Time_Format1)
    Events_History_df["Start Time"] = Events_History_df["Start Time"].dt.strftime(Time_Format)
    Events_History_df["End Time"] = Events_History_df["End Time"].dt.strftime(Time_Format)

    # Save
    Events_History_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events_History_df, Columns_list=["Date", "Start Time"], Accenting_list=[True, True]) 
    Events_History_df.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\History\\Events.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")

    # ----------------------- Summary Dataframe ----------------------- #
    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
    Summary.Generate_Summary(Settings=Settings, Configuration=Configuration, Calculation_source="History", Events=Events_History_df, Report_Period_Active_Days=None, Report_Period_Start=None, Report_Period_End=None, Team_Member_ID=None)
    Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Successfully downloaded and processed your history.", icon="check", fade_in_duration=1, GUI_Level_ID=1)


def My_Team_Download_and_Process(Settings: dict, Configuration: dict, window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, SP_Password: str) -> None:
    Managed_Team = Settings["0"]["General"]["User"]["Managed_Team"]
    Link_History_dict = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_Links"]
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]
    Sharepoint_Date_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Date"]
    Sharepoint_Date_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Date1"]
    Sharepoint_Date_Format2 = Settings["0"]["General"]["Formats"]["Sharepoint_Date2"]
    Sharepoint_Time_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Time"]
    Sharepoint_Time_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Time1"]

    # Team List and members
    Teams_list = Defaults_Lists.List_from_Dict(Dictionary=Managed_Team, Key_Argument="User Team")
    Teams_list = list(set(Teams_list))
    Teams_list_Count = len(Teams_list)
    Team_Members_Count = len(Managed_Team)

    # Progress bar
    Progress_Bar.configure(determinate_speed = round(number=50 / (Teams_list_Count + Team_Members_Count), ndigits=3))      # Counts only with downloads as Summary set it to 1

    # ----------------------- Download Events ----------------------- #
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    s_aut = Authentication.Authentication(Settings=Settings, Configuration=Configuration, SP_Password=SP_Password)

    # Downloader of Time Sheet of each team
    for team in Teams_list:
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label=f"Downloading: {team}") 
        SP_Link_team = Link_History_dict[team]

        Downloaded = Sharepoint.Download_Excel(Settings=Settings, s_aut=s_aut, SP_Link=SP_Link_team, Type="Team", Name=team)

        if Downloaded == True:
            try:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpent", Type="Team", Name=team)
            except:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpend", Type="Team", Name=team)
            Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
            data_boundary = Table_list[0][1]
            data_boundary = data_boundary.replace("O", "J")
            Events_Member_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

            mask1 = Events_Member_df["Activity description"] != "User included in TimeSpent"
            mask2 = Events_Member_df["Personnel number"] != "None"
            Events_Member_df = Events_Member_df[mask1 & mask2]
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Not possible to download TimeSheets from Sharepoint for {team}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # Dates/Time correct
        # Date
        try:
            Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="Date", Covert_Format=Sharepoint_Date_Format)
        except:
            try:
                Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="Date", Covert_Format=Sharepoint_Date_Format1)
            except:
                Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="Date", Covert_Format=Sharepoint_Date_Format2)
        Events_Member_df["Date"] = Events_Member_df["Date"].dt.strftime(Date_Format)

        # Time
        try:
            Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format)
            Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="End Time", Covert_Format=Sharepoint_Time_Format)
        except:
            Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format1)
            Events_Member_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Member_df, Column="End Time", Covert_Format=Sharepoint_Time_Format1)
        Events_Member_df["Start Time"] = Events_Member_df["Start Time"].dt.strftime(Time_Format)
        Events_Member_df["End Time"] = Events_Member_df["End Time"].dt.strftime(Time_Format)

        # Save
        Events_Member_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Events_Member_df, Columns_list=["Date", "Start Time"], Accenting_list=[True, True]) 
        Events_Member_df.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team\\{team}.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")

    # Process each team member on its own TimeSheets
    for key, value in Managed_Team.items():
        Team_Member_team = value["User Team"]
        Team_Member_ID = value["User ID"]
        Team_Member_name = value["User Name"]

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label=f"Processing: {Team_Member_name}") 

        Member_df = read_csv(filepath_or_buffer=Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team\\{Team_Member_team}.csv"), sep=";", header=0)
        mask1 = Member_df["Personnel number"] == Team_Member_ID
        mask2 = Member_df["Activity description"] != "User included in TimeSpent"
        Member_df = Member_df[mask1 & mask2]

        # ----------------------- Summary Dataframe ----------------------- #
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
        Summary.Generate_Summary(Settings=Settings, Configuration=Configuration, Calculation_source="Team", Events=Member_df, Report_Period_Active_Days=None, Report_Period_Start=None, Report_Period_End=None, Team_Member_ID=Team_Member_ID)
        Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Successfully downloaded and processed all team members.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        