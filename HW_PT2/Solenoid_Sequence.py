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

import DAQCplate as DAC
from threading import Thread
import piplates.RELAYplate as RELAY

class Solenoid_Sequence:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def Manifold_Off(self):      #turn off all solenoids in Manifold
        print  "Turn off all solenoids in Manifold \r\n"
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
        time.sleep(2)

    def PA_Off(self):         #turn off all solenoids in Pump Array
        print "Turn off P.A. Solenoids \r\n"
        print  "Relay 0 2 OFF \r\n"
        RELAY.relayOFF(0,2)   # turn off P.A._Solenoid on relay plate addr 0 relay number 2
        time.sleep(.22)
        print  "Relay 0 3 OFF \r\n"
        RELAY.relayOFF(0,3)   # turn off P.A._Solenoid on relay plate addr 0 relay number 3
        time.sleep(.22)
        print  "Relay 0 4 OFF \r\n"
        RELAY.relayOFF(0,4)   # turn off P.A._Solenoid on relay plate addr 0 relay number 4
        time.sleep(.22)
        print  "Relay 0 5 OFF \r\n"
        RELAY.relayOFF(0,5)   # turn off P.A._Solenoid on relay plate addr 0 relay number 5
        time.sleep(.22)
        print  "Relay 0 6 OFF \r\n"
        RELAY.relayOFF(0,6)   # turn off P.A._Solenoid on relay plate addr 0 relay number 6
        time.sleep(.22)
        print  "Relay 0 7 OFF \r\n"
        RELAY.relayOFF(0,7)   # turn off P.A._Solenoid on relay plate addr 0 relay number 7
        time.sleep(.22)
        print  "Relay 1 2 OFF \r\n"
        RELAY.relayOFF(1,2)   # turn off P.A._Solenoid on relay plate addr 0 relay number 8
        time.sleep(.22)
        print  "Relay 1 3 OFF \r\n"
        RELAY.relayOFF(1,3)   # turn off P.A._Solenoid on relay plate addr 0 relay number 9
        time.sleep(.22)
        time.sleep(2)
        
    def Manifold_On(self):      #turn on all solenoids in Manifold
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
        time.sleep(2)

    def PA_On(self):            #turn on all solenoids in Pump Array
        print  "P.A._Solenoid 24V ON \r\n"
        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 3
        time.sleep(.22)
        RELAY.relayON(0,4)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayON(0,5)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayON(0,7)   # turn ON the P.A._Solenoid on relay plate addr 0 relay number 7
        time.sleep(.22)
        RELAY.relayON(1,2)   # turn ON the P.A._Solenoid on relay plate addr 1 relay number 2
        time.sleep(.22)
        RELAY.relayON(1,3)   # turn ON the P.A._Solenoid on relay plate addr 1 relay number 3
        time.sleep(.22)
        time.sleep(2)

    def Dispense_or_Elute_Water(self):
        print "Start dispensing water or moving 50ul water to elution! 0111111 \r\n"
        DAC.setDOUTbit(5, 0)  # Activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 1)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 2)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 3)  # De-Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 4)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 5)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 6)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        
        RELAY.relayON(0,2)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        time.sleep(2)
        
    def Mix_Sample(self):
        print "Start sample and MM! 1011111 \r\n"
        DAC.clrDOUTbit(5, 0)  # De-activate 24V to Solenoid pins NOpen and COMM
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
        
        RELAY.relayON(0,3)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 3
        time.sleep(.22)
        time.sleep(2)
        
    def Move_PCR(self):
        print "Start moving to PCR! 1001101 \r\n"
        DAC.clrDOUTbit(5, 0)  # De-activate 24V to Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 1)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 2)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 3)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 4)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 5)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 6)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        time.sleep(2)
        
    def PCR_Injection(self):
        print "Move 2ul PCR to injection! 1010011 \r\n"
        DAC.clrDOUTbit(5, 0)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 1)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 2)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 3)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 4)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 5)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 6)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)

        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 3
        time.sleep(.22)

        time.sleep(2)
        
    def Injection(self):
        print "Start injection! 0000101 \r\n"
        DAC.clrDOUTbit(5, 0)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 1)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 2)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 3)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 4)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.setDOUTbit(5, 5)  # Activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        DAC.clrDOUTbit(5, 6)  # De-activate 24V to Manifold_Solenoid pins NOpen and COMM
        time.sleep(.22)
        time.sleep(2)

    def S_Sequence_Enable(self):
        print "Step1 \r\n"
        self.Manifold_On()
        print "Step1000 \r\n"
        self.PA_Off()
        time.sleep(10)
        
        print "Step2 \r\n"
        self.Dispense_or_Elute_Water()
        time.sleep(10)

        print "Step3 \r\n"
        self.Manifold_On()
        self.PA_Off()
        time.sleep(10)
        
        print "Step4"
        self.Dispense_or_Elute_Water()
        time.sleep(10)
        
        print "Step5"
        DAC.setDOUTbit(7, 0)
        self.Manifold_On()
        RELAY.relayOFF(0,3)   
        time.sleep(10)
    
        print "Step6"
        DAC.clrDOUTbit(7, 0)
        self.Manifold_On()
        RELAY.relayOFF(0,2)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,4)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(10)
        
        print "Step7"
        self.Manifold_On()
        self.PA_Off()
        time.sleep(10)
        
        print "Step8"
        self.Manifold_On()
        RELAY.relayON(0,4)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayON(0,5)   # turn ON the P.A._Solenoid4 on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn ON the P.A._Solenoid5 on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayON(0,7)   # turn ON the P.A._Solenoid6 on relay plate addr 0 relay number 7
        time.sleep(10)
        
        print "Step9"
        self.Manifold_On()
        self.PA_Off()
        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
        time.sleep(10)
        
        print "Step10"
        self.Mix_Sample()
        time.sleep(10)
        
        print "Step11"
        self.Move_PCR()
        time.sleep(10)
        
        print "Step12"
        self.Manifold_On()
        self.PA_Off()
        time.sleep(10)
        
        print "Step13"
        self.PCR_Injection()
        time.sleep(10)
        
        print "Step14"
        self.Manifold_On()
        RELAY.relayOFF(0,2)
        time.sleep(.22)
        RELAY.relayOFF(0,3)
        time.sleep(.22)
        RELAY.relayON(1,2)
        time.sleep(10)
        
        print "Step15"
        self.Manifold_On()
        self.PA_Off()
        time.sleep(10)
        
        print "Step16"
        self.Manifold_On()
        RELAY.relayON(1,2)
        time.sleep(.22)
        RELAY.relayON(1,3)
        time.sleep(10)
        
        print "Step17"
        self.Injection()
        self.PA_Off()
        time.sleep(10)
        
        print "Step18"
        self.Manifold_Off()
        self.PA_On()
        time.sleep(10)
        
        print "Step19"
        self.Manifold_Off()
        self.PA_Off()
        
        time.sleep(2)              
                
