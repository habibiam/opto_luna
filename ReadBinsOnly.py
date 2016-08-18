'''
Created on Aug 11, 2016

@author: Xianguang Yan
'''
from function import *
from collections import deque
import csv

#Global Variables
row_count = -1.0
input_str = []
columns = CSVClass()
col_count = 0
create_list = True
#Open CSV and read Moving Average
with open('results.csv', 'wb') as resultsfile:
    myWriter = csv.writer(resultsfile, delimiter=',')
    first_line = [] #write the header/description
    with open('test3.csv', 'rb') as csvfile:
        myReader= csv.reader(csvfile, delimiter=',')
        for row in myReader: 
            try:
                row_count = float(row[0])
                columns.rotate(row_count)
                inputBin(row_count, columns)
                print row_count
                print columns.moving_avg
            except:
                continue
            
with open('bin.csv', 'wb') as binfile:
    print columns.bin_1
    mybin = csv.writer(binfile, delimiter=',')
    #Write Bin: 
    mybin.writerow(['Bin 1: 510 - 530', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])

    mybin.writerow(getArray(columns))
    mybin.writerow([])
    
   