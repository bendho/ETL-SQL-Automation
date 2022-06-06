from __future__ import print_function
from genericpath import exists
from pickle import TRUE
import pandas as pd
import PySimpleGUI as sg
import os

import mainfile as mf 

def import_file():
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

    mf.import_csv(import_path)

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
    print("10. Unpivot Columns")
    print("11. Pivot Columns")
    menu_choice = input("choose a menu.... ")

    match menu_choice:
        case '0':
            return
        case '1':
            import_file()
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
        case '10':
            unpivot()
        case '11':
            pivot()

    print(" ")
    csv_menu() 

#This is used as a launchingpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()