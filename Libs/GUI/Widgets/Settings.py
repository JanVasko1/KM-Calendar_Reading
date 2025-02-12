# Import Libraries
from datetime import datetime

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import pywinstyles
import customtkinter
from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, BooleanVar, CTkToplevel, CTkOptionMenu, CTkButton, CTkCheckBox, CTkLabel
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox

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

def Check_Time_Continuation(Settings: dict, Configuration: dict, Format_Time: str, Start_Time: CTkEntry, End_Time: CTkEntry, Week_Day: str, Type: str) -> bool:
    Start_Time_dt = datetime.strptime(Start_Time.get(), Format_Time)
    End_Time_dt = datetime.strptime(End_Time.get(), Format_Time)
    if Start_Time_dt >= End_Time_dt:
        CTkMessagebox(title="Error", message=f"You entered same or sooner time as Start time, this is not compatible, please correct it. This value is not to be saved.", icon="cancel", fade_in_duration=1)
    else:
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", f"{Week_Day}", f"{Type}", "End_Time"], Information=End_Time.get())


def Retrieve_Activity_based_on_Type(Settings: dict, Configuration:dict, Project_Option_Var: CTkOptionMenu, Activity_Option_Var: CTkOptionMenu, Project_Variable: StringVar) -> None:
    Activity_by_Type_dict = Settings["Event_Handler"]["Activity"]["Activity_by_Type_dict"]
    Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]

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
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var, values=Activity_List, command=None)

def Calculate_duration(Settings: dict, Configuration: dict, Entry_Field: CTkEntry, Lunch_Brake_Duration_Frame_Var: int, Calendar_Type: str, Monday_Start: CTkEntry, Monday_End: CTkEntry, Tuesday_Start: CTkEntry, Tuesday_End: CTkEntry, Wednesday_Start: CTkEntry, Wednesday_End: CTkEntry, Thursday_Start: CTkEntry, Thursday_End: CTkEntry, Friday_Start: CTkEntry, Friday_End: CTkEntry, Saturday_Start: CTkEntry, Saturday_End: CTkEntry, Sunday_Start: CTkEntry, Sunday_End: CTkEntry) -> None:
    Format_Time = Settings["General"]["Formats"]["Time"]
    Monday_Working_day = Settings["General"]["Calendar"]["Monday"]["Working_Day"]
    Tuesday_Working_day = Settings["General"]["Calendar"]["Tuesday"]["Working_Day"]
    Wednesday_Working_day = Settings["General"]["Calendar"]["Wednesday"]["Working_Day"]
    Thursday_Working_day = Settings["General"]["Calendar"]["Thursday"]["Working_Day"]
    Friday_Working_day = Settings["General"]["Calendar"]["Friday"]["Working_Day"]
    Saturday_Working_day = Settings["General"]["Calendar"]["Saturday"]["Working_Day"]
    Sunday_Working_day = Settings["General"]["Calendar"]["Sunday"]["Working_Day"]


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
                Duration = Duration - Lunch_Brake_Duration_Frame_Var
            else:
                pass

        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", f"{Week_Day}", f"{Calendar_Type}", "Day_Duration"], Information=Duration)
        return Duration
    
    Cumulated_Duration = 0
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Monday_Start.get(), End_Time=Monday_End.get(), Week_Day="Monday", Calendar_Type=Calendar_Type, Working_Day=Monday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Tuesday_Start.get(), End_Time=Tuesday_End.get(), Week_Day="Tuesday", Calendar_Type=Calendar_Type, Working_Day=Tuesday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Wednesday_Start.get(), End_Time=Wednesday_End.get(), Week_Day="Wednesday", Calendar_Type=Calendar_Type, Working_Day=Wednesday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Thursday_Start.get(), End_Time=Thursday_End.get(), Week_Day="Thursday", Calendar_Type=Calendar_Type, Working_Day=Thursday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Friday_Start.get(), End_Time=Friday_End.get(), Week_Day="Friday", Calendar_Type=Calendar_Type, Working_Day=Friday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Saturday_Start.get(), End_Time=Saturday_End.get(), Week_Day="Saturday", Calendar_Type=Calendar_Type, Working_Day=Saturday_Working_day)
    Cumulated_Duration = Cumulated_Duration + Calculate_day_duration(Start_Time=Sunday_Start.get(), End_Time=Sunday_End.get(), Week_Day="Sunday", Calendar_Type=Calendar_Type, Working_Day=Sunday_Working_day)

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
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Totals", "Work"], Information=Total_Duration)
    elif Calendar_Type == "Vacation":
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Totals", "Vacation"], Information=Total_Duration)
    else:
        CTkMessagebox(title="Error", message="Calendar Type not allowed", icon="cancel", fade_in_duration=1)



# -------------------------------------------------------------------------- Tab Appearance --------------------------------------------------------------------------#
def Settings_General_Theme(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, window: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
    Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
    Win_Style_List = list(Configuration["Global_Appearance"]["Window"]["Style_List"])

    # ------------------------- Local Functions ------------------------#
    def Appearance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        customtkinter.set_appearance_mode(mode_string=Theme_Frame_Var)
        Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Theme_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Theme"], Information=Theme_Frame_Var)

    def Appearance_Change_Win_Style(Win_Style_Selected: str, window: CTk|CTkFrame) -> None:
        # Base Windows style setup --> always keep normal before change
        pywinstyles.apply_style(window=window, style="normal")
        pywinstyles.apply_style(window=window, style=Win_Style_Selected)
        Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Win_Style_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Style"], Information=Win_Style_Selected)

    # ------------------------- Main Functions -------------------------#
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Win_Style_Variable = StringVar(master=Frame, value=Win_Style_Actual)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="General Appearance", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="General Appearance settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Appearance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var))

    # Field - Windows Style
    Win_Style_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Window Style", Field_Type="Input_OptionMenu") 
    Win_Style_Frame_Var = Win_Style_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Win_Style_Frame_Var.configure(variable=Win_Style_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Win_Style_Frame_Var, values=Win_Style_List, command= lambda Win_Style_Selected: Appearance_Change_Win_Style(Win_Style_Selected=Win_Style_Selected, window=window))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Color(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

    # ------------------------- Local Functions ------------------------#
    def Settings_Disabling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            CTkMessagebox(title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1)

    def Appearance_Pick_Manual_Color(Color_Manual_Frame_Var: CTkEntry, Helper: str) -> None:
        def Quit_Save(Helper: str):
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Color_Picker_Frame.get())
            Color_Picker_window.destroy()

        def drag_win():
            x = Color_Picker_window.winfo_pointerx() - Color_Picker_window._offsetx
            y = Color_Picker_window.winfo_pointery() - Color_Picker_window._offsety
            Color_Picker_window.geometry(f"+{x}+{y}")

        def click_win():
            Color_Picker_window._offsetx = Color_Picker_window.winfo_pointerx() - Color_Picker_window.winfo_rootx()
            Color_Picker_window._offsety = Color_Picker_window.winfo_pointery() - Color_Picker_window.winfo_rooty()

            
        Color_Picker_window = CTkToplevel()
        #Color_Picker_window.configure(fg_color="#000001")
        Color_Picker_window.title("Color Picker")
        Color_Picker_window.geometry("295x240")
        Color_Picker_window.bind(sequence="<Escape>", func=lambda event: Quit_Save(Helper=Helper))
        #Color_Picker_window.bind(sequence="<Button-1>", func=lambda event:click_win())
        #Color_Picker_window.bind(sequence="<B1-Motion>", func=lambda event:drag_win())
        #Color_Picker_window.overrideredirect(boolean=True)
        Color_Picker_window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        Color_Picker_window.resizable(width=False, height=False)

        # Rounded corners 
        #Color_Picker_window.config(background="#000001")
        #Color_Picker_window.attributes("-transparentcolor", "#000001")

        Color_Picker_Frame = Elements.Get_Color_Picker(Configuration=Configuration, Frame=Color_Picker_window, Color_Manual_Frame_Var=Color_Manual_Frame_Var)

        # Build look of Widget --> must be before inset
        Color_Picker_Frame.pack(padx=0, pady=0) 

    # ------------------------- Main Functions -------------------------#
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Colors", Additional_Text="Applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Input_Normal") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual, placeholder_text_color="#949A9F")
    Accent_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Information=Accent_Color_Manual_Frame_Var.get()))

    # Button - Color Picker
    Accent_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Accent_Color_Picker_Button_Var = Accent_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Accent_Color_Picker_Button_Var.configure(text="Accent Color Picker", command = lambda :Appearance_Pick_Manual_Color(Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Accent_Color_Picker_Button_Var, message="Select manually Accent color.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"))
    Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")  # Must be here because of initial value

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Input_Normal") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual, placeholder_text_color="#949A9F")
    Hover_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Information=Hover_Color_Manual_Frame_Var.get()))

    # Button - Color Picker
    Hover_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Hover_Color_Picker_Button_Var = Hover_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Hover_Color_Picker_Button_Var.configure(text="Hover Color Picker", command = lambda:Appearance_Pick_Manual_Color(Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Hover_Color_Picker_Button_Var, message="Select manually Hover Color.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"))
    Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")   # Must be here because of initial value

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Settings_User_Widget(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    User_Name = Settings["General"]["User"]["Name"]
    User_ID = Settings["General"]["User"]["Code"]
    User_Email = Settings["General"]["User"]["Email"]
    User_Type = Settings["General"]["User"]["User_Type"]
    User_Type_list = list(Settings["General"]["User"]["User_Type_list"])
    
    # ------------------------- Local Functions ------------------------#
    def Password_required(User_Type_Variable: StringVar, User_Type_Frame_Var: str) -> None:
        def Dialog_Window_Request(title: str, text: str, Dialog_Type: str) -> str|None:
            # Password required
            dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
            Password = dialog.get_input()
            return Password
        
        if User_Type_Frame_Var == "User":
            User_Type_Variable.value = "User"
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=User_Type_Variable, File_Name="Settings", JSON_path=["General", "User", "User_Type"], Information=User_Type_Frame_Var)
        elif User_Type_Frame_Var == "Manager":
            Password = Dialog_Window_Request(title="Admin", text="Write your password", Dialog_Type="Password")

            if Password == "JVA_is_best":
                User_Type_Variable.value = "Manager"
                Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=User_Type_Variable, File_Name="Settings", JSON_path=["General", "User", "User_Type"], Information=User_Type_Frame_Var)
            else:
                User_Type_Variable.value = "User"
                CTkMessagebox(title="Error", message=f"Wrong administration password.", icon="cancel", fade_in_duration=1)
           

    # ------------------------- Main Functions -------------------------#
    User_Type_Variable = StringVar(master=Frame, value=User_Type)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="User", Additional_Text="Maintained by admin", Widget_size="Single_size", Widget_Label_Tooltip="This is setup of definition if user is considerate as user or user leading team with additional functionality.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - User ID
    User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Konica ID", Field_Type="Input_Normal")
    User_ID_Frame_Var = User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_ID_Frame_Var.configure(placeholder_text="My Konica ID.")
    User_ID_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Code"], Information=User_ID_Frame_Var.get()))
    Entry_field_Insert(Field=User_ID_Frame_Var, Value=User_ID)

    # Field - Name
    User_Name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Name", Field_Type="Input_Normal") 
    User_Name_Frame_Var = User_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_Name_Frame_Var.configure(placeholder_text="My Name.")
    User_Name_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Name"], Information=User_Name_Frame_Var.get()))
    Entry_field_Insert(Field=User_Name_Frame_Var, Value=User_Name)

    # Field - User Email
    User_Email_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Email", Field_Type="Input_Normal")
    User_Email_Frame_Var = User_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_Email_Frame_Var.configure(placeholder_text="My Konica ID.")
    User_Email_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Email"], Information=User_Email_Frame_Var.get()))
    Entry_field_Insert(Field=User_Email_Frame_Var, Value=User_Email)

    # Field - User Type
    User_Type_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Type ", Field_Type="Input_OptionMenu") 
    User_Type_Frame_Var = User_Type_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    User_Type_Frame_Var.configure(variable=User_Type_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=User_Type_Frame_Var, values=User_Type_list, command=lambda User_Type_Frame_Var: Password_required(User_Type_Variable=User_Type_Variable, User_Type_Frame_Var=User_Type_Frame_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab GEneral --------------------------------------------------------------------------#
def Settings_General_Sharepoint(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    SP_Auth_Address = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Auth_Address"]   
    SP_File_Name = Settings["General"]["Downloader"]["Sharepoint"]["File_name"]
    SP_Team = Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["My_Team"]
    SP_Teams_List = list(Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_List"])
    SP_Team_Variable = StringVar(master=Frame, value=SP_Team)

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Sharepoint", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Sharepoint related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Team
    SP_Team_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Team", Field_Type="Input_OptionMenu") 
    SP_Team_Frame_Var = SP_Team_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    SP_Team_Frame_Var.configure(variable=SP_Team_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=SP_Team_Frame_Var, values=SP_Teams_List, command=lambda SP_Team_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=SP_Team_Variable, File_Name="Settings", JSON_path=["General", "Downloader", "Sharepoint", "Teams", "My_Team"], Information=SP_Team_Frame_Var))

    # Field - File Name 
    SP_File_Name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="File Name", Field_Type="Input_Normal")
    SP_File_Name_Frame_Var = SP_File_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_File_Name_Frame_Var.configure(placeholder_text=SP_File_Name, placeholder_text_color="#949A9F")
    SP_File_Name_Frame_Var.configure(state="disabled")

    # Field - Auth Address
    SP_Auth_Address_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Auth Address", Field_Type="Input_Normal")
    SP_Auth_Address_Frame_Var = SP_Auth_Address_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Auth_Address_Frame_Var.configure(placeholder_text=SP_Auth_Address, placeholder_text_color="#949A9F")
    SP_Auth_Address_Frame_Var.configure(state="disabled")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Exchange(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
    Category_Color = Settings["Event_Handler"]["Project"]["Colors"]["Used"]
    Category_Color_list = list(Settings["Event_Handler"]["Project"]["Colors"]["Color_List"])
    Category_Color_Variable = StringVar(master=Frame, value=Category_Color)


    # ------------------------- Local Functions ------------------------#
    def Exchange_ReNew_Secret() -> None:
        print("Exchange_ReNew_Secret")
        # TODO --> show new popup and let fill password to let automatically be re-generated
        pass

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Exchange", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Exchange Server related settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Category Color
    Category_Color_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Category Color", Field_Type="Input_OptionMenu") 
    Category_Color_Frame_Var = Category_Color_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Category_Color_Frame_Var.configure(variable=Category_Color_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Category_Color_Frame_Var, values=Category_Color_list, command=lambda Category_Color_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Category_Color_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Project", "Colors", "Used"], Information=Category_Color_Frame_Var))

    # Field - Name
    EX_Client_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client ID", Field_Type="Input_Normal") 
    EX_Client_ID_Frame_Var = EX_Client_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Client_ID_Frame_Var.configure(placeholder_text=client_id, placeholder_text_color="#949A9F")
    EX_Client_ID_Frame_Var.configure(state="disabled")

    # Field - User ID
    Ex_Client_Secret_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Secret", Field_Type="Input_Normal")
    Ex_Client_Secret_Frame_Var = Ex_Client_Secret_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Client_Secret_Frame_Var.configure(placeholder_text=client_secret)
    Ex_Client_Secret_Frame_Var.configure(state="disabled", placeholder_text_color="#949A9F")

    # Field - Path to Sharepoint
    EX_Tenant_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tenant ID", Field_Type="Input_Normal")
    EX_Tenant_ID_Frame_Var = EX_Tenant_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    EX_Tenant_ID_Frame_Var.configure(placeholder_text=tenant_id)
    EX_Tenant_ID_Frame_Var.configure(state="disabled", placeholder_text_color="#949A9F")

    # Update Secret ID Button
    Button_Update_Secret = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Button_Update_Secret_Var = Button_Update_Secret.children["!ctkframe"].children["!ctkbutton"]
    Button_Update_Secret_Var.configure(text="Re-new Secret", command = lambda:Exchange_ReNew_Secret())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Update_Secret_Var, message="Update Secret ID.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Settings_General_Formats(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Date = Settings["General"]["Formats"]["Date"]
    Format_Time = Settings["General"]["Formats"]["Time"]
    Format_Exchange_DateTime = Settings["General"]["Formats"]["Exchange_DateTime"]
    Format_Sharepoint_Date = Settings["General"]["Formats"]["Sharepoint_Date"]
    Format_Sharepoint_Time = Settings["General"]["Formats"]["Sharepoint_Time"]
    Format_Sharepoint_DateTime = Settings["General"]["Formats"]["Sharepoint_DateTime"]

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Formats", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Dates formats used in program - non-changeable.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Program Date Format
    Program_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date", Field_Type="Input_Normal") 
    Program_Date_Frame_Var = Program_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Program_Date_Frame_Var.configure(placeholder_text=Format_Date, placeholder_text_color="#949A9F")
    Program_Date_Frame_Var.configure(state="disabled")

    # Field - Program Time Format
    Program_Time_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Time", Field_Type="Input_Normal")
    Program_Time_Frame_Var = Program_Time_Frame.children["!ctkframe3"].children["!ctkentry"]
    Program_Time_Frame_Var.configure(placeholder_text=Format_Time, placeholder_text_color="#949A9F")
    Program_Time_Frame_Var.configure(state="disabled")

    # Field - Exchange DateTime Format
    Exchange_DateTime_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Exchange DateTime", Field_Type="Input_Normal")
    Exchange_DateTime_Frame_Var = Exchange_DateTime_Frame.children["!ctkframe3"].children["!ctkentry"]
    Exchange_DateTime_Frame_Var.configure(placeholder_text=Format_Exchange_DateTime, placeholder_text_color="#949A9F")
    Exchange_DateTime_Frame_Var.configure(state="disabled")

    # Field - Sharepoint DAte Format
    Sharepoint_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Sharepoint Date", Field_Type="Input_Normal")
    Sharepoint_Date_Frame_Var = Sharepoint_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_Date_Frame_Var.configure(placeholder_text=Format_Sharepoint_Date, placeholder_text_color="#949A9F")
    Sharepoint_Date_Frame_Var.configure(state="disabled")

    # Field - Sharepoint Time Format
    Sharepoint_Time_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Sharepoint Time", Field_Type="Input_Normal")
    Sharepoint_Time_Frame_Var = Sharepoint_Time_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_Time_Frame_Var.configure(placeholder_text=Format_Sharepoint_Time, placeholder_text_color="#949A9F")
    Sharepoint_Time_Frame_Var.configure(state="disabled")

    # Field - Sharepoint Time Format
    Sharepoint_DateTime_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Sharepoint DateTime", Field_Type="Input_Normal")
    Sharepoint_DateTime_Frame_Var = Sharepoint_DateTime_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_DateTime_Frame_Var.configure(placeholder_text=Format_Sharepoint_DateTime, placeholder_text_color="#949A9F")
    Sharepoint_DateTime_Frame_Var.configure(state="disabled")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Parallel_events(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Parallel_Enabled = Settings["Event_Handler"]["Events"]["Parallel_Events"]["Use"]
    Start_Method = Settings["Event_Handler"]["Events"]["Parallel_Events"]["Start_Method"]
    Start_Method_List = Settings["Event_Handler"]["Events"]["Parallel_Events"]["Start_Method_List"]

    Parallel_Use_Variable = BooleanVar(master=Frame, value=Parallel_Enabled)
    Start_Method_Variable = StringVar(master=Frame, value=Start_Method)
    
    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Parallel Events Handler", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definitions of behavior of processing Events when program found that they are parallel.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Parallel_Events = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Parallel_Events_Var = Use_Parallel_Events.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Parallel_Events_Var.configure(variable=Parallel_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Parallel_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Parallel_Events", "Use"], Information=Parallel_Use_Variable))

    # Field - Start Method
    Start_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Same Start Time", Field_Type="Input_OptionMenu") 
    Start_Method_Frame_Var = Start_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Start_Method_Frame_Var.configure(variable=Start_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Start_Method_Frame_Var, values=Start_Method_List, command=lambda Start_Method_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Start_Method_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Parallel_Events", "Start_Method"], Information=Start_Method_Frame_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Join_events(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Join_Events_Enabled = Settings["Event_Handler"]["Events"]["Join_method"]["Use"]
    Join_Methods_List = list(Settings["Event_Handler"]["Events"]["Join_method"]["Methods_List"])
    Join_Free = Settings["Event_Handler"]["Events"]["Join_method"]["Free"]
    Join_Tentative = Settings["Event_Handler"]["Events"]["Join_method"]["Tentative"]
    Join_Busy = Settings["Event_Handler"]["Events"]["Join_method"]["Busy"]
    Join_OutOfOffice = Settings["Event_Handler"]["Events"]["Join_method"]["Out of Office"]
    Join_Work_Else = Settings["Event_Handler"]["Events"]["Join_method"]["Working elsewhere"]

    Join_Use_Variable = BooleanVar(master=Frame, value=Join_Events_Enabled)
    Join_Free_Variable = StringVar(master=Frame, value=Join_Free)
    Join_Tentative_Variable = StringVar(master=Frame, value=Join_Tentative)
    Join_Busy_Variable = StringVar(master=Frame, value=Join_Busy)
    Join_OutOfOffice_Variable = StringVar(master=Frame, value=Join_OutOfOffice)
    Join_Work_Else_Variable = StringVar(master=Frame, value=Join_Work_Else)

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Joining Events", Additional_Text="Under Construction", Widget_size="Single_size", Widget_Label_Tooltip="Joining Events belonging to same Visibility group.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Events_Joining = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Events_Joining_Var = Use_Events_Joining.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Events_Joining_Var.configure(variable=Join_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Use"], Information=Join_Use_Variable))

    # Field - Join Free Events
    Join_Free_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Free", Field_Type="Input_OptionMenu") 
    Join_Free_Frame_Var = Join_Free_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Free_Frame_Var.configure(variable=Join_Free_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Join_Free_Frame_Var, values=Join_Methods_List, command=lambda Join_Free_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_Free_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Free"], Information=Join_Free_Frame_Var))

    # Field - Join Tentative Events
    Join_Tentative_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tentative", Field_Type="Input_OptionMenu") 
    Join_Tentative_Frame_Var = Join_Tentative_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Tentative_Frame_Var.configure(variable=Join_Tentative_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Join_Tentative_Frame_Var, values=Join_Methods_List, command=lambda Join_Tentative_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_Tentative_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Tentative"], Information=Join_Tentative_Frame_Var))

    # Field - Join Busy Events
    Join_Busy_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Busy", Field_Type="Input_OptionMenu") 
    Join_Busy_Frame_Var = Join_Busy_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Busy_Frame_Var.configure(variable=Join_Busy_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Join_Busy_Frame_Var, values=Join_Methods_List, command=lambda Join_Busy_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_Busy_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Busy"], Information=Join_Busy_Frame_Var))

    # Field - Join Out of Office Events
    Join_OutOfOffice_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Out of Office", Field_Type="Input_OptionMenu") 
    Join_OutOfOffice_Frame_Var = Join_OutOfOffice_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_OutOfOffice_Frame_Var.configure(variable=Join_OutOfOffice_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Join_OutOfOffice_Frame_Var, values=Join_Methods_List, command=lambda Join_OutOfOffice_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_OutOfOffice_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Out of Office"], Information=Join_OutOfOffice_Frame_Var))

    # Field - Join Working ElseWhere Events
    Join_Work_ElseWhere_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Working ElseWhere", Field_Type="Input_OptionMenu") 
    Join_Work_ElseWhere_Frame_Var = Join_Work_ElseWhere_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Join_Work_ElseWhere_Frame_Var.configure(variable=Join_Work_Else_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Join_Work_ElseWhere_Frame_Var, values=Join_Methods_List, command=lambda Join_Work_ElseWhere_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Join_Work_Else_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Join_method", "Working elsewhere"], Information=Join_Work_ElseWhere_Frame_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Calendar --------------------------------------------------------------------------#
def Settings_Calendar_Working_Hours(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Time = Settings["General"]["Formats"]["Time"]

    Lunch_Brake_Duration =  Settings["General"]["Calendar"]["Lunch_Brake_Dur"]

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

    Total_Work_Duration =  Settings["General"]["Calendar"]["Totals"]["Work"]

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Calendar - My own calendar", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Setup of my general working hours I usually have. Used for Utilization forecast. Lunch brake automatically subtracted.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Monday
    Monday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday", Validation="Time") 
    Monday_Frame_Var1 = Monday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Monday_Frame_Var1.configure(placeholder_text="Day start time.")
    Monday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Monday", "Work_Hours", "Start_Time"], Information=Monday_Frame_Var1.get()))
    Entry_field_Insert(Field=Monday_Frame_Var1, Value=Monday_Work_Start)
    Monday_Frame_Var2 = Monday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Monday_Frame_Var2.configure(placeholder_text="Day end time.")
    Monday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Monday_Frame_Var1, End_Time=Monday_Frame_Var2, Week_Day="Monday", Type="Work_Hours"))
    Entry_field_Insert(Field=Monday_Frame_Var2, Value=Monday_Work_End)
    

    # Field - Tuesday
    Tuesday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday", Validation="Time") 
    Tuesday_Frame_Var1 = Tuesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Frame_Var1.configure(placeholder_text="Day start time.")
    Tuesday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Tuesday", "Work_Hours", "Start_Time"], Information=Tuesday_Frame_Var1.get()))
    Entry_field_Insert(Field=Tuesday_Frame_Var1, Value=Tuesday_Work_Start)
    Tuesday_Frame_Var2 = Tuesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Frame_Var2.configure(placeholder_text="Day end time.")
    Tuesday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Tuesday_Frame_Var1, End_Time=Tuesday_Frame_Var2, Week_Day="Tuesday", Type="Work_Hours"))
    Entry_field_Insert(Field=Tuesday_Frame_Var2, Value=Tuesday_Work_End)


    # Field - Wednesday
    Wednesday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday", Validation="Time") 
    Wednesday_Frame_Var1 = Wednesday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Frame_Var1.configure(placeholder_text="Day start time.")
    Wednesday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Wednesday", "Work_Hours", "Start_Time"], Information=Wednesday_Frame_Var1.get()))
    Entry_field_Insert(Field=Wednesday_Frame_Var1, Value=Wednesday_Work_Start)
    Wednesday_Frame_Var2 = Wednesday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Frame_Var2.configure(placeholder_text="Day end time.")
    Wednesday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Wednesday_Frame_Var1, End_Time=Wednesday_Frame_Var2, Week_Day="Wednesday", Type="Work_Hours"))
    Entry_field_Insert(Field=Wednesday_Frame_Var2, Value=Wednesday_Work_End)

    # Field - Thursday
    Thursday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday", Validation="Time") 
    Thursday_Frame_Var1 = Thursday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Frame_Var1.configure(placeholder_text="Day start time.")
    Thursday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Thursday", "Work_Hours", "Start_Time"], Information=Thursday_Frame_Var1.get()))
    Entry_field_Insert(Field=Thursday_Frame_Var1, Value=Thursday_Work_Start)
    Thursday_Frame_Var2 = Thursday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Frame_Var2.configure(placeholder_text="Day end time.")
    Thursday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Thursday_Frame_Var1, End_Time=Thursday_Frame_Var2, Week_Day="Thursday", Type="Work_Hours"))
    Entry_field_Insert(Field=Thursday_Frame_Var2, Value=Thursday_Work_End)

    # Field - Friday
    Friday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday", Validation="Time") 
    Friday_Frame_Var1 = Friday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Frame_Var1.configure(placeholder_text="Day start time.")
    Friday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Friday", "Work_Hours", "Start_Time"], Information=Friday_Frame_Var1.get()))
    Entry_field_Insert(Field=Friday_Frame_Var1, Value=Friday_Work_Start)
    Friday_Frame_Var2 = Friday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Frame_Var2.configure(placeholder_text="Day end time.")
    Friday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Friday_Frame_Var1, End_Time=Friday_Frame_Var2, Week_Day="Friday", Type="Work_Hours"))
    Entry_field_Insert(Field=Friday_Frame_Var2, Value=Friday_Work_End)

    # Field - Saturday
    Saturday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday", Validation="Time") 
    Saturday_Frame_Var1 = Saturday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Frame_Var1.configure(placeholder_text="Day start time.")
    Saturday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Saturday", "Work_Hours", "Start_Time"], Information=Saturday_Frame_Var1.get()))
    Entry_field_Insert(Field=Saturday_Frame_Var1, Value=Saturday_Work_Start)
    Saturday_Frame_Var2 = Saturday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Frame_Var2.configure(placeholder_text="Day end time.")
    Saturday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Saturday_Frame_Var1, End_Time=Saturday_Frame_Var2, Week_Day="Saturday", Type="Work_Hours"))
    Entry_field_Insert(Field=Saturday_Frame_Var2, Value=Saturday_Work_End)

    # Field - Sunday
    Sunday_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday", Validation="Time") 
    Sunday_Frame_Var1 = Sunday_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Frame_Var1.configure(placeholder_text="Day start time.")
    Sunday_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Sunday", "Work_Hours", "Start_Time"], Information=Sunday_Frame_Var1.get()))
    Entry_field_Insert(Field=Sunday_Frame_Var1, Value=Sunday_Work_Start)
    Sunday_Frame_Var2 = Sunday_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Frame_Var2.configure(placeholder_text="Day end time.")
    Sunday_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Sunday_Frame_Var1, End_Time=Sunday_Frame_Var2, Week_Day="Sunday", Type="Work_Hours"))
    Entry_field_Insert(Field=Sunday_Frame_Var2, Value=Sunday_Work_End)

    # Field - Lunch Break duration
    Lunch_Brake_Duration_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Lunch brake duration", Field_Type="Input_Normal", Validation="Integer")
    Lunch_Brake_Duration_Frame_Var = Lunch_Brake_Duration_Frame.children["!ctkframe3"].children["!ctkentry"]
    Lunch_Brake_Duration_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Lunch_Brake_Dur"], Information=int(Lunch_Brake_Duration_Frame_Var.get())))
    Entry_field_Insert(Field=Lunch_Brake_Duration_Frame_Var, Value=Lunch_Brake_Duration)

    # Field - Total Time
    Work_Calendar_Total = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Total Time", Field_Type="Input_Normal")
    Work_Calendar_Total_Var = Work_Calendar_Total.children["!ctkframe3"].children["!ctkentry"]
    Work_Calendar_Total_Var.configure(placeholder_text=Total_Work_Duration, placeholder_text_color="#949A9F")
    Work_Calendar_Total_Var.configure(state="disabled")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Button_Skip_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Skip_Add_Var.configure(text="Calculate", command = lambda: Calculate_duration(Settings=Settings, Configuration=Configuration, Entry_Field=Work_Calendar_Total_Var, Lunch_Brake_Duration_Frame_Var=int(Lunch_Brake_Duration_Frame_Var.get()), Calendar_Type="Work_Hours", Monday_Start=Monday_Frame_Var1, Monday_End=Monday_Frame_Var2, Tuesday_Start=Tuesday_Frame_Var1, Tuesday_End=Tuesday_Frame_Var2, Wednesday_Start=Wednesday_Frame_Var1, Wednesday_End=Wednesday_Frame_Var2, Thursday_Start=Thursday_Frame_Var1, Thursday_End=Thursday_Frame_Var2, Friday_Start=Friday_Frame_Var1, Friday_End=Friday_Frame_Var2, Saturday_Start=Saturday_Frame_Var1, Saturday_End=Saturday_Frame_Var2, Sunday_Start=Sunday_Frame_Var1, Sunday_End=Sunday_Frame_Var2))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Skip_Add_Var, message="Calculate total week duration.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Calendar_Vacation(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Format_Time = Settings["General"]["Formats"]["Time"]

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

    Total_Vacation_Duration =  Settings["General"]["Calendar"]["Totals"]["Vacation"]

    # ------------------------- Local Functions ------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Calendar - KM Working/Vacation/SickDay Hours", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="These hours be used in case of whole day vacation.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Monday
    Monday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Monday", Validation="Time") 
    Monday_Vac_Frame_Var1 = Monday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Monday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Monday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Monday", "Vacation", "Start_Time"], Information=Monday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Monday_Vac_Frame_Var1, Value=Monday_Vacation_Start)
    Monday_Vac_Frame_Var2 = Monday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Monday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Monday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Monday_Vac_Frame_Var1, End_Time=Monday_Vac_Frame_Var2, Week_Day="Monday", Type="Vacation"))
    Entry_field_Insert(Field=Monday_Vac_Frame_Var2, Value=Monday_Vacation_End)

    # Field - Tuesday
    Tuesday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Tuesday", Validation="Time") 
    Tuesday_Vac_Frame_Var1 = Tuesday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Tuesday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Tuesday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Tuesday", "Vacation", "Start_Time"], Information=Tuesday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Tuesday_Vac_Frame_Var1, Value=Tuesday_Vacation_Start)
    Tuesday_Vac_Frame_Var2 = Tuesday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Tuesday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Tuesday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Tuesday_Vac_Frame_Var1, End_Time=Tuesday_Vac_Frame_Var2, Week_Day="Tuesday", Type="Vacation"))
    Entry_field_Insert(Field=Tuesday_Vac_Frame_Var2, Value=Tuesday_Vacation_End)

    # Field - Wednesday
    Wednesday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Wednesday", Validation="Time") 
    Wednesday_Vac_Frame_Var1 = Wednesday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Wednesday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Wednesday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Wednesday", "Vacation", "Start_Time"], Information=Wednesday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Wednesday_Vac_Frame_Var1, Value=Wednesday_Vacation_Start)
    Wednesday_Vac_Frame_Var2 = Wednesday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Wednesday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Wednesday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Wednesday_Vac_Frame_Var1, End_Time=Wednesday_Vac_Frame_Var2, Week_Day="Wednesday", Type="Vacation"))
    Entry_field_Insert(Field=Wednesday_Vac_Frame_Var2, Value=Wednesday_Vacation_End)

    # Field - Thursday
    Thursday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Thursday", Validation="Time") 
    Thursday_Vac_Frame_Var1 = Thursday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Thursday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Thursday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Thursday", "Vacation", "Start_Time"], Information=Thursday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Thursday_Vac_Frame_Var1, Value=Thursday_Vacation_Start)
    Thursday_Vac_Frame_Var2 = Thursday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Thursday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Thursday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Thursday_Vac_Frame_Var1, End_Time=Thursday_Vac_Frame_Var2, Week_Day="Thursday", Type="Vacation"))
    Entry_field_Insert(Field=Thursday_Vac_Frame_Var2, Value=Thursday_Vacation_End)

    # Field - Friday
    Friday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Friday", Validation="Time") 
    Friday_Vac_Frame_Var1 = Friday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Friday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Friday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Friday", "Vacation", "Start_Time"], Information=Friday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Friday_Vac_Frame_Var1, Value=Friday_Vacation_Start)
    Friday_Vac_Frame_Var2 = Friday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Friday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Friday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Friday_Vac_Frame_Var1, End_Time=Friday_Vac_Frame_Var2, Week_Day="Friday", Type="Vacation"))
    Entry_field_Insert(Field=Friday_Vac_Frame_Var2, Value=Friday_Vacation_End)

    # Field - Saturday
    Saturday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Saturday", Validation="Time") 
    Saturday_Vac_Frame_Var1 = Saturday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Saturday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Saturday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Saturday", "Vacation", "Start_Time"], Information=Saturday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Saturday_Vac_Frame_Var1, Value=Saturday_Vacation_Start)
    Saturday_Vac_Frame_Var2 = Saturday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Saturday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Saturday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Saturday_Vac_Frame_Var1, End_Time=Saturday_Vac_Frame_Var2, Week_Day="Saturday", Type="Vacation"))
    Entry_field_Insert(Field=Saturday_Vac_Frame_Var2, Value=Saturday_Vacation_End)

    # Field - Sunday
    Sunday_Vac_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label="Sunday", Validation="Time") 
    Sunday_Vac_Frame_Var1 = Sunday_Vac_Frame.children["!ctkframe3"].children["!ctkentry"]
    Sunday_Vac_Frame_Var1.configure(placeholder_text="Day start time.")
    Sunday_Vac_Frame_Var1.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "Calendar", "Sunday", "Vacation", "Start_Time"], Information=Sunday_Vac_Frame_Var1.get()))
    Entry_field_Insert(Field=Sunday_Vac_Frame_Var1, Value=Sunday_Vacation_Start)
    Sunday_Vac_Frame_Var2 = Sunday_Vac_Frame.children["!ctkframe5"].children["!ctkentry"]
    Sunday_Vac_Frame_Var2.configure(placeholder_text="Day end time.")
    Sunday_Vac_Frame_Var2.bind("<FocusOut>", lambda Entry_value: Check_Time_Continuation(Settings=Settings, Configuration=Configuration, Format_Time=Format_Time, Start_Time=Sunday_Vac_Frame_Var1, End_Time=Sunday_Vac_Frame_Var2, Week_Day="Sunday", Type="Vacation"))
    Entry_field_Insert(Field=Sunday_Vac_Frame_Var2, Value=Sunday_Vacation_End)

    # Field - Total Time
    Vacation_Calendar_Total = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Total Time", Field_Type="Input_Normal")
    Vacation_Calendar_Total_Var = Vacation_Calendar_Total.children["!ctkframe3"].children["!ctkentry"]
    Vacation_Calendar_Total_Var.configure(placeholder_text=Total_Vacation_Duration, placeholder_text_color="#949A9F")
    Vacation_Calendar_Total_Var.configure(state="disabled")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Button_Skip_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Skip_Add_Var.configure(text="Calculate", command = lambda: Calculate_duration(Settings=Settings, Configuration=Configuration, Entry_Field=Vacation_Calendar_Total_Var, Lunch_Brake_Duration_Frame_Var=0, Calendar_Type="Vacation", Monday_Start=Monday_Vac_Frame_Var1, Monday_End=Monday_Vac_Frame_Var2, Tuesday_Start=Tuesday_Vac_Frame_Var1, Tuesday_End=Tuesday_Vac_Frame_Var2, Wednesday_Start=Wednesday_Vac_Frame_Var1, Wednesday_End=Wednesday_Vac_Frame_Var2, Thursday_Start=Thursday_Vac_Frame_Var1, Thursday_End=Thursday_Vac_Frame_Var2, Friday_Start=Friday_Vac_Frame_Var1, Friday_End=Friday_Vac_Frame_Var2, Saturday_Start=Saturday_Vac_Frame_Var1, Saturday_End=Saturday_Vac_Frame_Var2, Sunday_Start=Sunday_Vac_Frame_Var1, Sunday_End=Sunday_Vac_Frame_Var2))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Skip_Add_Var, message="Calculate total week Vacation duration.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Calendar_Start_End_Time(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Start_Event_json = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
    End_Event_json = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]

    # ------------------------- Local Functions ------------------------#
    def Check_Same_Values(Start_Event_Var: CTkEntry, End_Event_Var: CTkEntry) -> bool:
        if Start_Event_Var.get() == End_Event_Var.get():
            CTkMessagebox(title="Error", message=f"You entered same value as Work - Start, which would not work, please change it. This value is not to be saved.", icon="cancel", fade_in_duration=1)
        else:
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Start_End_Events", "End"], Information=End_Event_Var.get())

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Workday - Start / End Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Events Subject which defines Start and End time of each day in Calendar.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Work - Start
    Start_Event = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - Start", Field_Type="Input_Normal") 
    Start_Event_Var = Start_Event.children["!ctkframe3"].children["!ctkentry"]
    Start_Event_Var.configure(placeholder_text="Event Subject which starts day")
    Start_Event_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Start_End_Events", "Start"], Information=Start_Event_Var.get()))
    Entry_field_Insert(Field=Start_Event_Var, Value=Start_Event_json)

    # Field - Work - End
    End_Event = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Work - End", Field_Type="Input_Normal") 
    End_Event_Var = End_Event.children["!ctkframe3"].children["!ctkentry"]
    End_Event_Var.configure(placeholder_text="Event Subject which ends day")
    End_Event_Var.bind("<FocusOut>", lambda Entry_value: Check_Same_Values(Start_Event_Var=Start_Event_Var, End_Event_Var=End_Event_Var))
    Entry_field_Insert(Field=End_Event_Var, Value=End_Event_json)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Events - General --------------------------------------------------------------------------#
def Settings_Events_General_Lunch(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Lunch_Enabled = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Use"]
    Lunch_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Search_Text"]
    Lunch_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["All_Day"]
    Lunch_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Part_Day"]
    Lunch_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Lunch_Option_List"]

    Lunch_Use_Variable = BooleanVar(master=Frame, value=Lunch_Enabled)
    Lunch_All_Variable = StringVar(master=Frame, value=Lunch_All_Day)
    Lunch_Part_Variable = StringVar(master=Frame, value=Lunch_Part_Day)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Special - Lunch", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Lunch brake -> always skip it. \n Lunch break will always break Parallel Events.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Lunch = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Lunch_Var = Use_Lunch.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Lunch_Var.configure(variable=Lunch_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Lunch_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Lunch", "Use"], Information=Lunch_Use_Variable))

    # Field - Search Text
    Search_Text_Lunch = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Lunch_Var = Search_Text_Lunch.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Lunch_Var.configure(placeholder_text="Event Subject which defines lunch")
    Search_Text_Lunch_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Lunch", "Search_Text"], Information=Search_Text_Lunch_Var.get()))
    Entry_field_Insert(Field=Search_Text_Lunch_Var, Value=Lunch_Search_Text)

    # Field - All Day
    All_Day_Lunch = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Lunch_Var = All_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Lunch_Var.configure(variable=Lunch_All_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=All_Day_Lunch_Var, values=Lunch_Day_Option_List, command=lambda All_Day_Lunch_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Lunch_All_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Lunch", "All_Day"], Information=All_Day_Lunch_Var))

    # Field - Part Day
    Part_Day_Lunch = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Lunch_Var = Part_Day_Lunch.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Lunch_Var.configure(variable=Lunch_Part_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Part_Day_Lunch_Var, values=Lunch_Day_Option_List, command=lambda Part_Day_Lunch_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Lunch_Part_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Lunch", "Part_Day"], Information=Part_Day_Lunch_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_Vacation(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Vacation_Enabled = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Use"]
    Vacation_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Search_Text"]
    Vacation_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["All_Day"]
    Vacation_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Part_Day"]
    Vacation_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Vacation_Option_List"]
    Vacation_Delete_Events = Settings["Event_Handler"]["Events"]["Special_Events"]["Vacation"]["Delete_Events_w_KM_Calendar"]

    Vacation_Use_Variable = BooleanVar(master=Frame, value=Vacation_Enabled)
    Vacation_All_Variable = StringVar(master=Frame, value=Vacation_All_Day)
    Vacation_Part_Variable = StringVar(master=Frame, value=Vacation_Part_Day)
    Vacation_Delete_Events_Variable = BooleanVar(master=Frame, value=Vacation_Delete_Events)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#    
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Special - Vacation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Vacation")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Vacation = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Vacation_Var = Use_Vacation.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Vacation_Var.configure(variable=Vacation_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Vacation_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Vacation", "Use"], Information=Vacation_Use_Variable))

    # Field - Search Text
    Search_Text_Vacation = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Vacation_Var = Search_Text_Vacation.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Vacation_Var.configure(placeholder_text="Event Subject which defines vacation")
    Search_Text_Vacation_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Vacation", "Search_Text"], Information=Search_Text_Vacation_Var.get()))
    Entry_field_Insert(Field=Search_Text_Vacation_Var, Value=Vacation_Search_Text)

    # Field - All Day
    All_Day_Vacation = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_Vacation_Var = All_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_Vacation_Var.configure(variable=Vacation_All_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=All_Day_Vacation_Var, values=Vacation_Day_Option_List, command=lambda All_Day_Vacation_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Vacation_All_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Vacation", "All_Day"], Information=All_Day_Vacation_Var))

    # Field - Part Day
    Part_Day_Vacation = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_Vacation_Var = Part_Day_Vacation.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_Vacation_Var.configure(variable=Vacation_Part_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Part_Day_Vacation_Var, values=Vacation_Day_Option_List, command=lambda Part_Day_Vacation_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Vacation_Part_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Vacation", "Part_Day"], Information=Part_Day_Vacation_Var))

    # Field - Use
    Delete_Events_Vacation = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delete Events w Working H.", Field_Type="Input_CheckBox") 
    Delete_Events_Vacation_Var = Delete_Events_Vacation.children["!ctkframe3"].children["!ctkcheckbox"]
    Delete_Events_Vacation_Var.configure(variable=Vacation_Delete_Events_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Vacation_Delete_Events_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Vacation", "Delete_Events_w_Working_Hours"], Information=Vacation_Delete_Events_Variable))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_SickDay(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    SickDay_Enabled = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Use"]
    SickDay_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Search_Text"]
    SickDay_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["All_Day"]
    SickDay_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Part_Day"]
    SickDay_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["SickDay_Option_List"]
    SickDay_Delete_Events = Settings["Event_Handler"]["Events"]["Special_Events"]["SickDay"]["Delete_Events_w_KM_Calendar"]

    SickDay_Use_Variable = BooleanVar(master=Frame, value=SickDay_Enabled)
    SickDay_All_Variable = StringVar(master=Frame, value=SickDay_All_Day)
    SickDay_Part_Variable = StringVar(master=Frame, value=SickDay_Part_Day)
    SickDay_Delete_Events_Variable = BooleanVar(master=Frame, value=SickDay_Delete_Events)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Special - SickDay", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of SickDay")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_SickDay = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_SickDay_Var = Use_SickDay.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_SickDay_Var.configure(variable=SickDay_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=SickDay_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "SickDay", "Use"], Information=SickDay_Use_Variable))

    # Field - Search Text
    Search_Text_SickDay = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_SickDay_Var = Search_Text_SickDay.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_SickDay_Var.configure(placeholder_text="Event Subject which defines SickDay")
    Search_Text_SickDay_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "SickDay", "Search_Text"], Information=Search_Text_SickDay_Var.get()))
    Entry_field_Insert(Field=Search_Text_SickDay_Var, Value=SickDay_Search_Text)

    # Field - All Day
    All_Day_SickDay = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_SickDay_Var = All_Day_SickDay.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_SickDay_Var.configure(variable=SickDay_All_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=All_Day_SickDay_Var, values=SickDay_Day_Option_List, command=lambda All_Day_SickDay_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=SickDay_All_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "SickDay", "All_Day"], Information=All_Day_SickDay_Var))

    # Field - Part Day
    Part_Day_SickDay = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_SickDay_Var = Part_Day_SickDay.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_SickDay_Var.configure(variable=SickDay_Part_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Part_Day_SickDay_Var, values=SickDay_Day_Option_List, command=lambda Part_Day_SickDay_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=SickDay_Part_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "SickDay", "Part_Day"], Information=Part_Day_SickDay_Var))

    # Field - Use
    Delete_Events_SickDay = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delete Events w Working H.", Field_Type="Input_CheckBox") 
    Delete_Events_SickDay_Var = Delete_Events_SickDay.children["!ctkframe3"].children["!ctkcheckbox"]
    Delete_Events_SickDay_Var.configure(variable=SickDay_Delete_Events_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=SickDay_Delete_Events_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "SickDay", "Delete_Events_w_Working_Hours"], Information=SickDay_Delete_Events_Variable))


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_HomeOffice(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    HomeOffice_Enabled = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Use"]
    HomeOffice_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Search_Text"]
    HomeOffice_All_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["All_Day"]
    HomeOffice_Part_Day = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Part_Day"]
    HomeOffice_Day_Option_List = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["HomeOffice_Option_List"]

    HomeOffice_Use_Variable = BooleanVar(master=Frame, value=HomeOffice_Enabled)
    HomeOffice_All_Variable = StringVar(master=Frame, value=HomeOffice_All_Day)
    HomeOffice_Part_Variable = StringVar(master=Frame, value=HomeOffice_Part_Day)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Special - HomeOffice", Additional_Text="In the development", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of HomeOffice")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_HomeOffice = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_HomeOffice_Var = Use_HomeOffice.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_HomeOffice_Var.configure(variable=HomeOffice_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=HomeOffice_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "HomeOffice", "Use"], Information=HomeOffice_Use_Variable))


    # Field - Search Text
    Search_Text_HomeOffice = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_HomeOffice_Var = Search_Text_HomeOffice.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_HomeOffice_Var.configure(placeholder_text="Event Subject which defines home office")
    Search_Text_HomeOffice_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "HomeOffice", "Search_Text"], Information=Search_Text_HomeOffice_Var.get()))
    Entry_field_Insert(Field=Search_Text_HomeOffice_Var, Value=HomeOffice_Search_Text)

    # Field - All Day
    All_Day_HomeOffice = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    All_Day_HomeOffice_Var = All_Day_HomeOffice.children["!ctkframe3"].children["!ctkoptionmenu"]
    All_Day_HomeOffice_Var.configure(variable=HomeOffice_All_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=All_Day_HomeOffice_Var, values=HomeOffice_Day_Option_List, command=lambda All_Day_HomeOffice_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=HomeOffice_All_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "HomeOffice", "All_Day"], Information=All_Day_HomeOffice_Var))

    # Field - Part Day
    Part_Day = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Part Day", Field_Type="Input_OptionMenu") 
    Part_Day_HomeOffice_Var = Part_Day.children["!ctkframe3"].children["!ctkoptionmenu"]
    Part_Day_HomeOffice_Var.configure(variable=HomeOffice_Part_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Part_Day_HomeOffice_Var, values=HomeOffice_Day_Option_List, command=lambda Part_Day_HomeOffice_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=HomeOffice_Part_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "HomeOffice", "Part_Day"], Information=Part_Day_HomeOffice_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_Private(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Private_Enabled = Settings["Event_Handler"]["Events"]["Special_Events"]["Private"]["Use"]
    Private_Search_Text = Settings["Event_Handler"]["Events"]["Special_Events"]["Private"]["Search_Text"]
    Private_Method = Settings["Event_Handler"]["Events"]["Special_Events"]["Private"]["Method"]
    Private_Method_List = Settings["Event_Handler"]["Events"]["Special_Events"]["Private"]["Private_Option_List"]

    Private_Use_Variable = BooleanVar(master=Frame, value=Private_Enabled)
    Private_Method_Variable = StringVar(master=Frame, value=Private_Method)

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Special - Private", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings what program will do in case of Special Event Private, \n Split --> Special Event will split parallel events, like Lunch \n Do nothing --> This event will not do anything to parallel events")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Private = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Private_Var = Use_Private.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Private_Var.configure(variable=Private_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Private_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Private", "Use"], Information=Private_Use_Variable))

    # Field - Search Text
    Search_Text_Private = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Search text", Field_Type="Input_Normal") 
    Search_Text_Private_Var = Search_Text_Private.children["!ctkframe3"].children["!ctkentry"]
    Search_Text_Private_Var.configure(placeholder_text="Event Subject which defines private special event.")
    Search_Text_Private_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Private", "Search_Text"], Information=Search_Text_Private_Var.get()))
    Entry_field_Insert(Field=Search_Text_Private_Var, Value=Private_Search_Text)

    # Field - Method used
    Method_Private = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    Method_Private_Var = Method_Private.children["!ctkframe3"].children["!ctkoptionmenu"]
    Method_Private_Var.configure(variable=Private_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Method_Private_Var, values=Private_Method_List, command=lambda Method_Private_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Private_Method_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Special_Events", "Private", "Method"], Information=Method_Private_Var))


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Events_General_Skip(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Skip_Enabled = Settings["Event_Handler"]["Events"]["Skip"]["Use"]
    Events_Skip_list = Settings["Event_Handler"]["Events"]["Skip"]["Skip_List"]
    Skip_Use_Variable = BooleanVar(master=Frame, value=Skip_Enabled)

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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip", "Skip_List"], Information=Skip_Events)
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
                CTkMessagebox(title="Error", message=f"Subject not found, please check spelling.", icon="cancel", fade_in_duration=1)
            else:
                pass
            Skip_Events = [element for innerList in Frame_Skip_Table_Var.values for element in innerList]
            Skip_Events.remove("Skip Events")
            Skip_Events.sort()
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip", "Skip_List"], Information=Skip_Events)
        else:
            CTkMessagebox(title="Error", message=f"Header cannot be deleted.", icon="cancel", fade_in_duration=1)

    def Del_Skip_Event_all(Frame_Skip_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Skip_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Skip_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip", "Skip_List"], Information=[])

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Skip Events", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of text be skipped as TimeSheet Entry in the case that part of text is found in Event Subject.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Skip_Event = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Skip_Event_Var = Use_Skip_Event.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Skip_Event_Var.configure(variable=Skip_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Skip_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Skip", "Use"], Information=Skip_Use_Variable))

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Subject", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Skip Events Table
    Header_List = ["Skip Events"]
    Show_Events_Skip_list = [Header_List]
    for skip_Subject in Events_Skip_list:
        Show_Events_Skip_list.append([skip_Subject])
        
    Frame_Skip_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Body, Table_Size="Single_size", Table_Values=Show_Events_Skip_list, Table_Columns=len(Header_List), Table_Rows=len(Events_Skip_list) + 1)
    Frame_Skip_Table_Var = Frame_Skip_Table.children["!ctktable"]
    Frame_Skip_Table_Var.configure(wraplength=440)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Skip_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Skip_Add_Var.configure(text="Add", command = lambda:Add_Skip_Event(Header_List=Header_List, Subject_Text_Text_Var=Subject_Text_Text_Var, Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Skip_Add_Var, message="Add selected subject to skip list", ToolTip_Size="Normal")

    Button_Skip_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Skip_Del_One_Var.configure(text="Del", command = lambda:Del_Skip_Event_one(Subject_Text_Text_Var=Subject_Text_Text_Var, Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Skip_Del_One_Var, message="Delete row from table based on input text.", ToolTip_Size="Normal")

    Button_Skip_Del_all_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Skip_Del_all_Var.configure(text="Del all", command = lambda:Del_Skip_Event_all(Frame_Skip_Table_Var=Frame_Skip_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Skip_Del_all_Var, message="Delete all rows from table.", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



# -------------------------------------------------------------------------- Tab Events - Empty --------------------------------------------------------------------------#
def Settings_Events_Empty_Generally(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Activity", "Description", "Coverage Percentage"]
    Events_Empty_General_dict = Settings["Event_Handler"]["Events"]["Empty"]["General"]

    Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    Project_Variable = StringVar(master=Frame, value=Project_List[0])

    Activity_All_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
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
                CTkMessagebox(title="Error", message=f"Coverage must be between 0 - 100, please check it.", icon="cancel", fade_in_duration=1) 
        except:
            Add_flag = False
            CTkMessagebox(title="Error", message=f"Coverage is not whole number, check it.", icon="cancel", fade_in_duration=1)

        # Not To add same line
        if Add_flag == True:
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
            Empty_General_Events = Update_empty_information(Check_List=Empty_General_Events)

            General_dict = {}
            Counter = 0
            for Empty_General_Events_row in Empty_General_Events:
                Empty_General_Events_row_dict = dict(zip(Header_List, Empty_General_Events_row))
                General_dict[Counter] = Empty_General_Events_row_dict
                Counter += 1
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)
        else:
            pass
    
    def Del_Empty_Event_One(Header_List: list, Frame_Empty_General_Table_Var: CTkTable) -> None:
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)
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
        Delete_One_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete one line", width=510, height=260)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_One_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
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

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Coverage_Label_Var=Coverage_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_One_Confirm(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_One_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_Empty_Event_All(Frame_Empty_General_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_General_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_General_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information={})

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
                    CTkMessagebox(title="Error", message=f"Sum of all lines not equal 100, please check.", icon="cancel", fade_in_duration=1)
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
                Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "General"], Information=General_dict)

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

        Recalculate_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Recalculate", width=510, height=Recalculate_window_height)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Recalculate_window, Name="Recalculate coverage", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Helps to recalculate Coverage percentage so sum is equal 100")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        for line in range(0, Lines_No):
            # Field - Monday
            Fields_Frame = Elements_Groups.Get_Double_Field_Input(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column" , Label=f"Line {line}", Validation="Integer") 
            Var1 = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
            Var1.configure(placeholder_text=Empty_General_Events[line][3])
            Var1.configure(state="disabled")

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Recalculation_Confirm(Frame_Body=Frame_Body, Lines_No=Lines_No))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm coverage change.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Recalculation_Reject())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Empty Space coverage Events", Additional_Text="Sum of Coverage Percentage must equal 100%.", Widget_size="Triple_size", Widget_Label_Tooltip="For empty space (between Events in calendar) program use fill them by this setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Frame_Input_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Input_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")

    # Empty Events table
    Skip_Event_General_list = [Header_List]
    Events_Empty_General_dict_rows = Events_Empty_General_dict.items()
    for Sub_Row in Events_Empty_General_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_General_list.append(list(Sub_dict.values()))

    Frame_Empty_General_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_General_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_Event_General_list))
    Frame_Empty_General_Table_Var = Frame_Empty_General_Table.children["!ctktable"]
    Frame_Empty_General_Table_Var.configure(wraplength=230)

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var1 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var1.configure(variable=Project_Variable)

    # Field - Activity
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var1 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var1.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var1, values=Project_List, command = lambda Project_Option_Var1: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var1, Activity_Option_Var=Activity_Option_Var1, Project_Variable=Project_Variable))
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var1, values=[], command=None)

    # Field - Coverage
    Coverage_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Coverage", Field_Type="Input_Normal", Validation="Integer") 
    Coverage_Text_Var = Coverage_Text.children["!ctkframe3"].children["!ctkentry"]
    Coverage_Text_Var.configure(placeholder_text="Add %")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Buttons_count=4, Button_Size="Small") 
    Button_Empty_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Empty_Add_Var.configure(text="Add", command = lambda:Add_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var1=Project_Option_Var1, Activity_Option_Var1=Activity_Option_Var1, Coverage_Text_Var=Coverage_Text_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Add_Var, message="Add selected subject to skip list", ToolTip_Size="Normal")

    Button_Empty_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Empty_Del_One_Var.configure(text="Del", command = lambda:Del_Empty_Event_One(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_Empty_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Empty_Del_All_Var.configure(text="Del all", command = lambda:Del_Empty_Event_All(Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    Button_Empty_Recalculate_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton4"]
    Button_Empty_Recalculate_Var.configure(text="Recalculate", command = lambda:Recalculate_Empty_Event(Header_List=Header_List, Frame_Empty_General_Table_Var=Frame_Empty_General_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Empty_Recalculate_Var, message="Recalculate coverage for all lines.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Input_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    return Frame_Main



def Settings_Events_Empty_Schedule(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Activity", "Description", "Day of Week", "Start", "End"]
    Events_Empty_Schedules_dict = Settings["Event_Handler"]["Events"]["Empty"]["Scheduled"]

    Format_Time = Settings["General"]["Formats"]["Time"]

    Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    Project_Variable = StringVar(master=Frame, value=Project_List[0])

    Activity_All_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
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
            CTkMessagebox(title="Error", message=f"You didnt select any day of week, please update.", icon="cancel", fade_in_duration=1)

        # Time Checkers
        if Add_flag == True:
            try:
                Add_Start_Time_dt = datetime.strptime(Add_Start_Time, Format_Time)
                Add_End_Time_dt = datetime.strptime(Add_End_Time, Format_Time)

                if Add_End_Time_dt > Add_Start_Time_dt:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"End Time is before/equal to Start Time, please correct", icon="cancel", fade_in_duration=1)
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
            Schedule_Events = Update_empty_information(Check_List=Schedule_Events)

            Scheduled_dict = {}
            Counter = 0
            for Schedule_Events_row in Schedule_Events:
                Schedule_Events_row_dict = dict(zip(Header_List, Schedule_Events_row))
                Scheduled_dict[Counter] = Schedule_Events_row_dict
                Counter += 1
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information=Scheduled_dict)
        else:
            pass

    def Del_Schedule_Event_One(Header_List: list, Frame_Empty_Schedules_Table_Var: CTkTable) -> None:
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information=Scheduled_dict)
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
        Delete_Scheduled_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete one scheduled line", width=510, height=400)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Scheduled_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
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

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, WeekDays_Label_Var=WeekDays_Label_Var, Start_Label_Var=Start_Label_Var, End_Label_Var=End_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Schedule_Confirm(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Schedule_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Empty_Schedules_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Empty_Schedules_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Scheduled"], Information={})

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Events Scheduler", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple TimeSheet Entry planner.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Frame_Input_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")
    Frame_Input_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")

    # Scheduled Events table
    Skip_Event_Schedule_list = [Header_List]
    Skip_Event_Schedule_dict_rows = Events_Empty_Schedules_dict.items()
    for Sub_Row in Skip_Event_Schedule_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_Event_Schedule_list.append(list(Sub_dict.values()))

    Frame_Empty_Schedules_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_Event_Schedule_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_Event_Schedule_list))
    Frame_Empty_Schedules_Table_Var = Frame_Empty_Schedules_Table.children["!ctktable"]
    Frame_Empty_Schedules_Table_Var.configure(wraplength=150)

    # Field - Week Days
    Week_Days_Label = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Input_Area, Label_Size="Column_Header", Font_Size="Column_Header")
    Week_Days_Label.configure(text="Week Days")
    Week_Days_Label.pack_propagate(flag=False)

    Week_Days_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column")
    Week_Days_Frame.configure(width=300)

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
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var2 = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var2.configure(variable=Project_Variable)
    
    # Field - Activity --> placed before project because of variable to be used
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var2 = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var2.configure(variable=Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var2, values=Project_List, command = lambda Project_Option_Var2: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var2, Activity_Option_Var=Activity_Option_Var2, Project_Variable=Project_Variable))
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var2, values=Activity_All_List, command=None)

    # Field - Start Time
    Start_Time_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Start Time", Field_Type="Input_Normal", Validation="Time") 
    Start_Time_Text_Var = Start_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    Start_Time_Text_Var.configure(placeholder_text="HH:MM")

    # Field - End Time
    End_Time_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="End Time", Field_Type="Input_Normal", Validation="Time") 
    End_Time_Text_Var = End_Time_Text.children["!ctkframe3"].children["!ctkentry"]
    End_Time_Text_Var.configure(placeholder_text="HH:MM")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Schedule_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Schedule_Add_Var.configure(text="Add", command = lambda:Add_Schedule_Event(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var2=Project_Option_Var2, Activity_Option_Var2=Activity_Option_Var2, Start_Time_Text_Var=Start_Time_Text_Var, End_Time_Text_Var=End_Time_Text_Var, Monday_Check_Frame_Var=Monday_Check_Frame_Var, Tuesday_Check_Frame_Var=Tuesday_Check_Frame_Var, Wednesday_Check_Frame_Var=Wednesday_Check_Frame_Var, Thursday_Check_Frame_Var=Thursday_Check_Frame_Var, Friday_Check_Frame_Var=Friday_Check_Frame_Var, Saturday_Check_Frame_Var=Saturday_Check_Frame_Var, Sunday_Check_Frame_Var=Sunday_Check_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_Schedule_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Schedule_Del_One_Var.configure(text="Del", command = lambda:Del_Schedule_Event_One(Header_List=Header_List, Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_Schedule_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Schedule_Del_All_Var.configure(text="Del all", command = lambda:Del_Schedule_Event_All(Frame_Empty_Schedules_Table_Var=Frame_Empty_Schedules_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Schedule_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Input_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
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



def Settings_Events_Split(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Events_Empty_Split_Enabled = Settings["Event_Handler"]["Events"]["Empty"]["Split"]["Use"]
    Events_Empty_Split_Duration = Settings["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Duration"]
    Events_Empty_Split_Minimal_Time = Settings["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Minimal_Time"]
    Events_Empty_Split_Method = Settings["Event_Handler"]["Events"]["Empty"]["Split"]["Split_Method"]
    Events_Empty_Split_list = Settings["Event_Handler"]["Events"]["Empty"]["Split"]["Methods_List"]

    Empty_Split_Use_Variable = BooleanVar(master=Frame, value=Events_Empty_Split_Enabled)
    Events_Empty_Split_list_Variable = StringVar(master=Frame, value=Events_Empty_Split_Method, name="Events_Empty_Split_list_Variable")

    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Events Splitting", Additional_Text="Pay attention to Join Setup.", Widget_size="Single_size", Widget_Label_Tooltip="Use for splitting automatically filled events by program longer than defined duration. \nEffect of the split can be suppress partially / fully by Joining Events, depends on setup.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Empty_Split = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Empty_Split_Var = Use_Empty_Split.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Empty_Split_Var.configure(variable=Empty_Split_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Empty_Split_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Split", "Use"], Information=Empty_Split_Use_Variable))

    # Field - Duration
    Split_Duration_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Duration", Field_Type="Input_Normal", Validation="Integer") 
    Split_Duration_Text_Var = Split_Duration_Text.children["!ctkframe3"].children["!ctkentry"]
    Split_Duration_Text_Var.configure(placeholder_text="Empty space duration which will be splitted.")
    Split_Duration_Text_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Split", "Split_Duration"], Information=int(Split_Duration_Text_Var.get())))
    Entry_field_Insert(Field=Split_Duration_Text_Var, Value=Events_Empty_Split_Duration)

    # Field - Minimal Time
    Split_Min_Duration_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Minimal Time", Field_Type="Input_Normal") 
    Split_Min_Duration_Text_Var = Split_Min_Duration_Text.children["!ctkframe3"].children["!ctkentry"]
    Split_Min_Duration_Text_Var.configure(placeholder_text=Events_Empty_Split_Minimal_Time, placeholder_text_color="#949A9F")
    Split_Min_Duration_Text_Var.configure(state="disabled")

    # Field - All Day
    Split_Method = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="All Day", Field_Type="Input_OptionMenu") 
    Split_Method_Var = Split_Method.children["!ctkframe3"].children["!ctkoptionmenu"]
    Split_Method_Var.configure(variable=Events_Empty_Split_list_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Split_Method_Var, values=Events_Empty_Split_list, command=lambda Split_Method_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Events_Empty_Split_list_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Empty", "Split", "Split_Method"], Information=Split_Method_Var))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

# -------------------------------------------------------------------------- Tab Events - Rules --------------------------------------------------------------------------#
def Settings_Events_AutoFill(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Search Text", "Project", "Activity", "Location"]
    AutoFill_Rules_Enabled = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Use"]
    Events_AutoFill_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Dictionary"]

    Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    Project_All_List = Project_List
    Project_All_List.insert(0, " ") # Because there might be not filled one in Calendar

    Activity_All_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
    Activity_All_List.insert(0, " ") # Because there might be not filled one in Calendar
    Activity_All_List.sort()

    Location_List = Settings["Event_Handler"]["Location"]["Location_List"]
    Location_List.insert(0, " ") # Because there might be not filled one in Calendar

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
                    CTkMessagebox(title="Error", message=f"Rule with Search text already exists with Auto-filler.", icon="cancel", fade_in_duration=1)

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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information=AutoFill_dict)
        else:
            pass
        
    def Del_AutoFill_Event_One() -> None:
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information=AutoFill_dict)
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
        Delete_AutoFill_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete one line", width=510, height=260)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_AutoFill_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
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

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Activity_Label_Var=Activity_Label_Var, Description_Label_Var=Description_Label_Var, Location_Label_Var=Location_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_AutoFill_Confirm(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_AutoFill_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")

    def Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_AutoFiller_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_AutoFiller_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text", "Dictionary"], Information={})

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="AutoFill rules", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Simple rules applied on TimeSheet Entry if part/whole Search Text is found in Subject. If empty then do not fill it or overwrite it.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Input_Total = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Input_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")
    Frame_Input_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")

    # AutoFilling Table
    Skip_AutoFill_list = [Header_List]
    Events_AutoFill_dict_rows = Events_AutoFill_dict.items()
    for Sub_Row in Events_AutoFill_dict_rows:
        Sub_dict = Sub_Row[1]
        Skip_AutoFill_list.append(list(Sub_dict.values()))

    # BUG --> tabulka se načte pouze první sloupec a až po skrolování se dočte zbytek sloupců
    Frame_AutoFiller_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Skip_AutoFill_list, Table_Columns=len(Header_List), Table_Rows=len(Skip_AutoFill_list))
    Frame_AutoFiller_Table_Var = Frame_AutoFiller_Table.children["!ctktable"]
    Frame_AutoFiller_Table_Var.configure(wraplength=230)

    # Field - Use
    Use_AutoFill = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_AutoFill_Var = Use_AutoFill.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_AutoFill_Var.configure(variable=AutoFill_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=AutoFill_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Search_Text", "Use"], Information=AutoFill_Use_Variable))

    # Field - Subject
    Subject_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Search Text", Field_Type="Input_Normal") 
    Subject_Text_Text_Var = Subject_Text.children["!ctkframe3"].children["!ctkentry"]
    Subject_Text_Text_Var.configure(placeholder_text="Add new text")

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(variable=Project_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command=None)

    # Field - Activity --> really from list of all Activity, because rule can be without Project 
    Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Activity", Field_Type="Input_OptionMenu") 
    Activity_Option_Var = Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Activity_Option_Var.configure(variable=Activity_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Activity_Option_Var, values=Activity_All_List, command=None)

    # Field - Location
    Location_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Location", Field_Type="Input_OptionMenu") 
    Location_Option_Var = Location_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Location_Option_Var.configure(variable=Location_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Location_Option_Var, values=Location_List, command=None)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_AutoFill_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_AutoFill_Add_Var.configure(text="Add", command = lambda:Add_AutoFill_Event(Header_List=Header_List, Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var, Subject_Text_Text_Var=Subject_Text_Text_Var, Project_Option_Var=Project_Option_Var, Activity_Option_Var=Activity_Option_Var, Location_Option_Var=Location_Option_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_AutoFill_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_AutoFill_Del_One_Var.configure(text="Del", command = lambda:Del_AutoFill_Event_One())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_AutoFill_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_AutoFill_Del_All_Var.configure(text="Del all", command = lambda:Del_AutoFill_Event_All(Frame_AutoFiller_Table_Var=Frame_AutoFiller_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Input_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Input_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="y", expand=True, padx=0, pady=0)

    return Frame_Main


def Settings_Events_Activity_Correction(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Header_List = ["Project", "Wrong Activity", "Correct Activity"]
    Events_Activity_Correction_Enabled = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Use"]
    Events_Activity_Correction_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Dictionary"]
    Activity_Correction_Use_Variable = BooleanVar(master=Frame, value=Events_Activity_Correction_Enabled)

    Project_dict = Settings["Event_Handler"]["Project"]["Project_List"]
    Project_List = Defaults_Lists.List_from_Dict(Dictionary=Project_dict, Key_Argument="Project")
    Project_Variable = StringVar(master=Frame, value=Project_List[0])

    Activity_All_List = list(Settings["Event_Handler"]["Activity"]["Activity_List"])
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
            CTkMessagebox(title="Error", message=f"Project is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_Wrong_Activity == " ":
            Add_flag = False
            CTkMessagebox(title="Error", message=f"Wrong Activity is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_Correct_Activity == " ":
            Add_flag = False
            CTkMessagebox(title="Error", message=f"Correct Activity is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass
        
        # Not To add same line -->  consider only Search text
        if Add_flag == True:
            for AutoFill_Event in Check_List:
                if AutoFill_Event != Add_row:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"Rule with all combination already exists with Events Corrections.", icon="cancel", fade_in_duration=1)

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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information=Activity_Correction_dict)
        else:
            pass

    def Del_Activity_Correct_Event_One():
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information=Activity_Correction_dict)
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
        Delete_Activity_Correct_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete one Activity", width=510, height=250)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Activity_Correct_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
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

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, Line_Selected=Line_Selected, Project_Label_Var=Project_Label_Var, Wrong_Activity_Label_Var=Wrong_Activity_Label_Var, Correct_Activity_Label_Var=Correct_Activity_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Activity_Correct_Confirm(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, LineNo_Option_Var=LineNo_Option_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Activity_Correct_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")



    def Del_Activity_Correct_Event_all(Frame_Activity_Correct_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Activity_Correct_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Activity_Correct_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Dictionary"], Information={})

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Activity correction", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Change Activity in the processing of Events, when non-proper activity for Project is selected in calendar.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Input_Total = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Input_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")
    Frame_Input_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")

    # AutoFilling Table
    Activity_Correction_list = [Header_List]
    Events_Activity_Correction_dict_rows = Events_Activity_Correction_dict.items()
    for Sub_Row in Events_Activity_Correction_dict_rows:
        Sub_dict = Sub_Row[1]
        Activity_Correction_list.append(list(Sub_dict.values()))

    Frame_Activity_Correct_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Activity_Correction_list, Table_Columns=len(Header_List), Table_Rows=len(Activity_Correction_list))
    Frame_Activity_Correct_Table_Var = Frame_Activity_Correct_Table.children["!ctktable"]
    Frame_Activity_Correct_Table_Var.configure(wraplength=310)

    # Field - Use
    Use_Activity_Correction = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Activity_Correction_Var = Use_Activity_Correction.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Activity_Correction_Var.configure(variable=Activity_Correction_Use_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Activity_Correction_Use_Variable, File_Name="Settings", JSON_path=["Event_Handler", "Events", "Auto_Filler", "Activity_Correction", "Use"], Information=Activity_Correction_Use_Variable))

    # Field - Project
    Project_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Project", Field_Type="Input_OptionMenu") 
    Project_Option_Var = Project_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Project_Option_Var.configure(variable=Project_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command=None)

    # Field - Activity --> really from list of all Activity, because rule have to be set per with all possible activity
    Wrong_Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Wrong Activity", Field_Type="Input_OptionMenu") 
    Wrong_Activity_Option_Var = Wrong_Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Wrong_Activity_Option_Var.configure(variable=Wrong_Activity_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Wrong_Activity_Option_Var, values=Activity_All_List, command=None)

    # Field - Activity --> placed before project because of variable to be used
    Correct_Activity_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Correct Activity", Field_Type="Input_OptionMenu") 
    Correct_Activity_Option_Var = Correct_Activity_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    Correct_Activity_Option_Var.configure(variable=Correct_Activity_Variable)

    # Project/Activity OptionMenu update
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Project_Option_Var, values=Project_List, command = lambda Project_Option_Var: Retrieve_Activity_based_on_Type(Settings=Settings, Configuration=Configuration, Project_Option_Var=Project_Option_Var, Activity_Option_Var=Correct_Activity_Option_Var, Project_Variable=Project_Variable))
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Correct_Activity_Option_Var, values=Activity_All_List, command=None)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_AutoFill_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_AutoFill_Add_Var.configure(text="Add", command = lambda:Add_Activity_Correct_Event(Header_List=Header_List, Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var, Project_Option_Var=Project_Option_Var, Wrong_Activity_Option_Var=Wrong_Activity_Option_Var, Correct_Activity_Option_Var=Correct_Activity_Option_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_AutoFill_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_AutoFill_Del_One_Var.configure(text="Del", command = lambda:Del_Activity_Correct_Event_One())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_AutoFill_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_AutoFill_Del_All_Var.configure(text="Del all", command = lambda:Del_Activity_Correct_Event_all(Frame_Activity_Correct_Table_Var=Frame_Activity_Correct_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_AutoFill_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Input_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Input_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="y", expand=True, padx=0, pady=0)

    return Frame_Main


def Settings_My_Team(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Managed_Team_dict = Settings["General"]["User"]["Managed_Team"]
    Header_List = ["User Team", "User ID", "User Name"]
    SP_Teams_List = list(Settings["General"]["Downloader"]["Sharepoint"]["Teams"]["Team_List"])
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
            CTkMessagebox(title="Error", message=f"Sharepoint list is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_User_ID == "":
            Add_flag = False
            CTkMessagebox(title="Error", message=f"User ID list is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass

        if Add_User_Name == "":
            Add_flag = False
            CTkMessagebox(title="Error", message=f"User Name list is empty please fill it first.", icon="cancel", fade_in_duration=1)
        else:
            pass
       
        # Not To add same line --> consider only User within same 
        if Add_flag == True:
            for User_row in Check_List:
                if User_row != Add_row:
                    pass
                else:
                    Add_flag = False
                    CTkMessagebox(title="Error", message=f"The member is already exists in registered members..", icon="cancel", fade_in_duration=1)

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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Managed_Team"], Information=Managed_Users_dict)
            Defaults_Lists.Create_Folder(file_path=f"Operational\\My_Team\\{Add_User_ID}")
        else:
            pass

    def Del_Team_User_One():
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Managed_Team"], Information=Managed_Users_dict)
            Defaults_Lists.Delete_Folder(file_path=f"Operational\\My_Team\\{Delete_Folder_Name}")
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
        Delete_Managed_User_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete one User", width=510, height=250)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Managed_User_Window, Name="Delete Line", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To delete one line from table.")
        Frame_Body = Frame_Main.children["!ctkframe2"]
    
        # Field - Option Menu
        LineNo_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Line No", Field_Type="Input_OptionMenu") 
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

        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=LineNo_Option_Var, values=Lines_list, command= lambda Line_Selected: Update_Labels_Texts(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, Line_Selected=Line_Selected, User_Team_Label_Var=User_Team_Label_Var, User_ID_Label_Var=User_ID_Label_Var, User_Name_Label_Var=User_Name_Label_Var)) 

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Managed_Member_Confirm(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, LineNo_Option_Var=LineNo_Option_Var, User_ID_Label_Var=User_ID_Label_Var))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal")

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Managed_Member_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal")


    def Del_Team_User_all(Frame_Managed_Team_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Managed_Team_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Managed_Team_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "User", "Managed_Team"], Information={})
        Defaults_Lists.Delete_Folders(file_path=f"Operational\\My_Team")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="My managed team", Additional_Text="", Widget_size="Triple_size", Widget_Label_Tooltip="Add / del user from my team, users are then visible on Managed Team dashboard.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Input Field + button in one line
    Frame_Input_Total = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column")

    Frame_Input_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")
    Frame_Input_Area.configure(width=300)

    Frame_Table_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame_Input_Total, Field_Frame_Type="Single_Column")

    # My team Table
    Managed_Team_list = [Header_List]
    Managed_Team_dict_rows = Managed_Team_dict.items()
    for Sub_Row in Managed_Team_dict_rows:
        Sub_dict = Sub_Row[1]
        Managed_Team_list.append(list(Sub_dict.values()))

    Frame_Managed_Team_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Table_Area, Table_Size="Double_size", Table_Values=Managed_Team_list, Table_Columns=len(Header_List), Table_Rows=len(Managed_Team_list))
    Frame_Managed_Team_Table_Var = Frame_Managed_Team_Table.children["!ctktable"]
    Frame_Managed_Team_Table_Var.configure(wraplength=310)

    # Field - Managed Team SP List
    MT_SP_Teams_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Managed Team", Field_Type="Input_OptionMenu") 
    MT_SP_Teams_Frame_Var = MT_SP_Teams_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    MT_SP_Teams_Frame_Var.configure(variable=User_SP_Team_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=MT_SP_Teams_Frame_Var, values=SP_Teams_List, command=None)

    # Field - Managed Team User ID
    MT_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Member ID", Field_Type="Input_Normal") 
    MT_User_ID_Frame_Var = MT_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    MT_User_ID_Frame_Var.configure(placeholder_text="Team member ID")

    # Field - Managed Team User ID
    MT_User_Name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Input_Area, Field_Frame_Type="Single_Column" , Label="Member Name", Field_Type="Input_Normal") 
    MT_User_Name_Frame_Var = MT_User_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    MT_User_Name_Frame_Var.configure(placeholder_text="Team member Name")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Input_Area, Configuration=Configuration, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_MT_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_MT_Add_Var.configure(text="Add", command = lambda:Add_Team_User(Header_List=Header_List, Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var, MT_SP_Teams_Frame_Var=MT_SP_Teams_Frame_Var, MT_User_ID_Frame_Var=MT_User_ID_Frame_Var, MT_User_Name_Frame_Var=MT_User_Name_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Add_Var, message="Add selected combination into the list", ToolTip_Size="Normal")

    Button_MT_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_MT_Del_One_Var.configure(text="Del", command = lambda:Del_Team_User_One())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Del_One_Var, message="Delete row from table based on input index.", ToolTip_Size="Normal")

    Button_MT_Del_All_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_MT_Del_All_Var.configure(text="Del all", command = lambda:Del_Team_User_all(Frame_Managed_Team_Table_Var=Frame_Managed_Team_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Del_All_Var, message="Delete all rows from table.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Frame_Input_Total.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Frame_Input_Area.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Table_Area.pack(side="left", fill="y", expand=True, padx=0, pady=0)

    return Frame_Main
