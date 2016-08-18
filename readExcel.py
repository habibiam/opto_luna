'''
Created on Aug 4, 2016

@author: Xianguang Yan
'''
from function import *
from collections import deque
import csv

class MyClass:
    x = 0
    def f(self):
        return x

#Global Variables
row_count = -1
input_str = []
moving_avg = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg2 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg3 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg4 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg5 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg6 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg7 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg8 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg9 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
moving_avg10 = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

#Sum of Bins
BIN1 = 0
BIN2 = 0
BIN3 = 0
BIN4 = 0
BIN5 = 0
BIN6 = 0

#Number of Counts for Bins
bin1_count = 0
bin2_count = 0
bin3_count = 0
bin4_count = 0
bin5_count = 0
bin6_count = 0

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

#Function
#Places all the moving averages in the selected bins and adds them all up
def inputBin(number):
    global BIN1, BIN2, BIN3, BIN4, BIN5, BIN6, bin1_count, bin2_count, bin3_count, bin4_count, bin5_count, bin6_count
    if number >= BIN1_LOWER and number <= BIN1_UPPER:
            BIN1 = BIN1 + number
            bin1_count = bin1_count + 1  
    elif number >= BIN2_LOWER and number <= BIN2_UPPER:
            BIN2 = BIN2 + number
            bin2_count = bin2_count + 1 
    elif number >= BIN3_LOWER and number <= BIN3_UPPER:
            BIN3 = BIN3 + number
            bin3_count = bin3_count + 1           
    elif number >= BIN4_LOWER and number <= BIN4_UPPER:
            BIN4 = BIN4 + number
            bin4_count = bin4_count + 1
    elif number >= BIN5_LOWER and number <= BIN5_UPPER:
            BIN5 = BIN5 + number
            bin5_count = bin5_count + 1
    elif number >= BIN6_LOWER and number <= BIN6_UPPER:
            BIN6 = BIN6 + number
            bin6_count = bin6_count + 1      
                
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
                try:
                    moving_avg.rotate(-1)
                    moving_avg[9] = row[1]
                except:
                    print 'nothing in col 1'
                try:
                    moving_avg2.rotate(-1)
                    moving_avg2[9] = row[2]
                except:
                    print 'nothing in col 2'
                try:
                    moving_avg3.rotate(-1)
                    moving_avg3[9] = row[3]
                except:
                    print 'nothing in col 3'
                try:
                    moving_avg4.rotate(-1)
                    moving_avg4[9] = row[4]
                except:
                    print 'nothing in col 4'
                try:
                    moving_avg5.rotate(-1)
                    moving_avg5[9] = row[5]
                except:
                    print 'nothing in col 5'
                try:
                    moving_avg6.rotate(-1)
                    moving_avg6[9] = row[6]
                except:
                    print 'nothing in col 6'
                try:
                    moving_avg7.rotate(-1)
                    moving_avg7[9] = row[7]
                except:
                    print 'nothing in col 7'
                try:
                    moving_avg8.rotate(-1)
                    moving_avg8[9] = row[8]
                except:
                    print 'nothing in col 8'
                try:
                    moving_avg9.rotate(-1)
                    moving_avg9[9] = row[9]
                except:
                    print 'nothing in col 9'
                try:
                    moving_avg10.rotate(-1)
                    moving_avg10[9] = row[10]
                except:
                    print 'nothing in col 10'
                    
                row_count = int(row[0]) #checks current pixels
              
            elif (row_count >= 500) and (row_count <= 1500):
                try:
                    moving_avg.rotate(-1)
                    moving_avg[9] = row[1]
                    inputBin(getAvg(moving_avg))
                except:
                    print 'nothing in col 1'
                try:
                    moving_avg2.rotate(-1)
                    moving_avg2[9] = row[2]
                    inputBin(getAvg(moving_avg2))
                except:
                    print 'nothing in col 2'
                try:
                    moving_avg3.rotate(-1)
                    moving_avg3[9] = row[3]
                    inputBin(getAvg(moving_avg3))
                except:
                    print 'nothing in col 3'
                try:
                    moving_avg4.rotate(-1)
                    moving_avg4[9] = row[4]
                    inputBin(getAvg(moving_avg4))
                except:
                    print 'nothing in col 4'
                try:
                    moving_avg5.rotate(-1)
                    moving_avg5[9] = row[5]
                    inputBin(getAvg(moving_avg5))
                except:
                    print 'nothing in col 5'
                try:
                    moving_avg6.rotate(-1)
                    moving_avg6[9] = row[6]
                    inputBin(getAvg(moving_avg6))
                except:
                    print 'nothing in col 6'
                try:
                    moving_avg7.rotate(-1)
                    moving_avg7[9] = row[7]
                    inputBin(getAvg(moving_avg7))
                except:
                    print 'nothing in col 7'
                try:
                    moving_avg8.rotate(-1)
                    moving_avg8[9] = row[8]
                    inputBin(getAvg(moving_avg8))
                except:
                    print 'nothing in col 8'
                try:
                    moving_avg9.rotate(-1)
                    moving_avg9[9] = row[9]
                    inputBin(getAvg(moving_avg9))
                except:
                    print 'nothing in col 9'
                try:
                    moving_avg10.rotate(-1)
                    moving_avg10[9] = row[10]
                    inputBin(getAvg(moving_avg10))
                except:
                    print 'nothing in col 10'
                input_str.append(str(row_count))
                
                if(getAvg(moving_avg) != -1): #
                    input_str.append(str(getAvg(moving_avg)))
                if(getAvg(moving_avg2) != -1):
                    input_str.append(str(getAvg(moving_avg2)))
                if(getAvg(moving_avg3) != -1):
                    input_str.append(str(getAvg(moving_avg3)))
                if(getAvg(moving_avg4) != -1):
                    input_str.append(str(getAvg(moving_avg4)))
                if(getAvg(moving_avg5) != -1):
                    input_str.append(str(getAvg(moving_avg5)))
                if(getAvg(moving_avg6) != -1):
                    input_str.append(str(getAvg(moving_avg6)))
                if(getAvg(moving_avg7) != -1):
                    input_str.append(str(getAvg(moving_avg7)))
                if(getAvg(moving_avg8) != -1):
                    input_str.append(str(getAvg(moving_avg8)))
                if(getAvg(moving_avg9) != -1):
                    input_str.append(str(getAvg(moving_avg9)))
                if(getAvg(moving_avg10) != -1):
                    input_str.append(str(getAvg(moving_avg10)))    
                myWriter.writerow(input_str)
                input_str = []
                row_count = row_count + 1
                
            else:
                print str(BIN1) + ' ' + str(BIN2) + ' ' + str(BIN3) + ' ' + str(BIN4) + ' ' + str(BIN5) + ' ' + str(BIN6)
                break
            
with open('bin.csv', 'wb') as binfile:
    mybin = csv.writer(binfile, delimiter=',')
    mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
    mybin.writerow([str(averageSum(BIN1, bin1_count)), str(averageSum(BIN2, bin2_count)), str(averageSum(BIN3, bin3_count)), str(averageSum(BIN4, bin4_count)), str(averageSum(BIN5, bin5_count)), str(averageSum(BIN6, bin6_count))])
    print str(averageSum(BIN1, bin1_count)) + ' ' + str(averageSum(BIN2, bin2_count)) + ' ' + str(averageSum(BIN3, bin3_count)) + ' ' + str(averageSum(BIN4, bin4_count)) + ' ' + str(averageSum(BIN5, bin5_count)) + ' ' + str(averageSum(BIN6, bin6_count))
