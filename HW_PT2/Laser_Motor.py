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
from Reagent_Pump import Reagent_Pump
from Gel_Pump import Gel_Pump

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

GPIO.setmode(GPIO.BCM)

class Laser_Motor:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def Move_l_Laser_Enable(self):
        print  "Moving Laser3 stage to the left "
        target_motor = xyz_motor(3, 200, 100)
        atexit.register(target_motor.turn_off)
        for cycle in range(1, 300):
             target_motor.move(POSDIR, 1, DOUBLESTEP, LASCUR)  # Move down to switch
             time.sleep(.013)
    def Move_r_Laser_Enable(self):
        print  "Moving Laser stage to the right "
        target_motor = xyz_motor(3, 200, 100)
        atexit.register(target_motor.turn_off)
        for cycle in range(1, 300):
             target_motor.move(NEGDIR, 1, DOUBLESTEP, LASCUR)  # Move down to switch
             time.sleep(.013)
    def Move_left_Laser_Enable(self):
        print  "Moving Laser stage to the left "
        target_motor = xyz_motor(3, 200, 100)
        atexit.register(target_motor.turn_off)
        # Retract one step at a time until home switch active
        target_motor.move(POSDIR, 500, MICROSTEP, LASCUR)  
    def Move_right_Laser_Enable(self):
        print  "Moving Laser stage to the right "
        target_motor = xyz_motor(3, 200, 100)
        atexit.register(target_motor.turn_off)
        # Retract one step at a time until home switch active
        target_motor.move(NEGDIR, 500, MICROSTEP, LASCUR)  
    def Move_Laser_Home(self):
        print  "Moving Laser stage to the home switch "
        target_motor = xyz_motor(3, 200, 100)
        atexit.register(target_motor.turn_off)
        HomeMax = 400
        LaserPos = 0
        print "Waiting for DAC addr7 input 1 Laser Home switch to become Active  high"
        temp = 0
        for cycle in range(1, 2):
            temp = temp + DAC.getDINbit(7, 1)
            time.sleep(.01)
        if (temp >= 1):  # if home switch is active, print complete message
            print "Input DAC(7,1) Home sensor is already active high, moving left 110 first"
            target_motor.move(POSDIR, 60, MICROSTEP,
                              LASCUR)  # Moving left, away from the capillary 110
        temp = 0
        for cycle in range(1, 2):  # 1, 3
            temp = temp + DAC.getDINbit(7, 1)
            time.sleep(.01)
        print "Now starting Home"
        while ((temp == 0) and (LaserPos < HomeMax)):  # if home switch not active, move 1 step
            temp = 0
            for cycle in range(1, 2):
                temp = temp + DAC.getDINbit(7, 1)
                time.sleep(.01)
            target_motor.move(NEGDIR, 10, MICROSTEP, LASCUR)  # Moving towards the capillary 5
            LaserPos = LaserPos + 1

        print "Completed Laser move to Home switch"
        if ((DAC.getDINbit(7, 1) == 1)):  # if home switch is active, reset LaserPos
            print "Input DAC(7,1) Laser Home sensor is Now Active high"
            print  LaserPos
            LaserPos = 0
