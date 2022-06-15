from __future__ import print_function
from genericpath import exists
from pickle import TRUE
import pandas as pd
import PySimpleGUI as sg
import os

import mainfile as mf 

modified_df = False

#Reference functions
def select_ref():
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

    mf.select_reference(import_path)

#Import and Export functions 
def import_csv():
    inputed_file = input("Input the path for the file that you want to use... ")

    if not ".csv" in inputed_file:
        print("the file you picked was not a csv. please use a csv.")
        return False

    mf.import_csv(inputed_file)

def export_csv():
    if mf.check_modified_df() == False:
        return   

    export_path_input = input("Enter a file name to use, files will be exported into the exports folder. ")

    if(not export_path_input):
        print("You did not input a valid path.")
        return False

    cwd = os.getcwd()

    export_path = cwd + "/exports/" + export_path_input + ".csv"

    mf.export_csv(export_path)

def match_df():
    if mf.check_modified_df() == False:
        return   
    
    modified_df = mf.return_modified_df()

    print(modified_df.columns)
    
    match_column = input("Input a column to find a match with.... ")

    if not (match_column in modified_df.columns):
        print("You did not enter a valid column to match.")
        return False

    reference_df = mf.return_reference_df()
    print(reference_df.columns)

    reference_column = input("Input a column to match with from the reference table")

    if not (reference_column in reference_df.columns):
        print("You did not enter a valid column to match. ")
        return False

    mf.match_df(match_column, reference_column)  

def swap_columns():
    if mf.check_modified_df() == False:
        return   
 
    modified_df = mf.return_modified_df()

    print(list(modified_df.columns))

    column_a = input("Input Column A to swap... ")

    column_b = input("input Column B to swap... ")

    mf.swap_columns(column_a, column_b)

def pivot_columns():
    if mf.check_modified_df() == False:
        return   
 
    modified_df = mf.return_modified_df()

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
 
    mf.pivot(user_input_value, user_input_column)

def unpivot():
    if mf.check_modified_df() == False:
        return   

    modified_df = mf.return_modified_df()

    column_list = modified_df.columns.values.tolist()
    print(column_list)

    user_input_columns = input("Please enter the coulumns that you want to unpivot in a space seperated list... ")
    user_input_columns = user_input_columns.split(" ")

    for column_item in user_input_columns:
        if column_item not in column_list:
            print("The Column you inputed does not exist.")
            return False

    user_var_name = input("Input a name for the variable column. If nothing is inserted, a default name will be used.")
    if user_var_name == "" :
        user_var_name = "code"

    user_value_name = input("Input a name for the value column. If nothing is inserted, a default name will be used.")
    if user_value_name == "" :
       user_value_name = "data"

    mf.unpivot(user_input_columns, user_var_name, user_value_name)    

def sort_by_column():    
    if mf.check_modified_df() == False:
        print("There is not a DataFrame to try and sort")
        return

    modified_df = mf.return_modified_df()
    column_list = modified_df.columns.values.tolist()

    print(column_list)
    sort_choice = input("Enter the column that you would like to sort by...")

    mf.sort_columns(sort_choice)

def prune_columns():
    if mf.check_modified_df() == False:
        return   

    modified_df = mf.return_modified_df()
    column_list = modified_df.columns.values.tolist()
    print(column_list)

    prune_choices = input("Enter the columns that you would like to seperate. use a blank space to seperate your inputs. ")
    prune_choices = prune_choices.split(" ")

    mf.prune_df_columns(prune_choices)

def isolate_rows():
    if mf.check_modified_df() == False:
        return
    
    modified_df = mf.return_modified_df()
    column_list = modified_df.columns.values.tolist()
    
    print(column_list)
    prune_column = input("Input a column to look at when isolating data. ")

    if not prune_column in column_list:
        print("The column you inputed does not exist.")
        return
    
    prune_data = input("Enter data from the selected column to isolate rows by, use a space to seperate data ")
    prune_data = prune_data.split(" ")

    if len(prune_data) == 0:
        print("You didn't enter any data to try and isolate")

    mf.isolate_df_rows(prune_column, prune_data)
#Main Menu function
def csv_menu():
    print("0. Exit.")
    print("1. Chose a dataframe to use as a reference")
    print("2. Import a CSV file to transform")
    print("3. Export a DataFrame to a CSV")
    print("4. Match the imported DataFrame with a reference table")
    print("5. Swap columns from the current modified DF")
    print("6. Pivot Columns")
    print("7. Unpivot Columns")
    print("8. Prune Columns")
    print("9. Isolate Rows.")
    print("10. Sort by Column.")

    menu_choice = input("choose a menu.... ")

    match menu_choice:
        case '0':
            return
        case '1':
            select_ref()
        case '2':
            import_csv()
        case '3':
            export_csv()
        case '4':
            match_df()
        case '5':
            swap_columns()
        case '6':
            pivot_columns()
        case '7':
            unpivot()
        case '8':
            prune_columns()
        case '9':
            isolate_rows()
        case '10':
            sort_by_column()

    print(" ")
    csv_menu() 

#This is used as a launchpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()