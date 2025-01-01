# Import Libraries
import pandas
from pandas import DataFrame
import warnings
from datetime import timedelta

import Libs.Defaults_Lists as Defaults_Lists

import Libs.GUI.Bokeh_draw_chart as Bokeh_draw_chart
from bokeh.plotting import save, figure
from bokeh.layouts import layout
from bokeh.io import export_svgs, export_svg, export_png
from bokeh.models import DataRange1d, ColumnDataSource

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_Format = Settings["General"]["Formats"]["Date"]


# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Gen_Chart_Project_Activity(Category: str, theme: str, Events: DataFrame) -> None:
    warnings.filterwarnings("ignore")

    # Variable Defaults
    X_Series_Column = "Start_Date"  

    # General information about Game
    if theme == "Light" or theme == "Dark":
        Figure_height=370
        Figure_sizing_mode = "stretch_width"
        Chart_Settings = Defaults_Lists.Load_Figures(Theme=theme)
    else:
        CTkMessagebox(title="Error", message=f"Theme not supported as program cannot load Figure settings.", icon="cancel", fade_in_duration=1)
        raise ValueError
        
    Chart_Area_Propertie = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Chart_Area_Propertie"], columns=["Column_Color_Single", "Column_Color_Fill_1", "Column_Color_Fill_2", "Colors_pallete_Range", "Line_Column_Color", "Line_Thiknes", "Active_Area_size", "Active_Area_indented_percent", "Total_Area_size", "Interpolation", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom"], index=[0])
    Chart_Area_Propertie.Name = "Chart_Area_Propertie"
    Grid_properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Grid_properties"], columns=["X_Grid_Line", "X_Grid_Line_Style", "X_Grid_Line_Dash_Ration", "X_Grid_Line_Thiknes", "X_Grid_Line_Color", "X_Grid_Line_Color_Opacity", "Y_Grid_Line", "Y_Grid_Line_Style", "Y_Grid_Line_Dash_Ration", "Y_Grid_Line_Thiknes", "Y_Grid_Line_Color", "Y_Grid_Line_Color_Opacity"], index=[0])
    Grid_properties.Name = "Grid_properties"
    X_Axis_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["X_Axis_Properties"], columns=["X_Axis_Visible", "X_Axis_label_orient", "X_Axis_Line_Style", "X_Axis_Line_Thiknes", "X_Axis_Line_Color", "X_Axis_Line_Opacity", "X_Axis_Font", "X_Axis_Font_Size", "X_Axis_Font_Color", "X_Axis_Major_Tic_Color", "X_Axis_Major_Tic_Opacity", "X_Axis_Minor_Tic_Color", "X_Axis_Minor_Tic_Opacity"], index=[0])
    X_Axis_Properties.Name = "X_Axis_Properties"
    Y_Axis_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Y_Axis_Properties"], columns=["Y_Axis_Visible", "Y_Axis_label_orient", "Y_Axis_Line_Style", "Y_Axis_Line_Thiknes", "Y_Axis_Line_Color", "Y_Axis_Line_Opacity", "Y_Axis_Font", "Y_Axis_Font_Size", "Y_Axis_Font_Color", "Y_Axis_Major_Tic_Color", "Y_Axis_Major_Tic_Opacity", "Y_Axis_Minor_Tic_Color", "Y_Axis_Minor_Tic_Opacity"], index=[0])
    Y_Axis_Properties.Name = "Y_Axis_Properties"
    Color_Bar_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Color_Bar_Properties"], columns=["Color_Bar_Visible", "Color_Bar_Possition", "Color_Bar_Tick_Line_Color", "Color_Bar_Font", "Color_Bar_Font_Size", "Color_Bar_Font_Color"], index=[0])
    Color_Bar_Properties.Name = "Color_Bar_Properties"
    Legend_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Legend_Properties"], columns=["Legend_Visible", "Legend_Click_Policy", "Legend_Layer_Possition", "Legend_Possition", "Legend_Font", "Legend_Font_Size", "Legend_Font_Color", "Legend_Title_Visible", "Legend_Title_Font", "Legend_Title_Font_Size", "Legend_Title_Font_Color", "Legend_Title_Font_Style"], index=[0])
    Legend_Properties.Name = "Legend_Properties"
    Tool_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Tool_Properties"], columns=["Tool_AutoHide", "CrosshairTool_Visible", "CrosshairTool_Color", "CrosshairTool_Mode", "CrosshairTool_Thiknes", "WheelZoomTool_Visible", "BoxSelectTool_Visible", "BoxSelectTool_Mode", "HoverTool_Visible", "HoverTool_mode", "HoverTool_mute_policy", "TapTool_Visible", "PanTool_Visible", "PanTool_Dimension", "ResetTool_Visible", "FullscreenTool_Visible", "ZoomInTool_Visible", "ZoomOutTool_Visbile", "BoxZoomTool_Visbile", "BoxZoomTool_Mode", "PolyDrawTool_Visible", "HelpTool_Visible"], index=[0])
    Tool_Properties.Name = "Tool_Properties"
    Text_Area_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Text_Area_Properties"], columns=["Text_Area_Visible", "Area_width", "Area_height", "x_Range", "y_Range", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom", "Major_Text_fill_alpha", "Major_Text_Color", "Major_Text_Alpha", "Major_Text_Font", "Major_Text_Font_Size", "Major_Text_Font_Style", "Major_Text_Baseline", "Minor_Text_fill_alpha", "Minor_Text_Color", "Minor_Text_Alpha", "Minor_Text_Font", "Minor_Text_Font_Size", "Minor_Text_Font_Style", "Minor_Text_Baseline", "Arrow_Up_Color", "Arrow_Up_Head_Alpha", "Arrow_Down_Color", "Arrow_Down_Head_Alpha"], index=[0])
    Text_Area_Properties.Name = "Text_Area_Properties"
    Range_Tool_Properties = pandas.DataFrame(Chart_Settings["Bar_Vertical_Stucked_xTime_Charts"]["Range_Tool_Properties"], columns=["Range_Tool_Visible", "Range_Tool_Height_Percentage", "Range_Tool_Active_Def_Area", "Range_Tool_Active_Def_Color", "Range_Tool_Active_Def_Color_Opacity"], index=[0])
    Range_Tool_Properties.Name = "Range_Tool_Properties"

    # Process Data
    Events_GR = Events.loc[:, ["Start_Date", f"{Category}", "Duration_H"]]
    Value_df = Events_GR.groupby(["Start_Date", f"{Category}"]).sum()
    Value_df.sort_index(ascending=True, inplace=True)
    Value_df.reset_index(inplace=True)
    Colum_list = Value_df[f"{Category}"].tolist()
    Colum_list = list(set(Colum_list))
    Colum_list.sort()

    Value_df = Value_df.pivot(index="Start_Date", columns=f"{Category}", values="Duration_H")
    Value_df.fillna(value=0, inplace=True)
    Value_df.reset_index(inplace=True)
    
    Active_Area_size = int(Chart_Area_Propertie.iloc[0]["Active_Area_size"])
    Active_Area_indented = round((int(Active_Area_size) / 100) * int(Chart_Area_Propertie.iloc[0]["Active_Area_indented_percent"]),0)

    Value_df["Date"] = pandas.to_datetime(Value_df[X_Series_Column], format=Date_Format)
    Value_df.drop(labels=[f"{X_Series_Column}"], axis=1,inplace=True)
    Max_range = max(Value_df["Date"]) + timedelta(days=Active_Area_indented)

    # ToolTip
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
    Min_range_bound = Min_range

    if Max_range_len < Active_Area_size:
        pass
    elif Max_range_len > Active_Area_size:
        Min_Range_Len = Max_range_len - Active_Area_size
        Min_range = Value_df.iloc[Min_Range_Len]["Date"] - + timedelta(days=1)
    else:
        CTkMessagebox(title="Error", message=f"Calculation of X Axis Range finish in the else statement, should not be.", icon="cancel", fade_in_duration=1)
        raise ValueError

    x_range_set = DataRange1d(start=Min_range, end=Max_range, bounds=(Min_range_bound, Max_range))

    # Color pallete  
    Color_numbers = int(len(Colum_list))
    Colors_pallete = Bokeh_draw_chart.Get_Color_pallete(HEX_Color1=Chart_Area_Propertie.iloc[0]["Column_Color_Fill_1"], HEX_Color2=Chart_Area_Propertie.iloc[0]["Column_Color_Fill_2"], Pallete_steps=Color_numbers)
    Color_Map = Bokeh_draw_chart.Color_Mapper_Linear(Color_Pallete=Colors_pallete, Max=2, Min=1)

    # Draw + save chart
    Chart = figure(sizing_mode = Figure_sizing_mode, height=Figure_height, toolbar_location="below", x_range = x_range_set)
    Chart = Bokeh_draw_chart.Chart_General_Setup(Chart=Chart, Chart_Area_Propertie=Chart_Area_Propertie, Grid_properties=Grid_properties, X_Axis_Properties=X_Axis_Properties, Y_Axis_Properties=Y_Axis_Properties, Color_Bar_Properties=Color_Bar_Properties, Legend_Properties=Legend_Properties, Tool_Properties=Tool_Properties, Range_Tool_Properties=Range_Tool_Properties, ToolTip_list=ToolTip_list, ToolTip_list_count=ToolTip_list_count, ToolTip_Format=ToolTip_Format, Color_Map=Color_Map, Legend_n_cols = 1, theme=theme)

    # Legend Title text
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Chart.legend.title = f"{Category}"
    else:
        pass

    # Chart
    DataSource = ColumnDataSource(data = Value_df)
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Chart.vbar_stack(stackers=Colum_list, x="Date", width=50000000, color=Colors_pallete, source=DataSource, legend_label=Colum_list, border_radius = 6, muted_alpha=0.2, hover_color=Chart_Area_Propertie.iloc[0]["Column_Color_Single"])
    else:
        Chart.vbar_stack(stackers=Colum_list, x="Date", width=50000000, color=Colors_pallete, source=DataSource, border_radius = 6, muted_alpha=0.2, hover_color=Chart_Area_Propertie.iloc[0]["Column_Color_Single"])

    Chart_Layout = layout(children=[Chart],sizing_mode="stretch_width")

    # Split Value DF if production "Dummy = False" or just examples on common web "Dummy = True"
    if (theme == "Light") or (theme == "Dark"):
        save(obj=Chart_Layout, filename=f"Operational\\DashBoard_{Category}_{theme}.html", title=f"{Category}")
        #! Dodělat --> musí se doinstalovat webdriver: https://docs.bokeh.org/en/2.4.3/docs/user_guide/export.html#exporting-svg-images
        #export_png(obj=Chart_Layout, filename=f"Operational\\DashBoard_{Category}_{theme}.png", width=1643 , height=370)
        #export_svg(obj=Chart_Layout, filename=f"Operational\\DashBoard_{Category}_{theme}.svg", width=1643 , height=370)
        #export_svgs(obj=Chart_Layout,filename=f"Operational\\DashBoard_{Category}_{theme}2.svg", width=1643 , height=370)
    else:
        CTkMessagebox(title="Error", message=f"Cannot save as them is not supported.", icon="cancel", fade_in_duration=1)
        raise ValueError


def Gen_Chart_Calendar_Utilization(theme: str, Utilization_Calendar_df: DataFrame):
    warnings.filterwarnings("ignore")

    # Variable Defaults
    X_Series_Column = "Date"  
    X_Seris_Format = "datetime"

    # General information about Game
    if theme == "Light" or theme == "Dark":
        Figure_height=370
        Figure_sizing_mode = "stretch_width"
        Chart_Settings = Defaults_Lists.Load_Figures(Theme=theme)
    else:
        CTkMessagebox(title="Error", message=f"Theme not supported as program cannot load Figure settings.", icon="cancel", fade_in_duration=1)
        raise ValueError
    
    Chart_Area_Propertie = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Chart_Area_Propertie"], columns=["Line_Color_start_Range", "Line_Color_end_Range", "Line_Thiknes", "Under_Line_Area_Opacity", "Under_Line_Area_Fill_Color", "Tick_Simbol", "Tick_Size", "Active_Area_size", "Active_Area_indented_percent", "Total_Area_size", "Interpolation", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom"], index=[0])
    Chart_Area_Propertie.Name = "Chart_Area_Propertie"
    Grid_properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Grid_properties"], columns=["X_Grid_Line", "X_Grid_Line_Style", "X_Grid_Line_Dash_Ration", "X_Grid_Line_Thiknes", "X_Grid_Line_Color", "X_Grid_Line_Color_Opacity", "Y_Grid_Line", "Y_Grid_Line_Style", "Y_Grid_Line_Dash_Ration", "Y_Grid_Line_Thiknes", "Y_Grid_Line_Color", "Y_Grid_Line_Color_Opacity"], index=[0])
    Grid_properties.Name = "Grid_properties"
    X_Axis_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["X_Axis_Properties"], columns=["X_Axis_Visible", "X_Axis_label_orient", "X_Axis_Line_Style", "X_Axis_Line_Thiknes", "X_Axis_Line_Color", "X_Axis_Line_Opacity", "X_Axis_Font", "X_Axis_Font_Size", "X_Axis_Font_Color", "X_Axis_Major_Tic_Color", "X_Axis_Major_Tic_Opacity", "X_Axis_Minor_Tic_Color", "X_Axis_Minor_Tic_Opacity"], index=[0])
    X_Axis_Properties.Name = "X_Axis_Properties"
    Y_Axis_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Y_Axis_Properties"], columns=["Y_Axis_Visible", "Y_Axis_label_orient", "Y_Axis_Line_Style", "Y_Axis_Line_Thiknes", "Y_Axis_Line_Color", "Y_Axis_Line_Opacity", "Y_Axis_Font", "Y_Axis_Font_Size", "Y_Axis_Font_Color", "Y_Axis_Major_Tic_Color", "Y_Axis_Major_Tic_Opacity", "Y_Axis_Minor_Tic_Color", "Y_Axis_Minor_Tic_Opacity"], index=[0])
    Y_Axis_Properties.Name = "Y_Axis_Properties"
    Color_Bar_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Color_Bar_Properties"], columns=["Color_Bar_Visible", "Color_Bar_Possition", "Color_Bar_Tick_Line_Color", "Color_Bar_Font", "Color_Bar_Font_Size", "Color_Bar_Font_Color"], index=[0])
    Color_Bar_Properties.Name = "Color_Bar_Properties"
    Legend_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Legend_Properties"], columns=["Legend_Visible", "Legend_Click_Policy", "Legend_Layer_Possition", "Legend_Possition", "Legend_Font", "Legend_Font_Size", "Legend_Font_Color", "Legend_Title_Visible", "Legend_Title_Font", "Legend_Title_Font_Size", "Legend_Title_Font_Color", "Legend_Title_Font_Style"], index=[0])
    Legend_Properties.Name = "Legend_Properties"
    Range_Tool_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Range_Tool_Properties"], columns=["Range_Tool_Visible", "Range_Tool_Height_Percentage", "Range_Tool_Active_Def_Area", "Range_Tool_Active_Def_Color", "Range_Tool_Active_Def_Color_Opacity"], index=[0])
    Range_Tool_Properties.Name = "Range_Tool_Properties"
    Text_Area_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Text_Area_Properties"], columns=["Text_Area_Visible", "Area_width", "Area_height", "x_Range", "y_Range", "Background_Color", "Background_opacity", "Border_left", "Border_right", "Border_top", "Border_bottom", "Major_Text_fill_alpha", "Major_Text_Color", "Major_Text_Alpha", "Major_Text_Font", "Major_Text_Font_Size", "Major_Text_Font_Style", "Major_Text_Baseline", "Minor_Text_fill_alpha", "Minor_Text_Color", "Minor_Text_Alpha", "Minor_Text_Font", "Minor_Text_Font_Size", "Minor_Text_Font_Style", "Minor_Text_Baseline", "Arrow_Up_Color", "Arrow_Up_Head_Alpha", "Arrow_Down_Color", "Arrow_Down_Head_Alpha"], index=[0])
    Text_Area_Properties.Name = "Text_Area_Properties"
    Tool_Properties = pandas.DataFrame(Chart_Settings["Basic_Multy_Line_Charts"]["Tool_Properties"], columns=["Tool_AutoHide", "CrosshairTool_Visible", "CrosshairTool_Color", "CrosshairTool_Mode", "CrosshairTool_Thiknes", "WheelZoomTool_Visible", "BoxSelectTool_Visible", "BoxSelectTool_Mode", "HoverTool_Visible", "HoverTool_mode", "HoverTool_mute_policy", "TapTool_Visible", "PanTool_Visible", "PanTool_Dimension", "ResetTool_Visible", "FullscreenTool_Visible", "ZoomInTool_Visible", "ZoomOutTool_Visbile", "BoxZoomTool_Visbile", "BoxZoomTool_Mode", "PolyDrawTool_Visible", "HelpTool_Visible"], index=[0])
    Tool_Properties.Name = "Tool_Properties"

    # Process Data
    Utilization_Calendar_df.reset_index(inplace=True)
    Utilization_Calendar_df.rename(columns={"index": "Date"}, inplace=True)
    Value_df = Utilization_Calendar_df.loc[:, ["Date", "KM_Cumulative_Utilization", "Reported_Cumulative_Time"]]

    Value_df.drop_duplicates(inplace=True)
    Value_df.sort_values(by=["Date"], ascending=True, inplace=True)

    Active_Area_indented = round((int(Chart_Area_Propertie.iloc[0]["Active_Area_size"]) / 100) * int(Chart_Area_Propertie.iloc[0]["Active_Area_indented_percent"]),0)

    Value_df["Draw_Date2"] = pandas.to_datetime(Value_df[X_Series_Column], format=Date_Format)
    Value_df.drop(labels=["Date"], axis=1,inplace=True)
    Value_df.rename({"Draw_Date2": "Date"}, axis=1, inplace=True)
    Max_range = max(Value_df[f"{X_Series_Column}"]) + timedelta(days=Active_Area_indented)

    # ToolTip
    ToolTip_KM = [
        ("Date", "@Date{%F}"), 
        ("Value", "@KM_Cumulative_Utilization{0.00}")]

    ToolTip_Reported = [
        ("Date", "@Date{%F}"), 
        ("Value", "@Reported_Cumulative_Time{0.00}")]

    ToolTip_list = [ToolTip_KM, ToolTip_Reported]
    ToolTip_list_count = len(ToolTip_list)
    
    ToolTip_Format = {
        "@Date": "datetime",
        "@KM_Cumulative_Utilization": "numeral",
        "@Reported_Cumulative_Time": "numeral"}

    # x_Axis range
    Max_range_len = Value_df.shape[0]
    Active_Area_size = int(Chart_Area_Propertie.iloc[0]["Active_Area_size"])
    Min_range = min(Value_df[X_Series_Column])
    Min_range_bound = Min_range

    if Max_range_len < Active_Area_size:
        pass
    elif Max_range_len > Active_Area_size:
        Min_Range_Len = Max_range_len - Active_Area_size
        Min_range = Value_df.iloc[Min_Range_Len][X_Series_Column]
    else:
        CTkMessagebox(title="Error", message=f"Calculation of X Axis Range finish in the else statement, should not be.", icon="cancel", fade_in_duration=1)
        raise ValueError
    
    x_range_set = DataRange1d(start=Min_range, end=Max_range, bounds=(Min_range_bound, Max_range))

    # Color pallete    
    Colors_pallete1 = Bokeh_draw_chart.Get_Color_pallete(HEX_Color1=Chart_Area_Propertie.iloc[0]["Line_Color_start_Range"], HEX_Color2=Chart_Area_Propertie.iloc[0]["Line_Color_end_Range"], Pallete_steps=int(2))
    Color_Map = Bokeh_draw_chart.Color_Mapper_Linear(Color_Pallete=Colors_pallete1, Max=2, Min=1)
    Colors_pallete = Chart_Area_Propertie.iloc[0]["Under_Line_Area_Fill_Color"]

    # Draw + save chart
    Chart = figure(sizing_mode = Figure_sizing_mode, height=Figure_height, toolbar_location="below", x_axis_type=X_Seris_Format, x_range = x_range_set)
    Chart = Bokeh_draw_chart.Chart_General_Setup(Chart=Chart, Chart_Area_Propertie=Chart_Area_Propertie, Grid_properties=Grid_properties, X_Axis_Properties=X_Axis_Properties, Y_Axis_Properties=Y_Axis_Properties, Color_Bar_Properties=Color_Bar_Properties, Legend_Properties=Legend_Properties, Tool_Properties=Tool_Properties, Range_Tool_Properties=Range_Tool_Properties, ToolTip_list=ToolTip_list, ToolTip_list_count=ToolTip_list_count, ToolTip_Format=ToolTip_Format, Color_Map=Color_Map, Legend_n_cols = 1, theme=theme)

    # Legend Title text
    if Legend_Properties.iloc[0]["Legend_Title_Visible"] == True:
        Chart.legend.title = "Utilization vs reported hours"
    else:
        pass

    # Min-Max Values
    x_values_KM, y_values_KM = Bokeh_draw_chart.Bokeh_line_Interpolation(x_values = Value_df[X_Series_Column], y_values = Value_df["KM_Cumulative_Utilization"], Interpolate = Chart_Area_Propertie.iloc[0]["Interpolation"], Format = X_Seris_Format)
    x_values_Reported, y_values_Reported = Bokeh_draw_chart.Bokeh_line_Interpolation(x_values = Value_df[X_Series_Column], y_values = Value_df["Reported_Cumulative_Time"], Interpolate = Chart_Area_Propertie.iloc[0]["Interpolation"], Format = X_Seris_Format)
    Chart.varea(x=x_values_KM, y1=y_values_KM, y2=y_values_Reported, fill_color = Colors_pallete, alpha= float(Chart_Area_Propertie.iloc[0]["Under_Line_Area_Opacity"]))
    
    global GS_Diff_Line_Reported, GS_Diff_Line_KM, GS_Diff_Cycles_REported, GS_Diff_Cycles_KM
    if Legend_Properties.iloc[0]["Legend_Visible"] == True:
        GS_Diff_Line_KM = Chart.line(x=x_values_KM, y=y_values_KM, line_width= int(Chart_Area_Propertie.iloc[0]["Line_Thiknes"]), line_color = Colors_pallete1[1], line_join = "round", legend_label="KM Utilization")
        GS_Diff_Line_Reported = Chart.line(x=x_values_Reported, y=y_values_Reported, line_width= int(Chart_Area_Propertie.iloc[0]["Line_Thiknes"]), line_color = Colors_pallete1[0], line_join = "round", legend_label="Reported Time")
    else:
        GS_Diff_Line_KM = Chart.line(x=x_values_KM, y=y_values_KM, line_width= int(Chart_Area_Propertie.iloc[0]["Line_Thiknes"]), line_color = Colors_pallete1[1], line_join = "round")
        GS_Diff_Line_Reported = Chart.line(x=x_values_Reported, y=y_values_Reported, line_width= int(Chart_Area_Propertie.iloc[0]["Line_Thiknes"]), line_color = Colors_pallete1[0], line_join = "round")
    
    DataSource = ColumnDataSource(data = Value_df)
    if Chart_Area_Propertie.iloc[0]["Tick_Simbol"] == "cycle":
        if Legend_Properties.iloc[0]["Legend_Visible"] == True:
            GS_Diff_Cycles_KM = Chart.circle(source=DataSource, x=X_Series_Column, y="KM_Cumulative_Utilization", size=int(Chart_Area_Propertie.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Propertie.iloc[0]["Background_Color"], line_color=Colors_pallete1[1], hover_fill_color=Colors_pallete1[1], legend_label="KM Utilization")
            GS_Diff_Cycles_REported = Chart.circle(source=DataSource, x=X_Series_Column, y="Reported_Cumulative_Time", size=int(Chart_Area_Propertie.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Propertie.iloc[0]["Background_Color"], line_color=Colors_pallete1[0], hover_fill_color=Colors_pallete1[0], legend_label="Reported Time")
        else:
            GS_Diff_Cycles_KM = Chart.circle(source=DataSource, x=X_Series_Column, y="KM_Cumulative_Utilization", size=int(Chart_Area_Propertie.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Propertie.iloc[0]["Background_Color"], line_color=Colors_pallete1[1], hover_fill_color=Colors_pallete1[1])
            GS_Diff_Cycles_REported = Chart.circle(source=DataSource, x=X_Series_Column, y="Reported_Cumulative_Time", size=int(Chart_Area_Propertie.iloc[0]["Tick_Size"]), fill_color = Chart_Area_Propertie.iloc[0]["Background_Color"], line_color=Colors_pallete1[0], hover_fill_color=Colors_pallete1[0])
        Chart.hover[0].renderers = [GS_Diff_Cycles_REported]
        Chart.hover[1].renderers = [GS_Diff_Cycles_KM]

    Chart_Layout = layout(children=[Chart],sizing_mode='stretch_width')

    # Split Value DF if production "Dummy = False" or just examples on common web "Dummy = True"
    if (theme == "Light") or (theme == "Dark"):
        save(obj=Chart_Layout, filename=f"Operational\\DashBoard_Utilization_{theme}.html", title=f"Report Rage utilization compare")
        #! Dodělat --> musí se doinstalovat webdriver: https://docs.bokeh.org/en/2.4.3/docs/user_guide/export.html#exporting-svg-images
        #export_png(obj=Chart_Layout, filename=f"Operational\\DashBoard_{Category}_{theme}.png", width=1643 , height=370)
        #export_svg(obj=Chart_Layout, filename=f"Operational\\DashBoard_{Category}_{theme}.svg", width=1643 , height=370)
        #export_svgs(obj=Chart_Layout,filename=f"Operational\\DashBoard_{Category}_{theme}2.svg", width=1643 , height=370)
    else:
        CTkMessagebox(title="Error", message=f"Cannot save as them is not supported.", icon="cancel", fade_in_duration=1)
        raise ValueError