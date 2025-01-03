# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import pywinstyles
import customtkinter
from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, CTkToplevel
from CTkToolTip import CTkToolTip
from CTkTable import CTkTable

from CTkColorPicker import *


from pandas import DataFrame

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
Settings = Defaults_Lists.Load_Settings()
Configuration = Defaults_Lists.Load_Configuration() 

# Apperance
Theme_Actual = Configuration["Global_Apperance"]["Window"]["Theme"]
Theme_List = list(Configuration["Global_Apperance"]["Window"]["Theme_List"])
Win_Style_Actual = Configuration["Global_Apperance"]["Window"]["Style"]
Win_Style_List = list(Configuration["Global_Apperance"]["Window"]["Style_List"])
Accent_Color_Mode = Configuration["Global_Apperance"]["Window"]["Accent_Color_Mode"]
Accent_Color_Mode_List = list(Configuration["Global_Apperance"]["Window"]["Accent_Color_List"])
Accent_Color_Manual = Configuration["Global_Apperance"]["Window"]["Accent_Color_Manual"]

# Sharepoint
SP_Auth_Email = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
SP_Auth_Address = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]
SP_Link = Settings["General"]["Downloader"]["Sharepoint"]["Link"]
SP_File_Name = Settings["General"]["Downloader"]["Sharepoint"]["File_name"]
SP_Person_Name = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Name"]
SP_Person_ID = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]

# Outlook
Outlook_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]

# Formats
Format_Date = Settings["General"]["Formats"]["Date"]
Format_Time = Settings["General"]["Formats"]["Time"]
Format_SP_DateTime = Settings["General"]["Formats"]["Exchange_DateTime"]

# Vacation
Vacation_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Search_Text"]
Vacation_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["All_Day"]
Vacation_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Part_Day"]
Vacation_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Vacation_Option_List"]

# HomeOffice
HomeOffice_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Search_Text"]
HomeOffice_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["All_Day"]
HomeOffice_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Part_Day"]
HomeOffice_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["HomeOffice_Option_List"]

# Lunch
Lunch_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Search_Text"]
Lunch_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["All_Day"]
Lunch_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Part_Day"]
Lunch_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Lunch_Option_List"]

# Events
Skip_Events_list = Settings["Event_Handler"]["Events"]["Skip"]
Skip_Event_General_dict = Settings["Event_Handler"]["Events"]["Empty"]["General"]
Skip_Event_Schedules_dict = Settings["Event_Handler"]["Events"]["Empty"]["Scheduled"]
Skip_AutoFill_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]

# Calendar - Working Day
Monday_Work_Start = Settings["General"]["Calendar"]["Monday"]["Work_Hours"]["Start_Time"]
Tuesday_Work_Start = Settings["General"]["Calendar"]["Tuesday"]["Work_Hours"]["Start_Time"]
Wednesday_Work_Start = Settings["General"]["Calendar"]["Wednesday"]["Work_Hours"]["Start_Time"]
Thursday_Work_Start = Settings["General"]["Calendar"]["Thursday"]["Work_Hours"]["Start_Time"]
Friday_Work_Start = Settings["General"]["Calendar"]["Friday"]["Work_Hours"]["Start_Time"]
Saturday_Work_Start = Settings["General"]["Calendar"]["Saturday"]["Work_Hours"]["Start_Time"]
Sunday_Work_Start = Settings["General"]["Calendar"]["Sunday"]["Work_Hours"]["Start_Time"]

Monday_Work_End = Settings["General"]["Calendar"]["Monday"]["Work_Hours"]["End_Time"]
Tuesday_Work_End = Settings["General"]["Calendar"]["Tuesday"]["Work_Hours"]["End_Time"]
Wednesday_Work_End = Settings["General"]["Calendar"]["Wednesday"]["Work_Hours"]["End_Time"]
Thursday_Work_End = Settings["General"]["Calendar"]["Thursday"]["Work_Hours"]["End_Time"]
Friday_Work_End = Settings["General"]["Calendar"]["Friday"]["Work_Hours"]["End_Time"]
Saturday_Work_End = Settings["General"]["Calendar"]["Saturday"]["Work_Hours"]["End_Time"]
Sunday_Work_End = Settings["General"]["Calendar"]["Sunday"]["Work_Hours"]["End_Time"]

# Calendar - Vacation
Monday_Vacation_Start = Settings["General"]["Calendar"]["Monday"]["Vacation"]["Start_Time"]
Tuesday_Vacation_Start = Settings["General"]["Calendar"]["Tuesday"]["Vacation"]["Start_Time"]
Wednesday_Vacation_Start = Settings["General"]["Calendar"]["Wednesday"]["Vacation"]["Start_Time"]
Thursday_Vacation_Start = Settings["General"]["Calendar"]["Thursday"]["Vacation"]["Start_Time"]
Friday_Vacation_Start = Settings["General"]["Calendar"]["Friday"]["Vacation"]["Start_Time"]
Saturday_Vacation_Start = Settings["General"]["Calendar"]["Saturday"]["Vacation"]["Start_Time"]
Sunday_Vacation_Start = Settings["General"]["Calendar"]["Sunday"]["Vacation"]["Start_Time"]

Monday_Vacation_End = Settings["General"]["Calendar"]["Monday"]["Vacation"]["End_Time"]
Tuesday_Vacation_End = Settings["General"]["Calendar"]["Tuesday"]["Vacation"]["End_Time"]
Wednesday_Vacation_End = Settings["General"]["Calendar"]["Wednesday"]["Vacation"]["End_Time"]
Thursday_Vacation_End = Settings["General"]["Calendar"]["Thursday"]["Vacation"]["End_Time"]
Friday_Vacation_End = Settings["General"]["Calendar"]["Friday"]["Vacation"]["End_Time"]
Saturday_Vacation_End = Settings["General"]["Calendar"]["Saturday"]["Vacation"]["End_Time"]
Sunday_Vacation_End = Settings["General"]["Calendar"]["Sunday"]["Vacation"]["End_Time"]

# Calendar - Work Start and End 
Start_Event_json = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
End_Event_json = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]

# Projects and Activities
Project_List = list(Settings["Event_Handler"]["Project"]["Project_List"])
Project_List.insert(0, "")  # Because there might be not filled one in Calendar
Activity_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
Activity_List.insert(0, "") # Because there might be not filled one in Calendar
Location_List = Settings["Event_Handler"]["Location"]["Location_List"]

# Parralle Events
Divide_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Divide_Method"]
Divide_Method_List = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Divide_Method_List"]
Start_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Start_Method"]
Start_Method_List = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Start_Method_List"]

# Joinin Methods
Join_Methods_List = list(Settings["Event_Handler"]["Events"]["Join_method"]["Methods_List"])
Join_Free = Settings["Event_Handler"]["Events"]["Join_method"]["Free"]
Join_Tentative = Settings["Event_Handler"]["Events"]["Join_method"]["Tentative"]
Join_Busy = Settings["Event_Handler"]["Events"]["Join_method"]["Busy"]
Join_OutOfOffice = Settings["Event_Handler"]["Events"]["Join_method"]["Out of Office"]
Join_Work_Else = Settings["Event_Handler"]["Events"]["Join_method"]["Working elsewhere"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Apperance_Change_Theme(Theme_Selected: str) ->  None:
    customtkinter.set_appearance_mode(mode_string=Theme_Selected)

def Apperance_Change_Win_Style(Win_Style_Selected: str, window: CTk|CTkFrame) -> None:
    pywinstyles.apply_style(window=window, style=Win_Style_Selected)
    window.update_idletasks()

def Apperance_Accent_Color(Accent_Color_Mode_Variable: StringVar, Accent_Color_Manual_Frame_Var: CTkEntry) -> None:
    if Accent_Color_Mode_Variable.get() == "System":
        Accent_Color_Manual_Frame_Var.configure(state="disabled")
    elif Accent_Color_Mode_Variable.get() == "Manual":
        Accent_Color_Manual_Frame_Var.focus()
        Accent_Color_Manual_Frame_Var.configure(state="normal")
    elif Accent_Color_Mode_Variable.get() == "Original":
        Accent_Color_Manual_Frame_Var.configure(state="disabled")
    else:
        pass

def Apperance_Pick_Manual_Color(Accent_Color_Manual_Frame_Var: CTkEntry) -> None:
    Collor_Picker_window = CTkToplevel()
    Collor_Picker_window.title("Collor Picker")
    Collor_Picker_window.geometry("295x240")
    Collor_Picker_window.bind(sequence="<Escape>", func=lambda evet: Collor_Picker_window.destroy())
    Collor_Picker_window.overrideredirect(boolean=True)
    Collor_Picker_window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
    Collor_Picker_window.resizable(width=False, height=False)
    Collor_Picker_window.attributes('-topmost', True)
    pywinstyles.apply_style(window=Collor_Picker_window, style=Win_Style_Actual)
    customtkinter.set_appearance_mode(mode_string=Theme_Actual)

    Colorpicker_Frame = Elements.Get_Color_Picker(Frame=Collor_Picker_window, Accent_Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var)

    #? Build look of Widget --> must be before inset
    Colorpicker_Frame.pack(padx=0, pady=0) 
    

def Add_Skip_Event() -> None:
    print("Add_Skip_Event")
    #! Dodělat --> funkce přidání do Skip eventů a uložení do json a znovunačtení tabulky
    pass

def Exchange_ReNew_Secret() -> None:
    print("Exchange_ReNew_Secret")
    #! Dodělat --> Zobrazí popu form a nechá vyplnit nový SEcret ID a pouze uloží do DB
    pass

def Del_Skip_Event() -> None:
    print("Del_Skip_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Add_Empty_Event() -> None:
    print("Add_Empty_Event")
    #! Dodělat --> funkce přidání do Empty - General eventů a uložení do json a znovunačtení tabulky
    #! Check if Coverage is Number
    pass

def Del_Empty_Event_One() -> None:
    print("Del_Empty_Event_One")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Del_Empty_Event_All() -> None:
    print("Del_Empty_All_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Recalculate_Empty_Event(Table: CTkTable) -> None:
    print("Recalculate_Empty_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Add_Schedule_Event() -> None:
    print("Add_Schedule_Event")
    #! Dodělat --> funkce přidání do Schedule eventů a uložení do json a znovunačtení tabulky
    #! Dodělat --> Check if Times are in proper format
    pass

def Del_Schedule_Event_One() -> None:
    print("Del_Schedule_Event_One")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Del_Schedule_Event_All() -> None:
    print("Del_Schedule_Event_All")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Add_AutoFill_Event() -> None:
    print("Add_AutoFill_Event")
    #! Dodělat --> funkce přidání do Add_AutoFill_Event a uložení do json a znovunačtení tabulky
    pass

def Del_AutoFill_Event_One() -> None:
    print("Del_AutoFill_Event_One")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Del_AutoFill_Event_All() -> None:
    print("Del_AutoFill_Event_All")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def DashBoard_Chart_Project() -> None:
    print("DashBoard_Chart_Project")
    #! Dodělat --> Přepnout graf na Projekty
    pass

def DashBoard_Chart_Activity() -> None:
    print("DashBoard_Chart_Activity")
    #! Dodělat --> Přepnout graf na Aktivity
    pass


# ---------------------------------------------------------- Download Page Widgets ---------------------------------------------------------- #
def Download_Sharepoint(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Timesheets for donwload process.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Sharepoint = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Sharepoint_Radio_Var = Use_Sharepoint.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Sharepoint_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Sharepoint")

    # Field - User ID
    User_ID = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    User_ID_Text_Var = User_ID.children["!ctkframe3"].children["!ctkentry"]
    User_ID_Text_Var.configure(placeholder_text=SP_Person_ID)
    User_ID_Text_Var.configure(state="disabled")

    # Field - User Email
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=SP_Auth_Email)
    Email_Text_Var.configure(state="disabled")

    # Field - Password
    Password = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 

    # Field - Get whole report Period
    Whole_Period_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Whole report period", Field_Type="Input_CheckBox") 
    Whole_Period_Frame_Var = Whole_Period_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Whole_Period_Frame_Var.configure(text="")

    # Field - Maximal Today date
    Max_Today_Date_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="End Date max Today", Field_Type="Input_CheckBox") 
    Max_Today_Date_Frame_Var = Max_Today_Date_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Max_Today_Date_Frame_Var.configure(text="")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Use_Sharepoint.pack(side="top", padx=10, pady=(0,5))
    User_ID.pack(side="top", padx=10, pady=(0,5))
    Email.pack(side="top", padx=10, pady=(0,5))
    Password.pack(side="top", padx=10, pady=(0,5))
    Whole_Period_Frame.pack(side="top", padx=10, pady=(0,5))
    Max_Today_Date_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Download_Manual(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for downlaod process.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Manual = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Manual_Radio_Var = Use_Manual.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Manual_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Manual")

    # Field - User ID
    Date_From = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From / T", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text="Date From")

    # Field - User Email
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To / T", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text="Date To")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Use_Manual.pack(side="top", padx=10, pady=(0,5))
    Date_From.pack(side="top", padx=10, pady=(0,5))
    Date_To.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Download_Exchange(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange Server", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Exchange = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Exchange_Radio_Var = Use_Exchange.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Exchange_Radio_Var.configure(text="", variable=Download_Data_Source, value="Exchange")

    # Field - User ID
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")

    # Field - Password
    Password = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Use_Exchange.pack(side="top", padx=10, pady=(0,5))
    Email.pack(side="top", padx=10, pady=(0,5))
    Password.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Download_Outlook(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Outlook Classic Client", Additional_Text="Must be updated befor download", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Windows installtion of Outlook Classic client.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Outlook = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Outlook_Radio_Var = Use_Outlook.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Outlook_Radio_Var.configure(text="", variable=Download_Data_Source, value="Outlook_Client")

    # Field - User ID
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Use_Outlook.pack(side="top", padx=10, pady=(0,5))
    Email.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main


# ---------------------------------------------------------- Dashboard Page Widgets ---------------------------------------------------------- #
# ------------- Total Line -------------#
def DashBoard_Totals_Total_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: float) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="history", Widget_Label_Tooltip="Shows total hours.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Total_Hours_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Total_Hours_text.configure(text=f"{str(Data)}")

    Total_Hours_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Total_Hours_unit_text.configure(text=f"hours")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Total_Hours_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Total_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Average_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: float) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="clock-arrow-up", Widget_Label_Tooltip="Shows Averate hours per Event.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Average_Hours_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Average_Hours_text.configure(text=f"{str(Data)}")

    Average_Hours_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Average_Hours_unit_text.configure(text=f"/hours")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Average_Hours_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Average_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Counter_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="arrow-up-1-0", Widget_Label_Tooltip="Shows total counts of Events.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Event_Counter_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Event_Counter_text.configure(text=f"{str(Data)}")

    Event_Counter_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Event_Counter_unit_text.configure(text=f"")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Event_Counter_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Event_Counter_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Report_Period_Util_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="circle-percent", Widget_Label_Tooltip="Shows if Utilization of Reporting Period.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Coverage_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Coverage_text.configure(text=f"{str(Data)}")

    Coverage_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Coverage_unit_text.configure(text=f"%")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Active_Day_Util_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="activity", Widget_Label_Tooltip="Shows utilization in realtion to my calendar and for active days only.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Day_Average_Coverage_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Day_Average_Coverage_text.configure(text=f"{str(Data)}")

    Day_Average_Coverage_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Day_Average_Coverage_unit_text.configure(text=f"%")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Day_Average_Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Day_Average_Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Utilization_Surplus_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set="lucide", Icon_Name="message-square-diff", Widget_Label_Tooltip="Shows hours if Im surplus againts KM actual day utilization for Imput End Date.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Day_Average_Coverage_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Day_Average_Coverage_text.configure(text=f"{str(Data)}")

    Day_Average_Coverage_unit_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Day_Average_Coverage_unit_text.configure(text=f"hours")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Day_Average_Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Day_Average_Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main


def DashBoard_Project_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Projec_DF: DataFrame) -> CTkFrame:
    # Data preparation
    Table_Values = [["Project", "Count", "Total [H]", "Average [H]"]]
    Table_Data_List = Projec_DF.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)

    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Shows Projects Details.", Scrollable=True) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Table
    Project_Table = Elements.Get_Table(Frame=Frame_Body, Table_size="Dashboard_Project_Activity", columns=4, rows=Projec_DF.shape[0] + 1)
    Project_Table.configure(values=Table_Values)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Project_Detail1_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Projec_DF: DataFrame) -> CTkFrame:
    # Data preparation
    Projec_DF = Projec_DF.head(-1)
    Most_Occurence_ID =  Projec_DF["Count"].idxmax()
    Most_Occurence_Project = Projec_DF.iloc[Most_Occurence_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Most Occcurence", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Count_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Project_Count_text.configure(text=f"{Most_Occurence_Project}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Count_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Project_Detail2_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Projec_DF: DataFrame) -> CTkFrame:
    # Data preparation
    Projec_DF = Projec_DF.head(-1)
    Most_Hours_ID =  Projec_DF["Total[H]"].idxmax()
    Most_Project_Hours = Projec_DF.iloc[Most_Hours_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Most Hours", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Hours_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Project_Hours_text.configure(text=f"{Most_Project_Hours}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Project_Detail3_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Projec_DF: DataFrame) -> CTkFrame:
    # Data preparation
    Projec_DF = Projec_DF.head(-1)
    Most_Hours_ID =  Projec_DF["Average[H]"].idxmax()
    Most_Project_Avg_Hours = Projec_DF.iloc[Most_Hours_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Projects Average Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Hours_Avg_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Project_Hours_Avg_text.configure(text=f"{Most_Project_Avg_Hours}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Hours_Avg_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # Data preparation
    Table_Values = [["Activity", "Count", "Total [H]", "Average [H]"]]
    Table_Data_List = Activity_Df.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Shows Activity Details.", Scrollable=True) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Table
    Activity_Table = Elements.Get_Table(Frame=Frame_Body, Table_size="Dashboard_Project_Activity", columns=4, rows=Activity_Df.shape[0] + 1)
    Activity_Table.configure(values=Table_Values)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Activity_Detail1_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Occurence_ID =  Activity_Df["Count"].idxmax()
    Most_Occurence_Activity = Activity_Df.iloc[Most_Occurence_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Events Count.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Count_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Activity_Count_text.configure(text=f"{Most_Occurence_Activity}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Count_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Detail2_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Hours_ID =  Activity_Df["Total[H]"].idxmax()
    Most_Activity_Hours = Activity_Df.iloc[Most_Hours_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Activity Total Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Hours_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Activity_Hours_text.configure(text=f"{Most_Activity_Hours}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Detail3_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Hours_ID =  Activity_Df["Average[H]"].idxmax()
    Most_Activity_Avg_Hours = Activity_Df.iloc[Most_Hours_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Activity Average Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Hours_Avg_text = Elements.Get_Label(Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Activity_Hours_Avg_text.configure(text=f"{Most_Activity_Avg_Hours}")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Hours_Avg_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_WeekDays_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, WeekDays_Df: DataFrame) -> CTkFrame:
    # Data preparation
    Table_Values = [["Week Day", "Days Count", "Total Events", "Total [H]", "Average [H]", "My Utilization [%]", "Utilization [%]"]]
    Table_Data_List = WeekDays_Df.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Detal WeekDay Summary.", Scrollable=True) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Table
    WeekDays_Table = Elements.Get_Table(Frame=Frame_Body, Table_size="Dashboard_WeekDays", columns=7, rows=WeekDays_Df.shape[0] + 1)
    WeekDays_Table.configure(values=Table_Values)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    WeekDays_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Weeks_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Weeks_DF: DataFrame) -> CTkFrame:
    # Data preparation
    Table_Values = [["Week", "Days", "Days w/o weekend", "Total Events", "Total [H]", "Average [H]", "Week Utilization [%]", "Active Days Utilization [%]"]]
    Table_Data_List = Weeks_DF.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Week details.", Scrollable=True) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Table
    Week_Table = Elements.Get_Table(Frame=Frame_Body, Table_size="Dashboard_Weeks", columns=8, rows=Weeks_DF.shape[0] + 1)
    Week_Table.configure(values=Table_Values)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Week_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_DaysChart_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Events_DF: DataFrame) -> CTkFrame:
    # Data preparation
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Detail day Project / Activity distribution.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    #! Dodělat --> dokončit Dashboard --> načtení grafů podle zvoleného 

    # Update Secret ID Button
    Button_Show_Projects = Elements.Get_Button(Frame=Frame_Body, Button_Size="Small")
    Button_Show_Projects.configure(text="Projects", command = lambda:DashBoard_Chart_Project())
    CTkToolTip(widget=Button_Show_Projects, message="Shows Charts with Projects.")

    # Update Secret ID Button
    Button_Show_Activities = Elements.Get_Button(Frame=Frame_Body, Button_Size="Small")
    Button_Show_Activities.configure(text="Activities", command = lambda:DashBoard_Chart_Activity())
    CTkToolTip(widget=Button_Show_Activities, message="Shows Charts with Activities.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Projects.pack(side="right", padx=10, pady=(0,5))
    Button_Show_Activities.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def DashBoard_Cumulated_Time_Widget(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Events_DF: DataFrame) -> CTkFrame:
    # Data preparation
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Set=None, Icon_Name=None, Widget_Label_Tooltip="Comparison between KM planned utilization and reported houss.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    #! Dodělat --> dokončit Dashboard --> načtení grafů podle zvoleného 

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

# ---------------------------------------------------------- Data Page Widgets ---------------------------------------------------------- #

# ---------------------------------------------------------- Information Page Widgets ---------------------------------------------------------- #

# ---------------------------------------------------------- Settings Page Widgets ---------------------------------------------------------- #
# ------------- Apperance -------------#
def Settings_Aperance_Theme(Frame: CTk|CTkFrame, window: CTk|CTkFrame) -> CTkFrame:
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Win_Style_Variable = StringVar(master=Frame, value=Win_Style_Actual)
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="General Apperance", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(values=Theme_List, variable=Theme_Variable)
    Theme_Frame_Var.configure(command= lambda Theme_Selected: Apperance_Change_Theme(Theme_Selected=Theme_Selected))

    # Field - Windows Style
    Win_Style_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Window Style", Field_Type="Input_OptionMenu") 
    Win_Style_Frame_Var = Win_Style_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Win_Style_Frame_Var.configure(values=Win_Style_List, variable=Win_Style_Variable)
    Win_Style_Frame_Var.configure(command= lambda Win_Style_Selected: Apperance_Change_Win_Style(Win_Style_Selected=Win_Style_Selected, window=window))

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(values=Accent_Color_Mode_List, variable=Accent_Color_Mode_Variable)

    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Input_Normal") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual)

    # Button - Collor Picker
    Button_Color_Picker = Elements.Get_Button(Frame=Frame_Body, Button_Size="Small")
    Button_Color_Picker.configure(text="Color Picker", command = lambda:Apperance_Pick_Manual_Color(Accent_Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var))
    CTkToolTip(widget=Button_Color_Picker, message="Select Manual Accent Collor.")

    # Disabling fields --> Download_Date_Range_Source
    Accent_Color_Mode_Frame_Var.configure(command = lambda a :Apperance_Accent_Color(Accent_Color_Mode_Variable=Accent_Color_Mode_Variable, Accent_Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var))

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Theme_Frame.pack(side="top", padx=10, pady=(0,5))
    Win_Style_Frame.pack(side="top", padx=10, pady=(0,5))
    Accent_Color_Mode_Frame.pack(side="top", padx=10, pady=(0,5))
    Accent_Color_Manual_Frame.pack(side="top", padx=10, pady=(0,5))
    Button_Color_Picker.pack(side="right", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Aperance_Color_Pallete(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Color Palletes", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    #! Dodělat --> nastavit defaultní BArevnou čkálu pro celý systém (příklad pro grafy)

    return Frame_Main
    


# ------------- General -------------#
def Settings_General_Sharepoint(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    SP_Name_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Name", Field_Type="Input_Normal") 
    SP_Name_Frame_Var = SP_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Name_Frame_Var.configure(placeholder_text=SP_Person_Name)

    # Field - User ID
    SP_User_ID_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal")
    SP_User_ID_Frame_Var = SP_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_User_ID_Frame_Var.configure(placeholder_text=SP_Person_ID)

    # Field - Path to Sharepoint
    SP_Link_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Sharepoin Address", Field_Type="Input_Normal")
    SP_Link_Frame_Var = SP_Link_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Link_Frame_Var.configure(placeholder_text=SP_Link)

    # Field - File Name 
    SP_File_Name_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="File Name", Field_Type="Input_Normal")
    SP_File_Name_Frame_Var = SP_File_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_File_Name_Frame_Var.configure(placeholder_text=SP_File_Name)
    SP_File_Name_Frame_Var.configure(state="disabled")

    # Field - Auth Email
    SP_Auth_Email_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Auth Email", Field_Type="Input_Normal")
    SP_Auth_Email_Frame_Var = SP_Auth_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Auth_Email_Frame_Var.configure(placeholder_text=SP_Auth_Email)

    # Field - Auth Address
    SP_Auth_Address_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Auth Address", Field_Type="Input_Normal")
    SP_Auth_Address_Frame_Var = SP_Auth_Address_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Auth_Address_Frame_Var.configure(placeholder_text=SP_Auth_Address)
    SP_Auth_Address_Frame_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    SP_Name_Frame.pack(side="top", padx=10, pady=(0,5))
    SP_User_ID_Frame.pack(side="top", padx=10, pady=(0,5))
    SP_Link_Frame.pack(side="top", padx=10, pady=(0,5))
    SP_File_Name_Frame.pack(side="top", padx=10, pady=(0,5))
    SP_Auth_Email_Frame.pack(side="top", padx=10, pady=(0,5))
    SP_Auth_Address_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_General_Exchange(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Exchange Server related setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    EX_Client_ID_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client ID", Field_Type="Input_Normal") 
    EX_Client_ID_Frame_Var = EX_Client_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Client_ID_Frame_Var.configure(placeholder_text=client_id)
    EX_Client_ID_Frame_Var.configure(state="disabled")

    # Field - User ID
    Ex_Client_Secret_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Secret", Field_Type="Input_Normal")
    Ex_Client_Secret_Frame_Var = Ex_Client_Secret_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Client_Secret_Frame_Var.configure(placeholder_text=client_secret)
    Ex_Client_Secret_Frame_Var.configure(state="disabled")

    # Field - Path to Sharepoint
    EX_Tenant_ID_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tenant ID", Field_Type="Input_Normal")
    EX_Tenant_ID_Frame_Var = EX_Tenant_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Tenant_ID_Frame_Var.configure(placeholder_text=tenant_id)
    EX_Tenant_ID_Frame_Var.configure(state="disabled")

    # Update Secret ID Button
    Button_Update_Secret = Elements.Get_Button(Frame=Frame_Body, Button_Size="Small")
    Button_Update_Secret.configure(text="Re-new Secret", command = lambda:Exchange_ReNew_Secret())
    CTkToolTip(widget=Button_Update_Secret, message="Update Secret ID.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    EX_Client_ID_Frame.pack(side="top", padx=10, pady=(0,5))
    Ex_Client_Secret_Frame.pack(side="top", padx=10, pady=(0,5))
    EX_Tenant_ID_Frame.pack(side="top", padx=10, pady=(0,5))
    Button_Update_Secret.pack(side="right", padx=10, pady=(0,5))


    return Frame_Main



def Settings_General_Formats(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Formats", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Dates formats used in program - non-changable.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    Date_From = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text=Format_Date)
    Date_From_Text_Var.configure(state="disabled")

    # Field - User ID
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Time", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_Time)
    Date_To_Text_Var.configure(state="disabled")

    # Field - Email
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Exchange DateTime", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_SP_DateTime)
    Date_To_Text_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Date_From.pack(side="top", padx=10, pady=(0,5))
    Date_To.pack(side="top", padx=10, pady=(0,5))
    Date_To.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Parralel_events(Frame: CTk|CTkFrame) -> CTkFrame:
    Divide_Method_Variable = StringVar(master=Frame, value=Divide_Method)
    Start_Method_Variable = StringVar(master=Frame, value=Start_Method)
    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Parralel Events Handler", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definitions of behavior of processing Envents when program found that they are parrallel.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Divide Method
    Divide_Method_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Divide Method", Field_Type="Input_OptionMenu") 
    Divide_Method_Frame_Var = Divide_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Divide_Method_Frame_Var.configure(values=Divide_Method_List, variable=Divide_Method_Variable)

    # Field - Start Method
    Start_Method_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Start Method", Field_Type="Input_OptionMenu") 
    Start_Method_Frame_Var = Start_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Start_Method_Frame_Var.configure(values=Start_Method_List, variable=Start_Method_Variable)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Divide_Method_Frame.pack(side="top", padx=10, pady=(0,5))
    Start_Method_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Join_events(Frame: CTk|CTkFrame) -> CTkFrame:
    Join_Free_Variable = StringVar(master=Frame, value=Join_Free)
    Join_Tentative_Variable = StringVar(master=Frame, value=Join_Tentative)
    Join_Busy_Variable = StringVar(master=Frame, value=Join_Busy)
    Join_OutOfOffice_Variable = StringVar(master=Frame, value=Join_OutOfOffice)
    Join_Work_Else_Variable = StringVar(master=Frame, value=Join_Work_Else)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Joining Events", Additional_Text="Under Construction", Widget_size="Single_size", Widget_Label_Tooltip="Joining Events belonging to same Visibility group.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Join Free Events
    Join_Free_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Free", Field_Type="Input_OptionMenu") 
    Join_Free_Frame_Var = Join_Free_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Free_Frame_Var.configure(values=Join_Methods_List, variable=Join_Free_Variable)

    # Field - Join Tentative Events
    Join_Tentative_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Tentative", Field_Type="Input_OptionMenu") 
    Join_Tentative_Frame_Var = Join_Tentative_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Tentative_Frame_Var.configure(values=Join_Methods_List, variable=Join_Tentative_Variable)

    # Field - Join Busy Events
    Join_Busy_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Busy", Field_Type="Input_OptionMenu") 
    Join_Busy_Frame_Var = Join_Busy_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Busy_Frame_Var.configure(values=Join_Methods_List, variable=Join_Busy_Variable)

    # Field - Join Out of Office Events
    Join_OutOfOffice_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Out of Office", Field_Type="Input_OptionMenu") 
    Join_OutOfOffice_Frame_Var = Join_OutOfOffice_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_OutOfOffice_Frame_Var.configure(values=Join_Methods_List, variable=Join_OutOfOffice_Variable)

    # Field - Join Working ElseWhere Events
    Join_Work_ElseWhere_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Working ElseWhere", Field_Type="Input_OptionMenu") 
    Join_Work_ElseWhere_Frame_Var = Join_Work_ElseWhere_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Work_ElseWhere_Frame_Var.configure(values=Join_Methods_List, variable=Join_Work_Else_Variable)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Join_Free_Frame.pack(side="top", padx=10, pady=(0,5))
    Join_Tentative_Frame.pack(side="top", padx=10, pady=(0,5))
    Join_Busy_Frame.pack(side="top", padx=10, pady=(0,5))
    Join_OutOfOffice_Frame.pack(side="top", padx=10, pady=(0,5))
    Join_Work_ElseWhere_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



# ------------- Calendar -------------#
def Settings_Calendar_Working_Hours(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Calendar - My own calendar", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Setup of my general working hours I usually have.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Monday
    Monday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday") 
    Monday_Frame_Var1 = Monday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Monday_Frame_Var1.configure(placeholder_text=Monday_Work_Start)
    Monday_Frame_Var2 = Monday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Monday_Frame_Var2.configure(placeholder_text=Monday_Work_End)

    # Field - Tuesday
    Tuesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday") 
    Tuesday_Frame_Var1 = Tuesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Frame_Var1.configure(placeholder_text=Tuesday_Work_Start)
    Tuesday_Frame_Var2 = Tuesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Frame_Var2.configure(placeholder_text=Tuesday_Work_End)

    # Field - Wednesday
    Wednesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday") 
    Wednesday_Frame_Var1 = Wednesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Frame_Var1.configure(placeholder_text=Wednesday_Work_Start)
    Wednesday_Frame_Var2 = Wednesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Frame_Var2.configure(placeholder_text=Wednesday_Work_End)

    # Field - Thursday
    Thursday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday") 
    Thursday_Frame_Var1 = Thursday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Frame_Var1.configure(placeholder_text=Thursday_Work_Start)
    Thursday_Frame_Var2 = Thursday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Frame_Var2.configure(placeholder_text=Thursday_Work_End)

    # Field - Friday
    Friday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday") 
    Friday_Frame_Var1 = Friday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Frame_Var1.configure(placeholder_text=Friday_Work_Start)
    Friday_Frame_Var2 = Friday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Frame_Var2.configure(placeholder_text=Friday_Work_End)

    # Field - Saturday
    Saturday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday") 
    Saturday_Frame_Var1 = Saturday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Frame_Var1.configure(placeholder_text=Saturday_Work_Start)
    Saturday_Frame_Var2 = Saturday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Frame_Var2.configure(placeholder_text=Saturday_Work_End)

    # Field - Sunday
    Sunday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday") 
    Sunday_Frame_Var1 = Sunday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Frame_Var1.configure(placeholder_text=Sunday_Work_Start)
    Sunday_Frame_Var2 = Sunday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Frame_Var2.configure(placeholder_text=Sunday_Work_End)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Monday_Frame.pack(side="top", padx=10, pady=(0,5))
    Tuesday_Frame.pack(side="top", padx=10, pady=(0,5))
    Wednesday_Frame.pack(side="top", padx=10, pady=(0,5))
    Thursday_Frame.pack(side="top", padx=10, pady=(0,5))
    Friday_Frame.pack(side="top", padx=10, pady=(0,5))
    Saturday_Frame.pack(side="top", padx=10, pady=(0,5))
    Sunday_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Calendar_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Calendar - KM Working/Vacation Hours", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="These hours be used in case of whole day vacation.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Monday
    Monday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday") 
    Search_Text_Text_Var1 = Monday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Text_Var1.configure(placeholder_text=Monday_Vacation_Start)
    Search_Text_Text_Var2 = Monday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Search_Text_Text_Var2.configure(placeholder_text=Monday_Vacation_End)

    # Field - Tuesday
    Tuesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday") 
    Tuesday_Frame_Var1 = Tuesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Frame_Var1.configure(placeholder_text=Tuesday_Vacation_Start)
    Tuesday_Frame_Var2 = Tuesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Frame_Var2.configure(placeholder_text=Tuesday_Vacation_End)

    # Field - Wednesday
    Wednesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday") 
    Wednesday_Frame_Var1 = Wednesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Frame_Var1.configure(placeholder_text=Wednesday_Vacation_Start)
    Wednesday_Frame_Var2 = Wednesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Frame_Var2.configure(placeholder_text=Wednesday_Vacation_End)

    # Field - Thursday
    Thursday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday") 
    Thursday_Frame_Var1 = Thursday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Frame_Var1.configure(placeholder_text=Thursday_Vacation_Start)
    Thursday_Frame_Var2 = Thursday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Frame_Var2.configure(placeholder_text=Thursday_Vacation_End)

    # Field - Friday
    Friday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday") 
    Friday_Frame_Var1 = Friday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Frame_Var1.configure(placeholder_text=Friday_Vacation_Start)
    Friday_Frame_Var2 = Friday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Frame_Var2.configure(placeholder_text=Friday_Vacation_End)

    # Field - Saturday
    Saturday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday") 
    Saturday_Frame_Var1 = Saturday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Frame_Var1.configure(placeholder_text=Saturday_Vacation_Start)
    Saturday_Frame_Var2 = Saturday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Frame_Var2.configure(placeholder_text=Saturday_Vacation_End)

    # Field - Sunday
    Sunday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday") 
    Sunday_Frame_Var1 = Sunday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Frame_Var1.configure(placeholder_text=Sunday_Vacation_Start)
    Sunday_Frame_Var2 = Sunday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Frame_Var2.configure(placeholder_text=Sunday_Vacation_End)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Monday_Frame.pack(side="top", padx=10, pady=(0,5))
    Tuesday_Frame.pack(side="top", padx=10, pady=(0,5))
    Wednesday_Frame.pack(side="top", padx=10, pady=(0,5))
    Thursday_Frame.pack(side="top", padx=10, pady=(0,5))
    Friday_Frame.pack(side="top", padx=10, pady=(0,5))
    Saturday_Frame.pack(side="top", padx=10, pady=(0,5))
    Sunday_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Calendar_Start_End_Time(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Workday - Start / End Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Events Subject which defines Start and End time of each day in Calendar.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Work - Start
    Start_Event = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - Start", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text=Start_Event_json)

    # Field - Work - End
    Start_Event = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - End", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text=End_Event_json)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Start_Event.pack(side="top", padx=10, pady=(0,5))
    Start_Event.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



# ------------- Events - General -------------#
def Settings_Events_General_Lunch(Frame: CTk|CTkFrame) -> CTkFrame:
    Lunch_All_Variable = StringVar(master=Frame, value=Lunch_All_Day)
    Lunch_Part_Variable = StringVar(master=Frame, value=Lunch_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Lunch", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Lunch brake -> always skip it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Lunch_Var = Search_Text_Lunch.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Lunch_Var.configure(placeholder_text=Lunch_Search_Text)

    # Field - All Day
    All_Day_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Lunch_Var = All_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Lunch_Var.configure(values=Lunch_Day_Option_List, variable=Lunch_All_Variable)

    # Field - Part Day
    Part_Day_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Lunch_Var = Part_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Lunch_Var.configure(values=Lunch_Day_Option_List, variable=Lunch_Part_Variable)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Search_Text_Lunch.pack(side="top", padx=10, pady=(0,5))
    All_Day_Lunch.pack(side="top", padx=10, pady=(0,5))
    Part_Day_Lunch.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Events_General_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    Vacation_All_Variable = StringVar(master=Frame, value=Vacation_All_Day)
    Vacation_Part_Variable = StringVar(master=Frame, value=Vacation_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Vacation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Vacation")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Vacation_Var = Search_Text_Vacation.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Vacation_Var.configure(placeholder_text=Vacation_Search_Text)

    # Field - All Day
    All_Day_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Vacation_Var = All_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Vacation_Var.configure(values=Vacation_Day_Option_List, variable=Vacation_All_Variable)

    # Field - Part Day
    Part_Day_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Vacation_Var = Part_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Vacation_Var.configure(values=Vacation_Day_Option_List, variable=Vacation_Part_Variable)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Search_Text_Vacation.pack(side="top", padx=10, pady=(0,5))
    All_Day_Vacation.pack(side="top", padx=10, pady=(0,5))
    Part_Day_Vacation.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Events_General_HomeOffice(Frame: CTk|CTkFrame) -> CTkFrame:
    HomeOffice_All_Variable = StringVar(master=Frame, value=HomeOffice_All_Day)
    HomeOffice_Part_Variable = StringVar(master=Frame, value=HomeOffice_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - HomeOffice", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of HomeOffice")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_HomeOffice = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_HomeOffice_Var = Search_Text_HomeOffice.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_HomeOffice_Var.configure(placeholder_text=HomeOffice_Search_Text)

    # Field - All Day
    All_Day_HomeOffice = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_HomeOffice_Var = All_Day_HomeOffice.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_HomeOffice_Var.configure(values=HomeOffice_Day_Option_List, variable=HomeOffice_All_Variable)

    # Field - Part Day
    Part_Day = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_HomeOffice_Var = Part_Day.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_HomeOffice_Var.configure(values=HomeOffice_Day_Option_List, variable=HomeOffice_Part_Variable)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Search_Text_HomeOffice.pack(side="top", padx=10, pady=(0,5))
    All_Day_HomeOffice.pack(side="top", padx=10, pady=(0,5))
    Part_Day.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main



def Settings_Events_General_Skip(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Skip Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of text be skipped as TimeSheet Entry in the case that part of text is found in Event Subject.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Imput Field + button in one line
    Frame_Imput_Total_Skip = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Total_Skip.configure(height=50)
    Frame_Imput_Total_Skip.pack_propagate(flag=False)

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total_Skip, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=400)

    Frame_Button_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total_Skip, Field_Frame_Type="Single_Column")
    Frame_Button_Area.configure(width=96)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Subject", Field_Type="Input_Small") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Skip Events Table
    Show_Skip_Events_list = [["Skip Events"]]
    for skip_Subject in Skip_Events_list:
        Show_Skip_Events_list.append([skip_Subject])
    
    Frame_Skip_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Body, Table_Size="Single_size", Table_Values=Show_Skip_Events_list, Table_Columns=1, Table_Rows=len(Skip_Events_list))
    Frame_Skip_Table_Var = Frame_Skip_Table.children["!ctktable"]
    Frame_Skip_Table_Var.configure(wraplength=440)

    # Add Button
    Button_Skip_Add = Elements.Get_Button(Frame=Frame_Button_Area, Button_Size="Small")
    Button_Skip_Add.configure(text="Add", command = lambda:Add_Skip_Event())
    CTkToolTip(widget=Button_Skip_Add, message="Add selected subejct to skip list")

    # Del Button
    Button_Skip_Del = Elements.Get_Button(Frame=Frame_Button_Area, Button_Size="Small")
    Button_Skip_Del.configure(text="Del", command = lambda:Del_Skip_Event())
    CTkToolTip(widget=Button_Skip_Del, message="Delete row from table based on input index.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Total_Skip.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Button_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)
    Subject_Text.pack(side="top", padx=10, pady=(0,5))
    Button_Skip_Add.pack(side="left", padx=10, pady=(0,5))
    Button_Skip_Del.pack(side="left", padx=10, pady=(0,5))
    Frame_Skip_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main



# ------------- Events - Empty -------------#
def Settings_Events_Empty_Generaly(Frame: CTk|CTkFrame) -> CTkFrame:
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Action_Variable = StringVar(master=Frame, value=Activity_List[0])

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Empty Space coverage Evets", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="For emty space program use fill them by this setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)

    # Field - Coverage
    Coverage_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Coverage", Field_Type="Input_Normal") 
    Activity_Option_Var = Coverage_Text.children["!ctkframe3"].children["!ctkentry"]
    Activity_Option_Var.configure(placeholder_text="Add %")

    # Empty Events table
    Skip_Event_General_list = [["Project", "Activity", "Description", "Coverage Percentage"]]
    Skip_Event_General_dict_rows = Skip_Event_General_dict.items()
    for Sub_Row in Skip_Event_General_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_General_list.append(list(Sub_dict.values()))

    Frame_Empty_General_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_General_list, Table_Columns=4, Table_Rows=len(Skip_Event_General_list))
    Frame_Empty_General_Table_Var = Frame_Empty_General_Table.children["!ctktable"]
    Frame_Empty_General_Table_Var.configure(wraplength=230)

    # Add Button
    Button_Empty_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Add.configure(text="Add", command = lambda:Add_Empty_Event())
    CTkToolTip(widget=Button_Empty_Add, message="Add selected combination into the list")

    # Del One Button
    Button_Empty_Del_One = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Del_One.configure(text="Del", command = lambda:Del_Empty_Event_One())
    CTkToolTip(widget=Button_Empty_Del_One, message="Delete row from table based on input index.")

    # Del All Button
    Button_Empty_Del_All = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Del_All.configure(text="Del all", command = lambda:Del_Empty_Event_All())
    CTkToolTip(widget=Button_Empty_Del_All, message="Delete all rows from table.")

    # Recalculate Button
    Button_Empty_Recal = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Recal.configure(text="Recalculate", command = lambda:Recalculate_Empty_Event(Table=Frame_Empty_General_Table_Var))
    CTkToolTip(widget=Button_Empty_Recal, message="Recalculate coverage for all lines.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)
    Subject_Text.pack(side="top", padx=10, pady=(0,5))
    Project_Option.pack(side="top", padx=10, pady=(0,5))
    Activity_Option.pack(side="top", padx=10, pady=(0,5))
    Coverage_Text.pack(side="top", padx=10, pady=(0,5))
    Button_Empty_Add.pack(side="right", padx=10, pady=(0,5))
    Button_Empty_Del_One.pack(side="right", padx=10, pady=(0,5))
    Button_Empty_Del_All.pack(side="right", padx=10, pady=(0,5))
    Button_Empty_Recal.pack(side="right", padx=10, pady=(0,5))
    Frame_Empty_General_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main



def Settings_Events_Empt_Schedule(Frame: CTk|CTkFrame) -> CTkFrame:
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Action_Variable = StringVar(master=Frame, value=Activity_List[0])

    Mon_Var = IntVar(master=Frame, value=0)
    Tue_Var = IntVar(master=Frame, value=0)
    Wed_Var = IntVar(master=Frame, value=0)
    Thu_Var = IntVar(master=Frame, value=0)
    Fri_Var = IntVar(master=Frame, value=0)
    Sat_Var = IntVar(master=Frame, value=0)
    Sun_Var = IntVar(master=Frame, value=0)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Evets Scheduler", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple TimeSheet Entry planner.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)

    # Field - Start Time
    Start_Time_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Start Time", Field_Type="Input_Normal") 
    Start_Time_Text_Var = Start_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    Start_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")

    # Field - End Time
    End_Time_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="End Time", Field_Type="Input_Normal") 
    End_Time_Text_Var = End_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    End_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")

    # Field - Week Days
    Week_Days_Label = Elements.Get_Label(Frame=Frame_Imput_Area, Label_Size="Column_Header", Font_Size="Column_Header")
    Week_Days_Label.configure(text="Week Days")
    Week_Days_Label.pack_propagate(flag=False)

    Week_Days_Frame = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column")
    Week_Days_Frame.configure(width=300)

    Monday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Mon") 
    Monday_Check_Frame_Var = Monday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Monday_Check_Frame_Var.configure(variable=Mon_Var, text="")

    Tuesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Tue") 
    Tuesday_Check_Frame_Var = Tuesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Tuesday_Check_Frame_Var.configure(variable=Tue_Var, text="")

    Wednesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Wed") 
    Wednesday_Check_Frame_Var = Wednesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Wednesday_Check_Frame_Var.configure(variable=Wed_Var, text="")

    Thursday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Thu") 
    Thursday_Check_Frame_Var = Thursday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Thursday_Check_Frame_Var.configure(variable=Thu_Var, text="")

    Friday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Fri") 
    Friday_Check_Frame_Var = Friday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Friday_Check_Frame_Var.configure(variable=Fri_Var, text="")

    Saturday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sat") 
    Saturday_Check_Frame_Var = Saturday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Saturday_Check_Frame_Var.configure(variable=Sat_Var, text="")

    Sunday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sun") 
    Sunday_Check_Frame_Var = Sunday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Sunday_Check_Frame_Var.configure(variable=Sun_Var, text="")

    # Scheduled Events table
    Skip_Event_Schedule_list = [["Project", "Activity", "Description", "Day in week", "Start Time", "End Time"]]
    Skip_Event_Schedule_dict_rows = Skip_Event_Schedules_dict.items()
    for Sub_Row in Skip_Event_Schedule_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_Schedule_list.append(list(Sub_dict.values()))

    Frame_Empty_Schedules_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_Schedule_list, Table_Columns=6, Table_Rows=len(Skip_Event_Schedule_list))
    Frame_Empty_Schedules_Table_Var = Frame_Empty_Schedules_Table.children["!ctktable"]
    Frame_Empty_Schedules_Table_Var.configure(wraplength=150)

    # Add Button
    Button_Schedule_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Schedule_Add.configure(text="Add", command = lambda:Add_Schedule_Event())
    CTkToolTip(widget=Button_Schedule_Add, message="Add selected combination into the list")

    # Del Button
    Button_Schedule_Del_One = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Schedule_Del_One.configure(text="Del", command = lambda:Del_Schedule_Event_One())
    CTkToolTip(widget=Button_Schedule_Del_One, message="Delete row from table based on input index.")

    # Del All Button
    Button_Schedule_Del_All = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Schedule_Del_All.configure(text="Del all", command = lambda:Del_Schedule_Event_All())
    CTkToolTip(widget=Button_Schedule_Del_All, message="Delete all rows from table.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)
    Subject_Text.pack(side="top", padx=10, pady=(0,5))
    Project_Option.pack(side="top", padx=10, pady=(0,5))
    Activity_Option.pack(side="top", padx=10, pady=(0,5))
    Start_Time_Text.pack(side="top", padx=10, pady=(0,5))
    End_Time_Text.pack(side="top", padx=10, pady=(0,5))
    Week_Days_Label.pack(side="top", fill="none", expand=False, padx=10, pady=10)
    Week_Days_Frame.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Monday_Check_Frame.pack(side="left", padx=5, pady=5)
    Tuesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Wednesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Thursday_Check_Frame.pack(side="left", padx=5, pady=5)
    Friday_Check_Frame.pack(side="left", padx=5, pady=5)
    Saturday_Check_Frame.pack(side="left", padx=5, pady=5)
    Sunday_Check_Frame.pack(side="left", padx=5, pady=5)
    Button_Schedule_Add.pack(side="right", padx=10, pady=(0,5))
    Button_Schedule_Del_One.pack(side="right", padx=10, pady=(0,5))
    Button_Schedule_Del_All.pack(side="right", padx=10, pady=(0,5))
    Frame_Empty_Schedules_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    return Frame_Main



# ------------- Events - AutoFill -------------#
def Settings_Events_AutoFill(Frame: CTk|CTkFrame) -> CTkFrame:
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Action_Variable = StringVar(master=Frame, value=Activity_List[0])
    Location_Variable = StringVar(master=Frame, value=Location_List[0])
    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="AutoFill rules", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple ruless applied on TimeSheet Entry if part/whole Search Text is found in Subject. If empty then do not fill it or overwrite it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Search Text", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)

    # Field - Location
    Location_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Location", Field_Type="Input_OptionMenu") 
    Location_Option_Var = Location_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Location_Option_Var.configure(values=Location_List, variable=Location_Variable)

    # AutoFilling Table
    Skip_AutoFill_list = [["Find Text within subject", "Set Project", "Set Activity", "Set Location"]]
    Skip_AutoFill_dict_rows = Skip_AutoFill_dict.items()
    for Sub_Row in Skip_AutoFill_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_AutoFill_list.append(list(Sub_dict.values()))

    Frame_AutoFiller_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_AutoFill_list, Table_Columns=4, Table_Rows=len(Skip_AutoFill_list))
    Frame_AutoFiller_Table_Var = Frame_AutoFiller_Table.children["!ctktable"]
    Frame_AutoFiller_Table_Var.configure(wraplength=230)

    # Add Button
    Button_AutoFill_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_AutoFill_Add.configure(text="Add", command = lambda:Add_AutoFill_Event())
    CTkToolTip(widget=Button_AutoFill_Add, message="Add selected combination into the list")

    # Del Button
    Button_AutoFill_Del_One = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_AutoFill_Del_One.configure(text="Del", command = lambda:Del_AutoFill_Event_One())
    CTkToolTip(widget=Button_AutoFill_Del_One, message="Delete row from table based on input index.")

    # Del All Button
    Button_AutoFill_Del_All = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_AutoFill_Del_All.configure(text="Del all", command = lambda:Del_AutoFill_Event_All())
    CTkToolTip(widget=Button_AutoFill_Del_All, message="Delete all rows from table.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)
    Subject_Text.pack(side="top", padx=10, pady=(0,5))
    Project_Option.pack(side="top", padx=10, pady=(0,5))
    Activity_Option.pack(side="top", padx=10, pady=(0,5))
    Location_Option.pack(side="top", padx=10, pady=(0,5))
    Button_AutoFill_Add.pack(side="right", padx=10, pady=(0,5))
    Button_AutoFill_Del_One.pack(side="right", padx=10, pady=(0,5))
    Button_AutoFill_Del_All.pack(side="right", padx=10, pady=(0,5))
    Frame_AutoFiller_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    return Frame_Main