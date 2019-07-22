import fexcel
import pandas as pd
from os import listdir
import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
from os.path import isfile, join, isdir
mainpath = '/home/manan/Desktop/HvsR/';        #Edit the path of the directory
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

# Whole directory analysis for dT/dt
# Main directory = all height  directories
# Subdirectory = all height directories containing different radius files
#Filename for each file is in the way height_diameterserial(a or b)

# Output will be a text file with dT/dt for every file. This will be in the main directory

subdirpaths = [join(mainpath,dir) for dir in listdir(mainpath)]; #paths of the subdirectories
tstart = 90

def indexer(data):
    center = data.loc[:,'Untitled'].values;
    lower = 0;
    upper = 0;
    for i in range(len(center)-1):
        if center[i+1] > tstart:
            if center[i] < tstart:
                lower = i+1;
        if center[i+1] > 100:
            if center[i] < 100:
                upper = i+1;
                break
#
    ind = [lower,upper];
    return ind

def extractor(file):
    if file[0] == '1':
        lw = 105
        if file[4] == '5':
            dw = 5
        elif file[4] == '8':
            dw = 8
        elif file[4] == '1':
            if file[5] == '1':
                dw = 11
            else:
                dw = 14
    elif file[0] == '2':
        lw = 25
    elif file[0] == '4':
        lw = 45
    elif file[0] == '6':
        lw = 65
    elif file[0] == '8':
        lw = 85
    if file[3] == '5':
        dw = 5
    elif file[3] == '8':
        dw = 8
    elif file[3] == '1':
        if file[4] == '1':
            dw = 11
        else:
            dw = 14
    if file[len(file)-6] == 'a':
        trial_num = 1
    elif file[len(file)-6] == 'b':
        trial_num = 2
    return [lw,dw,trial_num]

def cell_extract(lw,dw,trial_num):
    rows1 = []
    rows2 = []
    data = pd.read_excel('/home/manan/Desktop/final_results.xlsx')
    print(data)
    height = data.loc[:,'Height (mm)'].values
    print(height)
    diameter = data.loc[:,'Diameter (mm)'].values
    print(diameter)
    for ind in range(len(height)):
        if height[ind] == lw:
            rows1.append(ind+1)
        if diameter[ind] == dw:
            rows2.append(ind+1)
    if trial_num == 1:
        col = 4
    elif trial_num == 2:
        col = 6
    row = list(set(rows1).intersection(rows2))[0]
    return [row,col]

fi = open('results.txt','a+');
for path in subdirpaths:
    fexcel.modify_xl(path)

    files = [f for f in listdir(path) if isfile(join(path, f))];
    for file in files:
        print(file)
        [lw,dw,trial_num] = extractor(file)
        print(extractor(file))
        [row,col] = cell_extract(lw,dw,trial_num)
        data = pd.read_excel(join(path, file));
        ind = indexer(data);
        center = data.loc[ind[0]:ind[1],'Untitled'].values;
        corner = data.loc[ind[0]:ind[1],'Untitled 1'].values;
        time = data.loc[ind[0]:ind[1],'Untitled 3'].values;
        print(time)
        num = time[0];
        for i in range(len(time)):
            time[i] = time[i] - num;

        # Plotting
        plt.figure();
        ax = plt.axes()
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
        ax.xaxis.set_minor_locator(plt.MaxNLocator(50))
        ax.yaxis.set_major_locator(plt.MaxNLocator(10))
        ax.yaxis.set_minor_locator(plt.MaxNLocator(50))
        ax.xaxis.grid(True, which='minor')
        plt.scatter(time,center, label = 'center')
        plt.scatter(time,corner, label = 'corner')
        ax.grid(which = 'major', linestyle='-', linewidth = 0.9, alpha=1.0)
        ax.grid(which = 'minor', linestyle=':', linewidth = 0.6, alpha=0.8)
        plt.legend(loc = 'upper left')
        plt.xlabel('time (sec)')
        plt.ylabel('T')
        plt.title(file)
    #    plt.show()
        plt.savefig('/home/manan/Desktop/plots/' + str(tstart) +'/' + file +'.png')

        #Storing the data in final_results.xlsx
        rb = xlrd.open_workbook('/home/manan/Desktop/final_results.xlsx')
        r_sheet = rb.sheet_by_index(0)
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        sheet.write(row,col,label = np.polyfit(time,center,1)[0])
        sheet.write(row,col+1,label = np.polyfit(time,corner,1)[0])
        wb.save('/home/manan/Desktop/final_results.xlsx')


        fi.write(file + ' center ' +str(np.polyfit(time,center,1)[0]) +'\n')
        fi.write(file + ' corner ' +str(np.polyfit(time,corner,1)[0]) +'\n')
