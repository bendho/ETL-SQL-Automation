from __future__ import print_function
from genericpath import exists
from pickle import TRUE
import pandas as pd
import PySimpleGUI as sg
import os 

#Reference tables. I need to look into adding more of these later on.
fips_df = pd.read_csv("reference_tables/fipscodes.csv", encoding="latin-1", on_bad_lines='skip')

#What dataframe is being used as a refernece? defaults to fipscodes
reference_df = fips_df

#Imported dataframe from the user.
imported_df = False

#Imported DataFrame post modifications.
modified_df = False

#Selects a reference table to use. Reference tables are stored within the refrence_tables folder

def select_reference():
    global reference_df

    print("The following files are avalible for use... ")
    for file in os.listdir("reference_tables"):
        if file.endswith(".csv"):
            print(file) 

    selected_file = input("Select a file to use...  ")

    cwd = os.getcwd()
    import_path = cwd + "/reference_tables/" + selected_file + ".csv"

    if  not exists(import_path):
        print("The file you are looking for does not exist within the directory.")
        return False
     
    reference_df = pd.read_csv(import_path, encoding="latin-1", on_bad_lines='skip')

    print(selected_file + " is now the selected file")

#Used to find rows within the fips_df that match the parameters. Returns the rows of intrest.
def find_area_rows (area_to_find):
    if area_to_find.empty :
        return False

    var_type = type(area_to_find)
    print(var_type)

    if not(isinstance(area_to_find, pd.core.series.Series)):
        return False

    if isinstance(area_to_find, str):
        area_to_find = area_to_find.casefold()

    active_table = fips_df

    column_list = active_table.columns.values.tolist()

    print(column_list)

    compare_choice = input("What column do you want to compare with the source CSV? ")

    if not(compare_choice in fips_df.columns):
        print("You did not chose a column that exists.")
        return False

    rows_of_intrest = fips_df[fips_df[compare_choice].str.casefold().isin([x.casefold() for x in area_to_find])]

    return rows_of_intrest

#This doesn't work just yet.
def sort_columns():
    global modified_df

    modified_df = modified_df.reset_index(drop=True)
    print(modified_df)

    column_list = modified_df.columns.values.tolist()
    print(" ")
    print(column_list)
    
    sort_choice = input("Enter the column that you would like to sort by...")
        
    modified_df = modified_df.sort_values(by=[sort_choice], ascending=True)

    print(modified_df)

#Joins the currnet modified_df to the original df and sets the modified_df as the result
def merge_with_import():
    global imported_df
    global modified_df

    column_list = imported_df.columns.values.tolist()
    print(column_list)
    print("")
    selected_import_column = input("Select a column from the original import column to try and merge...")

    column_list = modified_df.columns.values.tolist()
    print(column_list)
    print("")
    selected_current_column = input("Select a column from the currently modified column to try and merge...")

    modified_df = imported_df.merge(modified_df, left_on=selected_import_column, right_on=selected_current_column)

    modified_df = modified_df.drop(columns=[selected_current_column])
    print(modified_df)

def isolate_data(checked_rows, type_of_data) :

    parsed_data = checked_rows[checked_rows.columns.intersection(type_of_data)]
    return parsed_data

#Used to compare a df with a reference, reindexes the df to fit the reference.
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

    modified_df = find_area_rows(modified_df)

    print(modified_df)

#Used to get rid of df columns
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

def swap_columns():
    global modified_df
    columns = list(modified_df.columns)

    print(columns)

    column_a = input("Input Column A to swap... ")
    
    if column_a not in modified_df.columns:
        print("You have entered a column that does not exist.")
        return False
        
    column_b = input("Input Column B to swap... ")

    if column_b not in modified_df.columns:
        print("You have entered a column that does not exist.")
        return False 
 
    #This feels like spaghetti
    column_a, column_b = columns.index(column_a), columns.index(column_b)
    columns[column_a], columns[column_b] = columns[column_b], columns[column_a]
    modified_df = modified_df[columns]

    print(modified_df)

def prune_df_rows():
    global modified_df
    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    column_list = modified_df.columns.values.tolist()
    print(column_list)
    prune_column = input("Enter the column that you would like to use to prune data form. ")

    prune_choices = input("Enter the data that you want to prune from the selected column. Use spaces to seperate. ")
    prune_choices = prune_choices.split(" ")
    
    prune_df = pd.DataFrame(prune_choices, columns=["temp"])

    modified_df = modified_df.merge(prune_df, left_on=prune_column, right_on=["temp"])

    modified_df = modified_df.drop(columns=["temp"])

    print(modified_df)

#Imports a CSV
def import_csv():
    inputed_file = input("Input the path for the file that you want to use... ")

    if not ".csv" in inputed_file:
        print("the file you picked was not a csv. please use a csv.")
        return False

    global imported_df
    global modified_df

    imported_df = pd.read_csv(inputed_file, encoding="latin-1", on_bad_lines='skip')
    modified_df = imported_df #So people could export a unmodified csv. I am not sure why someone would do this, but you do you.

#Exports a CSV
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
    print("2. Compare a the currently loaded dataframe with a reference CSV")
    print("3. Prune columns of the currently loaded dataframe.")
    print("4. Prune rows of the currently loaded dataframe.")
    print("5. Sort columns of the currently loaded dataframe.")
    print("6. Merge the currently loaded dataframe with the imported CSV.")
    print("7. Export the currently loaded dataframe CSV.")
    print("8. Chose a table to use as a reference")
    print("9. Sort Columns")
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
            prune_df_rows()
        case '5':
            sort_columns()
        case '6':
            merge_with_import()
        case '7':
            export_csv()
        case '8':
            select_reference()
        case '9':
            swap_columns()

    print(" ")
    csv_menu() 

#This is used as a launchingpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()