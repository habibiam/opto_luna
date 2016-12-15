#!/usr/bin/env python

"""
#Testing Script for All Directories
Created on June 15 15:25:01 2016

@author: Xianguang Yan

"""

import os
import csv
import sys
import func
import ctypes

from func import script, convertFSA
from os import *
from os.path import isdir, isfile, join

# this gets me Directory Path
mypath = os.path.dirname(os.path.abspath(__file__))

# gets folders (searches through them)
onlyFiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]
print 'ALL DIRECTORIES (FOLDERS) IN PARENT', onlyFiles
# create Directory for All CSV and Check if Already Exist
newFolder = 'CSV FOLDER'
destination = join(mypath, newFolder)
if not os.path.exists(destination):
    os.makedirs(destination)

print 'Destination CSV FOLDER: ' + destination

# check Testing
print mypath


# make sure there isn't a duplicate before converting
def checkFile(filePath):
    # checks to see if there is a file there with the same name
    if not os.path.exists(filePath):
        return True
    else:
        print '\n xxxxxxxxxxxxxxxxxx     SKIPPED     xxxxxxxxxxxxxxxxxxxxxxxx \n'
        return False


fileSize = len(onlyFiles)
count = 0;
countC = 0;
# Everything in Each Directory
for x in range(fileSize):
    newPath = join(mypath, onlyFiles[x])
    newFiles = [j for j in listdir(newPath) if isfile(join(newPath, j))]
    print newFiles
    # goes through each file to see if its a .fsa
    for fp in newFiles:
        ext = os.path.splitext(fp)[-1].lower()
        if ext == '.fsa':
            newFsa = join(newPath, fp)
            # check file
            if (checkFile(join(destination, convertFSA(fp)))):
                print 'Directory Passed in ' + newFsa
                print 'Destination passed in ' + destination
                print 'File name Passed in ' + fp
                print '-------------------------------------------------------------'
                print '--------------------- PARSING FSA ---------------------------'
                print '------------------   CREATING FILE  -------------------------'
                print '-------------------------------------------------------------'
                script(newFsa, destination, fp)
                countC += 1
            else:
                count += 1

print '------------------------------------------------------------------------'
print '-----------                  DONE                  ---------------------'
print '------------------------------------------------------------------------'
print 'NUMBER OF FSA FILES FOUND: ', x
print 'FILES CREATED: ', countC
print 'FILES SKPPED: ', count


# Debugger Test See
# def Mbox(title, text, style):
#     ctypes.windll.user32.MessageBoxA(0, text, title, style)


# Mbox('Converter for: .fsv to .csv', 'Done!'
#      + '\n\n' + 'Number of files Found:   ' + str(x)
#      + '\n' + 'Files Created:   ' + str(countC)
#      + '\n' + 'Files Skipped:   ' + str(count), 1)
