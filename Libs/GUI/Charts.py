# Import Libraries
from pandas import DataFrame, to_datetime, read_csv
from warnings import filterwarnings

from datetime import datetime, timedelta

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Bokeh_draw_chart as Bokeh_draw_chart

from bokeh.plotting import save, figure
from bokeh.layouts import layout
from bokeh.models import DataRange1d, ColumnDataSource, Span, Label, Block, HoverTool

from CTkMessagebox import CTkMessagebox

filterwarnings("ignore")
# ---------------------------------------------------------- Local Functions---------------------------------------------------------- #
def Chart_update_html(Chart: str, color: str, opacity: float):
    with open(file=f"{Chart}", mode="r") as file:
        lines = file.readlines()
    file.close()

    Lines_new = []
    Header_Style_search_text = "html, body {"
    Body_Search_text = "<body>"
    Background_color_text = f"""        background-color: {color};\n"""
    Drag_view_text = f"""    <div class='pywebview-drag-region' style="color: {color}; opacity: {opacity};">.</div>\n"""

    Find_Header_style = -1
    Find_Body = -1
    for line in lines:
        Lines_new.append(line)
        if Find_Header_style == -1:
            Find_Header_style = line.find(Header_Style_search_text)
            if Find_Header_style > 0:
                # Insert text to as next line
                Lines_new.append(Background_color_text)
            else:
                pass
        else:
            pass

        if Find_Body == -1:
            Find_Body = line.find(Body_Search_text)
            if Find_Body > 0:
                # Insert text to as next line
                Lines_new.append(Drag_view_text)
            else:
                pass
        else:
            pass

    # Save again
    with open(file=f"{Chart}", mode="w") as new_file:
        new_file.writelines(Lines_new)
    new_file.close()


# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Gen_Chart_Project_Activity(Settings: dict, Calculation_source: str, Category: str, theme: str, Events: DataFrame, Report_Period_End: datetime|None, File_Sub_Path: str) -> None:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["General"]["Formats"]["Date"]
    X_Series_Column = "Date"  

    if theme == "Light" or theme == "Dark":
        Figure_height=370
        Figure_sizing_mode = "stretch_width"
        Chart_Settings = Defaults_Lists.Load_Figures(Theme=theme)
    else:
        CTkMessagebox(title="Error", message=f"Theme not supported as program cannot load Figure settings.", icon="cancel", fade_in_duration=1)
        
    # General information about Game
    Chart_Area_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Chart_Area_Properties"], columns=["Column_Color_Single", "Column_Color_Fill_1", "Column_Color_Fill_2", "Colors_Palette_Range", "Line_Column_Color", "Line_Thickness", "Active_Area_size", "Active_Area_indented_percent", "Total_Area_size", "Interpolation", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom"], index=[0])
    Chart_Area_Properties.Name = "Chart_Area_Properties"
    Grid_properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Grid_properties"], columns=["X_Grid_Line", "X_Grid_Line_Style", "X_Grid_Line_Dash_Ration", "X_Grid_Line_Thickness", "X_Grid_Line_Color", "X_Grid_Line_Color_Opacity", "Y_Grid_Line", "Y_Grid_Line_Style", "Y_Grid_Line_Dash_Ration", "Y_Grid_Line_Thickness", "Y_Grid_Line_Color", "Y_Grid_Line_Color_Opacity"], index=[0])
    Grid_properties.Name = "Grid_properties"
    X_Axis_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["X_Axis_Properties"], columns=["X_Axis_Visible", "X_Axis_label_orient", "X_Axis_Line_Style", "X_Axis_Line_Thickness", "X_Axis_Line_Color", "X_Axis_Line_Opacity", "X_Axis_Font", "X_Axis_Font_Size", "X_Axis_Font_Color", "X_Axis_Major_Tic_Color", "X_Axis_Major_Tic_Opacity", "X_Axis_Minor_Tic_Color", "X_Axis_Minor_Tic_Opacity"], index=[0])
    X_Axis_Properties.Name = "X_Axis_Properties"
    Y_Axis_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Y_Axis_Properties"], columns=["Y_Axis_Visible", "Y_Axis_label_orient", "Y_Axis_Line_Style", "Y_Axis_Line_Thickness", "Y_Axis_Line_Color", "Y_Axis_Line_Opacity", "Y_Axis_Font", "Y_Axis_Font_Size", "Y_Axis_Font_Color", "Y_Axis_Major_Tic_Color", "Y_Axis_Major_Tic_Opacity", "Y_Axis_Minor_Tic_Color", "Y_Axis_Minor_Tic_Opacity"], index=[0])
    Y_Axis_Properties.Name = "Y_Axis_Properties"
    Color_Bar_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Color_Bar_Properties"], columns=["Color_Bar_Visible", "Color_Bar_Position", "Color_Bar_Tick_Line_Color", "Color_Bar_Font", "Color_Bar_Font_Size", "Color_Bar_Font_Color"], index=[0])
    Color_Bar_Properties.Name = "Color_Bar_Properties"
    Legend_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Legend_Properties"], columns=["Legend_Visible", "Legend_Click_Policy", "Legend_Layer_Position", "Legend_Position", "Legend_Font", "Legend_Font_Size", "Legend_Font_Color", "Legend_Title_Visible", "Legend_Title_Font", "Legend_Title_Font_Size", "Legend_Title_Font_Color", "Legend_Title_Font_Style"], index=[0])
    Legend_Properties.Name = "Legend_Properties"
    Tool_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Tool_Properties"], columns=["Tool_AutoHide", "CrosshairTool_Visible", "CrosshairTool_Color", "CrosshairTool_Mode", "CrosshairTool_Thickness", "WheelZoomTool_Visible", "BoxSelectTool_Visible", "BoxSelectTool_Mode", "HoverTool_Visible", "HoverTool_mode", "HoverTool_mute_policy", "TapTool_Visible", "PanTool_Visible", "PanTool_Dimension", "ResetTool_Visible", "FullscreenTool_Visible", "ZoomInTool_Visible", "ZoomOutTool_Visible", "BoxZoomTool_Visible", "BoxZoomTool_Mode", "PolyDrawTool_Visible", "HelpTool_Visible"], index=[0])
    Tool_Properties.Name = "Tool_Properties"
    Text_Area_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Text_Area_Properties"], columns=["Text_Area_Visible", "Area_width", "Area_height", "x_Range", "y_Range", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom", "Major_Text_fill_alpha", "Major_Text_Color", "Major_Text_Alpha", "Major_Text_Font", "Major_Text_Font_Size", "Major_Text_Font_Style", "Major_Text_Baseline", "Minor_Text_fill_alpha", "Minor_Text_Color", "Minor_Text_Alpha", "Minor_Text_Font", "Minor_Text_Font_Size", "Minor_Text_Font_Style", "Minor_Text_Baseline", "Arrow_Up_Color", "Arrow_Up_Head_Alpha", "Arrow_Down_Color", "Arrow_Down_Head_Alpha"], index=[0])
    Text_Area_Properties.Name = "Text_Area_Properties"
    Range_Tool_Properties = DataFrame(Chart_Settings["Bar_Vertical_Stacked_xTime_Charts"]["Range_Tool_Properties"], columns=["Range_Tool_Visible", "Range_Tool_Height_Percentage", "Range_Tool_Active_Def_Area", "Range_Tool_Active_Def_Color", "Range_Tool_Active_Def_Color_Opacity"], index=[0])
    Range_Tool_Properties.Name = "Range_Tool_Properties"


    # ------------------------- Main Functions -------------------------#
    # Process Data
    Events_GR = Events.loc[:, ["Date", f"{Category}", "Duration_H"]]

    Value_df = Events_GR.groupby(["Date", f"{Category}"]).sum()
    Value_df.sort_index(ascending=True, inplace=True)
    Value_df.reset_index(inplace=True)
    Colum_list = Value_df[f"{Category}"].tolist()
    Colum_list = list(set(Colum_list))
    Colum_list.sort()

    Value_df = Value_df.pivot(index="Date", columns=f"{Category}", values="Duration_H")
    Value_df.fillna(value=0, inplace=True)
    Value_df.reset_index(inplace=True)
    
    Active_Area_size = int(Chart_Area_Properties.iloc[0]["Active_Area_size"])
    Active_Area_indented = round((int(Active_Area_size) / 100) * int(Chart_Area_Properties.iloc[0]["Active_Area_indented_percent"]),0)

    Value_df["Date"] = to_datetime(Value_df[X_Series_Column], format=Date_Format)
    Value_df = Defaults_Lists.PD_Column_to_DateTime(PD_DataFrame=Value_df, Column="Date", Covert_Format=Date_Format)
    Max_range = max(Value_df["Date"]) + timedelta(days=Active_Area_indented)

    # ToolTip
    # TODO --> Tooltip to be only in one containing all pf them, then transfer it to the helpers
    ToolTip = [
        ("Date", "@Date{%F}"), 
        (f"{Category}", "$name"), 
        ("Hours", "@$name")]
    ToolTip_list = [ToolTip]
    ToolTip_list_count = len(ToolTip_list)
    
    ToolTip_Format = {
        "@Date": "datetime",
        "@$name": "numeral"}

    # x_Axis range
    Max_range_len = Value_df.shape[0]
    Min_range = min(Value_df["Date"])
    Min_range_bound = Min_range - timedelta(days=1)

    if Max_range_len < Active_Area_size:
        pass
    elif Max_range_len >= Active_Area_size:
        Min_Range_Len = Max_range_len - Active_Area_size
        Min_range = Value_df.iloc[Min_Range_Len]["Date"]
    else:
        CTkMessagebox(title="Error", message=f"Calculation of X Axis Range finish in the else statement, should not be.", icon="cancel", fade_in_duration=1)

    x_range_set = DataRange1d(start=Min_range, end=Max_range, bounds=(Min_range_bound, Max_range))

    # Color Palette  
    Color_numbers = int(len(Colum_list))
    Colors_Palette = Bokeh_draw_chart.Get_Color_Palette(HEX_Color1=Chart_Area_Properties.iloc[0]["Column_Color_Fill_1"], HEX_Color2=Chart_Area_Properties.iloc[0]["Column_Color_Fill_2"], Palette_steps=Color_numbers)
    Color_Map = Bokeh_draw_chart.Color_Mapper_Linear(Color_Palette=Colors_Palette, Max=2, Min=1)

    # Draw + save chart
    Chart = figure(sizing_mode = Figure_sizing_mode, height=Figure_height, toolbar_location="below", x_range = x_range_set)
    Chart = Bokeh_draw_chart.Chart_General_Setup(Chart=Chart, Chart_Area_Properties=Chart_Area_Properties, Grid_properties=Grid_properties, X_Axis_Properties=X_Axis_Properties, Y_Axis_Properties=Y_Axis_Properties, Color_Bar_Properties=Color_Bar_Properties, Legend_Properties=Legend_Properties, Tool_Properties=Tool_Properties, Range_Tool_Properties=Range_Tool_Properties, ToolTip_list=ToolTip_list, ToolTip_list_count=ToolTip_list_count, ToolTip_Format=ToolTip_Format, Color_Map=Color_Map, Legend_n_cols = 1, theme=theme)

    # Legend Title text
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Chart.legend.title = f"{Category}"
    else:
        pass

    # ---------------------------- Background Rectangle ---------------------------- #
    # Y max coordinate for rectangle
    Value_df["Line_Sum"] = Value_df.iloc[:,1:].sum(axis=1)
    Y_Max_Coordinates = max(Value_df["Line_Sum"])
    Value_df.drop(labels=["Line_Sum"], axis=1, inplace=True)

    # Forecast availability
    Value_df_Max_Date = max(Value_df["Date"])
    Today_dt = datetime.now()
    if Today_dt < Value_df_Max_Date:
        Crate_Forecast = True
    else:
        Crate_Forecast = False

    # Registered Area
    if Calculation_source == "Current":
        try:
            Events_Registered_df = read_csv(Defaults_Lists.Absolute_path(relative_path=f"Operational\\Downloads\\Events_Registered.csv"), sep=";")
            if Events_Registered_df.empty:
                pass
            else:
                Event_Registered_Min_Data = min(Events_Registered_df["Date"])
                Event_Registered_Min_Data_dt = datetime.strptime(Event_Registered_Min_Data, Date_Format)
                Event_Registered_Min_Data_ts = (datetime.timestamp(Event_Registered_Min_Data_dt)) * 1000
                Event_Registered_Max_Date = max(Events_Registered_df["Date"])
                Event_Registered_Max_Data_dt = datetime.strptime(Event_Registered_Max_Date, Date_Format)
                Event_Registered_Max_Data_ts = (datetime.timestamp(Event_Registered_Max_Data_dt))  * 1000
                Registered_Block_width = Event_Registered_Max_Data_ts - Event_Registered_Min_Data_ts + 50000000

                glyph = Block(x=Event_Registered_Min_Data_ts - 25000000, y=0, width=Registered_Block_width, height=Y_Max_Coordinates, fill_color="#25c887", fill_alpha=0.1, line_width=0)
                Chart.add_glyph(glyph)

                fixed_label = Label(x=Event_Registered_Min_Data_ts, y=Y_Max_Coordinates, text="Already registered", text_font_size="10pt", text_color="#25c887")
                Chart.add_layout(fixed_label)
        except:
            pass
    else:
        pass
    # ForeCast
    if (Report_Period_End == None) or (Crate_Forecast == False):
        pass
    else:
        Today_str = datetime.strftime(Today_dt, Date_Format)
        Today_dt = datetime.strptime(Today_str, Date_Format)
        Today_ts = (datetime.timestamp(Today_dt)) * 1000
        Report_Period_End_ts = (datetime.timestamp(Report_Period_End))  * 1000
        Forecast_Block_width = Report_Period_End_ts - Today_ts

        glyph = Block(x=Today_ts + 50000000, y=0, width=Forecast_Block_width, height=Y_Max_Coordinates, fill_color="#ef8135", fill_alpha=0.1, line_width=0)
        Chart.add_glyph(glyph)

        fixed_label = Label(x=Today_ts + 50000000, y=Y_Max_Coordinates, text="Forecast period", text_font_size="10pt", text_color="#ef8135")
        Chart.add_layout(fixed_label)

    # Chart
    DataSource = ColumnDataSource(data = Value_df)
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Glyph_vbar_stack = Chart.vbar_stack(stackers=Colum_list, x="Date", width=50000000, line_color=None, color=Colors_Palette, source=DataSource, legend_label=Colum_list, border_radius = 6, muted_alpha=0.2, hover_color=Chart_Area_Properties.iloc[0]["Column_Color_Single"])
    else:
        Glyph_vbar_stack = Chart.vbar_stack(stackers=Colum_list, x="Date", width=50000000, line_color=None, color=Colors_Palette, source=DataSource, border_radius = 6, muted_alpha=0.2, hover_color=Chart_Area_Properties.iloc[0]["Column_Color_Single"])

    # ToolTip update Renderers --> update
    Glyph_vbar_stack_list = []
    for Glyph in Glyph_vbar_stack:
        Glyph_vbar_stack_list.append(Glyph)
    Chart.hover.renderers = Glyph_vbar_stack_list
    
    Chart_Layout = layout(children=[Chart],sizing_mode="stretch_width")

    # Split Value DF if production "Dummy = False" or just examples on common web "Dummy = True"
    if (theme == "Light") or (theme == "Dark"):
        save(obj=Chart_Layout, filename=Defaults_Lists.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_{Category}_{theme}.html"), title=f"{Category}")
        Chart_update_html(Chart=Defaults_Lists.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_{Category}_{theme}.html"), color=Chart_Area_Properties.iloc[0]["Background_Color"], opacity=Chart_Area_Properties.iloc[0]["Background_opacity"])
    else:
        CTkMessagebox(title="Error", message=f"Cannot save as them is not supported.", icon="cancel", fade_in_duration=1)
    
def Gen_Chart_Calendar_Utilization(Settings: dict, theme: str, Utilization_Calendar_df: DataFrame, File_Sub_Path: str):
    Date_Format = Settings["General"]["Formats"]["Date"]

    # Variable Defaults
    X_Series_Column = "Date"  
    X_Series_Format = "datetime"

    # General information about Game
    if theme == "Light" or theme == "Dark":
        Figure_height=370
        Figure_sizing_mode = "stretch_width"
        Chart_Settings = Defaults_Lists.Load_Figures(Theme=theme)
    else:
        CTkMessagebox(title="Error", message=f"Theme not supported as program cannot load Figure settings.", icon="cancel", fade_in_duration=1)
    
    Chart_Area_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Chart_Area_Properties"], columns=["Line_Color_start_Range", "Line_Color_end_Range", "Line_Thickness", "Under_Line_Area_Opacity", "Under_Line_Area_Fill_Color", "Tick_Symbol", "Tick_Size", "Active_Area_size", "Active_Area_indented_percent", "Total_Area_size", "Interpolation", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom"], index=[0])
    Chart_Area_Properties.Name = "Chart_Area_Properties"
    Grid_properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Grid_properties"], columns=["X_Grid_Line", "X_Grid_Line_Style", "X_Grid_Line_Dash_Ration", "X_Grid_Line_Thickness", "X_Grid_Line_Color", "X_Grid_Line_Color_Opacity", "Y_Grid_Line", "Y_Grid_Line_Style", "Y_Grid_Line_Dash_Ration", "Y_Grid_Line_Thickness", "Y_Grid_Line_Color", "Y_Grid_Line_Color_Opacity"], index=[0])
    Grid_properties.Name = "Grid_properties"
    X_Axis_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["X_Axis_Properties"], columns=["X_Axis_Visible", "X_Axis_label_orient", "X_Axis_Line_Style", "X_Axis_Line_Thickness", "X_Axis_Line_Color", "X_Axis_Line_Opacity", "X_Axis_Font", "X_Axis_Font_Size", "X_Axis_Font_Color", "X_Axis_Major_Tic_Color", "X_Axis_Major_Tic_Opacity", "X_Axis_Minor_Tic_Color", "X_Axis_Minor_Tic_Opacity"], index=[0])
    X_Axis_Properties.Name = "X_Axis_Properties"
    Y_Axis_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Y_Axis_Properties"], columns=["Y_Axis_Visible", "Y_Axis_label_orient", "Y_Axis_Line_Style", "Y_Axis_Line_Thickness", "Y_Axis_Line_Color", "Y_Axis_Line_Opacity", "Y_Axis_Font", "Y_Axis_Font_Size", "Y_Axis_Font_Color", "Y_Axis_Major_Tic_Color", "Y_Axis_Major_Tic_Opacity", "Y_Axis_Minor_Tic_Color", "Y_Axis_Minor_Tic_Opacity"], index=[0])
    Y_Axis_Properties.Name = "Y_Axis_Properties"
    Color_Bar_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Color_Bar_Properties"], columns=["Color_Bar_Visible", "Color_Bar_Position", "Color_Bar_Tick_Line_Color", "Color_Bar_Font", "Color_Bar_Font_Size", "Color_Bar_Font_Color"], index=[0])
    Color_Bar_Properties.Name = "Color_Bar_Properties"
    Legend_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Legend_Properties"], columns=["Legend_Visible", "Legend_Click_Policy", "Legend_Layer_Position", "Legend_Position", "Legend_Font", "Legend_Font_Size", "Legend_Font_Color", "Legend_Title_Visible", "Legend_Title_Font", "Legend_Title_Font_Size", "Legend_Title_Font_Color", "Legend_Title_Font_Style"], index=[0])
    Legend_Properties.Name = "Legend_Properties"
    Range_Tool_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Range_Tool_Properties"], columns=["Range_Tool_Visible", "Range_Tool_Height_Percentage", "Range_Tool_Active_Def_Area", "Range_Tool_Active_Def_Color", "Range_Tool_Active_Def_Color_Opacity"], index=[0])
    Range_Tool_Properties.Name = "Range_Tool_Properties"
    Text_Area_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Text_Area_Properties"], columns=["Text_Area_Visible", "Area_width", "Area_height", "x_Range", "y_Range", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom", "Major_Text_fill_alpha", "Major_Text_Color", "Major_Text_Alpha", "Major_Text_Font", "Major_Text_Font_Size", "Major_Text_Font_Style", "Major_Text_Baseline", "Minor_Text_fill_alpha", "Minor_Text_Color", "Minor_Text_Alpha", "Minor_Text_Font", "Minor_Text_Font_Size", "Minor_Text_Font_Style", "Minor_Text_Baseline", "Arrow_Up_Color", "Arrow_Up_Head_Alpha", "Arrow_Down_Color", "Arrow_Down_Head_Alpha"], index=[0])
    Text_Area_Properties.Name = "Text_Area_Properties"
    Tool_Properties = DataFrame(Chart_Settings["Basic_Multi_Line_Charts"]["Tool_Properties"], columns=["Tool_AutoHide", "CrosshairTool_Visible", "CrosshairTool_Color", "CrosshairTool_Mode", "CrosshairTool_Thickness", "WheelZoomTool_Visible", "BoxSelectTool_Visible", "BoxSelectTool_Mode", "HoverTool_Visible", "HoverTool_mode", "HoverTool_mute_policy", "TapTool_Visible", "PanTool_Visible", "PanTool_Dimension", "ResetTool_Visible", "FullscreenTool_Visible", "ZoomInTool_Visible", "ZoomOutTool_Visible", "BoxZoomTool_Visible", "BoxZoomTool_Mode", "PolyDrawTool_Visible", "HelpTool_Visible"], index=[0])
    Tool_Properties.Name = "Tool_Properties"

    # Process Data
    Utilization_Calendar_df.reset_index(inplace=True)
    Value_df = Utilization_Calendar_df.loc[:, ["index", "KM_Cumulative_Utilization", "Reported_Cumulative_Time"]]
    Value_df.rename(columns={"index": "Date"}, inplace=True)

    Value_df.drop_duplicates(inplace=True)
    Value_df.sort_values(by=["Date"], ascending=True, inplace=True)

    Active_Area_indented = round((int(Chart_Area_Properties.iloc[0]["Active_Area_size"]) / 100) * int(Chart_Area_Properties.iloc[0]["Active_Area_indented_percent"]),0)

    Value_df["Draw_Date2"] = to_datetime(Value_df[X_Series_Column], format=Date_Format)
    Value_df.drop(labels=["Date"], axis=1,inplace=True)
    Value_df.rename({"Draw_Date2": "Date"}, axis=1, inplace=True)
    Max_range = max(Value_df[f"{X_Series_Column}"]) + timedelta(days=Active_Area_indented)

    # ToolTip
    ToolTip_KM = [
        ("Date", "@Date{%F}"), 
        ("KM cumulated util.", "@KM_Cumulative_Utilization{0.00}"),
        ("My report cum. time", "@Reported_Cumulative_Time{0.00}")]

    ToolTip_list = [ToolTip_KM]
    ToolTip_list_count = len(ToolTip_list)
    
    ToolTip_Format = {
        "@Date": "datetime",
        "@KM_Cumulative_Utilization": "numeral",
        "@Reported_Cumulative_Time": "numeral"}

    # x_Axis range
    Max_range_len = Value_df.shape[0]
    Active_Area_size = int(Chart_Area_Properties.iloc[0]["Active_Area_size"])
    Min_range = min(Value_df[X_Series_Column])
    Min_range_bound = Min_range

    if Max_range_len <= Active_Area_size:
        pass
    elif Max_range_len > Active_Area_size:
        Min_Range_Len = Max_range_len - Active_Area_size
        Min_range = Value_df.iloc[Min_Range_Len][X_Series_Column]
    else:
        CTkMessagebox(title="Error", message=f"Calculation of X Axis Range finish in the else statement, should not be.", icon="cancel", fade_in_duration=1)
    
    x_range_set = DataRange1d(start=Min_range, end=Max_range, bounds=(Min_range_bound, Max_range))

    # Color Palette    
    Colors_Palette1 = Bokeh_draw_chart.Get_Color_Palette(HEX_Color1=Chart_Area_Properties.iloc[0]["Line_Color_start_Range"], HEX_Color2=Chart_Area_Properties.iloc[0]["Line_Color_end_Range"], Palette_steps=int(2))
    Color_Map = Bokeh_draw_chart.Color_Mapper_Linear(Color_Palette=Colors_Palette1, Max=2, Min=1)
    Colors_Palette = Chart_Area_Properties.iloc[0]["Under_Line_Area_Fill_Color"]

    # Draw + save chart
    Chart = figure(sizing_mode = Figure_sizing_mode, height=Figure_height, toolbar_location="below", x_axis_type=X_Series_Format, x_range = x_range_set)
    Chart = Bokeh_draw_chart.Chart_General_Setup(Chart=Chart, Chart_Area_Properties=Chart_Area_Properties, Grid_properties=Grid_properties, X_Axis_Properties=X_Axis_Properties, Y_Axis_Properties=Y_Axis_Properties, Color_Bar_Properties=Color_Bar_Properties, Legend_Properties=Legend_Properties, Tool_Properties=Tool_Properties, Range_Tool_Properties=Range_Tool_Properties, ToolTip_list=ToolTip_list, ToolTip_list_count=ToolTip_list_count, ToolTip_Format=ToolTip_Format, Color_Map=Color_Map, Legend_n_cols = 1, theme=theme)

    # Legend Title text
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Chart.legend.title = "Utilization vs reported hours"
    else:
        pass

    # Today vertical-Line
    Today = datetime.now().strftime(Date_Format)
    Today = datetime.strptime(Today, Date_Format)
    Today_line = Span(location=Today, dimension='height', line_color="#00A9FF", line_width=1, line_dash="dashed", line_alpha=0.8)
    Chart.add_layout(Today_line)

    fixed_label = Label(x=Today + timedelta(hours=3), y=0, text="Last Process Date", text_font_size="10pt", text_color="#00A9FF")
    Chart.add_layout(fixed_label)

    # Min-Max Values
    x_values_KM, y_values_KM = Bokeh_draw_chart.Bokeh_line_Interpolation(x_values = Value_df[X_Series_Column], y_values = Value_df["KM_Cumulative_Utilization"], Interpolate = Chart_Area_Properties.iloc[0]["Interpolation"], Format = X_Series_Format)
    x_values_Reported, y_values_Reported = Bokeh_draw_chart.Bokeh_line_Interpolation(x_values = Value_df[X_Series_Column], y_values = Value_df["Reported_Cumulative_Time"], Interpolate = Chart_Area_Properties.iloc[0]["Interpolation"], Format = X_Series_Format)
    Chart.varea(x=x_values_KM, y1=y_values_KM, y2=y_values_Reported, fill_color = Colors_Palette, alpha= float(Chart_Area_Properties.iloc[0]["Under_Line_Area_Opacity"]))
    
    global GS_Diff_Line_Reported, GS_Diff_Line_KM, GS_Diff_Cycles_REported, GS_Diff_Cycles_KM
    if Legend_Properties.iloc[0]["Legend_Visible"] == True:
        GS_Diff_Line_KM = Chart.line(x=x_values_KM, y=y_values_KM, line_width= int(Chart_Area_Properties.iloc[0]["Line_Thickness"]), line_color = Colors_Palette1[1], line_join = "round", legend_label="KM Utilization")
        GS_Diff_Line_Reported = Chart.line(x=x_values_Reported, y=y_values_Reported, line_width= int(Chart_Area_Properties.iloc[0]["Line_Thickness"]), line_color = Colors_Palette1[0], line_join = "round", legend_label="Reported Time")
    else:
        GS_Diff_Line_KM = Chart.line(x=x_values_KM, y=y_values_KM, line_width= int(Chart_Area_Properties.iloc[0]["Line_Thickness"]), line_color = Colors_Palette1[1], line_join = "round")
        GS_Diff_Line_Reported = Chart.line(x=x_values_Reported, y=y_values_Reported, line_width= int(Chart_Area_Properties.iloc[0]["Line_Thickness"]), line_color = Colors_Palette1[0], line_join = "round")
    
    DataSource = ColumnDataSource(data = Value_df)
    if Chart_Area_Properties.iloc[0]["Tick_Symbol"] == "cycle":
        if Legend_Properties.iloc[0]["Legend_Visible"] == True:
            GS_Diff_Cycles_KM = Chart.circle(source=DataSource, x=X_Series_Column, y="KM_Cumulative_Utilization", size=int(Chart_Area_Properties.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Properties.iloc[0]["Background_Color"], line_color=Colors_Palette1[1], hover_fill_color=Colors_Palette1[1], legend_label="KM Utilization")
            GS_Diff_Cycles_REported = Chart.circle(source=DataSource, x=X_Series_Column, y="Reported_Cumulative_Time", size=int(Chart_Area_Properties.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Properties.iloc[0]["Background_Color"], line_color=Colors_Palette1[0], hover_fill_color=Colors_Palette1[0], legend_label="Reported Time")
        else:
            GS_Diff_Cycles_KM = Chart.circle(source=DataSource, x=X_Series_Column, y="KM_Cumulative_Utilization", size=int(Chart_Area_Properties.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Properties.iloc[0]["Background_Color"], line_color=Colors_Palette1[1], hover_fill_color=Colors_Palette1[1])
            GS_Diff_Cycles_REported = Chart.circle(source=DataSource, x=X_Series_Column, y="Reported_Cumulative_Time", size=int(Chart_Area_Properties.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Properties.iloc[0]["Background_Color"], line_color=Colors_Palette1[0], hover_fill_color=Colors_Palette1[0])
        Chart.hover[0].renderers = [GS_Diff_Cycles_REported]

    Chart_Layout = layout(children=[Chart],sizing_mode='stretch_width')

    # Split Value DF if production "Dummy = False" or just examples on common web "Dummy = True"
    if (theme == "Light") or (theme == "Dark"):
        save(obj=Chart_Layout, filename=Defaults_Lists.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Utilization_{theme}.html"), title=f"Report Rage utilization compare")
        Chart_update_html(Chart=Defaults_Lists.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Utilization_{theme}.html"), color=Chart_Area_Properties.iloc[0]["Background_Color"], opacity=Chart_Area_Properties.iloc[0]["Background_opacity"])
    else:
        CTkMessagebox(title="Error", message=f"Cannot save as them is not supported.", icon="cancel", fade_in_duration=1)