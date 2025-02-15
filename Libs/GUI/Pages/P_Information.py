# Import Libraries
from  markdown import markdown

from customtkinter import CTk, CTkFrame
from tkhtmlview import HTMLLabel

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_Information(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    Work_Area_Detail_Background = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"]["Triple_size"]["fg_color"]
    
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]

    # ------------------------- Main Functions -------------------------#
    Frame_Information_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Information_Work_Detail_Area.grid_propagate(flag=False)

    # Get Theme --> because of background color
    Current_Theme = Defaults_Lists.Get_Current_Theme() 

    if Current_Theme == "Dark":
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]
    elif Current_Theme == "Light":
        HTML_Background_Color = Work_Area_Detail_Background[0]
        HTML_Font_Color = Work_Area_Detail_Font[0]
    elif Current_Theme == "System":
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]
    else:
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]

    # ------------------------- Info Text Area -------------------------#
    # Description
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Information_Work_Detail_Area, Frame_Size="Triple_size")

    with open("Libs\\GUI\\Information.md", "r", encoding="UTF-8") as file:
        html_markdown=markdown(text=file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"{html_markdown}", background=HTML_Background_Color, font="Roboto", fg=HTML_Font_Color)
    Information_html.configure(height=700)

    # Build look of Widget
    Frame_Information_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)
