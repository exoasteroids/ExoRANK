#-----------------------------------------------------------------------#
# ExoRANK v0.2.0
# By Hunter Brooks, at NAU, Flagstaff: June 10, 2024
#
# Purpose: Rank a Table Based Off Given Parameters
#-----------------------------------------------------------------------#


# Import all needed packages.
# ------------------------------------------------------------- #
import numpy as np
import pandas as pd
from tqdm import tqdm
import PySimpleGUI as sg
from astropy.io import fits
from astropy.io import ascii
# ------------------------------------------------------------- #


# Table Reading Functions
# ------------------------------------------------------------- #
def table_read():
    try:
        # Reads in the file depending on the filetype
        if values['type'] == 'CSV':
            # If the file is a CSV, read it using pandas
            table = pd.read_csv(values['file'])
        if values['type'] == 'FITS':
            # If the file is a FITS, read it using astropy
            fits_table = fits.open(values['file'])
            table = fits_table[1].data
        if values['type'] == 'ASCII':
            # If the file is an ASCII file, read it using astropy's ascii module
            table = ascii.read(values['file'])
        if values['type'] == 'IPAC':
            # If the file is an IPAC table, read it using astropy's ascii module with IPAC format
            table = ascii.read(values['file'], format='ipac')
        
        # Print confirmation message that the table has been loaded
        print('')
        print('#           Table Has Been Loaded!             #')
        print('')
        
        # Return the loaded table
        return table
    
    except:
        # In case of an error, return 0
        return 0

def column_read(table, user_options, user_types):
    try:
        # Initialize an empty list to hold the column data
        total_column = []
        
        # Iterate over the list of user-specified columns
        for i in range(len(user_options)):
            # Append the data from the specified column to the total_column list
            total_column.append(table[user_options[i]].tolist())
        
        # Return the list of columns
        return total_column
    
    except:
        # In case of an error, return 0
        return 0
# ------------------------------------------------------------- #    



# Matrix Creation Functions
# ------------------------------------------------------------- #
def parm_metrix(column_space, user_types):
    # Initialize an empty list to hold the total parameter space
    total_parm_space = []
    
    # Print a message indicating that the parameter space is being read
    print('')
    print('#           Parameter Space is Being Read!             #')
    
    # Loop over each entry in the first column of column_space
    for i in tqdm(range(len(column_space[0]))):
        # Initialize a temporary list to hold the current parameter space values
        temp_parm_space = []
        
        # Loop over each user-defined type
        for j in range(len(user_types)):
            current_type = user_types[j]
            
            # Check the type and calculate the corresponding parameter value
            if current_type == 'pwd':
                # Convert to pwd (assumed to be milliparsecs)
                temp_value = (column_space[j][i]) * 1000
                temp_parm_space.append(temp_value)
            if current_type == 'mag':
                # Convert to magnitude
                temp_value = 1000 / (column_space[j][i])
                temp_parm_space.append(temp_value)
            if current_type == 'plx':
                # Convert to parallax (assumed to be in milliarcseconds)
                temp_value = (column_space[j][i]) / 100
                temp_parm_space.append(temp_value)
            if current_type == 'distance':
                # Convert to distance in parsecs
                temp_value = (1000 / (column_space[j][i])) / 100
                temp_parm_space.append(temp_value)
            if current_type == 'teff':
                # Convert to effective temperature (assumed to be in units of 10,000 K)
                temp_value = (column_space[j][i]) / 10000
                temp_parm_space.append(temp_value)
            if current_type == 'pm':
                # Convert to proper motion (assumed to be in milliarcseconds/year)
                temp_value = 100 / (column_space[j][i])
                temp_parm_space.append(temp_value)
        
        # Append the temporary parameter space list to the total parameter space list
        total_parm_space.append(temp_parm_space)
        
    # Print a message indicating that the parameter space has been read
    print('#           Parameter Space Has Been Read!             #')
    print('')
    
    # Return the total parameter space list
    return total_parm_space

# ------------------------------------------------------------- #



# Matrix Ranking Functions
# ------------------------------------------------------------- #
def ranking_mult(parameter_matrix, user_scalings):
    # Initialize an empty list to hold the total rank list
    total_rank_list = []
    
    # Print a message indicating that the table is being ranked
    print('')
    print('#           Table Is Being Ranked!             #')
    
    # Loop over each entry in the parameter matrix
    for i in tqdm(range(len(parameter_matrix))):
        # Get the current parameter space (row) from the parameter matrix
        temp_parm_space = parameter_matrix[i]
        
        # Initialize a temporary list to hold the rank values
        temp_rank = []
        
        # Loop over each parameter and apply the corresponding scaling factor
        for j in range(len(temp_parm_space)):
            temp_rank.append(float(temp_parm_space[j]) * float(user_scalings[j]))  # Convert to float
        
        # Sum the scaled parameters and append to the total rank list
        total_rank_list.append(np.nansum(temp_rank))
        
    # Print a message indicating that the table has been ranked
    print('#           Table Has Been Ranked!             #')
    print('')
    
    # Return the total rank list
    return total_rank_list

def rank_table(table, ranked_list):
    # Print a message indicating that ranks are being added to the table
    print('#      Ranks Are Being Added to Table!         #')
    print('')
    
    # Add the ranked list as a new column 'Rank' to the table
    table['Rank'] = ranked_list
    
    # Return the updated table
    return table
# ------------------------------------------------------------- #



# Save Final Table Function
# ------------------------------------------------------------- #
def rank_table_save(ranked_table, output):
    # Print a message indicating that the table is being saved
    print('')
    print('#           Table Is Being Saved!             #')
    print('')
    
    # Convert the ranked table to a pandas DataFrame
    df = pd.DataFrame(ranked_table)
    
    # Save the DataFrame to a CSV file in the 'Output' directory with the specified output filename
    df.to_csv(f'Output/{output}.csv', index=False)
# ------------------------------------------------------------- #



# Sets General ExoRANK Settings
# ------------------------------------------------------------- #
sg.theme('DarkTeal1')

#Makes the drop down window for types of file in the multi-object search
filetype_list = ['CSV', 'FITS', 'ASCII', 'IPAC']
option_type_list = ['pwd', 'mag', 'plx', 'distance', 'teff', 'pm']
user_options = []
user_scalings = []
user_types = []
# ------------------------------------------------------------- #



# ExoRANK GUI Layout
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
window = sg.Window('ExoRANK', layout, size = (300, 380), grab_anywhere=False, finalize=True, enable_close_attempted_event = True)
# ------------------------------------------------------------- #



# Running ExoRANK GUI
# ------------------------------------------------------------- #
while True:
    #Reads all of the events and values, then reads which tab is currently in
    event, values = window.read()
    
    if event == "Change Settings":
        try:
            # Attempt to convert the number of options to an integer
            num_options = int(values['nop'])
        except:
            # Notify the user if there's an error in input
            print('#------------------------------------------------#')
            print('#   Please Enter a Correct Output!  #')
            print('#------------------------------------------------#')
            pass
        
        # Initialize lists for column options, types, and scalings
        col_option = [sg.Text('Column Name: ', font=('Times New Roman', 22), size=(16, 1), justification='center')]
        col_type = [sg.Text('Column Type: ', font=('Times New Roman', 22), size=(16, 1), justification='center')]
        col_scaling = [sg.Text('Column Scaling: ', font=('Times New Roman', 22), size=(16, 1), justification='center')]
        
        # Generate input fields for each option based on the number of options
        for i in range(num_options):
            col_option.append(sg.InputText(size=(18), font=('Times New Roman', 15), key=f'option_{i}'))
            col_type.append(sg.Combo(option_type_list, size=(16), font=('Times New Roman', 15), key=f'type_{i}'))
            col_scaling.append(sg.InputText(size=(18), font=('Times New Roman', 15), key=f'scaling_{i}'))
        
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
        
        # Infinite loop until the user cancels or saves settings
        while True:
            # Initialize lists to store user options, types, and scalings
            user_options = []
            user_types = []
            user_scalings = []
            
            # Read settings from the settings window
            settings_event, settings_values = settings_window.read()
            
            # Break the loop if the settings window is closed or canceled
            if settings_event == sg.WINDOW_CLOSED or settings_event == "Cancel":
                break
            
            # Check if the user clicked the "Save" button
            if settings_event == "Save":
                # Iterate over each option
                for i in range(num_options):
                    # Check if the scaling value is between 0 and 1 and if the type is valid
                    if 0 <= float(settings_values[f'scaling_{i}']) <= 1 and settings_values[f'type_{i}'] in ['pwd', 'mag', 'plx', 'distance', 'teff', 'pm']:
                        # If valid, append user options, types, and scalings
                        user_options.append(settings_values[f'option_{i}'])
                        user_types.append(settings_values[f'type_{i}'])
                        user_scalings.append(settings_values[f'scaling_{i}'])
                    else:
                        # If settings are incorrect, notify the user
                        print('#------------------------------------------------#')
                        print('#         Please Input Correct Settings!         #')
                        print('#------------------------------------------------#')
                
                # Check if all lists have the correct length
                if len(user_scalings) == num_options and len(user_options) == num_options and len(user_types) == num_options:
                    # Break the loop if settings are valid
                    break
                
                settings_window.close()
                
                # Show the main window again
                window.un_hide()
    
    if event in (None, 'Run'):
        try: 
            output = values['output2']
        except: 
            print('#------------------------------------------------#')
            print('#   Please Enter a Correct Output!  #')
            print('#------------------------------------------------#')
            pass
        
        if values['file'] == '': 
            print('#------------------------------------------------#')
            print('#             Please Enter a File!               #')
            print('#------------------------------------------------#')
            pass
        
        if values['type'] not in ['CSV', 'FITS', 'ASCII', 'IPAC']: 
            print('#------------------------------------------------#')
            print('#        Please Enter a Correct Filetype!        #')
            print('#------------------------------------------------#')
            pass
        
        if len(user_options) != 0 and len(user_types) != 0 and len(user_scalings) != 0: 
            print('#----------------------------------------------------#')
            print('#           ExoRANK Has Started Running!             #')
            print('# Please Wait While Calculations Are Being Performed #')
            print('#----------------------------------------------------#')
            
            table = table_read()
            if (table == 0).all().all(): 
                print('#------------------------------------------------#')
                print('#         Please Enter a Correct Table!          #')
                print('#------------------------------------------------#')
                pass
            else:
                column_space = column_read(table, user_options, user_types)
                if column_space == 0: 
                    print('#------------------------------------------------#')
                    print('#        Please Enter a Correct Setting!         #')
                    print('#------------------------------------------------#')
                    pass
                else: 
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
            print('#             Please Set Settings                #')
            print('#------------------------------------------------#')
            pass
               
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
# ------------------------------------------------------------- #



#Closes the window
window.close()