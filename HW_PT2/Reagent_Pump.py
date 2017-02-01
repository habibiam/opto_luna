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
FASTSTEP = 1       # This is Full Stepping mode, use to home motors at fastest speed
FULLSTEP = 1       # This is Full Stepping mode, use to home motors at fastest speed
MICROSTEP = 4      # This is 16 micro step per full step mode, use to precise position or for pumping slowly
DOUBLESTEP = 2     # Proved by Wei

LOWCUR = 1         # lowest current setting is 1, max is 16
MIDCUR = 2         # medium current setting is 2, max is 16
HIGHCUR = 4        # high current setting is 3, max is 16
LASCUR = 3         # 4
REAGENTCUR = 2     # 2: Proved by Ezra.
GELCUR = 2         # Proved by Ezra.
XZSTATIONCUR = 6   # optimal current to run the X and Z solution station
NEGDIR = -1        # Negative move direction
POSDIR = 1         # Positive move direction

"""
This class is created for motor/Syringe control in pump array.
"""

class Reagent_Pump:
    def __init__(self):
        self._running = True
        self.pumpLetter_to_address = { "M": 7, "P": 8, "W":9 , "S":10 }

    def terminate(self):
        self._running = False

    def move(self, motor_steps, pump_letter, move_up):
        """
        # TODO Need to find the conversion between microL and motor steps 
        """
        print "moving reagent pump " + pump_letter + "at " + str(motor_steps) + "motor steps"
        pump_address = self.pumpLetter_to_address[pump_letter]
        target_motor = xyz_motor(pump_address, 200, 100)
        atexit.register(target_motor.turn_off)
        if move_up == True: direction = NEGDIR
        elif move_up == False: direction = POSDIR
        target_motor.move(direction, motor_steps, DOUBLESTEP, REAGENTCUR)

    def Syringe1(self):
        target_motor = xyz_motor(7, 200, 300)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentMPos = 0
        temp = 0
        #while 1:
        RELAY.relayON(0,2)
        RELAY.relayON(0,3)
        time.sleep(1)
        target_motor.move(NEGDIR, 41100, DOUBLESTEP, REAGENTCUR) #MOVE UP
        RELAY.relayOFF(0,2)
        RELAY.relayOFF(0,3)
        time.sleep(1)
        target_motor.move(POSDIR, 41100, DOUBLESTEP, REAGENTCUR)  #MOVE DOWN
        time.sleep(2)
            
    def Syringe2(self):
        target_motor = xyz_motor(8, 200, 300)
        atexit.register(target_motor.turn_off)
        #while 1:
        RELAY.relayON(0,4)
        time.sleep(0.22)
        RELAY.relayON(0,5)
        time.sleep(1)
        target_motor.move(NEGDIR, 41100, DOUBLESTEP, REAGENTCUR) #MOVE UP 
        RELAY.relayOFF(0,4)
        time.sleep(0.22)
        RELAY.relayOFF(0,5)
        time.sleep(1)
        target_motor.move(POSDIR, 41100, DOUBLESTEP, REAGENTCUR)  #MOVE DOWN
        time.sleep(2)

    def Syringe3(self):
        target_motor = xyz_motor(9, 200, 300)
        atexit.register(target_motor.turn_off)
        #while 1:
        RELAY.relayON(0,6)
        time.sleep(0.22)
        RELAY.relayON(0,7)
        time.sleep(1)
        target_motor.move(NEGDIR, 41100, DOUBLESTEP, REAGENTCUR) #MOVE UP
        RELAY.relayOFF(0,6)
        time.sleep(0.22)
        RELAY.relayOFF(0,7)
        time.sleep(1)
        target_motor.move(POSDIR, 41100, DOUBLESTEP, REAGENTCUR)  #MOVE DOWN
        time.sleep(2)
            
    def Syringe4(self):
        target_motor = xyz_motor(10, 200, 300)
        atexit.register(target_motor.turn_off)
        #while 1:
        RELAY.relayON(1,2)
        time.sleep(0.22)
        RELAY.relayON(1,3)
        time.sleep(1)
        target_motor.move(NEGDIR, 41100, DOUBLESTEP, REAGENTCUR) #MOVE UP
        RELAY.relayOFF(1,2)
        time.sleep(0.22)
        RELAY.relayOFF(1,3)
        time.sleep(1)
        target_motor.move(POSDIR, 41100, DOUBLESTEP, REAGENTCUR)  #MOVE DOWN
        time.sleep(2)
           
    # This method is created to control reagent master in syringe 1.
    def move_reagentM_home(self):
        while 1:
            syringe1_thread = Thread(target = self.Syringe1)
            syringe1_thread.start()
            
            syringe2_thread = Thread(target = self.Syringe2)
            syringe2_thread.start()
            """
            syringe3_thread = Thread(target = self.Syringe3)
            syringe3_thread.start()
            syringe4_thread = Thread(target = self.Syringe4)
            syringe4_thread.start()
            """
            syringe1_thread.join()
            
            syringe2_thread.join()
            """
            syringe3_thread.join()
            syringe4_thread.join()
            """
            time.sleep(1)
        """
        print "Moving Reagent M Pump to the home switch "
        target_motor = xyz_motor(7, 200, 10000)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentMPos = 0
        temp = 0        
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 3)
            if ( temp > 0):
                 print "Input DAC(7,3) Home sensor is already active high"
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,3) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 10000, DOUBLESTEP, REAGENTCUR)  # Move DOWN 
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
            target_motor.move(POSDIR, 200, DOUBLESTEP, REAGENTCUR)  # Move UP to switch
            ReagentMPos = ReagentMPos + 1
        print "Completed ReagentMPos Pump move to Home switch"
        print  ReagentMPos
        if ((DAC.getDINbit(7, 3) == 1)):  # if home switch is active, reset ReagentMPos
            print "Input DAC(7,3) ReagentMPos Home sensor is active high"
            print  ReagentMPos
            ReagentMPos = 0
         """
    def move_reagentP_home(self):

        print  "Moving Reagent P Pump to the home switch "
        target_motor = xyz_motor(8, 200, 1600)
        atexit.register(target_motor.turn_off)
        HomeMax = 23800
        ReagentPPos = 0
        temp = 0
        target_motor.move(NEGDIR, 41000, DOUBLESTEP, REAGENTCUR) #MOVE UP
        target_motor.move(POSDIR, 41000, DOUBLESTEP, REAGENTCUR)  #MOVE DOWN
        """
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 4)
            time.sleep(.0001)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,4) Home sensor is already active high, moving up 2000"
            target_motor.move(NEGDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move up 
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
            target_motor.move(POSDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move down to switch
            ReagentPPos = ReagentPPos + 1
        print "Completed ReagentPPos Pump move to Home switch"
        print  ReagentPPos
        if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentPPos
            print "Input DAC(7,4) ReagentPPos Home sensor is active high"
            print  ReagentPPos
            ReagentPPos = 0
        """
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
