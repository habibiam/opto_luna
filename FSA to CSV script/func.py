"""
Created on June 15 15:25:01 2016

@author: Xianguang yan

"""
import csv
import sys
import os

from ABIFReader import *
from os.path import isdir, isfile, join


# runs the translation script
# Converts name field .FSA -> .CSV
def convertFSA(fileName):
    csvList = fileName.split('.')
    csvList[1] = '.csv'
    return ''.join(csvList)


# Converts Data FSA -> CSV
def script(directory, destination, name):
    reader3 = ABIFReader(directory)
    data = [reader3.getData('DATA', 1), reader3.getData('DATA', 2), reader3.getData('DATA', 3),
            reader3.getData('DATA', 4), reader3.getData('DATA', 105)]
    csvName = convertFSA(name)
    print 'Created this file: ' + csvName
    print 'Got Data...'
    print 'Writing Data...'
    print 'Data directory with csv file: ' + destination
    os.chdir(destination)
    print csvName

    # Writes To Destination
    with open(csvName, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Blue', 'Green', 'Yellow', 'Red', 'Orange'])
        writer.writerows(zip(*data))
