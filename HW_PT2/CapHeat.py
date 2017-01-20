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
from Laser_Motor import Laser_Motor
from Solenoid_Sequence import Solenoid_Sequence
from Solenoid import Solenoid

import DAQCplate as DAC
from threading import Thread
import piplates.RELAYplate as RELAY

class CapHeat:
    def __init__(self):
        self._running = True
        self.heat_on = False

    def terminate(self):
        self._running = False
        
    def Cap_Heater_Enable(self):
        self.heat_on = True
        while self.heat_on:
            print  "Heating ON, Capillary temperature voltage is "
            RELAY.toggleLED(0)
            time.sleep(2)

            temp = DAC.getADC(7, 0)
            time.sleep(.02)
            for cycle in range(1, 10):
                temp = DAC.getADC(7, 0)  # DAQC Board addr 7 input 0
                time.sleep(.02)
                temp = (9 * temp + DAC.getADC(7, 0)) / 10
                time.sleep(.02)
            for cycle in range(1, 10):
                temp3 = DAC.getADC(7, 0)
                if ((temp3 > (temp + .6) or (temp3 < (temp - .6)))):
                    temp3 = temp  # if new reading is way larger or smaller than average, ignore it
                time.sleep(.02)
                temp2 = DAC.getADC(7, 0)
                if ((temp2 > (temp + .6) or (temp2 < (temp - .6)))):
                    temp2 = temp  # if new reading is way larger or smaller than average, ignore it
                time.sleep(.02)
                temp = (temp + temp2 + temp3) / 3
                time.sleep(.02)
            if ( self.heat_on == True ) : print  temp
            if (( temp >= 2.00 ) and ( self.heat_on == True) ):  # If higher than 2.097V, then cooler than 60 celcius
                RELAY.relayON(0,1)   # turn oN the heater on relay plate addr 0 relay number 1
                RELAY.toggleLED(0)
                # print  "Heating ON, Capillary temperature voltage is "
                # print  temp
                time.sleep(.022)
            if (temp <= 1.86):
                RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
                RELAY.toggleLED(0)
                time.sleep(.022)

    def Cap_Heater_Off(self):

        print  "Heating OFF \r\n"
        self.heat_on = False
        time.sleep(0.2)             
        RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
        time.sleep(0.2)             
        RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
