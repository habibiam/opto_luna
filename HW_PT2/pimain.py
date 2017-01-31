#!/usr/bin/python
import time
import atexit
import sys
import spidev
import json
import serial
import DAQCplate as DAC
import RPi.GPIO as GPIO, os
import piplates.RELAYplate as RELAY

from CapHeat_DAC import CapHeat
from threading import Thread
from Gel_Pump import Gel_Pump
# from Solenoid import Solenoid
from xyz_motor import xyz_motor
from X_and_Z_Solution_Stage import X_and_Z_Solution_Stage
from Laser_Motor import Laser_Motor
from Reagent_Pump import Reagent_Pump
# from Solenoid_Sequence import Solenoid_Sequence
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor


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
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=60.0)

# class xyz_motor(object):
#     """Initialise the motor object.
#
#        axies       -- which motor to move
#                    1: X Motor
#                    2: Y_Motor
#                    3: Z_Motor
#                    Other: Invalid
#
#                    1: Normal connection (forward (moving away from the motor)-- positive steps)
#                    -1: Reversed connection (forward (moving away from the motor) -- negative steps)
#                    Other: Invalid
#
#        step_mode     -- which stepping mode to drive the motor
#                    1: Single coil steps
#                    2: Double coil steps
#                    3: Interleaved coil steps
#                    4: Microsteps
#
#        rpm       -- to set the rounds per minute
#
#        move_steps    -- to set how many steps to move
#                    actual_move_steps = move_steps*board_sku
#                    if actual_move_steps is postive it moves forward (away from the motor)
#                    if actual_move_steps is negative it moves backward (near to the motor)
#     """
#
#     def __init__(self, axies, steps_per_rev, rpm):
#
#         if axies == 1:  # Board 1,GelPump  pins M1 and M2
#             self.driver_hat = Opto_MotorHAT(addr=0x60)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
#         elif axies == 2:  # Board 1, pins M3 and M4
#             self.driver_hat = Opto_MotorHAT(addr=0x60)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
#         elif axies == 3:  # Board 2, pins M1 and M2
#             self.driver_hat = Opto_MotorHAT(addr=0x61)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
#         elif axies == 4:  # Board 2, pins M3 and M4
#             self.driver_hat = Opto_MotorHAT(addr=0x61)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
#         elif axies == 5:  # Board 3, pins M1 and M2
#             self.driver_hat = Opto_MotorHAT(addr=0x62)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
#         elif axies == 6:  # Board 3, pins M3 and M4
#             self.driver_hat = Opto_MotorHAT(addr=0x62)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
#         elif axies == 7:  # Board 4, pins M1 and M2
#             self.driver_hat = Opto_MotorHAT(addr=0x63)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 1)
#         elif axies == 8:  # Board 4, pins M3 and M4
#             self.driver_hat = Opto_MotorHAT(addr=0x63)
#             self.stepper_motor = self.driver_hat.getStepper(steps_per_rev, 2)
#         else:
#             print "Please choose the correct motor from below:"
#             print "  1: X_Motor\n  2: Y_Motor\n  3: Z_Motor"
#             sys.exit(0)
#         self.stepper_motor.setSpeed(rpm * 15)
#
#     def move(self, board_sku, move_steps, step_mode, current):
#         if (board_sku == 1) or (board_sku == -1):
#             actual_move_steps = board_sku * move_steps
#         else:
#             print "Please choose the correct board sku:"
#             print "  1: Normal Connection\n  -1: Reversed Connection"
#             self.turn_off()
#             sys.exit(0)
#
#         if actual_move_steps >= 0:
#             if step_mode == 1:
#                 self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.SINGLE, current)
#             elif step_mode == 2:
#                 self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.DOUBLE, current)
#             elif step_mode == 3:
#                 self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.INTERLEAVE, current)
#             elif step_mode == 4:
#                 self.stepper_motor.step(actual_move_steps, Opto_MotorHAT.FORWARD, Opto_MotorHAT.MICROSTEP, current)
#             else:
#                 print "Please choose the correct stepper mode:"
#                 print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
#                 self.turn_off()
#                 sys.exit(0)
#         else:
#             if step_mode == 1:
#                 self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.SINGLE, current)
#             elif step_mode == 2:
#                 self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.DOUBLE, current)
#             elif step_mode == 3:
#                 self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.INTERLEAVE, current)
#             elif step_mode == 4:
#                 self.stepper_motor.step(-actual_move_steps, Opto_MotorHAT.BACKWARD, Opto_MotorHAT.MICROSTEP, current)
#             else:
#                 print "Please choose the correct stepper mode:"
#                 print "  1: Single Coil Steps\n  2: Double Coil Steps\n  3: Interleaved Coil Steps\n  4: Microsteps"
#                 self.turn_off()
#                 sys.exit(0)
#
#     def turn_off(self):
#         self.driver_hat.getMotor(1).run(Opto_MotorHAT.RELEASE)
#         self.driver_hat.getMotor(2).run(Opto_MotorHAT.RELEASE)
#         self.driver_hat.getMotor(3).run(Opto_MotorHAT.RELEASE)
#         self.driver_hat.getMotor(4).run(Opto_MotorHAT.RELEASE)


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

if __name__ == "__main__":
    ######################### Create Class Object ############################

    Heat = CapHeat()

    GelPump = Gel_Pump()

    LaserMotor = Laser_Motor()

    Reagent_Pump_Mot = Reagent_Pump()

    X_Z_Solution_Station = X_and_Z_Solution_Stage()

    #########################################################################

    # global Cap_Heater_Enable, Move_left_Laser_Enable, Move_right_Laser_Enable
    # global Move_Laser_Home, Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
    # global Move_ReagentW_Home, Move_ReagentM_Home, Move_ReagentB_Home, Move_ReagentP_Home
    # global Move_l_Laser_Enable, Move_r_Laser_Enable
    #
    # global move_gel_pump_up, move_gel_pump_down
    # move_gel_pump_down = move_gel_pump_up = 0.0
    #
    # #################### STAGE X Z edit ####################
    # global move_stageX_left_small, move_stageX_left_big, move_stageX_right_small, move_stageX_right_big, move_stageZ_up, move_stageZ_down
    # move_stageX_left_small = move_stageX_left_big = move_stageX_right_small = move_stageX_right_big = move_stageZ_up = move_stageZ_down = 0.0
    #
    # # absolute positions
    # global move_to_sample, move_to_buffer, move_to_water, move_to_waste
    # move_to_sample = move_to_buffer = move_to_water = move_to_waste = 0.0

    print "Waiting for serial commands "
    port.write("\r\nEnter Pi Cmd:")
    rcv = readlineCR(port)

    while (rcv != "EXIT"):
        # port.write("\r\nEnter Pi Cmd:")
        rcv = readlineCR(port)
        if rcv != "":
            port.write("OK        \n")
        print "recieved serial string:" + rcv

        if (rcv == "RMHOME"):
            print "Move_Reagent M Home Moving Home Main \r\n"
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentM_home)
            RP_Mot.start()

        if (rcv == "RPHOME"):
            print "Move_Reagent P Home Moving Home\r\n"
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentP_home)
            RP_Mot.start()

        if (rcv == "RWHOME"):
            print "Move_Reagent W Home Moving Home\r\n"
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentW_home)
            RP_Mot.start()

        if (rcv == "RSHOME"):
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentS_home)
            RP_Mot.start()
            print "Move_Reagent S Home Moving Home\r\n"

        if (rcv == "RBHOME"):
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentB_home)
            RP_Mot.start()
            print "Move_Reagent B Home Moving Home\r\n"

        if (rcv == "REHOME"):
            RP_Mot = Thread(target=Reagent_Pump_Mot.move_reagentE_home)
            RP_Mot.start()
            print "Move_Reagent E Home Moving Home\r\n"

        if (rcv == "CAPHEATON"):
            print "Capillary Heater ON\r\n"
            HeatThread = Thread(target=Heat.Cap_Heater_Enable)  # Create the thread to run Heat
            HeatThread.start()  # start runing the cap heater thread above

        if (rcv == "CAPHEATOFF"):
            print "Capillary Heater OFF\r\n"
            HeatThread = Thread(target=Heat.Cap_Heater_Off)  # Create the thread to run Heat
            HeatThread.start()  # start runing the cap heater thread above

        if (rcv == "LASLEFT"):
            LM_Mot = Thread(target=LaserMotor.Move_left_Laser_Enable)
            LM_Mot.start()

        if (rcv == "LASRIGHT"):
            LM_Mot = Thread(target=LaserMotor.Move_right_Laser_Enable)
            LM_Mot.start()

        if (rcv == "RET" or rcv == "LASRET" or rcv == "LASHOME"):
            print "Moving Laser to home switch \r\n"
            LM_Mot = Thread(target=LaserMotor.Move_Laser_Home)
            LM_Mot.start()

        if (rcv == "GPHOME"):
            print "Moving Gel Pump to Home switch \r\n"
            GP_Mot = Thread(target=GelPump.move_gelPump_home)
            GP_Mot.start()

        if (rcv == "GPSTART"):
            print "Moving Gel Pump to Start switch \r\n"
            GP_Mot = Thread(target=GelPump.move_gelPump_start)
            GP_Mot.start()

        if (rcv == "GPUP"):
            print "Moving Gel Pump UP \r\n"
            GP_Mot = Thread(target=GelPump.move_gel_pump_up)
            GP_Mot.start()

        if (rcv == "GPDOWN"):
            print "Moving Gel Pump DOWN \r\n"
            GP_Mot = Thread(target=GelPump.move_gel_pump_down)
            GP_Mot.start()

        if (rcv == "GPRATE"):
            Move_GelPump_Move = 1
            print "Moving Gel Pump to position \r\n"

        # STAGE X Z edit
        if (rcv == "SXLFTSM"):
            print "Moving Stage X to the left towards the small vial \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageX_left_small)
            XZ_SS.start()
        if (rcv == "SXRGHTSM"):
            print "Moving Stage X to the right towards the small vial \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageX_right_small)
            XZ_SS.start()
        if (rcv == "SXLFTBIG"):
            print "Moving Stage X to the left towards a big vial \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageX_left_big)
            XZ_SS.start()
        if (rcv == "SXRGHTBIG"):
            print "Moving Stage X to the right towards a big vial \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageX_right_big)
            XZ_SS.start()
        if (rcv == "STAGEZUP"):
            print "Moving Stage Z up by an increment\r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageZ_up)
            XZ_SS.start()
        if (rcv == "STAGEZDN"):
            print "Moving Stage Z down by an increment\r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_stageZ_down)
            XZ_SS.start()
        if (rcv == "SXSAMPLE"):
            print "Moving Stage X to sample! \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_to_sample)
            XZ_SS.start()
        if (rcv == "SXBUFFER"):
            print "Moving Stage X to buffer! \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_to_buffer)
            XZ_SS.start()

        if (rcv == "SXWATER"):
            print "Moving Stage X to water! \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_to_water)
            XZ_SS.start()

        if (rcv == "SXWASTE"):
            print "Moving Stage X to waste! \r\n"
            XZ_SS = Thread(target=X_Z_Solution_Station.move_to_waste)
            XZ_SS.start()


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
