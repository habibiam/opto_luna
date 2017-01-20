#!/usr/bin/python
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import time
import atexit
import sys
import RPi.GPIO as GPIO, os
import spidev
import json
import serial
from xyz_motor import xyz_motor

import DAQCplate as DAC
from threading import Thread
import piplates.RELAYplate as RELAY

I2C60 = 1
I2C61 = 0
I2C62 = 2
I2C63 = 3
FASTSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
FULLSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
MICROSTEP = 4  # This is 16 micro step per full step mode, use to precise position or for pumping slowly
DOUBLESTEP = 2 # Wei

LOWCUR = 1  # lowest current setting is 1, max is 16
MIDCUR = 2  # medium current setting is 2, max is 16
HIGHCUR = 4  # high current setting is 3, max is 16
LASCUR = 3 #4
REAGENTCUR = 4
GELCUR = 2
XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
NEGDIR = -1  # Negative move direction
POSDIR = 1  # Positive move direction
from constant import Home_AD_ave

class Read_AD:
    def __init__(self):
        self._running = True
        self.ave_on = True

    def terminate(self):
        self._running = False

    def GelPumpReadAD_Enable(self):
        self.ave_on = True
        while self.ave_on:
            #print "Reading ADC 7 1 for Gel Pump Start sensor"
            temp = 0.0
            AD_ave = 0.0
            good_count = 8
            for cycle in range(1, 9):
                temp = DAC.getADC(7, 1)
                time.sleep(.001)
                if (temp > 4.1 or temp < 0.13):
                    temp = 0  # Ignore bad reads
                    good_count = good_count - 1
                    # reduce ave count to make up for bad data
                AD_ave = AD_ave + temp
            if (good_count == 0): good_count = 1
            Home_AD_ave = (AD_ave / good_count)
            #print "H_AD_Ave and gd8=", Home_AD_ave, good_count

    def GelPumpReadAD_Disable(self):
        self.ave_on = False

    def move_gelPump_home(self):
        print  "Moving Gel Pump to the upper home switch "
        print "Completed Gel Pump move to Home switch"
        print  GelPos
        if ((DAC.getDINbit(7, 0) == 1)):  # if home switch is active, reset GelPos
            print "Input DAC(7,0) Gel Home sensor is active high"
            print  GelPos
            GelPos = 0

    def move_gelPump_start(self):

        target_motor = xyz_motor(1, 200, 100)
        HomeMax = 123800
        GelPos = 0
        temp = 0
        print "Waiting for DAC addr7 Analog input 2 (index start at 0) Gel Start switch to become Active "

        for cycle in range(1, 3):
            temp = DAC.getADC(7, 1)
            #print temp
            time.sleep(.001)
            if (temp == 0):  # if home switch is active, print complete message
                print "Input DAC Analog input(7,1) Gel Start sensor is already active low, moving up to get off top"
                target_motor.move(POSDIR, 10, DOUBLESTEP, GELCUR)

        ave = 5.0
        while ((ave >= 0.8) and (GelPos < HomeMax)):  # if gel start switch not active, move 9 step
            temp = 0.0
            ave = 0.0
            good_count = 8
            for cycle in range(1, 9):
                temp = DAC.getADC(7, 1)
                time.sleep(.001)
                if (temp > 4.1 or temp < 0.3):
                    temp = 0  # Ignore bad reads
                    good_count = good_count - 1
                    # reduce ave count to make up for bad data
                ave = ave + temp
                print "temp=", temp
            if (good_count == 0): good_count = 1
            ave = (ave / good_count)
            #time.sleep(.001)
            #print "Ave and good_count = ", ave, good_count

            target_motor.move(NEGDIR, 10, DOUBLESTEP, GELCUR) #10
            GelPos = GelPos + 10

        print "Completed Gel Pump move to top of syring, steps moved =", GelPos
        temp = 0
        for cycle in range(1, 4):
            temp = (temp + DAC.getADC(7, 1))
            time.sleep(.001)
        print "Input Analog input(7,1) Gel Start sensor "
        print temp
        if (temp <= 5):  # if home switch is active, print complete message
            print "Input analog DAC(7,1) Gel Start sensor is now Active Low"
            print  GelPos
                 
