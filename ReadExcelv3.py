'''
Created on Aug 4, 2016

@author: Xianguang Yan

@purpose: A GUI Interface that is used to take a large chunk of scans and parse it into bins

'''
from function import *
from collections import deque
import csv
from Tkinter import *
import matplotlib.pyplot as plt

#Global Variables
top = Tk()

#Graphs The bins once you press Graph
def Graph():
    #variables
    plt.close()
    time = .5
    count_val = 0
    x_axis = []
    ybin1 = []
    ybin2 = []
    ybin3 = []
    ybin4 = []
    ybin5 = []
    ybin6 = []
    count = True
    
    #read from bin and gets plot
    with open('bin.csv', 'rb') as csvfile:
        myReader = csv.reader(csvfile, delimiter = ',')
        for row in myReader:
            if count:
                count = False
            else:
                count_val = count_val + time
                x_axis.append(count_val)
                print x_axis
                ybin1.append(row[0])
                ybin2.append(row[1])
                ybin3.append(row[2])
                ybin4.append(row[3])
                ybin5.append(row[4])
                ybin6.append(row[5])
                print ybin1, ybin2, ybin3, ybin4, ybin5, ybin6
               
                
    #plots the data
    plt.plot(x_axis, ybin1, color = 'red', label = 'Bin 1')
    plt.plot(x_axis, ybin2, color = 'blue', label = 'Bin 2')                
    plt.plot(x_axis, ybin3, color = 'yellow', label = 'Bin 3')
    plt.plot(x_axis, ybin4, color = 'green', label = 'Bin 4') 
    plt.plot(x_axis, ybin5, color = 'orange', label = 'Bin 5')
    plt.plot(x_axis, ybin6, color = 'purple', label = 'Bin 6')
    
    #x and y labels
    plt.xlabel('Time (ms)')
    plt.ylabel('Bin Value')
    plt.title('Welcome To My Graph')
    plt.legend()
    
    plt.show()
    
#Main Code that does Moving Average    
def RunCode():
    
    global bin1_l
    row_count = -1.0
    input_str = []
    columns = list()
    col_count = 0
    create_list = True
    file_name = ""
    try:
        #Open CSV and read Moving Average
        setNum(checkNum(bin1_l.get()), checkNum(bin1_u.get()), checkNum(bin2_l.get()), checkNum(bin2_u.get), checkNum(bin3_l.get()), checkNum(bin3_u.get()), checkNum(bin4_l.get()), checkNum(bin4_u.get()), checkNum(bin5_l.get()), checkNum(bin5_u.get()), checkNum(bin6_l.get()), checkNum(bin6_u.get()))
        with open('results.csv', 'wb') as resultsfile:
            myWriter = csv.writer(resultsfile, delimiter=',')
            first_line = [] #write the header/description
            with open(str(file_input_label.get()), 'rb') as csvfile:
                myReader= csv.reader(csvfile, delimiter=',')
                for row in myReader:  #Goes through every line in the test file
                    if row_count == -1: #Get Lines Until Pixel Starts
                        for x in range(len(row)):
                            try:
                                if len(row[x]) != 0 and row[0] != 0:
        
                                    row_count = float(row[0])   #starts pixel count
                                    col_count = col_count + 1
                            except:                    #tests for words or headers and prints them back into results
                                print row[x]
                                first_line.append(row[x]) #Means its junk data so just store it like it is
                        myWriter.writerow(first_line)
                        first_line = []
                        
                    elif create_list: #creates the list once
                        columns = [CSVClass() for i in range(col_count)]
                        create_list = False
                        
                    elif row_count < 490: # Do nothing from 0 - 490
                        
                        row_count = float(row[0])
                        
                    elif row_count >= 490 and row_count < 500: #Sets Up Moving Average Algorithim (Note not a true "Moving Average") If want true must imput + 5 to columns[0 + 5]
                        print columns[0].getMovingAvg()
                        for i in range(col_count):
                            try:
                                columns[i].rotate(row[i + 1])
                            except:
                                continue
                        row_count = float(row[0]) #checks current pixels
                      
                    elif (row_count >= 500) and (row_count <= 1500): #Does Everything here and Writes it into the file called "results.csv"
            
                        for i in range(col_count):
                            try:
                                columns[i].rotate(row[i + 1])
                                inputBin(row_count, getAvg(columns[i].getMovingAvg()), columns[i])
                            except:
                                continue
                            
                                    
                        #Appends Pixel Number
                        input_str.append(str(row_count))
                        for i in range(col_count): 
                            if(getAvg(columns[i].getMovingAvg()) != -1): 
                                input_str.append(str(getAvg(columns[i].getMovingAvg())))
                        #write Row
                        myWriter.writerow(input_str)
                        print input_str
                        input_str = []
                        row_count = row_count + 1
                        
                        
                    else:
                        break
                    
        #Once Data is Gathered Writes the Bin to the Bin Folder            
        with open('bin.csv', 'wb') as binfile:
            mybin = csv.writer(binfile, delimiter=',')
            #Write Bin
            mybin.writerow(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6'])
            for i in range(col_count):
                if (checkCol(columns[i])):  #Saftey Check
                    mybin.writerow(getArray(columns[i]))
                    print getArray(columns[i])

    except EXCEPTION:
        print "error"  
        print str(file_input_label.get())  

###############
#GUI INTERFACE#
###############

top.wm_title("Program Bin V1.0 Created by Xianguang Yan")

#Labels
upper_label = Label(top, text = "Upper Parameter").grid(row = 0, column = 2)
lower_label = Label(top, text = "Lower Parameter").grid(row = 0, column = 1)
bin_label = Label(top, text = "Bins Number").grid(row = 0, column = 0)
bin1_label = Label(top, text = "Bin 1: ").grid(row = 1, column = 0)
bin2_label = Label(top, text = "Bin 2: ").grid(row = 2, column = 0)
bin3_label = Label(top, text = "Bin 3: ").grid(row = 3, column = 0)
bin4_label = Label(top, text = "Bin 4: ").grid(row = 4, column = 0)
bin5_label = Label(top, text = "Bin 5: ").grid(row = 5, column = 0)
bin6_label = Label(top, text = "Bin 6: ").grid(row = 6, column = 0)
file_label = Label(top, text = "CSV FILE NAME: ").grid(row = 7, column = 0)

#Entry
bin1_l = Entry(top, justify = CENTER)
bin1_l.grid(row = 1, column = 1)
bin1_u = Entry(top, justify = CENTER)
bin1_u.grid(row = 1, column = 2)
bin2_l = Entry(top, justify = CENTER)
bin2_l.grid(row = 2, column = 1)
bin2_u = Entry(top, justify = CENTER)
bin2_u.grid(row = 2, column = 2)
bin3_l = Entry(top, justify = CENTER)
bin3_l.grid(row = 3, column = 1)
bin3_u = Entry(top, justify = CENTER)
bin3_u.grid(row = 3, column = 2)
bin4_l = Entry(top, justify = CENTER)
bin4_l.grid(row = 4, column = 1)
bin4_u = Entry(top, justify = CENTER)
bin4_u.grid(row = 4, column = 2)
bin5_l = Entry(top, justify = CENTER)
bin5_l.grid(row = 5, column = 1)
bin5_u = Entry(top, justify = CENTER)
bin5_u.grid(row = 5, column = 2)
bin6_l = Entry(top, justify = CENTER)
bin6_l.grid(row = 6, column = 1)
bin6_u = Entry(top, justify = CENTER)
bin6_u.grid(row = 6, column = 2)


file_input_label = Entry(top, justify = CENTER)
file_input_label.grid(row = 7, column = 1)


#Button
run_btn = Button(top, text = 'RUN', command = RunCode, width = 10).grid(row = 7, column = 2)
graph_btn = Button(top, text = 'GRAPH', command = Graph, width = 10).grid(row = 8, column = 2)

top.mainloop()
                  
   