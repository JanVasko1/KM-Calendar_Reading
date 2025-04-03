# Import Libraries
import json
from datetime import datetime

import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.File_Manipulation as File_Manipulation

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetTableFrame, WidgetRow_CheckBox, WidgetRow_Input_Entry, WidgetRow_Double_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Color_Picker, Widget_Buttons_Row

import pywinstyles

from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, BooleanVar, CTkOptionMenu, CTkButton, CTkCheckBox, CTkLabel, set_appearance_mode
from CTkTable import CTkTable

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Entry_field_Insert(Field: CTkEntry, Value: str|int) -> None:
    if type(Value) == str:
        if Value != "":
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    elif type(Value) == int:
        if Value > 0:
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    else:
        pass

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

def Retrieve_Activity_based_on_Type(Settings: dict, Configuration:dict, Project_Option_Var: CTkOptionMenu, Activity_Option_Var: CTkOptionMenu, Project_Variable: StringVar, GUI_Level_ID: int|None = None) -> None:
    Activity_by_Type_dict = Settings["0"]["Event_Handler"]["Activity"]["Activity_by_Type_dict"]
    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]

    try:
        Project_Variable.set(value=Project_Option_Var)
        # Get Selected Project and retrieve Project Type of selected Project
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
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var, values=Activity_List, command=None, GUI_Level_ID=GUI_Level_ID)

def Check_Time_Continuation(Settings: dict, Configuration: dict, window: CTk|None, Format_Time: str, Start_Time: str, End_Time: str, Week_Day: str, Type: str) -> bool:
    Start_Time_dt = datetime.strptime(Start_Time, Format_Time)
    End_Time_dt = datetime.strptime(End_Time, Format_Time)
    if Start_Time_dt >= End_Time_dt:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"You entered same or sooner time as Start time, this is not compatible, please correct it. This value is not to be saved.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Calendar", f"{Week_Day}", f"{Type}", "End_Time"], Information=End_Time)


def Calculate_duration(Settings: dict, Configuration: dict, window: CTk|None, Entry_Field: CTkEntry, Lunch_Brake_Duration: int, Calendar_Type: str, Monday_Start: str, Monday_End: str, Tuesday_Start: str, Tuesday_End: str, Wednesday_Start: str, Wednesday_End: str, Thursday_Start: str, Thursday_End: str, Friday_Start: str, Friday_End: str, Saturday_Start: str, Saturday_End: str, Sunday_Start: str, Sunday_End: str) -> None:
    Format_Time = Settings["0"]["General"]["Formats"]["Time"]
    Monday_Working_day = Settings["0"]["General"]["Calendar"]["Monday"]["Working_Day"]
    Tuesday_Working_day = Settings["0"]["General"]["Calendar"]["Tuesday"]["Working_Day"]
    Wednesday_Working_day = Settings["0"]["General"]["Calendar"]["Wednesday"]["Working_Day"]
    Thursday_Working_day = Settings["0"]["General"]["Calendar"]["Thursday"]["Working_Day"]
    Friday_Working_day = Settings["0"]["General"]["Calendar"]["Friday"]["Working_Day"]
    Saturday_Working_day = Settings["0"]["General"]["Calendar"]["Saturday"]["Working_Day"]
    Sunday_Working_day = Settings["0"]["General"]["Calendar"]["Sunday"]["Working_Day"]


    def Calculate_day_duration(Start_Time: str, End_Time: str, Week_Day: str, Calendar_Type: str, Working_Day: bool) -> int:
        if (Start_Time == "") or (End_Time == ""):
            Duration = 0
        else:
            Start_Time_dt = datetime.strptime(Start_Time, Format_Time)
            End_Time_dt = datetime.strptime(End_Time, Format_Time)
            Duration_dt = End_Time_dt - Start_Time_dt
            Duration = int(Duration_dt.total_seconds() / 60)

            # Subtract Lunch break for Working Calendar
            if (Working_Day == True) and (Calendar_Type == "Work_Hours"):
                Duration = Duration - Lunch_Brake_Duration
            else:
                pass

        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Calendar", f"{Week_Day}", f"{Calendar_Type}", "Day_Duration"], Information=Duration)
        return Duration
    
    Cumulated_Duration = 0
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Monday_Start, End_Time=Monday_End, Week_Day="Monday", Calendar_Type=Calendar_Type, Working_Day=Monday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Tuesday_Start, End_Time=Tuesday_End, Week_Day="Tuesday", Calendar_Type=Calendar_Type, Working_Day=Tuesday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Wednesday_Start, End_Time=Wednesday_End, Week_Day="Wednesday", Calendar_Type=Calendar_Type, Working_Day=Wednesday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Thursday_Start, End_Time=Thursday_End, Week_Day="Thursday", Calendar_Type=Calendar_Type, Working_Day=Thursday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Friday_Start, End_Time=Friday_End, Week_Day="Friday", Calendar_Type=Calendar_Type, Working_Day=Friday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Saturday_Start, End_Time=Saturday_End, Week_Day="Saturday", Calendar_Type=Calendar_Type, Working_Day=Saturday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Sunday_Start, End_Time=Sunday_End, Week_Day="Sunday", Calendar_Type=Calendar_Type, Working_Day=Sunday_Working_day)

    Hours = Cumulated_Duration // 60
    Minutes = Cumulated_Duration - (Hours * 60) 
    if Hours < 10:
        Hours = f"0{Hours}"
    else:
        Hours = f"{Hours}"

    if Minutes < 10: 
        Minutes = f"0{Minutes}"
    else:
        Minutes = f"{Minutes}"
    Total_Duration = f"{Hours}:{Minutes}"

    # Update Value in field
    Entry_Field.configure(state="normal")
    Entry_Field.configure(placeholder_text=Total_Duration)
    Entry_Field.configure(state="disabled")

    # Save to json
    if Calendar_Type == "Work_Hours":
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Calendar", "Totals", "Work"], Information=Total_Duration)
    elif Calendar_Type == "Vacation":
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Calendar", "Totals", "Vacation"], Information=Total_Duration)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Calendar Type not allowed", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- Tab Appearance --------------------------------------------------------------------------#
def Settings_General_Appearance(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]
    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # ------------------------- Local Functions ------------------------#
    def Appearance_Change_Theme() ->  None:
        set_appearance_mode(mode_string=Theme_Variable.get())

    # ------------------------- Main Functions -------------------------#
    # Widget
    Appearance_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Appearance", Additional_Text="SideBar applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="General Appearance setup.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Theme_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Theme", Variable=Theme_Variable, Values=Theme_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Theme"], Local_function_list=[Appearance_Change_Theme], GUI_Level_ID=GUI_Level_ID) 

    Accent_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Appearance_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Accent color", Label_Size="Field_Label", Font_Size="Section_Separator")
    Accent_Color_Manual_Row = WidgetRow_Color_Picker(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Accent Color Manual", Value=Accent_Color_Manual, placeholder_text_color="#949A9F", Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Button_ToolTip="Color Picker.", Picker_Always_on_Top=True, Picker_Fixed_position=True, GUI_Level_ID=GUI_Level_ID + 1)
    Accent_Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["App Default", "Windows", "Manual"], Freeze_fields=[[Accent_Color_Manual_Row],[Accent_Color_Manual_Row],[]])
    Accent_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Accent Color Mode", Variable=Accent_Color_Mode_Variable, Values=Accent_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Field_list=[Accent_Color_Manual_Row], Field_Blocking_dict=Accent_Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Hover_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Appearance_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Hover color", Label_Size="Field_Label", Font_Size="Section_Separator")
    Hover_Color_Manual_Row = WidgetRow_Color_Picker(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Manual", Value=Hover_Color_Manual, placeholder_text_color="#949A9F", Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Button_ToolTip="Color Picker.", Picker_Always_on_Top=True, Picker_Fixed_position=True, GUI_Level_ID=GUI_Level_ID + 1)
    Hover_Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["App Default", "Accent Lighter", "Manual"], Freeze_fields=[[Hover_Color_Manual_Row],[Hover_Color_Manual_Row],[]])
    Hover_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Mode", Variable=Hover_Color_Mode_Variable, Values=Hover_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Field_list=[Hover_Color_Manual_Row], Field_Blocking_dict=Hover_Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Appearance_Widget.Add_row(Rows=[Theme_Row, Accent_Section_Row, Accent_Color_Mode_Row, Accent_Color_Manual_Row, Hover_Section_Row, Hover_Color_Mode_Row, Hover_Color_Manual_Row])

    return Appearance_Widget


def Settings_User_Widget(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    User_Name = Settings["0"]["General"]["User"]["Name"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    User_Email = Settings["0"]["General"]["User"]["Email"]
    Page_Selected = Configuration["Global_Appearance"]["Window"]["Init_Page"]["Selected"]
    Page_Selected_list = list(Configuration["Global_Appearance"]["Window"]["Init_Page"]["Page_List"])
    User_Type = Settings["0"]["General"]["User"]["User_Type"]
    User_Type_list = list(Settings["0"]["General"]["User"]["User_Type_list"])
    User_Type_Variable = StringVar(master=Frame, value=User_Type, name="User_Type_Variable")
    Page_Selected_Variable = StringVar(master=Frame, value=Page_Selected, name="Page_Selected_Variable")
    
    # ------------------------- Local Functions ------------------------#
    def Password_required(User_Type_Variable: StringVar, Value: str) -> None:
        def Dialog_Window_Request(title: str, text: str, Dialog_Type: str) -> str|None:
            # Password required
            dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
            Password = dialog.get_input()
            return Password
        
        if Value == "User":
            User_Type_Variable.value = "User"
        elif Value == "Manager":
            Password = Dialog_Window_Request(title="Admin", text="Write your password", Dialog_Type="Password")

            if Password == "JVA_is_best":
                User_Type_Variable.value = "Manager"
            else:
                User_Type_Variable.value = "User"
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Wrong administration password.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
           

    # ------------------------- Main Functions -------------------------#
    # Widget
    User_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="User", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="This is setup of definition if user is considerate as user or user leading team with additional functionality.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    User_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=User_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="User ID", Value=User_ID, placeholder_text="My Konica ID.", Save_To="Settings", Save_path=["0", "General", "User", "Code"])
    User_Name_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=User_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="User Name", Value=User_Name, placeholder_text="My Name.", Save_To="Settings", Save_path=["0", "General", "User", "Name"])
    User_Email_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=User_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="User Email", Value=User_Email, placeholder_text="My Konica email.", Save_To="Settings", Save_path=["0", "General", "User", "Email"])
    Default_Page_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=User_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Default page", Variable=Page_Selected_Variable, Values=Page_Selected_list, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Init_Page", "Selected"], GUI_Level_ID=GUI_Level_ID) 
    User_Type_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=User_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="User Type", Variable=User_Type_Variable, Values=User_Type_list, Save_To="Settings", Save_path=["0", "General", "User", "User_Type"], GUI_Level_ID=GUI_Level_ID) 
    User_Type_Row.Local_function_list = [lambda: Password_required(User_Type_Variable=User_Type_Variable, Value=User_Type_Row.Get_Value())]

    # Add Fields to Widget Body
    User_Widget.Add_row(Rows=[User_ID_Row, User_Name_Row, User_Email_Row, Default_Page_Row, User_Type_Row])

    return User_Widget


# -------------------------------------------------------------------------- Tab GEneral --------------------------------------------------------------------------#
def Settings_General_Sharepoint(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    SP_Auth_Address = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]   
    SP_File_Name = Settings["0"]["General"]["Downloader"]["Sharepoint"]["File_name"]
    SP_Team = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
    SP_Teams_List = list(Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_List"])
    SP_Team_Variable = StringVar(master=Frame, value=SP_Team)

    # ------------------------- Main Functions -------------------------#
    # Widget
    Sharepoint_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Sharepoint", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    SP_Team_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Team", Variable=SP_Team_Variable, Values=SP_Teams_List, Save_To="Settings", Save_path=["0", "General", "Downloader", "Sharepoint", "Teams", "My_Team"], GUI_Level_ID=GUI_Level_ID) 
    SP_File_Name_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="File Name", Value="", placeholder_text=SP_File_Name, placeholder_text_color="#949A9F")
    SP_File_Name_Row.Freeze()
    SP_Auth_Address_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Auth Address", Value="", placeholder_text=SP_Auth_Address, placeholder_text_color="#949A9F")
    SP_Auth_Address_Row.Freeze()

    # Add Fields to Widget Body
    Sharepoint_Widget.Add_row(Rows=[SP_Team_Row, SP_File_Name_Row, SP_Auth_Address_Row])

    return Sharepoint_Widget

def Settings_General_Exchange(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Category_Active_Color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Active_Color"]
    Category_Non_Active_Color = Settings["0"]["Event_Handler"]["Project"]["Colors"]["Non_Active_Color"]
    Category_Color_list = list(Settings["0"]["Event_Handler"]["Project"]["Colors"]["Color_List"])
    Category_Active_Color_Variable = StringVar(master=Frame, value=Category_Active_Color)
    Category_Non_Active_Color_Variable = StringVar(master=Frame, value=Category_Non_Active_Color)

    # ------------------------- Local Functions ------------------------#
    def Save_set_key_Auth(Key: str, Value: str) ->  None:
        Defaults_Lists.Save_set_key_Auth(Key=Key, Value=Value)

    # ------------------------- Main Functions -------------------------#
    # Widget
    Exchange_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Exchange", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Exchange Server related settings.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Categories_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Exchange_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Categories", Label_Size="Field_Label", Font_Size="Section_Separator")
    Active_Category_Color_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Category Active Color", Variable=Category_Active_Color_Variable, Values=Category_Color_list, Save_To="Settings", Save_path=["0", "Event_Handler", "Project", "Colors", "Active_Color"], GUI_Level_ID=GUI_Level_ID) 
    Non_Active_Category_Color_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Category Non-Active Color", Variable=Category_Non_Active_Color_Variable, Values=Category_Color_list, Save_To="Settings", Save_path=["0", "Event_Handler", "Project", "Colors", "Non_Active_Color"], GUI_Level_ID=GUI_Level_ID) 

    OAuth_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Exchange_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="OAuth2", Label_Size="Field_Label", Font_Size="Section_Separator")
    NAV_Display_name_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Client Name", Value=Display_name, placeholder_text="Enter Name of Auth app.")
    NAV_Display_name_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="Display_name", Value=NAV_Display_name_Row.Get_Value())]
    NAV_Client_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Client ID", Value=client_id, placeholder_text="Enter Client ID of Auth app.")
    NAV_Client_ID_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="client_id", Value=NAV_Client_ID_Row.Get_Value())]
    NAV_Client_Secret_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Password", Label="Client Secret", Value=client_secret, placeholder_text="Enter Secret ID of Auth app.")
    NAV_Client_Secret_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="client_secret", Value=NAV_Client_Secret_Row.Get_Value())]
    Exchange_Tenant_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Tenant ID", placeholder_text=tenant_id, placeholder_text_color="#949A9F")

    # Add Fields to Widget Body
    Exchange_Widget.Add_row(Rows=[Categories_Section_Row, Active_Category_Color_Row, Non_Active_Category_Color_Row, OAuth_Section_Row, NAV_Display_name_Row, NAV_Client_ID_Row, NAV_Client_Secret_Row, Exchange_Tenant_ID_Row])

    return Exchange_Widget

def Settings_General_Formats(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Date = Settings["0"]["General"]["Formats"]["Date"]
    Format_Time = Settings["0"]["General"]["Formats"]["Time"]
    Format_Exchange_DateTime = Settings["0"]["General"]["Formats"]["Exchange_DateTime"]
    Format_Sharepoint_DateTime = Settings["0"]["General"]["Formats"]["Sharepoint_DateTime"]
    Format_Sharepoint_Date = Settings["0"]["General"]["Formats"]["Sharepoint_Date"]
    Format_Sharepoint_Date1 = Settings["0"]["General"]["Formats"]["Sharepoint_Date1"]
    Format_Sharepoint_Date2 = Settings["0"]["General"]["Formats"]["Sharepoint_Date2"]
    Format_Sharepoint_Time = Settings["0"]["General"]["Formats"]["Sharepoint_Time"]
    Format_Sharepoint_Time1 = Settings["0"]["General"]["Formats"]["Sharepoint_Time1"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Formats_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Formats", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Dates formats used in program - non-changeable.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Program_Date_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date", Value="", placeholder_text=Format_Date, placeholder_text_color="#949A9F")
    Program_Date_Row.Freeze()
    Program_Time_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Time", Value="", placeholder_text=Format_Time, placeholder_text_color="#949A9F")
    Program_Time_Row.Freeze()
    Exchange_DateTime_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Exchange DateTime", Value="", placeholder_text=Format_Exchange_DateTime, placeholder_text_color="#949A9F")
    Exchange_DateTime_Row.Freeze()
    Sharepoint_DateTime_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint DateTime", Value="", placeholder_text=Format_Sharepoint_DateTime, placeholder_text_color="#949A9F")
    Sharepoint_DateTime_Row.Freeze()
    Sharepoint_Date_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint Date 1", Value="", placeholder_text=Format_Sharepoint_Date, placeholder_text_color="#949A9F")
    Sharepoint_Date_Row.Freeze()
    Sharepoint_Date2_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint Date 2", Value="", placeholder_text=Format_Sharepoint_Date1, placeholder_text_color="#949A9F")
    Sharepoint_Date2_Row.Freeze()
    Sharepoint_Date3_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint Date 3", Value="", placeholder_text=Format_Sharepoint_Date2, placeholder_text_color="#949A9F")
    Sharepoint_Date3_Row.Freeze()
    Sharepoint_Time_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint Time 1", Value="", placeholder_text=Format_Sharepoint_Time, placeholder_text_color="#949A9F")
    Sharepoint_Time_Row.Freeze()
    Sharepoint_Time2_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Formats_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Sharepoint Time 2", Value="", placeholder_text=Format_Sharepoint_Time1, placeholder_text_color="#949A9F")
    Sharepoint_Time2_Row.Freeze()

    # Add Fields to Widget Body
    Formats_Widget.Add_row(Rows=[Program_Date_Row, Program_Time_Row, Exchange_DateTime_Row, Sharepoint_DateTime_Row, Sharepoint_Date_Row, Sharepoint_Date2_Row, Sharepoint_Date3_Row, Sharepoint_Time_Row, Sharepoint_Time2_Row])

    return Formats_Widget

# -------------------------------------------------------------------------- Tab Calendar --------------------------------------------------------------------------#
def Settings_Calendar_Working_Hours(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Time = Settings["0"]["General"]["Formats"]["Time"]
    Lunch_Brake_Duration =  Settings["0"]["General"]["Calendar"]["Lunch_Brake_Dur"]
    Monday_Work_Start = Settings["0"]["General"]["Calendar"]["Monday"]["Work_Hours"]["Start_Time"]
    Tuesday_Work_Start = Settings["0"]["General"]["Calendar"]["Tuesday"]["Work_Hours"]["Start_Time"]
    Wednesday_Work_Start = Settings["0"]["General"]["Calendar"]["Wednesday"]["Work_Hours"]["Start_Time"]
    Thursday_Work_Start = Settings["0"]["General"]["Calendar"]["Thursday"]["Work_Hours"]["Start_Time"]
    Friday_Work_Start = Settings["0"]["General"]["Calendar"]["Friday"]["Work_Hours"]["Start_Time"]
    Saturday_Work_Start = Settings["0"]["General"]["Calendar"]["Saturday"]["Work_Hours"]["Start_Time"]
    Sunday_Work_Start = Settings["0"]["General"]["Calendar"]["Sunday"]["Work_Hours"]["Start_Time"]
    Monday_Work_End = Settings["0"]["General"]["Calendar"]["Monday"]["Work_Hours"]["End_Time"]
    Tuesday_Work_End = Settings["0"]["General"]["Calendar"]["Tuesday"]["Work_Hours"]["End_Time"]
    Wednesday_Work_End = Settings["0"]["General"]["Calendar"]["Wednesday"]["Work_Hours"]["End_Time"]
    Thursday_Work_End = Settings["0"]["General"]["Calendar"]["Thursday"]["Work_Hours"]["End_Time"]
    Friday_Work_End = Settings["0"]["General"]["Calendar"]["Friday"]["Work_Hours"]["End_Time"]
    Saturday_Work_End = Settings["0"]["General"]["Calendar"]["Saturday"]["Work_Hours"]["End_Time"]
    Sunday_Work_End = Settings["0"]["General"]["Calendar"]["Sunday"]["Work_Hours"]["End_Time"]

    Total_Work_Duration =  Settings["0"]["General"]["Calendar"]["Totals"]["Work"]

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    My_Calendar_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Calendar - My own calendar", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Setup of my general working hours I usually have. Used for Utilization forecast. Lunch brake automatically subtracted.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Monday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Monday", Value1=Monday_Work_Start, Value2=Monday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Monday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Monday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Monday_Row.Get_Value1(), End_Time=Monday_Row.Get_Value2(), Week_Day="Monday", Type="Work_Hours")]
    Tuesday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Tuesday", Value1=Tuesday_Work_Start, Value2=Tuesday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Tuesday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Tuesday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Tuesday_Row.Get_Value1(), End_Time=Tuesday_Row.Get_Value2(), Week_Day="Tuesday", Type="Work_Hours")]
    Wednesday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Wednesday", Value1=Wednesday_Work_Start, Value2=Wednesday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Wednesday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Wednesday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Wednesday_Row.Get_Value1(), End_Time=Wednesday_Row.Get_Value2(), Week_Day="Wednesday", Type="Work_Hours")]
    Thursday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Thursday", Value1=Thursday_Work_Start, Value2=Thursday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Thursday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Thursday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Thursday_Row.Get_Value1(), End_Time=Thursday_Row.Get_Value2(), Week_Day="Thursday", Type="Work_Hours")]
    Friday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Friday", Value1=Friday_Work_Start, Value2=Friday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Friday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Friday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Friday_Row.Get_Value1(), End_Time=Friday_Row.Get_Value2(), Week_Day="Friday", Type="Work_Hours")]
    Saturday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Saturday", Value1=Saturday_Work_Start, Value2=Saturday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Saturday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Saturday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Saturday_Row.Get_Value1(), End_Time=Saturday_Row.Get_Value2(), Week_Day="Saturday", Type="Work_Hours")]
    Sunday_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Sunday", Value1=Sunday_Work_Start, Value2=Sunday_Work_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Sunday", "Work_Hours", "Start_Time"], Validation1="Time", Validation2="Time")
    Sunday_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Sunday_Row.Get_Value1(), End_Time=Sunday_Row.Get_Value2(), Week_Day="Sunday", Type="Work_Hours")]
    Lunch_Brake_Duration_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Lunch brake duration", Value=Lunch_Brake_Duration, Save_To="Settings", Save_path=["0", "General", "Calendar", "Lunch_Brake_Dur"], Validation="Integer")
    Work_Calendar_Total_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Total Time", placeholder_text=Total_Work_Duration, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "General", "Calendar", "Lunch_Brake_Dur"], Validation="Time")
    Work_Calendar_Total_Row.Freeze()
    Button_Functions = [lambda: Calculate_duration(Settings=Settings, Configuration=Configuration, window=window, Entry_Field=Work_Calendar_Total_Row.Input_Entry, Lunch_Brake_Duration=int(Lunch_Brake_Duration_Row.Get_Value()), Calendar_Type="Work_Hours", Monday_Start=Monday_Row.Get_Value1(), Monday_End=Monday_Row.Get_Value2(), Tuesday_Start=Tuesday_Row.Get_Value1(), Tuesday_End=Tuesday_Row.Get_Value2(), Wednesday_Start=Wednesday_Row.Get_Value1(), Wednesday_End=Wednesday_Row.Get_Value2(), Thursday_Start=Thursday_Row.Get_Value1(), Thursday_End=Thursday_Row.Get_Value2(), Friday_Start=Friday_Row.Get_Value1(), Friday_End=Friday_Row.Get_Value2(), Saturday_Start=Saturday_Row.Get_Value1(), Saturday_End=Saturday_Row.Get_Value2(), Sunday_Start=Sunday_Row.Get_Value1(), Sunday_End=Sunday_Row.Get_Value2())]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=My_Calendar_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=1, Button_Size="Small", Button_Text=["Calculate"], Button_ToolTips=["Calculate total week duration."], Button_Functions=Button_Functions, GUI_Level_ID=GUI_Level_ID)
    

    # Add Fields to Widget Body
    My_Calendar_Widget.Add_row(Rows=[Monday_Row, Tuesday_Row, Wednesday_Row, Thursday_Row, Friday_Row, Saturday_Row, Sunday_Row, Lunch_Brake_Duration_Row, Work_Calendar_Total_Row, Button_Row])

    return My_Calendar_Widget


def Settings_Calendar_Vacation(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Time = Settings["0"]["General"]["Formats"]["Time"]
    Monday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Monday"]["Vacation"]["Start_Time"]
    Tuesday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Tuesday"]["Vacation"]["Start_Time"]
    Wednesday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Wednesday"]["Vacation"]["Start_Time"]
    Thursday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Thursday"]["Vacation"]["Start_Time"]
    Friday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Friday"]["Vacation"]["Start_Time"]
    Saturday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Saturday"]["Vacation"]["Start_Time"]
    Sunday_Vacation_Start = Settings["0"]["General"]["Calendar"]["Sunday"]["Vacation"]["Start_Time"]
    Monday_Vacation_End = Settings["0"]["General"]["Calendar"]["Monday"]["Vacation"]["End_Time"]
    Tuesday_Vacation_End = Settings["0"]["General"]["Calendar"]["Tuesday"]["Vacation"]["End_Time"]
    Wednesday_Vacation_End = Settings["0"]["General"]["Calendar"]["Wednesday"]["Vacation"]["End_Time"]
    Thursday_Vacation_End = Settings["0"]["General"]["Calendar"]["Thursday"]["Vacation"]["End_Time"]
    Friday_Vacation_End = Settings["0"]["General"]["Calendar"]["Friday"]["Vacation"]["End_Time"]
    Saturday_Vacation_End = Settings["0"]["General"]["Calendar"]["Saturday"]["Vacation"]["End_Time"]
    Sunday_Vacation_End = Settings["0"]["General"]["Calendar"]["Sunday"]["Vacation"]["End_Time"]
    Total_Vacation_Duration =  Settings["0"]["General"]["Calendar"]["Totals"]["Vacation"]

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#¨
    # Widget
    KM_Calendar_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Calendar - KM Working/Vacation/SickDay Hours", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="These hours be used in case of whole day vacation/SickDay and for KM Utilization charts and information.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Monday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Monday", Value1=Monday_Vacation_Start, Value2=Monday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Monday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Monday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Monday_Vac_Row.Get_Value1(), End_Time=Monday_Vac_Row.Get_Value2(), Week_Day="Monday", Type="Vacation")]
    Tuesday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Tuesday", Value1=Tuesday_Vacation_Start, Value2=Tuesday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Tuesday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Tuesday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Tuesday_Vac_Row.Get_Value1(), End_Time=Tuesday_Vac_Row.Get_Value2(), Week_Day="Tuesday", Type="Vacation")]
    Wednesday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Wednesday", Value1=Wednesday_Vacation_Start, Value2=Wednesday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Wednesday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Wednesday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Wednesday_Vac_Row.Get_Value1(), End_Time=Wednesday_Vac_Row.Get_Value2(), Week_Day="Wednesday", Type="Vacation")]
    Thursday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Thursday", Value1=Thursday_Vacation_Start, Value2=Thursday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Thursday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Thursday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Thursday_Vac_Row.Get_Value1(), End_Time=Thursday_Vac_Row.Get_Value2(), Week_Day="Thursday", Type="Vacation")]
    Friday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Friday", Value1=Friday_Vacation_Start, Value2=Friday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Friday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Friday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Friday_Vac_Row.Get_Value1(), End_Time=Friday_Vac_Row.Get_Value2(), Week_Day="Friday", Type="Vacation")]
    Saturday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Saturday", Value1=Saturday_Vacation_Start, Value2=Saturday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Saturday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Saturday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Saturday_Vac_Row.Get_Value1(), End_Time=Saturday_Vac_Row.Get_Value2(), Week_Day="Saturday", Type="Vacation")]
    Sunday_Vac_Row = WidgetRow_Double_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Sunday", Value1=Sunday_Vacation_Start, Value2=Sunday_Vacation_End, placeholder_text1="Day start time.", placeholder_text2="Day end time.", Save_To="Settings", Save_path1=["0", "General", "Calendar", "Sunday", "Vacation", "Start_Time"], Validation1="Time", Validation2="Time")
    Sunday_Vac_Row.Local_function2_list = [lambda: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, window=window, Format_Time=Format_Time, Start_Time=Sunday_Vac_Row.Get_Value1(), End_Time=Sunday_Vac_Row.Get_Value2(), Week_Day="Sunday", Type="Vacation")]
    Work_Calendar_Total_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Total Time", placeholder_text=Total_Vacation_Duration, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "General", "Calendar", "Lunch_Brake_Dur"], Validation="Time")
    Work_Calendar_Total_Row.Freeze()
    Button_Functions = [lambda: Calculate_duration(Settings=Settings, Configuration=Configuration, window=window, Entry_Field=Work_Calendar_Total_Row.Input_Entry, Lunch_Brake_Duration=0, Calendar_Type="Work_Hours", Monday_Start=Monday_Vac_Row.Get_Value1(), Monday_End=Monday_Vac_Row.Get_Value2(), Tuesday_Start=Tuesday_Vac_Row.Get_Value1(), Tuesday_End=Tuesday_Vac_Row.Get_Value2(), Wednesday_Start=Wednesday_Vac_Row.Get_Value1(), Wednesday_End=Wednesday_Vac_Row.Get_Value2(), Thursday_Start=Thursday_Vac_Row.Get_Value1(), Thursday_End=Thursday_Vac_Row.Get_Value2(), Friday_Start=Friday_Vac_Row.Get_Value1(), Friday_End=Friday_Vac_Row.Get_Value2(), Saturday_Start=Saturday_Vac_Row.Get_Value1(), Saturday_End=Saturday_Vac_Row.Get_Value2(), Sunday_Start=Sunday_Vac_Row.Get_Value1(), Sunday_End=Sunday_Vac_Row.Get_Value2())]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=KM_Calendar_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=1, Button_Size="Small", Button_Text=["Calculate"], Button_ToolTips=["Calculate total week duration."], Button_Functions=Button_Functions, GUI_Level_ID=GUI_Level_ID)
    

    # Add Fields to Widget Body
    KM_Calendar_Widget.Add_row(Rows=[Monday_Vac_Row, Tuesday_Vac_Row, Wednesday_Vac_Row, Thursday_Vac_Row, Friday_Vac_Row, Saturday_Vac_Row, Sunday_Vac_Row, Work_Calendar_Total_Row, Button_Row])

    return KM_Calendar_Widget


def Settings_Calendar_Start_End_Time(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Start_Event_json = Settings["0"]["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
    End_Event_json = Settings["0"]["Event_Handler"]["Events"]["Start_End_Events"]["End"]

    # ------------------------- Local Functions ------------------------#
    def Check_Same_Values(Start_Event_Row: WidgetRow_Input_Entry, End_Event_Row: WidgetRow_Input_Entry) -> bool:
        if Start_Event_Row.Get_Value() == End_Event_Row.Get_Value():
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You entered same value as Work - Start, which would not work, please change it. This value is not to be saved.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            End_Event_Row.Input_Entry.delete(first_index=0, last_index=100)
            End_Event_Row.Input_Entry.focus()
        else:
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Start_End_Events", "End"], Information=End_Event_Row.Get_Value())

    # ------------------------- Main Functions -------------------------#
    # Widget
    Calendar_Start_End_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Workday - Start / End Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Events Subject which defines Start and End time of each day in Calendar.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Start_Event_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Calendar_Start_End_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Work - Start", Value=Start_Event_json, placeholder_text="Event Subject which starts day.", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Start_End_Events", "Start"])
    End_Event_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Calendar_Start_End_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Work - End", Value=End_Event_json, placeholder_text="Event Subject which ends day")
    End_Event_Row.Local_function_list = [lambda: Check_Same_Values(Start_Event_Row=Start_Event_Row, End_Event_Row=End_Event_Row)]

    # Add Fields to Widget Body
    Calendar_Start_End_Widget.Add_row(Rows=[Start_Event_Row, End_Event_Row])

    return Calendar_Start_End_Widget


# -------------------------------------------------------------------------- Tab Events - General --------------------------------------------------------------------------#
def Settings_Parallel_events(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Parallel_Enabled = Settings["0"]["Event_Handler"]["Events"]["Parallel_Events"]["Use"]
    Start_Method = Settings["0"]["Event_Handler"]["Events"]["Parallel_Events"]["Start_Method"]
    Start_Method_List = Settings["0"]["Event_Handler"]["Events"]["Parallel_Events"]["Start_Method_List"]

    Parallel_Use_Variable = BooleanVar(master=Frame, value=Parallel_Enabled)
    Start_Method_Variable = StringVar(master=Frame, value=Start_Method)
    
    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    Parallel_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Parallel Events Handler", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definitions of behavior of processing Events when program found that they are parallel.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Parallel_Events_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Parallel_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Parallel_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Parallel_Events", "Use"])
    Start_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Parallel_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Same Start Time", Variable=Start_Method_Variable, Values=Start_Method_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Parallel_Events", "Start_Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Parallel_Widget.Add_row(Rows=[Use_Parallel_Events_Row, Start_Method_Row])

    return Parallel_Widget

def Settings_Join_events(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Join_Events_Enabled = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Use"]
    Join_Methods_List = list(Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Methods_List"])
    Join_Free = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Free"]
    Join_Tentative = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Tentative"]
    Join_Busy = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Busy"]
    Join_OutOfOffice = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Out of Office"]
    Join_Work_Else = Settings["0"]["Event_Handler"]["Events"]["Join_method"]["Working elsewhere"]
    Join_Use_Variable = BooleanVar(master=Frame, value=Join_Events_Enabled)
    Join_Free_Variable = StringVar(master=Frame, value=Join_Free)
    Join_Tentative_Variable = StringVar(master=Frame, value=Join_Tentative)
    Join_Busy_Variable = StringVar(master=Frame, value=Join_Busy)
    Join_OutOfOffice_Variable = StringVar(master=Frame, value=Join_OutOfOffice)
    Join_Work_Else_Variable = StringVar(master=Frame, value=Join_Work_Else)

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    Join_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Joining Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Joining Events belonging to same Visibility group.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Events_Joining_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Join_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Use"])
    Join_Free_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Free", Variable=Join_Free_Variable, Values=Join_Methods_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Free"], GUI_Level_ID=GUI_Level_ID) 
    Join_Tentative_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Tentative", Variable=Join_Tentative_Variable, Values=Join_Methods_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Tentative"], GUI_Level_ID=GUI_Level_ID) 
    Join_Busy_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Busy", Variable=Join_Busy_Variable, Values=Join_Methods_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Busy"], GUI_Level_ID=GUI_Level_ID) 
    Join_OutOfOffice_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Out of Office", Variable=Join_OutOfOffice_Variable, Values=Join_Methods_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Out of Office"], GUI_Level_ID=GUI_Level_ID) 
    Join_Work_ElseWhere_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Join_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Working ElseWhere", Variable=Join_Work_Else_Variable, Values=Join_Methods_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Join_method", "Working elsewhere"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Join_Widget.Add_row(Rows=[Use_Events_Joining_Row, Join_Free_Row, Join_Tentative_Row, Join_Busy_Row, Join_OutOfOffice_Row, Join_Work_ElseWhere_Row])

    return Join_Widget

def Settings_Events_Split(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Events_Empty_Split_Enabled = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Use"]
    Events_Empty_Split_Duration = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Duration"]
    Events_Empty_Split_Minimal_Time = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Minimal_Time"]
    Events_Empty_Split_Method = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Method"]
    Events_Empty_Split_list = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Split"]["Methods_List"]
    Empty_Split_Use_Variable = BooleanVar(master=Frame, value=Events_Empty_Split_Enabled)
    Events_Empty_Split_list_Variable = StringVar(master=Frame, value=Events_Empty_Split_Method, name="Events_Empty_Split_list_Variable")

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    Splitting_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Events Splitting", Additional_Text="Pay attention to Join Setup.", Widget_size="Single_size", Widget_Label_Tooltip="Use for splitting automatically filled events by program longer than defined duration. \nEffect of the split can be suppress partially / fully by Joining Events, depends on setup.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Empty_Split_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Splitting_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Empty_Split_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Empty", "Split", "Use"])
    Split_Duration_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Splitting_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Duration", Value=Events_Empty_Split_Duration, placeholder_text="Empty space duration which will be splitted.", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Empty", "Split", "Split_Duration"], Validation="Integer")
    Split_Min_Duration_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Splitting_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Minimal Time", placeholder_text=Events_Empty_Split_Minimal_Time, placeholder_text_color="#949A9F", Validation="Integer")
    Split_Min_Duration_Row.Freeze()

    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Equal Split", "Random Split"], Freeze_fields=[[Split_Duration_Row],[]])
    Split_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Splitting_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Events_Empty_Split_list_Variable, Values=Events_Empty_Split_list, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Empty", "Split", "Split_Method"], Field_list=[Split_Duration_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Splitting_Widget.Add_row(Rows=[Use_Empty_Split_Row, Split_Method_Row, Split_Duration_Row, Split_Min_Duration_Row])

    return Splitting_Widget



def Settings_Events_General_Skip(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Skip_Enabled = Settings["0"]["Event_Handler"]["Events"]["Skip"]["Use"]
    Events_Skip_list = Settings["0"]["Event_Handler"]["Events"]["Skip"]["Skip_List"]
    Skip_Use_Variable = BooleanVar(master=Frame, value=Skip_Enabled)

    # ------------------------- Local Functions -------------------------#
    def Add_Skip_Event(Header_List: list, Add_text: str, Frame_Skip_Table_Var: CTkTable) -> None:
        Add_flag = True

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
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Subject is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            # Save to Settings.json
            Skip_Events = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
            Skip_Events.remove(Header_List)
            Skip_Events.sort()
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Skip", "Skip_List"], Information=Skip_Events)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Subject is already within list of skip Events.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Del_Skip_Event_one(Del_text: str, Frame_Skip_Table_Var: CTkTable) -> None:
        # Find Index
        Deleted_flag = False
        if Del_text != "Skip Events":
            Table_len = len(Frame_Skip_Table_Var.values)
            for Table_index in range(0, Table_len):
                Table_row_value = Frame_Skip_Table_Var.values[Table_index][0]
                if Del_text == Table_row_value:
                    Frame_Skip_Table_Var.delete_row(index=Table_index)
                    Deleted_flag = True
                    break
                else:
                    pass
            if Deleted_flag == False:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Subject not found, please check spelling.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass
            Skip_Events = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
            Skip_Events.remove("Skip Events")
            Skip_Events.sort()
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Skip", "Skip_List"], Information=Skip_Events)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Header cannot be deleted.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Del_Skip_Event_all(Frame_Skip_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Skip_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Skip_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Skip", "Skip_List"], Information=[])

    def Save_Skip():
        # Copy Settings file into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Skip_Events",
            "Data": Events_Skip_list}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Skip_Events", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Skip Events has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Skip(Button_Load_Skip: CTkButton, Table: CTkTable):
        def Skip_drop_func(file):
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Skip_Events", JSON_path=["0", "Event_Handler", "Events", "Skip", "Skip_List"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Table, JSON_path=["0", "Event_Handler", "Events", "Skip", "Skip_List"])
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_Skip, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=Skip_drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)

    # ------------------------- Main Functions -------------------------#
    # Widget
    Skip_General_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Skip Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of text be skipped as TimeSheet Entry in the case that part of text is found in Event Subject.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Skip_Event_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Skip_General_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Skip_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Skip", "Use"])
    Subject_Text_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Skip_General_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Subject", placeholder_text="Add new text", placeholder_text_color="#949A9F")
    
    # Skip Events Table
    Header_List = ["Skip Events"]
    Show_Events_Skip_list = [Header_List]
    for skip_Subject in Events_Skip_list:
        Show_Events_Skip_list.append([skip_Subject])

    Frame_Skip_Table_Widget = WidgetTableFrame(Configuration=Configuration, Frame=Skip_General_Widget.Body_Frame, Table_Size="Single_size", Table_Values=Show_Events_Skip_list, Table_Columns=len(Header_List), Table_Rows=len(Events_Skip_list) + 1, wraplength=440, GUI_Level_ID=GUI_Level_ID + 1)

    Buttons_texts = ["Add", "Del", "Del All", "Export", "Import"]
    Buttons_ToolTips = ["Add selected subject to skip list.", "Delete row from table based on input text.", "Delete all rows from table.", "Save table content.", "Load and add new records to table."]
    Buttons_Functions = [lambda: Add_Skip_Event(Header_List=Header_List, Add_text=Subject_Text_Row.Get_Value(), Frame_Skip_Table_Var=Frame_Skip_Table_Widget.Table),
                         lambda: Del_Skip_Event_one(Del_text=Subject_Text_Row.Get_Value(), Frame_Skip_Table_Var=Frame_Skip_Table_Widget.Table),
                         lambda: Del_Skip_Event_all(Frame_Skip_Table_Var=Frame_Skip_Table_Widget.Table),
                         lambda: Save_Skip(),
                         lambda: Load_Skip(Button_Load_Skip=Button_Row.Frame_Buttons.children["!ctkbutton5"], Table=Frame_Skip_Table_Widget.Table)]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=Skip_General_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=5, Button_Size="Small", Button_Text=Buttons_texts, Button_ToolTips=Buttons_ToolTips, Button_Functions=Buttons_Functions, GUI_Level_ID=GUI_Level_ID)

    # Add Fields to Widget Body
    Skip_General_Widget.Add_row(Rows=[Use_Skip_Event_Row, Subject_Text_Row, Frame_Skip_Table_Widget, Button_Row])

    return Skip_General_Widget


def Settings_Events_General_Lunch(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Lunch_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Use"]
    Lunch_Search_Text = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Search_Text"]
    Lunch_All_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["All_Day"]
    Lunch_Part_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Part_Day"]
    Lunch_Day_Option_List = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Lunch_Option_List"]
    Lunch_Use_Variable = BooleanVar(master=Frame, value=Lunch_Enabled)
    Lunch_All_Variable = StringVar(master=Frame, value=Lunch_All_Day)
    Lunch_Part_Variable = StringVar(master=Frame, value=Lunch_Part_Day)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    Lunch_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Special - Lunch", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Lunch brake -> always skip it. \n Lunch break will always break Parallel Events.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Lunch_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Lunch_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Lunch_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Lunch", "Use"])
    Search_Text_Lunch_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Lunch_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Search text", Value=Lunch_Search_Text, placeholder_text="Event Subject which defines lunch", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Lunch", "Search_Text"])
    All_Day_Lunch_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Lunch_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="All Day", Variable=Lunch_All_Variable, Values=Lunch_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Lunch", "All_Day"], GUI_Level_ID=GUI_Level_ID) 
    Part_Day_Lunch_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Lunch_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Part Day", Variable=Lunch_Part_Variable, Values=Lunch_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Lunch", "Part_Day"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Lunch_Widget.Add_row(Rows=[Use_Lunch_Row, Search_Text_Lunch_Row, All_Day_Lunch_Row, Part_Day_Lunch_Row])

    return Lunch_Widget


def Settings_Events_General_Vacation(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Vacation_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Use"]
    Vacation_Search_Text = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Search_Text"]
    Vacation_All_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["All_Day"]
    Vacation_Part_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Part_Day"]
    Vacation_Day_Option_List = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Vacation_Option_List"]
    Vacation_Delete_Events = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Delete_Events_w_KM_Calendar"]
    Vacation_Use_Variable = BooleanVar(master=Frame, value=Vacation_Enabled)
    Vacation_All_Variable = StringVar(master=Frame, value=Vacation_All_Day)
    Vacation_Part_Variable = StringVar(master=Frame, value=Vacation_Part_Day)
    Vacation_Delete_Events_Variable = BooleanVar(master=Frame, value=Vacation_Delete_Events)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#    
    # Widget
    Vacation_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Special - Vacation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Vacation.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Vacation_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Vacation_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Vacation_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Vacation", "Use"])
    Search_Text_Vacation_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Vacation_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Search text", Value=Vacation_Search_Text, placeholder_text="Event Subject which defines vacation", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Vacation", "Search_Text"])
    All_Day_Vacation_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Vacation_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="All Day", Variable=Vacation_All_Variable, Values=Vacation_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Vacation", "All_Day"], GUI_Level_ID=GUI_Level_ID) 
    Part_Day_Vacation_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Vacation_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Part Day", Variable=Vacation_Part_Variable, Values=Vacation_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Vacation", "Part_Day"], GUI_Level_ID=GUI_Level_ID) 
    Delete_Events_Vacation_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Vacation_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Delete Events w Working H.", Variable=Vacation_Delete_Events_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Vacation", "Delete_Events_w_KM_Calendar"])

    # Add Fields to Widget Body
    Vacation_Widget.Add_row(Rows=[Use_Vacation_Row, Delete_Events_Vacation_Row, Search_Text_Vacation_Row, All_Day_Vacation_Row, Part_Day_Vacation_Row])

    return Vacation_Widget

def Settings_Events_General_SickDay(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    SickDay_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Use"]
    SickDay_Search_Text = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Search_Text"]
    SickDay_All_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["All_Day"]
    SickDay_Part_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Part_Day"]
    SickDay_Day_Option_List = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["SickDay_Option_List"]
    SickDay_Delete_Events = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Delete_Events_w_KM_Calendar"]
    SickDay_Use_Variable = BooleanVar(master=Frame, value=SickDay_Enabled)
    SickDay_All_Variable = StringVar(master=Frame, value=SickDay_All_Day)
    SickDay_Part_Variable = StringVar(master=Frame, value=SickDay_Part_Day)
    SickDay_Delete_Events_Variable = BooleanVar(master=Frame, value=SickDay_Delete_Events)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    SickDay_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Special - SickDay", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of SickDay", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_SickDay_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=SickDay_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=SickDay_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "SickDay", "Use"])
    Search_Text_SickDay_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=SickDay_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Search text", Value=SickDay_Search_Text, placeholder_text="Event Subject which defines SickDay.", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "SickDay", "Search_Text"])
    All_Day_SickDay_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=SickDay_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="All Day", Variable=SickDay_All_Variable, Values=SickDay_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "SickDay", "All_Day"], GUI_Level_ID=GUI_Level_ID) 
    Part_Day_SickDay_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=SickDay_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Part Day", Variable=SickDay_Part_Variable, Values=SickDay_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "SickDay", "Part_Day"], GUI_Level_ID=GUI_Level_ID) 
    Delete_Events_SickDay_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=SickDay_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Delete Events w Working H.", Variable=SickDay_Delete_Events_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "SickDay", "Delete_Events_w_KM_Calendar"])

    # Add Fields to Widget Body
    SickDay_Widget.Add_row(Rows=[Use_SickDay_Row, Delete_Events_SickDay_Row, Search_Text_SickDay_Row, All_Day_SickDay_Row, Part_Day_SickDay_Row])

    return SickDay_Widget

def Settings_Events_General_HomeOffice(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    HomeOffice_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Use"]
    HomeOffice_Search_Text = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Search_Text"]
    HomeOffice_All_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["All_Day"]
    HomeOffice_Part_Day = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Part_Day"]
    HomeOffice_Day_Option_List = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["HomeOffice_Option_List"]
    HomeOffice_Use_Variable = BooleanVar(master=Frame, value=HomeOffice_Enabled)
    HomeOffice_All_Variable = StringVar(master=Frame, value=HomeOffice_All_Day)
    HomeOffice_Part_Variable = StringVar(master=Frame, value=HomeOffice_Part_Day)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    HomeOffice_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Special - HomeOffice", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of HomeOffice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_HomeOffice_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=HomeOffice_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=HomeOffice_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "HomeOffice", "Use"])
    Search_Text_HomeOffice_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=HomeOffice_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Search text", Value=HomeOffice_Search_Text, placeholder_text="Event Subject which defines home office.", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "HomeOffice", "Search_Text"])
    All_Day_HomeOffice_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=HomeOffice_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="All Day", Variable=HomeOffice_All_Variable, Values=HomeOffice_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "HomeOffice", "All_Day"], GUI_Level_ID=GUI_Level_ID) 
    Part_Day_HomeOffice_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=HomeOffice_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Part Day", Variable=HomeOffice_Part_Variable, Values=HomeOffice_Day_Option_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "HomeOffice", "Part_Day"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    HomeOffice_Widget.Add_row(Rows=[Use_HomeOffice_Row, Search_Text_HomeOffice_Row, All_Day_HomeOffice_Row, Part_Day_HomeOffice_Row])

    return HomeOffice_Widget

def Settings_Events_General_Private(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Private_Enabled = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]["Use"]
    Private_Search_Text = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]["Search_Text"]
    Private_Method = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]["Method"]
    Private_Method_List = Settings["0"]["Event_Handler"]["Events"]["Special_Events"]["Private"]["Private_Option_List"]
    Private_Use_Variable = BooleanVar(master=Frame, value=Private_Enabled)
    Private_Method_Variable = StringVar(master=Frame, value=Private_Method)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Widget
    Private_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Special - Private", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Special Event Private, \n Split --> Special Event will split parallel events, like Lunch \n Do nothing --> This event will not do anything to parallel events.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Private_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Private_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Private_Use_Variable, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Private", "Use"])
    Search_Text_Private_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Private_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Search text", Value=Private_Search_Text, placeholder_text="Event Subject which defines private special event.", Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Private", "Search_Text"])
    Method_Private_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Private_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Private_Method_Variable, Values=Private_Method_List, Save_To="Settings", Save_path=["0", "Event_Handler", "Events", "Special_Events", "Private", "Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Private_Widget.Add_row(Rows=[Use_Private_Row, Search_Text_Private_Row, Method_Private_Row])

    return Private_Widget

# -------------------------------------------------------------------------- Tab Events - Empty --------------------------------------------------------------------------#
def Settings_Events_Empty_Generally(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Activity", "Description", "Coverage Percentage"]
    Events_Empty_General_dict = Settings["0"]["Event_Handler"]["Events"]["Empty"]["General"]

    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    if not Project_List:
        Project_Variable = StringVar(master=Frame, value="")
    else:
        Project_Variable = StringVar(master=Frame, value=Project_List[0])

    Activity_All_List = list(Settings["0"]["Event_Handler"]["Activity"]["Activity_List"])
    Activity_All_List.insert(0, " ") # Because there might be not filled one in Calendar
    Activity_All_List.sort()
    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])

    # ------------------------- Local Functions -------------------------#
    def Add_Empty_Event(Header_List: list, Frame_Empty_General_Table_Var: CTkTable, Subject_Text_Text_Var: CTkEntry, Project_Option_Var1: CTkOptionMenu, Activity_Option_Var1: CTkOptionMenu, Coverage_Text_Var: CTkEntry) -> None:
        Add_flag = True
        # Load single values
        Add_Description = Subject_Text_Text_Var.get()
        Add_Project = Project_Option_Var1.get()
        Add_Activity = Activity_Option_Var1.get()
        Add_Coverage = Coverage_Text_Var.get()
        Add_row = [Add_Project, Add_Activity, Add_Description, Add_Coverage]

        Check_List = Frame_Empty_General_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)

        # Values checkers
        try:
            Add_Coverage = int(Add_Coverage)
            if Add_Coverage > 0 and Add_Coverage <= 100:
                pass
            else:
                Add_flag = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Coverage must be between 0 - 100, please check it.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        except:
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Coverage is not whole number, check it.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # Not To add same line
        if Add_flag == True:
            for Empty_Event in Check_List:
                if Empty_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Rule already exists with Fill Empty.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_flag == True:
            Frame_Empty_General_Table_Var.add_row(values=Add_row)
            
            # Save to Settings.json
            Empty_General_Events = Frame_Empty_General_Table_Var.values
            Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
            Empty_General_Events = Update_empty_information(Check_List=Empty_General_Events)

            General_dict = {}
            Counter = 0
            for Empty_General_Events_row in Empty_General_Events:
                Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                General_dict[Counter] = Empty_General_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "General"], Information=General_dict)
        else:
            pass
    
    def Del_Empty_Event_One(Header_List: list, Frame_Empty_General_Table_Var: CTkTable, Button_Empty_Del_One_Var: CTkButton) -> None:
        def Delete_One_Confirm(Frame_Empty_General_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_Empty_General_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Empty_General_Events = Frame_Empty_General_Table_Var.values
            Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
            Empty_General_Events = Update_empty_information(Check_List=Empty_General_Events)

            General_dict = {}
            Counter = 0
            for Empty_General_Events_row in Empty_General_Events:
                Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                General_dict[Counter] = Empty_General_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "General"], Information=General_dict)
            Delete_One_Close()

        def Delete_One_Close() -> None:
            Delete_One_Window.destroy()

        def Update_Labels_Texts(Line_Selected: int, Frame_Empty_General_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, Coverage_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=Line_Selected)
            Selected_Project = Frame_Empty_General_Table_Var.get(row=Line_Selected, column=0)
            Selected_Activity = Frame_Empty_General_Table_Var.get(row=Line_Selected, column=1)
            Selected_Description = Frame_Empty_General_Table_Var.get(row=Line_Selected, column=2)
            Selected_Coverage = Frame_Empty_General_Table_Var.get(row=Line_Selected, column=3)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            Coverage_Label_Var.configure(text=Selected_Coverage)

        # calculate number of lines in table
        Empty_General_Events = Frame_Empty_General_Table_Var.values
        Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
        Lines_No = len(Empty_General_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_One_Window_geometry = (510, 260)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Empty_Del_One_Var, New_Window_width=Delete_One_Window_geometry[0])
        Delete_One_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete one line", max_width=Delete_One_Window_geometry[0], max_height=Delete_One_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_One_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=2))
        Coverage_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Coverage") 
        Coverage_Label_Var = Coverage_Label.children["!ctkframe3"].children["!ctklabel"]
        Coverage_Label_Var.configure(text=Frame_Empty_General_Table_Var.get(row=1, column=3))

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Coverage_Label_Var=Coverage_Label_Var), GUI_Level_ID=GUI_Level_ID + 1)

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_One_Confirm(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_One_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

    def Del_Empty_Event_All(Frame_Empty_General_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_General_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_General_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "General"], Information={})

    def Recalculate_Empty_Event(Header_List: list, Frame_Empty_General_Table_Var: CTkTable, Button_Empty_Recalculate_Var: CTkButton) -> None:
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
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Not everything is Integer. 1 - 100 without decimal.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            # Check if equal 100
            if Add_flag == True:
                Values_sum = sum(New_Values_list)
                if Values_sum == 100:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Sum of all lines not equal 100, please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
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
                Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "General"], Information=General_dict)

                Recalculation_Reject()
            else:
                pass

        def Recalculation_Reject() -> None:
            Recalculate_window.destroy()

        # calculate number of lines in table
        Empty_General_Events = Frame_Empty_General_Table_Var.values
        Empty_General_Events = [i for i in Empty_General_Events if i != Header_List]
        Lines_No = len(Empty_General_Events)

        Recalculate_window_height = (Lines_No * 40) + 100

        Recalculate_window_geometry = (510, Recalculate_window_height)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Empty_Recalculate_Var, New_Window_width=Recalculate_window_geometry[0])
        Recalculate_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Recalculate", max_width=Recalculate_window_geometry[0], max_height=Recalculate_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Recalculate_window, Name="Recalculate coverage", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Helps to recalculate Coverage percentage so sum is equal 100", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        for line in range(0, Lines_No):
            # Field - Monday
            Fields_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label=f"Line {line}", Validation="Integer") 
            Var1 = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
            Var1.configure(placeholder_text=Empty_General_Events[line][3])
            Var1.configure(state="disabled")

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Recalculation_Confirm(Frame_Body=Frame_Body, Lines_No=Lines_No))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm coverage change.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Recalculation_Reject())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

    def Save_Empty():
        # Copy Settings file into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Empty_Events",
            "Data": Events_Empty_General_dict}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Empty_Events", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Empty Events logic has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Empty(Button_Load_Empty: CTkButton):
        def Empty_drop_func(file):
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Empty_Events", JSON_path=["0", "Event_Handler", "Events", "Empty", "General"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Frame_Empty_General_Table_Var, JSON_path=["0", "Event_Handler", "Events", "Empty", "General"])
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_Empty, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=Empty_drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Empty Space coverage Events", Additional_Text="Sum of Coverage Percentage must equal 100%.", Widget_size="Triple_size", Widget_Label_Tooltip="For empty space (between Events in calendar) program use fill them by this setup.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)

    # Empty Events table
    Skip_Event_General_list = [Header_List]
    Events_Empty_General_dict_rows = Events_Empty_General_dict.items()
    for Sub_Row in Events_Empty_General_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_General_list.append(list(Sub_dict.values()))

    Frame_Empty_General_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Column_B, Table_Size="Double_size", Table_Values=Skip_Event_General_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_Event_General_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Empty_General_Table_Var = Frame_Empty_General_Table.children["!ctktable"]
    Frame_Empty_General_Table_Var.configure(wraplength=230)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var1 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var1.configure(variable=Project_Variable)

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var1 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var1.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var1, values=Project_List, command = lambda Project_Option_Var1: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var1, Activity_Option_Var=Activity_Option_Var1, Project_Variable=Project_Variable, GUI_Level_ID=GUI_Level_ID), GUI_Level_ID=GUI_Level_ID)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var1, values=[], command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Coverage
    Coverage_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Coverage", Field_Type="Input_Normal", Validation="Integer") 
    Coverage_Text_Var = Coverage_Text.children["!ctkframe3"].children["!ctkentry"]
    Coverage_Text_Var.configure(placeholder_text="Add %")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Empty_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Empty_Add_Var.configure(text="Add", command = lambda:Add_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var1=Project_Option_Var1, Activity_Option_Var1=Activity_Option_Var1, Coverage_Text_Var=Coverage_Text_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Add_Var, message="Add selected subject to skip list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Empty_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Empty_Del_One_Var.configure(text="Del", command = lambda:Del_Empty_Event_One(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Button_Empty_Del_One_Var=Button_Empty_Del_One_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Empty_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Empty_Del_All_Var.configure(text="Del all", command = lambda:Del_Empty_Event_All(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Frame2 = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Save_Empty = Button_Frame2.children["!ctkframe"].children["!ctkbutton"]
    Button_Save_Empty.configure(text="Export", command = lambda:Save_Empty())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Empty, message="Save table content.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Load_Empty = Button_Frame2.children["!ctkframe"].children["!ctkbutton2"]
    Button_Load_Empty.configure(text="Import", command = lambda:Load_Empty(Button_Load_Empty=Button_Load_Empty))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Empty, message="Load and add new records to table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Empty_Recalculate_Var = Button_Frame2.children["!ctkframe"].children["!ctkbutton3"]
    Button_Empty_Recalculate_Var.configure(text="Recalcul.", command = lambda:Recalculate_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Button_Empty_Recalculate_Var=Button_Empty_Recalculate_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Recalculate_Var, message="Recalculate coverage for all lines.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    return Frame_Main



def Settings_Events_Empty_Schedule(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Activity", "Description", "Day of Week", "Start", "End"]
    Events_Empty_Schedules_dict = Settings["0"]["Event_Handler"]["Events"]["Empty"]["Scheduled"]

    Format_Time = Settings["0"]["General"]["Formats"]["Time"]

    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    if not Project_List:
        Project_Variable = StringVar(master=Frame, value="")
    else:
        Project_Variable = StringVar(master=Frame, value=Project_List[0])


    Activity_All_List = list(Settings["0"]["Event_Handler"]["Activity"]["Activity_List"])
    Activity_All_List.insert(0, " ") # Because there might be not filled one in Calendar
    Activity_All_List.sort()
    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])

    Mon_Var = IntVar(master=Frame, value=0)
    Tue_Var = IntVar(master=Frame, value=0)
    Wed_Var = IntVar(master=Frame, value=0)
    Thu_Var = IntVar(master=Frame, value=0)
    Fri_Var = IntVar(master=Frame, value=0)
    Sat_Var = IntVar(master=Frame, value=0)
    Sun_Var = IntVar(master=Frame, value=0)

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
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You didn't select any day of week, please update.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # Time Checkers
        if Add_flag == True:
            try:
                Add_Start_Time_dt = datetime.strptime(Add_Start_Time, Format_Time)
                Add_End_Time_dt = datetime.strptime(Add_End_Time, Format_Time)

                if Add_End_Time_dt > Add_Start_Time_dt:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="End Time is before/equal to Start Time, please correct", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            except:
                Add_flag = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="One of the time is not actually time, please correct", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        # Not To add same line
        if Add_flag == True:
            for Schedule_Event in Check_List:
                if Schedule_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Rule already exists with Fill Empty.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_flag == True:
            Frame_Empty_Schedules_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Schedule_Events = Frame_Empty_Schedules_Table_Var.values
            Schedule_Events = [i for i in Schedule_Events if i != Header_List]
            Schedule_Events = Update_empty_information(Check_List=Schedule_Events)

            Scheduled_dict = {}
            Counter = 0
            for Schedule_Events_row in Schedule_Events:
                Schedule_Events_row_dict = dict(zip(Header_List, Schedule_Events_row))
                Scheduled_dict[Counter] = Schedule_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "Scheduled"], Information=Scheduled_dict)
        else:
            pass

    def Del_Schedule_Event_One(Header_List: list, Frame_Empty_Schedules_Table_Var: CTkTable, Button_Schedule_Del_One_Var: CTkButton) -> None:
        def Delete_Schedule_Confirm(Frame_Empty_Schedules_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_Empty_Schedules_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Empty_Scheduled_Events = Frame_Empty_Schedules_Table_Var.values
            Empty_Scheduled_Events = [i for i in Empty_Scheduled_Events if i != Header_List]
            Empty_Scheduled_Events = Update_empty_information(Check_List=Empty_Scheduled_Events)

            Scheduled_dict = {}
            Counter = 0
            for Empty_Scheduled_Events_row in Empty_Scheduled_Events:
                Empty_Scheduled_Events_row_dict = dict(zip(Header_List, Empty_Scheduled_Events_row))
                Scheduled_dict[Counter] = Empty_Scheduled_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "Scheduled"], Information=Scheduled_dict)
            Delete_Schedule_Close()

        def Delete_Schedule_Close() -> None:
            Delete_Scheduled_Window.destroy()

        def Update_Labels_Texts(Line_Selected: int, Frame_Empty_Schedules_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, WeekDays_Label_Var: CTkLabel, Start_Label_Var: CTkLabel, End_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=Line_Selected)
            Selected_Project = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=0)
            Selected_Activity = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=1)
            Selected_Description = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=2)
            Selected_WeekDays = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=3)
            Selected_Start = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=4)
            Selected_End = Frame_Empty_Schedules_Table_Var.get(row=Line_Selected, column=5)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            WeekDays_Label_Var.configure(text=Selected_WeekDays)
            Start_Label_Var.configure(text=Selected_Start)
            End_Label_Var.configure(text=Selected_End)

        # calculate number of lines in table
        Empty_Scheduled_Events = Frame_Empty_Schedules_Table_Var.values
        Empty_Scheduled_Events = [i for i in Empty_Scheduled_Events if i != Header_List]
        Lines_No = len(Empty_Scheduled_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_Scheduled_Window_geometry = (510, 400)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Schedule_Del_One_Var, New_Window_width=Delete_Scheduled_Window_geometry[0])
        Delete_Scheduled_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete one scheduled line", max_width=Delete_Scheduled_Window_geometry[0], max_height=Delete_Scheduled_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Scheduled_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=2))
        WeekDays_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Day of Week") 
        WeekDays_Label_Var = WeekDays_Label.children["!ctkframe3"].children["!ctklabel"]
        WeekDays_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=3))
        Start_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Start") 
        Start_Label_Var = Start_Label.children["!ctkframe3"].children["!ctklabel"]
        Start_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=4))
        End_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="End") 
        End_Label_Var = End_Label.children["!ctkframe3"].children["!ctklabel"]
        End_Label_Var.configure(text=Frame_Empty_Schedules_Table_Var.get(row=1, column=5))

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, WeekDays_Label_Var=WeekDays_Label_Var, Start_Label_Var=Start_Label_Var, End_Label_Var=End_Label_Var), GUI_Level_ID=GUI_Level_ID + 1)

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Schedule_Confirm(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Schedule_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

    def Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_Schedules_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_Schedules_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Empty", "Scheduled"], Information={})

    def Save_Scheduler():
        # Copy Settings file into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Scheduler",
            "Data": Events_Empty_Schedules_dict}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Scheduler", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Scheduler has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Scheduler(Button_Load_Scheduler: CTkButton):
        def Scheduler_drop_func(file):
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Scheduler", JSON_path=["0", "Event_Handler", "Events", "Empty", "Scheduled"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Frame_Empty_Schedules_Table_Var, JSON_path=["0", "Event_Handler", "Events", "Empty", "Scheduled"])
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_Scheduler, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=Scheduler_drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Events Scheduler", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple TimeSheet Entry planner.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)

    # Scheduled Events table
    Skip_Event_Schedule_list = [Header_List]
    Skip_Event_Schedule_dict_rows = Events_Empty_Schedules_dict.items()
    for Sub_Row in Skip_Event_Schedule_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_Schedule_list.append(list(Sub_dict.values()))

    Frame_Empty_Schedules_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Column_B, Table_Size="Double_size", Table_Values=Skip_Event_Schedule_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_Event_Schedule_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Empty_Schedules_Table_Var = Frame_Empty_Schedules_Table.children["!ctktable"]
    Frame_Empty_Schedules_Table_Var.configure(wraplength=150)

    # Field - Week Days
    Week_Days_Label = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Column_A, Label_Size="Column_Header", Font_Size="Column_Header")
    Week_Days_Label.configure(text="Week Days")
    Week_Days_Label.pack_propagate(flag=False)

    Week_Days_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column")
    Week_Days_Frame.configure(width=300)
    Week_Days_Label.pack(side="top", fill="none", expand=False, padx=10, pady=10)
    Week_Days_Frame.pack(side="top", fill="none", expand=False, padx=0, pady=0)

    Monday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Mon") 
    Monday_Check_Frame_Var = Monday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Monday_Check_Frame_Var.configure(variable=Mon_Var, text="")

    Tuesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Tue") 
    Tuesday_Check_Frame_Var = Tuesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Tuesday_Check_Frame_Var.configure(variable=Tue_Var, text="")

    Wednesday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Wed") 
    Wednesday_Check_Frame_Var = Wednesday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Wednesday_Check_Frame_Var.configure(variable=Wed_Var, text="")

    Thursday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Thu") 
    Thursday_Check_Frame_Var = Thursday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Thursday_Check_Frame_Var.configure(variable=Thu_Var, text="")

    Friday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Fri") 
    Friday_Check_Frame_Var = Friday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Friday_Check_Frame_Var.configure(variable=Fri_Var, text="")

    Saturday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sat") 
    Saturday_Check_Frame_Var = Saturday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Saturday_Check_Frame_Var.configure(variable=Sat_Var, text="")

    Sunday_Check_Frame = Elements_Groups.Get_Vertical_Field_Input(Configuration=Configuration, Frame=Week_Days_Frame, Field_Frame_Type="Vertical_CheckBox" , Label="Sun") 
    Sunday_Check_Frame_Var = Sunday_Check_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Sunday_Check_Frame_Var.configure(variable=Sun_Var, text="")

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var2 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var2.configure(variable=Project_Variable)
    
    # Field - Activity --> placed before project because of variable to be used
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var2 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var2.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var2, values=Project_List, command = lambda Project_Option_Var2: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var2, Activity_Option_Var=Activity_Option_Var2, Project_Variable=Project_Variable, GUI_Level_ID=GUI_Level_ID), GUI_Level_ID=GUI_Level_ID)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var2, values=Activity_All_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Start Time
    Start_Time_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Start Time", Field_Type="Input_Normal", Validation="Time") 
    Start_Time_Text_Var = Start_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    Start_Time_Text_Var.configure(placeholder_text="HH:MM")

    # Field - End Time
    End_Time_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="End Time", Field_Type="Input_Normal", Validation="Time") 
    End_Time_Text_Var = End_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    End_Time_Text_Var.configure(placeholder_text="HH:MM")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Buttons_count=5, Button_Size="Small") 
    Button_Schedule_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Schedule_Add_Var.configure(text="Add", command = lambda:Add_Schedule_Event(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var2=Project_Option_Var2, Activity_Option_Var2=Activity_Option_Var2, Start_Time_Text_Var=Start_Time_Text_Var, End_Time_Text_Var=End_Time_Text_Var, Monday_Check_Frame_Var=Monday_Check_Frame_Var, Tuesday_Check_Frame_Var=Tuesday_Check_Frame_Var, Wednesday_Check_Frame_Var=Wednesday_Check_Frame_Var, Thursday_Check_Frame_Var=Thursday_Check_Frame_Var, Friday_Check_Frame_Var=Friday_Check_Frame_Var, Saturday_Check_Frame_Var=Saturday_Check_Frame_Var, Sunday_Check_Frame_Var=Sunday_Check_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Schedule_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Schedule_Del_One_Var.configure(text="Del", command = lambda:Del_Schedule_Event_One(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Button_Schedule_Del_One_Var=Button_Schedule_Del_One_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Schedule_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Schedule_Del_All_Var.configure(text="Del all", command = lambda:Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Save_Scheduler = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Save_Scheduler.configure(text="Export", command = lambda:Save_Scheduler())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Scheduler, message="Save table content.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Load_Scheduler = Button_Frame.children["!ctkframe"].children["!ctkbutton5"]
    Button_Load_Scheduler.configure(text="Import", command = lambda:Load_Scheduler(Button_Load_Scheduler=Button_Load_Scheduler))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Scheduler, message="Load and add new records to table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Monday_Check_Frame.pack(side="left", padx=5, pady=5)
    Tuesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Wednesday_Check_Frame.pack(side="left", padx=5, pady=5)
    Thursday_Check_Frame.pack(side="left", padx=5, pady=5)
    Friday_Check_Frame.pack(side="left", padx=5, pady=5)
    Saturday_Check_Frame.pack(side="left", padx=5, pady=5)
    Sunday_Check_Frame.pack(side="left", padx=5, pady=5)

    return Frame_Main

# -------------------------------------------------------------------------- Tab Events - Rules --------------------------------------------------------------------------#
def Settings_Events_AutoFill(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Search Text", "Project", "Activity", "Location"]
    AutoFill_Rules_Enabled = Settings["0"]["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Use"]
    Events_AutoFill_dict = Settings["0"]["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Dictionary"]

    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    Project_All_List = Project_List
    Project_All_List.insert(0, " ") # Because there might be not filled one in Calendar

    Activity_All_List = list(Settings["0"]["Event_Handler"]["Activity"]["Activity_List"])
    Activity_All_List.insert(0, " ") # Because there might be not filled one in Calendar
    Activity_All_List.sort()

    Location_List = Settings["0"]["Event_Handler"]["Location"]["Location_List"]

    AutoFill_Use_Variable = BooleanVar(master=Frame, value=AutoFill_Rules_Enabled)
    Project_Variable = StringVar(master=Frame, value=Project_All_List[0])

    Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])
    Location_Variable = StringVar(master=Frame, value=Location_List[0])

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
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Search Text is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
        
        # Not To add same line -->  consider only Search text
        if Add_flag == True:
            for AutoFill_Event in Check_List:
                if AutoFill_Event[0] != Add_row[0]:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Rule with Search text already exists with Auto-filler.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        if Add_flag == True:
            Frame_AutoFiller_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Auto_Fill_Events = Frame_AutoFiller_Table_Var.values
            Auto_Fill_Events = [i for i in Auto_Fill_Events if i != Header_List]
            Auto_Fill_Events = Update_empty_information(Check_List=Auto_Fill_Events)

            AutoFill_dict = {}
            Counter = 0
            for Auto_Fill_Events_row in Auto_Fill_Events:
                Auto_Fill_Events_row_row_dict = dict(zip(Header_List, Auto_Fill_Events_row))
                AutoFill_dict[Counter] = Auto_Fill_Events_row_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information=AutoFill_dict)
        else:
            pass
        
    def Del_AutoFill_Event_One(Button_AutoFill_Del_One_Var: CTkButton) -> None:
        def Delete_AutoFill_Confirm(Frame_AutoFiller_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_AutoFiller_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            AutoFill_Events = Frame_AutoFiller_Table_Var.values
            AutoFill_Events = [i for i in AutoFill_Events if i != Header_List]
            AutoFill_Events = Update_empty_information(Check_List=AutoFill_Events)

            AutoFill_dict = {}
            Counter = 0
            for AutoFill_Events_row in AutoFill_Events:
                AutoFill_Events_row_dict = dict(zip(Header_List, AutoFill_Events_row))
                AutoFill_dict[Counter] = AutoFill_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information=AutoFill_dict)
            Delete_AutoFill_Close()

        def Delete_AutoFill_Close() -> None:
            Delete_AutoFill_Window.destroy()

        def Update_Labels_Texts(Line_Selected: int, Frame_AutoFiller_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Activity_Label_Var: CTkLabel, Description_Label_Var: CTkLabel, Location_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=Line_Selected)
            Selected_Project = Frame_AutoFiller_Table_Var.get(row=Line_Selected, column=0)
            Selected_Activity = Frame_AutoFiller_Table_Var.get(row=Line_Selected, column=1)
            Selected_Description = Frame_AutoFiller_Table_Var.get(row=Line_Selected, column=2)
            Selected_Location = Frame_AutoFiller_Table_Var.get(row=Line_Selected, column=3)

            Project_Label_Var.configure(text=Selected_Project)
            Activity_Label_Var.configure(text=Selected_Activity)
            Description_Label_Var.configure(text=Selected_Description)
            Location_Label_Var.configure(text=Selected_Location)

        # calculate number of lines in table
        AutoFill_Events = Frame_AutoFiller_Table_Var.values
        AutoFill_Events = [i for i in AutoFill_Events if i != Header_List]
        Lines_No = len(AutoFill_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_AutoFill_Window_geometry = (510, 260)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_AutoFill_Del_One_Var, New_Window_width=Delete_AutoFill_Window_geometry[0])
        Delete_AutoFill_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete one line", max_width=Delete_AutoFill_Window_geometry[0], max_height=Delete_AutoFill_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_AutoFill_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project: ") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=0))
        Activity_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Activity: ") 
        Activity_Label_Var = Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Activity_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=1))
        Description_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description: ") 
        Description_Label_Var = Description_Label.children["!ctkframe3"].children["!ctklabel"]
        Description_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=2))
        Location_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Location: ") 
        Location_Label_Var = Location_Label.children["!ctkframe3"].children["!ctklabel"]
        Location_Label_Var.configure(text=Frame_AutoFiller_Table_Var.get(row=1, column=3))

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Location_Label_Var=Location_Label_Var), GUI_Level_ID=GUI_Level_ID + 1)

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_AutoFill_Confirm(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_AutoFill_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

    def Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_AutoFiller_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_AutoFiller_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information={})

    def Save_AutoFill():
        # Copy Settings file into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Rules",
            "Data": Events_AutoFill_dict}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Rules", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Rules has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_AutoFill(Button_Load_AutoFill: CTkButton):
        def AutoFill_drop_func(file):
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Rules", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Frame_AutoFiller_Table_Var, JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"])
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_AutoFill, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=AutoFill_drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="AutoFill rules", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple rules applied on TimeSheet Entry if part/whole Search Text is found in Subject. If empty then do not fill it or overwrite it.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)

    # AutoFilling Table
    Skip_AutoFill_list = [Header_List]
    Events_AutoFill_dict_rows = Events_AutoFill_dict.items()
    for Sub_Row in Events_AutoFill_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_AutoFill_list.append(list(Sub_dict.values()))

    Frame_AutoFiller_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Column_B, Table_Size="Double_size", Table_Values=Skip_AutoFill_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_AutoFill_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_AutoFiller_Table_Var = Frame_AutoFiller_Table.children["!ctktable"]
    Frame_AutoFiller_Table_Var.configure(wraplength=230)

    # Field - Use
    Use_AutoFill = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_AutoFill_Var = Use_AutoFill.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_AutoFill_Var.configure(variable=AutoFill_Use_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=AutoFill_Use_Variable, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Search_Text", "Use"], Information=AutoFill_Use_Variable))

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Search Text", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(variable=Project_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Activity --> really from list of all Activity, because rule can be without Project 
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(variable=Activity_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var, values=Activity_All_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Location
    Location_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Location", Field_Type="Input_OptionMenu") 
    Location_Option_Var = Location_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Location_Option_Var.configure(variable=Location_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Location_Option_Var, values=Location_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Buttons_count=5, Button_Size="Small") 
    Button_AutoFill_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_AutoFill_Add_Var.configure(text="Add", command = lambda:Add_AutoFill_Event(Header_List=Header_List, Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var=Project_Option_Var, Activity_Option_Var=Activity_Option_Var, Location_Option_Var=Location_Option_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_AutoFill_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_AutoFill_Del_One_Var.configure(text="Del", command = lambda:Del_AutoFill_Event_One(Button_AutoFill_Del_One_Var=Button_AutoFill_Del_One_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_AutoFill_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_AutoFill_Del_All_Var.configure(text="Del all", command = lambda:Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Save_AutoFill = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Save_AutoFill.configure(text="Export", command = lambda:Save_AutoFill())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_AutoFill, message="Save table content.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Load_AutoFill = Button_Frame.children["!ctkframe"].children["!ctkbutton5"]
    Button_Load_AutoFill.configure(text="Import", command = lambda:Load_AutoFill(Button_Load_AutoFill=Button_Load_AutoFill))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_AutoFill, message="Load and add new records to table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    return Frame_Main


def Settings_Events_Activity_Correction(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Wrong Activity", "Correct Activity"]
    Events_Activity_Correction_Enabled = Settings["0"]["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Use"]
    Events_Activity_Correction_dict = Settings["0"]["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Dictionary"]
    Activity_Correction_Use_Variable = BooleanVar(master=Frame, value=Events_Activity_Correction_Enabled)

    Project_dict = Settings["0"]["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    if not Project_List:
        Project_Variable = StringVar(master=Frame, value="")
    else:
        Project_Variable = StringVar(master=Frame, value=Project_List[0])


    Activity_All_List = list(Settings["0"]["Event_Handler"]["Activity"]["Activity_List"])
    Activity_All_List.insert(0, " ") # Because there might be not filled one in Calendar
    Activity_All_List.sort()

    Wrong_Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])
    Correct_Activity_Variable = StringVar(master=Frame, value=Activity_All_List[0])

    # ------------------------- Local Functions -------------------------#
    def Add_Activity_Correct_Event(Header_List: list, Frame_Activity_Correct_Table_Var: CTkTable, Project_Option_Var: CTkOptionMenu, Wrong_Activity_Option_Var: CTkOptionMenu, Correct_Activity_Option_Var: CTkOptionMenu) -> None:
        Add_flag = True
        # Load single values
        Add_Project = Project_Option_Var.get()
        Add_Wrong_Activity = Wrong_Activity_Option_Var.get()
        Add_Correct_Activity = Correct_Activity_Option_Var.get()

        Check_List = Frame_Activity_Correct_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)
        Add_row = [Add_Project, Add_Wrong_Activity, Add_Correct_Activity]

        # Values checkers --> all must be inserted
        if Add_Project == " ":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Project is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_Wrong_Activity == " ":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Wrong Activity is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_Correct_Activity == " ":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Correct Activity is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
        
        # Not To add same line -->  consider only Search text
        if Add_flag == True:
            for AutoFill_Event in Check_List:
                if AutoFill_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Rule with all combination already exists with Events Corrections.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        if Add_flag == True:
            Frame_Activity_Correct_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Activity_Corrections_Events = Frame_Activity_Correct_Table_Var.values
            Activity_Corrections_Events = [i for i in Activity_Corrections_Events if i != Header_List]
            Activity_Corrections_Events = Update_empty_information(Check_List=Activity_Corrections_Events)

            Activity_Correction_dict = {}
            Counter = 0
            for Activity_Corrections_Events_row in Activity_Corrections_Events:
                Activity_Corrections_Events_row_dict = dict(zip(Header_List, Activity_Corrections_Events_row))
                Activity_Correction_dict[Counter] = Activity_Corrections_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information=Activity_Correction_dict)
        else:
            pass

    def Del_Activity_Correct_Event_One(Button_Activity_Cor_Del_One_Var: CTkButton):
        def Delete_Activity_Correct_Confirm(Frame_Activity_Correct_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Frame_Activity_Correct_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Activity_Corrections_Events = Frame_Activity_Correct_Table_Var.values
            Activity_Corrections_Events = [i for i in Activity_Corrections_Events if i != Header_List]
            Activity_Corrections_Events = Update_empty_information(Check_List=Activity_Corrections_Events)

            Activity_Correction_dict = {}
            Counter = 0
            for Activity_Corrections_Events_row in Activity_Corrections_Events:
                Activity_Corrections_Events_row_dict = dict(zip(Header_List, Activity_Corrections_Events_row))
                Activity_Correction_dict[Counter] = Activity_Corrections_Events_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information=Activity_Correction_dict)
            Delete_Activity_Correct_Close()

        def Delete_Activity_Correct_Close() -> None:
            Delete_Activity_Correct_Window.destroy()

        def Update_Labels_Texts(Line_Selected: int, Frame_Activity_Correct_Table_Var: CTkTable, Project_Label_Var: CTkLabel, Wrong_Activity_Label_Var: CTkLabel, Correct_Activity_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=Line_Selected)
            Selected_Project = Frame_Activity_Correct_Table_Var.get(row=Line_Selected, column=0)
            Selected_Wrong_Activity = Frame_Activity_Correct_Table_Var.get(row=Line_Selected, column=1)
            Selected_Correct_Activity = Frame_Activity_Correct_Table_Var.get(row=Line_Selected, column=2)

            Project_Label_Var.configure(text=Selected_Project)
            Wrong_Activity_Label_Var.configure(text=Selected_Wrong_Activity)
            Correct_Activity_Label_Var.configure(text=Selected_Correct_Activity)

        # calculate number of lines in table
        Activity_Corrections_Events = Frame_Activity_Correct_Table_Var.values
        Activity_Corrections_Events = [i for i in Activity_Corrections_Events if i != Header_List]
        Lines_No = len(Activity_Corrections_Events)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_Activity_Correct_Window_geometry = (510, 250)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Activity_Cor_Del_One_Var, New_Window_width=Delete_Activity_Correct_Window_geometry[0])
        Delete_Activity_Correct_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete one Activity", max_width=Delete_Activity_Correct_Window_geometry[0], max_height=Delete_Activity_Correct_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Activity_Correct_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Field - Project Label
        Project_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Project: ") 
        Project_Label_Var = Project_Label.children["!ctkframe3"].children["!ctklabel"]
        Project_Label_Var.configure(text=Frame_Activity_Correct_Table_Var.get(row=1, column=0))
        Wrong_Activity_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Wrong Activity: ") 
        Wrong_Activity_Label_Var = Wrong_Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Wrong_Activity_Label_Var.configure(text=Frame_Activity_Correct_Table_Var.get(row=1, column=1))
        Correct_Activity_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Correct Activity: ") 
        Correct_Activity_Label_Var = Correct_Activity_Label.children["!ctkframe3"].children["!ctklabel"]
        Correct_Activity_Label_Var.configure(text=Frame_Activity_Correct_Table_Var.get(row=1, column=2))

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Wrong_Activity_Label_Var=Wrong_Activity_Label_Var, Correct_Activity_Label_Var=Correct_Activity_Label_Var), GUI_Level_ID=GUI_Level_ID + 1)

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Activity_Correct_Confirm(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Activity_Correct_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)


    def Del_Activity_Correct_Event_all(Frame_Activity_Correct_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Activity_Correct_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Activity_Correct_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information={})

    def Save_Activity_Correct():
        # Copy Settings file into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Activity_Correction",
            "Data": Events_Activity_Correction_dict}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Activity_Correction", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Activity corrections has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Activity_Correct(Button_Load_Activity_Correct: CTkButton):
        def Activity_Correct_drop_func(file):
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Activity_Correction", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Frame_Activity_Correct_Table_Var, JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"])
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_Activity_Correct, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=Activity_Correct_drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Activity correction", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Change Activity in the processing of Events, when non-proper activity for Project is selected in calendar.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)

    # AutoFilling Table
    Activity_Correction_list = [Header_List]
    Events_Activity_Correction_dict_rows = Events_Activity_Correction_dict.items()
    for Sub_Row in Events_Activity_Correction_dict_rows:
        Sub_dict = Sub_Row[1]
        Activity_Correction_list.append(list(Sub_dict.values()))

    Frame_Activity_Correct_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Column_B, Table_Size="Double_size", Table_Values=Activity_Correction_list, Table_Columns=len(Header_List), Table_Rows=len(Activity_Correction_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Activity_Correct_Table_Var = Frame_Activity_Correct_Table.children["!ctktable"]
    Frame_Activity_Correct_Table_Var.configure(wraplength=310)

    # Field - Use
    Use_Activity_Correction = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Activity_Correction_Var = Use_Activity_Correction.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Activity_Correction_Var.configure(variable=Activity_Correction_Use_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=Activity_Correction_Use_Variable, File_Name="Settings", JSON_path=["0", "Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Use"], Information=Activity_Correction_Use_Variable))

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(variable=Project_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Activity --> really from list of all Activity, because rule have to be set per with all possible activity
    Wrong_Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Wrong Activity", Field_Type="Input_OptionMenu") 
    Wrong_Activity_Option_Var = Wrong_Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Wrong_Activity_Option_Var.configure(variable=Wrong_Activity_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Wrong_Activity_Option_Var, values=Activity_All_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Activity --> placed before project because of variable to be used
    Correct_Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Correct Activity", Field_Type="Input_OptionMenu") 
    Correct_Activity_Option_Var = Correct_Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Correct_Activity_Option_Var.configure(variable=Correct_Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command = lambda Project_Option_Var: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var, Activity_Option_Var=Correct_Activity_Option_Var, Project_Variable=Project_Variable, GUI_Level_ID=GUI_Level_ID), GUI_Level_ID=GUI_Level_ID)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Correct_Activity_Option_Var, values=Activity_All_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Buttons_count=5, Button_Size="Small") 
    Button_Activity_Cor_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Activity_Cor_Add_Var.configure(text="Add", command = lambda:Add_Activity_Correct_Event(Header_List=Header_List, Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, Project_Option_Var=Project_Option_Var, Wrong_Activity_Option_Var=Wrong_Activity_Option_Var, Correct_Activity_Option_Var=Correct_Activity_Option_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Activity_Cor_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Activity_Cor_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Activity_Cor_Del_One_Var.configure(text="Del", command = lambda:Del_Activity_Correct_Event_One(Button_Activity_Cor_Del_One_Var=Button_Activity_Cor_Del_One_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Activity_Cor_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Activity_Cor_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Activity_Cor_Del_All_Var.configure(text="Del all", command = lambda:Del_Activity_Correct_Event_all(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Activity_Cor_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Save_Activity_Correct = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Save_Activity_Correct.configure(text="Export", command = lambda:Save_Activity_Correct())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Activity_Correct, message="Save table content.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Load_Activity_Correct = Button_Frame.children["!ctkframe"].children["!ctkbutton5"]
    Button_Load_Activity_Correct.configure(text="Import", command = lambda:Load_Activity_Correct(Button_Load_Activity_Correct=Button_Load_Activity_Correct))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Activity_Correct, message="Load and add new records to table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    return Frame_Main


def Settings_My_Team(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Managed_Team_dict = Settings["0"]["General"]["User"]["Managed_Team"]
    Header_List = ["User Team", "User ID", "User Name"]
    SP_Teams_List = list(Settings["0"]["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_List"])
    User_SP_Team_Variable = StringVar(master=Frame, value=SP_Teams_List[0])


    # ------------------------- Local Functions -------------------------#

    def Add_Team_User(Header_List: list, Frame_Managed_Team_Table_Var: CTkTable, MT_SP_Teams_Frame_Var: CTkOptionMenu, MT_User_ID_Frame_Var: CTkEntry, MT_User_Name_Frame_Var: CTkEntry) -> None:
        Add_flag = True
        # Load single values
        Add_SP_Team = MT_SP_Teams_Frame_Var.get()
        Add_User_ID = MT_User_ID_Frame_Var.get()
        Add_User_Name = MT_User_Name_Frame_Var.get()

        Check_List = Frame_Managed_Team_Table_Var.values
        Check_List = Update_empty_information(Check_List=Check_List)
        Add_row = [Add_SP_Team, Add_User_ID, Add_User_Name]

        # Values checkers --> all must be inserted
        if Add_SP_Team == " ":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Sharepoint list is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_User_ID == "":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="User ID list is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        if Add_User_Name == "":
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="User Name list is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
       
        # Not To add same line --> consider only User within same 
        if Add_flag == True:
            for User_row in Check_List:
                if User_row != Add_row:
                    pass
                else:
                    Add_flag = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="The member is already exists in registered members..", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        if Add_flag == True:
            Frame_Managed_Team_Table_Var.add_row(values=Add_row)

            # Save to Settings.json
            Managed_Team_Users = Frame_Managed_Team_Table_Var.values
            Managed_Team_Users = [i for i in Managed_Team_Users if i != Header_List]
            Managed_Team_Users = Update_empty_information(Check_List=Managed_Team_Users)

            Managed_Users_dict = {}
            Counter = 0
            for Managed_Team_Users_row in Managed_Team_Users:
                Managed_Team_Users_row_dict = dict(zip(Header_List, Managed_Team_Users_row))
                Managed_Users_dict[Counter] = Managed_Team_Users_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Managed_Team"], Information=Managed_Users_dict)
            File_Manipulation.Create_Folder(Configuration=Configuration, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team\\{Add_User_ID}"))
        else:
            pass

    def Del_Team_User_One(Button_MT_Del_One_Var: CTkButton):
        def Delete_Managed_Member_Confirm(Frame_Managed_Team_Table_Var: CTkTable, LineNo_Option_Var: CTkOptionMenu, User_ID_Label_Var: CTkLabel) -> None:
            Selected_Line_To_Del = LineNo_Option_Var.get()
            Delete_Folder_Name = User_ID_Label_Var.cget(attribute_name="text")
            Frame_Managed_Team_Table_Var.delete_row(index=Selected_Line_To_Del)

            # Save to Settings.json
            Managed_Team_Users = Frame_Managed_Team_Table_Var.values
            Managed_Team_Users = [i for i in Managed_Team_Users if i != Header_List]
            Managed_Team_Users = Update_empty_information(Check_List=Managed_Team_Users)

            Managed_Users_dict = {}
            Counter = 0
            for Managed_Team_Users_row in Managed_Team_Users:
                Managed_Team_Users_row_dict = dict(zip(Header_List, Managed_Team_Users_row))
                Managed_Users_dict[Counter] = Managed_Team_Users_row_dict
                Counter += 1
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Managed_Team"], Information=Managed_Users_dict)
            Folder_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team\\{Delete_Folder_Name}")
            File_Manipulation.Delete_All_Files(Configuration=Configuration, window=window, file_path=Folder_Path, include_hidden=True)
            File_Manipulation.Delete_Folder(Configuration=Configuration, window=window, file_path=Folder_Path)
            Delete_Managed_Member_Close()   

        def Delete_Managed_Member_Close() -> None:
            Delete_Managed_User_Window.destroy()

        def Update_Labels_Texts(Line_Selected: int, Frame_Managed_Team_Table_Var: CTkTable, User_Team_Label_Var: CTkLabel, User_ID_Label_Var: CTkLabel, User_Name_Label_Var: CTkLabel) -> None:
            Line_Option_Variable.set(value=Line_Selected)
            Selected_Team = Frame_Managed_Team_Table_Var.get(row=Line_Selected, column=0)
            Selected_User_ID = Frame_Managed_Team_Table_Var.get(row=Line_Selected, column=1)
            Selected_User_Name = Frame_Managed_Team_Table_Var.get(row=Line_Selected, column=2)

            User_Team_Label_Var.configure(text=Selected_Team)
            User_ID_Label_Var.configure(text=Selected_User_ID)
            User_Name_Label_Var.configure(text=Selected_User_Name)

        # calculate number of lines in table
        Managed_Team_Users = Frame_Managed_Team_Table_Var.values
        Managed_Team_Users = [i for i in Managed_Team_Users if i != Header_List]
        Lines_No = len(Managed_Team_Users)
        Lines_list = [x for x in range(1, Lines_No + 1)] # Must skip Headers
        Line_Option_Variable = IntVar(master=Frame, value=Lines_list[0])

        # TopUp Window
        Delete_Managed_User_Window_geometry = (510, 250)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_MT_Del_One_Var, New_Window_width=Delete_Managed_User_Window_geometry[0])
        Delete_Managed_User_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete one User", max_width=Delete_Managed_User_Window_geometry[0], max_height=Delete_Managed_User_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Managed_User_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
        LineNo_Option_Var = LineNo_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
        LineNo_Option_Var.configure(variable=Line_Option_Variable)

        # Fields - Labels
        User_Team_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Team: ") 
        User_Team_Label_Var = User_Team_Label.children["!ctkframe3"].children["!ctklabel"]
        User_Team_Label_Var.configure(text=Frame_Managed_Team_Table_Var.get(row=1, column=0))
        User_ID_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID: ") 
        User_ID_Label_Var = User_ID_Label.children["!ctkframe3"].children["!ctklabel"]
        User_ID_Label_Var.configure(text=Frame_Managed_Team_Table_Var.get(row=1, column=1))
        User_Name_Label = Elements_Groups.Get_Double_Label(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Name: ") 
        User_Name_Label_Var = User_Name_Label.children["!ctkframe3"].children["!ctklabel"]
        User_Name_Label_Var.configure(text=Frame_Managed_Team_Table_Var.get(row=1, column=2))

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, Line_Selected=Line_Selected, User_Team_Label_Var=User_Team_Label_Var, User_ID_Label_Var=User_ID_Label_Var, User_Name_Label_Var=User_Name_Label_Var), GUI_Level_ID=GUI_Level_ID + 1) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Managed_Member_Confirm(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, LineNo_Option_Var=LineNo_Option_Var, User_ID_Label_Var=User_ID_Label_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Managed_Member_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)


    def Del_Team_User_all(Frame_Managed_Team_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Managed_Team_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Managed_Team_Table_Var.delete_row(index=Table_index)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Managed_Team"], Information={})
        File_Manipulation.Delete_Folders(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team"))

    def Save_MT():
        # Save My_Team Dict into Downloads Folder
        Export_dict = {
            "Type": "TimeSheets_Team",
            "Data": Managed_Team_dict}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Team", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Managed Team has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_MT(Button_Load_MT: CTkButton):
        def MT_drop_func(file: str) -> None:
            response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Question", message=f"Do you want to overwrite data or add them?", icon="question", fade_in_duration=1, option_1="Overwrite", option_2="Add", GUI_Level_ID=1)
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="TimeSheets_Team", JSON_path=["0", "General", "User", "Managed_Team"], Method=response)
            CustomTkinter_Functions.Insert_Data_to_Table(Settings=Settings, Configuration=Configuration, window=window, Table=Frame_Managed_Team_Table_Var, JSON_path=["0", "General", "User", "Managed_Team"])
            Import_window.destroy()  
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message=f"Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_MT, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=GUI_Level_ID + 1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=lambda file: MT_drop_func(file=file))
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID + 1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="My managed team", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Add / del user from my team, users are then visible on Managed Team dashboard.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)

    # My team Table
    Managed_Team_list = [Header_List]
    Managed_Team_dict_rows = Managed_Team_dict.items()
    for Sub_Row in Managed_Team_dict_rows:
        Sub_dict = Sub_Row[1]
        Managed_Team_list.append(list(Sub_dict.values()))

    Frame_Managed_Team_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Column_B, Table_Size="Double_size", Table_Values=Managed_Team_list, Table_Columns=len(Header_List), Table_Rows=len(Managed_Team_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Managed_Team_Table_Var = Frame_Managed_Team_Table.children["!ctktable"]
    Frame_Managed_Team_Table_Var.configure(wraplength=310)

    # Field - Managed Team SP List
    MT_SP_Teams_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Managed Team", Field_Type="Input_OptionMenu") 
    MT_SP_Teams_Frame_Var = MT_SP_Teams_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    MT_SP_Teams_Frame_Var.configure(variable=User_SP_Team_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=MT_SP_Teams_Frame_Var, values=SP_Teams_List, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Managed Team User ID
    MT_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Member ID", Field_Type="Input_Normal") 
    MT_User_ID_Frame_Var = MT_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    MT_User_ID_Frame_Var.configure(placeholder_text="Team member ID")

    # Field - Managed Team User ID
    MT_User_Name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, Field_Frame_Type="Single_Column" , Label="Member Name", Field_Type="Input_Normal") 
    MT_User_Name_Frame_Var = MT_User_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    MT_User_Name_Frame_Var.configure(placeholder_text="Team member Name")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Column_A, Configuration=Configuration, Field_Frame_Type="Single_Column" , Buttons_count=5, Button_Size="Small") 
    Button_MT_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_MT_Add_Var.configure(text="Add", command = lambda:Add_Team_User(Header_List=Header_List, Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, MT_SP_Teams_Frame_Var=MT_SP_Teams_Frame_Var, MT_User_ID_Frame_Var=MT_User_ID_Frame_Var, MT_User_Name_Frame_Var=MT_User_Name_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_MT_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_MT_Del_One_Var.configure(text="Del", command = lambda:Del_Team_User_One(Button_MT_Del_One_Var=Button_MT_Del_One_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_MT_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_MT_Del_All_Var.configure(text="Del all", command = lambda:Del_Team_User_all(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Save_Mt = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Save_Mt.configure(text="Export", command = lambda: Save_MT())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Mt, message="Save table content.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Load_MT = Button_Frame.children["!ctkframe"].children["!ctkbutton5"]
    Button_Load_MT.configure(text="Import", command = lambda: Load_MT(Button_Load_MT=Button_Load_MT))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_MT, message="Load and add new records to table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    return Frame_Main
