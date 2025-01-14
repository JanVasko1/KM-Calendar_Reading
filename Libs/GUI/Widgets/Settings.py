# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import pywinstyles
import customtkinter
from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, CTkToplevel, CTkOptionMenu, CTkButton, CTkCheckBox, CTkLabel
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox

from CTkColorPicker import *

# -------------------------------------------------------------------------------------------------------------------------------------------------- Set Defaults -------------------------------------------------------------------------------------------------------------------------------------------------- #
client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
Settings = Defaults_Lists.Load_Settings()
Configuration = Defaults_Lists.Load_Configuration() 

# Apperance
Theme_Actual = Configuration["Global_Apperance"]["Window"]["Theme"]
Theme_List = list(Configuration["Global_Apperance"]["Window"]["Theme_List"])
Win_Style_Actual = Configuration["Global_Apperance"]["Window"]["Style"]
Win_Style_List = list(Configuration["Global_Apperance"]["Window"]["Style_List"])
Accent_Color_Mode = Configuration["Global_Apperance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
Accent_Color_Mode_List = list(Configuration["Global_Apperance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
Accent_Color_Manual = Configuration["Global_Apperance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

Hover_Color_Mode = Configuration["Global_Apperance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
Hover_Color_Mode_List = list(Configuration["Global_Apperance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
Hover_Color_Manual = Configuration["Global_Apperance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

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
Vacation_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Search Text"]
Vacation_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["All_Day"]
Vacation_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Part_Day"]
Vacation_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Vacation_Option_List"]

# HomeOffice
HomeOffice_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Search Text"]
HomeOffice_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["All_Day"]
HomeOffice_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Part_Day"]
HomeOffice_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["HomeOffice_Option_List"]

# Lunch
Lunch_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Search Text"]
Lunch_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["All_Day"]
Lunch_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Part_Day"]
Lunch_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Lunch_Option_List"]

# Events
Skip_Events_list = Settings["Event_Handler"]["Events"]["Skip"]
Skip_Event_General_dict = Settings["Event_Handler"]["Events"]["Empty"]["General"]
Skip_Event_Schedules_dict = Settings["Event_Handler"]["Events"]["Empty"]["Scheduled"]
Skip_AutoFill_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]

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
Project_List = []
Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]
for key, value in Project_dict.items():
    Project_List.append(value["Project"])
Project_List.sort()

Activity_List1 = []
Activity_List2 = []
Activity_by_Type_dict = Settings["Event_Handler"]["Activity"]["Activity_by_Type_dict"]
Activity_All_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
Activity_All_List.insert(0, "") # Because there might be not filled one in Calendar
Activity_All_List.sort()
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

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Update_empty_information(Check_List: list):
    Check_List_len = len(Check_List)
    for Check_List_index in range(0, Check_List_len):
        Check_List_row = Check_List[Check_List_index]
        Check_List_row_len = len(Check_List_row)
        for Check_List_row_index in range(0, Check_List_row_len):
            Check_List_row_Element = Check_List_row[Check_List_row_index]
            if Check_List_row_Element == " ":
                Check_List[Check_List_index][Check_List_row_index] = ""
            else:
                pass
    return Check_List


def Retrive_Activity_based_on_Type(Project_Option_Var: CTkOptionMenu, Activity_Option_Var: CTkOptionMenu, Project_Variable: StringVar) -> None:
    try:
        Project_Variable.set(value=Project_Option_Var)
        # Get Selected Proejct and retrive Project Type of selected Project
        for key, value in Project_dict.items():
            Project = value["Project"]
            if Project == Project_Option_Var:
                Project_Type = value["Project_Type"]
                break
        for key, value in Activity_by_Type_dict.items():
            Activity_Type = value["Project_Type"]
            if Project_Type == Activity_Type:
                Activity_List = value["Activity"]
                Activity_List.sort()
                break
    except:
        Activity_List = [""]
    Activity_Option_Var.set(value="")
    Elements.Get_Option_Menu_Advance(attach=Activity_Option_Var, values=Activity_List, command=None)

# -------------------------------------------------------------------------- Tab Apperance --------------------------------------------------------------------------#
def Settings_Aperance_Theme(Frame: CTk|CTkFrame, window: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Apperance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        Theme_Variable.set(Theme_Frame_Var)
        customtkinter.set_appearance_mode(mode_string=Theme_Frame_Var)
        Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Theme"], Information=Theme_Frame_Var)

    def Apperance_Change_Win_Style(Win_Style_Selected: str, window: CTk|CTkFrame) -> None:
        Win_Style_Variable.set(Win_Style_Selected)
        # Base Windows style setup --> always keep normal before change
        pywinstyles.apply_style(window=window, style="normal")
        pywinstyles.apply_style(window=window, style=Win_Style_Selected)
        Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Style"], Information=Win_Style_Selected)

    # ------------------------- Main Functions -------------------------#
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Win_Style_Variable = StringVar(master=Frame, value=Win_Style_Actual)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="General Apperance", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="GEnerall apperance settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Apperance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var))

    # Field - Windows Style
    Win_Style_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Window Style", Field_Type="Input_OptionMenu") 
    Win_Style_Frame_Var = Win_Style_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Win_Style_Frame_Var.configure(variable=Win_Style_Variable)
    Elements.Get_Option_Menu_Advance(attach=Win_Style_Frame_Var, values=Win_Style_List, command= lambda Win_Style_Selected: Apperance_Change_Win_Style(Win_Style_Selected=Win_Style_Selected, window=window))

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Aperance_Color_Pallete(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Settings_Disabeling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        Variable.set(value=Selected_Value)
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            CTkMessagebox(title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1)

    def Apperance_Pick_Manual_Color(Color_Manual_Frame_Var: CTkEntry, Helper: str) -> None:
        def Quit_Save(Helper: str):
            Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Apperance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Colorpicker_Frame.get())
            Collor_Picker_window.destroy()
            
        Collor_Picker_window = CTkToplevel()
        Collor_Picker_window.configure(fg_color="#000001")
        Collor_Picker_window.title("Collor Picker")
        Collor_Picker_window.geometry("295x240")
        Collor_Picker_window.bind(sequence="<Escape>", func=lambda evet: Quit_Save(Helper=Helper))
        Collor_Picker_window.overrideredirect(boolean=True)
        Collor_Picker_window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Collor_Picker_window.resizable(width=False, height=False)

        # Rounded corners 
        Collor_Picker_window.config(background="#000001")
        Collor_Picker_window.attributes("-transparentcolor", "#000001")

        Colorpicker_Frame = Elements.Get_Color_Picker(Frame=Collor_Picker_window, Color_Manual_Frame_Var=Color_Manual_Frame_Var)

        #? Build look of Widget --> must be before inset
        Colorpicker_Frame.pack(padx=0, pady=0) 

    # ------------------------- Main Functions -------------------------#
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Color Palletes", Additional_Text="Applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Input_Normal") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual)

    # Button - Collor Picker
    Accent_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Accent_Color_Picker_Button_Var = Accent_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Accent_Color_Picker_Button_Var.configure(text="Accent Color Picker", command = lambda :Apperance_Pick_Manual_Color(Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent"))
    Elements.Get_ToolTip(widget=Accent_Color_Picker_Button_Var, message="Select manualy Accent collor.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabeling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"))
    Settings_Disabeling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Input_Normal") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual)

    # Button - Collor Picker
    Hover_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Hover_Color_Picker_Button_Var = Hover_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Hover_Color_Picker_Button_Var.configure(text="Hover Color Picker", command = lambda:Apperance_Pick_Manual_Color(Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover"))
    Elements.Get_ToolTip(widget=Hover_Color_Picker_Button_Var, message="Select manualy Hover collor.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabeling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"))
    Settings_Disabeling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")


    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
    


# -------------------------------------------------------------------------- Tab GEneral --------------------------------------------------------------------------#
def Settings_General_Sharepoint(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    SP_Name_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Name", Field_Type="Input_Normal") 
    SP_Name_Frame_Var = SP_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Name_Frame_Var.configure(placeholder_text=SP_Person_Name)

    # Field - User ID
    SP_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal")
    SP_User_ID_Frame_Var = SP_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_User_ID_Frame_Var.configure(placeholder_text=SP_Person_ID)

    # Field - Path to Sharepoint
    SP_Link_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Sharepoin Address", Field_Type="Input_Normal")
    SP_Link_Frame_Var = SP_Link_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Link_Frame_Var.configure(placeholder_text=SP_Link)

    # Field - File Name 
    SP_File_Name_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="File Name", Field_Type="Input_Normal")
    SP_File_Name_Frame_Var = SP_File_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_File_Name_Frame_Var.configure(placeholder_text=SP_File_Name)
    SP_File_Name_Frame_Var.configure(state="disabled")

    # Field - Auth Email
    SP_Auth_Email_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Auth Email", Field_Type="Input_Normal")
    SP_Auth_Email_Frame_Var = SP_Auth_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Auth_Email_Frame_Var.configure(placeholder_text=SP_Auth_Email)

    # Field - Auth Address
    SP_Auth_Address_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Auth Address", Field_Type="Input_Normal")
    SP_Auth_Address_Frame_Var = SP_Auth_Address_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Auth_Address_Frame_Var.configure(placeholder_text=SP_Auth_Address)
    SP_Auth_Address_Frame_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Exchange(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Exchange_ReNew_Secret() -> None:
        print("Exchange_ReNew_Secret")
        #! Dodělat --> Zobrazí popu form a nechá vyplnit nový SEcret ID a pouze uloží do DB
        pass

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Exchange Server related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    EX_Client_ID_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client ID", Field_Type="Input_Normal") 
    EX_Client_ID_Frame_Var = EX_Client_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Client_ID_Frame_Var.configure(placeholder_text=client_id)
    EX_Client_ID_Frame_Var.configure(state="disabled")

    # Field - User ID
    Ex_Client_Secret_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Secret", Field_Type="Input_Normal")
    Ex_Client_Secret_Frame_Var = Ex_Client_Secret_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Client_Secret_Frame_Var.configure(placeholder_text=client_secret)
    Ex_Client_Secret_Frame_Var.configure(state="disabled")

    # Field - Path to Sharepoint
    EX_Tenant_ID_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tenant ID", Field_Type="Input_Normal")
    EX_Tenant_ID_Frame_Var = EX_Tenant_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Tenant_ID_Frame_Var.configure(placeholder_text=tenant_id)
    EX_Tenant_ID_Frame_Var.configure(state="disabled")

    # Update Secret ID Button
    Button_Update_Secret = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Button_Update_Secret_Var = Button_Update_Secret.children["!ctkframe"].children["!ctkbutton"]
    Button_Update_Secret_Var.configure(text="Re-new Secret", command = lambda:Exchange_ReNew_Secret())
    Elements.Get_ToolTip(widget=Button_Update_Secret_Var, message="Update Secret ID.", ToolTip_Size="Normal")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Outlook(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Outlook", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Outlook Client related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    Outlook_Email_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal") 
    Outlook_Email_Frame_Var = Outlook_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    Outlook_Email_Frame_Var.configure(placeholder_text=Outlook_Email)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Formats(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Formats", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Dates formats used in program - non-changable.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Name
    Date_From = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date", Field_Type="Input_Normal") 
    Date_From_Text_Var = Date_From.children["!ctkframe3"].children["!ctkentry"]
    Date_From_Text_Var.configure(placeholder_text=Format_Date)
    Date_From_Text_Var.configure(state="disabled")

    # Field - User ID
    Date_To = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Time", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_Time)
    Date_To_Text_Var.configure(state="disabled")

    # Field - Email
    Date_To = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Exchange DateTime", Field_Type="Input_Normal")
    Date_To_Text_Var = Date_To.children["!ctkframe3"].children["!ctkentry"]
    Date_To_Text_Var.configure(placeholder_text=Format_SP_DateTime)
    Date_To_Text_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Parralel_events(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    Divide_Method_Variable = StringVar(master=Frame, value=Divide_Method)
    Start_Method_Variable = StringVar(master=Frame, value=Start_Method)
    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Parralel Events Handler", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definitions of behavior of processing Envents when program found that they are parrallel.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Divide Method
    Divide_Method_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Divide Method", Field_Type="Input_OptionMenu") 
    Divide_Method_Frame_Var = Divide_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Divide_Method_Frame_Var.configure(variable=Divide_Method_Variable)
    Elements.Get_Option_Menu_Advance(attach=Divide_Method_Frame_Var, values=Divide_Method_List, command=None)

    # Field - Start Method
    Start_Method_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Start Method", Field_Type="Input_OptionMenu") 
    Start_Method_Frame_Var = Start_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Start_Method_Frame_Var.configure(variable=Start_Method_Variable)
    Elements.Get_Option_Menu_Advance(attach=Start_Method_Frame_Var, values=Start_Method_List, command=None)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Join_events(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    Join_Free_Variable = StringVar(master=Frame, value=Join_Free)
    Join_Tentative_Variable = StringVar(master=Frame, value=Join_Tentative)
    Join_Busy_Variable = StringVar(master=Frame, value=Join_Busy)
    Join_OutOfOffice_Variable = StringVar(master=Frame, value=Join_OutOfOffice)
    Join_Work_Else_Variable = StringVar(master=Frame, value=Join_Work_Else)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Joining Events", Additional_Text="Under Construction", Widget_size="Single_size", Widget_Label_Tooltip="Joining Events belonging to same Visibility group.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Join Free Events
    Join_Free_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Free", Field_Type="Input_OptionMenu") 
    Join_Free_Frame_Var = Join_Free_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Free_Frame_Var.configure(variable=Join_Free_Variable)
    Elements.Get_Option_Menu_Advance(attach=Join_Free_Frame_Var, values=Join_Methods_List, command=None)

    # Field - Join Tentative Events
    Join_Tentative_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Tentative", Field_Type="Input_OptionMenu") 
    Join_Tentative_Frame_Var = Join_Tentative_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Tentative_Frame_Var.configure(variable=Join_Tentative_Variable)
    Elements.Get_Option_Menu_Advance(attach=Join_Tentative_Frame_Var, values=Join_Methods_List, command=None)

    # Field - Join Busy Events
    Join_Busy_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Busy", Field_Type="Input_OptionMenu") 
    Join_Busy_Frame_Var = Join_Busy_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Busy_Frame_Var.configure(variable=Join_Busy_Variable)
    Elements.Get_Option_Menu_Advance(attach=Join_Busy_Frame_Var, values=Join_Methods_List, command=None)

    # Field - Join Out of Office Events
    Join_OutOfOffice_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Out of Office", Field_Type="Input_OptionMenu") 
    Join_OutOfOffice_Frame_Var = Join_OutOfOffice_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_OutOfOffice_Frame_Var.configure(variable=Join_OutOfOffice_Variable)
    Elements.Get_Option_Menu_Advance(attach=Join_OutOfOffice_Frame_Var, values=Join_Methods_List, command=None)

    # Field - Join Working ElseWhere Events
    Join_Work_ElseWhere_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Events - Working ElseWhere", Field_Type="Input_OptionMenu") 
    Join_Work_ElseWhere_Frame_Var = Join_Work_ElseWhere_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Work_ElseWhere_Frame_Var.configure(variable=Join_Work_Else_Variable)
    Elements.Get_Option_Menu_Advance(attach=Join_Work_ElseWhere_Frame_Var, values=Join_Methods_List, command=None)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Calendar --------------------------------------------------------------------------#
def Settings_Calendar_Working_Hours(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Calendar - My own calendar", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Setup of my general working hours I usually have. Used for projected Utilization.")
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

    return Frame_Main



def Settings_Calendar_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
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

    return Frame_Main



def Settings_Calendar_Start_End_Time(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Workday - Start / End Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Events Subject which defines Start and End time of each day in Calendar.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Work - Start
    Start_Event = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - Start", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text=Start_Event_json)

    # Field - Work - End
    End_Event = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - End", Field_Type="Input_Normal") 
    End_Event_Var = End_Event.children["!ctkframe3"].children["!ctkentry"]
    End_Event_Var.configure(placeholder_text=End_Event_json)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Events - General --------------------------------------------------------------------------#
def Settings_Events_General_Lunch(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    Lunch_All_Variable = StringVar(master=Frame, value=Lunch_All_Day)
    Lunch_Part_Variable = StringVar(master=Frame, value=Lunch_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Lunch", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Lunch brake -> always skip it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_Lunch = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Lunch_Var = Search_Text_Lunch.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Lunch_Var.configure(placeholder_text=Lunch_Search_Text)

    # Field - All Day
    All_Day_Lunch = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Lunch_Var = All_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Lunch_Var.configure(variable=Lunch_All_Variable)
    Elements.Get_Option_Menu_Advance(attach=All_Day_Lunch_Var, values=Lunch_Day_Option_List, command=None)

    # Field - Part Day
    Part_Day_Lunch = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Lunch_Var = Part_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Lunch_Var.configure(variable=Lunch_Part_Variable)
    Elements.Get_Option_Menu_Advance(attach=Part_Day_Lunch_Var, values=Lunch_Day_Option_List, command=None)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_Vacation(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    Vacation_All_Variable = StringVar(master=Frame, value=Vacation_All_Day)
    Vacation_Part_Variable = StringVar(master=Frame, value=Vacation_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - Vacation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Vacation")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_Vacation = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Vacation_Var = Search_Text_Vacation.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Vacation_Var.configure(placeholder_text=Vacation_Search_Text)

    # Field - All Day
    All_Day_Vacation = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Vacation_Var = All_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Vacation_Var.configure(variable=Vacation_All_Variable)
    Elements.Get_Option_Menu_Advance(attach=All_Day_Vacation_Var, values=Vacation_Day_Option_List, command=None)

    # Field - Part Day
    Part_Day_Vacation = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Vacation_Var = Part_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Vacation_Var.configure(variable=Vacation_Part_Variable)
    Elements.Get_Option_Menu_Advance(attach=Part_Day_Vacation_Var, values=Vacation_Day_Option_List, command=None)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_HomeOffice(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    HomeOffice_All_Variable = StringVar(master=Frame, value=HomeOffice_All_Day)
    HomeOffice_Part_Variable = StringVar(master=Frame, value=HomeOffice_Part_Day)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Special - HomeOffice", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of HomeOffice")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Seach Text
    Search_Text_HomeOffice = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_HomeOffice_Var = Search_Text_HomeOffice.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_HomeOffice_Var.configure(placeholder_text=HomeOffice_Search_Text)

    # Field - All Day
    All_Day_HomeOffice = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_HomeOffice_Var = All_Day_HomeOffice.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_HomeOffice_Var.configure(variable=HomeOffice_All_Variable)
    Elements.Get_Option_Menu_Advance(attach=All_Day_HomeOffice_Var, values=HomeOffice_Day_Option_List, command=None)

    # Field - Part Day
    Part_Day = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_HomeOffice_Var = Part_Day.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_HomeOffice_Var.configure(variable=HomeOffice_Part_Variable)
    Elements.Get_Option_Menu_Advance(attach=Part_Day_HomeOffice_Var, values=HomeOffice_Day_Option_List, command=None)

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_Skip(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Add_Skip_Event(Header_List: list, Subject_Text_Text_Var: CTkEntry, Frame_Skip_Table_Var: CTkTable) -> None:
        Add_flag = True
        Add_text = Subject_Text_Text_Var.get()

        Check_List = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
        Header_List = Header_List[0]

        # Not To add same line
        for Skip_Event in Check_List:
            if Skip_Event == Add_text:
                Add_flag = False
            else:
                pass

        if Add_flag == True:
            if Add_text != "":
                Frame_Skip_Table_Var.add_row(values=[Add_text])
            else:
                CTkMessagebox(title="Error", message=f"Subject is empty please fill it first.", icon="cancel", fade_in_duration=1)

            # Save to Settings.json
            Skip_Events = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
            Skip_Events.remove(Header_List)
            Skip_Events.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip"], Information=Skip_Events)
        else:
            CTkMessagebox(title="Error", message=f"Subject is already within list of skip Events.", icon="cancel", fade_in_duration=1)

    def Del_Skip_Event_one(Subject_Text_Text_Var: CTkEntry, Frame_Skip_Table_Var: CTkTable) -> None:
        # Find Index
        Deleted_flag = False
        Search_text = Subject_Text_Text_Var.get()
        if Search_text != "Skip Events":
            Table_len = len(Frame_Skip_Table_Var.values)
            for Table_index in range(0, Table_len):
                Table_row_value = Frame_Skip_Table_Var.values[Table_index][0]
                if Search_text == Table_row_value:
                    Frame_Skip_Table_Var.delete_row(index=Table_index)
                    Deleted_flag = True
                    break
                else:
                    pass
            if Deleted_flag == False:
                CTkMessagebox(title="Error", message=f"Subject not found, pelase check spelling.", icon="cancel", fade_in_duration=1)
            else:
                pass
            Skip_Events = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
            Skip_Events.remove("Skip Events")
            Skip_Events.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip"], Information=Skip_Events)
        else:
            CTkMessagebox(title="Error", message=f"Header cannot be deleted.", icon="cancel", fade_in_duration=1)

    def Del_Skip_Event_all(Frame_Skip_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Skip_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Skip_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip"], Information=[])

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Skip Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of text be skipped as TimeSheet Entry in the case that part of text is found in Event Subject.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Subject", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Skip Events Table
    Header_List = ["Skip Events"]
    Show_Skip_Events_list = [Header_List]
    for skip_Subject in Skip_Events_list:
        Show_Skip_Events_list.append([skip_Subject])
        
    Frame_Skip_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Body, Table_Size="Single_size", Table_Values=Show_Skip_Events_list, Table_Columns=1, Table_Rows=len(Skip_Events_list) + 1)
    Frame_Skip_Table_Var = Frame_Skip_Table.children["!ctktable"]
    Frame_Skip_Table_Var.configure(wraplength=440)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Skip_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Skip_Add_Var.configure(text="Add", command = lambda:Add_Skip_Event(Header_List=Header_List, Subject_Text_Text_Var=Subject_Text_Text_Var, Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(widget=Button_Skip_Add_Var, message="Add selected subejct to skip list", ToolTip_Size="Normal")

    Button_Skip_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Skip_Del_One_Var.configure(text="Del", command = lambda:Del_Skip_Event_one(Subject_Text_Text_Var=Subject_Text_Text_Var, Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(widget=Button_Skip_Del_One_Var, message="Delete row from table based on input text.", ToolTip_Size="Normal")

    Button_Skip_Del_all_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Skip_Del_all_Var.configure(text="Del all", command = lambda:Del_Skip_Event_all(Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(widget=Button_Skip_Del_all_Var, message="Delete all rows from table.", ToolTip_Size="Normal")


    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Events - Empty --------------------------------------------------------------------------#
def Settings_Events_Empty_Generaly(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Add_Empty_Event(Header_List: list, Frame_Empty_General_Table_Var: CTkTable, Subject_Text_Text_Var: CTkEntry, Project_Option_Var1: CTkOptionMenu, Activity_Option_Var1: CTkOptionMenu, Coverage_Text_Var: CTkEntry) -> None:
        Add_flag = True
        # Load single values
        Add_Description = Subject_Text_Text_Var.get()
        Add_Project = Project_Option_Var1.get()
        Add_Activity = Activity_Option_Var1.get()
        Add_Coverage = Coverage_Text_Var.get()

        Check_List = Frame_Empty_General_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)

        # Values checkers
        try:
            Add_Coverage = int(Add_Coverage)
            if Add_Coverage > 0 and Add_Coverage <= 100:
                pass
            else:
                Add_flag = False
                CTkMessagebox(title="Error", message=f"Coverage must be between 0 - 100, please check it.", icon="cancel", fade_in_duration=1) 
        except:
            Add_flag = False
            CTkMessagebox(title="Error", message=f"Coverage is not whole number, check it.", icon="cancel", fade_in_duration=1)

        # Not To add same line
        if Add_flag == True:
            Add_row = [Add_Project, Add_Activity, Add_Description, Add_Coverage]
            for Empty_Event in Check_List:
                if Empty_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"Rule already exists with Fill Empty.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_flag == True:
            Frame_Empty_General_Table_Var.add_row(values=Add_row)
            
            # Save to Settings.json
            Empty_General_Events = Frame_Empty_General_Table_Var.values
            Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]

            General_dict = {}
            Counter = 0
            for Empty_General_Events_row in Empty_General_Events:
                Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                General_dict[Counter] = Empty_General_Events_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)
        else:
            pass
    
    def Del_Empty_Event_One(Header_List: list, Frame_Empty_General_Table_Var: CTkTable) -> None:
        def Delete_One_Confirm(Frame_Empty_General_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_Empty_General_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Empty_General_Events = Frame_Empty_General_Table_Var.values
            Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]

            General_dict = {}
            Counter = 0
            for Empty_General_Events_row in Empty_General_Events:
                Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                General_dict[Counter] = Empty_General_Events_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)
            Delete_One_Close()

        def Delete_One_Close() -> None:
            Delete_One_Window.destroy()

        def Update_Labels_Texts(LineNo_Option_Var: int, Frame_Empty_General_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, Coverage_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=LineNo_Option_Var)
            Selected_Project = Frame_Empty_General_Table_Var.get(row=LineNo_Option_Var, column=0)
            Selected_Activity = Frame_Empty_General_Table_Var.get(row=LineNo_Option_Var, column=1)
            Selected_Description = Frame_Empty_General_Table_Var.get(row=LineNo_Option_Var, column=2)
            Selected_Coverage = Frame_Empty_General_Table_Var.get(row=LineNo_Option_Var, column=3)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            Coverage_Label_Var.configure(text=Selected_Coverage)

        # callculat number of lines in table
        Empty_General_Events = Frame_Empty_General_Table_Var.values
        Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
        Lines_No = len(Empty_General_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_One_Window = CTkToplevel()
        Delete_One_Window.configure(fg_color="#000001")
        Delete_One_Window.title("Collor Picker")
        Delete_One_Window.geometry(f"510x260")
        Delete_One_Window.bind(sequence="<Escape>", func=lambda evet: Delete_One_Window.destroy())
        Delete_One_Window.overrideredirect(boolean=True)
        Delete_One_Window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Delete_One_Window.resizable(width=False, height=False)

        # Rounded corners 
        Delete_One_Window.config(background="#000001")
        Delete_One_Window.attributes("-transparentcolor", "#000001")

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Delete_One_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=2))
        Coverage_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Coverage") 
        Coverage_Label_Var = Coverage_Label.children["!ctkframe3"].children["!ctklabel"]
        Coverage_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=3))

        Elements.Get_Option_Menu_Advance(attach=LineNo_Option_Var, values=Lines_list, command= lambda LineNo_Option_Var: Update_Labels_Texts(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, LineNo_Option_Var=LineNo_Option_Var, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Coverage_Label_Var=Coverage_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_One_Confirm(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_One_Close())
        Elements.Get_ToolTip(widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_Empty_Event_All(Frame_Empty_General_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_General_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_General_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information={})

    def Recalculate_Empty_Event(Header_List: list, Frame_Empty_General_Table_Var: CTkTable) -> None:
        def Recalculation_Confirm(Frame_Body: CTkFrame, Lines_No: int) -> None:
            Add_flag = True
            New_Values_list = []
            for i in range(0, Lines_No + 1):
                if i == 0:
                    i = ""
                elif i == 1:
                    continue
                else:
                    pass
                Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe5"].children["!ctkentry"]
                Value = Value_CTkEntry.get()
                New_Values_list.append(Value)

            # Check that all are integers
            try:

                New_Values_list = [int(x) for x in New_Values_list]
            except: 
                Add_flag = False
                CTkMessagebox(title="Error", message=f"Not everything is Integer. 1 - 100 without decimal.", icon="cancel", fade_in_duration=1)

            # Check if equal 100
            if Add_flag == True:
                Values_sum = sum(New_Values_list)
                if Values_sum == 100:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"Sum of all lines not equal 100, pelase check.", icon="cancel", fade_in_duration=1)
            else:
                pass

            if Add_flag == True:
                for i in range(1, Lines_No + 1):
                    Frame_Empty_General_Table_Var.insert(row=i, column=3, value=New_Values_list[i - 1])

                # Save to Settings.json
                Empty_General_Events = Frame_Empty_General_Table_Var.values
                Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]

                General_dict = {}
                Counter = 0
                for Empty_General_Events_row in Empty_General_Events:
                    Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                    General_dict[Counter] = Empty_General_Events_row_dict
                    Counter += 1
                Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)

                Recalculation_Reject()
            else:
                pass

        def Recalculation_Reject() -> None:
            Recalculate_window.destroy()

        # callculat number of lines in table
        Empty_General_Events = Frame_Empty_General_Table_Var.values
        Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
        Lines_No = len(Empty_General_Events)

        Recalculate_window_height = (Lines_No * 40) + 100

        Recalculate_window = CTkToplevel()
        Recalculate_window.configure(fg_color="#000001")
        Recalculate_window.title("Collor Picker")
        Recalculate_window.geometry(f"510x{Recalculate_window_height}")
        Recalculate_window.bind(sequence="<Escape>", func=lambda evet: Recalculate_window.destroy())
        Recalculate_window.overrideredirect(boolean=True)
        Recalculate_window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Recalculate_window.resizable(width=False, height=False)

        # Rounded corners 
        Recalculate_window.config(background="#000001")
        Recalculate_window.attributes("-transparentcolor", "#000001")

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Recalculate_window, Name="Recalculate coverage", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Helps to recalculate Coverage percentage so sum is equal 100")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        for line in range(0, Lines_No):
            # Field - Monday
            Fields_Frame = Elements_Groups.Get_Double_Field_Imput(Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label=f"Line {line}") 
            Var1 = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
            Var1.configure(placeholder_text=Empty_General_Events[line][3])
            Var1.configure(state="disabled")

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Recalculation_Confirm(Frame_Body=Frame_Body, Lines_No=Lines_No))
        Elements.Get_ToolTip(widget=Button_Confirm_Var, message="Confirm coverage change.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Recalculation_Reject())
        Elements.Get_ToolTip(widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    # ------------------------- Main Functions -------------------------#
    Header_List = ["Project", "Activity", "Description", "Coverage Percentage"]
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Empty Space coverage Evets", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="For emty space (between Events in calendar) program use fill them by this setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    # Empty Events table
    Skip_Event_General_list = [Header_List]
    Skip_Event_General_dict_rows = Skip_Event_General_dict.items()
    for Sub_Row in Skip_Event_General_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_General_list.append(list(Sub_dict.values()))

    Frame_Empty_General_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_General_list, Table_Columns=4, Table_Rows=len(Skip_Event_General_list))
    Frame_Empty_General_Table_Var = Frame_Empty_General_Table.children["!ctktable"]
    Frame_Empty_General_Table_Var.configure(wraplength=230)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var1 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var1.configure(variable=Project_Variable)

    # Field - Activity --> placed before project because of variable to be used
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var1 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var1.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(attach=Project_Option_Var1, values=Project_List, command = lambda Project_Option_Var1: Retrive_Activity_based_on_Type(Project_Option_Var=Project_Option_Var1, Activity_Option_Var=Activity_Option_Var1, Project_Variable=Project_Variable))
    Elements.Get_Option_Menu_Advance(attach=Activity_Option_Var1, values=[], command=None)

    # Field - Coverage
    Coverage_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Coverage", Field_Type="Input_Normal") 
    Coverage_Text_Var = Coverage_Text.children["!ctkframe3"].children["!ctkentry"]
    Coverage_Text_Var.configure(placeholder_text="Add %")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Buttons_count=4, Button_Size="Small") 
    Button_Empty_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Empty_Add_Var.configure(text="Add", command = lambda:Add_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var1=Project_Option_Var1, Activity_Option_Var1=Activity_Option_Var1, Coverage_Text_Var=Coverage_Text_Var))
    Elements.Get_ToolTip(widget=Button_Empty_Add_Var, message="Add selected subejct to skip list", ToolTip_Size="Normal")

    Button_Empty_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Empty_Del_One_Var.configure(text="Del", command = lambda:Del_Empty_Event_One(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(widget=Button_Empty_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_Empty_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Empty_Del_All_Var.configure(text="Del all", command = lambda:Del_Empty_Event_All(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(widget=Button_Empty_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    Button_Empty_Recal_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Empty_Recal_Var.configure(text="Recalculate", command = lambda:Recalculate_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(widget=Button_Empty_Recal_Var, message="Recalculate coverage for all lines.", ToolTip_Size="Normal")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    return Frame_Main



def Settings_Events_Empt_Schedule(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Get_Selected_Day_Week(Monday_Check_Frame_Var: CTkCheckBox, Tuesday_Check_Frame_Var: CTkCheckBox, Wednesday_Check_Frame_Var: CTkCheckBox, Thursday_Check_Frame_Var: CTkCheckBox, Friday_Check_Frame_Var: CTkCheckBox, Saturday_Check_Frame_Var: CTkCheckBox, Sunday_Check_Frame_Var: CTkCheckBox) -> list:
        Add_Monday = Monday_Check_Frame_Var.get()
        Add_Tuesday = Tuesday_Check_Frame_Var.get()
        Add_Wednesday = Wednesday_Check_Frame_Var.get()
        Add_Thursday = Thursday_Check_Frame_Var.get()
        Add_Friday = Friday_Check_Frame_Var.get()
        Add_Saturday = Saturday_Check_Frame_Var.get()
        Add_Sunday = Sunday_Check_Frame_Var.get()

        Collect_list = [Add_Monday, Add_Tuesday, Add_Wednesday, Add_Thursday, Add_Friday, Add_Saturday, Add_Sunday]
        Add_Day_of_Week = []
        Week_Day = 1
        for day in Collect_list:
            if day == 1:
                Add_Day_of_Week.append(Week_Day)
            else:
                pass
            Week_Day += 1
        return Add_Day_of_Week

    def Add_Schedule_Event(Header_List: list, Frame_Empty_Schedules_Table_Var: CTkTable, Subject_Text_Text_Var: CTkEntry, Project_Option_Var2: CTkOptionMenu, Activity_Option_Var2: CTkOptionMenu, Start_Time_Text_Var: CTkEntry, End_Time_Text_Var: CTkEntry, Monday_Check_Frame_Var: CTkCheckBox, Tuesday_Check_Frame_Var: CTkCheckBox, Wednesday_Check_Frame_Var: CTkCheckBox, Thursday_Check_Frame_Var: CTkCheckBox, Friday_Check_Frame_Var: CTkCheckBox, Saturday_Check_Frame_Var: CTkCheckBox, Sunday_Check_Frame_Var: CTkCheckBox) -> None:
        from datetime import datetime
        Add_flag = True
        # Load single values
        Add_Description = Subject_Text_Text_Var.get()
        Add_Project = Project_Option_Var2.get()
        Add_Activity = Activity_Option_Var2.get()
        Add_Start_Time = Start_Time_Text_Var.get()
        Add_End_Time = End_Time_Text_Var.get()
        Add_Day_of_Week = Get_Selected_Day_Week(Monday_Check_Frame_Var=Monday_Check_Frame_Var, Tuesday_Check_Frame_Var=Tuesday_Check_Frame_Var, Wednesday_Check_Frame_Var=Wednesday_Check_Frame_Var, Thursday_Check_Frame_Var=Thursday_Check_Frame_Var, Friday_Check_Frame_Var=Friday_Check_Frame_Var, Saturday_Check_Frame_Var=Saturday_Check_Frame_Var, Sunday_Check_Frame_Var=Sunday_Check_Frame_Var)

        Check_List = Frame_Empty_Schedules_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)
        Add_row = [Add_Project, Add_Activity, Add_Description, Add_Day_of_Week, Add_Start_Time, Add_End_Time]

        # Values checkers
        # Not empty calendar
        if len(Add_Day_of_Week) != 0:
            pass
        else:
            Add_flag = False
            CTkMessagebox(title="Error", message=f"You didnt select any day of week, pelase update.", icon="cancel", fade_in_duration=1)

        # Time Checkers
        if Add_flag == True:
            try:
                Add_Start_Time_dt = datetime.strptime(Add_Start_Time, Format_Time)
                Add_End_Time_dt = datetime.strptime(Add_End_Time, Format_Time)

                if Add_End_Time_dt > Add_Start_Time_dt:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"End Time is before/equal to Start Time, pelase correct", icon="cancel", fade_in_duration=1)
            except:
                Add_flag = False
                CTkMessagebox(title="Error", message=f"One of the time is not actually time, please correct", icon="cancel", fade_in_duration=1)
        else:
            pass

        # Not To add same line
        if Add_flag == True:
            for Schedule_Event in Check_List:
                if Schedule_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"Rule already exists with Fill Empty.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_flag == True:
            Frame_Empty_Schedules_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Schedule_Events = Frame_Empty_Schedules_Table_Var.values
            Schedule_Events = [i for i in Schedule_Events if i != Header_List]

            Schedule_dict = {}
            Counter = 0
            for Schedule_Events_row in Schedule_Events:
                Schedule_Events_row_dict = dict(zip(Header_List, Schedule_Events_row))
                Schedule_dict[Counter] = Schedule_Events_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information=Schedule_dict)
        else:
            pass

    def Del_Schedule_Event_One(Header_List: list, Frame_Empty_Schedules_Table_Var: CTkTable) -> None:
        def Delete_Schedule_Confirm(Frame_Empty_Schedules_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_Empty_Schedules_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Empty_Scheduled_Events = Frame_Empty_Schedules_Table_Var.values
            Empty_Scheduled_Events = [i for i in Empty_Scheduled_Events if i != Header_List]

            Scheduled_dict = {}
            Counter = 0
            for Empty_Scheduled_Events_row in Empty_Scheduled_Events:
                Empty_Scheduled_Events_row_dict = dict(zip(Header_List, Empty_Scheduled_Events_row))
                Scheduled_dict[Counter] = Empty_Scheduled_Events_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information=Scheduled_dict)
            Delete_Schedule_Close()

        def Delete_Schedule_Close() -> None:
            Delete_Scheduled_Window.destroy()

        def Update_Labels_Texts(LineNo_Option_Var: int, Frame_Empty_Schedules_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, WeekDays_Label_Var: CTkLabel, Start_Label_Var: CTkLabel, End_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=LineNo_Option_Var)
            Selected_Project = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=0)
            Selected_Activity = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=1)
            Selected_Description = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=2)
            Selected_WeekDays = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=3)
            Selected_Start = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=4)
            Selected_End = Frame_Empty_Schedules_Table_Var.get(row=LineNo_Option_Var, column=5)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            WeekDays_Label_Var.configure(text=Selected_WeekDays)
            Start_Label_Var.configure(text=Selected_Start)
            End_Label_Var.configure(text=Selected_End)

        # callculat number of lines in table
        Empty_Scheduled_Events = Frame_Empty_Schedules_Table_Var.values
        Empty_Scheduled_Events = [i for i in Empty_Scheduled_Events if i != Header_List]
        Lines_No = len(Empty_Scheduled_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_Scheduled_Window = CTkToplevel()
        Delete_Scheduled_Window.configure(fg_color="#000001")
        Delete_Scheduled_Window.title("Collor Picker")
        Delete_Scheduled_Window.geometry(f"510x400")
        Delete_Scheduled_Window.bind(sequence="<Escape>", func=lambda evet: Delete_Scheduled_Window.destroy())
        Delete_Scheduled_Window.overrideredirect(boolean=True)
        Delete_Scheduled_Window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Delete_Scheduled_Window.resizable(width=False, height=False)

        # Rounded corners 
        Delete_Scheduled_Window.config(background="#000001")
        Delete_Scheduled_Window.attributes("-transparentcolor", "#000001")

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Delete_Scheduled_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=2))
        WeekDays_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Day of Week") 
        WeekDays_Label_Var = WeekDays_Label.children["!ctkframe3"].children["!ctklabel"]
        WeekDays_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=3))
        Start_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Start") 
        Start_Label_Var = Start_Label.children["!ctkframe3"].children["!ctklabel"]
        Start_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=4))
        End_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="End") 
        End_Label_Var = End_Label.children["!ctkframe3"].children["!ctklabel"]
        End_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=5))

        Elements.Get_Option_Menu_Advance(attach=LineNo_Option_Var, values=Lines_list, command= lambda LineNo_Option_Var: Update_Labels_Texts(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, LineNo_Option_Var=LineNo_Option_Var, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, WeekDays_Label_Var=WeekDays_Label_Var, Start_Label_Var=Start_Label_Var, End_Label_Var=End_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Schedule_Confirm(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Schedule_Close())
        Elements.Get_ToolTip(widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_Schedules_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_Schedules_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information={})

    # ------------------------- Main Functions -------------------------#
    Header_List = ["Project", "Activity", "Description", "Day of Week", "Start", "End"]
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])

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

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    # Scheduled Events table
    Skip_Event_Schedule_list = [Header_List]
    Skip_Event_Schedule_dict_rows = Skip_Event_Schedules_dict.items()
    for Sub_Row in Skip_Event_Schedule_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_Schedule_list.append(list(Sub_dict.values()))

    Frame_Empty_Schedules_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_Schedule_list, Table_Columns=6, Table_Rows=len(Skip_Event_Schedule_list))
    Frame_Empty_Schedules_Table_Var = Frame_Empty_Schedules_Table.children["!ctktable"]
    Frame_Empty_Schedules_Table_Var.configure(wraplength=150)

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

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var2 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var2.configure(variable=Project_Variable)
    
    # Field - Activity --> placed before project because of variable to be used
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var2 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var2.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(attach=Project_Option_Var2, values=Project_List, command = lambda Project_Option_Var2: Retrive_Activity_based_on_Type(Project_Option_Var=Project_Option_Var2, Activity_Option_Var=Activity_Option_Var2, Project_Variable=Project_Variable))
    Elements.Get_Option_Menu_Advance(attach=Activity_Option_Var2, values=Activity_All_List, command=None)

    # Field - Start Time
    Start_Time_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Start Time", Field_Type="Input_Normal") 
    Start_Time_Text_Var = Start_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    Start_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")

    # Field - End Time
    End_Time_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="End Time", Field_Type="Input_Normal") 
    End_Time_Text_Var = End_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    End_Time_Text_Var.configure(placeholder_text=f"{Format_Time}")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Schedule_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Schedule_Add_Var.configure(text="Add", command = lambda:Add_Schedule_Event(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var2=Project_Option_Var2, Activity_Option_Var2=Activity_Option_Var2, Start_Time_Text_Var=Start_Time_Text_Var, End_Time_Text_Var=End_Time_Text_Var, Monday_Check_Frame_Var=Monday_Check_Frame_Var, Tuesday_Check_Frame_Var=Tuesday_Check_Frame_Var, Wednesday_Check_Frame_Var=Wednesday_Check_Frame_Var, Thursday_Check_Frame_Var=Thursday_Check_Frame_Var, Friday_Check_Frame_Var=Friday_Check_Frame_Var, Saturday_Check_Frame_Var=Saturday_Check_Frame_Var, Sunday_Check_Frame_Var=Sunday_Check_Frame_Var))
    Elements.Get_ToolTip(widget=Button_Schedule_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_Schedule_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Schedule_Del_One_Var.configure(text="Del", command = lambda:Del_Schedule_Event_One(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var))
    Elements.Get_ToolTip(widget=Button_Schedule_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_Schedule_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Schedule_Del_All_Var.configure(text="Del all", command = lambda:Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var))
    Elements.Get_ToolTip(widget=Button_Schedule_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="y", expand=True, padx=0, pady=0)

    Week_Days_Label.pack(side="top", fill="none", expand=False, padx=10, pady=10)
    Week_Days_Frame.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Monday_Check_Frame.pack(side="left", padx=5, pady=5)
    Tuesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Wednesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Thursday_Check_Frame.pack(side="left", padx=5, pady=5)
    Friday_Check_Frame.pack(side="left", padx=5, pady=5)
    Saturday_Check_Frame.pack(side="left", padx=5, pady=5)
    Sunday_Check_Frame.pack(side="left", padx=5, pady=5)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Events - Rules --------------------------------------------------------------------------#
def Settings_Events_AutoFill(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Add_AutoFill_Event(Header_List: list, Frame_AutoFiller_Table_Var: CTkTable, Subject_Text_Text_Var: CTkEntry, Project_Option_Var: CTkOptionMenu, Activity_Option_Var: CTkOptionMenu, Location_Option_Var: CTkOptionMenu) -> None:
        Add_flag = True
        # Load single values
        Add_Search_Text = Subject_Text_Text_Var.get()
        Add_Project = Project_Option_Var.get()
        Add_Activity = Activity_Option_Var.get()
        Add_Location = Location_Option_Var.get()

        Check_List = Frame_AutoFiller_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)
        Add_row = [Add_Search_Text, Add_Project, Add_Activity, Add_Location]

        # Values checkers
        # Search text
        if Add_Search_Text == "":
            Add_flag = False
            CTkMessagebox(title="Error", message=f"Search Text is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass
        
        # Not To add same line -->  consider only Search text
        if Add_flag == True:
            for AutoFill_Event in Check_List:
                if AutoFill_Event[0] != Add_row[0]:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"Rule with Search text already exists with Autofiller.", icon="cancel", fade_in_duration=1)

        if Add_flag == True:
            Frame_AutoFiller_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Auto_Fill_Events = Frame_AutoFiller_Table_Var.values
            Auto_Fill_Events = [i for i in Auto_Fill_Events if i != Header_List]

            Auto_Fill_dict = {}
            Counter = 0
            for Auto_Fill_Events_row in Auto_Fill_Events:
                Auto_Fill_Events_row_row_dict = dict(zip(Header_List, Auto_Fill_Events_row))
                Auto_Fill_dict[Counter] = Auto_Fill_Events_row_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text"], Information=Auto_Fill_dict)
        else:
            pass
        
    def Del_AutoFill_Event_One() -> None:
        def Delete_AutoFill_Confirm(Frame_AutoFiller_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_AutoFiller_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            AutoFill_Events = Frame_AutoFiller_Table_Var.values
            AutoFill_Events = [i for i in AutoFill_Events if i != Header_List]

            AutoFill_dict = {}
            Counter = 0
            for AutoFill_Events_row in AutoFill_Events:
                AutoFill_Events_row_dict = dict(zip(Header_List, AutoFill_Events_row))
                AutoFill_dict[Counter] = AutoFill_Events_row_dict
                Counter += 1
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text"], Information=AutoFill_dict)
            Delete_AutoFill_Close()

        def Delete_AutoFill_Close() -> None:
            Delete_AutoFill_Window.destroy()

        def Update_Labels_Texts(LineNo_Option_Var: int, Frame_AutoFiller_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, Location_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=LineNo_Option_Var)
            Selected_Project = Frame_AutoFiller_Table_Var.get(row=LineNo_Option_Var, column=0)
            Selected_Activity = Frame_AutoFiller_Table_Var.get(row=LineNo_Option_Var, column=1)
            Selected_Description = Frame_AutoFiller_Table_Var.get(row=LineNo_Option_Var, column=2)
            Selected_Location = Frame_AutoFiller_Table_Var.get(row=LineNo_Option_Var, column=3)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            Location_Label_Var.configure(text=Selected_Location)

        # callculat number of lines in table
        AutoFill_Events = Frame_AutoFiller_Table_Var.values
        AutoFill_Events = [i for i in AutoFill_Events if i != Header_List]
        Lines_No = len(AutoFill_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_AutoFill_Window = CTkToplevel()
        Delete_AutoFill_Window.configure(fg_color="#000001")
        Delete_AutoFill_Window.title("Collor Picker")
        Delete_AutoFill_Window.geometry(f"510x260")
        Delete_AutoFill_Window.bind(sequence="<Escape>", func=lambda evet: Delete_AutoFill_Window.destroy())
        Delete_AutoFill_Window.overrideredirect(boolean=True)
        Delete_AutoFill_Window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Delete_AutoFill_Window.resizable(width=False, height=False)

        # Rounded corners 
        Delete_AutoFill_Window.config(background="#000001")
        Delete_AutoFill_Window.attributes("-transparentcolor", "#000001")

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Delete_AutoFill_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project: ") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity: ") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description: ") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=2))
        Location_Label = Elements_Groups.Get_Double_Label(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Coverage: ") 
        Location_Label_Var = Location_Label.children["!ctkframe3"].children["!ctklabel"]
        Location_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=3))

        Elements.Get_Option_Menu_Advance(attach=LineNo_Option_Var, values=Lines_list, command= lambda LineNo_Option_Var: Update_Labels_Texts(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, LineNo_Option_Var=LineNo_Option_Var, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Location_Label_Var=Location_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_AutoFill_Confirm(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_AutoFill_Close())
        Elements.Get_ToolTip(widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_AutoFiller_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_AutoFiller_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text"], Information={})

    # ------------------------- Main Functions -------------------------#
    Header_List = ["Search Text", "Project", "Activity", "Location"]
    Project_Variable = StringVar(master=Frame, value=Project_List[0])
    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])
    Location_Variable = StringVar(master=Frame, value=Location_List[0])

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="AutoFill rules", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple rules applied on TimeSheet Entry if part/whole Search Text is found in Subject. If empty then do not fill it or overwrite it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Imput Field + button in one line
    Frame_Imput_Total = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Imput_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")
    Frame_Imput_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame_Imput_Total, Field_Frame_Type="Single_Column")

    # AutoFilling Table
    Skip_AutoFill_list = [Header_List]
    Skip_AutoFill_dict_rows = Skip_AutoFill_dict.items()
    for Sub_Row in Skip_AutoFill_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_AutoFill_list.append(list(Sub_dict.values()))

    Frame_AutoFiller_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_AutoFill_list, Table_Columns=4, Table_Rows=len(Skip_AutoFill_list))
    Frame_AutoFiller_Table_Var = Frame_AutoFiller_Table.children["!ctktable"]
    Frame_AutoFiller_Table_Var.configure(wraplength=230)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Search Text", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(variable=Project_Variable)
    Elements.Get_Option_Menu_Advance(attach=Project_Option_Var, values=Project_List, command=None)

    # Field - Activity --> opravdu z listu všech aktivit protože mohu nastavit pravidlo bez Projektu
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(variable=Activity_Variable)
    Elements.Get_Option_Menu_Advance(attach=Activity_Option_Var, values=Activity_All_List, command=None)

    # Field - Location
    Location_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Label="Location", Field_Type="Input_OptionMenu") 
    Location_Option_Var = Location_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Location_Option_Var.configure(variable=Location_Variable)
    Elements.Get_Option_Menu_Advance(attach=Location_Option_Var, values=Location_List, command=None)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Imput_Area, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_AutoFill_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_AutoFill_Add_Var.configure(text="Add", command = lambda:Add_AutoFill_Event(Header_List=Header_List, Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var=Project_Option_Var, Activity_Option_Var=Activity_Option_Var, Location_Option_Var=Location_Option_Var))
    Elements.Get_ToolTip(widget=Button_AutoFill_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_AutoFill_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_AutoFill_Del_One_Var.configure(text="Del", command = lambda:Del_AutoFill_Event_One())
    Elements.Get_ToolTip(widget=Button_AutoFill_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_AutoFill_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_AutoFill_Del_All_Var.configure(text="Del all", command = lambda:Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var))
    Elements.Get_ToolTip(widget=Button_AutoFill_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Imput_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Imput_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="y", expand=True, padx=0, pady=0)

    return Frame_Main