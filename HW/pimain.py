#!/usr/bin/python
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import atexit
import sys
import RPi.GPIO as GPIO, os

import DAQCplate as DAC
from threading import Thread

import json
import time

import serial


I2C60 = 1
I2C61 = 0
I2C62 = 2
I2C63 = 3
FASTSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
FULLSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
MICROSTEP = 4  # This is 16 micro step per full step mode, use to precise position or for pumping slowly
DOUBLECOILMICROSTEP = 2 # Wei

LOWCUR = 1  # lowest current setting is 1, max is 16
MIDCUR = 2  # medium current setting is 2, max is 16
HIGHCUR = 4  # high current setting is 3, max is 16
XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
NEGDIR = -1  # Negative move direction
POSDIR = 1  # Positive move direction

GPIO.setmode(GPIO.BCM)


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
        self.driver_hat.getMotor(1).run(Opto_MotorHAT.RELEASE)
        self.driver_hat.getMotor(2).run(Opto_MotorHAT.RELEASE)
        self.driver_hat.getMotor(3).run(Opto_MotorHAT.RELEASE)
        self.driver_hat.getMotor(4).run(Opto_MotorHAT.RELEASE)


def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        if ch >= 'a' and ch <= 'z':
            # ch = ch - ' '
            print "USE CAPS"
            port.write("USE CAPS\r\n")
        if ch == '\r' or ch == '\n' or ch == '':
            return rv
        rv += ch


port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=60.0)


class Motor:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        pass

#         global Move_left_Laser_Enable, Move_right_Laser_Enable
#         global Move_Laser_Home, LaserPos
#         global Move_ReagentW_Home, Move_ReagentM_Home, Move_ReagentB_Home, Move_ReagentP_Home
#         global Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
#
#         global move_gel_pump_down, move_gel_pump_up
#
#         global Move_l_Laser_Enable, Move_r_Laser_Enable
#         # STAGE X Z edit
#         # STAGE X Z edit
#         global move_stageX_left_small, move_stageX_left_big, move_stageX_right_small, move_stageX_right_big, move_stageZ_up, move_stageZ_down
#         global move_to_sample, move_to_buffer, move_to_water, move_to_waste
#
#         z_stage_move_step = 6000 # 6000
#         x_stage_move_step_big = 4500 # 4500
#         x_stage_move_step_small = 4000 # 4000
#
#         sample_abs_pos = 3100 #3100
#
#         buffer_abs_pos = sample_abs_pos + x_stage_move_step_small#7100
#         water_abs_pos = buffer_abs_pos + x_stage_move_step_big #11600
#         waste_abs_pos = water_abs_pos + x_stage_move_step_big #16100
#
#         while self._running:
#
#             if Move_ReagentW_Home:
#                 print  "Moving ReagentW stage to the home switch "
#                 target_motor = xyz_motor(2, 100, 600)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 3800
#                 ReagentWPos = 0
#                 print "Waiting for DAC addr7 input 3 ReagentW Home switch to become Active "
#                 while ((DAC.getDINbit(7, 4) != 1) and (ReagentWPos < HomeMax) and (
#                     Move_ReagentW_Home == 1)):  # if home switch not active, move 1 step
#                     target_motor.move(NEGDIR, 1, FASTSTEP,
#                                       MIDCUR)  # Retract one step at a time until home switch active
#                     ReagentWPos = ReagentWPos + 1
#                 if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentWPos
#                     print "Input DAC(7,4) ReagentW Home sensor is active"
#                     print  ReagentWPos
#                     ReagentWPos = 0
#                 Move_ReagentW_Home = 0
#
#             if Move_ReagentM_Home:
#                 print  "Moving ReagentM stage to the home switch "
#                 target_motor = xyz_motor(4, 600, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 3800
#                 ReagentMPos = 0
#                 print "Waiting for DAC addr7 input 3 ReagentW Home switch to become Active "
#                 while ((DAC.getDINbit(7, 4) != 1) and (ReagentMPos < HomeMax) and (
#                     Move_ReagentM_Home == 1)):  # if home switch not active, move 1 step
#                     target_motor.move(NEGDIR, 1, FASTSTEP,
#                                       MIDCUR)  # Retract one step at a time until home switch active
#                     ReagentMPos = ReagentMPos + 1
#                 if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentWPos
#                     print "Input DAC(7,4) ReagentW Home sensor is active"
#                     print  ReagentMPos
#                     ReagentMPos = 0
#                 Move_ReagentM_Home = 0
#
#             if Move_ReagentB_Home:
#                 print  "Moving ReagentB stage to the home switch "
#                 target_motor = xyz_motor(5, 600, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 3800
#                 ReagentBPos = 0
#                 print "Waiting for DAC addr7 input 3 ReagentB Home switch to become Active "
#                 while ((DAC.getDINbit(7, 5) != 1) and (ReagentBPos < HomeMax) and (
#                     Move_ReagentB_Home == 1)):  # if home switch not active, move 1 step
#                     target_motor.move(NEGDIR, 1, FASTSTEP,
#                                       MIDCUR)  # Retract one step at a time until home switch active
#                     ReagentBPos = ReagentBPos + 1
#                 if ((DAC.getDINbit(7, 5) == 1)):  # if home switch is active, reset ReagentBPos
#                     print "Input DAC(7,5) ReagentB Home sensor is active"
#                     print  ReagentBPos
#                     ReagentBPos = 0
#                 Move_ReagentB_Home = 0
#
#             if Move_ReagentP_Home:
#                 print  "Moving ReagentP stage to the home switch "
#                 target_motor = xyz_motor(6, 600, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 3800
#                 ReagentPPos = 0
#                 print "Waiting for DAC addr7 input 3 ReagentP Home switch to become Active "
#                 while ((DAC.getDINbit(7, 6) != 1) and (ReagentPPos < HomeMax) and (
#                     Move_ReagentP_Home == 1)):  # if home switch not active, move 1 step
#                     target_motor.move(NEGDIR, 1, FASTSTEP,
#                                       MIDCUR)  # Retract one step at a time until home switch active
#                     ReagentPPos = ReagentPPos + 1
#                 if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentPPos
#                     print "Input DAC(7,6) ReagentP Home sensor is active"
#                     print  ReagentPPos
#                     ReagentPPos = 0
#                 Move_ReagentP_Home = 0
#
#             if Move_l_Laser_Enable:
#                 print  "Moving Laser3 stage to the left "
#                 target_motor = xyz_motor(2, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 for cycle in range(1, 2000):
#                     target_motor.move(NEGDIR, 1, FULLSTEP,
#                                       HIGHCUR)  # Retract one step at a time until home switch active
#                     time.sleep(.001)
#                 Move_l_Laser_Enable = 0
#
#             if Move_r_Laser_Enable:
#                 print  "Moving Laser stage to the right "
#                 target_motor = xyz_motor(2, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 for cycle in range(1, 2000):
#                     target_motor.move(POSDIR, 1, FULLSTEP,
#                                       HIGHCUR)  # Retract one step at a time until home switch active
#                     time.sleep(.001)
#                 Move_r_Laser_Enable = 0
#
#             if Move_left_Laser_Enable:
#                 print  "Moving Laser stage to the left "
#                 target_motor = xyz_motor(3, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(NEGDIR, 2, MICROSTEP, HIGHCUR)  # Retract one step at a time until home switch active
#                 Move_left_Laser_Enable = 0
#
#             if Move_right_Laser_Enable:
#                 print  "Moving Laser stage to the right "
#                 target_motor = xyz_motor(3, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(POSDIR, 2, MICROSTEP, HIGHCUR)  # Retract one step at a time until home switch active
#                 Move_right_Laser_Enable = 0
#
#             if move_gel_pump_up:
#                 """
#                 LOWCUR = 1  # lowest current setting is 1, max is 16
#                 MIDCUR = 2  # medium current setting is 2, max is 16
#                 HIGHCUR = 4  # high current setting is 3, max is 16
#                 XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
#                 NEGDIR = -1  # Negative move direction
#                 POSDIR = 1  # Positive move direction
#
#                 """
#                 print "Moving Gel pump up"
#                 target_motor = xyz_motor(1, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 min = 2.0
#                 run_once = False
#                 t_end = time.time() + 60 * min
#                 while time.time() < t_end:
#                     target_motor.move(POSDIR, 1, DOUBLECOILMICROSTEP, HIGHCUR)
#                     time.sleep(0.005)
#                     if (run_once): break
#                 print "finished"
#                 move_gel_pump_down = 0
#                 port.write("done   \n")
#                 print "sent done to port"
#
#             if move_gel_pump_down:
#                 print "Moving Gel pump down"
#                 target_motor = xyz_motor(1, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 min = 2.0
#                 run_once = False
#                 t_end = time.time() + 60 * min
#                 while time.time() < t_end:
#                     target_motor.move(NEGDIR, 1, DOUBLECOILMICROSTEP, HIGHCUR)
#                     time.sleep(0.005)
#                     if (run_once): break
#                 print "finished"
#                 move_gel_pump_down = 0
#                 port.write("done   \n")
#                 print "sent done to port"
#
#
#             if Move_GelPump_Home:
#                 print  "Moving Gel Pump to the upper home switch "
#                 target_motor = xyz_motor(1, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 123800
#                 GelPos = 0
#                 temp = 0
#                 for cycle in range(1, 2):
#                     temp = temp + DAC.getDINbit(7, 0)
#                     time.sleep(.01)
#                 if (temp >= 1):  # if home switch is active, print complete message
#                     print "Input DAC(7,0) Home sensor is already active high, moving down 110 first"
#                     target_motor.move(NEGDIR, 60, MICROSTEP,
#                                       LOWCUR)  # Retract one step at a time until home switch active
#                 temp = 0
#                 for cycle in range(1, 2):
#                     temp = temp + DAC.getDINbit(7, 0)
#                     time.sleep(.01)
#                 print "Starting Home, for DAC addr7 input 0 Gel Home switch to become Active "
#                 while ((temp == 0) and (GelPos < HomeMax) and (
#                     Move_GelPump_Home == 1)):  # if home switch not active, move 1 step
#                     temp = 0
#                     for cycle in range(1, 2):
#                         temp = temp + DAC.getDINbit(7, 0)
#                         time.sleep(.01)
#                     target_motor.move(POSDIR, 10, FASTSTEP,
#                                       LOWCUR)  # Go forward, up to top of gel pump to allow gel replacement
#                     GelPos = GelPos + 1
#                 print "Completed Gel Pump move to Home switch"
#                 print  GelPos
#                 if ((DAC.getDINbit(7, 0) == 1)):  # if home switch is active, reset GelPos
#                     print "Input DAC(7,0) Gel Home sensor is active high"
#                     print  GelPos
#                     GelPos = 0
#                 Move_GelPump_Home = 0
#
#             if Move_GelPump_Start:
#                 target_motor = xyz_motor(1, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 123800
#                 GelPos = 0
#                 temp = 0
#                 print "Waiting for DAC addr7 input 2 Gel Start switch to become Active "
#
#                 for cycle in range(1, 3):
#                     temp = DAC.getADC(7, 2)
#                     print temp
#                     time.sleep(.02)
#                     if (temp == 0):  # if home switch is active, print complete message
#                         print "Input DAC Analog input(7,2) Gel Start sensor is already active low, moving up to get off top"
#                         target_motor.move(POSDIR, 30, FASTSTEP, LOWCUR)  # bring motor up
#
#                 ave = 5.0
#                 while ((ave >= 0.8) and (GelPos < HomeMax) and (
#                     Move_GelPump_Start == 1)):  # if gel start switch not active, move 9 step
#                     temp = 0.0
#                     ave = 0.0
#                     good_count = 8
#                     for cycle in range(1, 9):
#                         temp = DAC.getADC(7, 2)
#                         time.sleep(.002)
#                         if (temp > 3.1 or temp < 0.3):
#                             temp = 0  # Ignore bad reads
#                             good_count = good_count - 1
#                             # reduce ave count to make up for bad data
#                         ave = ave + temp
#                         print "temp=", temp
#                     if (good_count == 0): good_count = 1
#                     ave = (ave / good_count)
#                     time.sleep(.002)
#                     print "Ave and good_count = ", ave, good_count
#
#                     target_motor.move(NEGDIR, 9, MICROSTEP, LOWCUR)  # bring motor down one step at a time
#                     GelPos = GelPos + 9
#
#                 print "Completed Gel Pump move to top of syring, steps moved =", GelPos
#                 temp = 0
#                 for cycle in range(1, 4):
#                     temp = (temp + DAC.getADC(7, 2))
#                     time.sleep(.02)
#                 print "Input Analog input(7,2) Gel Start sensor "
#                 print temp
#                 if (temp <= 5):  # if home switch is active, print complete message
#                     print "Input analog DAC(7,2) Gel Start sensor is now Active Low"
#                     print  GelPos
#                 Move_GelPump_Start = 0
#
#             if Move_Laser_Home:
#                 print  "Moving Laser stage to the home switch "
#                 target_motor = xyz_motor(3, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 HomeMax = 400
#                 LaserPos = 0
#                 print "Waiting for DAC addr7 input 1 Laser Home switch to become Active  high"
#                 temp = 0
#                 for cycle in range(1, 2):
#                     temp = temp + DAC.getDINbit(7, 1)
#                     time.sleep(.01)
#                 if (temp >= 1):  # if home switch is active, print complete message
#                     print "Input DAC(7,1) Home sensor is already active high, moving left 110 first"
#                     target_motor.move(NEGDIR, 110, MICROSTEP, HIGHCUR)  # Moving left, away from the capillary
#                 temp = 0
#                 for cycle in range(1, 3):
#                     temp = temp + DAC.getDINbit(7, 1)
#                     time.sleep(.01)
#                 print "Now starting Home"
#                 while ((temp == 0) and (LaserPos < HomeMax) and (
#                     Move_Laser_Home == 1)):  # if home switch not active, move 1 step
#                     temp = 0
#                     for cycle in range(1, 2):
#                         temp = temp + DAC.getDINbit(7, 1)
#                         time.sleep(.01)
#                     target_motor.move(POSDIR, 5, MICROSTEP, HIGHCUR)  # Moving towards the capillary
#                     LaserPos = LaserPos + 1
#
#                 print "Completed Laser move to Home switch"
#                 if ((DAC.getDINbit(7, 1) == 1)):  # if home switch is active, reset LaserPos
#                     print "Input DAC(7,1) Laser Home sensor is Now Active high"
#                     print  LaserPos
#                     LaserPos = 0
#                 Move_Laser_Home = 0
#
#             if Move_GelPump_Move:
#                 GelPos = 0
#                 print "Moving Gel Pump down 10uL  \r\n"
#                 target_motor = xyz_motor(1, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(NEGDIR, 300, MICROSTEP, HIGHCUR)  # Go downward, gel pump down to pump gel
#                 GelPos = GelPos + 10
#                 for cycle in range(1, 10):  # Every 20 seconds pump one step
#                     print "Moving Gel Pump down at 3uL per hour  \r\n"
#                     time.sleep(0.2)
#                     target_motor.move(NEGDIR, 1, MICROSTEP, HIGHCUR)  # Go downward, gel pump down to pump gel
#                 Move_GelPump_Move = 0
#
#
#
# ############################## SOLUTION STATION #################################
#             # Relative positioning for Solution Station X and Z
#             if move_stageX_left_small:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(NEGDIR, x_stage_move_step_small, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
#                 self.stage_x_and_z_pos["x_pos"] -= x_stage_move_step_small
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_stageX_left_small = 0
#                 port.write("done  \n")
#             if move_stageX_right_small:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 print "Moving Stage X RIGHT"
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(POSDIR, x_stage_move_step_small, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
#                 self.stage_x_and_z_pos["x_pos"] += x_stage_move_step_small
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_stageX_right_small = 0
#                 port.write("done   \n")
#                 # print "sent done to port"
#             if move_stageX_left_big:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 # print "Moving Stage X LEFT"
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(NEGDIR, x_stage_move_step_big, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to big vial, increment is 4500
#                 self.stage_x_and_z_pos["x_pos"] -= x_stage_move_step_big
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_stageX_left_big = 0
#                 port.write("done   \n")
#                 print "sent done to port"
#             if move_stageX_right_big:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 # print "Moving Stage X RIGHT"
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 target_motor.move(POSDIR, x_stage_move_step_big, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to big vial, increment is 4500
#                 self.stage_x_and_z_pos["x_pos"] += x_stage_move_step_big
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_stageX_right_big = 0
#                 port.write("done   \n")
#                 print "sent done to port"
#             if move_stageZ_up:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] >= z_stage_move_step:
#                     print "Stage z is already at the top"
#                     move_stageZ_up = 0
#                     port.write("done   \n")
#                     print "sent done to port"
#                 else:
#                     print "Moving Stage Z UP"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(NEGDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # NEGDIR makes Stage Z go up
#                     self.stage_x_and_z_pos["z_pos"] += z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                     move_stageZ_up = 0
#                     port.write("done   \n")
#                     print "sent done to port"
#             if move_stageZ_down:
#                 if self.stage_x_and_z_pos["z_pos"] <= 0:
#                     print "Stage z is already at the very bottom"
#                     move_stageZ_down = 0
#                     port.write("done   \n")
#                     print "sent done to port"
#                 else:
#                     print "Moving Stage Z DOWN"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                     move_stageZ_down = 0
#                     port.write("done   \n")
#                     print "sent done to port"
#
#
#
#             # Absolute positions for stage x
#             if move_to_sample:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#
#                 current_x_pos = self.stage_x_and_z_pos["x_pos"] # get the current position from the json file
#                 relative_steps = abs(sample_abs_pos - current_x_pos) # find the relative pos
#
#                 # Move motor based on current_x_pos of the motor and sample_abs_pos
#                 if current_x_pos < sample_abs_pos: # if current_x_pos == 0
#                     target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 elif current_x_pos > sample_abs_pos: # if current_x_pos == 7500, 12000, 16500
#                     target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#
#                 self.stage_x_and_z_pos["x_pos"] = sample_abs_pos
#                 # update the json file
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_to_sample = 0
#                 # Print to the LunaSrv
#                 port.write("done   \n")
#                 print "sent done to port"
#
#             if move_to_buffer:
#                 # Check to see if z is position 0, if not then bring z to home
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 # buffer_abs_pos = 7500
#                 current_x_pos = self.stage_x_and_z_pos["x_pos"]
#                 relative_steps = abs(buffer_abs_pos - current_x_pos)
#
#                 if current_x_pos < buffer_abs_pos: # if current_x_pos == 0, 3500
#                     target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 elif current_x_pos > buffer_abs_pos: # if current_x_pos == 12000, 16500
#                     target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 # update the json file
#                 self.stage_x_and_z_pos["x_pos"] = buffer_abs_pos
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_to_buffer = 0
#                 # Print to the LunaSrv
#                 port.write("done   \n")
#                 print "sent done to port"
#
#             if move_to_water:
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#                 current_x_pos = self.stage_x_and_z_pos["x_pos"]
#                 relative_steps = abs(water_abs_pos - current_x_pos)
#
#                 if current_x_pos < water_abs_pos:  # if current_x_pos == 0, 3500
#                     target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 elif current_x_pos > water_abs_pos:  # if current_x_pos == 12000, 16500
#                     target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 # update the json file
#                 self.stage_x_and_z_pos["x_pos"] = water_abs_pos
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_to_water = 0
#                 # Print to the LunaSrv
#                 port.write("done   \n")
#                 print "sent done to port"
#
#             if move_to_waste:
#                 if self.stage_x_and_z_pos["z_pos"] > 0:
#                     print "Moving Stage Z DOWN FIRST"
#                     target_motor = xyz_motor(2, 200, 100)
#                     atexit.register(target_motor.turn_off)
#                     target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
#                     self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
#                     with open('stage_x_z_absolute_position.json', 'w') as wf:
#                         json.dump(self.stage_x_and_z_pos, wf)
#                 target_motor = xyz_motor(6, 200, 100)
#                 atexit.register(target_motor.turn_off)
#
#                 current_x_pos = self.stage_x_and_z_pos["x_pos"]
#                 relative_steps = abs(waste_abs_pos - current_x_pos)
#
#                 if current_x_pos < waste_abs_pos:  # if current_x_pos == 0, 3500
#                     target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 elif current_x_pos > waste_abs_pos:  # if current_x_pos == 12000, 16500
#                     target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
#                 # update the json file
#                 self.stage_x_and_z_pos["x_pos"] = waste_abs_pos
#                 with open('stage_x_z_absolute_position.json', 'w') as wf:
#                     json.dump(self.stage_x_and_z_pos, wf)
#                 move_to_waste = 0
#                 # Print to the LunaSrv
#                 port.write("done   \n")
#                 print "sent done to port"

class X_and_Z_Solution_Stage_Motor(Motor):

    def __init__(self):
        Motor.__init__(self)
        with open('stage_x_z_absolute_position.json') as f:
            self.stage_x_and_z_pos = json.load(f)

        # Need to check z first, then x
        """
        if (self.stage_x_and_z_pos["z_pos"] !=0):
            print "Moving Stage Z Home"
            target_motor = xyz_motor(2, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(POSDIR, self.stage_x_and_z_pos["z_pos"], MICROSTEP, HIGHCUR)  # POSDIR makes Stage Z go down
            self.stage_x_and_z_pos["z_pos"] -= self.stage_x_and_z_pos["z_pos"]
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
        if (self.stage_x_and_z_pos["x_pos"] != 0):
            print "Moving Stage X HOME"
            target_motor = xyz_motor(6, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(NEGDIR, self.stage_x_and_z_pos["x_pos"], MICROSTEP,
                              HIGHCUR)  # To move from big to big vial, increment is 4500
            self.stage_x_and_z_pos["x_pos"] -= self.stage_x_and_z_pos["x_pos"]
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
        """

    def run(self):
        # STAGE X Z edit
        # STAGE X Z edit
        global move_stageX_left_small, move_stageX_left_big, move_stageX_right_small, move_stageX_right_big, move_stageZ_up, move_stageZ_down
        global move_to_sample, move_to_buffer, move_to_water, move_to_waste

        z_stage_move_step = 6600 # 6000
        x_stage_move_step_big = 4500 # 4500
        x_stage_move_step_small = 4000 # 4000

        sample_abs_pos = 3100 #3100

        buffer_abs_pos = sample_abs_pos + x_stage_move_step_small#7100
        water_abs_pos = buffer_abs_pos + x_stage_move_step_big #11600
        waste_abs_pos = water_abs_pos + x_stage_move_step_big #16100

        while self._running:
############################## SOLUTION STATION #################################
            # Relative positioning for Solution Station X and Z
            if move_stageX_left_small:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(NEGDIR, x_stage_move_step_small, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
                self.stage_x_and_z_pos["x_pos"] -= x_stage_move_step_small
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_stageX_left_small = 0
                port.write("done  \n")
            if move_stageX_right_small:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                print "Moving Stage X RIGHT"
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(POSDIR, x_stage_move_step_small, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
                self.stage_x_and_z_pos["x_pos"] += x_stage_move_step_small
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_stageX_right_small = 0
                port.write("done   \n")
                # print "sent done to port"
            if move_stageX_left_big:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                # print "Moving Stage X LEFT"
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(NEGDIR, x_stage_move_step_big, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to big vial, increment is 4500
                self.stage_x_and_z_pos["x_pos"] -= x_stage_move_step_big
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_stageX_left_big = 0
                port.write("done   \n")
                print "sent done to port"
            if move_stageX_right_big:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                # print "Moving Stage X RIGHT"
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(POSDIR, x_stage_move_step_big, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # To move from big to big vial, increment is 4500
                self.stage_x_and_z_pos["x_pos"] += x_stage_move_step_big
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_stageX_right_big = 0
                port.write("done   \n")
                print "sent done to port"
            if move_stageZ_up:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] >= z_stage_move_step:
                    print "Stage z is already at the top"
                    move_stageZ_up = 0
                    port.write("done   \n")
                    print "sent done to port"
                else:
                    print "Moving Stage Z UP"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(NEGDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # NEGDIR makes Stage Z go up
                    self.stage_x_and_z_pos["z_pos"] += z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                    move_stageZ_up = 0
                    port.write("done   \n")
                    print "sent done to port"
            if move_stageZ_down:
                if self.stage_x_and_z_pos["z_pos"] <= 0:
                    print "Stage z is already at the very bottom"
                    move_stageZ_down = 0
                    port.write("done   \n")
                    print "sent done to port"
                else:
                    print "Moving Stage Z DOWN"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                    move_stageZ_down = 0
                    port.write("done   \n")
                    print "sent done to port"



            # Absolute positions for stage x
            if move_to_sample:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)

                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)

                current_x_pos = self.stage_x_and_z_pos["x_pos"] # get the current position from the json file
                relative_steps = abs(sample_abs_pos - current_x_pos) # find the relative pos

                # Move motor based on current_x_pos of the motor and sample_abs_pos
                if current_x_pos < sample_abs_pos: # if current_x_pos == 0
                    target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                elif current_x_pos > sample_abs_pos: # if current_x_pos == 7500, 12000, 16500
                    target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)

                self.stage_x_and_z_pos["x_pos"] = sample_abs_pos
                # update the json file
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_to_sample = 0
                # Print to the LunaSrv
                port.write("done   \n")
                print "sent done to port"

            if move_to_buffer:
                # Check to see if z is position 0, if not then bring z to home
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                # buffer_abs_pos = 7500
                current_x_pos = self.stage_x_and_z_pos["x_pos"]
                relative_steps = abs(buffer_abs_pos - current_x_pos)

                if current_x_pos < buffer_abs_pos: # if current_x_pos == 0, 3500
                    target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                elif current_x_pos > buffer_abs_pos: # if current_x_pos == 12000, 16500
                    target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                # update the json file
                self.stage_x_and_z_pos["x_pos"] = buffer_abs_pos
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_to_buffer = 0
                # Print to the LunaSrv
                port.write("done   \n")
                print "sent done to port"

            if move_to_water:
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)
                current_x_pos = self.stage_x_and_z_pos["x_pos"]
                relative_steps = abs(water_abs_pos - current_x_pos)

                if current_x_pos < water_abs_pos:  # if current_x_pos == 0, 3500
                    target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                elif current_x_pos > water_abs_pos:  # if current_x_pos == 12000, 16500
                    target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                # update the json file
                self.stage_x_and_z_pos["x_pos"] = water_abs_pos
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_to_water = 0
                # Print to the LunaSrv
                port.write("done   \n")
                print "sent done to port"

            if move_to_waste:
                if self.stage_x_and_z_pos["z_pos"] > 0:
                    print "Moving Stage Z DOWN FIRST"
                    target_motor = xyz_motor(2, 200, 100)
                    atexit.register(target_motor.turn_off)
                    target_motor.move(POSDIR, z_stage_move_step, DOUBLECOILMICROSTEP, XZSTATIONCUR)  # POSDIR makes Stage Z go down
                    self.stage_x_and_z_pos["z_pos"] -= z_stage_move_step
                    with open('stage_x_z_absolute_position.json', 'w') as wf:
                        json.dump(self.stage_x_and_z_pos, wf)
                target_motor = xyz_motor(6, 200, 100)
                atexit.register(target_motor.turn_off)

                current_x_pos = self.stage_x_and_z_pos["x_pos"]
                relative_steps = abs(waste_abs_pos - current_x_pos)

                if current_x_pos < waste_abs_pos:  # if current_x_pos == 0, 3500
                    target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                elif current_x_pos > waste_abs_pos:  # if current_x_pos == 12000, 16500
                    target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
                # update the json file
                self.stage_x_and_z_pos["x_pos"] = waste_abs_pos
                with open('stage_x_z_absolute_position.json', 'w') as wf:
                    json.dump(self.stage_x_and_z_pos, wf)
                move_to_waste = 0
                # Print to the LunaSrv
                port.write("done   \n")
                print "sent done to port"


class Laser_Motor(Motor):
    def __init__(self):
        Motor.__init__(self)

    def run(self):
        global Move_left_Laser_Enable, Move_right_Laser_Enable
        global Move_Laser_Home, LaserPos

        global Move_l_Laser_Enable, Move_r_Laser_Enable

        while self._running:
            if Move_l_Laser_Enable:
                print  "Moving Laser3 stage to the left "
                target_motor = xyz_motor(2, 200, 100)
                atexit.register(target_motor.turn_off)
                for cycle in range(1, 2000):
                    target_motor.move(NEGDIR, 1, FULLSTEP,
                                      HIGHCUR)  # Retract one step at a time until home switch active
                    time.sleep(.001)
                Move_l_Laser_Enable = 0

            if Move_r_Laser_Enable:
                print  "Moving Laser stage to the right "
                target_motor = xyz_motor(2, 200, 100)
                atexit.register(target_motor.turn_off)
                for cycle in range(1, 2000):
                    target_motor.move(POSDIR, 1, FULLSTEP,
                                      HIGHCUR)  # Retract one step at a time until home switch active
                    time.sleep(.001)
                Move_r_Laser_Enable = 0

            if Move_left_Laser_Enable:
                print  "Moving Laser stage to the left "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(NEGDIR, 2, MICROSTEP, HIGHCUR)  # Retract one step at a time until home switch active
                Move_left_Laser_Enable = 0

            if Move_right_Laser_Enable:
                print  "Moving Laser stage to the right "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(POSDIR, 2, MICROSTEP, HIGHCUR)  # Retract one step at a time until home switch active
                Move_right_Laser_Enable = 0

            class Laser_Motor(Motor):
                def __init__(self):
                    Motor.__init__(self)

                def run(self):
                    global Move_left_Laser_Enable, Move_right_Laser_Enable
                    global Move_Laser_Home, LaserPos

                    global Move_l_Laser_Enable, Move_r_Laser_Enable

                    while self._running:
                        if Move_l_Laser_Enable:
                            print  "Moving Laser3 stage to the left "
                            target_motor = xyz_motor(2, 200, 100)
                            atexit.register(target_motor.turn_off)
                            for cycle in range(1, 2000):
                                target_motor.move(NEGDIR, 1, FULLSTEP,
                                                  HIGHCUR)  # Retract one step at a time until home switch active
                                time.sleep(.001)
                            Move_l_Laser_Enable = 0

                        if Move_r_Laser_Enable:
                            print  "Moving Laser stage to the right "
                            target_motor = xyz_motor(2, 200, 100)
                            atexit.register(target_motor.turn_off)
                            for cycle in range(1, 2000):
                                target_motor.move(POSDIR, 1, FULLSTEP,
                                                  HIGHCUR)  # Retract one step at a time until home switch active
                                time.sleep(.001)
                            Move_r_Laser_Enable = 0

                        if Move_left_Laser_Enable:
                            print  "Moving Laser stage to the left "
                            target_motor = xyz_motor(3, 200, 100)
                            atexit.register(target_motor.turn_off)
                            target_motor.move(NEGDIR, 2, MICROSTEP,
                                              HIGHCUR)  # Retract one step at a time until home switch active
                            Move_left_Laser_Enable = 0

                        if Move_right_Laser_Enable:
                            print  "Moving Laser stage to the right "
                            target_motor = xyz_motor(3, 200, 100)
                            atexit.register(target_motor.turn_off)
                            target_motor.move(POSDIR, 2, MICROSTEP,
                                              HIGHCUR)  # Retract one step at a time until home switch active
                            Move_right_Laser_Enable = 0

                        if Move_Laser_Home:
                            print  "Moving Laser stage to the home switch "
                            target_motor = xyz_motor(3, 200, 100)
                            atexit.register(target_motor.turn_off)
                            HomeMax = 400
                            LaserPos = 0
                            print "Waiting for DAC addr7 input 1 Laser Home switch to become Active  high"
                            temp = 0
                            for cycle in range(1, 2):
                                temp = temp + DAC.getDINbit(7, 1)
                                time.sleep(.01)
                            if (temp >= 1):  # if home switch is active, print complete message
                                print "Input DAC(7,1) Home sensor is already active high, moving left 110 first"
                                target_motor.move(NEGDIR, 110, MICROSTEP,
                                                  HIGHCUR)  # Moving left, away from the capillary
                            temp = 0
                            for cycle in range(1, 3):
                                temp = temp + DAC.getDINbit(7, 1)
                                time.sleep(.01)
                            print "Now starting Home"
                            while ((temp == 0) and (LaserPos < HomeMax) and (
                                        Move_Laser_Home == 1)):  # if home switch not active, move 1 step
                                temp = 0
                                for cycle in range(1, 2):
                                    temp = temp + DAC.getDINbit(7, 1)
                                    time.sleep(.01)
                                target_motor.move(POSDIR, 5, MICROSTEP, HIGHCUR)  # Moving towards the capillary
                                LaserPos = LaserPos + 1

                            print "Completed Laser move to Home switch"
                            if ((DAC.getDINbit(7, 1) == 1)):  # if home switch is active, reset LaserPos
                                print "Input DAC(7,1) Laser Home sensor is Now Active high"
                                print  LaserPos
                                LaserPos = 0
                            Move_Laser_Home = 0
class Reagent_Pump(Motor):
    def __init__(self):
        Motor.__init__(self)

    def run(self):
        global Move_ReagentW_Home, Move_ReagentM_Home, Move_ReagentB_Home, Move_ReagentP_Home

        while self._running:
            if Move_ReagentW_Home:
                print  "Moving ReagentW stage to the home switch "
                target_motor = xyz_motor(2, 100, 600)
                atexit.register(target_motor.turn_off)
                HomeMax = 3800
                ReagentWPos = 0
                print "Waiting for DAC addr7 input 3 ReagentW Home switch to become Active "
                while ((DAC.getDINbit(7, 4) != 1) and (ReagentWPos < HomeMax) and (
                    Move_ReagentW_Home == 1)):  # if home switch not active, move 1 step
                    target_motor.move(NEGDIR, 1, FASTSTEP,
                                      MIDCUR)  # Retract one step at a time until home switch active
                    ReagentWPos = ReagentWPos + 1
                if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentWPos
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
                while ((DAC.getDINbit(7, 4) != 1) and (ReagentMPos < HomeMax) and (
                    Move_ReagentM_Home == 1)):  # if home switch not active, move 1 step
                    target_motor.move(NEGDIR, 1, FASTSTEP,
                                      MIDCUR)  # Retract one step at a time until home switch active
                    ReagentMPos = ReagentMPos + 1
                if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentWPos
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
                while ((DAC.getDINbit(7, 5) != 1) and (ReagentBPos < HomeMax) and (
                    Move_ReagentB_Home == 1)):  # if home switch not active, move 1 step
                    target_motor.move(NEGDIR, 1, FASTSTEP,
                                      MIDCUR)  # Retract one step at a time until home switch active
                    ReagentBPos = ReagentBPos + 1
                if ((DAC.getDINbit(7, 5) == 1)):  # if home switch is active, reset ReagentBPos
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
                while ((DAC.getDINbit(7, 6) != 1) and (ReagentPPos < HomeMax) and (
                    Move_ReagentP_Home == 1)):  # if home switch not active, move 1 step
                    target_motor.move(NEGDIR, 1, FASTSTEP,
                                      MIDCUR)  # Retract one step at a time until home switch active
                    ReagentPPos = ReagentPPos + 1
                if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentPPos
                    print "Input DAC(7,6) ReagentP Home sensor is active"
                    print  ReagentPPos
                    ReagentPPos = 0
                Move_ReagentP_Home = 0

class Gel_Pump(Motor):

    def __init__(self):
        Motor.__init__(self)

    def run(self):
        global Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
        global move_gel_pump_down, move_gel_pump_up

        while self._running:
            if move_gel_pump_up:
                """
                LOWCUR = 1  # lowest current setting is 1, max is 16
                MIDCUR = 2  # medium current setting is 2, max is 16
                HIGHCUR = 4  # high current setting is 3, max is 16
                XZSTATIONCUR = 6 # optimal current to run the X and Z solution station
                NEGDIR = -1  # Negative move direction
                POSDIR = 1  # Positive move direction

                """
                print "Moving Gel pump up"
                target_motor = xyz_motor(1, 200, 100)
                atexit.register(target_motor.turn_off)
                min = 2.0
                run_once = False
                t_end = time.time() + 60 * min
                while time.time() < t_end:
                    target_motor.move(POSDIR, 1, DOUBLECOILMICROSTEP, HIGHCUR)
                    time.sleep(0.005)
                    if (run_once): break
                print "finished"
                move_gel_pump_down = 0
                port.write("done   \n")
                print "sent done to port"

            if move_gel_pump_down:
                print "Moving Gel pump down"
                target_motor = xyz_motor(1, 200, 100)
                atexit.register(target_motor.turn_off)
                min = 2.0
                run_once = False
                t_end = time.time() + 60 * min
                while time.time() < t_end:
                    target_motor.move(NEGDIR, 1, DOUBLECOILMICROSTEP, HIGHCUR)
                    time.sleep(0.005)
                    if (run_once): break
                print "finished"
                move_gel_pump_down = 0
                port.write("done   \n")
                print "sent done to port"

            if Move_GelPump_Home:
                print  "Moving Gel Pump to the upper home switch "
                target_motor = xyz_motor(1, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 123800
                GelPos = 0
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 0)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,0) Home sensor is already active high, moving down 110 first"
                    target_motor.move(NEGDIR, 60, MICROSTEP,
                                      LOWCUR)  # Retract one step at a time until home switch active
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 0)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 0 Gel Home switch to become Active "
                while ((temp == 0) and (GelPos < HomeMax) and (
                            Move_GelPump_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 0)
                        time.sleep(.01)
                    target_motor.move(POSDIR, 10, FASTSTEP,
                                      LOWCUR)  # Go forward, up to top of gel pump to allow gel replacement
                    GelPos = GelPos + 1
                print "Completed Gel Pump move to Home switch"
                print  GelPos
                if ((DAC.getDINbit(7, 0) == 1)):  # if home switch is active, reset GelPos
                    print "Input DAC(7,0) Gel Home sensor is active high"
                    print  GelPos
                    GelPos = 0
                Move_GelPump_Home = 0

            if Move_GelPump_Start:
                target_motor = xyz_motor(1, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 123800
                GelPos = 0
                temp = 0
                print "Waiting for DAC addr7 input 2 Gel Start switch to become Active "

                for cycle in range(1, 3):
                    temp = DAC.getADC(7, 2)
                    print temp
                    time.sleep(.02)
                    if (temp == 0):  # if home switch is active, print complete message
                        print "Input DAC Analog input(7,2) Gel Start sensor is already active low, moving up to get off top"
                        target_motor.move(POSDIR, 30, FASTSTEP, LOWCUR)  # bring motor up

                ave = 5.0
                while ((ave >= 0.8) and (GelPos < HomeMax) and (
                            Move_GelPump_Start == 1)):  # if gel start switch not active, move 9 step
                    temp = 0.0
                    ave = 0.0
                    good_count = 8
                    for cycle in range(1, 9):
                        temp = DAC.getADC(7, 2)
                        time.sleep(.002)
                        if (temp > 3.1 or temp < 0.3):
                            temp = 0  # Ignore bad reads
                            good_count = good_count - 1
                            # reduce ave count to make up for bad data
                        ave = ave + temp
                        print "temp=", temp
                    if (good_count == 0): good_count = 1
                    ave = (ave / good_count)
                    time.sleep(.002)
                    print "Ave and good_count = ", ave, good_count

                    target_motor.move(NEGDIR, 9, MICROSTEP, LOWCUR)  # bring motor down one step at a time
                    GelPos = GelPos + 9

                print "Completed Gel Pump move to top of syring, steps moved =", GelPos
                temp = 0
                for cycle in range(1, 4):
                    temp = (temp + DAC.getADC(7, 2))
                    time.sleep(.02)
                print "Input Analog input(7,2) Gel Start sensor "
                print temp
                if (temp <= 5):  # if home switch is active, print complete message
                    print "Input analog DAC(7,2) Gel Start sensor is now Active Low"
                    print  GelPos
                Move_GelPump_Start = 0


            if Move_GelPump_Move:
                GelPos = 0
                print "Moving Gel Pump down 10uL  \r\n"
                target_motor = xyz_motor(1, 200, 100)
                atexit.register(target_motor.turn_off)
                target_motor.move(NEGDIR, 300, MICROSTEP, HIGHCUR)  # Go downward, gel pump down to pump gel
                GelPos = GelPos + 10
                for cycle in range(1, 10):  # Every 20 seconds pump one step
                    print "Moving Gel Pump down at 3uL per hour  \r\n"
                    time.sleep(0.2)
                    target_motor.move(NEGDIR, 1, MICROSTEP, HIGHCUR)  # Go downward, gel pump down to pump gel
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

if __name__ == "__main__":

    global Cap_Heater_Enable, Move_left_Laser_Enable, Move_right_Laser_Enable
    global Move_Laser_Home, Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
    global Move_ReagentW_Home, Move_ReagentM_Home, Move_ReagentB_Home, Move_ReagentP_Home
    global Move_l_Laser_Enable, Move_r_Laser_Enable

    global move_gel_pump_up, move_gel_pump_down
    move_gel_pump_down = move_gel_pump_up = 0.0

    #################### STAGE X Z edit ####################
    global move_stageX_left_small, move_stageX_left_big, move_stageX_right_small, move_stageX_right_big, move_stageZ_up, move_stageZ_down
    move_stageX_left_small = move_stageX_left_big = move_stageX_right_small = move_stageX_right_big = move_stageZ_up = move_stageZ_down = 0.0

    # absolute positions
    global move_to_sample, move_to_buffer, move_to_water, move_to_waste
    move_to_sample = move_to_buffer = move_to_water = move_to_waste = 0.0


    ######################################################################333333
    Move_left_Laser_Enable = Move_right_Laser_Enable = Move_ReagentW_Home = Move_l_Laser_Enable = Move_r_Laser_Enable = 0.0
    Cap_Heater_Enable = Move_Laser_Home = Move_GelPump_Home = Move_GelPump_Start = Move_GelPump_Move = 0.0
    Move_ReagentP_Home = Move_ReagentB_Home = Move_ReagentM_Home = 0
    Heat = CapHeat()  # Create Class CapHeat
    HeatThread = Thread(target=Heat.run)  # Create the thread to run Heat
    HeatThread.start()  # start runing the cap heater thread above

    # Mot = Motor()  # Create Class Motor
    # MotThread = Thread(target=Mot.run)  # Create the thread to run Heat
    # MotThread.start()  # start runing the Motor  thread above

    X_and_Z_Solution_Stage_Mot = X_and_Z_Solution_Stage_Motor()  # Create Class Motor
    X_Z_SS_Mot = Thread(target=X_and_Z_Solution_Stage_Mot.run)  # Create the thread to run Heat
    X_Z_SS_Mot.start()  # start runing the Motor  thread above

    Reagent_Pump_Mot = Reagent_Pump()
    RP_Mot = Thread(target=Reagent_Pump_Mot.run)
    RP_Mot.start()

    GelPump = Gel_Pump()
    GP_Mot = Thread(target=GelPump.run)
    GP_Mot.start()

    LaserMotor = Laser_Motor()
    LM_Mot = Thread(target=LaserMotor.run)
    LM_Mot.start()

    print "Waiting for serial commands "
    port.write("\r\nEnter Pi Cmd:")
    rcv = readlineCR(port)

    while (rcv != "EXIT"):
        # port.write("\r\nEnter Pi Cmd:")
        rcv = readlineCR(port)
        if rcv != "":
            port.write("OK        \n")
        print "recieved serial string:" + rcv

        if (rcv == "R"):
            Move_r_Laser_Enable = 1

        if (rcv == "L"):
            Move_l_Laser_Enable = 1

        if (rcv == "RWHOME"):
            Move_ReagentW_Home = 1
            print "Move_Reagent W Home Moving Home\r\n"

        if (rcv == "RMHOME"):
            Move_ReagentM_Home = 1
            print "Move_Reagent M Home Moving Home\r\n"

        if (rcv == "RPHOME"):
            Move_ReagentP_Home = 1
            print "Move_Reagent P Home Moving Home\r\n"

        if (rcv == "RBHOME"):
            Move_ReagentB_Home = 1
            print "Move_Reagent B Home Moving Home\r\n"

        if (rcv == "CAPSETT"):
            print "Capillary Heater Set temp\r\n"

        if (rcv == "CAPGETT"):
            print "Capillary Heater Get temp\r\n"

        if (rcv == "CAPHEATON"):
            Cap_Heater_Enable = 1
            print "Capillary Heater ON\r\n"

        if (rcv == "CAPHEATOFF"):
            Cap_Heater_Enable = 0
            print "Capillary Heater OFF\r\n"

        if (rcv == "LASLEFT"):
            Move_left_Laser_Enable = 1
            print "Moved Laser Motor to the left\r\n"

        if (rcv == "LASRIGHT"):
            Move_right_Laser_Enable = 1
            print "Moved Laser Motor to the right\r\n"

        if (rcv == "RET" or rcv == "LASRET"):
            Move_Laser_Home = 1
            print "Moving Laser to home switch \r\n"

        if (rcv == "GPHOME"):
            Move_GelPump_Home = 1
            print "Moving Gel Pump to Home switch \r\n"

        if (rcv == "GPSTART"):
            Move_GelPump_Start = 1
            print "Moving Gel Pump to Start switch \r\n"

        if (rcv == "GPUP"):
            move_gel_pump_up = 1
            print "Moving Gel Pump UP \r\n"

        if (rcv == "GPDOWN"):
            move_gel_pump_down = 1
            print "Moving Gel Pump DOWN \r\n"

        if (rcv == "GPRATE"):
            Move_GelPump_Move = 1
            print "Moving Gel Pump to position \r\n"

        # STAGE X Z edit
        if (rcv == "SXLFTSM"):
            move_stageX_left_small = 1
            print "Moving Stage X to the left towards the small vial \r\n"
        if (rcv == "SXRGHTSM"):
            move_stageX_right_small = 1
            print "Moving Stage X to the right towards the small vial \r\n"
        if (rcv == "SXLFTBIG"):
            move_stageX_left_big = 1
            print "Moving Stage X to the left towards a big vial \r\n"
        if (rcv == "SXRGHTBIG"):
            move_stageX_right_big = 1
            print "Moving Stage X to the right towards a big vial \r\n"
        if (rcv == "STAGEZUP"):
            move_stageZ_up = 1
            print "Moving Stage Z up by an increment\r\n"
        if (rcv == "STAGEZDN"):
            move_stageZ_down = 1
            print "Moving Stage Z down by an increment\r\n"

        if (rcv == "SXSAMPLE"):
            move_to_sample = 1
            print "Moving Stage X to sample! \r\n"

        if (rcv == "SXBUFFER"):
            move_to_buffer = 1
            print "Moving Stage X to buffer! \r\n"

        if (rcv == "SXWATER"):
            move_to_water = 1
            print "Moving Stage X to water! \r\n"

        if (rcv == "SXWASTE"):
            move_to_waste = 1
            print "Moving Stage X to waste! \r\n"


        if (rcv == "K") or (rcv == "KILL") or (rcv == "QUIT") or (rcv == "Q"):
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

        if (rcv == "?"):
            print "CAPHEATON CAPHEATOFF LASLEFT LASRIGHT L  R  LASHOME GPHOME GPSTART GPRATE Q QUIT L R\r\n"
            print "STAGEXRIGHT STAGEXLEFT STAGEZUP STAGEZDN\r\n"
            port.write("CAPHEATON CAPHEATOFF LASLEFT LASRIGHT L  R  LASHOME GPHOME GPSTART GPRATE Q QUIT L R\r\n")

    st1.termintate()
    target_motor.turn_off()
