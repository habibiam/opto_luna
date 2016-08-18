'''
Created on Aug 4, 2016

@author: Xianguang Yan
'''
from __future__ import division
from collections import deque

#Bin Boundries
BIN1_LOWER = 512.0
BIN1_UPPER = 532.0
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

#Sets Bin Boundries
def setNum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12):
    global BIN1_LOWER, BIN1_UPPER, BIN2_LOWER, BIN2_UPPER, BIN3_LOWER, BIN3_UPPER, BIN4_LOWER, BIN4_UPPER, BIN5_LOWER, BIN5_UPPER, BIN6_LOWER, BIN6_UPPER
    BIN1_LOWER = a1
    BIN1_UPPER = a2
    BIN2_LOWER = a3
    BIN2_UPPER = a4
    BIN3_LOWER = a5
    BIN3_UPPER = a6
    BIN4_LOWER = a7
    BIN4_UPPER = a8
    BIN5_LOWER = a9
    BIN5_UPPER = a10
    BIN6_LOWER = a11
    BIN6_UPPER = a12

#checks if its a real number    
def checkNum(number):
    try:
        if float(number) > 0 and float(number) < 2000:
            return float(number)
    except:
        return 0

#check if bin is excess or real (Not really needed, but just "in case")
def checkCol(csvFile):
    if csvFile.bin_1 <= 0 and csvFile.bin_2 <= 0 and csvFile.bin_3 <= 0 and csvFile.bin_4 <= 0 and csvFile.bin_5 <= 0 and csvFile.bin_6 <= 0:
        return False

    else:
        return True

#format of the row in an array, this is how csv file takes inputs to be written
def getArray(csvFile):
    return [str(averageSum(csvFile.bin_1, csvFile.count_1)), str(averageSum(csvFile.bin_2, csvFile.count_2)), str(averageSum(csvFile.bin_3, csvFile.count_3)), str(averageSum(csvFile.bin_4, csvFile.count_4)), str(averageSum(csvFile.bin_5, csvFile.count_5)), str(averageSum(csvFile.bin_6, csvFile.count_6))]

#Figures out which bin to input in, and takes the number and inputs it into the csv class
def inputBin(col, number, csvFile):
    if   col >= BIN1_LOWER and col <= BIN1_UPPER:
        csvFile.addBin1(number)
    elif col >= BIN2_LOWER and col <= BIN2_UPPER:
        csvFile.addBin2(number)
    elif col >= BIN3_LOWER and col <= BIN3_UPPER:
        csvFile.addBin3(number)           
    elif col >= BIN4_LOWER and col <= BIN4_UPPER:
        csvFile.addBin4(number)
    elif col >= BIN5_LOWER and col <= BIN5_UPPER:
        csvFile.addBin5(number)
    elif col >= BIN6_LOWER and col <= BIN6_UPPER:
        csvFile.addBin6(number)
                
#gets the average of 10 numbers for moving average
def getAvg(l):
    try:
        sum = int(l[0]) + int(l[1]) + int(l[2]) + int(l[3]) + int(l[4]) + int(l[5]) + int(l[6]) + int(l[7]) + int(l[8]) + int(l[9])
        #sum = float(l[0]) + float(l[1]) + float(l[2]) + float(l[3]) + float(l[4]) + float(l[5]) + float(l[6]) + float(l[7]) + float(l[8]) + float(l[9])
        sum = sum/10.000
        if sum == 0:
            return -1
        else:
            return sum
    except:
        return -1

#gets total average
def averageSum(input, amount):
    if amount != 0:
        return input/amount
    else:
        return 0

#csv class
class CSVClass:
    #Variables
    def __init__(self):
        self.bin_1 = 0
        self.bin_2 = 0
        self.bin_3 = 0
        self.bin_4 = 0
        self.bin_5 = 0
        self.bin_6 = 0
        self.count_1 = 0
        self.count_2 = 0
        self.count_3 = 0
        self.count_4 = 0
        self.count_5 = 0
        self.count_6 = 0
        self.moving_avg = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    #rotate values to put new values in    
    def rotate(self, input):
        try:
            self.moving_avg.rotate(-1)
            self.moving_avg[9] = input
        except:
            print 'Error Rotating input'
    
    #return value    
    def getMovingAvg(self):
        return self.moving_avg
    
    #Rest is short Functions ++ Functions
    def addBin1(self, bin_1):
        self.bin_1 = self.bin_1 + bin_1
        self.count_1 = self.count_1 + 1
        
    def addBin2(self, bin_2):
        self.bin_2 = self.bin_2 + bin_2
        self.count_2 = self.count_2 + 1
        
    def addBin3(self, bin_3):
        self.bin_3 = self.bin_3 + bin_3
        self.count_3 = self.count_3 + 1
        
    def addBin4(self, bin_4):
        self.bin_4 = self.bin_4 + bin_4
        self.count_4 = self.count_4 + 1
        
    def addBin5(self, bin_5):
        self.bin_5 = self.bin_5 + bin_5
        self.count_5 = self.count_5 + 1
        
    def addBin6(self, bin_6):
        self.bin_6 = self.bin_6 + bin_6
        self.count_6 = self.count_6 + 1
