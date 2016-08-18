'''
Created on Aug 4, 2016

@author: Xianguang Yan
'''
from function import *
from collections import deque
import csv

#Global Variables
row_count = -1
input_str = []
col1 = CSVClass()
col2 = CSVClass()
col3 = CSVClass()
col4 = CSVClass()
col5 = CSVClass()
col6 = CSVClass()
col7 = CSVClass()
col8 = CSVClass()
col9 = CSVClass()
col10 = CSVClass()

#Bin Boundries
BIN1_LOWER = 5200.0
BIN1_UPPER = 5300.0
BIN2_LOWER = 5300.0
BIN2_UPPER = 5400.0
BIN3_LOWER = 5400.0
BIN3_UPPER = 5500.0
BIN4_LOWER = 5500.0
BIN4_UPPER = 5600.0
BIN5_LOWER = 5600.0
BIN5_UPPER = 5700.0
BIN6_LOWER = 5700.0
BIN6_UPPER = 5800.0

        
def getArray(csvFile):
    return [str(averageSum(csvFile.bin_1, csvFile.count_1)), str(averageSum(csvFile.bin_2, csvFile.count_2)), str(averageSum(csvFile.bin_3, csvFile.count_3)), str(averageSum(csvFile.bin_4, csvFile.count_4)), str(averageSum(csvFile.bin_5, csvFile.count_5)), str(averageSum(csvFile.bin_6, csvFile.count_6))]

def inputBin(number, csvFile):
    if number >= BIN1_LOWER and number <= BIN1_UPPER:
        csvFile.addBin1(number)
    elif number >= BIN2_LOWER and number <= BIN2_UPPER:
        csvFile.addBin2(number)
    elif number >= BIN3_LOWER and number <= BIN3_UPPER:
        csvFile.addBin3(number)           
    elif number >= BIN4_LOWER and number <= BIN4_UPPER:
        csvFile.addBin4(number)
    elif number >= BIN5_LOWER and number <= BIN5_UPPER:
        csvFile.addBin5(number)
    elif number >= BIN6_LOWER and number <= BIN6_UPPER:
        csvFile.addBin6(number)
                
#Open CSV and read Moving Average
with open('results.csv', 'wb') as resultsfile:
    myWriter = csv.writer(resultsfile, delimiter=',')
    first_line = [] #write the header/description
    next_line = []
    with open('test.csv', 'rb') as csvfile:
        myReader= csv.reader(csvfile, delimiter=',')
        for row in myReader: 
            if row_count == -1: #Get First Line of Words
                for x in range(len(row)):
                    if len(row[x]) != 0:
                        print row[x]
                        first_line.append(row[x])
                    else:
                        myWriter.writerow(first_line)
                        break
                row_count = 0
            elif row_count < 490: # Do nothing from 0 - 490
                row_count = int(row[0])
            elif row_count >= 490 and row_count < 500: #Sets Up Moving Average
                print col1.getMovingAvg()
                col1.rotate(row[1])
                col2.rotate(row[2])
                col3.rotate(row[3])
                col4.rotate(row[4])
                col5.rotate(row[5])
                col6.rotate(row[6])  
                col7.rotate(row[7])
                col8.rotate(row[8])
                col9.rotate(row[9])
                col10.rotate(row[10])  
                row_count = int(row[0]) #checks current pixels
              
            elif (row_count >= 500) and (row_count <= 1500):
    
                col1.rotate(row[1])
                inputBin(getAvg(col1.getMovingAvg()), col1)
                
                col2.rotate(row[2])
                inputBin(getAvg(col2.getMovingAvg()), col2)
                
                col3.rotate(row[3])
                inputBin(getAvg(col3.getMovingAvg()), col3)
                
                col4.rotate(row[4])
                inputBin(getAvg(col4.getMovingAvg()), col4)
                
                col5.rotate(row[5])
                inputBin(getAvg(col5.getMovingAvg()), col5)
                
                col6.rotate(row[6])
                inputBin(getAvg(col6.getMovingAvg()), col6)

                col7.rotate(row[7])
                inputBin(getAvg(col7.getMovingAvg()), col7)
                
                col8.rotate(row[8])
                inputBin(getAvg(col8.getMovingAvg()), col8)
                
                col9.rotate(row[9])
                inputBin(getAvg(col9.getMovingAvg()), col9)
                
                col10.rotate(row[10])
                inputBin(getAvg(col10.getMovingAvg()), col10)    
                            
                #Appends Pixel Number
                input_str.append(str(row_count))
                
                
                if(getAvg(col1.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col1.getMovingAvg())))
                if(getAvg(col2.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col2.getMovingAvg())))
                if(getAvg(col3.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col3.getMovingAvg())))
                if(getAvg(col4.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col4.getMovingAvg())))
                if(getAvg(col5.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col5.getMovingAvg())))
                if(getAvg(col6.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col6.getMovingAvg())))
                if(getAvg(col7.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col7.getMovingAvg())))
                if(getAvg(col8.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col8.getMovingAvg())))
                if(getAvg(col9.getMovingAvg()) != -1): 
                    input_str.append(str(getAvg(col9.getMovingAvg())))
                if(getAvg(col10.getMovingAvg()) != -1):
                    input_str.append(str(getAvg(col10.getMovingAvg())))
                    
                myWriter.writerow(input_str)
                print col1.count_2
                print input_str
                input_str = []
                row_count = row_count + 1
                
                
            else:
                break
            
with open('bin.csv', 'wb') as binfile:
    mybin = csv.writer(binfile, delimiter=',')
    print col1.count_1, col2.count_2, col1.bin_1, col2.bin_1
    #Write Bin
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col1))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col2))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col3))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col4))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col5))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col6))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col7))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col8))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col9))
    
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow(getArray(col10))
    
