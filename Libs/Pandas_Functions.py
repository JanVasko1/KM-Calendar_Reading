# Import Libraries
from pandas import DataFrame, Series, to_datetime, concat

# --------------------------------------------- Pandas --------------------------------------------- #
def PD_Column_to_DateTime(PD_DataFrame: DataFrame, Column: str, Covert_Format: str) -> DataFrame:
    PD_DataFrame[Column] = to_datetime(arg=PD_DataFrame[Column], format=Covert_Format)
    return PD_DataFrame

def Dataframe_sort(Sort_Dataframe: DataFrame, Columns_list: list, Accenting_list: list) -> DataFrame:
    # Sort Dataframe and reindex 
    Sort_Dataframe.sort_values(by=Columns_list, ascending=Accenting_list, axis=0, inplace = True)
    Sort_Dataframe.reset_index(inplace=True)
    Sort_Dataframe.drop(labels=["index"], inplace=True, axis=1)
    return Sort_Dataframe

def Dataframe_Filter_on_Multiple(Filter_df: DataFrame, Filter_Column: str, Filter_Values: list) -> DataFrame:
    filtered_df = Filter_df[Filter_df[f"{Filter_Column}"].isin(Filter_Values)]
    return filtered_df

def Dataframe_Apply_Value_from_df2(row: Series, Fill_Column: str, Compare_Column_df1: list, Compare_Column_df2: list, Search_df: DataFrame, Search_Column: str):
    # Fill_Column must exists in Dataframe before call of function
    conditions = [Search_df[Compare_Column_df2[index]] == row[Compare_Column_df1[index]] for index, value in enumerate(Compare_Column_df1)]
    combined_condition = Series([True] * len(Search_df), index=Search_df.index)
    for condition in conditions:
        combined_condition &= condition
    new_val = Search_df.loc[combined_condition, f"{Search_Column}"].to_numpy()
    if len(new_val) > 0:
        return new_val[0]
    return row[f"{Fill_Column}"]
    
def Dataframe_Insert_Row_at_position(Insert_DataFrame: DataFrame, Insert_At_index: int, New_Row: dict):
    # Insert the new row
    df1 = Insert_DataFrame.iloc[:Insert_At_index]
    df2 = Insert_DataFrame.iloc[Insert_At_index:]
    new_df = concat([df1, DataFrame([New_Row]), df2]).reset_index(drop=True)
    return new_df