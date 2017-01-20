#!/usr/bin/python
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import time
import atexit
import sys
import RPi.GPIO as GPIO, os
import spidev
import json
import serial

class xyz_motor(object):
    """Initialise the motor object.

       axies       -- which motor to move
                   1: X Motor
                   2: Y_Motor
                   3: Z_Motor
                   Other: Invalid

                   1: Normal connection (forward (moving away from the motor)-- positive steps)
                   -1: Reversed connection (forward (moving away from the motor) -- negative steps)
                   Other: Invalid

       step_mode     -- which stepping mode to drive the motor
                   1: Single coil steps
                   2: Double coil steps
                   3: Interleaved coil steps
                   4: Microsteps

       rpm       -- to set the rounds per minute

       move_steps    -- to set how many steps to move
                   actual_move_steps = move_steps*board_sku
                   if actual_move_steps is postive it moves forward (away from the motor)
                   if actual_move_steps is negative it moves backward (near to the motor)
    """

    def __init__(self, axies, steps_per_rev, rpm):

        self.spi = spidev.SpiDev()
        self.speed = 100000
        self.spi.open(0,1)
        self.spi.max_speed_hz=self.speed

        if axies == 1:  # Board 1,GelPump  pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x60)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 2:  # Board 1, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x60)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        elif axies == 3:  # Board 2, pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x61)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 4:  # Board 2, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x61)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        elif axies == 5:  # Board 3, pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x62)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 6:  # Board 3, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x62)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        elif axies == 7:  # Board 4, pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x63)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 8:  # Board 4, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x63)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        elif axies == 9:  # Board 5, pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x64)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 10:  # Board 5, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x64)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        elif axies == 11:  # Board 6, pins M1 and M2
            self.driver_hat = Opto_MotorHAT(addr=0x65)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
        elif axies == 12:  # Board 6, pins M3 and M4
            self.driver_hat = Opto_MotorHAT(addr=0x65)
            self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
        else:
            print "Please choose the correct motor from below:"
            print "  1: X_Motor\n  2: Y_Motor\n  3: Z_Motor"
            sys.exit(0)
        self.stepper_motor.setSpeed(rpm * 15)

    def move(self, board_sku, move_steps, step_mode, current):
        if (board_sku == 1) or (board_sku == -1):
            actual_move_steps = board_sku * move_steps
        else:
            print "Please choose the correct board sku:"
            print "  1: Normal Connection\n  -1: Reversed Connection"
            self.turn_off()
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
                self.turn_off()
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
                self.turn_off()
                sys.exit(0)
    
    def turn_off(self):
        # Turn off motor, 1 thru 4 is motor mode
        self.driver_hat.getMotor(1).run(Opto_MotorHAT.RELEASE)  
        self.driver_hat.getMotor(2).run(Opto_MotorHAT.RELEASE)
        self.driver_hat.getMotor(3).run(Opto_MotorHAT.RELEASE)
        self.driver_hat.getMotor(4).run(Opto_MotorHAT.RELEASE)
