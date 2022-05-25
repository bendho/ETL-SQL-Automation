from __future__ import print_function
from genericpath import exists
import pandas as pd
import PySimpleGUI as sg
import os 

#Imported dataframe from the user.
imported_df = False
#Imported DataFrame post modifications.
modified_df = False

#Reference tables. I need to look into adding more of these later on.

fips_df = pd.read_csv("reference_tables/fipscodes.csv", encoding="latin-1", on_bad_lines='skip')

#Used to find rows within the fips_df that match the parameters. Returns the rows of intrest.
def find_area_rows (area_to_find, geotype_of_area):
    if area_to_find.empty :
        return False

    var_type = type(area_to_find)
    print(var_type)

    if not(isinstance(area_to_find, pd.core.series.Series)):
        return False

    if isinstance(area_to_find, str):
        area_to_find = area_to_find.casefold()
        geotype_of_area = geotype_of_area.casefold()

    active_table = fips_df

    column_list = active_table.columns.values.tolist()

    print(column_list)

    compare_choice = input("What column do you want to compare with the source CSV? ")


#This is a questionable way of coding this, but it works. I should take a look at this later if I can think of something. 

    if not(compare_choice in fips_df.columns):
        print("You did not chose a column that exists.")
        return False

    if (geotype_of_area == False or not geotype_of_area):
        rows_of_intrest = fips_df[fips_df[compare_choice].str.casefold().isin([x.casefold() for x in area_to_find])]
    else :
        rows_of_intrest = fips_df[fips_df[compare_choice].str.casefold().isin([x.casefold() for x in area_to_find]) & (fips_df["geotype"].str.casefold() == geotype_of_area)]

    return rows_of_intrest

#This doesn't work just yet.
def sort_columns():
    global modified_df

    do_sort = input("Do you want to sort the data? y/n ")

    if do_sort == "y":

        modified_df = modified_df.reset_index(drop=True)

        column_list = modified_df.columns.values.tolist()
        print(column_list)
        
        sort_choice = input("Enter the column that you would like to sort by...")
        
        modified_df.sort_values(by=[sort_choice], ascending=False)

def isolate_data(checked_rows, type_of_data) :

    parsed_data = checked_rows[checked_rows.columns.intersection(type_of_data)]
    return parsed_data

# Handles the conversion of actual CSV files.
def compare_df():
    global modified_df

    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    print(modified_df.columns)

    ref_column = input("Chose a column to use as a reference... ")
    modified_df = modified_df.loc[: , ref_column]

    if modified_df.empty :
        print("The column you chose lacks data.")
        return
    
    print(modified_df)

    geo_input = input("Enter a geotype, if none is entered everything will show.... ")
    modified_df = find_area_rows(modified_df, geo_input)

    print(modified_df)

def prune_df_columns():
    global modified_df
    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    column_list = modified_df.columns.values.tolist()
    print(column_list)
    prune_choices = input("Enter the columns that you would like to seperate. use a blank space to seperate your inputs. ")
    prune_choices = prune_choices.split(" ")

    if not all(item in column_list for item in prune_choices):
        return False
        
    modified_df = isolate_data(modified_df, prune_choices)
    print(modified_df)
    
def import_csv():
    inputed_file = input("Input the path for the file that you want to use... ")

    if not ".csv" in inputed_file:
        print("the file you picked was not a csv. please use a csv.")
        return False

    global imported_df
    global modified_df

    imported_df = pd.read_csv(inputed_file, encoding="latin-1", on_bad_lines='skip')
    modified_df = imported_df #So people could export a unmodified csv. I am not sure why someone would do this, but you do you.

def export_csv():
    global modified_df
    
    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    export_path_input = input("Enter a file name to use, files will be exported into the exports folder. ")

    if(not export_path_input):
        print("You did not input a valid path.")
        return False

    cwd = os.getcwd()

    export_path = cwd + "/exports/" + export_path_input + ".csv"

    modified_df.to_csv(export_path)
    print("csv was successfuly exported to " + export_path)

def csv_menu():
    print("0. Exit.")
    print("1. Import a CSV")
    print("2. Compare a the imported CSV with a reference CSV")
    print("3. Prune columns of the imported CSV.")
    print("4. Export the imported CSV.")
    menu_choice = input("choose a menu.... ")

    match menu_choice:
        case '0':
            return
        case '1':
            import_csv()
        case '2':
            compare_df()
        case '3':
            prune_df_columns()
        case '4':
            export_csv()

    print(" ")
    csv_menu() 

#API query to CSV.


#This is used as a launchingpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()