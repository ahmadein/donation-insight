# Table of Contents
1. [Project Summary](README.md#insight-donation-analysis)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Getting Started](README.md#getting-started)
4. [Prerequisites](README.md#prerequisites)
5. [Dependencies](README.md#dependencies)
6. [How to Run](README.md#how-to-run)
7. [Running the tests](README.md#running-the-tests)

# Insight Donation Analysis

This project is to tackle the insight data challenge to analyze donations to political campaigns. The target is to read and process large file as streaming line by line and highlight the repeated donors. The output should not include the repeated donors specific information but stats about which committees received donations from which zip code and at what year. 

# Details of Implementation

The code is implemented in Python 3. The problem is solved by reading the donation file either specified by the user or by default in the input folder one level up from the code. 
In addition, the code calculates the total amount of donations and percentile received from repeated donors specific to each committee, year and zip code

The data is parsed using a python file called *"donation-analytics.py"*. The code is designed to run quickly and to make the entire process as O(n). This was done by utilizing the use of two dictionaries. One is to save the name unique id of the donors and the year they donated in (to ignore the out of order entries). This dictionary made answering the question if a donor is repeated or not very quick as an O(1) process. The second dictionary is a nested dictionary to save the values of donations given from repeated donors based on the year and zip code, hence it was a four level nested dictionary. Again, that helped finding previous donations fast which helped in speeding up the code processing. A clever utilization of try except statement was done to ask the question if *cmte_ID[ZIP_CODE[year]]* was previously found or not instead of using multiple if conditions. As it was possible that a committee was donated to before but not from the same zip code or (even same zip code but not same year]. The try except statement was able to take care of this in one line. 

At the end, the code writes the records of committees' received donations and zip codes and years in addition to the percentile in a file. The file path can be entered by a user or can be default as one level output folder from the source code.

The code avoids hard coding of feature locations by giving the user the options to modify the column number of the features using the following dictionary

```
columns_header = {'CMTE_ID': 0, 'NAME': 7, 'ZIP_CODE': 10, 'TRANSACTION_DT': 13,
 'TRANSACTION_AMT': 14, 'OTHER_ID': 15}  # default dictionary for which columns to read
index_to_keep = [columns_header['CMTE_ID'], columns_header['NAME'], columns_header['ZIP_CODE'], columns_header['TRANSACTION_DT'],
 columns_header['TRANSACTION_AMT'], columns_header['OTHER_ID']]
```

The code runs quick and memory efficient. In one second, it can complete processing 12.8k lines per second of the input file and output the lines related to them on my simple machine. The memory usage is very low as with the use of the dictionaries, **memory used for them are 197MB** to process a file of 6.8M lines with a size of 1.2GB

# Getting Started

Clone or download the repository. Ensure that the donation file and percentile file exists in the right place or provide the paths of the files to the code as shown in the section how to run

# Prerequisites

Make Sure you have Python 3 installed and can be called using python command. If the python program needs to be called using the command *python 3* instead of *python*, please create an alias or modify the run.sh and run_tests.sh accordingly

# Dependencies

```
import numpy as np
import argparse
import time
import sys
```
*numpy* is to calculate the percentile and sum. <br />
*argparse* is to parse the command line arguments given to the file to allow multiple options such as changing paths of files or changing the column number of different fields that the code needs to read in case of reading from different file format. This is a good feature to avoid hard coding. <br />
*time* is to calculate the time that was taken to run the code (optional) <br />
*sys* is to calculate the memory size (optional)

# How to Run

You can run the code by calling the code donation-analytics inside the folder ...\src\. This will run the default code which will read a text file called 'itcont.txt' and 'percentile.txt' inside the folder ...\input\ and will write all the donations list in the file 'repeat-donors.txt' inside the folder ...\output\. In addition, you can run the code by passing arguments to it which can define the input and output files of the codes to be used instead of the default.

Here are all the possible arguments for the code
```
-in or --input_file
-out or --output_file
-per or --percentile_file 
```

-in or --input_file defines the input file path. The default is '...\input\itcont.txt'  
-out or --output_file defines the input file path. The default is '...\output\repeat-donors.txt'<br />
-per or --percentile_file defines the input file path. The default is '...\input\percentile.txt'  

Here are some examples
```
python process_log.py # everything is in default file
python ./src/donation-analytics.py -in ./input/itcont.txt -per 
	./input/percentile.txt -out ./output/repeat_donors.txt
```

Also you can use this dictionary to match the columns of data in your input file by modifying the index next to the field you need

```
columns_header = {'CMTE_ID': 0, 'NAME': 7, 'ZIP_CODE': 10, 'TRANSACTION_DT': 13,
 'TRANSACTION_AMT': 14, 'OTHER_ID': 15}  
```
# Running the tests

All tests exist in the run_tests.sh inside ...\insight_testsuite. An additional test case was added to ensure that the code reads in the right chronological order.

