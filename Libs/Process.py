# Import Libraries
import Libs.Download.Downloader as Downloader
import Libs.Sharepoint.Authentication as Authentication
import Libs.Sharepoint.Sharepoint as Sharepoint

import Libs.Event_Handler.Fill_Empty_Place as Fill_Empty_Place
import Libs.Event_Handler.Divide_Events as Divide_Events
import Libs.Event_Handler.Location_Set as Location_Set
import Libs.Event_Handler.Skip_Events as Skip_Events
import Libs.Event_Handler.Parallel_Events as Parallel_Events
import Libs.Event_Handler.AutoFiller as AutoFiller
import Libs.Event_Handler.Special_Events as Special_Events
import Libs.Event_Handler.Join_Events as Join_Events
import Libs.Summary as Summary
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTkProgressBar, CTk, CTkLabel
from CTkMessagebox import CTkMessagebox

import pandas

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Time_format = Settings["General"]["Formats"]["Time"]
Personnel_number = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]

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

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Download_and_Process(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: str, Download_Data_Source: str, SP_Date_From_Method: str, SP_Date_To_Method: str, SP_Man_Date_To: str, SP_Password: str|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None) -> None:
    Progress_Bar.configure(determinate_speed = round(number=50 / 17, ndigits=3))
    
    # Download Events 
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    Events, Events_Registered_df, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Download_canceled = Downloader.Download_Events(Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Date_From_Method=SP_Date_From_Method, SP_Date_To_Method=SP_Date_To_Method, SP_Man_Date_To=SP_Man_Date_To, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    
    if Download_canceled == False:
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Process Events
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Overnight Events") 
        Events = Divide_Events.OverMidnight_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Skip Events") 
        Events = Skip_Events.Skip_Events(Events=Events, Type="Regular")
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty") 
        Events = Fill_Empty_Place.Fill_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Too long Empty Events") 
        Events = Divide_Events.Empty_Split_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Fill Empty Coverage") 
        Events = Fill_Empty_Place.Fill_Events_Coverage(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True])

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Location set") 
        Events = Location_Set.Location_Set(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Lunch") 
        Events = Special_Events.Lunch(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Private") 
        Events = Special_Events.Private(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Skip Events") 
        Events = Skip_Events.Skip_Events(Events=Events, Type="Special")
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Parallel Events") 
        Events = Parallel_Events.Parallel_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="AutoFilling") 
        Events = AutoFiller.AutoFiller(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Auto Activity Corrections") 
        Events = AutoFiller.Auto_Activity_Corrections(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Vacation") 
        Events = Special_Events.Vacation(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Sick Day") 
        Events = Special_Events.SickDay(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="HomeOffice") 
        Events = Special_Events.HomeOffice(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Joining Events") 
        Events = Join_Events.Join_Events(Events=Events)
        Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Start_Date", "Start_Time"], Accenting_list=[True, True]) 

        # Summary Dataframe
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
        Events = Summary.Generate_Summary(Events=Events, Events_Registered_df=Events_Registered_df, Report_Period_Active_Days=Report_Period_Active_Days, Report_Period_Start=Report_Period_Start, Report_Period_End=Report_Period_End)

        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Done", value=1) 
        CTkMessagebox(title="Success", message="Successfully downloaded and processed.", icon="check", option_1="Thanks", fade_in_duration=1)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Canceled", value=0) 



def Pre_Periods_Download_and_Process(window: CTk, Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, SP_Password: str, Download_Periods: list) -> None:
    Events = pandas.DataFrame()
    Events_Registered_df = pandas.DataFrame()
    SP_Team = Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
    SP_Link_History = Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["History_Links"][f"{SP_Team}"]

    # Progress bar
    Download_Periods_Count = len(Download_Periods)
    Progress_Bar.configure(determinate_speed = round(number=50 / (Download_Periods_Count), ndigits=3))      # Counts only with downloads as Summary set it to 1

    # Download Events 
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Downloading", value=0) 
    s_aut = Authentication.Authentication(SP_Password=SP_Password)
    for period in Download_Periods:
        History_Year = str(period[0])
        History_month = f"0{period[1]}" if period[1] < 10 else str(period[1])
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label=f"Download: {History_Year} - {History_month}") 
        
        # Download
        SP_Link_Updated = SP_Link_History.replace("____", History_Year)
        SP_Link_Updated = SP_Link_Updated.replace("__", History_month)

        SP_History_Name = f"SP_{History_Year}_{History_month}"

        Downloaded = Sharepoint.Download_Excel(s_aut=s_aut, SP_Link=SP_Link_Updated, Type="SP_History", Name=SP_History_Name)

        if Downloaded == True:
            TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Sheet_Name="TimeSpent", Type="SP_History", Name=SP_History_Name)
            Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
            data_boundary = Table_list[0][1]
            data_boundary = data_boundary.replace("O", "J")
            Events_Registered_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

            mask1 = Events_Registered_df["Personnel number"] == Personnel_number
            mask2 = Events_Registered_df["Activity description"] != "User included in TimeSpent"

            Events_Registered_df = Events_Registered_df[mask1 & mask2]

            Events_Registered_df = pandas.concat(objs=[Events_Registered_df, Events_Registered_df], axis=0)
        else:
            CTkMessagebox(title="Error", message=f"Cannot download history period {History_Year}-{History_month} from Sharepoint.", icon="cancel", fade_in_duration=1)

    print(Events_Registered_df)
    Events_Registered_df = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events_Registered_df, Columns_list=["Date", "Start Time"], Accenting_list=[True, True]) 

    # Summary Dataframe
    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Label="Summary") 
    Events = Summary.Generate_Summary(Events=Events, Events_Registered_df=Events_Registered_df, Report_Period_Active_Days=None, Report_Period_Start=None, Report_Period_End=None)
