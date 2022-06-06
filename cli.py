from __future__ import print_function
from genericpath import exists
from pickle import TRUE
import pandas as pd
import PySimpleGUI as sg
import os

import mainfile as mf 

modified_df = False

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

def import_csv():
    inputed_file = input("Input the path for the file that you want to use... ")

    if not ".csv" in inputed_file:
        print("the file you picked was not a csv. please use a csv.")
        return False

    mf.import_csv(inputed_file)

def export_csv():
    export_path_input = input("Enter a file name to use, files will be exported into the exports folder. ")

    if(not export_path_input):
        print("You did not input a valid path.")
        return False

    cwd = os.getcwd()

    export_path = cwd + "/exports/" + export_path_input + ".csv"

    mf.export_csv(export_path)
   

def csv_menu():
    print("0. Exit.")
    print("1. Chose a dataframe to use as a reference")
    print("2. Import a CSV file to transform")
    print("3. Export a DataFrame to a CSV")

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

    print(" ")
    csv_menu() 

#This is used as a launchingpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()