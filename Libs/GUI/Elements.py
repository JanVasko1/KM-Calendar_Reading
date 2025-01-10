# Import Libraries
from PIL import Image

from customtkinter import CTkButton, CTk, CTkFrame, CTkScrollableFrame, CTkEntry, CTkLabel, CTkFont, CTkImage, CTkRadioButton, CTkTabview, CTkOptionMenu, CTkCheckBox, CTkProgressBar, CTkInputDialog, CTkComboBox
from CTkTable import CTkTable
from CTkColorPicker import CTkColorPicker
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

from iconipy import IconFactory 
import winaccent

import Libs.Defaults_Lists as Defaults_Lists

Configuration = Defaults_Lists.Load_Configuration() 
Accent_Color_Mode = Configuration["Global_Apperance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
Accent_Color_Style_Manual = Configuration["Global_Apperance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

Hover_Color_Mode = Configuration["Global_Apperance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
Hover_Color_Style_Manual = Configuration["Global_Apperance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

# Accent Color
if Accent_Color_Mode == "System":
    Accent_Color = winaccent.accent_normal
elif Accent_Color_Mode == "Manual":
    Accent_Color = Accent_Color_Style_Manual
elif Accent_Color_Mode == "Widget":
    Accent_Color = ""
else:
    Accent_Color = ""
    CTkMessagebox(title="Error", message=f"Accent Color mode: {Accent_Color_Mode}, which is not supported.", icon="cancel", fade_in_duration=1)

# Hover Color
if Hover_Color_Mode == "Manual":
    Hover_Color = Hover_Color_Style_Manual
elif Hover_Color_Mode == "Widget":
    Hover_Color = ""
else:
    Hover_Color = ""
    CTkMessagebox(title="Error", message=f"Hover Color mode: {Hover_Color_Mode}, which is not supported.", icon="cancel", fade_in_duration=1)


# ---------------------------------------------- Local Functions ----------------------------------------------# 
def Define_Color(Color_json: list|str, Global_Color: str) -> tuple|str|None:
    if type(Color_json) is list:
        Selected_color = tuple(Color_json)
    else:
        if Color_json == "Global_Accent_Color":
            Selected_color = Global_Color
        elif Color_json == "Global_Hover_Color":
            Selected_color = Global_Color
        else:
            Selected_color = Color_json
    return Selected_color

# ---------------------------------------------- Font ----------------------------------------------# 
def Get_Font(Font_Size: str) -> CTkFont:
    Configuration_Font_Text_Main = Configuration["Font"][f"{Font_Size}"]
    Font_Text_Main = CTkFont(
        family = Configuration_Font_Text_Main["family"],
        size = Configuration_Font_Text_Main["size"],
        weight = Configuration_Font_Text_Main["weight"],
        slant = Configuration_Font_Text_Main["slant"],
        underline = Configuration_Font_Text_Main["underline"],
        overstrike = Configuration_Font_Text_Main["overstrike"])
    return Font_Text_Main

# ---------------------------------------------- Text ----------------------------------------------# 
def Get_Label(Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str) -> CTkLabel:
    Configuration_Text_Main = Configuration["Labels"][f"{Label_Size}"]
    Text_Main = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size=Font_Size),
        height = Configuration_Text_Main["height"],
        fg_color = Configuration_Text_Main["fg_color"],
        text_color = tuple(Configuration_Text_Main["text_color"]),
        anchor = Configuration_Text_Main["anchor"],
        padx = Configuration_Text_Main["padx"],
        pady = Configuration_Text_Main["pady"],
        wraplength = Configuration_Text_Main["wraplength"])
    return Text_Main

def Get_Label_Icon(Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str, Icon_Set: str, Icon_Name: str, Icon_Size: str,) -> CTkLabel:
    Frame_Label = Get_Label(Frame=Frame, Label_Size=Label_Size, Font_Size=Font_Size)
    CTK_Image = Get_CTk_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Label.configure(image=CTK_Image, text="", anchor="e")
    return Frame_Label

# ---------------------------------------------- Buttons ----------------------------------------------# 
def Get_Button(Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]

    fg_color = Define_Color(Color_json=Configuration_Button_Normal["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Button_Normal["border_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_Button_Normal["hover_color"], Global_Color=Hover_Color)

    Button_Normal = CTkButton(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        border_color = border_color,
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = fg_color,
        hover = Configuration_Button_Normal["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Normal["anchor"],
        text_color=tuple(Configuration_Button_Normal["text_color"]))
    return Button_Normal

def Get_Button_Icon(Frame: CTk|CTkFrame, Icon_Set: str, Icon_Name: str, Icon_Size: str, Button_Size: str) -> CTkFrame:
    Configuration_Button_Icon = Configuration["Buttons"][f"{Button_Size}"]

    fg_color = Define_Color(Color_json=Configuration_Button_Icon["fg_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_Button_Icon["hover_color"], Global_Color=Hover_Color)

    Frame_Button = CTkButton(
        master = Frame,
        width = Configuration_Button_Icon["width"],
        height = Configuration_Button_Icon["height"],
        corner_radius = Configuration_Button_Icon["corner_radius"],
        border_width = Configuration_Button_Icon["border_width"],
        bg_color = Configuration_Button_Icon["bg_color"],
        fg_color = fg_color,
        hover = Configuration_Button_Icon["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Icon["anchor"],
        text = "")
    CTK_Image = Get_CTk_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Button.configure(image=CTK_Image, text="")
    return Frame_Button

def Get_Button_Chart(Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Chart = Configuration["Buttons"][f"{Button_Size}"]

    fg_color = Define_Color(Color_json=Configuration_Button_Chart["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Button_Chart["border_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_Button_Chart["hover_color"], Global_Color=Hover_Color)

    Frame_Button = CTkButton(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Button_Chart["width"],
        height = Configuration_Button_Chart["height"],
        corner_radius = Configuration_Button_Chart["corner_radius"],
        border_width = Configuration_Button_Chart["border_width"],
        border_color = border_color,
        bg_color = Configuration_Button_Chart["bg_color"],
        fg_color = fg_color,
        hover = Configuration_Button_Chart["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Chart["anchor"],
        text_color=tuple(Configuration_Button_Chart["text_color"]))
    return Frame_Button

# ---------------------------------------------- Fields ----------------------------------------------# 
def Get_Entry_Field(Frame: CTk|CTkFrame, Field_Size: str) -> CTkEntry:
    Configuration_Field = Configuration["Fields"]["Entry"][f"{Field_Size}"]

    fg_color = Define_Color(Color_json=Configuration_Field["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Field["border_color"], Global_Color=Accent_Color)

    Field = CTkEntry(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Field["width"],
        height = Configuration_Field["height"],
        corner_radius = Configuration_Field["corner_radius"],
        border_width = Configuration_Field["border_width"],
        border_color = border_color,
        bg_color = Configuration_Field["bg_color"],
        fg_color = fg_color,
        text_color = tuple(Configuration_Field["text_color"]),
        placeholder_text_color = tuple(Configuration_Field["placeholder_text_color"]))
    return Field

def Get_Password_Normal(Frame: CTk|CTkFrame) -> CTkEntry:
    Configuration_Password_Normal = Configuration["Fields"]["Entry"]["Normal"]

    fg_color = Define_Color(Color_json=Configuration_Password_Normal["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Password_Normal["border_color"], Global_Color=Accent_Color)

    Password_Normal = CTkEntry(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Password_Normal["width"],
        height = Configuration_Password_Normal["height"],
        corner_radius = Configuration_Password_Normal["corner_radius"],
        border_width = Configuration_Password_Normal["border_width"],
        border_color = border_color,
        bg_color = Configuration_Password_Normal["bg_color"],
        fg_color = fg_color,
        text_color = tuple(Configuration_Password_Normal["text_color"]),
        placeholder_text_color = tuple(Configuration_Password_Normal["placeholder_text_color"]),
        show="*")
    return Password_Normal

def Get_RadioButton_Normal(Frame: CTk|CTkFrame) -> CTkRadioButton:
    Configuration_RadioButton_Normal = Configuration["Fields"]["RadioButton"]["Normal"]
    
    fg_color = Define_Color(Color_json=Configuration_RadioButton_Normal["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_RadioButton_Normal["border_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_RadioButton_Normal["hover_color"], Global_Color=Hover_Color)

    RadioButton_Normal = CTkRadioButton(
        master = Frame,
        width = Configuration_RadioButton_Normal["width"],
        height = Configuration_RadioButton_Normal["height"],
        radiobutton_width = Configuration_RadioButton_Normal["radiobutton_width"],
        radiobutton_height = Configuration_RadioButton_Normal["radiobutton_height"],
        corner_radius = Configuration_RadioButton_Normal["corner_radius"],
        border_width_unchecked = Configuration_RadioButton_Normal["border_width_unchecked"],
        border_width_checked = Configuration_RadioButton_Normal["border_width_checked"],
        fg_color = fg_color,
        border_color = border_color,
        hover_color = hover_color,
        hover = Configuration_RadioButton_Normal["hover"])
    return RadioButton_Normal

def Get_Option_Menu(Frame: CTk|CTkFrame) -> CTkOptionMenu:
    # Base CTkOptionMenu
    Configuration_Base_Option_Menu = Configuration["Fields"]["OptionMenu"]["BaseCTk"]["Normal"]
    
    fg_color_base = Define_Color(Color_json=Configuration_Base_Option_Menu["fg_color"], Global_Color=Accent_Color)
    button_hover_color_base = Define_Color(Color_json=Configuration_Base_Option_Menu["button_hover_color"], Global_Color=Hover_Color)
    dropdown_hover_color_base = Define_Color(Color_json=Configuration_Base_Option_Menu["dropdown_hover_color"], Global_Color=Hover_Color)

    Base_Option_Menu = CTkOptionMenu(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Base_Option_Menu["width"],
        height = Configuration_Base_Option_Menu["height"],
        corner_radius = Configuration_Base_Option_Menu["corner_radius"],
        bg_color = Configuration_Base_Option_Menu["bg_color"],
        fg_color = fg_color_base,
        button_color = tuple([Accent_Color, Accent_Color]),
        button_hover_color = button_hover_color_base,
        text_color = tuple(Configuration_Base_Option_Menu["text_color"]),
        text_color_disabled = tuple(Configuration_Base_Option_Menu["text_color_disabled"]),
        dropdown_fg_color = tuple(Configuration_Base_Option_Menu["dropdown_fg_color"]),
        dropdown_hover_color = dropdown_hover_color_base,
        dropdown_text_color = tuple(Configuration_Base_Option_Menu["dropdown_text_color"]),
        hover = Configuration_Base_Option_Menu["hover"],
        dynamic_resizing = Configuration_Base_Option_Menu["dynamic_resizing"],
        anchor = Configuration_Base_Option_Menu["anchor"])
    
    return Base_Option_Menu

def Get_Option_Menu_Advance(attach: CTkOptionMenu|CTkComboBox|CTkLabel|CTkButton, values: list) -> CTkScrollableDropdown:
    # Advance CTkScrollableDropdown
    Configuration_Advance_Option_Menu = Configuration["Fields"]["OptionMenu"]["AdvancedCTk"]["Normal"]

    fg_color_advance = Define_Color(Color_json=Configuration_Advance_Option_Menu["fg_color"], Global_Color=Accent_Color)
    scrollbar_button_hover_color_advance = Define_Color(Color_json=Configuration_Advance_Option_Menu["scrollbar_button_hover_color"], Global_Color=Hover_Color)
    hover_color_advance = Define_Color(Color_json=Configuration_Advance_Option_Menu["hover_color"], Global_Color=Hover_Color)

    #! Dodělat --> výšku a šížku

    Advance_Option_Menu = CTkScrollableDropdown(
        attach = attach,
        values = values,
        image_values = Configuration_Advance_Option_Menu["image_values"],
        width = Configuration_Advance_Option_Menu["width"],
        height = Configuration_Advance_Option_Menu["height"],
        fg_color = fg_color_advance,
        button_color = Configuration_Advance_Option_Menu["button_color"],
        hover_color = hover_color_advance,
        text_color = Configuration_Advance_Option_Menu["text_color"],
        button_height = Configuration_Advance_Option_Menu["button_height"],
        justify = Configuration_Advance_Option_Menu["justify"],
        frame_corner_radius = Configuration_Advance_Option_Menu["frame_corner_radius"],
        frame_border_width = Configuration_Advance_Option_Menu["frame_border_width"],
        frame_border_color = Configuration_Advance_Option_Menu["frame_border_color"],
        scrollbar = Configuration_Advance_Option_Menu["scrollbar"],
        scrollbar_button_color = Configuration_Advance_Option_Menu["scrollbar_button_color"],
        scrollbar_button_hover_color = scrollbar_button_hover_color_advance,
        resize = Configuration_Advance_Option_Menu["resize"],
        autocomplete = Configuration_Advance_Option_Menu["autocomplete"],
        alpha = Configuration_Advance_Option_Menu["alpha"])

    return Advance_Option_Menu

def Get_CheckBox(Frame: CTk|CTkFrame) -> CTkCheckBox:
    Configuration_Check_Box = Configuration["Fields"]["CheckBox"]["Normal"]
    
    fg_color = Define_Color(Color_json=Configuration_Check_Box["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Check_Box["border_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_Check_Box["hover_color"], Global_Color=Hover_Color)

    Check_Box = CTkCheckBox(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Check_Box["width"],
        height = Configuration_Check_Box["height"],
        checkbox_width = Configuration_Check_Box["checkbox_width"],
        checkbox_height = Configuration_Check_Box["checkbox_height"],
        corner_radius = Configuration_Check_Box["corner_radius"],
        border_width = Configuration_Check_Box["border_width"],
        border_color = border_color,
        bg_color = Configuration_Check_Box["bg_color"],
        fg_color = fg_color,
        hover_color = hover_color,
        checkmark_color = tuple(Configuration_Check_Box["checkmark_color"]),
        text_color = tuple(Configuration_Check_Box["text_color"]),
        hover = Configuration_Check_Box["hover"])
    return Check_Box


# ---------------------------------------------- Frames ----------------------------------------------# 
# NonScrolable
def Get_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_NonScrollable = Configuration["Frames"]["Page_Frames"][f"{Frame_Size}"]
    
    fg_color = Define_Color(Color_json=Configuration_NonScrollable["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_NonScrollable["border_color"], Global_Color=Accent_Color)

    Frame_NonScrolable = CTkFrame(
        master = Frame,
        width = Configuration_NonScrollable["width"],
        height = Configuration_NonScrollable["height"],
        corner_radius = Configuration_NonScrollable["corner_radius"],
        border_width = Configuration_NonScrollable["border_width"],
        border_color = border_color,
        bg_color = Configuration_NonScrollable["bg_color"],
        fg_color = fg_color)
    return Frame_NonScrolable

def Get_Dashboards_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_Dashboard = Configuration["Frames"]["Dashboard"]["Backbround_Frames"][f"{Frame_Size}"]
    
    fg_color = Define_Color(Color_json=Configuration_Dashboard["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Dashboard["border_color"], Global_Color=Accent_Color)

    Frame_NonScrolable = CTkFrame(
        master = Frame,
        width = Configuration_Dashboard["width"],
        height = Configuration_Dashboard["height"],
        corner_radius = Configuration_Dashboard["corner_radius"],
        border_width = Configuration_Dashboard["border_width"],
        border_color = border_color,
        bg_color = Configuration_Dashboard["bg_color"],
        fg_color = fg_color)
    return Frame_NonScrolable

# ------------------------------------------------------------------------------------------------------------ Widgets  ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------ Dashboards Widgets Frames ------------------------------------------#
def Get_Dashboard_Widget_Frame_Body(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Body = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Dash_Body["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Frame_Dash_Body["border_color"], Global_Color=Accent_Color)

    Frame_Body = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body["width"],
        height = Configuration_Frame_Dash_Body["height"],
        corner_radius = Configuration_Frame_Dash_Body["corner_radius"],
        border_width = Configuration_Frame_Dash_Body["border_width"],
        border_color = border_color,
        bg_color = Configuration_Frame_Dash_Body["bg_color"],
        fg_color = fg_color)
    return Frame_Body

def Get_Dashboard_Widget_Frame_Body_Scrollable(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkScrollableFrame:
    Configuration_Frame_Dash_Body_Scroll = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body_Scrollable"]
    
    fg_color = Define_Color(Color_json=Configuration_Frame_Dash_Body_Scroll["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Frame_Dash_Body_Scroll["border_color"], Global_Color=Accent_Color)

    Frame_Body_Scroll = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body_Scroll["width"],
        height = Configuration_Frame_Dash_Body_Scroll["height"],
        corner_radius = Configuration_Frame_Dash_Body_Scroll["corner_radius"],
        border_width = Configuration_Frame_Dash_Body_Scroll["border_width"],
        border_color = border_color,
        bg_color = Configuration_Frame_Dash_Body_Scroll["bg_color"],
        fg_color = fg_color,
        scrollbar_fg_color = Configuration_Frame_Dash_Body_Scroll["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Frame_Dash_Body_Scroll["scrollbar_button_color"]),
        scrollbar_button_hover_color = tuple([Accent_Color, Accent_Color]))
    return Frame_Body_Scroll

def Get_Dashboard_Widget_Frame_Header(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Header = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Header"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Dash_Header["fg_color"], Global_Color=Accent_Color)

    Frame_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Header["width"],
        height = Configuration_Frame_Dash_Header["height"],
        corner_radius = Configuration_Frame_Dash_Header["corner_radius"],
        border_width = Configuration_Frame_Dash_Header["border_width"],
        bg_color = Configuration_Frame_Dash_Header["bg_color"],
        fg_color = fg_color)
    return Frame_Header

def Get_Dashboard_Widget_Frame_Area(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Data = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Data_Area"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Dash_Data["fg_color"], Global_Color=Accent_Color)

    Frame_Area = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Data["width"],
        height = Configuration_Frame_Dash_Data["height"],
        corner_radius = Configuration_Frame_Dash_Data["corner_radius"],
        border_width = Configuration_Frame_Dash_Data["border_width"],
        bg_color = Configuration_Frame_Dash_Data["bg_color"],
        fg_color = fg_color)
    return Frame_Area

# ------------------------------------------ Widget Frames ------------------------------------------#
# Scrolable --> Frames For tables
def Get_Widget_Scrolable_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkScrollableFrame:
    Configuration_Scrollable = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"][f"{Frame_Size}"]

    fg_color = Define_Color(Color_json=Configuration_Scrollable["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Scrollable["border_color"], Global_Color=Accent_Color)

    Frame_Scrollable = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Scrollable["width"],
        corner_radius = Configuration_Scrollable["corner_radius"],
        border_width = Configuration_Scrollable["border_width"],
        border_color = border_color,
        bg_color = Configuration_Scrollable["bg_color"],
        fg_color =fg_color,
        scrollbar_fg_color = Configuration_Scrollable["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Scrollable["scrollbar_button_color"]),
        scrollbar_button_hover_color = tuple(Configuration_Scrollable["scrollbar_button_hover_color"]))
    return Frame_Scrollable

def Get_Widget_Frame_Body(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Body"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Single_Column["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Frame_Single_Column["border_color"], Global_Color=Accent_Color)

    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column["width"],
        corner_radius = Configuration_Frame_Single_Column["corner_radius"],
        border_width = Configuration_Frame_Single_Column["border_width"],
        border_color = border_color,
        bg_color = Configuration_Frame_Single_Column["bg_color"],
        fg_color = fg_color)
    return Frame_Single_Column

def Get_Widget_Frame_Header(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Header = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Header"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Single_Column_Header["fg_color"], Global_Color=Accent_Color)

    Frame_Single_Column_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Header["width"],
        height = Configuration_Frame_Single_Column_Header["height"],
        corner_radius = Configuration_Frame_Single_Column_Header["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Header["border_width"],
        bg_color = Configuration_Frame_Single_Column_Header["bg_color"],
        fg_color = fg_color)
    return Frame_Single_Column_Header

def Get_Widget_Frame_Area(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Data_Area = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Data_Area"]

    fg_color = Define_Color(Color_json=Configuration_Frame_Single_Column_Data_Area["fg_color"], Global_Color=Accent_Color)

    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Data_Area["width"],
        corner_radius = Configuration_Frame_Single_Column_Data_Area["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Data_Area["border_width"],
        bg_color = Configuration_Frame_Single_Column_Data_Area["bg_color"],
        fg_color = fg_color)
    return Frame_Single_Column

# ------------------------------------------ Widget Field Frames ------------------------------------------#
def Get_Widget_Field_Frame_Area(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Area = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Area"]

    fg_color = Define_Color(Color_json=Configuration_Field_Single_Area["fg_color"], Global_Color=Accent_Color)

    Frame_Field_Single_Area = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Area["width"],
        height = Configuration_Field_Single_Area["height"],
        corner_radius = Configuration_Field_Single_Area["corner_radius"],
        border_width = Configuration_Field_Single_Area["border_width"],
        bg_color = Configuration_Field_Single_Area["bg_color"],
        fg_color = fg_color)
    return Frame_Field_Single_Area

def Get_Widget_Field_Frame_Label(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Label = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Label"]

    fg_color = Define_Color(Color_json=Configuration_Field_Single_Label["fg_color"], Global_Color=Accent_Color)

    Frame_Field_Single_Label = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Label["width"],
        height = Configuration_Field_Single_Label["height"],
        corner_radius = Configuration_Field_Single_Label["corner_radius"],
        border_width = Configuration_Field_Single_Label["border_width"],
        bg_color = Configuration_Field_Single_Label["bg_color"],
        fg_color = fg_color)
    return Frame_Field_Single_Label

def Get_Widget_Field_Frame_Space(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Space = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Space"]

    fg_color = Define_Color(Color_json=Configuration_Field_Single_Space["fg_color"], Global_Color=Accent_Color)

    Frame_Field_Single_Space = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Space["width"],
        height = Configuration_Field_Single_Space["height"],
        corner_radius = Configuration_Field_Single_Space["corner_radius"],
        border_width = Configuration_Field_Single_Space["border_width"],
        bg_color = Configuration_Field_Single_Space["bg_color"],
        fg_color = fg_color)
    return Frame_Field_Single_Space

def Get_Widget_Field_Frame_Value(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Value = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Value"]

    fg_color = Define_Color(Color_json=Configuration_Field_Single_Value["fg_color"], Global_Color=Accent_Color)

    Frame_Field_Single_Value = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Value["width"],
        height = Configuration_Field_Single_Value["height"],
        corner_radius = Configuration_Field_Single_Value["corner_radius"],
        border_width = Configuration_Field_Single_Value["border_width"],
        bg_color = Configuration_Field_Single_Value["bg_color"],
        fg_color = fg_color)
    return Frame_Field_Single_Value

# ------------------------------------------ Tab View ------------------------------------------ 
def Get_Tab_View(Frame: CTk|CTkFrame, Tab_size: str) -> CTkTabview:
    Configuration_TabView_Normal = Configuration["TabView"][f"{Tab_size}"]
    
    border_color = Define_Color(Color_json=Configuration_TabView_Normal["border_color"], Global_Color=Accent_Color)
    segmented_button_fg_color = Define_Color(Color_json=Configuration_TabView_Normal["segmented_button_fg_color"], Global_Color=Accent_Color)
    segmented_button_selected_hover_color = Define_Color(Color_json=Configuration_TabView_Normal["segmented_button_selected_hover_color"], Global_Color=Hover_Color)
    segmented_button_unselected_color = Define_Color(Color_json=Configuration_TabView_Normal["segmented_button_unselected_color"], Global_Color=Accent_Color)
    segmented_button_unselected_hover_color = Define_Color(Color_json=Configuration_TabView_Normal["segmented_button_unselected_hover_color"], Global_Color=Hover_Color)

    TabView_Normal = CTkTabview(
        master = Frame,
        width = Configuration_TabView_Normal["width"],
        height = Configuration_TabView_Normal["height"],
        corner_radius = Configuration_TabView_Normal["corner_radius"],
        border_width = Configuration_TabView_Normal["border_width"],
        border_color = border_color,
        bg_color = Configuration_TabView_Normal["bg_color"],
        segmented_button_fg_color = segmented_button_fg_color,
        segmented_button_selected_color = tuple([Accent_Color, Accent_Color]),
        segmented_button_selected_hover_color = segmented_button_selected_hover_color,
        segmented_button_unselected_color = segmented_button_unselected_color,
        segmented_button_unselected_hover_color = segmented_button_unselected_hover_color,
        text_color = tuple(Configuration_TabView_Normal["text_color"]),
        text_color_disabled = tuple(Configuration_TabView_Normal["text_color_disabled"]),
        anchor = Configuration_TabView_Normal["anchor"])
    return TabView_Normal

# ---------------------------------------------- Tables ----------------------------------------------# 
def Get_Table(Frame: CTk|CTkFrame, Table_size: str, rows: int, columns: int) -> CTkTable:
    Configuration_Table_Single = Configuration["Tables"][f"{Table_size}"]
    
    colors = Define_Color(Color_json=Configuration_Table_Single["colors"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_Table_Single["border_color"], Global_Color=Accent_Color)
    hover_color = Define_Color(Color_json=Configuration_Table_Single["hover_color"], Global_Color=Hover_Color)

    Table_Single = CTkTable(
        master = Frame,
        row = rows,
        column = columns,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Table_Single["width"],
        colors = colors,
        border_width = Configuration_Table_Single["border_width"],
        border_color = border_color,
        color_phase = Configuration_Table_Single["color_phase"],
        orientation = Configuration_Table_Single["orientation"],
        header_color = Accent_Color,
        corner_radius = Configuration_Table_Single["corner_radius"],
        hover_color = hover_color,
        wraplength = Configuration_Table_Single["wraplength"],
        justify = Configuration_Table_Single["justify"],
        anchor = Configuration_Table_Single["anchor"])
    return Table_Single

# ---------------------------------------------- Icons ----------------------------------------------# 
def Create_Icon(Icon_Set: str, Icon_Name: str, Icon_Size: str, Theme_index: int) -> Image:
    # Theme_Index: 0 --> light, 1 --> dark
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    
    if Icon_Size == "Side_Bar_active":
        Used_Icon_Color = Accent_Color
    else:
        Used_Icon_Color = Configuration_Icon["font_color"][Theme_index]
    
    Icon_Fact = IconFactory(
        icon_set = Icon_Set,
        icon_size = Configuration_Icon["icon_size"],
        font_size = Configuration_Icon["font_size"],
        font_color = Used_Icon_Color,
        outline_width = Configuration_Icon["outline_width"],
        outline_color = Configuration_Icon["outline_color"][Theme_index],
        background_color = Configuration_Icon["background_color"][Theme_index],
        background_radius = Configuration_Icon["background_radius"])
    Icon_PIL = Icon_Fact.asPil(Icon_Name)
    return Icon_PIL

def Get_CTk_Icon(Icon_Set: str, Icon_Name: str, Icon_Size: str) -> CTkImage:
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    Icon_Size_px = Configuration_Icon["icon_size"]
    Picture = CTkImage(
        light_image = Create_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=0),
        dark_image =Create_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=1),
        size = (Icon_Size_px, Icon_Size_px))
    return Picture

def Get_Backgruond_Image(Frame: CTk|CTkFrame, Image_Name: str, postfix: str, width: int, heigh: int) -> CTkLabel:
    Picture = CTkImage(
        light_image = Image.open(f"D:\\KM-Calendar_Reading\\Libs\\GUI\\Icons\\{Image_Name}_Light.{postfix}"),
        dark_image = Image.open(f"D:\\KM-Calendar_Reading\\Libs\\GUI\\Icons\\{Image_Name}_Dark.{postfix}"),
        size = (width, heigh))
    Background_Image_Label = Get_Label(Frame=Frame, Label_Size="Main", Font_Size="Main")
    Background_Image_Label.configure(image=Picture, text="")
    return Background_Image_Label

# ---------------------------------------------- Progress Bar ----------------------------------------------# 
def Get_ProgressBar(Frame: CTk|CTkFrame, orientation: str, Progress_Size: str) -> CTkProgressBar:
    Configuration_ProgressBar = Configuration["ProgressBar"][f"{orientation}"][f"{Progress_Size}"]
    
    fg_color = Define_Color(Color_json=Configuration_ProgressBar["fg_color"], Global_Color=Accent_Color)
    border_color = Define_Color(Color_json=Configuration_ProgressBar["border_color"], Global_Color=Accent_Color)
    progress_color = Define_Color(Color_json=Configuration_ProgressBar["progress_color"], Global_Color=Accent_Color)

    Progress_Bar = CTkProgressBar(
        master = Frame,
        width = Configuration_ProgressBar["width"],
        height = Configuration_ProgressBar["height"],
        border_width = Configuration_ProgressBar["border_width"],
        border_color = border_color,
        corner_radius = Configuration_ProgressBar["corner_radius"],
        bg_color = Configuration_ProgressBar["bg_color"],
        fg_color = fg_color,
        progress_color = progress_color,
        orientation = Configuration_ProgressBar["orientation"],
        determinate_speed = Configuration_ProgressBar["determinate_speed"],
        indeterminate_speed = Configuration_ProgressBar["indeterminate_speed"],
        mode = Configuration_ProgressBar["mode"])
    return Progress_Bar


# ---------------------------------------------- InputDialog ----------------------------------------------# 
def Get_DialogWindow(text: str, title: str, Dialog_Type: str) -> CTkInputDialog:
    Configuration_Dialog = Configuration["InputDialog"][f"{Dialog_Type}"]
    
    fg_color = Define_Color(Color_json=Configuration_Dialog["fg_color"], Global_Color=Accent_Color)
    text_color = Define_Color(Color_json=Configuration_Dialog["text_color"], Global_Color=Accent_Color)
    button_fg_color = Define_Color(Color_json=Configuration_Dialog["button_fg_color"], Global_Color=Accent_Color)
    button_hover_color = Define_Color(Color_json=Configuration_Dialog["button_hover_color"], Global_Color=Hover_Color)
    button_text_color = Define_Color(Color_json=Configuration_Dialog["button_text_color"], Global_Color=Accent_Color)
    entry_fg_color = Define_Color(Color_json=Configuration_Dialog["entry_fg_color"], Global_Color=Accent_Color)
    entry_border_color = Define_Color(Color_json=Configuration_Dialog["entry_border_color"], Global_Color=Accent_Color)
    entry_text_color = Define_Color(Color_json=Configuration_Dialog["entry_text_color"], Global_Color=Accent_Color)

    Dialog = CTkInputDialog(
        text=text,
        title=title,
        font = Get_Font(Font_Size="Field_Label"),
        fg_color = fg_color,
        text_color = text_color,
        button_fg_color = button_fg_color,
        button_hover_color = button_hover_color,
        button_text_color = button_text_color,
        entry_fg_color = entry_fg_color,
        entry_border_color = entry_border_color,
        entry_text_color = entry_text_color,
        password = Configuration_Dialog["password"])
    return Dialog

# ---------------------------------------------- ColorPicker ----------------------------------------------# 
def Get_Color_Picker(Frame: CTk|CTkFrame, Color_Manual_Frame_Var: CTkEntry) -> CTkColorPicker:
    def Change_Entry_Information(color: str) -> None:
        Color_Manual_Frame_Var.delete(first_index=0, last_index=8)
        Color_Manual_Frame_Var.insert(index=0, string=color)

    Configuration_ColorPicker = Configuration["ColorPicker"]

    fg_color = Define_Color(Color_json=Configuration_ColorPicker["fg_color"], Global_Color=Accent_Color)

    Color_Picker = CTkColorPicker(
        master = Frame,
        width = Configuration_ColorPicker["width"],
        initial_color = Configuration_ColorPicker["initial_color"],
        fg_color = fg_color,
        slider_border = Configuration_ColorPicker["slider_border"],
        corner_radius = Configuration_ColorPicker["corner_radius"],
        command = lambda color: Change_Entry_Information(color=color),
        orientation = Configuration_ColorPicker["orientation"])
    return Color_Picker

# ---------------------------------------------- CTkToolTip ----------------------------------------------# 
def Get_ToolTip(widget: any, message: str, ToolTip_Size) -> CTkToolTip:
    Configuration_ToolTip = Configuration["Tooltips"][f"{ToolTip_Size}"]

    border_color = Define_Color(Color_json=Configuration_ToolTip["border_color"], Global_Color=Accent_Color)

    ToolTip = CTkToolTip(
        widget = widget,
        message = message,
        delay = Configuration_ToolTip["delay"],
        follow = Configuration_ToolTip["follow"],
        x_offset = Configuration_ToolTip["x_offset"],
        y_offset = Configuration_ToolTip["y_offset"],
        bg_color = Configuration_ToolTip["bg_color"],
        corner_radius = Configuration_ToolTip["corner_radius"],
        border_width = Configuration_ToolTip["border_width"],
        border_color = border_color,
        alpha = Configuration_ToolTip["alpha"],
        padding = tuple(Configuration_ToolTip["padding"]))
    return ToolTip