#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
 
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr = 0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
 
atexit.register(turnOffMotors)

myStepper = mh.getStepper(1000, 2)
myStepper.setSpeed(300)

while (True):
	print("Single coil steps")
	myStepper.step(1000, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
	myStepper.step(1000, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	print("Double coil steps")
	myStepper.step(1000, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
	myStepper.step(1000, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
	print("Interleaved coil steps")
	myStepper.step(1000, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
	myStepper.step(1000, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
	print("Microsteps")
	myStepper.step(1000, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
	myStepper.step(1000, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
	
# stepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
# stepper2.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
