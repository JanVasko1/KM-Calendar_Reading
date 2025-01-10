from pandas import DataFrame
import pandas
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Details_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def AutoFiller(Events: DataFrame):
    for row in Events.iterrows():
        # Define current row as pandas Series
        row_index = row[0]
        row_Series = pandas.Series(row[1])
        Event_Subject = row_Series["Subject"]
        Event_Project = row_Series["Project"]
        Event_Activity = row_Series["Activity"]
        Event_Location = row_Series["Location"]

        for item in Details_dict.items():
            Search_text = item[1]["Search_Text"]
            Part_Found = Event_Subject.find(Search_text)

            if Part_Found == -1:
                pass
            else:
                Project = item[1]["Project"]
                Activity = item[1]["Activity"]
                Location = item[1]["Location"]

                # Project
                if (Project != "") and (Project != Event_Project):
                    Events.at[row_index, "Project"] = Project
                else:
                    pass

                # Activity
                if (Activity != "") and (Activity != Event_Activity):
                    Events.at[row_index, "Activity"] = Activity
                else:
                    pass

                # Location
                if (Location != "") and (Location != Event_Location):
                    Events.at[row_index, "Location"] = Location
                else:
                    pass       
    return Events

def Auto_Activity_Corrections(Events: DataFrame):
    #! Dodělat --> nastavit nějaký automatický process a taky data do SEttings, který by automaticky kontrolovali povolené kombinace Projektu a Aktivity a případně opravit aktivitu + potřeba upravit nastavení a stahovat i k projektům a Aktivitám vztah na "Project Type"
    """
    - musí se vytvořit i nové nastavení a musí se to pokrýt i v stahování "Project/ Activity", kdy ty kombinace by měl aktualizovat
    - pro každý záznam musí kontorlovat jestli Project a Activity patří pod stejný "Proejct Type" a když ne mapovat
    Mapování
        Project - Activity --> Activity
    """
    return Events
