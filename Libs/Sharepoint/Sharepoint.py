# Import Libraries
import Libs.Sharepoint.Authentication as Authentication
import Libs.Defaults_Lists as Defaults_Lists
from openpyxl import load_workbook
from pandas import DataFrame
import pandas
import sharepy

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
SP_Team = Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
SP_Link = Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_Links"][f"{SP_Team}"]
SP_Link_domain = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]
SP_File_Name = Settings["General"]["Downloader"]["Sharepoint"]["File_name"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
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
    r = s_aut.getfile(f"{SP_Link_domain}{SP_Link}", filename=f"Operational\\{SP_File_Name}")
    return True

def Get_WorkSheet(Sheet_Name: str):
    WorkBook = load_workbook(filename=f"Operational\\{SP_File_Name}")
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
    

def Time_sheets_Identify_empty_row(TimeSheets_df: DataFrame) -> list[str, str]:
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
                Excel_row_No += 2   # add 2 because of that program works with indexes (start from 0) and find first occurrence of values
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
def Upload(Events: DataFrame, SP_Password: str|None) -> None:
    # Authentication
    s_aut = Authentication.Authentication(SP_Password=SP_Password)

    # Download
    Downloaded = Download_Excel(s_aut=s_aut)

    if Downloaded == True:
        # Get WorkSheet
        TimeSpent_ws = Get_WorkSheet(Sheet_Name="TimeSpent")

        # Get Table List from Worksheet
        Table_list = Get_Tables_on_Worksheet(Sheet=TimeSpent_ws)

        # TimeSheets_df
        data_boundary = Table_list[0][1]
        data_boundary = data_boundary.replace("O", "J")
        TimeSheets_df = Get_Table_Data(ws=TimeSpent_ws, data_boundary=data_boundary)
        A_Cell, E_Cell = Time_sheets_Identify_empty_row(TimeSheets_df=TimeSheets_df)

        # TODO --> automatically upload to Sharepoint only to new lines "Paste as text only"
        CTkMessagebox(title="Warning Message!", message=f"First Cell: {A_Cell}, {E_Cell} --> Not finished development", icon="warning", fade_in_duration=1, option_1="OK")
        

def Get_Project_and_Activity(SP_Password: str|None) -> None:
    # Authentication
    s_aut = Authentication.Authentication(SP_Password=SP_Password)

    # Download
    Downloaded = Download_Excel(s_aut=s_aut)
    
    if Downloaded == True:
        Get_Project()
        Get_Activity()
        
def Get_Project() -> None:
    Projects_df = pandas.read_excel(io=f"Operational\\{SP_File_Name}", sheet_name="Projects", usecols="A:C", skiprows=1, nrows=100, header=None)
    Projects_df.drop(columns=[1], inplace=True)
    Projects_df.rename(columns={0: "Project", 2: "Project_Type"}, inplace=True)

    Projects_df = Projects_df.T
    Projects_dict = Projects_df.to_dict()

    # Save to Settings.json
    Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Project", "Project_List"], Information=Projects_dict)
    
def Get_Activity() -> None:
    Activities_df = pandas.read_excel(io=f"Operational\\{SP_File_Name}", sheet_name="Activity", usecols="A:B", skiprows=1, nrows=100, header=None)
    Column_List = Activities_df[1].to_list()
    Empty_line_index = Column_List.index("Activity")
    Activities_df = Activities_df.iloc[Empty_line_index + 1:]
    Activities_df.reset_index(inplace=True)
    Activities_df.drop(columns=["index"], inplace=True)
    Activities_df.rename(columns={0: "Project_Type", 1: "Activity"}, inplace=True)

    Activity_list = list(set(Activities_df["Activity"]))
    Activity_list.sort()

    Project_Type_list = list(set(Activities_df["Project_Type"]))
    Project_Type_list.sort()

    # Dictionary creation
    Activity_by_Type_dict = {}
    Counter = 0
    for Project_Type in Project_Type_list:
        mask =  Activities_df["Project_Type"] == Project_Type
        Filtered_Df = Activities_df[mask]
        Activity_by_Type_list = Filtered_Df["Activity"].to_list()
        Activity_by_Type_list.sort()

        Activity_by_Type_dict[Counter] = {
            "Project_Type": Project_Type,
            "Activity": Activity_by_Type_list
        }
        Counter += 1

    # Save to Settings.json
    Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Activity", "Activity_List"], Information=Activity_list)
    Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Activity", "Activity_by_Type_dict"], Information=Activity_by_Type_dict)
