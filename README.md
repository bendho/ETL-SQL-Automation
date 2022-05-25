# ETL Automation CLI Program (pending name.)
This program is supposed to speed up the importing and exporting of csv files. Made using Python.

Reference CSVs are stored within the reference_table folder.

Use `-python mainfile.py` in a terminal with the directory set to the project folder to start the program.
Export .CSVs are exported into the exports folder.

# Commands

## Import CSV
loads a CSV file into the buffer, for manipulation

## Compare
Compares the currently loaded CSV with a reference CSV file

## Prune Columns
Removes all of the columns except for the ones inputed

## Prune Rows
Removes all of the rows except for the ones inputed

## Sort
Reindexes all of the data within the currently buffered table to a user inputed column

## Merge
Merges the buffered table with the original CSV that was imported, storing the product as the buffered table.

## Export
Exports the buffered table into a CSV.
