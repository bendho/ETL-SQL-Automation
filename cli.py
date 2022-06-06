from __future__ import print_function
from genericpath import exists
from pickle import TRUE
import pandas as pd
import PySimpleGUI as sg
import os

import mainfile as mf 

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

def csv_menu():
    print("0. Exit.")
    print("1. Chose a dataframe to use as a reference")

    menu_choice = input("choose a menu.... ")

    match menu_choice:
        case '0':
            return
        case '1':
            select_ref()

    print(" ")
    csv_menu() 

#This is used as a launchingpad to reach other parts of the program
def menu_function() :
    csv_menu()

menu_function()