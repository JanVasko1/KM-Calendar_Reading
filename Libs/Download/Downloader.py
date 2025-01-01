# Import Libraries
from pandas import DataFrame as DataFrame
from datetime import datetime, timedelta

import Libs.Download.Outlook_Client as Outlook_Client
import Libs.Download.Exchange as Exchange
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Sharepoint.Authentication as Authentication
import Libs.Sharepoint.Sharepoint as Sharepoint

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]
Personnel_number = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]

BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events(Download_Date_Range_Source: str, Download_Data_Source: str, SP_Password: str|None, SP_Whole_Period: bool|None, SP_End_Date_Max_Today_Var: bool|None, Exchange_Password: str|None, Input_Start_Date: str|None, Input_End_Date: str|None) -> DataFrame:
    # Default
    Report_Period_Active_Days = None
    Report_Period_Start = None
    Report_Period_End = None
    Download_canceled = False
    Events = DataFrame()

    # Date Selection
    while True:
        if Download_Date_Range_Source == "Sharepoint":
            # Authentication
            s_aut = Authentication.Authentication(SP_Password=SP_Password)

            # Download
            Downloaded = Sharepoint.Download_Excel(s_aut=s_aut)

            if Downloaded == True:
                # Start/End Date
                Utilization_Sheet = Sharepoint.Get_WorkSheet(Sheet_Name="Utilization")
                Report_Period_Start = Utilization_Sheet["G2"].value
                Report_Period_End = Utilization_Sheet["H2"].value
                Report_Period_Active_Days = int(Utilization_Sheet["I2"].value)

                Input_Start_Date_dt = Report_Period_Start
                Input_End_Date_dt = Report_Period_End
                
                Today = datetime.today()
                Today = Today.replace(hour=0, minute=0, second=0, microsecond=0)

                # Downlaod whole Reporting Period
                if SP_Whole_Period == False:
                    # My last Date imported 
                    TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Sheet_Name="TimeSpent")
                    Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
                    data_boundary = Table_list[0][1]
                    data_boundary = data_boundary.replace("O", "J")
                    TimeSheets_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

                    mask1 = TimeSheets_df["Personnel number"] == Personnel_number
                    mask2 = TimeSheets_df["Date"] != "=Utilization!$G$2"
                    TimeSheets_df = TimeSheets_df[mask1 & mask2]
                    
                    if TimeSheets_df.empty:
                        # Starepoint doesnt contain any my data
                        pass
                    else:
                        My_Last_Day = max(TimeSheets_df["Date"])
                        My_Last_Day = My_Last_Day.split(" ")
                        My_Last_Day_dt = datetime.strptime(My_Last_Day[0], Date_format)

                        # Get also Reporting Period Days
                        if My_Last_Day_dt >= Today:
                            # Skip whole automatic because it should not load anything
                            CTkMessagebox(title="Error", message=f"Last Day Reported is: {My_Last_Day_dt} --> cannot perform automatic Download. Use Manual.", icon="cancel", fade_in_duration=1)
                            raise ValueError
                        else:
                            Input_Start_Date_dt = My_Last_Day_dt + timedelta(days=1)
                elif SP_Whole_Period == True:
                    pass

                # End date maximal today
                if SP_End_Date_Max_Today_Var == True:
                    # Dates updates --> to confirm correct dates selection
                    if Input_End_Date_dt > Today:
                        Input_End_Date_dt = Today
                    else:
                        pass
                else:
                    pass
            else:
                CTkMessagebox(title="Error", message="It was not possible to automatically dowload the master data from Sharepoint, please select Start Date and End Date manually.", icon="cancel", fade_in_duration=1)
                raise ValueError

            # Date check
            Question_Message = CTkMessagebox(title="Information", message=f"Dates range to download: \n Date From: {Input_Start_Date_dt.strftime(Date_format)}\n Date To: {Input_End_Date_dt.strftime(Date_format)}", icon="question", fade_in_duration=1, option_1="Confirm", option_2="Reject")
            response = Question_Message.get()
            if response == "Confirm":
                pass
            else:
                Download_canceled = True
                CTkMessagebox(title="Error", message="Download process canceled by user.", icon="cancel", fade_in_duration=1)

        elif Download_Date_Range_Source == "Manual":
            # Prepare dates for download
            Input_Start_Date = Input_Start_Date.upper()
            Input_End_Date = Input_End_Date.upper()

            Input_Start_Date_dt = datetime.strptime(Input_Start_Date, Date_format)
            Input_End_Date_dt = datetime.strptime(Input_End_Date, Date_format)
        else:
            CTkMessagebox(title="Error", message=f"Date source: {Download_Date_Range_Source} is not compatible, should be Sharepoint or Manual. Try again.", icon="cancel", fade_in_duration=1)
            raise ValueError
        
        try:
            # Check if Input_Start_Date <= Input_End_Date
            if Input_Start_Date_dt <= Input_End_Date_dt:
                pass
            else:
                CTkMessagebox(title="Error", message="Start Date is after End Date --> try again.", icon="cancel", fade_in_duration=1)
                raise ValueError

            # add 1 day 
            Filter_Start_Date_dt = Input_Start_Date_dt - timedelta(days=1)
            Filter_End_Date_dt = Input_End_Date_dt + timedelta(days=1)
            Filter_Start_Date = Filter_Start_Date_dt.strftime(Date_format)
            Filter_End_Date = Filter_End_Date_dt.strftime(Date_format)
            break
        except:
            CTkMessagebox(title="Error", message="Something went wrong, try again.", icon="cancel", fade_in_duration=1)
            raise ValueError

    # Engine selection
    if Download_canceled == False:
        if Download_Data_Source == "Outlook_Client":
            Events = Outlook_Client.Download_Events(Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Filter_Start_Date=Filter_Start_Date, Filter_End_Date=Filter_End_Date) 
        elif Download_Data_Source == "Exchange":
            Events = Exchange.Download_Events(Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Filter_Start_Date=Filter_Start_Date, Filter_End_Date=Filter_End_Date, Exchange_Password=Exchange_Password) 
        else:
            CTkMessagebox(title="Error", message=f"Download source is not supported (Outlook_clasic, API_Exchange_server), current is {Download_Data_Source}", icon="cancel", fade_in_duration=1)
            raise ValueError
    else:
        pass
    
    return Events, Report_Period_Active_Days, Report_Period_Start, Report_Period_End, Input_Start_Date_dt, Input_End_Date_dt, Download_canceled