# Import Libraries
import json
from pandas import DataFrame as DataFrame
from datetime import datetime, timedelta
from tqdm import tqdm

import Libs.Download.Outlook_Client as Outlook_Client
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Sharepoint.Authentication as Authentication
import Libs.Sharepoint.Sharepoint as Sharepoint

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Date_format = Settings["General"]["Formats"]["Date"]
Time_format = Settings["General"]["Formats"]["Time"]
Personnel_number = Settings["General"]["Person"]["Code"]

BusyStatus_List = Defaults_Lists.Busy_Status_List()

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Download_Events() -> DataFrame:
    # Date Selection
    while True:
        Auto_download = input(f"\n Do you want to auto downlaod missing days from Sharepoit? [Y/N]?")
        Auto_download = Auto_download.upper()

        if Auto_download == "Y":
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Data_df_TQDM = tqdm(total=int(1),desc=f"{now}>> Getting Data from Sharepoint")

            # Authentication
            s_aut = Authentication.Authentication()

            # Download
            Downloaded = Sharepoint.Download_Excel(s_aut=s_aut)

            if Downloaded == True:
                # Start/End Date
                Utilization_Sheet = Sharepoint.Get_WorkSheet(Sheet_Name="Utilization")
                Input_Start_Date_dt = Utilization_Sheet["G2"].value
                Input_End_Date_dt = Utilization_Sheet["H2"].value

                # My last Date imported
                TimeSpent_Sheet = Sharepoint.Get_WorkSheet(Sheet_Name="TimeSpent")
                Table_list = Sharepoint.Get_Tables_on_Worksheet(Sheet=TimeSpent_Sheet)
                data_boundary = Table_list[0][1]
                data_boundary = data_boundary.replace("O", "J")
                TimeSheets_df = Sharepoint.Get_Table_Data(ws=TimeSpent_Sheet, data_boundary=data_boundary)

                mask1 = TimeSheets_df["Personnel number"] == Personnel_number
                mask2 = TimeSheets_df["Date"] != "=Utilization!$G$2"
                TimeSheets_df = TimeSheets_df[mask1 & mask2]

                # Dats updates --> to confirm correct dates selection
                Today = datetime.today()
                Today = Today.replace(hour=0, minute=0, second=0, microsecond=0)
                if Input_End_Date_dt > Today:
                    Input_End_Date_dt = Today
                else:
                    pass

                if TimeSheets_df.empty:
                    # Starepoint doesnt contain any my data
                    pass
                else:
                    My_Last_Day = max(TimeSheets_df["Date"])
                    My_Last_Day = My_Last_Day.split(" ")
                    My_Last_Day_dt = datetime.strptime(My_Last_Day[0], Date_format)

                    if My_Last_Day_dt >= Today:
                        pass
                    else:
                        Input_Start_Date_dt = My_Last_Day_dt + timedelta(days=1)

                print(f"Start Date: {Input_Start_Date_dt.strftime(Date_format)}")
                print(f"End Date: {Input_End_Date_dt.strftime(Date_format)}")

            else:
                #! Dodělat --> co udělat když se nepodaří stáhnout
                pass

            Data_df_TQDM.update(1) 
            Data_df_TQDM.close()

        elif Auto_download == "N":
            # Manually select dates
            print("\n Manually select dates:")
            Input_Start_Date = input("""Set the Start Date in format "YYYY-MM-DD"/"t": """)
            Input_End_Date = input("""Set the End Date in format "YYYY-MM-DD"/"t": """)

            # Prepare dates for download
            Input_Start_Date = Input_Start_Date.upper()
            Input_End_Date = Input_End_Date.upper()

            # Today shortcut
            if Input_Start_Date == "T":
                Input_Start_Date_dt = datetime.now()
                Input_Start_Date_dt = Input_Start_Date_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                Input_Start_Date_dt = datetime.strptime(Input_Start_Date, Date_format)

            if Input_End_Date == "T":
                Input_End_Date_dt = datetime.now()
                Input_End_Date_dt = Input_End_Date_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                Input_End_Date_dt = datetime.strptime(Input_End_Date, Date_format)
        else:
            continue
        

        try:
            # Check if Input_Start_Date <= Input_End_Date
            if Input_Start_Date_dt <= Input_End_Date_dt:
                pass
            else:
                print("Start Date is after End Date --> try again.")
                raise ValueError

            # add 1 day 
            Filter_Start_Date_dt = Input_Start_Date_dt - timedelta(days=1)
            Filter_End_Date_dt = Input_End_Date_dt + timedelta(days=1)
            Filter_Start_Date = Filter_Start_Date_dt.strftime(Date_format)
            Filter_End_Date = Filter_End_Date_dt.strftime(Date_format)
            break
        except:
            print("Something went wrong, try again.")
            pass

    # Engine selection
    Events_Process_df = Outlook_Client.Download_Events(Input_Start_Date_dt=Input_Start_Date_dt, Input_End_Date_dt=Input_End_Date_dt, Filter_Start_Date=Filter_Start_Date, Filter_End_Date=Filter_End_Date) 
    return Events_Process_df