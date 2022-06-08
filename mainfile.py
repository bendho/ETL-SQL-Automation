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

#Return functions, these are mostly used for anything that requires the use of one of the dataframes outside of the main program
def return_reference_df():
    return reference_df

def return_modified_df():
    return modified_df

def return_imported_df():
    return imported_df
    
#Selects a reference table to use. Reference tables are stored within the refrence_tables folder
def select_reference(input_path):
    global reference_df

    if  not exists(input_path):
        print("The file does not exist.")
        return False
     
    reference_df = pd.read_csv(input_path, encoding="latin-1", on_bad_lines='skip')

    print(input_path + " is now the current reference file")

#Imports a file
def import_csv(inputed_file):

    global imported_df
    global modified_df

    imported_df = pd.read_csv(inputed_file, encoding="latin-1", on_bad_lines='skip')
    modified_df = imported_df 

    print("The DataFrame has been imported")

#Exports a CSV
def export_csv(export_path):
    global modified_df

    if modified_df is False:
        print("There is no database to export. Please import a file.")
        return False   

    modified_df.to_csv(export_path)

    print("csv was successfuly exported to " + export_path)


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
def match_df(column_to_match, ref_column):
    global modified_df
    global reference_df

    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    if not(column_to_match in modified_df.columns):
        print("You did not chose a column that exists.")
        return False

    column_to_match = modified_df.loc[: , column_to_match]

    if reference_df[ref_column].empty :
        print("The column you chose lacks data.")
        return False

    if not(ref_column in reference_df.columns):
        print("You did not chose a reference column that exists.")
        return False

    if isinstance(column_to_match, str):
        column_to_match = column_to_match.casefold() 

    rows_of_intrest = reference_df[reference_df[ref_column].str.casefold().isin([x.casefold() for x in column_to_match])]

    modified_df = rows_of_intrest

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

#swaps columns based off user input.
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

def unpivot():
    global modified_df

    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    column_list = modified_df.columns.values.tolist()
    print(column_list)

    user_input_columns = input("Please enter the coulumns that you want to unpivot in a space seperated list... ")
    user_input_columns = user_input_columns.split(" ")

    for column_item in user_input_columns:
        if column_item not in column_list:
            print("The Column you inputed does not exist.")
            return False
    
    safe_columns = [x for x in column_list if x not in user_input_columns]

    user_var_name = input("Input a name for the variable column. If nothing is inserted, a default name will be used.")
    if user_var_name == "" :
        user_var_name = "code"

    user_value_name = input("Input a name for the value column. If nothing is inserted, a default name will be used.")
    if user_value_name == "" :
       user_value_name = "data"

    modified_df = pd.melt(modified_df, id_vars = safe_columns, value_vars = user_input_columns, value_name = user_value_name, var_name = user_var_name)
    print(modified_df)        

def pivot():
    global modified_df

    if modified_df is False:
        print("There is not a database to export. Please import a file.")
        return False

    column_list = modified_df.columns.values.tolist()
    print(column_list)

    user_input_value = input("Please enter value column that you'd like to pivot... ")

    if user_input_value not in column_list:
        print("The Column you inputed does not exist.")
        return False
 
    user_input_column = input("Please enter the column that you'd like to turn into rows.... ")

    if user_input_column not in column_list:
        print("The Column you inputed does not exist.")
        return False
    
    safe_columns = [x for x in column_list if x not in user_input_column]
    safe_columns = [x for x in safe_columns if x not in user_input_value]

    modified_df = modified_df.pivot_table(index=safe_columns, values = user_input_value, columns= user_input_column)            
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
