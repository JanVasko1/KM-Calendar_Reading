# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

# -------------------------------------------------------------------------------------------------------------------------------------------------- Set Defaults -------------------------------------------------------------------------------------------------------------------------------------------------- #
client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
Settings = Defaults_Lists.Load_Settings()
Configuration = Defaults_Lists.Load_Configuration() 

# Sharepoint
SP_Auth_Email = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
SP_Person_ID = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]

# Outlook
Outlook_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]

# -------------------------------------------------------------------------------------------------------------------------------------------------- Download Page Widgets -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Download_Sharepoint(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint - missing dates", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Timesheets for donwload process. \n - End Date Max Toda --> Date-To = Today \n - Simulate Report period --> Dates are selected according to Sharepoint.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Sharepoint = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Sharepoint_Radio_Var = Use_Sharepoint.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Sharepoint_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Sharepoint")

    # Field - User ID
    User_ID = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    User_ID_Text_Var = User_ID.children["!ctkframe3"].children["!ctkentry"]
    User_ID_Text_Var.configure(placeholder_text=SP_Person_ID)
    User_ID_Text_Var.configure(state="disabled")

    # Field - User Email
    Email = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=SP_Auth_Email)
    Email_Text_Var.configure(state="disabled")

    # Field - Password
    Password = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 

    # Field - Maximal Today date
    Max_Today_Date_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="End Date max Today", Field_Type="Input_CheckBox") 
    Max_Today_Date_Frame_Var = Max_Today_Date_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Max_Today_Date_Frame_Var.configure(text="")

    # Field - Get whole report Period
    Whole_Period_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Simulate report period", Field_Type="Input_CheckBox") 
    Whole_Period_Frame_Var = Whole_Period_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Whole_Period_Frame_Var.configure(text="")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Manual(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for downlaod process. Format YYYY-MM-DD")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Manual = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Manual_Radio_Var = Use_Manual.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Manual_Radio_Var.configure(text="", variable=Download_Date_Range_Source, value="Manual")

    # Field - User ID
    Date_From = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From / T", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text="Date From")

    # Field - User Email
    Date_To = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To / T", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text="Date To")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Exchange(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange Server", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Exchange = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Exchange_Radio_Var = Use_Exchange.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Exchange_Radio_Var.configure(text="", variable=Download_Data_Source, value="Exchange")

    # Field - User ID
    Email = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")

    # Field - Password
    Password = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Outlook(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Outlook Classic Client", Additional_Text="Must be updated befor download", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Windows installtion of Outlook Classic client.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Outlook = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton") 
    Use_Outlook_Radio_Var = Use_Outlook.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Outlook_Radio_Var.configure(text="", variable=Download_Data_Source, value="Outlook_Client")

    # Field - User ID
    Email = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Email_Text_Var = Email.children["!ctkframe3"].children["!ctkentry"]
    Email_Text_Var.configure(placeholder_text=Outlook_Email)
    Email_Text_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main