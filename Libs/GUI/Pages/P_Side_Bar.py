# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Pages.P_Download as P_Download
import Libs.GUI.Pages.P_DashBoard as P_DashBoard
import Libs.GUI.Pages.P_My_Team as P_My_Team
import Libs.GUI.Pages.P_Data as P_Data
import Libs.GUI.Pages.P_Information as P_Information
import Libs.GUI.Pages.P_Settings_App as P_Settings_App
import Libs.GUI.Pages.P_Settings_Event as P_Settings_Event

import Libs.GUI.Elements as Elements
class SidebarApp:
    def __init__(self, Side_Bar_Frame: CTkFrame, Settings: dict, Configuration: dict, window: CTk, Frame_Work_Area_Main: CTkFrame):
        self.Side_Bar_Frame = Side_Bar_Frame
        self.Settings = Settings
        self.Configuration = Configuration
        self.window = window
        self.Frame_Work_Area_Main = Frame_Work_Area_Main

        # Application
        self.Application = Defaults_Lists.Load_Application()
        self.Program_Version = self.Application["Application"]["Version"]

        # User Type
        User_Type = Settings["0"]["General"]["User"]["User_Type"]
            
        # Add buttons to the sidebar
        if User_Type == "User":
            self.names = ["Download", 
                            "Dashboard", 
                            "Data", 
                            "Information", 
                            "Gen_Settings",
                            "Event_Settings",
                            "Close"]
            
            self.icons = ["download", 
                        "layout-dashboard", 
                        "file-spreadsheet", 
                        "info", 
                        "monitor-cog",
                        "calendar-cog",
                        "power"]
            
            self.messages = ["Download new data.", 
                            "My dashboard page.", 
                            "Data to export page.", 
                            "Application information page.",
                            "General application settings page.", 
                            "Events relation application settings page.", 
                            "Close application."]
            
            # Icons
            self.Icon_Default_pady = 10
            self.Side_Bar_Top_pady = 195
            self.Side_Bar_Bottom_pady = 235
        elif User_Type == "Manager":
            self.names = ["Download", 
                            "Dashboard", 
                            "Team_Dashboard", 
                            "Data", 
                            "Information", 
                            "Gen_Settings",
                            "Event_Settings",
                            "Close"]
            
            self.icons = ["download", 
                        "layout-dashboard", 
                        "users", 
                        "file-spreadsheet", 
                        "info", 
                        "monitor-cog",
                        "calendar-cog",
                        "power"]
            
            self.messages = ["Download new data.", 
                            "My dashboard page.", 
                            "My Team page.", 
                            "Data to export page.", 
                            "Application information page.",
                            "General application settings page.", 
                            "Events relation application settings page.", 
                            "Close application."]
            
            # Icons
            self.Icon_Default_pady = 10
            self.Side_Bar_Top_pady = 165
            self.Side_Bar_Bottom_pady = 210

        self.Icon_count = len(self.names)

        # Active button tracker
        self.active_button = "Download"
        
        # Build SideBar
        self.create_company_logo()
        self.create_sidebar_buttons()
        self.create_Application_version()
        self.Show_Download_Page()

    def create_company_logo(self):
        Logo = Elements.Get_Custom_Image(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=50)
        Logo.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    def create_sidebar_buttons(self):
        self.Active_Window = 0
        self.buttons = []
        for button_index, button_name in enumerate(self.names):
            if button_name == "Close":
                # TurnOff wit red color
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
            elif  button_name == self.active_button:
                # Initiate Active Button
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active", Button_Size="Picture_Transparent")
            else:
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
            button.configure(command = self.create_command(button_index=button_index, button_name=button_name))
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=button, message=self.messages[button_index], ToolTip_Size="Normal", GUI_Level_ID=0)

            # Place button 
            if button_index == 0:
                # First Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Side_Bar_Top_pady, self.Icon_Default_pady))
            elif (button_index > 0) and (button_index < self.Icon_count - 1):
                # Middle Icons
                button.pack(side="top", fill="none", expand=False, padx=5, pady=self.Icon_Default_pady)
            else:
                # Last Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Icon_Default_pady, self.Side_Bar_Bottom_pady))
            self.buttons.append(button)

    def create_Application_version(self):
        Program_Version_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
        Program_Version_text.configure(text=f"{self.Program_Version}", text_color = "#efefef")
        Program_Version_text.pack(side="top", fill="none", expand=False, padx=5, pady=(0, 10))

    def create_command(self, button_index, button_name):
        """Return a command function for the given page."""
        def command():
            self.change_page(button_index=button_index, button_name=button_name)
        return command

    def change_page(self, button_index, button_name):
        # Reset the color of all buttons
        for button_index_intern, button in enumerate(self.buttons):
            if button_index_intern < self.Icon_count - 1:
                button.configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index_intern], Icon_Size="Side_Bar_regular"))

        # Mark Active button
        self.buttons[button_index].configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active"))


        if button_name == "Download":
            self.Show_Download_Page()
        elif button_name == "Dashboard":
            self.Show_Dashboard_Page()
        elif button_name == "Team_Dashboard":
            self.Show_Team_Dashboard_Page()
        elif button_name == "Data":
            self.Show_Data_Page()
        elif button_name == "Information":
            self.Show_Information_Page()
        elif button_name == "Gen_Settings":
            self.Show_App_Settings_Page()
        elif button_name == "Event_Settings":
            self.Show_Event_Settings_Page()
        elif button_name == "Close":
            self.Show_Close_Page()
        else:
            pass

    def Clear_Frame(self, Pre_Working_Frame: CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()

    def Show_Download_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Download.Page_Download(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_Dashboard_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_DashBoard.Page_Dashboard(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Team_Dashboard_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_My_Team.Page_User_Dashboard(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Data_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Data.Page_Data(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Information_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Information.Page_Information(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_App_Settings_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Settings_App.Page_App_Settings(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Event_Settings_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Settings_Event.Page_Event_Settings(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
    
    def Show_Close_Page(self) -> None:
        # Delete Operational data from Settings
        self.window.quit()