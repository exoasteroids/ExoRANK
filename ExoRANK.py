
# Import all needed packages.
# ------------------------------------------------------------- #
# GUI Packages
import PySimpleGUI as sg
import pandas as pd
from astropy.io import fits
from astropy.io import ascii
import tqdm
import numpy as np
import csv

def table_read(): 
    #Reads in the file depending on the filetype
    if values['type'] == 'CSV':
        table = pd.read_csv(values['file'])
    if values['type'] == 'FITS':
        fits_table = fits.open(values['file'])
        table = fits_table[1].data
    if values['type'] == 'ASCII':
        table = ascii.read(values['file'])
    if values['type'] == 'IPAC':
        table = ascii.read(values['file'], format = 'ipac')
    
    print('')
    print('#           Table Has Been Loaded!             #')
    print('')
    return table

def column_read(table, user_options, user_types): 
    total_column = []
    for i in range(len(user_options)): 
        total_column.append(table[user_options[i]].tolist())
    return total_column

def parm_metrix(column_space, user_types): 
    total_parm_space = []
    for i in tqdm(range(len(column_space[0]))): 
        temp_parm_space = []
        for j in range(len(user_types)): 
            current_type = user_types[j]
            if current_type == 'pwd': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'mag': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'plx': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'distance': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'teff': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'pm': 
                temp_value = 1
                current_type.append(temp_value)
            if current_type == 'spt': 
                temp_value = 1
                current_type.append(temp_value)
        total_parm_space.append(current_type)
    return total_parm_space

def ranking_mult(parameter_matrix, user_scalings): 
    total_rank_list = []
    print('')
    print('#           Table Is Being Ranked!             #')
    
    for i in tqdm(range(len(parameter_matrix))): 
        temp_parm_space = parameter_matrix[i]
        temp_rank = []
        for j in range(len(temp_parm_space)): 
            temp_rank.append(temp_parm_space[j]*user_scalings[j])
        total_rank_list.append(np.nansum(temp_rank))
        
    print('#           Table Has Been Ranked!             #')
    print('')
    return total_rank_list

def rank_table(table, ranked_list): 
    print('')
    print('#      Ranks Are Being Added to Table!         #')
    print('')
    for i in range(len(table)):
        table[i].append(ranked_list[i])
    return table

def rank_table_save(ranked_table, output): 
    print('')
    print('#           Table Is Being Loaded!             #')
    print('')
    with open(f'Output/{output}.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(ranked_table)

# Sets General WRAP Theme
sg.theme('LightBlue')

#Makes the drop down window for types of file in the multi-object search
filetype_list = ['CSV', 'FITS', 'ASCII', 'IPAC']
option_type_list = ['pwd', 'mag', 'plx', 'distance', 'teff', 'pm', 'spt']

# WRAP GUI LAYOUT
# ------------------------------------------------------------- #
#Makes the layout of WRAP for the single object search, by providing a location for: ra, dec, radius, output file name, catalogs, and output
layout = [
    [sg.Text('ExoRANK', justification='center', size=(12, 1), font = ('Chalkduster', 52))],

    [sg.Text('File Directory', font = ('Times New Roman', 22), size=(50, 1), justification='center')],
    [sg.Text('(CSV, FITS, ASCII, IPAC)', font = ('Times New Roman', 20), size=(50, 1), justification='center')],

    [sg.FileBrowse('File Browser', size = (80, 1), key = 'file', file_types = [('CSV Files', '*.csv'), ('FITS Files', '*.fits'), ('ASCII Files', '*.txt'), ('IPAC Files', '*.txt')])],
    [sg.Text('Filetype', font = ('Times New Roman', 22), size=(12, 1), justification='center'), sg.Text('NOP', size=(25, 1), justification='center', font = ('Times New Roman', 22))],
    [sg.Combo(filetype_list, size = (14), font = ('Times New Roman', 15), key = 'type'), sg.InputText(size = (18), font = ('Times New Roman', 15), key = 'nop')],            
                    
    [sg.Text('Output File Name', size=(25, 1), justification='center', font = ('Times New Roman', 22))], 
    [sg.InputText(key = 'output2', font = ('Times New Roman', 15), size = (40, 2), justification='center')],        
    
    [sg.Button('Change Settings', font = ('Times New Roman', 15), size = (40, 1))],        
                    
    [sg.Button('Run', size = (12), button_color = '#95D49B'), sg.Button('Help', size = (12), button_color = '#F7CC7C'), sg.Button('Close', size = (12), button_color = '#E48671')]
        ]

#Generates the window based off the layouts above
window = sg.Window('ExoRANK', layout, size = (300, 360), grab_anywhere=False, finalize=True, enable_close_attempted_event = True)

# RUNNING WRAP GUI
# ------------------------------------------------------------- #
#Keeps the window open
while True:
    #Reads all of the events and values, then reads which tab is currently in
    event, values = window.read()
    
    num_options = int(values['nop'])
    output = values['output2']
    
    if event == "Change Settings":
        col_option = [sg.Text('Column Name: ', font = ('Times New Roman', 22), size=(16, 1), justification='center')]
        col_type = [sg.Text('Column Type: ', font = ('Times New Roman', 22), size=(16, 1), justification='center')]
        col_scaling = [sg.Text('Column Scaling: ', font = ('Times New Roman', 22), size=(16, 1), justification='center')]
        for i in range(num_options): 
            col_option.append(sg.InputText(size = (18), font = ('Times New Roman', 15), key = f'option_{i}'))
            col_type.append(sg.Combo(option_type_list, size = (16), font = ('Times New Roman', 15), key = 'type'))
            col_scaling.append(sg.InputText(size = (18), font = ('Times New Roman', 15), key = f'scaling_{i}'))
        
        # Settings window layout
        settings_layout = [
            col_option,
            col_type, 
            col_scaling,
            [sg.Button("Save"), sg.Button("Cancel")],
        ]
        
        # Create the settings window
        settings_window = sg.Window("Settings", settings_layout, modal=True)
        
        # Hide the main window
        window.hide()
        
        # Event loop for the settings window
        while True:
            user_options = []
            user_types = []
            user_scalings = []
            settings_event, settings_values = settings_window.read()
            
            if settings_event == sg.WINDOW_CLOSED or settings_event == "Cancel":
                break
            
            if settings_event == "Save":
                for i in range(num_options): 
                    if 0 <= float(settings_values[f'scaling_{i}']) <= 1 and settings_values[f'type_{i}'] in ['pwd', 'mag', 'plx', 'distance', 'teff', 'pm', 'spt']: 
                        user_options.append(settings_values[f'option_{i}'])
                        user_types.append(settings_values[f'type_{i}'])
                        user_scalings.append(settings_values[f'scaling_{i}']) 
                    else: 
                        print('#------------------------------------------------#')
                        print('#         Please Input Correct Settings!         #')
                        print('#------------------------------------------------#')
                if int(len(user_scalings)) == int(num_options) and int(len(user_options)) == int(num_options) and int(len(user_types)) == int(num_options): 
                    break
        
        settings_window.close()
        
        # Show the main window again
        window.un_hide()
    
    if event in (None, 'Run'):
        
        if len(user_options) != 0 and len(user_types) != 0 and len(user_scalings) != 0: 
            print('#----------------------------------------------------#')
            print('#           ExoRANK Has Started Running!             #')
            print('# Please Wait While Calculations Are Being Performed #')
            print('#----------------------------------------------------#')
            table = table_read()
            column_space = column_read(table, user_options, user_types)
            parameter_matrix = parm_metrix(column_space, user_types)
            ranked_list = ranking_mult(parameter_matrix, user_scalings)
            ranked_table = rank_table(table, ranked_list)
            rank_table_save(ranked_table, output)
            print('#----------------------------------------------------#')
            print('#           ExoRANK Has Finished Running!            #')
            print('# Output Table Was Saved to "Output" File Directory  #')
            print('#----------------------------------------------------#')
        else: 
            print('#------------------------------------------------#')
            print('#       Please Set Interall Settings             #')
            print('#------------------------------------------------#')
               
    #Provides the user with the authors information if the 'Help' button is pressed
    if event in (None, 'Help'):
        print('#------------------------------------------------#')
        print('#       Thank you for using ExoRANK!             #')
        print('#      Authors Contact: hcb98@nau.edu            #')
        print('#------------------------------------------------#')

    #Closes WRAP if the 'Close WRAP' button is pressed
    if event in (None, 'Close'):
        print('#------------------------------------------------#')
        print('               Closing ExoRANK                       ')
        print('#------------------------------------------------#')
        break

#Closes the window
window.close()