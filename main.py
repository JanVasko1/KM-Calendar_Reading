
# Import Libraries
import os
import time

from customtkinter import CTk, CTkFrame, set_appearance_mode
import pywinstyles

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    User_Name = Settings["General"]["User"]["Name"]
    User_ID = Settings["General"]["User"]["Code"]
    User_Email = Settings["General"]["User"]["Email"]

    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = Defaults_Lists.Get_Current_Theme() 
        if Current_Theme == "Dark":
            set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            set_appearance_mode(mode_string="dark")
        else:
            set_appearance_mode(mode_string="system")

    # ------------------------- Main Functions -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Set="lucide", Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal")

    # Account Mail
    Frame_User_Email = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Email.configure(text=User_Email)
    Frame_User_Email.pack_propagate(flag=False)

    # Account ID
    Frame_User_ID = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_ID.configure(text=User_ID)
    Frame_User_ID.pack_propagate(flag=False)

    # Account Name
    Frame_User_Name = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Name.configure(text=User_Name)
    Frame_User_Name.pack_propagate(flag=False)

    # Build look of Widget
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Email.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

# ------------------------------------------------------------------------------------------------------------------------------------ Side Bar ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame) -> CTkFrame:
    User_Type = Settings["General"]["User"]["User_Type"]

    global Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady, Icon_Default_pady, Logo_Height, Logo_width, Side_Bar_Frame_Height, Icon_Button_Height, Logo_pady
    
    if User_Type == "User":
        Icon_count = 6
    elif User_Type == "Manager":
        Icon_count = 7

    Icon_Default_pady = 10
    Logo_Height = 40
    Logo_width = 70
    Logo_pady = 20
    
    Side_Bar_Frame_Height = Side_Bar_Frame._current_height
    Icon_Button_Height = Configuration["Buttons"]["Picture_SideBar"]["height"]

    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()
            window.update_idletasks()

    def Show_Download_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Download as P_Download
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        P_Download.Page_Download(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_DashBoard as P_DashBoard
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_DashBoard.Page_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Team_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_My_Team as P_My_Team
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_My_Team.Page_User_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Data_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Data as P_Data
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Data.Page_Data(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Information as P_Information
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Information.Page_Information(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Settings as P_Settings
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Define_Icons_Top_Bottom_indent(Frame_Height: int, Icon_count: int, Icon_Button_Height: int, Icon_Default_pady: int, Logo_height: int, Logo_pady: int) -> list[int, int]:
        Total_Logo_Height = Logo_height + (2 * Logo_pady)
        Total_Icons_Height = Icon_count * (Icon_Button_Height + (2 * Icon_Default_pady))
        Side_Bar_Middle_point = Frame_Height // 2
        Side_Bar_Icon_top_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2)
        Side_Bar_Icon_Bottom_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2) - Total_Logo_Height - Logo_pady

        return Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")


    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="download", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Download_Row = 0
    elif User_Type == "Manager":
        Download_Row = 0
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=Download_Row))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Download new data.", ToolTip_Size="Normal")

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="layout-dashboard", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Dashboard_Row = 1
    elif User_Type == "Manager":
        Dashboard_Row = 1
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Dashboard_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Dashboard, message="My dashboard page.", ToolTip_Size="Normal")

    # Page - Users Dashboard
    if User_Type == "User":
        pass
    elif User_Type == "Manager":
        Team_Row = 2
        Icon_Frame_Users_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="users", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
        Icon_Frame_Users_Dashboard.configure(command = lambda: Show_Team_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Team_Row))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Users_Dashboard, message="My Team page.", ToolTip_Size="Normal")

    # Page - Data
    Icon_Frame_Data = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="file-spreadsheet", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Data_Row = 2
    elif User_Type == "Manager":
        Data_Row = 3
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page(Active_Window = Active_Window, Side_Bar_Row=Data_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Data, message="Data to export page.", ToolTip_Size="Normal")

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Information_Row = 3
    elif User_Type == "Manager":
        Information_Row = 4
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=Information_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Information, message="Application information page.", ToolTip_Size="Normal")

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Settings_Row = 4
    elif User_Type == "Manager":
        Settings_Row = 5
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=Settings_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal")

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_SideBar")
    Icon_Frame_Close.configure(command = lambda: window.quit())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Close, message="Close application.", ToolTip_Size="Normal")

    Konica_Logo = Elements.Get_Background_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=Logo_width, heigh=Logo_Height)

    # Define intend
    Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady = Define_Icons_Top_Bottom_indent(Frame_Height=Side_Bar_Frame_Height, Icon_count=Icon_count, Icon_Button_Height=Icon_Button_Height, Icon_Default_pady=Icon_Default_pady, Logo_height=Logo_Height, Logo_pady=Logo_pady)

    # Build look of Widget
    Active_Window.grid(row=1, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
    if User_Type == "User":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=5, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Konica_Logo.grid(row=6, column=0, padx=(0, 0), pady=Logo_pady, sticky="", columnspan=2)
    elif User_Type == "Manager":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Users_Dashboard.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=5, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=6, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Konica_Logo.grid(row=7, column=0, padx=(0, 0), pady=Logo_pady, sticky="", columnspan=2)

    # Initiate default window
    Show_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Dashboard_Row)


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheets")
        super().iconbitmap(bitmap=Defaults_Lists.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\TimeSheet.ico"))
        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self,event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self,event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

if __name__ == "__main__":
    Settings = Defaults_Lists.Load_Settings()
    Configuration = Defaults_Lists.Load_Configuration() 

    
    Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

    # Create folders if do not exists
    try:
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\DashBoard\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\Downloads\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\My_Team\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\History\\"))
    except:
        pass

    window = Win()
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    Window_Frame_width = 1800
    Window_Frame_height = 900
    left_position = int(display_width // 2 - Window_Frame_width // 2)
    top_position = int(display_height // 2 - Window_Frame_height // 2)
    window.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

    # Rounded corners 
    window.config(background="#000001")
    window.attributes("-transparentcolor", "#000001")

    # Base Windows style setup --> always keep normal before change
    set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")
    pywinstyles.apply_style(window=window, style=Win_Style_Actual)

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Configuration=Configuration, Frame=window, Frame_Size="Background")
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="Work_Area")
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Header")
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Detail = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
    Frame_Work_Area_Detail.pack_propagate(flag=False)
    Frame_Work_Area_Detail.pack(side="left", fill="none", expand=False)

    Get_Header(Frame=Frame_Header)
    Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar)
    

    # run
    window.mainloop()