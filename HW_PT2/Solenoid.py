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

import DAQCplate as DAC
from threading import Thread
import piplates.RELAYplate as RELAY

class Solenoid:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        
    def Solenoid_Off(self):
                
        print  "Solenoid 5 0 OFF \r\n"
        DAC.clrDOUTbit(5, 0)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 1 OFF \r\n"
        DAC.clrDOUTbit(5, 1)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 2 OFF \r\n"
        DAC.clrDOUTbit(5, 2)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 3 OFF \r\n"
        DAC.clrDOUTbit(5, 3)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 4 OFF \r\n"
        DAC.clrDOUTbit(5, 4)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 5 OFF \r\n"
        DAC.clrDOUTbit(5, 5)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 6 OFF \r\n"
        DAC.clrDOUTbit(5, 6)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        print  "Solenoid 5 7 OFF \r\n"
        DAC.clrDOUTbit(5, 7)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        
        print "Turn off Capillary Heater, Cartridge Solenoid and P.A. Solenoids \r\n"
        RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayOFF(0,2)   # turn off the PA_S1 on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayOFF(0,3)   # turn off the PA_S2 on relay plate addr 0 relay number 3
        time.sleep(.22)
        RELAY.relayOFF(0,4)   # turn off the PA_S3 on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayOFF(0,5)   # turn off the PA_S4 on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayOFF(0,6)   # turn off the PA_S5 on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayOFF(0,7)   # turn off the PA_S6 on relay plate addr 0 relay number 7
        time.sleep(.22)
        RELAY.relayOFF(1,1)   # turn off Cartridge_Solenoid on relay plate addr 1 relay number 1
        time.sleep(.22)
        RELAY.relayOFF(1,2)   # turn off the P.A._S7 on relay plate addr 1 relay number 2
        time.sleep(.22)
        RELAY.relayOFF(1,3)   # turn off the P.A._S8 on relay plate addr 1 relay number 3
        time.sleep(.22)
        
        
        RELAY.relayOFF(1,4)   # turn off the xx on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayOFF(1,5)   # turn off the xx on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayOFF(1,6)   # turn off the xx on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayOFF(1,7)   # turn off the xx on relay plate addr 0 relay number 1
        time.sleep(.22)
        
        """

        """
        DAC.clrDOUTbit(7, 0)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 1)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 2)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 3)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 4)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 5)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 6)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(7, 7)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        
        DAC.clrDOUTbit(6, 0)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 1)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 2)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 3)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 4)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 5)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 6)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(6, 7)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        time.sleep(1)


    def Solenoid_Enable(self):

        print "Manifold_Solenoid ON \r\n"
        DAC.setDOUTbit(5, 0)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 1)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)    
        DAC.setDOUTbit(5, 2)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 3)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 4)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 5)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 6)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        
        print  "Capillary Heater ON \r\n"
        RELAY.relayON(0,1)   # turn ON Capillary heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        
        print  "P.A._Solenoid 24V ON \r\n"
        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid1 on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn ON the P.A._Solenoid2 on relay plate addr 0 relay number 3
        time.sleep(.22)
        RELAY.relayON(0,4)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayON(0,5)   # turn ON the P.A._Solenoid4 on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn ON the P.A._Solenoid5 on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayON(0,7)   # turn ON the P.A._Solenoid6 on relay plate addr 0 relay number 7
        time.sleep(.22)
        RELAY.relayON(1,2)   # turn ON the P.A._Solenoid7 on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayON(1,3)   # turn ON the P.A._Solenoid8 on relay plate addr 0 relay number 3
        time.sleep(.22)
        
        print "Cartridge_Solenoid ON \r\n"
        RELAY.relayON(1,1)   # turn ON Cartridge_Solenoid on relay plate addr 1 relay number 1
        time.sleep(.32)
        
        #"""   Not used yet!!!
        RELAY.relayON(1,4)   # turn ON the XX on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayON(1,5)   # turn ON the XX on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayON(1,6)   # turn ON the XX on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayON(1,7)   # turn ON the XX on relay plate addr 0 relay number 7
        time.sleep(.22)
        
        DAC.setDOUTbit(7, 0)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(7, 1)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(7, 2)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(7, 3)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.42)
        DAC.setDOUTbit(7, 4)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)
        DAC.setDOUTbit(7, 5)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)
        DAC.setDOUTbit(7, 6)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)
        
        DAC.setDOUTbit(6, 0)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(6, 1)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(6, 2)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(6, 3)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.42)
        DAC.setDOUTbit(6, 4)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)
        DAC.setDOUTbit(6, 5)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)
        DAC.setDOUTbit(6, 6)  # Activate 24V to capillary heater pins NOpen and COMM
        time.sleep(.32)                   
        time.sleep(1)
   
