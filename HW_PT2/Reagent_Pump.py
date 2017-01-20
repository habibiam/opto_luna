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

class Reagent_Pump:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def move_reagentM_home(self):
        print "Moving Reagent M Pump to the home switch "
        target_motor = xyz_motor(7, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentMPos = 0
        temp = 0
        target_motor.move(NEGDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move up 
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 3)
            if ( temp > 0):
                 print "Input DAC(7,3) Home sensor is already active high"
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,3) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 3)
            if ( temp >= 1):
                 print "Input DAC(7,3) Home sensor is already active high"
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 3 Home switch to become Active "
        while ((temp == 0) and (ReagentMPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 3)
                if ( temp > 0):
                    print "Input DAC(7,3) Home sensor is already active high"
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentMPos = ReagentMPos + 50
        print "Completed ReagentMPos Pump move to Home switch"
        print  ReagentMPos
        if ((DAC.getDINbit(7, 3) == 1)):  # if home switch is active, reset ReagentMPos
            print "Input DAC(7,3) ReagentMPos Home sensor is active high"
            print  ReagentMPos
            ReagentMPos = 0

    def move_reagentP_home(self):

        print  "Moving Reagent P Pump to the home switch "
        target_motor = xyz_motor(8, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentPPos = 0
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 4)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,4) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 4)
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 4 Home switch to become Active "
        while ((temp == 0) and (ReagentPPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 4)
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentPPos = ReagentPPos + 1
        print "Completed ReagentPPos Pump move to Home switch"
        print  ReagentPPos
        if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentPPos
            print "Input DAC(7,4) ReagentPPos Home sensor is active high"
            print  ReagentPPos
            ReagentPPos = 0

    def move_reagentW_home(self):
        print  "Moving Reagent W Pump to the home switch "
        target_motor = xyz_motor(9, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentWPos = 0
        temp = 0
        target_motor.move(NEGDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move up 
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 5)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,5) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 5)
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 5 Home switch to become Active "
        while ((temp == 0) and (ReagentWPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 5)
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentWPos = ReagentWPos + 50
        print "Completed ReagentWPos Pump move to Home switch"
        print  ReagentWPos
        if ((DAC.getDINbit(7, 5) == 1)):  # if home switch is active, reset ReagentWPos
            print "Input DAC(7,5) ReagentWPos Home sensor is active high"
            print  ReagentWPos
            ReagentWPos = 0

    def move_reagentS_home(self):
        print  "Moving Reagent S Pump to the home switch "
        target_motor = xyz_motor(10, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentSPos = 0
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 6)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,6) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 6)
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 6 Home switch to become Active "
        print  "Moving Reagent S Pump to the home switch, input 6 "
        while ((temp == 0) and (ReagentSPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 6)
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentSPos
                print "Input DAC(7,6) ReagentSPos Home sensor is active high"
            ReagentSPos = ReagentSPos + 1
        print "Completed ReagentSPos Pump move to Home switch"
        print  ReagentSPos
        if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentSPos
            print "Input DAC(7,6) ReagentSPos Home sensor is active high"
            print  ReagentSPos
            ReagentSPos = 0

    def move_reagentE_home(self):
        print  "Moving Reagent E Pump to the home switch "
        target_motor = xyz_motor(11, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentEPos = 0
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 7)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,7) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 7)
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 7 Home switch to become Active "
        while ((temp == 0) and (ReagentEPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentEPos = ReagentEPos + 1
        print "Completed ReagentEPos Pump move to Home switch"
        print  ReagentEPos
        if ((DAC.getDINbit(7, 7) == 1)):  # if home switch is active, reset ReagentEPos
            print "Input DAC(7,7) ReagentEPos Home sensor is active high"
            print  ReagentEPos
            ReagentEPos = 0

    def move_reagentB_home(self):
        print  "Moving Reagent B Pump to the home switch "
        target_motor = xyz_motor(12, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 18000
        ReagentBPos = 0
        temp = 0
        target_motor.move(NEGDIR, 8000, DOUBLESTEP, REAGENTCUR)  # Move up 
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 8)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,8) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 8)
            time.sleep(.0001)
        print "Starting Home, for DAC addr7 input 8 Home switch to become Active "
        while ((temp == 0) and (ReagentBPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 8)
                time.sleep(.0001)
            target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentBPos = ReagentBPos + 50
        print "Completed ReagentBPos Pump move to Home switch"
        print  ReagentBPos
        if ((DAC.getDINbit(7, 8) == 1)):  # if home switch is active, reset ReagentBPos
            print "Input DAC(7,8) ReagentBPos Home sensor is active high"
            print  ReagentBPos
            ReagentBPos = 0
