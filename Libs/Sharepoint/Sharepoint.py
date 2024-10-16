#into je tu: D:\Time_Sheet_App
import Libs.Sharepoint.Authentication as Authentication
from openpyxl import load_workbook
from pandas import DataFrame
import pandas
import sharepy
import json
from tqdm import tqdm

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

SP_Link = Settings["General"]["Downloader"]["Sharepoint"]["Link"]
SP_Link_domain = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]

def Get_Table_Data(ws, data_boundary) -> DataFrame:
    data = ws[data_boundary]
    content = [[str(cell.internal_value) for cell in ent] for ent in data]
    header = content[0]
    data_rows = content[1:]
    TimeSheets_df = pandas.DataFrame(data=data_rows, columns = header)
    TimeSheets_df = TimeSheets_df[["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]]
    return TimeSheets_df

def Download_Excel(s_aut: sharepy) -> str:
    # Download
    r = s_aut.getfile(f"{SP_Link_domain}{SP_Link}", filename=".\\Libs\\Sharepoint\\TimeSheets.xlsx")
    return True

def Get_WorkSheet(Sheet_Name: str):
    WorkBook = load_workbook(filename=".\\Libs\\Sharepoint\\TimeSheets.xlsx")
    Sheet = WorkBook[Sheet_Name]
    return Sheet

def Get_Tables_on_Worksheet(Sheet) -> list:
    Table_list = []
    for key, value in Sheet.tables.items():
        Table = []
        Table.append(str(key))
        Table.append(str(value))
        Table_list.append(Table)
    return Table_list
    

def Timesheets_Identify_empty_row(TimeSheets_df: DataFrame) -> list[str, str]:
    # Reorder lines
    TimeSheets_df2 = TimeSheets_df.sort_index(ascending=False)

    # Find first non empty line and get index of empty line (crossing from NULL to Value)
    Pre_Row_Personnel_number = "Row_Personnel_number"
    Pre_Row_Date = "Row_Date"
    Pre_Row_Network_Description = "Row_Network_Description"
    Pre_Row_Activity = "Row_Activity"
    Pre_Row_Activity_description = "Row_Activity_description"
    Pre_Row_Start_Time = "Row_Start_Time"
    Pre_Row_End_Time = "Row_End_Time"

    for row in TimeSheets_df2.iterrows():
        # read values from row
        Row_Series = pandas.Series(row[1])
        Row_Index = row[0]
        Row_Personnel_number = Row_Series["Personnel number"]
        Row_Date = Row_Series["Date"]
        Row_Network_Description = Row_Series["Network Description"]
        Row_Activity = Row_Series["Activity"]
        Row_Activity_description = Row_Series["Activity description"]
        Row_Start_Time = Row_Series["Start Time"]
        Row_End_Time = Row_Series["End Time"]

        # Compare
        if (Pre_Row_Personnel_number == "None") and (Pre_Row_Date == "None") and (Pre_Row_Network_Description == "None") and (Pre_Row_Activity == "None") and (Pre_Row_Activity_description == "None") and (Pre_Row_Start_Time == "None") and (Pre_Row_End_Time == "None"):
            if (Row_Personnel_number == "None") and (Row_Date == "None") and (Row_Network_Description == "None") and (Row_Activity == "None") and (Row_Activity_description == "None") and (Row_Start_Time == "None") and (Row_End_Time == "None"):
                Excel_row_No = Row_Index
            else:
                Excel_row_No += 2   # add 2 because of that program works with indexes (start from 0) and find first occurence of values
                break

        Pre_Row_Personnel_number = Row_Personnel_number
        Pre_Row_Date = Row_Date
        Pre_Row_Network_Description = Row_Network_Description
        Pre_Row_Activity = Row_Activity
        Pre_Row_Activity_description = Row_Activity_description
        Pre_Row_Start_Time = Row_Start_Time
        Pre_Row_End_Time = Row_End_Time

    # Check because of first line
    if Excel_row_No == 0:
        Excel_row_No = 2
    else:
        pass
    
    A_Cell = f"A{Excel_row_No}"
    E_Cell = f"E{Excel_row_No}"
    return A_Cell, E_Cell

# ---------------------------------------------------------- Main Functions ---------------------------------------------------------- #
def Upload(Events: DataFrame) -> None:
    # Authentication
    s_aut = Authentication.Authentication()

    # Download
    Downloaded = Download_Excel(s_aut=s_aut)

    if Downloaded == True:
        # Get WorkSheet
        TimeSpent_ws = Get_WorkSheet(s_aut=s_aut, Sheet_Name="TimeSpent")

        # Get Table List from Worksheet
        Table_list = Get_Tables_on_Worksheet(Sheet=TimeSpent_ws)

        # TimeSheets_df
        data_boundary = Table_list[0][1]
        data_boundary = data_boundary.replace("O", "J")
        TimeSheets_df = Get_Table_Data(ws=TimeSpent_ws, data_boundary=data_boundary)
        A_Cell, E_Cell = Timesheets_Identify_empty_row(TimeSheets_df=TimeSheets_df)
        print(f"First Cell: {A_Cell}, {E_Cell}")
        #! Dodělat
