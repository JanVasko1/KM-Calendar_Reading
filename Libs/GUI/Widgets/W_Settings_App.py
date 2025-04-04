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
    Accent_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["App Default", "Windows", "Manual"], Freeze_fields=[[Accent_Color_Manual_Row],[Accent_Color_Manual_Row],[]])
    Accent_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Accent Color Mode", Variable=Accent_Color_Mode_Variable, Values=Accent_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Field_list=[Accent_Color_Manual_Row], Field_Blocking_dict=Accent_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Hover_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Appearance_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Hover color", Label_Size="Field_Label", Font_Size="Section_Separator")
    Hover_Color_Manual_Row = WidgetRow_Color_Picker(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Manual", Value=Hover_Color_Manual, placeholder_text_color="#949A9F", Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Button_ToolTip="Color Picker.", Picker_Always_on_Top=True, Picker_Fixed_position=True, GUI_Level_ID=GUI_Level_ID + 1)
    Hover_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["App Default", "Accent Lighter", "Manual"], Freeze_fields=[[Hover_Color_Manual_Row],[Hover_Color_Manual_Row],[]])
    Hover_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Mode", Variable=Hover_Color_Mode_Variable, Values=Hover_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Field_list=[Hover_Color_Manual_Row], Field_Blocking_dict=Hover_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

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
