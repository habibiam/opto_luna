import atexit
import sys
import RPi.GPIO as GPIO, os

import DAQCplate as DAC
from threading import Thread

import json
import time

import serial


class CapHeat:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global Cap_Heater_Enable
        Cap_Heater_Enable = 0.0

        while self._running:
            while Cap_Heater_Enable == 0:
                DAC.clrDOUTbit(7, 0)  # De-activate 24V to capillary heater pins NOpen and COMM
                # Analog input is on DACQ plate address 7 pin 0
                # print  "Heating OFF, Capillary temperature voltage is "
                time.sleep(2)

            while Cap_Heater_Enable:
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
                    time.sleep(2)
                if (temp <= 1.86):
                    DAC.clrDOUTbit(7, 0)  # De-activate 24V to capillary heater pins NOpen and COMM
                    # print  "Heating OFF, Capillary temperature voltage is "
                    # print  temp
                    time.sleep(2)