# -*- coding: utf-8 -*-
'''
Created on Aug 18, 2016

@author: Xianguang Yan
'''

from Tkinter import *
from time import sleep

#Global
#GUI
luna = Tk()
luna.wm_title("GUI TEC CONTROLLER v1.0")

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
#REFRESH FRAME
def updateTime(number):
    cur_temp.set(str(number))
    luna.update()

#RUNS PID FUNCTION
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
    
    

#labels
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
cur_temp_label = Label(luna, text = "Current Temperature: ").grid(row = 0, column = 6)
cur_temp_dynamic_label = Label(luna, textvariable = cur_temp).grid(row = 0, column = 7)
cur_label_label = Label(luna, text = "°F").grid(row = 0, column = 8)

#Entry
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

#Buttons
port_connect = Button(luna, text = "Connect").grid (row = 0, column = 0)
step1_time_entry = Entry(luna, justify = CENTER, width = 7)
step2_time_entry = Entry(luna, justify = CENTER, width = 7)
step3_time_entry = Entry(luna, justify = CENTER, width = 7)
step3_time_entry.grid(row = 7, column = 1)
step2_time_entry.grid(row = 6, column = 1)
step1_time_entry.grid(row = 5, column = 1)
run_btn = Button(luna, text = "Run", command = runStep).grid(row = 9, column = 0)
#List

luna.mainloop()
