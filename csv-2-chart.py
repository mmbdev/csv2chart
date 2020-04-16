# interpreter [optional-arg]
# -*- coding: utf-8 -*-

# Header and Copyright Informations
__author__ = "Marian Buehler"
__copyright__ = "Copyright 2019, DULCOMETER-Graphenerstellung"
__credits__ = ["wattec GmbH"]
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Marian Buehler"
__email__ = ""
__status__ = "Production"


# Plot Data with Ploty.Express
# https://plot.ly/python/plot-data-from-csv/
# https://plot.ly/python/v3/plot-data-from-csv/

import plotly
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Packeges for FileOpenDialog
import tkinter as tk
from tkinter import filedialog

# standard packages
import os
import csv 
import fileinput
import sys
import re
from shutil import copyfile
import time

# Open File Dialog to Choose CSV File
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

#Defining all Filenames
inputFileName = file_path
outputFileName1 = os.path.splitext(inputFileName)[0] + "_comma.csv"
outputFileName2 = os.path.splitext(inputFileName)[0] + "_change-header-line.csv"
outputFileName3 = os.path.splitext(inputFileName)[0] + "_skip-rows.csv"
outputFileName4 = os.path.splitext(inputFileName)[0] + "_clean-row-replace1.csv"
outputFileName5 = os.path.splitext(inputFileName)[0] + "_clean-row-cut1.csv"
outputFileName6 = os.path.splitext(inputFileName)[0] + "_clean-row-replace2.csv"

# Replace all Semicolons to Commas
with open(inputFileName, 'r') as f:
    with open(outputFileName1, 'w') as t:
        for lines in f:
            new_line = lines.replace(";",",")
            t.write(new_line)

# Replace Haeder Line
with open(outputFileName2, "w") as outfile:
    for line in fileinput.input(
        [outputFileName1],
        inplace=False):
        if fileinput.isfirstline():
            outfile.write('Datum-Uhrzeit,Chlor-ppm-Wert\n')
        else:
            outfile.write(line)

#Remove and Rename File to Raw-Name
os.remove(inputFileName)
os.remove(outputFileName1)
os.rename(outputFileName2, inputFileName)

# Remove Row 2-4
skip_lines = range(1, 4)  # the range is zero-indexed

with open(inputFileName) as f_in, open(outputFileName3, "w") as f_out:
    current_line = 0  # keep a line counter
    for line in f_in:  # read the input file line by line
        if current_line not in skip_lines:
            f_out.write(line)  # not in our skip range, write the line
        current_line += 1  # increase the line counter

# Remove and Rename File to Raw-Name
os.remove(inputFileName)
os.rename(outputFileName3, inputFileName)

# Delete Last Comma and Delete other Values
with open(inputFileName, 'r') as file_text:       #Open your file
    lines = file_text.readlines()                 #Read all the lines from your file, then put them in a list
    newlines = []                                 #Make a list to save edits in
    for line in lines:                            #Loop over all the lines, each line will first go into variable line for some actions
        newline = line.replace(', , , ,  ', 'A')  #Replace the text in word_delete to an empty string (aka nothing)
        newlines.append(newline)                  #Add the edit to the list with edits
with open(outputFileName4, 'w') as file_text:     #Open the file, but in write mode
    file_text.writelines(newlines)                #Write the list with edits to the new file

# Remove and Rename File to Raw-Name
os.remove(inputFileName)
os.rename(outputFileName4, inputFileName)

with open(inputFileName, 'r') as file_text:                         #Open your file
    lines = file_text.readlines()                                   # Read all the lines from your file, then put them in a list
    newlines = []                                                   #Make a list to save edits in
    for line in lines:                                              #Loop over all the lines, each line will first go into variable line for some actions
        newline = re.sub(',.*Aus, ','',line,flags=re.DOTALL)        #Replace the text in word_delete to an empty string (aka nothing)
        newlines.append(newline)                                    #Add the edit to the list with edits
with open(outputFileName5, 'w') as file_text:                       #Open the file, but in write mode
    file_text.writelines(newlines)                                  #Write the list with edits to the new file

# Remove and Rename File to Raw-Name
os.remove(inputFileName)
os.rename(outputFileName5, inputFileName)

with open(inputFileName, 'r') as file_text:       #Open your file
    lines = file_text.readlines()                 #Read all the lines from your file, then put them in a list
    newlines = []                                 #Make a list to save edits in
    for line in lines:                            #Loop over all the lines, each line will first go into variable line for some actions
        newline = line.replace('A', ',')          #Replace the text in word_delete to an empty string (aka nothing)
        newlines.append(newline)                  #Add the edit to the list with edits
with open(outputFileName6, 'w') as file_text:     #Open the file, but in write mode
    file_text.writelines(newlines)                #Write the list with edits to the new file

# Remove and Rename File to Raw-Name
os.remove(inputFileName)
os.rename(outputFileName6, inputFileName)

# Read CSV Path with Filename
df = pd.read_csv(inputFileName)

# Change column to datetime type
df['Datum-Uhrzeit'] = pd.to_datetime(df['Datum-Uhrzeit']) 
#df['Datum-Uhrzeit'].dt.strftime('%H:%M:%S')

# Read Input CSV File
# print(df)
# input()

#Choose Variables and Figure-Setup
# fig = go.Figure(go.Scatter(x = df['Datum-Uhrzeit'], y = df['Chlor-ppm-Wert'],
#                  name='Chlor-Anteil in ppm'))

#fig.update_layout(title='Chlormessungsdiagramm von Datei ' + os.path.basename(file_path),
#                   plot_bgcolor='rgb(230, 230,230)',
#                   showlegend=True)

# With axis labeling
fig = px.line(df, x = 'Datum-Uhrzeit', y = 'Chlor-ppm-Wert', title='Chlormessungsdiagramm von Datei ' + os.path.basename(file_path))

# Copy Chart to the same Data-Folder

diagramm_path = os.path.dirname(file_path) + "/Diagramme"

if not os.path.exists(diagramm_path):
    os.mkdir(diagramm_path)

fig.write_image('{}/{}.png'.format(diagramm_path, os.path.basename(file_path)))

#Draw Diagramm
fig.show()

# input("Press some Key to exit")
