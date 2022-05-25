from __future__ import print_function
from pickle import FALSE
import pandas as pd
import PySimpleGUI as sg
import os 

#Imported dataframe from the user.
imported_df = pd.DataFrame

#Reference tables. I need to look into adding more of these later on.

fips_df = pd.read_csv("reference_tables/fipscodes.csv", encoding="latin-1", on_bad_lines='skip')

#Used to find rows within the fips_df that match the parameters. Returns the rows of intrest.
def find_area_rows (area_to_find, geotype_of_area):
    if area_to_find.empty :
        return False

    var_type = type(area_to_find)
    print(var_type)

    if not(isinstance(area_to_find, pd.core.series.Series)):
        return FALSE

    if isinstance(area_to_find, str):
        area_to_find = area_to_find.casefold()
        geotype_of_area = geotype_of_area.casefold()

    active_table = fips_df

    column_list = active_table.columns.values.tolist()

    print(column_list)

    compare_choice = input("What column do you want to compare with the source CSV? ")


#This is a questionable way of coding this, but it works. I should take a look at this later if I can think of something. 
    if (geotype_of_area == False or not geotype_of_area):
        rows_of_intrest = fips_df[fips_df[compare_choice].str.casefold().isin([x.casefold() for x in area_to_find])]
    else :
        rows_of_intrest = fips_df[fips_df[compare_choice].str.casefold().isin([x.casefold() for x in area_to_find]) & (fips_df["geotype"].str.casefold() == geotype_of_area)]
    
    rows_of_intrest = rows_of_intrest.reset_index(drop=True)
    # rows_of_intrest.reindex(index=range(len(rows_of_intrest)))
    
    do_sort = input("Do you want to sort the data? y/n ")

    if do_sort == "y":
        column_list = rows_of_intrest.columns.values.tolist()
        print(column_list)
        
        sort_choice = input("Enter the column that you would like to sort by...")
        
        rows_of_intrest.sort_values(by=[sort_choice], ascending=False)

    return rows_of_intrest

def isolate_data(checked_rows, type_of_data) :

    parsed_data = checked_rows[checked_rows.columns.intersection(type_of_data)]
    return parsed_data


def export_file(data_to_export):

    export_file_question = input("export file? This may overwrite any existing files in the export folder with the same name. y/n ")
    
    if export_file_question != "y":
        return
    
    export_path_input = input("Enter a file name to use, files will be exported into the exports folder. ")

    if(not export_path_input):
        print("You did not input a valid path.")
        return False
    

    cwd = os.getcwd()

    export_path = cwd + "/exports/" + export_path_input + ".csv"

    data_to_export.to_csv(export_path)
    print("csv was successfuly exported to " + export_path)

# Handles the conversion of actual CSV files.
def file_input():
    inputed_file = input("Input the path for the file that you want to use... ")

    if not ".csv" in inputed_file:
        print("the file you picked was not a csv. please use a csv.")
        return False
    
    reference_df = pd.read_csv(inputed_file, encoding="latin-1", on_bad_lines='skip')
    
    print(reference_df.columns)

    ref_column = input("Chose a column to use as a reference... ")
    reference_df = reference_df.loc[: , ref_column]

    if reference_df.empty :
        print("The column you chose lacks data.")
        return
    
    print(reference_df)

    geo_input = input("Enter a geotype, if none is entered everything will show.... ")

    found_rows = find_area_rows(reference_df, geo_input)

    print(found_rows)

    choice = input("Would you like to further prune your selection? y/n ")

    if choice == "y":
        column_list = found_rows.columns.values.tolist()
        print(column_list)
        prune_choices = input("Enter the columns that you would like to seperate. use a blank space to seperate your inputs. ")
        prune_choices = prune_choices.split(" ")
        pruned_data = isolate_data(found_rows, prune_choices)
        print(pruned_data)

        found_rows = pruned_data
    
    choice = input("Do you want to export this file? y/n ")

    if choice =="y":
        export_file(pruned_data)

#This is used as a launchingpad to reach other parts of the program
def main_function() :
    file_input()

main_function()