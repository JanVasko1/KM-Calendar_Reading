# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, StringVar, CTkEntry
from CTkMessagebox import CTkMessagebox

# -------------------------------------------------------------------------------------------------------------------------------------------------- Set Defaults -------------------------------------------------------------------------------------------------------------------------------------------------- #
client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
Settings = Defaults_Lists.Load_Settings()
Configuration = Defaults_Lists.Load_Configuration() 

# Sharepoint
SP_Auth_Email = Settings["General"]["Downloader"]["Sharepoint"]["Auth"]["Email"]
SP_Person_ID = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]

SP_Date_From_Method = Settings["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method"]
SP_Date_From_Method_list = Settings["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_From"]["Date_From_Method_List"]
SP_Date_To_Method = Settings["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method"]
SP_Date_To_Method_list = Settings["General"]["Downloader"]["Sharepoint"]["Download_Options"]["Date_To"]["Date_To_Method_List"]

# Outlook
Outlook_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]

# -------------------------------------------------------------------------------------------------------------------------------------------------- Download Page Widgets -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Download_Sharepoint(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    def Sharepoint_Disabeling_Man_Date_To(Selected_Value: str, Entry_Field: CTkEntry, Variable: StringVar) -> None:
        Variable.set(value=Selected_Value)
        if (Selected_Value == "Today") or (Selected_Value == "Last Report Day"):
            Entry_Field.delete(first_index=0, last_index=1000)
            Entry_Field.configure(placeholder_text="")
            Entry_Field.configure(state="disabled")
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Entry_Field.configure(placeholder_text="YYYY-MM-DD")
        else:
            CTkMessagebox(title="Error", message="Downlaod To Method not allowed.", icon="cancel", fade_in_duration=1)

    SP_Date_From_Variable = StringVar(master=Frame, value=SP_Date_From_Method)
    SP_Date_To_Variable = StringVar(master=Frame, value=SP_Date_To_Method)

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Sharepoint - missing dates", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Get Date-From and Date-To directly from Sharepoint Timesheets for donwload process.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Sharepoint_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Sharepoint") 
    Use_Sharepoint_Frame_Var = Use_Sharepoint_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Sharepoint_Frame_Var.configure(text="", variable=Download_Date_Range_Source)

    # Field - User ID
    SP_User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal") 
    SP_User_ID_Text_Frame_Var = SP_User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_User_ID_Text_Frame_Var.configure(placeholder_text=SP_Person_ID, placeholder_text_color="#949A9F")
    SP_User_ID_Text_Frame_Var.configure(state="disabled")

    # Field - User Email
    SP_Email_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    SP_Email_Text_Frame_Var = SP_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Email_Text_Frame_Var.configure(placeholder_text=SP_Auth_Email, placeholder_text_color="#949A9F")
    SP_Email_Text_Frame_Var.configure(state="disabled")

    # Field - Date From Method
    SP_Date_From_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From", Field_Type="Input_OptionMenu") 
    SP_Date_From_Option_Var = SP_Date_From_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    SP_Date_From_Option_Var.configure(variable=SP_Date_From_Variable)
    Elements.Get_Option_Menu_Advance(attach=SP_Date_From_Option_Var, values=SP_Date_From_Method_list, command=None)

    # Field - Date To Method
    SP_Date_To_Option = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To", Field_Type="Input_OptionMenu") 
    SP_Date_To_Option_Var = SP_Date_To_Option.children["!ctkframe3"].children["!ctkoptionmenu"]
    SP_Date_To_Option_Var.configure(variable=SP_Date_To_Variable)

    # Field - Manual Date To
    SM_Man_Date_To_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Manual Date To", Field_Type="Input_Normal", Validation="Date") 
    SM_Man_Date_To_Frame_Var = SM_Man_Date_To_Frame.children["!ctkframe3"].children["!ctkentry"]

    # Disabling fields --> Manula Date To 
    Elements.Get_Option_Menu_Advance(attach=SP_Date_To_Option_Var, values=SP_Date_To_Method_list, command = lambda SP_Date_To_Option_Var: Sharepoint_Disabeling_Man_Date_To(Selected_Value=SP_Date_To_Option_Var, Entry_Field=SM_Man_Date_To_Frame_Var, Variable=SP_Date_To_Variable))
    Sharepoint_Disabeling_Man_Date_To(Selected_Value=SP_Date_To_Method, Entry_Field=SM_Man_Date_To_Frame_Var, Variable=SP_Date_To_Variable)    # Must be here because of initial value
    

    # Field - Password
    SP_Password_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    SP_Password_Frame_Var = SP_Password_Frame.children["!ctkframe3"].children["!ctkentry"]
    SP_Password_Frame_Var.configure(placeholder_text="Fill your password.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Manual(Frame: CTk|CTkFrame, Download_Date_Range_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Manual", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Define manual dates for downlaod process. Format YYYY-MM-DD")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Manual") 
    Use_Manual_Frame_Var = Use_Manual_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Manual_Frame_Var.configure(text="", variable=Download_Date_Range_Source)

    # Field - User ID
    Man_Date_From_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date From", Field_Type="Input_Normal", Validation="Date") 
    Man_Date_From_Frame_Var = Man_Date_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    Man_Date_From_Frame_Var.configure(placeholder_text="YYYY-MM-DD")

    # Field - User Email
    Man_Date_To_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date To", Field_Type="Input_Normal", Validation="Date")
    Man_Date_To_Frame_Var = Man_Date_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    Man_Date_To_Frame_Var.configure(placeholder_text="YYYY-MM-DD")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Exchange(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Exchange Server", Additional_Text="Must be on Local network or VPN", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Konica Minolta Exchange server directly.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Exchange_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Exchange") 
    Use_Exchange_Frame_Var = Use_Exchange_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Exchange_Frame_Var.configure(text="", variable=Download_Data_Source)

    # Field - User ID
    Ex_Email_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Ex_Email_Frame_Var = Ex_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Email_Frame_Var.configure(placeholder_text=Outlook_Email, placeholder_text_color="#949A9F")
    Ex_Email_Frame_Var.configure(state="disabled")

    # Field - Password
    Ex_Password_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Password", Field_Type="Password_Normal") 
    Ex_Password_Frame_Var = Ex_Password_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ex_Password_Frame_Var.configure(placeholder_text="Fill your password.")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Download_Outlook(Frame: CTk|CTkFrame, Download_Data_Source: StringVar) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Outlook Classic Client", Additional_Text="Must be updated befor download", Widget_size="Single_size", Widget_Label_Tooltip="Data source is Windows installtion of Outlook Classic client.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Outlook_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_RadioButton", Var_Value="Outlook_Client") 
    Use_Outlook_Frame_Var = Use_Outlook_Frame.children["!ctkframe3"].children["!ctkradiobutton"]
    Use_Outlook_Frame_Var.configure(text="", variable=Download_Data_Source)

    # Field - User ID
    Out_Email_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Email", Field_Type="Input_Normal")
    Out_Email_Frame_Var = Out_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    Out_Email_Frame_Var.configure(placeholder_text=Outlook_Email, placeholder_text_color="#949A9F")
    Out_Email_Frame_Var.configure(state="disabled")

    #? Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main