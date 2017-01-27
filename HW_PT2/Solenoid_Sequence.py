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
        self.reagent_pump = Reagent_Pump()

    def terminate(self):
        self._running = False
        
    #This funcition is created to turn off all solenoids in Manifold.
    def Manifold_Off(self):
        
        print  "Turn off all solenoids in Manifold. \r\n"
        DAC.clrDOUTbit(5, 0)  # Manifold_Solenoid 5 0 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 1)  # Manifold_Solenoid 5 1 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 2)  # Manifold_Solenoid 5 2 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 3)  # Manifold_Solenoid 5 3 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 4)  # Manifold_Solenoid 5 4 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 5)  # Manifold_Solenoid 5 5 OFF
        time.sleep(.22)
        DAC.clrDOUTbit(5, 6)  # Manifold_Solenoid 5 6 OFF
        time.sleep(.22)
        time.sleep(2)
        
    #This function is created to turn off all solenoids in Pump Array.
    def PA_Off(self):
        
        print "Turn off all solenoids in Pump Array. \r\n"
        RELAY.relayOFF(0,2)   # turn off P.A._Solenoid on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayOFF(0,3)   # turn off P.A._Solenoid on relay plate addr 0 relay number 3
        time.sleep(.22)
        RELAY.relayOFF(0,4)   # turn off P.A._Solenoid on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayOFF(0,5)   # turn off P.A._Solenoid on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayOFF(0,6)   # turn off P.A._Solenoid on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayOFF(0,7)   # turn off P.A._Solenoid on relay plate addr 0 relay number 7
        time.sleep(.22)
        RELAY.relayOFF(1,2)   # turn off P.A._Solenoid on relay plate addr 1 relay number 2
        time.sleep(.22)
        RELAY.relayOFF(1,3)   # turn off P.A._Solenoid on relay plate addr 1 relay number 3
        time.sleep(.22)
        time.sleep(2)

    #This function is created to turn on all solenoids in Manifold.    
    def Manifold_On(self):
        
        print "Turn on all solenoids in Manifold. \r\n"
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

    #This function is created to turn on all solenoids in Pump Array.
    def PA_On(self):
        
        print  "Turn on all solenoids in Pump Array \r\n"
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
        time.sleep(2)

    #This two functions are created to control solenoids for step 2. 
    def Dispense_or_Elute_Water_1(self):
        
        print "Start dispensing water or moving 50ul water to elution!  \r\n"
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
        
       
    def Dispense_or_Elute_Water_2(self):

        print "Start dispensing water or moving 50ul water to elution (Continue)!  \r\n" 
        RELAY.relayON(0,2)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(2)

    #This function is created to control solenoids for step 6 
    def Aspirate_MM_Air(self):

        print "Start aspirating MM air! \r\n"
        DAC.clrDOUTbit(7, 0)  #Turn off lamp
        time.sleep(.22)
        RELAY.relayOFF(0,2)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,4)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn oN the heater on relay plate addr 0 relay number 1
        time.sleep(2)
        
    #This fucntion is created to control solenoids for step 8
    def Move_MM_To_Mixing(self):

        print "Start moving MM to mixing! \r\n"
        RELAY.relayON(0,4)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
        time.sleep(.22)
        RELAY.relayON(0,5)   # turn ON the P.A._Solenoid4 on relay plate addr 0 relay number 5
        time.sleep(.22)
        RELAY.relayON(0,6)   # turn ON the P.A._Solenoid5 on relay plate addr 0 relay number 6
        time.sleep(.22)
        RELAY.relayON(0,7)   # turn ON the P.A._Solenoid6 on relay plate addr 0 relay number 7
        time.sleep(2)
        
    #This function is created to control solenoids for step 10.    
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
        time.sleep(2)

    #This function is created to control solenoids for step 11    
    def Move_PCR(self):
        
        print "Start moving to PCR!  \r\n"
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

    #This two functions are created to control solenoids for step 13    
    def PCR_Injection_1(self):
        
        print "Move 2ul PCR to injection! \r\n"
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

    def PCR_Injection_2(self):
        
        print "Move 2ul PCR to injection (Continue)! \r\n"
        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 2
        time.sleep(.22)
        RELAY.relayON(0,3)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 3
        time.sleep(2)
        
    #This function is created to control solenoids for step 14
    def Aspirate_Air(self):

        print "Aspirate air! \r\n"
        RELAY.relayOFF(0,2)
        time.sleep(.22)
        RELAY.relayOFF(0,3)
        time.sleep(.22)
        RELAY.relayON(1,2)
        time.sleep(2)

    #This function is created to control solenoids for step 17     
    def Injection(self):
        
        print "Start injection!  \r\n"
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

    # This function is created to start running sequence.
    def S_Sequence_Enable(self):

        ###########################################################################
        print "Running Step 1: Aspirate Water! \r\n"
        manifold_on_thread_1 = Thread(target = self.Manifold_On)
        manifold_on_thread_1.start()
        pa_off_thread_1 = Thread(target = self.PA_Off)
        pa_off_thread_1.start()
        
        manifold_on_thread_1.join()
        pa_off_thread_1.join()
        
        #Syringe 1: 50uL
        move1_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move1_thread.start()

        move1_thread.join()
        time.sleep(20)
        
        ############################################################################
        print "Running Step 2: Dispense Water! \r\n"
        dispense_or_elute_water_thread1 = Thead(target = self.Dispense_or_Elute_Water_1)
        dispense_or_elute_water_thread1.start()
        dispense_or_elute_water_thread2 = Thead(target = self.Dispense_or_Elute_Water_2)
        dispense_or_elute_water_thread2.start()

        dispense_or_elute_water_thread1.join()
        dispense_or_elute_water_thread2.join()

        time.sleep(20)
        
        #############################################################################
        print "Running Step 3: Aspirate Air! \r\n"
        manifold_on_thread_2 = Thread(target = self.Manifold_On)
        manifold_on_thread_2.start()
        pa_off_thread_2 = Thread(target = self.PA_Off)
        pa_off_thread_2.start()
        
        manifold_on_thread_2.join()
        pa_off_thread_2.join()
        #Syringe 1: 100uL
        move2_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move2_thread.start()

        move2_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 4: Move 50uL water to elution! \r\n"
        dispense_or_elute_water_thread3 = Thead(target = self.Dispense_or_Elute_Water_1)
        dispense_or_elute_water_thread3.start()
        dispense_or_elute_water_thread4 = Thead(target = self.Dispense_or_Elute_Water_2)
        dispense_or_elute_water_thread4.start()

        dispense_or_elute_water_thread3.join()
        dispense_or_elute_water_thread4.join()

        #Syringe 1: 50uL
        move3_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move3_thread.start()

        move3_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 5: Elution! \r\n"
        DAC.setDOUTbit(7, 0)  #Turn on the lamp
        self.Manifold_On()
        RELAY.relayOFF(0,3)   
        time.sleep(20)

        #############################################################################
        print "Running Step 6: Aspirate MM air! \r\n"
        manifold_on_thread_3 = Thread(target = self.Manifold_On)
        manifold_on_thread_3.start()
        aspirate_air_thread1 = Thread(target = self.Aspirate_MM_Air)
        aspirate_air_thread1.start()

        manifold_on_thread_3.join()
        aspirate_air_thread1.join()

        #Syring2 : 5uL
        move4_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "P", "motor_steps": 10000,"move_up": True})
        move4_thread.start()
        #Syringe 3: 5uL
        move5_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "W", "motor_steps": 10000,"move_up": True})
        move5_thread.start()

        move4_thread.join()
        move5_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 7: Aspirate MM! \r\n"
        manifold_on_thread_4 = Thread(target = self.Manifold_On)
        manifold_on_thread_4.start()
        pa_off_thread_3 = Thread(target = self.PA_Off)
        pa_off_thread_3.start()
        
        manifold_on_thread_4.join()
        pa_off_thread_3.join()
        #Syring2 : 7uL
        move6_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "P", "motor_steps": 10000,"move_up": True})
        move6_thread.start()
        #Syringe 3: 7uL
        move7_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "W", "motor_steps": 10000,"move_up": True})
        move7_thread.start()

        move6_thread.join()
        move7_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 8: Move MM to mixing! \r\n"
        #TODO: Add Takasago
        manifold_on_thread_5 = Thread(target = self.Manifold_On)
        manifold_on_thread_5.start()
        move_mm_to_mixing_thread = Thread(target = self.Move_MM_To_Mixing)
        move_mm_to_mixing_thread.start()

        manifold_on_thread_5.join()
        move_mm_to_mixing_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 9: Aspirate air! \r\n"
        manifold_on_thread_6 = Thread(target = self.Manifold_On)
        manifold_on_thread_6.start()
        pa_off_thread_4 = Thread(target = self.PA_Off)
        pa_off_thread_4.start()
        RELAY.relayON(0,2)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4

        manifold_on_thread_6.join()
        pa_off_thread_4.join()

        #Syring 1: 50uL
        move8_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move8_thread.start()
        
        move8_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 10: Mix sample and MM! \r\n"
        self.Mix_Sample()
        #Syring 1: 44uL
        move9_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move9_thread.start()
        
        move9_thread.join()
        time.sleep(20)
        
        #############################################################################
        print "Running Step 11: Move to PCR! \r\n"
        self.Move_PCR()
        #Syring 1: 34uL
        move10_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move10_thread.start()
        
        move10_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 12: PCR! \r\n"
        manifold_on_thread_7 = Thread(target = self.Manifold_On)
        manifold_on_thread_7.start()
        pa_off_thread_5 = Thread(target = self.PA_Off)
        pa_off_thread_5.start()

        manifold_on_thread_7.join()
        pa_off_thread_5.join()

        #Syring 1: 34uL
        move11_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move11_thread.start()
        
        move11_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 13: Move 2uL PCR to injection! \r\n"
        pcr_injection1_thread = Thread(target = self.PCR_Injection_1)
        pcr_injection1_thread.start()
        pcr_injection2_thread = Thread(target = self.PCR_Injection_2)
        pcr_injection2_thread.start()

        pcr_injection1_thread.join()
        pcr_injection2_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 14: Aspirate Air! \r\n"
        manifold_on_thread_8 = Thread(target = self.Manifold_On)
        manifold_on_thread_8.start()
        aspirate_air_thread = Thread(target = self.Aspirate_Air)
        aspirate_air_thread.start()

        manifold_on_thread_8.join()
        aspirate_air_thread.join()
        #Syring 4: 50uL
        move12_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move12_thread.start()
        
        move12_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 15: Aspirate Standard! \r\n"
        manifold_on_thread_9 = Thread(target = self.Manifold_On)
        manifold_on_thread_9.start()
        pa_off_thread_6 = Thread(target = self.PA_Off)
        pa_off_thread_6.start()

        manifold_on_thread_9.join()
        pa_off_thread_6.join()

        #Syring 4: 60uL
        move13_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move13_thread.start()
        
        move13_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 16: Dispense standard to injection! \r\n"
        self.Manifold_On()
        RELAY.relayON(1,2)
        time.sleep(.22)
        RELAY.relayON(1,3)
        time.sleep(20)

        #############################################################################
        print "Running Step 17: Injection! \r\n"
        injection_thread = Thread(target = self.Injection)
        injection_thread.start()
        pa_off_thread_7 = Thread(target = self.PA_Off)
        pa_off_thread_7.start()
        
        injection_thread.join()
        pa_off_thread_7.join()
        
        time.sleep(20)

        #############################################################################
        print "Running Step 18: Syringe clean! \r\n"
        manifold_off_thread_10 = Thread(target = self.Manifold_Off)
        manifold_off_thread_10.start()
        pa_on_thread_8 = Thread(target = self.PA_On)
        pa_on_thread_8.start()

        manifold_off_thread_10.join()
        pa_on_thread_8.join()

        #Syring 1: 100uL
        move14_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move14_thread.start()
        #Syring 2: 100uL
        move15_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move15_thread.start()
        #Syring 3: 100uL
        move16_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move16_thread.start()
        #Syring 4: 100uL
        move17_thread = Thread(target = self.reagent_pump.move, kwargs= {"pump_letter": "M", "motor_steps": 10000,"move_up": True})
        move17_thread.start()
        
        move14_thread.join()
        move15_thread.join()
        move16_thread.join()
        move17_thread.join()
        time.sleep(20)

        #############################################################################
        print "Running Step 19: Syringe dry! \r\n"
        manifold_off_thread_11 = Thread(target = self.Manifold_Off)
        manifold_off_thread_11.start()
        pa_off_thread_9 = Thread(target = self.PA_Off)
        pa_off_thread_9.start()

        manifold_off_thread_11.join()
        pa_off_thread_9.join()
        
        time.sleep(2)              
                
