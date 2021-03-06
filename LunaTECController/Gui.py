# -*- coding: utf-8 -*-
'''
Created on Aug 18, 2016

@author: Xianguang Yan

Description: This python file sets the interface of the GUI and opens the port

'''

from Tkinter import *
from time import sleep
from serial import *
from CheckSerial import *
from Function import *

#Global Variables
luna = Tk()
luna.wm_title("GUI TEC CONTROLLER v1.0")
input = serial.Serial()

#Sets up the class to pass in paramaters from the user input
class TECParamaters():
    def __init__(self):
        self.entry = 0
        self.kp = 0
        self.kd = 0
        self.ki = 0
        self.ts = 0
        self.vol = 0
        self.temp = 0
        self.step1_temp = 0
        self.step1_time = 0
        self.step2_temp = 0
        self.step2_time = 0   
        self.step3_temp = 0
        self.step3_time = 0

#Functions
"""
Description: Sets up the default values to talk to the com port, this is set for windows. Throws
    an exception if there was an error opening port.
Input: None
Return: None
"""
def connectBtn():
    try:
        input.port = variable_port.get()
        input.baudrate = 115200
        input.stopbits = STOPBITS_ONE
        input.parity = PARITY_NONE
        input.writeTimeout = 1
        input.timeout = 1
        input.open()
        input.close()
        print "Success Opening Port"
    except EXCEPTION, e1:
        print 'Error Opening Port' + str(e1)
        
"""
Description: This function sets the display temperature on the gui
Input: Value of temperature can be an int or float
Return: None
"""

def updateTime(number):
    cur_temp.set(str(number))
    luna.update()

"""
Description: Gets all the paramters from the entry fields of the GUI and stores it in "tecPara". Then passes it into the pidFunction
#Note: Work in Progress
Input: None
Return: None
"""

def runStep():
    tecPara = TECParamaters
    count = 0
    checkpoint = False
    checkpointVal = int(check_entry.get())
    #SETUP AND CHECK FOR ENTRY IF VALID NUMBER
    try:
        tecPara.entry = int(check_entry.get())
        tecPara.kd = float(kd_entry.get())
        tecPara.kp = float(kp_entry.get())
        tecPara.ki = float(ki_entry.get())
        tecPara.ts = float(ts_entry.get())
        tecPara.vol = float(vol_entry.get())
        tecPara.temp = float(idle_temp_entry.get())
        tecPara.step1_temp = float(step1_temp_entry.get())
        tecPara.step1_time = float(step1_time_entry.get())
        tecPara.step2_temp = float(step2_temp_entry.get())
        tecPara.step2_time = float(step2_time_entry.get())
        tecPara.step3_temp = float(step3_temp_entry.get())
        tecPara.step3_time = float(step3_time_entry.get())
        checkpoint = True        

    except:
        print 'One or more entries are incorrect.'
    if int(check_entry.get()) > 0 and checkpoint:
        while count < checkpointVal:
            count += 1
            #pidFunc(step1)
            
"""
Description: A test Function that executes one single command, will return an error if failed to send due to com port issue. If so, please initialize the port before sending
Input: None
Return: None
"""    
def defaultRun():
    try:
        input.close()
        input.open()
        input.write(get_command('10','00c8')) #get command takes in "command"(2bytes), and then "Value" (8bytes)
        print input.readline()
        input.close()
        print "Executed"
    except Exception, e1:
        input.close()
        print "ERROR SENDING VALUE" + str(e1)
        
"""
Description: Enables output, I would run this just in case, if the command returns 1 in its value then it is enabled, "0000" is disable. Discription is taken from the manual.
Input: None
Return: None
"""

def outputEnable():
    try:
        input.close()
        input.open()
        input.write(get_command('24',"0001"))
        print input.readline()
        input.close()
        print "Executed"
    except EXCEPTION, e1:
        input.close()
        print "Error Enabling Output" + str(e1)
            
#String Variable lables for the GUI
cur_temp = StringVar()
idle_temp_label = Label(luna, text = "IDLE Temperature").grid(row = 2, column = 0)
step1_label = Label(luna, text = "STEP 1: ").grid(row = 5, column = 0)
step2_label = Label(luna, text = "STEP 2: ").grid(row = 6, column = 0)
step3_label = Label(luna, text = "STEP 3: ").grid(row = 7, column = 0)
check_label = Label(luna, text = "Check Number: ").grid(row = 8, column = 0)
gains_label = Label(luna, text = "Gains Values").grid(row = 2, column  = 6)
xx_xx = Label(luna, text = "").grid(row = 1)
kp_label = Label(luna, text = "  KP: ").grid(row = 3, column = 5)
kd_label = Label(luna, text = "  KD: ").grid(row = 4, column = 5)
ki_label = Label(luna, text = "  KI: ").grid(row = 5, column = 5)
ts_label = Label(luna, text = "  TS: ").grid(row = 6, column = 5)
vol_label = Label(luna, text = "  Volume: ").grid(row = 7, column = 5)
step1_degree_label = Label(luna, text = "°F    ").grid(row = 5, column = 4)
step2_degree_label = Label(luna, text = "°F    ").grid(row = 6, column = 4)
step3_degree_label = Label(luna, text = "°F    ").grid(row = 7, column = 4)
step1_seconds_label = Label(luna, text = "Seconds").grid(row = 5, column = 2)
step2_seconds_label = Label(luna, text = "Seconds").grid(row = 6, column = 2)
step3_seconds_label = Label(luna, text = "Seconds").grid(row = 7, column = 2)
cur_temp_label = Label(luna, text = "Current Temperature: ").grid(row = 0, column = 6)
cur_temp_dynamic_label = Label(luna, textvariable = cur_temp).grid(row = 0, column = 7)
cur_label_label = Label(luna, text = "°F").grid(row = 0, column = 8)

#Entry Labels For the GUI
idle_temp_entry = Entry(luna, justify = CENTER)
step1_temp_entry = Entry(luna, justify = CENTER, width = 7)
step2_temp_entry = Entry(luna, justify = CENTER, width = 7)
step3_temp_entry = Entry(luna, justify = CENTER, width = 7)
kp_entry = Entry(luna, justify = CENTER)
kd_entry = Entry(luna, justify = CENTER)
ki_entry = Entry(luna, justify = CENTER)
ts_entry = Entry(luna, justify = CENTER)
vol_entry = Entry(luna, justify = CENTER)
check_entry = Entry(luna, justify = CENTER, width = 7)

idle_temp_entry.grid(row = 3, column = 0)
step1_temp_entry.grid(row = 5, column = 3)
step2_temp_entry.grid(row = 6, column = 3)
step3_temp_entry.grid(row = 7, column = 3)  
check_entry.grid(row = 8, column = 1)
kp_entry.grid(row = 3, column = 6)
kd_entry.grid(row = 4, column = 6)
ki_entry.grid(row = 5, column = 6)
ts_entry.grid(row = 6, column = 6)
vol_entry.grid(row = 7, column = 6)

#Buttons For the GUI
port_connect = Button(luna, text = "Connect", command = connectBtn).grid (row = 0, column = 0)
step1_time_entry = Entry(luna, justify = CENTER, width = 7)
step2_time_entry = Entry(luna, justify = CENTER, width = 7)
step3_time_entry = Entry(luna, justify = CENTER, width = 7)
step3_time_entry.grid(row = 7, column = 1)
step2_time_entry.grid(row = 6, column = 1)
step1_time_entry.grid(row = 5, column = 1)
run_btn = Button(luna, text = "Run", command = runStep).grid(row = 9, column = 0)
test_btn = Button(luna, text = "Test Run", command = defaultRun).grid(row = 9, column = 1)
output_enable_btn = Button (luna, text = "Output Enable", command = outputEnable).grid(row = 9, column = 2)

#List/Dropdown Menu for the GUI
port_list = serial_ports()
variable_port = StringVar(luna)
variable_port.set("None")
"""
When executing this python script it will try and find open ports, if there are no available ports, you must close and double check if there
is any connected ports. If no ports are found then there will be no dropdown menu to selected a port.
"""
try:
    coms_list = apply(OptionMenu, (luna, variable_port) + tuple(port_list))
    coms_list.grid(row = 0, column = 2)
except:
    print 'Error Finding Ports No Ports Found'
    
luna.mainloop()
