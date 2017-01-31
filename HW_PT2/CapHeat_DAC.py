#!/usr/bin/python
from pimain import port

from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import time
import atexit
import sys
import RPi.GPIO as GPIO, os
import spidev
import serial
# from xyz_motor import xyz_motor
# from Reagent_Pump import Reagent_Pump
# from Gel_Pump import Gel_Pump
# from Laser_Motor import Laser_Motor
# from Solenoid_Sequence import Solenoid_Sequence
# from Solenoid import Solenoid

import DAQCplate as DAC
from threading import Thread


class CapHeat:
    def __init__(self):
        self._running = True
        self.heat_on = False

    def terminate(self):
        self._running = False

    def Cap_Heater_Enable(self):
        """
        Cap_Heater_Enable for DAC plate (not relay board, the original one is for the relay board.
        :return:
        """
        self.heat_on = True
        while self.heat_on:
            print  "Heating ON, Capillary temperature"
            temp = DAC.getADC(7, 0)
            time.sleep(.02)
            for cycle in range(1, 10):
                temp = DAC.getADC(7, 0)  #
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
            print  temp
            if (temp >= 2.00):  # If higher than 2.097V, then cooler than 60 celcius
                DAC.setDOUTbit(7, 0)  # Activate 24V to capillary heater pins NOpen and COMM
                # print  "Heating ON, Capillary temperature voltage is "
                # print  temp
            if (temp <= 1.86):
                DAC.clrDOUTbit(7, 0)  # De-activate 24V to capillary heater pins NOpen and COMM
                # print  "Heating OFF, Capillary temperature voltage is "
                # print  temp
            port.write(str(temp) + "\n")
            time.sleep(2)

    def Cap_Heater_Off(self):

        print  "Heating OFF \r\n"
        self.heat_on = False
        port.write("Cap Off\n")
        # time.sleep(0.2)
        # RELAY.relayOFF(0, 1)  # turn off the heater on relay plate addr 0 relay number 1
        # time.sleep(0.2)
        # RELAY.relayOFF(0, 1)  # turn off the heater on relay plate addr 0 relay number 1
