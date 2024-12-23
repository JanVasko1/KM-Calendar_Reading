# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
from customtkinter import CTk, CTkFrame, IntVar, StringVar
from CTkToolTip import CTkToolTip

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
# Sharepoint
SP_Email = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
SP_Link_domain = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]

# Person
Person_Name = Settings["General"]["Person"]["Name"]
Person_ID = Settings["General"]["Person"]["Code"]

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
Skip_AutoFill_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Details"]

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
Project_List.insert(0, "")
Activity_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
Activity_List.insert(0, "")
Location_List = Settings["Event_Handler"]["Location"]["Location_List"]

# Parralle Events
Divide_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Divide_Method"]
Divide_Method_List = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Divide_Method_List"]
Start_Method = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Start_Method"]
Start_Method_List = Settings["Event_Handler"]["Events"]["Parralel_Events"]["Start_Method_List"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Add_Skip_Event() -> None:
    print("Add_Skip_Event")
    #! Dodělat --> funkce přidání do Skip eventů a uložení do json a znovunačtení tabulky
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

def Del_Empty_Event() -> None:
    print("Del_Empty_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Add_Schedule_Event() -> None:
    print("Add_Schedule_Event")
    #! Dodělat --> funkce přidání do Schedule eventů a uložení do json a znovunačtení tabulky
    #! Check if Times are in proper format
    pass

def Del_Schedule_Event() -> None:
    print("Del_Schedule_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

def Add_AutoFill_Event() -> None:
    print("Add_AutoFill_Event")
    #! Dodělat --> funkce přidání do Add_AutoFill_Event a uložení do json a znovunačtení tabulky
    pass

def Del_AutoFill_Event() -> None:
    print("Del_AutoFill_Event")
    #! Dodělat --> vymazat z tabulky a uložit do Json
    pass

# ---------------------------------------------------------- Download Page Widgets ---------------------------------------------------------- #
def Download_Sharepoint(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Timesheets for donwload process.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Use
    Use_Sharepoint = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Sharepoint_Radio_Var = Use_Sharepoint.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Sharepoint_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Sharepoint")
    Use_Sharepoint.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    User_ID = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    User_ID_Text_Var = User_ID.children["!ctkframe3"].children["!ctkentry"]
    User_ID_Text_Var.configure(placeholder_text=Person_ID)
    User_ID_Text_Var.configure(state="disabled")
    User_ID.pack(side="top", padx=10, pady=(0,5))

    # Field - User Email
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=SP_Email)
    Email_Text_Var.configure(state="disabled")
    Email.pack(side="top", padx=10, pady=(0,5))

    # Field - Password
    Password = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    Password.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Download_Manual(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for downlaod process.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Use
    Use_Manual = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Manual_Radio_Var = Use_Manual.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Manual_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Manual")
    Use_Manual.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    Date_From = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From / T", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text="Date From")
    Date_From.pack(side="top", padx=10, pady=(0,5))

    # Field - User Email
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To / T", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text="Date To")
    Date_To.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Download_Exchange(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange Server", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Use
    Use_Exchange = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Exchange_Radio_Var = Use_Exchange.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Exchange_Radio_Var.configure(text="", variable=Download_Data_Source, value="Exchange")
    Use_Exchange.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")
    Email.pack(side="top", padx=10, pady=(0,5))

    # Field - Password
    Password = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    Password.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Download_Outlook(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Outlook Classic Client", Additional_Text="Must be updated befor download", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Windows installtion of Outlook Classic client.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Use
    Use_Outlook = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Outlook_Radio_Var = Use_Outlook.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Outlook_Radio_Var.configure(text="", variable=Download_Data_Source, value="Outlook_Client")
    Use_Outlook.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    Email = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")
    Email.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

# ---------------------------------------------------------- Dashboard Page Widgets ---------------------------------------------------------- #

# ---------------------------------------------------------- Data Page Widgets ---------------------------------------------------------- #

# ---------------------------------------------------------- Information Page Widgets ---------------------------------------------------------- #

# ---------------------------------------------------------- Settings Page Widgets ---------------------------------------------------------- #
# ------------- General -------------#
def Settings_General_Sharepoint(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Name
    Date_From = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Name", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text=Person_Name)
    Date_From.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Person_ID)
    Date_To.pack(side="top", padx=10, pady=(0,5))

    # Field - Email
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=SP_Email)
    Date_To.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_General_Formats(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Formats", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Dates formats used in program - non-changable.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Name
    Date_From = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text=Format_Date)
    Date_From_Text_Var.configure(state="disabled")
    Date_From.pack(side="top", padx=10, pady=(0,5))

    # Field - User ID
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Time", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_Time)
    Date_To_Text_Var.configure(state="disabled")
    Date_To.pack(side="top", padx=10, pady=(0,5))

    # Field - Email
    Date_To = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Exchange DateTime", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_SP_DateTime)
    Date_To_Text_Var.configure(state="disabled")
    Date_To.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main


def Settings_Parralel_events(Frame: CTk|CTkFrame) -> CTkFrame:
    Divide_Method_Variable = StringVar(master=Frame, value=Divide_Method)
    Start_Method_Variable = StringVar(master=Frame, value=Start_Method)
    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Parralel Events Handler", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definitions of behavior of processing Envents when program found that they are parrallel.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Divide Method
    Divide_Method_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Divide Method", Field_Type="Input_OptionMenu") 
    Divide_Method_Frame_Var = Divide_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Divide_Method_Frame_Var.configure(values=Divide_Method_List, variable=Divide_Method_Variable)
    Divide_Method_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Start Method
    Start_Method_Frame = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Start Method", Field_Type="Input_OptionMenu") 
    Start_Method_Frame_Var = Start_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Start_Method_Frame_Var.configure(values=Start_Method_List, variable=Start_Method_Variable)
    Start_Method_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Join_events(Frame: CTk|CTkFrame) -> CTkFrame:
    #! Dodělat --> Joining Events Setup
    pass

# ------------- Calendar -------------#
def Settings_Calendar_Working_Hours(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Calendar - Working Hours", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Setup of my general working hours I usually have.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Monday
    Monday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday") 
    Monday_Frame_Var1 = Monday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Monday_Frame_Var1.configure(placeholder_text=Monday_Work_Start)
    Monday_Frame_Var2 = Monday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Monday_Frame_Var2.configure(placeholder_text=Monday_Work_End)
    Monday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Tuesday
    Tuesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday") 
    Tuesday_Frame_Var1 = Tuesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Frame_Var1.configure(placeholder_text=Tuesday_Work_Start)
    Tuesday_Frame_Var2 = Tuesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Frame_Var2.configure(placeholder_text=Tuesday_Work_End)
    Tuesday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Wednesday
    Wednesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday") 
    Wednesday_Frame_Var1 = Wednesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Frame_Var1.configure(placeholder_text=Wednesday_Work_Start)
    Wednesday_Frame_Var2 = Wednesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Frame_Var2.configure(placeholder_text=Wednesday_Work_End)
    Wednesday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Thursday
    Thursday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday") 
    Thursday_Frame_Var1 = Thursday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Frame_Var1.configure(placeholder_text=Thursday_Work_Start)
    Thursday_Frame_Var2 = Thursday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Frame_Var2.configure(placeholder_text=Thursday_Work_End)
    Thursday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Friday
    Friday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday") 
    Friday_Frame_Var1 = Friday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Frame_Var1.configure(placeholder_text=Friday_Work_Start)
    Friday_Frame_Var2 = Friday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Frame_Var2.configure(placeholder_text=Friday_Work_End)
    Friday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Saturday
    Saturday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday") 
    Saturday_Frame_Var1 = Saturday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Frame_Var1.configure(placeholder_text=Saturday_Work_Start)
    Saturday_Frame_Var2 = Saturday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Frame_Var2.configure(placeholder_text=Saturday_Work_End)
    Saturday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Sunday
    Sunday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday") 
    Sunday_Frame_Var1 = Sunday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Frame_Var1.configure(placeholder_text=Sunday_Work_Start)
    Sunday_Frame_Var2 = Sunday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Frame_Var2.configure(placeholder_text=Sunday_Work_End)
    Sunday_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Calendar_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Calendar - Vacation Hours", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="These hours be used in case of whole day vacation.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Monday
    Monday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday") 
    Search_Text_Text_Var1 = Monday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Text_Var1.configure(placeholder_text=Monday_Vacation_Start)
    Search_Text_Text_Var2 = Monday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Search_Text_Text_Var2.configure(placeholder_text=Monday_Vacation_End)
    Monday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Tuesday
    Tuesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday") 
    Tuesday_Frame_Var1 = Tuesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Frame_Var1.configure(placeholder_text=Tuesday_Vacation_Start)
    Tuesday_Frame_Var2 = Tuesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Frame_Var2.configure(placeholder_text=Tuesday_Vacation_End)
    Tuesday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Wednesday
    Wednesday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday") 
    Wednesday_Frame_Var1 = Wednesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Frame_Var1.configure(placeholder_text=Wednesday_Vacation_Start)
    Wednesday_Frame_Var2 = Wednesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Frame_Var2.configure(placeholder_text=Wednesday_Vacation_End)
    Wednesday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Thursday
    Thursday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday") 
    Thursday_Frame_Var1 = Thursday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Frame_Var1.configure(placeholder_text=Thursday_Vacation_Start)
    Thursday_Frame_Var2 = Thursday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Frame_Var2.configure(placeholder_text=Thursday_Vacation_End)
    Thursday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Friday
    Friday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday") 
    Friday_Frame_Var1 = Friday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Frame_Var1.configure(placeholder_text=Friday_Vacation_Start)
    Friday_Frame_Var2 = Friday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Frame_Var2.configure(placeholder_text=Friday_Vacation_End)
    Friday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Saturday
    Saturday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday") 
    Saturday_Frame_Var1 = Saturday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Frame_Var1.configure(placeholder_text=Saturday_Vacation_Start)
    Saturday_Frame_Var2 = Saturday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Frame_Var2.configure(placeholder_text=Saturday_Vacation_End)
    Saturday_Frame.pack(side="top", padx=10, pady=(0,5))

    # Field - Sunday
    Sunday_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday") 
    Sunday_Frame_Var1 = Sunday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Frame_Var1.configure(placeholder_text=Sunday_Vacation_Start)
    Sunday_Frame_Var2 = Sunday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Frame_Var2.configure(placeholder_text=Sunday_Vacation_End)
    Sunday_Frame.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Calendar_Start_End_Time(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Workday - Start / End Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Events Subject which defines Start and End time of each day in Calendar.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Work - Start
    Start_Event = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - Start", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text=Start_Event_json)
    Start_Event.pack(side="top", padx=10, pady=(0,5))

    # Field - Work - End
    Start_Event = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - End", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text=End_Event_json)
    Start_Event.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main


# ------------- Events - General -------------#
def Settings_Events_General_Lunch(Frame: CTk|CTkFrame) -> CTkFrame:
    Lunch_All_Variable = StringVar(master=Frame, value=Lunch_All_Day)
    Lunch_Part_Variable = StringVar(master=Frame, value=Lunch_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Lunch", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Lunch brake -> always skip it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Seach Text
    Search_Text_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Lunch_Var = Search_Text_Lunch.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Lunch_Var.configure(placeholder_text=Lunch_Search_Text)
    Search_Text_Lunch.pack(side="top", padx=10, pady=(0,5))

    # Field - All Day
    All_Day_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Lunch_Var = All_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Lunch_Var.configure(values=Lunch_Day_Option_List, variable=Lunch_All_Variable)
    All_Day_Lunch.pack(side="top", padx=10, pady=(0,5))

    # Field - Part Day
    Part_Day_Lunch = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Lunch_Var = Part_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Lunch_Var.configure(values=Lunch_Day_Option_List, variable=Lunch_Part_Variable)
    Part_Day_Lunch.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Events_General_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    Vacation_All_Variable = StringVar(master=Frame, value=Vacation_All_Day)
    Vacation_Part_Variable = StringVar(master=Frame, value=Vacation_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Vacation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Vacation")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Seach Text
    Search_Text_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Vacation_Var = Search_Text_Vacation.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Vacation_Var.configure(placeholder_text=Vacation_Search_Text)
    Search_Text_Vacation.pack(side="top", padx=10, pady=(0,5))

    # Field - All Day
    All_Day_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Vacation_Var = All_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Vacation_Var.configure(values=Vacation_Day_Option_List, variable=Vacation_All_Variable)
    All_Day_Vacation.pack(side="top", padx=10, pady=(0,5))

    # Field - Part Day
    Part_Day_Vacation = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Vacation_Var = Part_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Vacation_Var.configure(values=Vacation_Day_Option_List, variable=Vacation_Part_Variable)
    Part_Day_Vacation.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Events_General_HomeOffice(Frame: CTk|CTkFrame) -> CTkFrame:
    HomeOffice_All_Variable = StringVar(master=Frame, value=HomeOffice_All_Day)
    HomeOffice_Part_Variable = StringVar(master=Frame, value=HomeOffice_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - HomeOffice", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of HomeOffice")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Field - Seach Text
    Search_Text_HomeOffice = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_HomeOffice_Var = Search_Text_HomeOffice.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_HomeOffice_Var.configure(placeholder_text=HomeOffice_Search_Text)
    Search_Text_HomeOffice.pack(side="top", padx=10, pady=(0,5))

    # Field - All Day
    All_Day_HomeOffice = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_HomeOffice_Var = All_Day_HomeOffice.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_HomeOffice_Var.configure(values=HomeOffice_Day_Option_List, variable=HomeOffice_All_Variable)
    All_Day_HomeOffice.pack(side="top", padx=10, pady=(0,5))

    # Field - Part Day
    Part_Day = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_HomeOffice_Var = Part_Day.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_HomeOffice_Var.configure(values=HomeOffice_Day_Option_List, variable=HomeOffice_Part_Variable)
    Part_Day.pack(side="top", padx=10, pady=(0,5))

    return Frame_Main

def Settings_Events_General_Skip(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Skip Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of text be skipped as TimeSheet Entry in the case that part of text is found in Event Subject.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Imput Field + button in one line
    Frame_Imput_Total_Skip = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Total_Skip.configure(height=50)
    Frame_Imput_Total_Skip.pack_propagate(flag=False)
    Frame_Imput_Total_Skip.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total_Skip, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=400)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Button_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total_Skip, Field_Frame_Type="Single_Column")
    Frame_Button_Area.configure(width=96)
    Frame_Button_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Subject", Field_Type="Input_Small") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")
    Subject_Text.pack(side="top", padx=10, pady=(0,5))

    # Add Button
    Button_Skip_Add = Elements.Get_Button(Frame=Frame_Button_Area, Button_Size="Small")
    Button_Skip_Add.configure(text="Add", command = lambda:Add_Skip_Event())
    Button_Skip_Add.pack(side="left", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Skip_Add, message="Add selected subejct to skip list")

    # Del Button
    Button_Skip_Del = Elements.Get_Button(Frame=Frame_Button_Area, Button_Size="Small")
    Button_Skip_Del.configure(text="Del", command = lambda:Del_Skip_Event())
    Button_Skip_Del.pack(side="left", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Skip_Del, message="Delete row from table based on input index.")

    # Skip Events Table
    Show_Skip_Events_list = [["Skip Events"]]
    for skip_Subject in Skip_Events_list:
        Show_Skip_Events_list.append([skip_Subject])
    
    Frame_Skip_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Body, Table_Size="Single_size", Table_Values=Show_Skip_Events_list, Table_Columns=1, Table_Rows=len(Skip_Events_list))
    Frame_Skip_Table_Var = Frame_Skip_Table.children["!ctktable"]
    Frame_Skip_Table_Var.configure(wraplength=440)
    Frame_Skip_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

# ------------- Events - Empty -------------#
def Settings_Events_Empty_Generaly(Frame: CTk|CTkFrame) -> CTkFrame:
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Action_Variable = StringVar(master=Frame, value=Activity_List[0])

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Empty Space coverage Evets", Additional_Text="These evets will be used according to coverage", Widget_size="Triple_size", Widget_Label_Tooltip="For emty space program use fill them by this setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")
    Subject_Text.pack(side="top", padx=10, pady=(0,5))

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)
    Project_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)
    Activity_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Coverage
    Coverage_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Coverage", Field_Type="Input_Normal") 
    Activity_Option_Var = Coverage_Text.children["!ctkframe3"].children["!ctkentry"]
    Activity_Option_Var.configure(placeholder_text="Add %")
    Coverage_Text.pack(side="top", padx=10, pady=(0,5))

    # Add Button
    Button_Empty_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Add.configure(text="Add", command = lambda:Add_Empty_Event())
    Button_Empty_Add.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Empty_Add, message="Add selected combination into the list")

    # Del Button
    Button_Empty_Del = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Empty_Del.configure(text="Del", command = lambda:Del_Empty_Event())
    Button_Empty_Del.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Empty_Del, message="Delete row from table based on input index.")

    # Empty Events table
    Skip_Event_General_list = [["Project", "Activity", "Description", "Coverage Percentage"]]
    Skip_Event_General_dict_rows = Skip_Event_General_dict.items()
    for Sub_Row in Skip_Event_General_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_General_list.append(list(Sub_dict.values()))

    Frame_Empty_General_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_General_list, Table_Columns=4, Table_Rows=len(Skip_Event_General_list))
    Frame_Empty_General_Table_Var = Frame_Empty_General_Table.children["!ctktable"]
    Frame_Empty_General_Table_Var.configure(wraplength=230)
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
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Evets Scheduler", Additional_Text="Shedule Periodical Events", Widget_size="Triple_size", Widget_Label_Tooltip="Simple TimeSheet Entry planner.")
    Frame_Body = Frame_Main.children["!ctkframe2"]
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")
    Subject_Text.pack(side="top", padx=10, pady=(0,5))

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)
    Project_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)
    Activity_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Start Time
    Start_Time_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Start Time", Field_Type="Input_Normal") 
    Start_Time_Text_Var = Start_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    Start_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")
    Start_Time_Text.pack(side="top", padx=10, pady=(0,5))

    # Field - End Time
    End_Time_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="End Time", Field_Type="Input_Normal") 
    End_Time_Text_Var = End_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    End_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")
    End_Time_Text.pack(side="top", padx=10, pady=(0,5))

    # Field - Week Days
    Week_Days_Label = Elements.Get_Text_Column_Header(Frame=Frame_Imput_Area)
    Week_Days_Label.configure(text="Week Days")
    Week_Days_Label.pack_propagate(flag=False)
    Week_Days_Label.pack(side="top", fill="none", expand=False, padx=10, pady=10)

    Week_Days_Frame = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column")
    Week_Days_Frame.configure(width=300)
    Week_Days_Frame.pack(side="top", fill="none", expand=False, padx=0, pady=0)

    Monday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Mon") 
    Monday_Check_Frame_Var = Monday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Monday_Check_Frame_Var.configure(variable=Mon_Var, text="")
    Monday_Check_Frame.pack(side="left", padx=5, pady=5)

    Tuesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Tue") 
    Tuesday_Check_Frame_Var = Tuesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Tuesday_Check_Frame_Var.configure(variable=Tue_Var, text="")
    Tuesday_Check_Frame.pack(side="left", padx=5, pady=5)

    Wednesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Wed") 
    Wednesday_Check_Frame_Var = Wednesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Wednesday_Check_Frame_Var.configure(variable=Wed_Var, text="")
    Wednesday_Check_Frame.pack(side="left", padx=5, pady=5)

    Thursday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Thu") 
    Thursday_Check_Frame_Var = Thursday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Thursday_Check_Frame_Var.configure(variable=Thu_Var, text="")
    Thursday_Check_Frame.pack(side="left", padx=5, pady=5)

    Friday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Fri") 
    Friday_Check_Frame_Var = Friday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Friday_Check_Frame_Var.configure(variable=Fri_Var, text="")
    Friday_Check_Frame.pack(side="left", padx=5, pady=5)

    Saturday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sat") 
    Saturday_Check_Frame_Var = Saturday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Saturday_Check_Frame_Var.configure(variable=Sat_Var, text="")
    Saturday_Check_Frame.pack(side="left", padx=5, pady=5)

    Sunday_Check_Frame = Elements_Groups.Get_Vertical_Field_Imput(Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sun") 
    Sunday_Check_Frame_Var = Sunday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Sunday_Check_Frame_Var.configure(variable=Sun_Var, text="")
    Sunday_Check_Frame.pack(side="left", padx=5, pady=5)

    # Add Button
    Button_Schedule_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Schedule_Add.configure(text="Add", command = lambda:Add_Schedule_Event())
    Button_Schedule_Add.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Schedule_Add, message="Add selected combination into the list")

    # Del Button
    Button_Schedule_Del = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_Schedule_Del.configure(text="Del", command = lambda:Del_Schedule_Event())
    Button_Schedule_Del.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_Schedule_Del, message="Delete row from table based on input index.")

    # Scheduled Events table
    Skip_Event_Schedule_list = [["Project", "Activity", "Description", "Day in week", "Start Time", "End Time"]]
    Skip_Event_Schedule_dict_rows = Skip_Event_Schedules_dict.items()
    for Sub_Row in Skip_Event_Schedule_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_Schedule_list.append(list(Sub_dict.values()))

    Frame_Empty_Schedules_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_Schedule_list, Table_Columns=6, Table_Rows=len(Skip_Event_Schedule_list))
    Frame_Empty_Schedules_Table_Var = Frame_Empty_Schedules_Table.children["!ctktable"]
    Frame_Empty_Schedules_Table_Var.configure(wraplength=150)
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
    Frame_Main.pack(side="top", padx=15, pady=15)

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Search Text", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")
    Subject_Text.pack(side="top", padx=10, pady=(0,5))

    # Field - Project
    Project_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(values=Project_List, variable=Project_Variable)
    Project_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Activity_List, variable=Action_Variable)
    Activity_Option.pack(side="top", padx=10, pady=(0,5))

    # Field - Location
    Activity_Option = Elements_Groups.Get_Single_Field_Imput(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Location", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(values=Location_List, variable=Location_Variable)
    Activity_Option.pack(side="top", padx=10, pady=(0,5))

    # Del Button
    Button_AutoFill_Del = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_AutoFill_Del.configure(text="Del", command = lambda:Del_AutoFill_Event())
    Button_AutoFill_Del.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_AutoFill_Del, message="Delete row from table based on input index.")

    # Add Button
    Button_AutoFill_Add = Elements.Get_Button(Frame=Frame_Imput_Area, Button_Size="Small")
    Button_AutoFill_Add.configure(text="Add", command = lambda:Add_AutoFill_Event())
    Button_AutoFill_Add.pack(side="right", padx=10, pady=(0,5))
    CTkToolTip(widget=Button_AutoFill_Add, message="Add selected combination into the list")

    # AutoFilling Table
    Skip_AutoFill_list = [["Find Text within subject", "Set Project", "Set Activity", "Set Location"]]
    Skip_AutoFill_dict_rows = Skip_AutoFill_dict.items()
    for Sub_Row in Skip_AutoFill_dict_rows:
        Skip_AutoFill_list.append(Sub_Row[1])

    Frame_AutoFiller_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_AutoFill_list, Table_Columns=4, Table_Rows=len(Skip_AutoFill_list))
    Frame_AutoFiller_Table_Var = Frame_AutoFiller_Table.children["!ctktable"]
    Frame_AutoFiller_Table_Var.configure(wraplength=230)
    Frame_AutoFiller_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    return Frame_Main