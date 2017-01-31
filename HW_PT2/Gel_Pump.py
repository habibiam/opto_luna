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

class Gel_Pump:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def move_gel_pump_up(self):
        
        """
        LOWCUR = 1  # lowest current setting is 1, max is 16
        MIDCUR = 2  # medium current setting is 2, max is 16
        HIGHCUR = 4  # high current setting is 3, max is 16
        XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
        NEGDIR = -1  # Negative move direction
        POSDIR = 1  # Positive move direction

        """
        print "Moving Gel pump up"
        target_motor = xyz_motor(1, 200, 100)
        atexit.register(target_motor.turn_off)
        min = 2.0
        run_once = False
        t_end = time.time() + 60 * min
        while time.time() < t_end:
            target_motor.move(POSDIR, 1, DOUBLESTEP, HIGHCUR)
            time.sleep(0.005)
            if (run_once): break
        print "finished"
        port.write("GP Done\n")

    def move_gel_pump_down(self):
        print "Moving Gel pump down"
        target_motor = xyz_motor(1, 200, 100)
        atexit.register(target_motor.turn_off)
        min = 2.0
        run_once = False
        t_end = time.time() + 60 * min
        while time.time() < t_end:
            target_motor.move(NEGDIR, 1, DOUBLESTEP, HIGHCUR)
            time.sleep(0.02)
            time.sleep(2.00)
            if (run_once): break
        print "finished"
        port.write("GP Done\n")

    def move_gelPump_home(self):
        print  "Moving Gel Pump to the upper home switch "
        target_motor = xyz_motor(1, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 123800
        GelPos = 0
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 0)
            time.sleep(.01)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,0) Home sensor is already active high, moving down 400 first"
            target_motor.move(NEGDIR, 400, DOUBLESTEP, GELCUR)
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 0)
            time.sleep(.001)
        print "Starting Home, for DAC addr7 input 0 Gel Home switch to become Active "
        while ((temp == 0) and (GelPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 0)
                time.sleep(.001)
            target_motor.move(POSDIR, 10, DOUBLESTEP, GELCUR)
            GelPos = GelPos + 1
        print "Completed Gel Pump move to Home switch"
        print  GelPos
        if ((DAC.getDINbit(7, 0) == 1)):  # if home switch is active, reset GelPos
            print "Input DAC(7,0) Gel Home sensor is active high"
            print  GelPos
            GelPos = 0

    def move_gelPump_start(self):
        '''
        target_motor = xyz_motor(1, 200, 100)
        target_motor.move(POSDIR, 2000, DOUBLESTEP, GELCUR) #Up
        target_motor.move(NEGDIR, 2000, DOUBLESTEP, GELCUR) #Dn
        target_motor.move(POSDIR, 8000, MICROSTEP, GELCUR) #Up
        target_motor.move(NEGDIR, 8000, MICROSTEP, GELCUR) #Dn
        time.sleep(2.0)
        '''
        
        target_motor = xyz_motor(1, 200, 100)
        HomeMax = 123800
        GelPos = 0
        temp = 0
        print "Waiting for DAC addr7 Analog input 2 (index start at 0) Gel Start switch to become Active "

        for cycle in range(1, 3):
            temp = DAC.getADC(7, 1)
            print temp
            time.sleep(.02)
            if (temp == 0):  # if home switch is active, print complete message
                print "Input DAC Analog input(7,1) Gel Start sensor is already active low, moving up to get off top"
                target_motor.move(POSDIR, 10, DOUBLESTEP, GELCUR)

        ave = 5.0
        while ((ave >= 0.8) and (GelPos < HomeMax)):  # if gel start switch not active, move 9 step
            temp = 0.0
            ave = 0.0
            good_count = 2
            for cycle in range(1, 3):
                temp = DAC.getADC(7, 1)
                time.sleep(.0002)
                if (temp > 4.1 or temp < 0.3):
                    temp = 0  # Ignore bad reads
                    good_count = good_count - 1
                    # reduce ave count to make up for bad data
                ave = ave + temp
                #print "temp=", temp
            if (good_count == 0): good_count = 1
            ave = (ave / good_count)
            #time.sleep(.002)
            print "Ave and good_count = ", ave, good_count

            target_motor.move(NEGDIR, 10, DOUBLESTEP, GELCUR) #10
            GelPos = GelPos + 9

        print "Completed Gel Pump move to top of syring, steps moved =", GelPos
        temp = 0
        for cycle in range(1, 4):
            temp = (temp + DAC.getADC(7, 1))
            time.sleep(.02)
        print "Input Analog input(7,1) Gel Start sensor "
        print temp
        if (temp <= 5):  # if home switch is active, print complete message
            print "Input analog DAC(7,1) Gel Start sensor is now Active Low"
            print  GelPos
                 
