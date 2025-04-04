# Import Libraries
from datetime import datetime
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_RadioButton, WidgetRow_Input_Entry, WidgetRow_OptionMenu, WidgetRow_Date_Picker

from customtkinter import CTk, CTkFrame, StringVar, IntVar

# -------------------------------------------------------------------------------------------------------------------------------------------------- Download Page Widgets -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Download_Sharepoint(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Date_Range_Source: StringVar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    User_Email = Settings["0"]["General"]["User"]["Email"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    SP_Date_From_Method = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method"]
    SP_Date_From_Method_list = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method_List"]
    SP_Date_To_Method = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method"]
    SP_Date_To_Method_list = Settings["0"]["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method_List"]
    SP_Date_From_Variable = StringVar(master=Frame, value=SP_Date_From_Method)
    SP_Date_To_Variable = StringVar(master=Frame, value=SP_Date_To_Method)

    # ------------------------- Main Functions -------------------------#
    # Widget
    Download_Sharepoint_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Sharepoint", Additional_Text="Must be on Local network or VPN.", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Time-sheets for download process.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    SP_User_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="User ID", placeholder_text=User_ID, placeholder_text_color="#949A9F")
    SP_User_ID_Row.Freeze()
    SP_Email_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Email", placeholder_text=User_Email, placeholder_text_color="#949A9F")
    SP_Email_Row.Freeze()
    SP_Date_From_Option_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Date From", Variable=SP_Date_From_Variable, Values=SP_Date_From_Method_list, GUI_Level_ID=GUI_Level_ID) 

    SM_Man_Date_To_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Manual Date To", Date_format=Date_Format, Value="", placeholder_text_color="#949A9F", Button_ToolTip="Date Picker.", Save_To=None, Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    Date_To_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Today", "Manual", "Last Report Day"], Freeze_fields=[[SM_Man_Date_To_Row],[],[SM_Man_Date_To_Row]])
    SP_Date_To_Option_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Date To", Variable=SP_Date_To_Variable, Values=SP_Date_To_Method_list, Field_list=[SM_Man_Date_To_Row], Field_Blocking_dict=Date_To_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    SP_Password_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Password", Label="Password", placeholder_text="Fill your password.")

    Use_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Sharepoint", "Manual"], Freeze_fields=[[],[SP_Password_Row]])
    Use_Sharepoint_Row = WidgetRow_RadioButton(Settings=Settings, Configuration=Configuration, master=Download_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Download_Date_Range_Source, ON_Value="Sharepoint", Field_list=[SP_Password_Row], Field_Blocking_dict=Use_Fields_Blocking_dict)

    # Add Fields to Widget Body
    Download_Sharepoint_Widget.Add_row(Rows=[Use_Sharepoint_Row, SP_User_ID_Row, SP_Email_Row, SP_Date_From_Option_Row, SP_Date_To_Option_Row, SM_Man_Date_To_Row, SP_Password_Row])

    return Download_Sharepoint_Widget


def Download_Manual(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Date_Range_Source: StringVar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Download_Manual_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for download process.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Man_Date_From_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Download_Manual_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Date From", Date_format=Date_Format, Value="", placeholder_text_color="#949A9F", Button_ToolTip="Date Picker.", Save_To=None, Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    Man_Date_To_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Download_Manual_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Date To", Date_format=Date_Format, Value="", placeholder_text_color="#949A9F", Button_ToolTip="Date Picker.", Save_To=None, Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    Use_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Sharepoint", "Manual"], Freeze_fields=[[Man_Date_From_Row, Man_Date_To_Row],[]])
    Use_Manual_Row = WidgetRow_RadioButton(Settings=Settings, Configuration=Configuration, master=Download_Manual_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Download_Date_Range_Source, ON_Value="Manual", Field_list=[Man_Date_From_Row, Man_Date_To_Row], Field_Blocking_dict=Use_Fields_Blocking_dict)

    # Add Fields to Widget Body
    Download_Manual_Widget.Add_row(Rows=[Use_Manual_Row, Man_Date_From_Row, Man_Date_To_Row])

    return Download_Manual_Widget

def Download_Exchange(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, Download_Data_Source: StringVar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Download_Exchange_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Exchange Server", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Ex_Email_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Download_Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Email", placeholder_text=User_Email, placeholder_text_color="#949A9F")
    Ex_Email_Row.Freeze()
    Ex_Password_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Download_Exchange_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Password", Label="Password", placeholder_text="Fill your password.")

    # Add Fields to Widget Body
    Download_Exchange_Widget.Add_row(Rows=[Ex_Email_Row, Ex_Password_Row])

    return Download_Exchange_Widget

def Per_Period_Selection(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
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
    # Widget
    Previous_Periods_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Previous Periods range", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define Which periods should be downloaded from TimeSheet History. Included.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Past_Month_From_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Previous_Periods_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="From Month", Variable=Month_From_Variable, Values=Month_list, GUI_Level_ID=GUI_Level_ID) 
    Past_Year_From_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Previous_Periods_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="From Year", Variable=Year_From_Variable, Values=Year_list, GUI_Level_ID=GUI_Level_ID) 
    Past_Month_To_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Previous_Periods_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="To Month", Variable=Month_To_Variable, Values=Month_list, GUI_Level_ID=GUI_Level_ID) 
    Past_Year_To_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Previous_Periods_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="To Year", Variable=Year_To_Variable, Values=Year_list, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Previous_Periods_Widget.Add_row(Rows=[Past_Month_From_Row, Past_Year_From_Row, Past_Month_To_Row, Past_Year_To_Row])

    return Previous_Periods_Widget

def Pre_Download_Sharepoint(Settings: dict, Configuration:dict, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    User_Email = Settings["0"]["General"]["User"]["Email"]
    User_ID = Settings["0"]["General"]["User"]["Code"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Pre_Sharepoint_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Sharepoint - authenticate", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Used for Sharepoint authentication to download data.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    SP_User_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Pre_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="User ID", placeholder_text=User_ID, placeholder_text_color="#949A9F")
    SP_User_ID_Row.Freeze()
    SP_Email_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Pre_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Email", placeholder_text=User_Email, placeholder_text_color="#949A9F")
    SP_Email_Row.Freeze()
    SP_Pre_Password_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Pre_Sharepoint_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Password", Label="Password", placeholder_text="Fill your password.")

    # Add Fields to Widget Body
    Pre_Sharepoint_Widget.Add_row(Rows=[SP_User_ID_Row, SP_Email_Row, SP_Pre_Password_Row])

    return Pre_Sharepoint_Widget