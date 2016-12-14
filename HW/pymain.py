#!/usr/bin/python
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import time
import atexit
import sys
import RPi.GPIO as GPIO,os

I2C60 = 1
I2C61 = 0
I2C62 = 2
I2C63 = 3

GPIO.setmode(GPIO.BCM)

class xyz_motor(object):

	"""Initialise the motor object.
		
		axies		 -- which motor to move
						1: X Motor
						2: Y_Motor
						3: Z_Motor
						Other: Invalid
		
						1: Normal connection (forward (moving away from the motor)-- positive steps)
						-1: Reversed connection (forward (moving away from the motor) -- negative steps)
						Other: Invalid
						
		step_mode 	 -- which stepping mode to drive the motor
						1: Single coil steps
						2: Double coil steps
						3: Interleaved coil steps
						4: Microsteps
						
		rpm		 -- to set the rounds per minute
		
		move_steps	 -- to set how many steps to move
						actual_move_steps = move_steps*board_sku
						if actual_move_steps is postive it moves forward (away from the motor)
						if actual_move_steps is negative it moves backward (near to the motor)
    """

	def __init__(self, axies, steps_per_rev, rpm):

		if axies == 1:  # Board 1,GelPump  pins M1 and M2
			self.driver_hat = Opto_MotorHAT(addr = 0x60)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		elif axies == 2:  # Board 1, pins M3 and M4
			self.driver_hat = Opto_MotorHAT(addr = 0x60)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		elif axies == 3:  # Board 2, pins M1 and M2
			self.driver_hat = Opto_MotorHAT(addr = 0x61)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		elif axies == 4:  # Board 2, pins M3 and M4
			self.driver_hat = Opto_MotorHAT(addr = 0x61)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		elif axies == 5:  # Board 3, pins M1 and M2
			self.driver_hat = Opto_MotorHAT(addr = 0x62)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		elif axies == 6:  # Board 3, pins M3 and M4
			self.driver_hat = Opto_MotorHAT(addr = 0x62)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		elif axies == 7:  # Board 4, pins M1 and M2
			self.driver_hat = Opto_MotorHAT(addr = 0x63)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		elif axies == 8:  # Board 4, pins M3 and M4
			self.driver_hat = Opto_MotorHAT(addr = 0x63)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		else:
			print "Please choose the correct motor from below:"
			print "  1: X_Motor\n  2: Y_Motor\n  3: Z_Motor"
			sys.exit(0)
		self.stepper_motor.setSpeed(rpm*15)

	def move(self, board_sku, move_steps, step_mode,current):
		if (board_sku == 1) or (board_sku == -1):
			actual_move_steps = board_sku*move_steps
		else:
			print "Please choose the correct board sku:"
			print "  1: Normal Connection\n  -1: Reversed Connection"
			turn_off()
			sys.exit(0)
		
		if actual_move_steps >= 0:
			if step_mode == 1:
				self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.SINGLE, current)
			elif step_mode == 2:
				self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.DOUBLE, current)
			elif step_mode == 3:
				self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.INTERLEAVE, current)
			elif step_mode == 4:
				self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.MICROSTEP, current)
			else:
				print "Please choose the correct stepper mode:"
				print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
				turn_off()
				sys.exit(0)
		else:
			if step_mode == 1:
				self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.SINGLE, current)
			elif step_mode == 2:
				self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.DOUBLE, current)
			elif step_mode == 3:
				self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.INTERLEAVE, current)
			elif step_mode == 4:
				self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.MICROSTEP, current)
			else:
				print "Please choose the correct stepper mode:"
				print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
				turn_off()
				sys.exit(0)

	def turn_off(self):
		self.driver_hat.getMotor(1).run(Opto_MotorHAT.RELEASE)
		self.driver_hat.getMotor(2).run(Opto_MotorHAT.RELEASE)
		self.driver_hat.getMotor(3).run(Opto_MotorHAT.RELEASE)
		self.driver_hat.getMotor(4).run(Opto_MotorHAT.RELEASE)

import serial

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        if ch >= 'a' and ch <= 'z':
            #ch = ch - ' '
            print "USE CAPS"
            port.write("USE CAPS\r\n")
        if ch=='\r' or ch=='\n' or ch=='':
            return rv
        rv += ch

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=60.0)


class Motor:
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self):
        global Move_left_Laser_Enable,Move_right_Laser_Enable
        global Move_Laser_Home,LaserPos
        global Move_ReagentW_Home,Move_ReagentM_Home,Move_ReagentB_Home,Move_ReagentP_Home
        global Move_GelPump_Home,Move_GelPump_Start, Move_GelPump_Move 
        global Move_l_Laser_Enable,Move_r_Laser_Enable


        while self._running:

           if Move_ReagentW_Home:
                print  "Moving ReagentW stage to the home switch "  
	        target_motor = xyz_motor(2, 100, 600)
	        atexit.register(target_motor.turn_off)
                HomeMax = 3800
                ReagentWPos = 0
                print "Waiting for DAC addr7 input 3 ReagentW Home switch to become Active "
                while ((DAC.getDINbit(7,4) != 1) and (ReagentWPos < HomeMax) and (Move_ReagentW_Home == 1)):   #if home switch not active, move 1 step
	              target_motor.move(-1, 1, 1, 2) # Retract laser stage one step at a time until home switch active
                      ReagentWPos = ReagentWPos + 1
                if ((DAC.getDINbit(7,4) == 1) ):   #if home switch is active, reset ReagentWPos
                      print "Input DAC(7,4) ReagentW Home sensor is active" 
                      print  ReagentWPos
                      ReagentWPos = 0
                Move_ReagentW_Home = 0

           if Move_ReagentM_Home:
                print  "Moving ReagentM stage to the home switch "  
	        target_motor = xyz_motor(4, 600, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 3800
                ReagentMPos = 0
                print "Waiting for DAC addr7 input 3 ReagentW Home switch to become Active "
                while ((DAC.getDINbit(7,4) != 1) and (ReagentMPos < HomeMax) and (Move_ReagentM_Home == 1)):   #if home switch not active, move 1 step
	              target_motor.move(-1, 1, 1, 1) # Retract laser stage one step at a time until home switch active
                      ReagentMPos = ReagentMPos + 1
                if ((DAC.getDINbit(7,4) == 1) ):   #if home switch is active, reset ReagentWPos
                      print "Input DAC(7,4) ReagentW Home sensor is active" 
                      print  ReagentMPos
                      ReagentMPos = 0
                Move_ReagentM_Home = 0

           if Move_ReagentB_Home:
                print  "Moving ReagentB stage to the home switch "  
	        target_motor = xyz_motor(5, 600, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 3800
                ReagentBPos = 0
                print "Waiting for DAC addr7 input 3 ReagentB Home switch to become Active "
                while ((DAC.getDINbit(7,5) != 1) and (ReagentBPos < HomeMax) and (Move_ReagentB_Home == 1)):   #if home switch not active, move 1 step
	              target_motor.move(-1, 1, 1, 1) # Retract laser stage one step at a time until home switch active
                      ReagentBPos = ReagentBPos + 1
                if ((DAC.getDINbit(7,5) == 1) ):   #if home switch is active, reset ReagentBPos
                      print "Input DAC(7,5) ReagentB Home sensor is active" 
                      print  ReagentBPos
                      ReagentBPos = 0
                Move_ReagentB_Home = 0

           if Move_ReagentP_Home:
                print  "Moving ReagentP stage to the home switch "  
	        target_motor = xyz_motor(6, 600, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 3800
                ReagentPPos = 0
                print "Waiting for DAC addr7 input 3 ReagentP Home switch to become Active "
                while ((DAC.getDINbit(7,6) != 1) and (ReagentPPos < HomeMax) and (Move_ReagentP_Home == 1)):   #if home switch not active, move 1 step
	              target_motor.move(-1, 1, 1, 1) # Retract laser stage one step at a time until home switch active
                      ReagentPPos = ReagentPPos + 1
                if ((DAC.getDINbit(7,6) == 1) ):   #if home switch is active, reset ReagentPPos
                      print "Input DAC(7,6) ReagentP Home sensor is active" 
                      print  ReagentPPos
                      ReagentPPos = 0
                Move_ReagentP_Home = 0


           if Move_l_Laser_Enable:
                print  "Moving Laser stage to the left "  
	        target_motor = xyz_motor(3, 200, 100)
	        atexit.register(target_motor.turn_off)
	        target_motor.move(-1, 4, 4, 3) # move left 10 steps
                Move_l_Laser_Enable = 0

           if Move_r_Laser_Enable:
                print  "Moving Laser stage to the right "  
	        target_motor = xyz_motor(3, 200, 100)
	        atexit.register(target_motor.turn_off)
	        target_motor.move(1, 4, 4, 3) # move right 20 steps
                Move_r_Laser_Enable = 0

           if Move_left_Laser_Enable:
                print  "Moving Laser stage to the left "  
	        target_motor = xyz_motor(3, 200, 100)
	        atexit.register(target_motor.turn_off)
	        target_motor.move(-1, 2, 4, 3) # move left 10 steps
                Move_left_Laser_Enable = 0

           if Move_right_Laser_Enable:
                print  "Moving Laser stage to the right "  
	        target_motor = xyz_motor(3, 200, 100)
	        atexit.register(target_motor.turn_off)
	        target_motor.move(1, 2, 4, 3) # move right 20 steps
                Move_right_Laser_Enable = 0

           if Move_GelPump_Home:
                print  "Moving Gel Pump to the upper home switch "  
	        target_motor = xyz_motor(1, 200, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 23800
                GelPos = 0
                temp = 0
                for cycle in range (1,2):
                     temp = temp + DAC.getDINbit(7,0)
                     time.sleep(.01)
                if (temp >= 1 ):   #if home switch is active, print complete message
                      print "Input DAC(7,0) Home sensor is already active high, moving down 110 first" 
	              #target_motor.move(-1, 110, 4, 3) # Moving down, away from the top
	              target_motor.move(-1, 1, 1, 1)   # Go down
                temp = 0
                for cycle in range (1,2):
                     temp = temp + DAC.getDINbit(7,0)
                     time.sleep(.01)
                print "Starting Home, for DAC addr7 input 0 Gel Home switch to become Active "
                while ((temp == 0) and (GelPos < HomeMax) and (Move_GelPump_Home == 1)):   #if home switch not active, move 1 step
                      temp = 0
                      for cycle in range (1,2):
                           temp = temp + DAC.getDINbit(7,0)
                           time.sleep(.01)
	              #target_motor.move(1, 5, 4, 3)  #
	              target_motor.move(1, 1, 1, 1) # Go forward, up to top of gel pump to allow gel replacement
                      GelPos = GelPos + 1
                print "Completed Gel Pump move to Home switch"
                print  GelPos
                if ((DAC.getDINbit(7,0) == 1) ):   #if home switch is active, reset GelPos
                      print "Input DAC(7,0) Gel Home sensor is active high" 
                      print  GelPos
                      GelPos = 0
                Move_GelPump_Home = 0

           if Move_GelPump_Start :
	        target_motor = xyz_motor(1, 200, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 23800
                GelPos = 0
                temp = 0
                print "Waiting for DAC addr7 input 2 Gel Start switch to become Active "

                for cycle in range (1,3):
                     temp = temp + DAC.getDINbit(7,2)
                     time.sleep(.01)
                     if (temp == 0 ):   #if home switch is active, print complete message
                        print "Input DAC(7,2) Gel Start sensor is already active low, moving up to get off top" 
	                target_motor.move(1, 30, 1, 1) # bring motor up 

                while ((temp != 0) and ( GelPos < HomeMax) and (Move_GelPump_Start == 1)):   #if gel start switch not active, move 1 step
                     temp = 0
                     for cycle in range (1,3):
                       temp = temp + DAC.getDINbit(7,2)
                       time.sleep(.01)
             
	             target_motor.move(-1, 3, 1, 1) # bring motor down one step at a time 
                     GelPos = GelPos + 1

                print "Completed Gel Pump move to top of syring"
                print  GelPos
                if ((DAC.getDINbit(7,2) == 0) ):   #if home switch is active, print complete message
                     print "Input DAC(7,2) Gel Start sensor is now Active Low" 
                     print  GelPos
                Move_GelPump_Start = 0

           if Move_Laser_Home:
                print  "Moving Laser stage to the home switch "  
	        target_motor = xyz_motor(3, 200, 100)
	        atexit.register(target_motor.turn_off)
                HomeMax = 400
                LaserPos = 0
                print "Waiting for DAC addr7 input 1 Laser Home switch to become Active  high"
                temp = 0
                for cycle in range (1,2):
                     temp = temp + DAC.getDINbit(7,1)
                     time.sleep(.01)
                if (temp >= 1 ):   #if home switch is active, print complete message
                      print "Input DAC(7,1) Home sensor is already active high, moving left 110 first" 
	              target_motor.move(-1, 110, 4, 3) # Moving left, away from the capillary
                temp = 0
                for cycle in range (1,3):
                     temp = temp + DAC.getDINbit(7,1)
                     time.sleep(.01)
                print "Now starting Home" 
                while ((temp == 0) and (LaserPos < HomeMax) and (Move_Laser_Home == 1)):   #if home switch not active, move 1 step
                      temp = 0
                      for cycle in range (1,2):
                           temp = temp + DAC.getDINbit(7,1)
                           time.sleep(.01)
	              target_motor.move(1, 5, 4, 3) # Moving towards the capillary
                      LaserPos = LaserPos + 1
                print "Completed Laser move to Home switch"
                if ((DAC.getDINbit(7,1) == 1) ):   #if home switch is active, reset LaserPos
                      print "Input DAC(7,1) Laser Home sensor is Now Active high" 
                      print  LaserPos
                      LaserPos = 0
                Move_Laser_Home = 0

           if Move_GelPump_Move :
                GelPos = 0
                print "Moving Gel Pump down 10uL  \r\n"
	        target_motor = xyz_motor(1, 200, 100)
	        atexit.register(target_motor.turn_off)
	        target_motor.move(-1, 200, 1, 1) # Go downward, gel pump down to pump gel 
                GelPos = GelPos + 10
                Move_GelPump_Move = 0



class CapHeat:
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self):
        global Cap_Heater_Enable

        while self._running:
          while Cap_Heater_Enable == 0:
                DAC.clrDOUTbit(7,0)       #De-activate 24V to capillary heater pins NOpen and COMM
                #print  "Heating OFF, Capillary temperature voltage is "  
                time.sleep(2)

          while Cap_Heater_Enable:
              temp =  DAC.getADC(7,0)
              time.sleep(.02)
              for cycle in range (1,10):
                  temp =  DAC.getADC(7,0)
                  time.sleep(.04)
                  temp =  (9 * temp + DAC.getADC(7,0)) / 10
                  time.sleep(.02)
                  #print "9 times ave "
              print  temp
              if ( temp >= 2.00 ):  # If higher than 2.097V, then cooler than 60 celcius
                DAC.setDOUTbit(7,0)       #Activate 24V to capillary heater pins NOpen and COMM
                #print  "Heating ON, Capillary temperature voltage is "  
                #print  temp
                time.sleep(2)
              if ( temp <= 1.86 ):
                DAC.clrDOUTbit(7,0)       #De-activate 24V to capillary heater pins NOpen and COMM
                #print  "Heating OFF, Capillary temperature voltage is "  
                #print  temp
                time.sleep(2)

import DAQCplate as DAC
from threading import Thread

if __name__ == "__main__":

        global Cap_Heater_Enable,Move_left_Laser_Enable,Move_right_Laser_Enable
        global Move_Laser_Home,Move_GelPump_Home,Move_GelPump_Start, Move_GelPump_Move
        global Move_ReagentW_Home, Move_ReagentM_Home, Move_ReagentB_Home, Move_ReagentP_Home 
        global Move_l_Laser_Enable,Move_r_Laser_Enable

        Move_left_Laser_Enable = Move_right_Laser_Enable = Move_ReagentW_Home = Move_l_Laser_Enable = Move_r_Laser_Enable = 0.0 
        Cap_Heater_Enable = Move_Laser_Home = Move_GelPump_Home = Move_GelPump_Start = Move_GelPump_Move = 0.0
        Move_ReagentP_Home = Move_ReagentB_Home = Move_ReagentM_Home = 0 
        Heat = CapHeat()                      #Create Class CapHeat
        HeatThread = Thread(target=Heat.run)  #Create the thread to run Heat
        HeatThread.start()                    # start runing the cap heater thread above 

        Mot = Motor()                         #Create Class Motor
        MotThread = Thread(target=Mot.run)    #Create the thread to run Heat
        MotThread.start()                     # start runing the Motor  thread above 


        print "Waiting for serial commands "
        port.write("\r\nEnter Pi Cmd:")
        rcv = readlineCR(port)
        
        while (rcv != "EXIT"):
            #port.write("\r\nEnter Pi Cmd:")
            rcv = readlineCR(port)
            port.write("OK\n" )
            print "recieved serial string:" + rcv
            
            if ( rcv == "R" ):
               Move_r_Laser_Enable = 1

            if ( rcv == "L" ):
               Move_l_Laser_Enable = 1

            if ( rcv == "REAGW" ):
               Move_ReagentW_Home = 1
               print "Move_ReagentW_Home Moving Home\r\n"

            if ( rcv == "REAGM" ):
               Move_ReagentM_Home = 1
               print "Move_ReagentM_Home Moving Home\r\n"

            if ( rcv == "REAGP" ):
               Move_ReagentP_Home = 1
               print "Move_ReagentP_Home Moving Home\r\n"

            if ( rcv == "REAGB" ):
               Move_ReagentB_Home = 1
               print "Move_ReagentB_Home Moving Home\r\n"

            if ( rcv == "CAPHEAT" ):
               Cap_Heater_Enable = 1
               print "Capillary Heater ON\r\n"

            if ( rcv == "LEFT" ):
               Move_left_Laser_Enable = 1
               print "Moving Laser left \r\n"

            if ( rcv == "RIGHT" ):
               Move_right_Laser_Enable = 1
               print "Moving Laser left \r\n"

            if ( rcv == "RETRACT"  or rcv == "LASRET"  ):
               Move_Laser_Home = 1
               print "Moving Laser to home switch \r\n"

            if ( rcv == "GELRET" ):
               Move_GelPump_Home = 1
               print "Moving Gel Pump to Home switch \r\n"

            if ( rcv == "GELSTRT" ):
               Move_GelPump_Start = 1
               print "Moving Gel Pump to Start switch \r\n"

            if ( rcv == "GELMV" ):
               Move_GelPump_Move = 10
               print "Moving Gel Pump to position \r\n"

            if ( rcv == "K" ) or ( rcv == "KILL" ) or ( rcv == "QUIT" ) or ( rcv == "Q" ):
               Cap_Heater_Enable = 0
               Move_ReagentW_Home = 0
               Move_ReagentM_Home = 0
               Move_ReagentB_Home = 0
               Move_ReagentP_Home = 0
               Move_GelPump_Move = 0
               Move_GelPump_Start = 0
               Move_GelPump_Home = 0
               Move_Laser_Home = 0
               Move_left_Laser_Enable = 0
               Move_right_Laser_Enable = 0
	       target_motor = xyz_motor(1, 200, 100)
	       target_motor.turn_off()
	       target_motor = xyz_motor(2, 200, 100)
	       target_motor.turn_off()
	       target_motor = xyz_motor(3, 200, 100)
	       target_motor.turn_off()
	       target_motor = xyz_motor(4, 200, 100)
	       target_motor.turn_off()
	       target_motor = xyz_motor(5, 200, 100)
	       target_motor.turn_off()
	       target_motor = xyz_motor(6, 200, 100)
	       target_motor.turn_off()
               print "Stopping all motors and heater\r\n"

            if ( rcv == "?" ):
               print "CAPHEAT LEFT RIGHT LASRET GELRET GELSTRT GELMV Q QUIT L R\r\n"
               port.write("CAPHEAT LEFT RIGHT LASRET GELRET GELSTRT GELMV Q QUIT\r\n")


        st1.termintate()
	target_motor.turn_off()
