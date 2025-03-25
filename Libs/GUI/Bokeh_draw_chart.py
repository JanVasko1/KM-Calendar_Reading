# Library Imports
from pandas import Timestamp, to_datetime
import numpy
import math
from PIL import ImageColor
from math import sin, cos, pi

from bokeh.models import LinearColorMapper, LogColorMapper, GlobalInlineStyleSheet, Arrow, NormalHead
from bokeh.transform import transform

def Hex_Tile_Coordinates(x_values):
    Coordinates_count = len(x_values)
    Square_ratio = [1, Coordinates_count]
    Pre_Numbers_dif = Coordinates_count - 1

    for First_Number in range(1, Coordinates_count):
        Second_Number = math.ceil(Coordinates_count / First_Number)
        Numbers_dif = abs(First_Number - Second_Number)

        if Pre_Numbers_dif < Numbers_dif:
            break

        if Numbers_dif < Pre_Numbers_dif:
            Square_ratio[0] = int(First_Number)
            Square_ratio[1] = int(Second_Number)

        Pre_Numbers_dif = Numbers_dif

    if Square_ratio[0] < Square_ratio[1]:
        Helper = Square_ratio[0]
        Square_ratio[0] = Square_ratio[1]
        Square_ratio[1] = Helper

    Coordinates_x = []
    Coordinates_y = []

    Increment = 0
    y = 0
    for x in range(0, Square_ratio[0]):
        if x %2 != 0:
            Increment += 1
        for y in range(0, Square_ratio[1]):
            Coordinates_x.append(-x)
            Coordinates_y.append(y + Increment)
        else:
            pass
            
    if (Square_ratio[0] * Square_ratio[1]) > Coordinates_count:
        Place_to_Del = (Square_ratio[0] * Square_ratio[1]) - Coordinates_count
        Coordinates_x = Coordinates_x[:-Place_to_Del]
        Coordinates_y = Coordinates_y[:-Place_to_Del]

    Coordinates_x = numpy.array(Coordinates_x)
    Coordinates_y = numpy.array(Coordinates_y)
    return Coordinates_x, Coordinates_y

def Bokeh_line_Interpolation(x_values, y_values, Interpolate, Format, multiplication = 15):
    if Interpolate == True:
        # Library Imports
        from scipy.interpolate import PchipInterpolator

        Interpolate_range = int(x_values.shape[0]) * multiplication
        if Format == "linear":
            x_vals = numpy.linspace(1, int(x_values.shape[0]), Interpolate_range)
            x_vals = x_vals + int(x_values.iloc[0]) - 1
            spl = PchipInterpolator(x = x_values, y = y_values, axis=1)
            y_vals = spl(x_vals)
            return x_vals, y_vals
        elif Format == "datetime":
            start = Timestamp(x_values.iloc[0])
            end = Timestamp(x_values.iloc[x_values.shape[0]-1])
            x_dates = numpy.linspace(start.value, end.value, Interpolate_range)
            spl = PchipInterpolator(x = x_values, y = y_values, axis=1)
            y_vals = spl(x_dates)
            x_dates = to_datetime(x_dates)           
            return x_dates, y_vals
        else:
            return x_values, y_values
    else:
        return x_values, y_values

def Get_Color_Palette(HEX_Color1, HEX_Color2, Palette_steps) -> list:
    def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    Color_Palette = []

    # Convert Colors HEX --> RGB
    RGB_Color1 = ImageColor.getrgb(str(HEX_Color1))
    RGB_Color2 = ImageColor.getrgb(str(HEX_Color2))

    R_Step = abs(RGB_Color1[0] - RGB_Color2[0])/Palette_steps
    G_Step = abs(RGB_Color1[1] - RGB_Color2[1])/Palette_steps
    B_Step = abs(RGB_Color1[2] - RGB_Color2[2])/Palette_steps

    R_color = RGB_Color1[0]
    G_color = RGB_Color1[1]
    B_color = RGB_Color1[2]

    # Create ColorPalette in HEX
    for Palette_step in range(0, Palette_steps):
        if Palette_step == 0:
            # Interval beginning
            Color_Palette.append(HEX_Color1)
        elif Palette_step == Palette_steps - 1:
            # Interval end
            Color_Palette.append(HEX_Color2)
        else:
            # Interval Middle
            # Red
            if RGB_Color1[0] < RGB_Color2[0]:
                R_color = R_color + R_Step
                R_Export = int(round(R_color))
            elif RGB_Color1[0] > RGB_Color2[0]: 
                R_color = R_color - R_Step
                R_Export = int(round(R_color))
            else:
                R_Export = int(RGB_Color1[0])

            # Green
            if RGB_Color1[1] < RGB_Color2[1]:
                G_color = G_color + G_Step
                G_Export = int(round(G_color))
            elif RGB_Color1[1] > RGB_Color2[1]: 
                G_color = G_color - G_Step
                G_Export = int(round(G_color))
            else:
                G_Export = int(RGB_Color1[1])

            # Blue
            if RGB_Color1[2] < RGB_Color2[2]:
                B_color = B_color + B_Step
                B_Export = int(round(B_color))
            elif RGB_Color1[2] > RGB_Color2[2]: 
                B_color = B_color - B_Step
                B_Export = int(round(B_color))
            else:
                B_Export = int(RGB_Color1[2])

            Color_Palette.append(rgb2hex(R_Export,G_Export,B_Export))

    return Color_Palette

def Color_Palette_Fix():
    Color_Palette = ["#FC181C", "#FC18A5", "#CB18FC", "#4218FC", "#1877FC", "#18FCF8", "#18FC6F", "#49FC18", "#D2FC18", "#FC9D18"]
    return Color_Palette

def Color_Mapper_Linear(Color_Palette, Max, Min):
    Color_Map = LinearColorMapper(palette=Color_Palette, high=Max, low=Min)
    return Color_Map
 
def Color_Mapper_Log(Color_Palette, Max, Min):
    Color_Map = LogColorMapper(palette=Color_Palette, high=Max, low=Min)
    return Color_Map

def Color_Palette_Transform(Color_Palette, Name):
    Color_Map = transform(field_name=Name, transform=Color_Palette)
    return Color_Map

def x_coordinates(radius, angle):
    x = radius * cos(angle)
    return x

def y_coordinates(radius, angle):
    y = radius * sin(angle)
    return y

def round_percentage(item):
    item = round(float(item),2)
    item = str(f"{item}%")
    return item

def text_Position(Start_rad, Stop_rad):
    text_angle = ((Stop_rad - Start_rad) / 2 ) + Start_rad
    return text_angle

def Text_angle(angle):
    angle2 = angle - (360 / pi)
    return angle2


def Chart_General_Setup(Chart, Chart_Area_Properties, Grid_properties, X_Axis_Properties, Y_Axis_Properties, Color_Bar_Properties, Legend_Properties, Tool_Properties, Range_Tool_Properties, ToolTip_list, ToolTip_list_count, ToolTip_Format, Color_Map, theme, Legend_n_cols = 1):
    #----------------------------------- General -----------------------------------#
    # Font Download 
    stylesheet = GlobalInlineStyleSheet(css="""@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap')""")
    Chart.stylesheets.append(stylesheet)

    # BackGround Colors
    Chart.background_fill_color = Chart_Area_Properties.iloc[0]["Background_Color"]
    Chart.background_fill_alpha = float(Chart_Area_Properties.iloc[0]["Background_opacity"])
    
    # Outline
    Chart.outline_line_color = Chart_Area_Properties.iloc[0]["Background_Color"]
    Chart.outline_line_alpha = float(Chart_Area_Properties.iloc[0]["Background_opacity"])
    #Chart.outline_line_width = 0

    # Borders
    Chart.border_fill_color = Chart_Area_Properties.iloc[0]["Background_Color"]
    Chart.border_fill_alpha = float(Chart_Area_Properties.iloc[0]["Background_opacity"])
    Chart.min_border_left = int(Chart_Area_Properties.iloc[0]["Border_left"])
    Chart.min_border_right = int(Chart_Area_Properties.iloc[0]["Border_right"])
    Chart.min_border_top = int(Chart_Area_Properties.iloc[0]["Border_top"])
    Chart.min_border_bottom = int(Chart_Area_Properties.iloc[0]["Border_bottom"])

    # Axis - X
    if X_Axis_Properties.iloc[0]["X_Axis_Visible"] == True:
        Chart.xaxis.visible = X_Axis_Properties.iloc[0]["X_Axis_Visible"]
        Chart.xaxis.major_label_orientation = X_Axis_Properties.iloc[0]["X_Axis_label_orient"]
        Chart.xaxis.major_label_text_color = X_Axis_Properties.iloc[0]["X_Axis_Font_Color"]
        Chart.xaxis.major_label_text_font = X_Axis_Properties.iloc[0]["X_Axis_Font"]
        Chart.xaxis.major_label_text_font_size = str(X_Axis_Properties.iloc[0]["X_Axis_Font_Size"])+"px"

        Chart.xaxis.axis_line_width = int(X_Axis_Properties.iloc[0]["X_Axis_Line_Thickness"])
        Chart.xaxis.axis_line_color = X_Axis_Properties.iloc[0]["X_Axis_Line_Color"]
        Chart.xaxis.axis_line_alpha = float(X_Axis_Properties.iloc[0]["X_Axis_Line_Opacity"])
        Chart.xaxis.major_tick_line_color  = X_Axis_Properties.iloc[0]["X_Axis_Major_Tic_Color"]
        Chart.xaxis.major_tick_line_alpha  = float(X_Axis_Properties.iloc[0]["X_Axis_Major_Tic_Opacity"])
        Chart.xaxis.minor_tick_line_color = X_Axis_Properties.iloc[0]["X_Axis_Minor_Tic_Color"]
        Chart.xaxis.minor_tick_line_alpha = float(X_Axis_Properties.iloc[0]["X_Axis_Minor_Tic_Opacity"])
    else:
        Chart.xaxis.visible = False

    # Axis - Y
    if Y_Axis_Properties.iloc[0]["Y_Axis_Visible"] == True:
        Chart.yaxis.visible = Y_Axis_Properties.iloc[0]["Y_Axis_Visible"]
        Chart.yaxis.major_label_orientation = Y_Axis_Properties.iloc[0]["Y_Axis_label_orient"]
        Chart.yaxis.major_label_text_color = Y_Axis_Properties.iloc[0]["Y_Axis_Font_Color"]
        Chart.yaxis.major_label_text_font = Y_Axis_Properties.iloc[0]["Y_Axis_Font"]
        Chart.yaxis.major_label_text_font_size = str(Y_Axis_Properties.iloc[0]["Y_Axis_Font_Size"])+"px"

        Chart.yaxis.axis_line_width = int(Y_Axis_Properties.iloc[0]["Y_Axis_Line_Thickness"])
        Chart.yaxis.axis_line_color = Y_Axis_Properties.iloc[0]["Y_Axis_Line_Color"]
        Chart.yaxis.axis_line_alpha = float(Y_Axis_Properties.iloc[0]["Y_Axis_Line_Opacity"])
        Chart.yaxis.major_tick_line_color = Y_Axis_Properties.iloc[0]["Y_Axis_Major_Tic_Color"]
        Chart.yaxis.major_tick_line_alpha = float(Y_Axis_Properties.iloc[0]["Y_Axis_Major_Tic_Opacity"])
        Chart.yaxis.minor_tick_line_color = Y_Axis_Properties.iloc[0]["Y_Axis_Minor_Tic_Color"]
        Chart.yaxis.minor_tick_line_alpha = float(Y_Axis_Properties.iloc[0]["Y_Axis_Minor_Tic_Opacity"])
    else:
        Chart.yaxis.visible = False

    # Grid
    if Grid_properties.iloc[0]["X_Grid_Line"] == True:
        Chart.xgrid.visible = Grid_properties.iloc[0]["X_Grid_Line"]
        Chart.xgrid.grid_line_color = Grid_properties.iloc[0]["X_Grid_Line_Color"]
        Chart.xgrid.grid_line_width = int(Grid_properties.iloc[0]["X_Grid_Line_Thickness"])
        if Grid_properties.iloc[0]["X_Grid_Line_Style"] == "dash":
            Chart.xgrid.grid_line_dash = Grid_properties.iloc[0]["X_Grid_Line_Dash_Ration"]
        Chart.xgrid.grid_line_alpha = float(Grid_properties.iloc[0]["X_Grid_Line_Color_Opacity"])
    else:
        Chart.xgrid.visible = False

    if Grid_properties.iloc[0]["Y_Grid_Line"] == True:
        Chart.ygrid.visible = Grid_properties.iloc[0]["Y_Grid_Line"]
        Chart.ygrid.grid_line_color = Grid_properties.iloc[0]["Y_Grid_Line_Color"]
        Chart.ygrid.grid_line_width = int(Grid_properties.iloc[0]["Y_Grid_Line_Thickness"])
        if Grid_properties.iloc[0]["Y_Grid_Line_Style"] == "dash":
            Chart.ygrid.grid_line_dash = Grid_properties.iloc[0]["Y_Grid_Line_Dash_Ration"]
        Chart.ygrid.grid_line_alpha = float(Grid_properties.iloc[0]["Y_Grid_Line_Color_Opacity"])
    else:
        Chart.ygrid.visible = False
    
    #----------------------------------- ToolBar -----------------------------------#
    # General
    Chart.toolbar.autohide = Tool_Properties.iloc[0]["Tool_AutoHide"]
    Chart.toolbar.logo = None
    Active_Inspect_list = []
    Chart.toolbar.tools = []
    # CrosshairTool
    if Tool_Properties.iloc[0]["CrosshairTool_Visible"] == True:
        Cross_Line_Color = Tool_Properties.iloc[0]["CrosshairTool_Color"]
        Cross_Line_Thickness = int(Tool_Properties.iloc[0]["CrosshairTool_Thickness"])
        # Library Imports
        from bokeh.models import CrosshairTool, Span

        # Individual
        if Tool_Properties.iloc[0]["CrosshairTool_Mode"] == "vline":
            Span_height = Span(dimension="height", line_dash="dashed", line_width=Cross_Line_Thickness, line_color=Cross_Line_Color)
            Crosshair_Tool = CrosshairTool(overlay=Span_height)
        elif Tool_Properties.iloc[0]["CrosshairTool_Mode"] == "hline":
            Span_width = Span(dimension="width", line_dash="dashed", line_width=Cross_Line_Thickness, line_color=Cross_Line_Color)
            Crosshair_Tool = CrosshairTool(overlay=Span_width)
        elif Tool_Properties.iloc[0]["CrosshairTool_Mode"] == "both":
            Span_width = Span(dimension="width", line_dash="dashed", line_width=Cross_Line_Thickness, line_color=Cross_Line_Color)
            Span_height = Span(dimension="height", line_dash="dashed", line_width=Cross_Line_Thickness, line_color=Cross_Line_Color)
            Crosshair_Tool = CrosshairTool(overlay=[Span_width, Span_height])
        else:
            Crosshair_Tool = CrosshairTool()
            
        Chart.add_tools(Crosshair_Tool)
        Active_Inspect_list.append(Crosshair_Tool)
    else:
        pass

    # WheelZoomTool
    if Tool_Properties.iloc[0]["WheelZoomTool_Visible"] == True:
        # Library Imports
        from bokeh.models import WheelZoomTool

        Wheel_Zoom_Tool = WheelZoomTool()
        Chart.add_tools(Wheel_Zoom_Tool)
        Chart.toolbar.active_scroll = Wheel_Zoom_Tool
    else:
        pass

    # BoxSelectTool
    if Tool_Properties.iloc[0]["BoxSelectTool_Visible"] == True:
        # Library Imports
        from bokeh.models import BoxSelectTool

        Box_Select_Tool = BoxSelectTool()
        Box_Select_Tool.dimensions = Tool_Properties.iloc[0]["BoxSelectTool_Mode"]
        Chart.add_tools(Box_Select_Tool)
        Chart.toolbar.active_drag = Box_Select_Tool
    else:
        pass

    # HoverTool
    if Tool_Properties.iloc[0]["HoverTool_Visible"] == True:
        # Library Imports
        from bokeh.models import HoverTool

        for i in range(0, ToolTip_list_count):
            Hover_Tool = HoverTool()
            Hover_Tool.tooltips = ToolTip_list[i]
            Hover_Tool.muted_policy = Tool_Properties.iloc[0]["HoverTool_mute_policy"]
            Hover_Tool.formatters = ToolTip_Format
            if Tool_Properties.iloc[0]["HoverTool_mode"] != "":
                Hover_Tool.mode = Tool_Properties.iloc[0]["HoverTool_mode"]
            else:
                pass
            Chart.add_tools(Hover_Tool)
            Active_Inspect_list.append(Hover_Tool)
    else:
        pass

    # TapTool
    if Tool_Properties.iloc[0]["TapTool_Visible"] == True:
        # Library Imports
        from bokeh.models import TapTool

        Tap_Tool = TapTool()
        Chart.add_tools(Tap_Tool)
    else:
        pass

    # PanTool
    if Tool_Properties.iloc[0]["PanTool_Visible"] == True:
        # Library Imports
        from bokeh.models import PanTool

        Pan_Tool = PanTool()
        Pan_Tool.dimensions = Tool_Properties.iloc[0]["PanTool_Dimension"]       # width, height, both
        Chart.add_tools(Pan_Tool)
        Chart.toolbar.active_drag = Pan_Tool
    else:
        pass

    # ResetTool
    if Tool_Properties.iloc[0]["ResetTool_Visible"] == True:
        # Library Imports
        from bokeh.models import ResetTool

        Reset_Tool = ResetTool()
        Chart.add_tools(Reset_Tool)
    else:
        pass

    # FullscreenTool
    if Tool_Properties.iloc[0]["FullscreenTool_Visible"] == True:
        # Library Imports
        from bokeh.models import FullscreenTool

        Full_screen_Tool = FullscreenTool()
        Chart.add_tools(Full_screen_Tool)
    else:
        pass

    # ZoomInTool
    if Tool_Properties.iloc[0]["ZoomInTool_Visible"] == True:
        # Library Imports
        from bokeh.models import ZoomInTool

        Zoom_In_Tool = ZoomInTool()
        Chart.add_tools(Zoom_In_Tool)
    else:
        pass

    # ZoomOutTool
    if Tool_Properties.iloc[0]["ZoomOutTool_Visible"] == True:
        # Library Imports
        from bokeh.models import ZoomOutTool

        Zoom_Out_Tool = ZoomOutTool()
        Chart.add_tools(Zoom_Out_Tool)
    else:
        pass

    # BoxZoomTool
    if Tool_Properties.iloc[0]["BoxZoomTool_Visible"] == True:
        # Library Imports
        from bokeh.models import BoxZoomTool

        Box_Zoom_Tool = BoxZoomTool()
        Box_Zoom_Tool.dimensions = Tool_Properties.iloc[0]["BoxZoomTool_Mode"]
        Chart.add_tools(Box_Zoom_Tool)
        #Chart.toolbar.active_drag = Box_Zoom_Tool
    else:
        pass

    # PolyDrawTool
    if Tool_Properties.iloc[0]["PolyDrawTool_Visible"] == True:
        # Library Imports
        from bokeh.models import PolyDrawTool

        PolyDraw_Tool = PolyDrawTool()
        Chart.add_tools(PolyDraw_Tool)
    else:
        pass

    # RangeTool
    if Range_Tool_Properties.iloc[0]["Range_Tool_Visible"] == True:
        # Library Imports
        from bokeh.models import RangeTool

        Range_Tool = RangeTool()
        Chart.add_tools(Range_Tool)
    else:
        pass

    # HelpTool
    if Tool_Properties.iloc[0]["HelpTool_Visible"] == True:
        # Library Imports
        from bokeh.models import HelpTool

        Help_Tool = HelpTool()
        Help_Tool.description = "Learn more about Chart content and gain knowledge."
        Chart.add_tools(Help_Tool)
    else:
        pass

    # Default Tools
    Chart.toolbar.active_inspect = Active_Inspect_list

    #----------------------------------- Color Bar -----------------------------------#
    # Color Bar
    if Color_Bar_Properties.iloc[0]["Color_Bar_Visible"] == True:
        # Library Imports
        from bokeh.models import ColorBar

        color_bar = ColorBar(color_mapper=Color_Map)
        color_bar.background_fill_color = Chart_Area_Properties.iloc[0]["Background_Color"]
        color_bar.background_fill_alpha = 0
        color_bar.major_tick_line_color = Color_Bar_Properties.iloc[0]["Color_Bar_Tick_Line_Color"]
        color_bar.major_label_text_font = Color_Bar_Properties.iloc[0]["Color_Bar_Font"]
        color_bar.major_label_text_font_size = str(Color_Bar_Properties.iloc[0]["Color_Bar_Font_Size"])+"px"
        color_bar.major_label_text_color = Color_Bar_Properties.iloc[0]["Color_Bar_Font_Color"]
        Chart.add_layout(color_bar, Color_Bar_Properties.iloc[0]["Color_Bar_Position"])
    else:
        pass

    #----------------------------------- Legend -----------------------------------#
    # Legend
    if  Legend_Properties.iloc[0]["Legend_Visible"] == True:
        # Library Imports
        from bokeh.models import Legend

        Chart_Legend = Legend()
        Chart_Legend.ncols = Legend_n_cols

        # Position
        if Legend_Properties.iloc[0]["Legend_Layer_Position"] == "Outher":
            Chart.add_layout(Chart_Legend, Legend_Properties.iloc[0]["Legend_Position"])   # "right", "left", "above", "below", "center"
        elif Legend_Properties.iloc[0]["Legend_Layer_Position"] == "Inner":
            Chart.add_layout(Chart_Legend, Legend_Properties.iloc[0]["Legend_Position"])   #"top_left", "top_center", "top_right", "center_right", "bottom_right", "bottom_center", "bottom_left", "center_left", "center"
        else:
            Chart.add_layout(Chart_Legend, Legend_Properties.iloc[0]["Legend_Position"])  

        # Background
        Chart_Legend.background_fill_color = Chart_Area_Properties.iloc[0]["Background_Color"]
        Chart_Legend.background_fill_alpha = 0

        # Border
        Chart_Legend.border_line_width = 0
        Chart_Legend.border_line_alpha = 0
        Chart_Legend.border_line_color = Chart_Area_Properties.iloc[0]["Background_Color"]

        # Inactive
        Chart_Legend.inactive_fill_color = Chart_Area_Properties.iloc[0]["Background_Color"]
        Chart_Legend.inactive_fill_alpha = 0.7

        Chart_Legend.click_policy = Legend_Properties.iloc[0]["Legend_Click_Policy"]
        Chart_Legend.location = Legend_Properties.iloc[0]["Legend_Position"]
        
        # Label Texts
        Chart_Legend.label_text_font = Legend_Properties.iloc[0]["Legend_Font"]
        Chart_Legend.label_text_font_size = str(Legend_Properties.iloc[0]["Legend_Font_Size"])+"px"
        Chart_Legend.label_text_color = Legend_Properties.iloc[0]["Legend_Font_Color"] 

        # Title
        if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
            Chart_Legend.title = ""  # Title Text is set on each Chart itself
            Chart_Legend.title_text_font = Legend_Properties.iloc[0]["Legend_Title_Font"]
            Chart_Legend.title_text_font_size = str(Legend_Properties.iloc[0]["Legend_Title_Font_Size"])+"px"
            Chart_Legend.title_text_color = Legend_Properties.iloc[0]["Legend_Title_Font_Color"]
            Chart_Legend.title_text_font_style = Legend_Properties.iloc[0]["Legend_Title_Font_Style"]
        else:
            pass
    else:
        pass

    return Chart

def Text_Area_Setup(Chart, Text_Area_Properties):
    Chart.xaxis.visible = False
    Chart.yaxis.visible = False
    Chart.xgrid.visible = False
    Chart.ygrid.visible = False

    # BackGround Colors
    Chart.background_fill_color = Text_Area_Properties.iloc[0]["Background_Color"]
    Chart.background_fill_alpha = float(Text_Area_Properties.iloc[0]["Background_opacity"])

    # Outline
    Chart.outline_line_color = Text_Area_Properties.iloc[0]["Background_Color"]
    Chart.outline_line_alpha = float(Text_Area_Properties.iloc[0]["Background_opacity"])

    # Borders
    Chart.border_fill_color = Text_Area_Properties.iloc[0]["Background_Color"]
    Chart.border_fill_alpha = float(Text_Area_Properties.iloc[0]["Background_opacity"])
    Chart.min_border_left = int(Text_Area_Properties.iloc[0]["Border_left"])
    Chart.min_border_right = int(Text_Area_Properties.iloc[0]["Border_right"])
    Chart.min_border_top = int(Text_Area_Properties.iloc[0]["Border_top"])
    Chart.min_border_bottom = int(Text_Area_Properties.iloc[0]["Border_bottom"])
    return Chart

def Draw_Arrow_Up(x_start, color, head_alpha):
    Arrow_Up_Head = NormalHead(size=12, fill_color=color, fill_alpha = float(head_alpha), line_width = 0, line_alpha = 1, line_color = "black")
    Arrow_up = Arrow(end=Arrow_Up_Head, x_start=x_start, y_start=2, x_end=x_start, y_end=8, line_color=color, line_width=5, line_alpha = 1)
    return Arrow_up

def Draw_Arrow_Down(x_start, color, head_alpha):
    Arrow_Down_Head = NormalHead(size=12, fill_color=color, fill_alpha = float(head_alpha), line_width = 0, line_alpha = 1, line_color = "black")
    Arrow_Down = Arrow(end=Arrow_Down_Head, x_start=x_start, y_start=8, x_end=x_start, y_end=2, line_color=color, line_width=5, line_alpha = 1)
    return Arrow_Down