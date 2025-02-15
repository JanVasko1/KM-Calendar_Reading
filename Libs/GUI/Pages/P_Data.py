# Import Libraries
from pandas import DataFrame, read_csv

from customtkinter import CTk, CTkFrame, CTkLabel
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_Data(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    # ------------------------- Local Functions -------------------------#
    global Info_current_row, Info_Table_Rows, Events_List_Header
    Info_current_row = 0
    Info_Table_Rows = 20
    Events_List_Header = ["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]

    def change_first(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row > Info_Table_Rows:
            Info_current_row = Info_Table_Rows
            Showed_events = Events_List[0 : Info_Table_Rows]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{0} / {Info_Table_Rows} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_left(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row > Info_Table_Rows:
            Info_current_row -= Info_Table_Rows
            Start_interval = Info_current_row - Info_Table_Rows
            End_interval = Info_current_row

            if Start_interval < 0:
                Start_interval = 0
                End_interval = Info_Table_Rows
            else:
                pass

            Showed_events = Events_List[Start_interval : End_interval]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Start_interval} / {End_interval} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_right(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row < Events_list_len:
            Info_current_row += Info_Table_Rows
            Start_interval = Info_current_row - Info_Table_Rows
            End_interval = Info_current_row
            Showed_events = Events_List[Start_interval : Info_current_row]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Start_interval} / {End_interval} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_last(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row < Events_list_len:
            Info_current_row = Events_list_len
            Showed_events = Events_List[Events_list_len - Info_Table_Rows : Events_list_len]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Events_list_len - Info_Table_Rows} / {Events_list_len} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def Data_Excel():
        import subprocess
        subprocess.run('start excel "Operational\\Downloads\\Events.csv"', shell=True, capture_output=False, text=False)

    def Data_Upload(Events: DataFrame):
        SP_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        if SP_Password == None:
            CTkMessagebox(title="Error", message="Cannot upload, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Upload(Events=Events, SP_Password=SP_Password)
            CTkMessagebox(title="Success", message="Successfully uploaded to Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)

    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Data_Button_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Data_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Data_Work_Detail_Area.grid_propagate(flag=False)

    Events = read_csv(f"Operational\\Downloads\\Events.csv", sep=";")

    # ------------------------- Buttons Area -------------------------#
    # Download Button
    Button_Upload = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Upload.configure(text="Upload", command = lambda:Data_Upload(Events=Events))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Upload, message="Upload processed data directly to Sharepoint TimeSheets.", ToolTip_Size="Normal")

    # Download Button
    Button_Excel = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Excel.configure(text="Excel", command = lambda:Data_Excel())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Excel, message="Show generated Excel file.", ToolTip_Size="Normal")

    # ------------------------- Work Area -------------------------#
    # Current Page text
    Page_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Label_Size="H1", Font_Size="H1")

    # Data table
    Events_List = []
    for row in Events.iterrows():
        Events_List.append(row[1].to_list())
    Events_list_len = len(Events_List)

    Frame_Events_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Table_Values=None, Table_Size="Triple_size", Table_Columns=8, Table_Rows=Info_Table_Rows + 1)
    Frame_Events_Table_Var = Frame_Events_Table.children["!ctktable"]
    Frame_Events_Table_Var.configure(wraplength=180)
    # Init values in table
    change_right(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len)

    # Beginning Button
    Button_First = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_First.configure(text="<<", command = lambda: change_first(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_First, message="First page", ToolTip_Size="Normal")

    # Pre Button
    Button_Pre = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Pre.configure(text="<", command = lambda: change_left(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Pre, message="Previous page", ToolTip_Size="Normal")

    # next Button
    Button_Next = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Next.configure(text=">", command = lambda: change_right(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Next, message="Next page", ToolTip_Size="Normal")

    # End Button
    Button_Last = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Last.configure(text=">>", command = lambda: change_last(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Last, message="Last page", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Data_Button_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Data_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    Button_Upload.grid(row=0, column=0, padx=5, pady=15, sticky="e")
    Button_Excel.grid(row=0, column=1, padx=5, pady=15, sticky="e")

    Frame_Events_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Button_First.pack(side="left", expand=True, padx=(600,10), pady=10)
    Button_Pre.pack(side="left", expand=True, padx=(10,10), pady=10)
    Page_text.pack(side="left", expand=True, pady=10)
    Button_Next.pack(side="left", expand=True, padx=(10,10), pady=10)
    Button_Last.pack(side="left", expand=True, padx=(10,600), pady=10)


