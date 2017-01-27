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
REAGENTCUR = 2
GELCUR = 2
XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
NEGDIR = -1  # Negative move direction
POSDIR = 1  # Positive move direction

class Y_Stage:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def move_Y_home(self):
        print  "Moving Y_stage to home switch "
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 123800
        Pos = 0
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(5, 0)
            time.sleep(.01)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(5, 0) Home sensor is already active high, moving down 400 first"
            target_motor.move(NEGDIR, 5000, DOUBLESTEP, REAGENTCUR)
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(5, 0)
            time.sleep(.001)
        print "Starting Home, for DAC addr7 input 0 Y_stage switch to become Active "
        while ((temp == 0) and (Pos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(5, 0)
                time.sleep(.001)
            target_motor.move(POSDIR, 1000, DOUBLESTEP, REAGENTCUR)  #move down
            Pos = Pos + 1
        print "Completed Y_stage move to Home switch"
        print  Pos
        if ((DAC.getDINbit(5, 0) == 1)):  # if home switch is active, reset Pos
            print "Input DAC(5,0) Y_stage sensor is active high"
            print  Pos
            Pos = 0

    def move_Y_start(self):
        print "Moving Y stage "
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        # Retract one step at a time until home switch active
        target_motor.move(NEGDIR, 5000, DOUBLESTEP, REAGENTCUR) #move up
        target_motor.move(NEGDIR, 1, DOUBLESTEP, 0) 
                 
