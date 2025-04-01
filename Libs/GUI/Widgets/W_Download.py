# Import Libraries
from datetime import datetime
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, StringVar, IntVar

# -------------------------------------------------------------------------------------------------------------------------------------------------- Download Page Widgets -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Download_Sharepoint(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Date_Range_Source: StringVar, GUI_Level_ID: int|None = None) -> CTkFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    SP_Date_From_Method = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method"]
    SP_Date_From_Method_list = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method_List"]
    SP_Date_To_Method = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method"]
    SP_Date_To_Method_list = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method_List"]

    def Sharepoint_Disabling_Man_Date_To(Selected_Value: str, Entry_Field: CTkEntry, Drop_Down_But: CTkButton, Variable: StringVar) -> None:
        Variable.set(value=Selected_Value)
        if (Selected_Value == "Today") or (Selected_Value == "Last Report Day"):
            Entry_Field.delete(first_index=0, last_index=1000)
            Entry_Field.configure(placeholder_text="")
            Entry_Field.configure(state="disabled")
            Drop_Down_But.configure(state="disabled")
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Entry_Field.configure(placeholder_text="YYYY-MM-DD")
            Drop_Down_But.configure(state="normal")
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Download To Method not allowed.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    SP_Date_From_Variable = StringVar(master=Frame, value=SP_Date_From_Method)
    SP_Date_To_Variable = StringVar(master=Frame, value=SP_Date_To_Method)

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Sharepoint - missing dates", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Time-sheets for download process.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Sharepoint_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Sharepoint") 
    Use_Sharepoint_Frame_Var = Use_Sharepoint_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Sharepoint_Frame_Var.configure(text="", variable=Download_Date_Range_Source)

    # Field - User ID
    SP_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    SP_User_ID_Text_Frame_Var = SP_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_User_ID_Text_Frame_Var.configure(placeholder_text=User_ID, placeholder_text_color="#949A9F")
    SP_User_ID_Text_Frame_Var.configure(state="disabled")

    # Field - User Email
    SP_Email_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    SP_Email_Text_Frame_Var = SP_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Email_Text_Frame_Var.configure(placeholder_text=User_Email, placeholder_text_color="#949A9F")
    SP_Email_Text_Frame_Var.configure(state="disabled")

    # Field - Date From Method
    SP_Date_From_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From", Field_Type="Input_OptionMenu") 
    SP_Date_From_Option_Var = SP_Date_From_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    SP_Date_From_Option_Var.configure(variable=SP_Date_From_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=SP_Date_From_Option_Var, values=SP_Date_From_Method_list, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Date To Method
    SP_Date_To_Option = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To", Field_Type="Input_OptionMenu") 
    SP_Date_To_Option_Var = SP_Date_To_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    SP_Date_To_Option_Var.configure(variable=SP_Date_To_Variable)

    # Field - Manual Date To
    SM_Man_Date_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Manual Date To", Field_Type="Date_Picker", Validation="Date") 
    SM_Man_Date_To_Frame_Var = SM_Man_Date_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_SM_Man_Date_To_Frame_Var = SM_Man_Date_To_Frame.children["!ctkframe3"].children["!ctkbutton"]
    SM_Man_Date_To_Frame_Var.configure(placeholder_text="YYYY-MM-DD")
    Button_SM_Man_Date_To_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=SM_Man_Date_To_Frame_Var, Clicked_on_Button=Button_SM_Man_Date_To_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_SM_Man_Date_To_Frame_Var, message="Entry_DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Disabling fields --> Manual Date To 
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=SP_Date_To_Option_Var, values=SP_Date_To_Method_list, command = lambda SP_Date_To_Option_Var: Sharepoint_Disabling_Man_Date_To(Selected_Value=SP_Date_To_Option_Var, Entry_Field=SM_Man_Date_To_Frame_Var, Drop_Down_But=Button_SM_Man_Date_To_Frame_Var, Variable=SP_Date_To_Variable), GUI_Level_ID=GUI_Level_ID)
    Sharepoint_Disabling_Man_Date_To(Selected_Value=SP_Date_To_Method, Entry_Field=SM_Man_Date_To_Frame_Var, Drop_Down_But=Button_SM_Man_Date_To_Frame_Var, Variable=SP_Date_To_Variable)    # Must be here because of initial value
    
    # Field - Password
    SP_Password_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    SP_Password_Frame_Var = SP_Password_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Password_Frame_Var.configure(placeholder_text="Fill your password.")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Manual(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Date_Range_Source: StringVar, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for download process.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Manual") 
    Use_Manual_Frame_Var = Use_Manual_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Manual_Frame_Var.configure(text="", variable=Download_Date_Range_Source)

    # Field - Date From
    Man_Date_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From", Field_Type="Date_Picker", Validation="Date") 
    Man_Date_From_Frame_Var = Man_Date_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_Date_From_Frame_Var = Man_Date_From_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_Date_From_Frame_Var.configure(placeholder_text="YYYY-MM-DD")
    Button_Man_Date_From_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_Date_From_Frame_Var, Clicked_on_Button=Button_Man_Date_From_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_Date_From_Frame_Var, message="Entry_DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Field - Date To
    Man_Date_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To", Field_Type="Date_Picker", Validation="Date")
    Man_Date_To_Frame_Var = Man_Date_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_Date_To_Frame_Var = Man_Date_To_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_Date_To_Frame_Var.configure(placeholder_text="YYYY-MM-DD")
    Button_Man_Date_To_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_Date_To_Frame_Var, Clicked_on_Button=Button_Man_Date_To_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_Date_To_Frame_Var, message="Entry_DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Exchange(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Data_Source: StringVar, GUI_Level_ID: int|None = None) -> CTkFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Exchange Server", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Exchange_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Exchange") 
    Use_Exchange_Frame_Var = Use_Exchange_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Exchange_Frame_Var.configure(text="", variable=Download_Data_Source)

    # Field - User ID
    Ex_Email_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Ex_Email_Frame_Var = Ex_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Email_Frame_Var.configure(placeholder_text=User_Email, placeholder_text_color="#949A9F")
    Ex_Email_Frame_Var.configure(state="disabled")

    # Field - Password
    Ex_Password_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    Ex_Password_Frame_Var = Ex_Password_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Password_Frame_Var.configure(placeholder_text="Fill your password.")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Per_Period_Selection(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    Today = datetime.now()
    Current_year = Today.year
    Current_month = Today.month
    Year_list = [Current_year - x for x in range(0, 5)]
    Month_list = [x for x in range(1, 13)]

    Year_From_Variable = IntVar(master=Frame, value=Current_year)
    Month_From_Variable = IntVar(master=Frame, value=Current_month)
    Year_To_Variable = IntVar(master=Frame, value=Current_year)
    Month_To_Variable = IntVar(master=Frame, value=Current_month)
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Previous Periods range", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define Which periods should be downloaded from TimeSheet History. Included.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Month From
    Past_Month_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="From Month", Field_Type="Input_OptionMenu") 
    Past_Month_From_Frame_Var = Past_Month_From_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Past_Month_From_Frame_Var.configure(variable=Month_From_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Past_Month_From_Frame_Var, values=Month_list, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Year From
    Past_Year_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="From Year", Field_Type="Input_OptionMenu") 
    Past_Year_From_Frame_Var = Past_Year_From_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Past_Year_From_Frame_Var.configure(variable=Year_From_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Past_Year_From_Frame_Var, values=Year_list, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Month To
    Past_Month_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="To Month", Field_Type="Input_OptionMenu") 
    Past_Month_To_Frame_Var = Past_Month_To_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Past_Month_To_Frame_Var.configure(variable=Month_To_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Past_Month_To_Frame_Var, values=Month_list, command=None, GUI_Level_ID=GUI_Level_ID)

    # Field - Year To
    Past_Year_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="To Year", Field_Type="Input_OptionMenu") 
    Past_Year_To_Frame_Var = Past_Year_To_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Past_Year_To_Frame_Var.configure(variable=Year_To_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Past_Year_To_Frame_Var, values=Year_list, command=None, GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Pre_Download_Sharepoint(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    User_ID = Settings["0"]["General"]["User"]["Code"]

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Sharepoint - authenticate", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Used for Sharepoint authentication to download data.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - User ID
    Past_SP_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    Past_SP_User_ID_Text_Frame_Var = Past_SP_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    Past_SP_User_ID_Text_Frame_Var.configure(placeholder_text=User_ID, placeholder_text_color="#949A9F")
    Past_SP_User_ID_Text_Frame_Var.configure(state="disabled")

    # Field - User Email
    Past_SP_Email_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Past_SP_Email_Text_Frame_Var = Past_SP_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    Past_SP_Email_Text_Frame_Var.configure(placeholder_text=User_Email, placeholder_text_color="#949A9F")
    Past_SP_Email_Text_Frame_Var.configure(state="disabled")

    # Field - Password
    Past_SP_Password_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    Past_SP_Password_Frame_Var = Past_SP_Password_Frame.children["!ctkframe3"].children["!ctkentry"]
    Past_SP_Password_Frame_Var.configure(placeholder_text="Fill your password.")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
