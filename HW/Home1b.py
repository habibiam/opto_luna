#!/usr/bin/python
# from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from Opto_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
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
		
		boagit clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.gitrd_sku	 -- which board is under use
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

        #def InputGPIO (IOPin)
        #   GPIO.setup(IOPin, GPIO.IN)
        #   GPIO.Input(IOPin)


	def __init__(self, axies, steps_per_rev, rpm):
                GPIO.setup(5, GPIO.IN)
		if axies == 1:
			self.driver_hat = Adafruit_MotorHAT(addr = 0x60)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		elif axies == 2:
			self.driver_hat = Adafruit_MotorHAT(addr = 0x60)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		elif axies == 3:
			self.driver_hat = Adafruit_MotorHAT(addr = 0x61)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
		elif axies == 0:
			self.driver_hat = Adafruit_MotorHAT(addr = 0x61)
			self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
		else:
			print "Please choose the correct motor from below:"
			print "  1: X_Motor\n  2: Y_Motor\n  3: Z_Motor"
			sys.exit(0)
		self.stepper_motor.setSpeed(rpm)

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
				self.stepper_motor.step(actual_move_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE, current)
			elif step_mode == 2:
				self.stepper_motor.step(actual_move_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE, current)
			elif step_mode == 3:
				self.stepper_motor.step(actual_move_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE, current)
			elif step_mode == 4:
				self.stepper_motor.step(actual_move_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE, current)
			elif step_mode == 4:l_move_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP
			else:
				print "Please choose the correct stepper mode:"
				print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
				turn_off()
				sys.exit(0)
		else:
			if step_mode == 1:
				self.stepper_motor.step(-actual_move_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE, current)
			elif step_mode == 2:
				self.stepper_motor.step(-actual_move_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE, current)
			elif step_mode == 3:
				self.stepper_motor.step(-actual_move_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE, current)
			elif step_mode == 4:
				self.stepper_motor.step(-actual_move_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP, current)
			else:
				print "Please choose the correct stepper mode:"
				print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
				turn_off()
				sys.exit(0)

	def turn_off(self):
		self.driver_hat.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
		self.driver_hat.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
		self.driver_hat.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
		self.driver_hat.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

import DAQCplate as DAC

if __name__ == "__main__":

	#print "move motor addr 61  M2 slide  = xyz_motor(3, 600, 100)"
	target_motor = xyz_motor(3, 600, 100)
	atexit.register(target_motor.turn_off)

	# self.driver_hat.getMotor(4).setPWM(2,220)
	# target_motor.setPWM(2, 220)  # Motor 2 is PWM2 and PWM7 
	# target_motor.setPWM(7, 220)  # Motor 2 is PWM2 and PWM7 
	# target_motor.setSpeed(220)  # Speed 1 to 255
        DAC.setDOUTbit(0,0)
        time.sleep(.1)
        DAC.setDOUTbit(0,1)
        time.sleep(.1)
        DAC.setDOUTbit(0,2)
        time.sleep(.1)
        DAC.setDOUTbit(0,3)
        time.sleep(.1)
        DAC.setDOUTbit(0,4)
        time.sleep(.1)
        DAC.setDOUTbit(0,5)
        time.sleep(.1)
        DAC.setDOUTbit(0,6)
        time.sleep(.1)

        DAC.setLED(0,0)
        DAC.setLED(0,1)
        # if  boards DAC.setLED(1,0)
        # if  boards DAC.setLED(1,1)
        time.sleep(1)
        #DAC.clrLED(0,0)
        #DAC.clrLED(0,1)
        #DAC.clrLED(1,0)
        #DAC.clrLED(1,1)

	target_motor.move(-1, 90, 2, 1) # back up the motor to front edge before homing
        HomeMax = 3800
        SlidePos = 0
        while (( SlidePos < HomeMax) and (GPIO.input(5) != GPIO.LOW)):  # if home switch not active, move 1 step
	      target_motor.move(1, 1, 3, 1) # step one at a time towards home switch
              SlidePos += 1
                 
        #print "Home position is" 
        print  SlidePos

	target_motor.move(-1, SlidePos, 3, 1)  #Retract
	target_motor.turn_off()

	# target_motor = xyz_motor(I2C61, 900, 100)
	# atexit.register(target_motor.turn_off)
	# print "move  motor addr61 M1 out and back "
	# target_motor.move(1, 400, 2, 4) # fully retracted
	# target_motor.move(-1, 400, 2, 4) # fully extended
	# target_motor.move(1, 400, 2, 4) # fully retracted
	# print "end move 2"
	# target_motor.turn_off()
