# Import Libraries
from pandas import DataFrame as DataFrame
from datetime import datetime, timedelta

import Libs.Download.Exchange as Exchange
import Libs.Sharepoint.Authentication as Authentication
import Libs.Sharepoint.Sharepoint as Sharepoint
import Libs.GUI.Elements as Elements

import Libs.Defaults_Lists as Defaults_Lists
import Libs.File_Manipulation as File_Manipulation
import Libs.Pandas_Functions as Pandas_Functions
import Libs.Data_Functions as Data_Functions

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Settings: dict, Configuration: dict, Download_Date_Range_Source: str, Download_Data_Source: str, SP_Date_From_Method: str, SP_Date_To_Method: str, SP_Man_Date_To: str, SP_Password: str|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None) -> DataFrame:
    # Default
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]
    Sharepoint_Date_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Date"]
    Sharepoint_Date_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Date1"]
    Sharepoint_Date_Format2 = Settings["0"]["General"]["Formats"]["Sharepoint_Date2"]
    Sharepoint_Time_Format = Settings["0"]["General"]["Formats"]["Sharepoint_Time"]
    Sharepoint_Time_Format1 = Settings["0"]["General"]["Formats"]["Sharepoint_Time1"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    SP_Team_Current = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
    SP_Link_Current = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_Links"][f"{SP_Team_Current}"]

    Report_Period_Active_Days = None
    Report_Period_Start = None
    Report_Period_End = None
    Download_canceled = False

    Events = DataFrame()
    Events_Registered_df = DataFrame()  # Because of case when it is not downloaded from Sharepoint, but output must exists
    File_Manipulation.Delete_File(file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\Downloads\\Events_Registered.csv"))

    Today = datetime.today()
    Today = Today.replace(hour=0, minute=0, second=0, microsecond=0)

    # -------------- Sharepoint  -------------- #
    if Download_Date_Range_Source == "Sharepoint":
        # Authentication
        s_aut = Authentication.Authentication(Settings=Settings, Configuration=Configuration, SP_Password=SP_Password)

        # Download
        Downloaded = Sharepoint.Download_Excel(Settings=Settings, s_aut=s_aut, SP_Link=SP_Link_Current, Type="Current", Name=None)

        if Downloaded == True:
            # Report Period Information
            Utilization_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="Utilization", Type="Current", Name=None)
            Report_Period_Start = Utilization_Sheet["G2"].value
            Report_Period_End = Utilization_Sheet["H2"].value
            Report_Period_Active_Days = int(Utilization_Sheet["I2"].value)

            # My last Date imported 
            try:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpent", Type="Current", Name=None)
            except:
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Settings=Settings, Sheet_Name="TimeSpend", Type="Current", Name=None)
            Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
            data_boundary = Table_list[0][1]
            data_boundary = data_boundary.replace("O", "J")
            Events_Registered_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

            mask1 = Events_Registered_df["Personnel number"] == User_ID
            mask2 = Events_Registered_df["Activity description"] != "User included in TimeSpent"
            mask3 = Events_Registered_df["Date"] != "=Utilization!$G$2"
            Events_Registered_df = DataFrame(Events_Registered_df[mask1 & mask2 & mask3])

            # Dates/Time correct
            # Date
            try:
                Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="Date", Covert_Format=Sharepoint_Date_Format)
            except:
                try:
                    Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="Date", Covert_Format=Sharepoint_Date_Format1)
                except:
                    Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="Date", Covert_Format=Sharepoint_Date_Format2)
            Events_Registered_df["Date"] = Events_Registered_df["Date"].dt.strftime(Date_Format)

            # Time
            try:
                Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format)
                Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="End Time", Covert_Format=Sharepoint_Time_Format)
            except:
                Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="Start Time", Covert_Format=Sharepoint_Time_Format1)
                Events_Registered_df = Pandas_Functions.PD_Column_to_DateTime(PD_DataFrame=Events_Registered_df, Column="End Time", Covert_Format=Sharepoint_Time_Format1)
            Events_Registered_df["Start Time"] = Events_Registered_df["Start Time"].dt.strftime(Time_Format)
            Events_Registered_df["End Time"] = Events_Registered_df["End Time"].dt.strftime(Time_Format)
                
                
            if Events_Registered_df.empty:
                # Sharepoint doesn't contain any my data
                My_Last_Day_dt = Report_Period_Start 
            else:
                My_Last_Day = max(Events_Registered_df["Date"])
                My_Last_Day_dt = datetime.strptime(My_Last_Day, Date_Format)
                My_Last_Day_dt = My_Last_Day_dt + timedelta(days=1) # Need to add 1 day to set download day after my last reported day

                if My_Last_Day_dt >= Today:
                    # Skip whole automatic because it should not load anything
                    Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Last Day Reported is: {My_Last_Day_dt} --> cannot perform automatic Download. Use Manual.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    pass

            # Date-From Selection
            if SP_Date_From_Method == "Last Registered Date":
                Input_Start_Date_dt = My_Last_Day_dt
            elif SP_Date_From_Method == "First Report Day": 
                Input_Start_Date_dt = Report_Period_Start
                Events_Registered_df = DataFrame()
            else:
                Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Cannot define Start date as not know method selected. Method: {SP_Date_From_Method}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            # Date-To Selection
            if SP_Date_To_Method == "Today":
                Input_End_Date_dt = Today
            elif SP_Date_To_Method == "Manual":
                Input_End_Date_dt = datetime.strptime(SP_Man_Date_To, Date_Format)

                # Check if Manual date is smaller than Report End Date
                if Input_End_Date_dt > Report_Period_End:
                    Elements.Get_MessageBox(Configuration=Configuration, title="Question", message=f"Manual Date you entered {Input_End_Date_dt} is after Period End date {Report_Period_End}, will be automatically switched to Report End date. Do you agree?", icon="question",  option_1="Confirm", option_2="Reject", fade_in_duration=1, GUI_Level_ID=1)
                    if response == "Confirm":
                        Input_End_Date_dt = Report_Period_End
                    else:
                        Download_canceled = True
                        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Download process canceled by user.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

                # Check if manual is higher than Input_Start_Date_dt
                if Input_End_Date_dt >= Input_Start_Date_dt:
                    pass
                else:
                    Download_canceled = True
                    Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Download process canceled End date is before Start Date.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            elif SP_Date_To_Method == "Last Report Day":
                Input_End_Date_dt = Report_Period_End
            else:
                Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Cannot define End date as not know method selected. Method: {SP_Date_To_Method}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"It was not possible to automatically download the master data from Sharepoint, please select Start Date and End Date manually.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # Date check
        response = Elements.Get_MessageBox(Configuration=Configuration, title="Question", message=f"Dates range to download: \n Date From: {Input_Start_Date_dt.strftime(Date_Format)}\n Date To: {Input_End_Date_dt.strftime(Date_Format)}", icon="question", option_1="Confirm", option_2="Reject", fade_in_duration=1, GUI_Level_ID=1)
        if response == "Confirm":
            pass
        else:
            Download_canceled = True
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Download process canceled by user.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        
        Events_Registered_df.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\Downloads\\Events_Registered.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")

    # -------------- Manual  -------------- #
    elif Download_Date_Range_Source == "Manual":
        # Prepare dates for download
        Input_Start_Date = Input_Start_Date.upper()
        Input_End_Date = Input_End_Date.upper()

        Input_Start_Date_dt = datetime.strptime(Input_Start_Date, Date_Format)
        Input_End_Date_dt = datetime.strptime(Input_End_Date, Date_Format)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Date source: {Download_Date_Range_Source} is not compatible, should be Sharepoint or Manual. Try again.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    
    # -------------- Dates Checker  -------------- #
    try:
        # Check if Input_Start_Date <= Input_End_Date
        if Input_Start_Date_dt <= Input_End_Date_dt:
            pass
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Start Date is after End Date --> try again.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # add 1 day 
        Filter_Start_Date_dt = Input_Start_Date_dt - timedelta(days=1)
        Filter_End_Date_dt = Input_End_Date_dt + timedelta(days=1)
        Filter_Start_Date = Filter_Start_Date_dt.strftime(Date_Format)
        Filter_End_Date = Filter_End_Date_dt.strftime(Date_Format)
    except:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Something went wrong, try again.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    # Engine selection
    if Download_canceled == False:
        if Download_Data_Source == "Exchange":
            Events = Exchange.Download_Events(Settings=Settings, Configuration=Configuration, Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Filter_Start_Date=Filter_Start_Date, Filter_End_Date=Filter_End_Date, Exchange_Password=Exchange_Password) 
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Download source is not supported (Outlook_Client, API_Exchange_server), current is {Download_Data_Source}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass
    
    return Events, Events_Registered_df, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Download_canceled