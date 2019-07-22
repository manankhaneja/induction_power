# Takes the raw data directory as input
# Processes each file (excel file) in the directory and do the required time interpolation
# The format of each file is fixed-- This increase the ease of processing of the file

import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
from os import listdir
from os.path import isfile, join

def modify_xl(mypath):
    print(mypath)
#   mypath = '/home/manan/Desktop/check';        #Edit the path of the directory
    files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]


    for file in files:
        rb = xlrd.open_workbook(file)       # wb == workbook
        wb = copy(rb)
        wbsheet = wb.get_sheet(0)
        sheet = rb.sheet_by_index(0)
        timeval = sheet.col_values(4)       # 4 means column 5 in the file which is the time column
        timeval[0] = '0';                     # Changing the title from string to a number
        i = 1;                      # the first column value is title of the column
        while i < len(timeval) - 14:             # Limiting the total time to be less than 1000/14 seconds. 14 is the frequency of data capturing
            step = (timeval[i+14] - timeval[i])/14;
            for j in range(13):
                temp = timeval[i] + step*(j+1);
                wbsheet.write(i+j+1,4,temp)
            i = i+14;
        wb.save(file);
