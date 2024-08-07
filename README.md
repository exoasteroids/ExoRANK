<h1 align="center" id="title"> 📉 ExoRANK 📈 </h1>
<div align="center">

<p id="description"> <b>ExoRANK</b> is a tool designed to rank data within a table based on specified input parameters, which are derived from the column names in the table. The supported input parameters include probability of a white dwarf, magnitude space, parallax, distance, effective temperature, and proper motion. The program processes the data and outputs the original CSV file with an additional column labeled "Rank".  </p>
</div>

<div align="center">
  <h2>🛠️ Installation 🛠️</h2>
</div>

<div align="center">
<pp><b>🐍 Anaconda Environment 🐍</b><pp>
</div>
<div align="center">
<pp><b>-----------------------------------------</b><pp>
</div>

**Note**: Making use of an Anaconda (Conda) environment is highly recommended due to potential compatibility issues with older Python and pip packages when using ExoRANK.

1. **Download Anaconda Navigator**: To get started, please visit [Anaconda's official website](https://www.anaconda.com) and download the version of Anaconda Navigator that matches your operating system.

2. **Access Anaconda Environments**: After downloading and installing Anaconda Navigator, launch the application. In the Navigator's main window, you will find an "Environments" option on the left. Click on it to access your Conda environments.

3. **Create a New Conda Environment**: In the "Environments" section, you will see a plus sign labeled "Create." Click on it to create a new Conda environment.

4. **Customize Environment Settings**: Give your new environment a name of your choice (e.g., "exorank"). Next, select a Python version that is closest to Python 3.8 (e.g., 3.8.18). Then, click the "Create" button to create the environment.

5. **Environment Creation**: The environment creation process may take a while, as Conda will install the necessary packages and dependencies for WRAP.

6. **Activate Your Conda Environment**: Once the environment is successfully created, you can activate it in your terminal. Open your terminal and enter the following command, replacing `*conda name*` with the name you chose for your environment:
   ```bash
   conda activate *conda name*

<div align="center">
  <p><b>⬇️ PIP Installation ⬇️</b></p>
</div>
<div align="center">
<pp><b>-----------------------------------------</b><pp>
</div>

1. Once the conda environment is activated, go to your directory containing the ExoRANK contents and enter the directory named Output (e.g., "cd Documents/GitHub/ExoRANK").
2. Run the command:
   ```bash
   pip install -r requirements.txt


<div align="center">
<pp><b> Opening ExoRANK </b><pp>
</div>
<div align="center">
<pp><b>-----------------------------------------</b><pp>
</div>

To open the application, type the following command into your terminal:

**Note that the "python" command might change on how python is installed on your machine**

- For MacOS: `python ExoRANK.py`
- For Windows: `python .\ExoRANK.py`

<div align="center">
  <h2>🏆 Using ExoRANK 🏆</h2>
</div>

<div align="center">
  <p><b>How to Use ExoRANK</b></p>
</div>
<div align="center">
<pp><b>-----------------------------------------</b><pp>
</div>

**ExoRANK Main Window**

1. Open ExoRANK. You will need to provide ten inputs before clicking "Run":
2. Click "Ranking File Browser" to select your table that is going to be ranked. Supported table types are CSV, FITS, ASCII, and IPAC.
3. Click "True-Positive File Browser" to select your table that is going to be added randomly in as your true-positives. Supported table types are CSV, FITS, ASCII, and IPAC.
4. Click "True-Negative File Browser" to select your table that is going to be added randomly in as your true-negatives. Supported table types are CSV, FITS, ASCII, and IPAC.
5. Choose the file type of your selected tables from the dropdown menu below. All tables must be the same file type
6. Enter the number of parameters by typing a positive integer in the "NOP" text box. This represents the columns you are using in the ranking algorithm.
7. Input a positive integer into the "Chunk Size" text box to select the size of each output csv, ie how many rows.
8. Input a percentage, between 0 and 1, into the "Positive %" text box to select the percentage of the chunk size with be true-positives. 
9. Input a percentage, between 0 and 1, into the "Negative %" text box to select the percentage of the chunk size with be true-negatives. 
10. Type the desired output file name as a string in the "Output File Name" text box.
11. Click the "Change Settings" button at the bottom. A new window will appear. Refer to the instructions below for guidance on using this popup window.
12. Once all parameters are set, click "Run" to execute the algorithm.
13. The output tables will be saved as a CSV file in the "Output" file directory.

**ExoRANK "Change Settings" Window**

1. Once you click the "Change Settings" button, a new window will appear with N columns (equal to the number of parameters entered earlier). Each column corresponds to a different parameter and contains three rows requiring input.
2. In the first row, labeled "Column Name," enter the name of the column to be used as a parameter.
3. The second row, labeled "Column Type," features a dropdown menu with the following options:
    * ***pwd***: Probability of White Dwarf (range: 0 to 1)
    * ***mag***: Magnitude of a particular band
    * ***plx***: Parallax of an object in milliarcseconds
    * ***distance***: Distance of an object in parsecs
    * ***teff***: Effective temperature of the white dwarf in Kelvin
    * ***pm***: Proper motion of the white dwarf in milliarcseconds per year
1. The third row, labeled "Column Scaling," requires you to input a scaling value for each parameter, ranging from 0 to 1.
2. After all fields are completed, click "Save" to return to the main window in ExoRANK.

<div align="center">
  <p><b>⚠️ Significant Details ⚠️</b></p>
  <p>-----------------------------------------</p>
</div>

- **Note 1**: Only tested on MacOS >11; problems may occur for older versions of MacOS and Windows ***(NOT SUPPORTED ON LINUX)***.
- **Note 2**: The window close button has been disabled; to close ExoRANK, please click the red "Close" button at the bottom.
- **Note 3**: Even though Right Ascension and Declination are not used in the ranking algorithm, ExoRANK requires two columns labeled: "RA" and "DEC" for use. 
-  **Note 4**: If the number of true-positives and true-negatives goes over the size of the sample you provide then it will simple just add how many rows are in the csv, ie resample has been turned off. 


<div align="center">
  <h2>📞 Support 📞</h2>
</div>

- **Mr. Hunter Brooks**
  - Email: hcb98@nau.edu
