#!/usr/bin/python
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor
import time
import atexit
import sys
import RPi.GPIO as GPIO, os
import spidev
import json
import serial

I2C60 = 1
I2C61 = 0
I2C62 = 2
I2C63 = 3
FASTSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
FULLSTEP = 1  # This is Full Stepping mode, use to home motors at fastest speed
MICROSTEP = 4  # This is 16 micro step per full step mode, use to precise position or for pumping slowly
DOUBLESTEP = 2 # Wei

LOWCUR = 1  # lowest current setting is 1, max is 16
MIDCUR = 2  # medium current setting is 2, max is 16
HIGHCUR = 4  # high current setting is 3, max is 16
LASCUR = 3 #4
REAGENTCUR = 4
GELCUR = 2
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

def readlineusbCR(usbport):
    """
    Used for when the pi is the LunaSrv. Replacement/no external PC
    :param usbport:
    :return:
    """
    rv = ""
    while True:
        ch = usbport.read()
        if ch >= 'a' and ch <= 'z':
            # ch = ch - ' '
            print "USE CAPS"
            #port.write("USE CAPS\r\n")
        if ch == '\r' or ch == '\n' or ch == '':
            return rv
        rv += ch

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

# port is rs232 on the GPIO header pins 6,8,10
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=60.0)

# usbport is the usb port on the ras pi
#usbport = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1.0)

# usb00port is the usb port 00 on the ras pi
#usb00port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1.0)


class Motor:
    def __init__(self):
        self._running = True
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
    def terminate(self):
        self._running = False

    def run(self):
        pass

class Reagent_Pump(Motor):
    def __init__(self):
        Motor.__init__(self)

    def run(self):
        global Move_ReagentM_Home
        global Move_ReagentP_Home
        global Move_ReagentW_Home
        global Move_ReagentS_Home
        global Move_ReagentE_Home
        global Move_ReagentB_Home
        
        while self._running:
            #time.sleep(30)
            time.sleep(2)

            ################################################################################
            if Move_ReagentM_Home:
                print  "Moving Reagent M Pump to the home switch "
                target_motor = xyz_motor(7, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 23800
                ReagentMPos = 0
                temp = 0
                target_motor.move(NEGDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move up 
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 3)
                    if ( temp > 0):
                         print "Input DAC(7,3) Home sensor is already active high"
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,3) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 3)
                    if ( temp >= 1):
                         print "Input DAC(7,3) Home sensor is already active high"
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 3 Home switch to become Active "
                while ((temp == 0) and (ReagentMPos < HomeMax) and (
                    Move_ReagentM_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 3)
                        if ( temp > 0):
                            print "Input DAC(7,3) Home sensor is already active high"
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    ReagentMPos = ReagentMPos + 50
                print "Completed ReagentMPos Pump move to Home switch"
                print  ReagentMPos
                if ((DAC.getDINbit(7, 3) == 1)):  # if home switch is active, reset ReagentMPos
                    print "Input DAC(7,3) ReagentMPos Home sensor is active high"
                    print  ReagentMPos
                    ReagentMPos = 0
                Move_ReagentM_Home = 0
                
            ################################################################################
            if Move_ReagentP_Home:
                print  "Moving Reagent P Pump to the home switch "
                target_motor = xyz_motor(8, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 23800
                ReagentPPos = 0
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 4)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,4) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 4)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 4 Home switch to become Active "
                while ((temp == 0) and (ReagentPPos < HomeMax) and (
                    Move_ReagentP_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 4)
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    ReagentPPos = ReagentPPos + 1
                print "Completed ReagentPPos Pump move to Home switch"
                print  ReagentPPos
                if ((DAC.getDINbit(7, 4) == 1)):  # if home switch is active, reset ReagentPPos
                    print "Input DAC(7,4) ReagentPPos Home sensor is active high"
                    print  ReagentPPos
                    ReagentPPos = 0
                Move_ReagentP_Home = 0
                
            ################################################################################    
            if Move_ReagentW_Home:
                print  "Moving Reagent W Pump to the home switch "
                target_motor = xyz_motor(9, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 23800
                ReagentWPos = 0
                temp = 0
                target_motor.move(NEGDIR, 6000, DOUBLESTEP, REAGENTCUR)  # Move up 
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 5)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,5) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 5)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 5 Home switch to become Active "
                while ((temp == 0) and (ReagentWPos < HomeMax) and (
                    Move_ReagentW_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 5)
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    ReagentWPos = ReagentWPos + 50
                print "Completed ReagentWPos Pump move to Home switch"
                print  ReagentWPos
                if ((DAC.getDINbit(7, 5) == 1)):  # if home switch is active, reset ReagentWPos
                    print "Input DAC(7,5) ReagentWPos Home sensor is active high"
                    print  ReagentWPos
                    ReagentWPos = 0
                Move_ReagentW_Home = 0
                
            ################################################################################
            if Move_ReagentS_Home:
                print  "Moving Reagent S Pump to the home switch "
                target_motor = xyz_motor(10, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 23800
                ReagentSPos = 0
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 6)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,6) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 6)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 6 Home switch to become Active "
                print  "Moving Reagent S Pump to the home switch, input 6 "
                while ((temp == 0) and (ReagentSPos < HomeMax) and (
                    Move_ReagentS_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 6)
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentSPos
                        print "Input DAC(7,6) ReagentSPos Home sensor is active high"
                    ReagentSPos = ReagentSPos + 1
                print "Completed ReagentSPos Pump move to Home switch"
                print  ReagentSPos
                if ((DAC.getDINbit(7, 6) == 1)):  # if home switch is active, reset ReagentSPos
                    print "Input DAC(7,6) ReagentSPos Home sensor is active high"
                    print  ReagentSPos
                    ReagentSPos = 0
                Move_ReagentS_Home = 0
                
            ################################################################################
            if Move_ReagentE_Home:
                print  "Moving Reagent E Pump to the home switch "
                target_motor = xyz_motor(11, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 23800
                ReagentEPos = 0
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 7)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,7) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 7)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 7 Home switch to become Active "
                while ((temp == 0) and (ReagentEPos < HomeMax) and (
                    Move_ReagentE_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    ReagentEPos = ReagentEPos + 1
                print "Completed ReagentEPos Pump move to Home switch"
                print  ReagentEPos
                if ((DAC.getDINbit(7, 7) == 1)):  # if home switch is active, reset ReagentEPos
                    print "Input DAC(7,7) ReagentEPos Home sensor is active high"
                    print  ReagentEPos
                    ReagentEPos = 0
                Move_ReagentE_Home = 0
                
            ################################################################################
            if Move_ReagentB_Home:
                print  "Moving Reagent B Pump to the home switch "
                target_motor = xyz_motor(12, 200, 100)
                atexit.register(target_motor.turn_off)
                HomeMax = 18000
                ReagentBPos = 0
                temp = 0
                target_motor.move(NEGDIR, 8000, DOUBLESTEP, REAGENTCUR)  # Move up 
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 8)
                    time.sleep(.01)
                if (temp >= 1):  # if home switch is active, print complete message
                    print "Input DAC(7,8) Home sensor is already active high, moving up 2000"
                    target_motor.move(NEGDIR, 2000, DOUBLESTEP, REAGENTCUR)  # Move up 
                temp = 0
                for cycle in range(1, 2):
                    temp = temp + DAC.getDINbit(7, 8)
                    time.sleep(.01)
                print "Starting Home, for DAC addr7 input 8 Home switch to become Active "
                while ((temp == 0) and (ReagentBPos < HomeMax) and (
                    Move_ReagentB_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 8)
                        time.sleep(.01)
                    target_motor.move(POSDIR, 50, DOUBLESTEP, REAGENTCUR)  # Move down to switch
                    ReagentBPos = ReagentBPos + 50
                print "Completed ReagentBPos Pump move to Home switch"
                print  ReagentBPos
                if ((DAC.getDINbit(7, 8) == 1)):  # if home switch is active, reset ReagentBPos
                    print "Input DAC(7,8) ReagentBPos Home sensor is active high"
                    print  ReagentBPos
                    ReagentBPos = 0
                Move_ReagentB_Home = 0
  

class Gel_Pump(Motor):

    def __init__(self):
        Motor.__init__(self)

    def terminate(self):
        self._running = False

    def run(self):
        global Move_GelPump_Home
        global Move_GelPump_Start
        global Move_GelPump_Move
        global move_gel_pump_down
        global move_gel_pump_up

        while self._running:
            
            time.sleep(2)
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
                    target_motor.move(POSDIR, 1, DOUBLESTEP, HIGHCUR)
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
                    target_motor.move(NEGDIR, 1, DOUBLESTEP, HIGHCUR)
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
                    target_motor.move(NEGDIR, 60, DOUBLESTEP, GELCUR)
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
                    target_motor.move(POSDIR, 10, DOUBLESTEP, GELCUR)
                    GelPos = GelPos + 1
                print "Completed Gel Pump move to Home switch"
                print  GelPos
                if ((DAC.getDINbit(7, 0) == 1)):  # if home switch is active, reset GelPos
                    print "Input DAC(7,0) Gel Home sensor is active high"
                    print  GelPos
                    GelPos = 0
                Move_GelPump_Home = 0

            if Move_GelPump_Start:
                for cycle in range(1, 2):
                   print "moving 10 rev "
                   target_motor = xyz_motor(1, 200, 100)  # 10 rev per second velocity
                   target_motor.move(POSDIR, 600, DOUBLESTEP, GELCUR) #10
   
                   print "moving 10 rev  "
                   target_motor = xyz_motor(1, 200, 100)  # 10 rev per second velocity
                   target_motor.move(NEGDIR, 600, DOUBLESTEP, GELCUR) #10


                '''
                target_motor = xyz_motor(1, 200, 100)
                HomeMax = 123800
                GelPos = 0
                temp = 0
                print "Waiting for DAC addr7 Analog input 2 (index start at 0) Gel Start switch to become Active "

                for cycle in range(1, 3):
                    temp = DAC.getADC(7, 1)
                    print temp
                    time.sleep(.02)
                    if (temp == 0):  # if home switch is active, print complete message
                        print "Input DAC Analog input(7,1) Gel Start sensor is already active low, moving up to get off top"
                        target_motor.move(POSDIR, 10, DOUBLESTEP, GELCUR)

                ave = 5.0
                while ((ave >= 0.8) and (GelPos < HomeMax) and (
                            Move_GelPump_Start == 1)):  # if gel start switch not active, move 9 step
                    temp = 0.0
                    ave = 0.0
                    good_count = 8
                    for cycle in range(1, 9):
                        temp = DAC.getADC(7, 1)
                        time.sleep(.001)
                        if (temp > 4.1 or temp < 0.3):
                            temp = 0  # Ignore bad reads
                            good_count = good_count - 1
                            # reduce ave count to make up for bad data
                        ave = ave + temp
                        print "temp=", temp
                    if (good_count == 0): good_count = 1
                    ave = (ave / good_count)
                    time.sleep(.002)
                    print "Ave and good_count = ", ave, good_count

                    target_motor.move(NEGDIR, 10, DOUBLESTEP, GELCUR) #10
                    GelPos = GelPos + 9

                print "Completed Gel Pump move to top of syring, steps moved =", GelPos
                temp = 0
                for cycle in range(1, 4):
                    temp = (temp + DAC.getADC(7, 1))
                    time.sleep(.02)
                print "Input Analog input(7,1) Gel Start sensor "
                print temp
                if (temp <= 5):  # if home switch is active, print complete message
                    print "Input analog DAC(7,1) Gel Start sensor is now Active Low"
                    print  GelPos
                '''
                Move_GelPump_Start = 0

class Laser_Motor(Motor):
    def __init__(self):
        Motor.__init__(self)

    def run(self):
        global Move_left_Laser_Enable
        global Move_right_Laser_Enable
        global Move_Laser_Home
        global LaserPos
        global Move_l_Laser_Enable
        global Move_r_Laser_Enable

        while self._running:
            time.sleep(2)

            # Move_l and Move_left has different .move function setting
            if Move_l_Laser_Enable:
                print  "Moving Laser3 stage to the left "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                for cycle in range(1, 300):
                     target_motor.move(POSDIR, 1, DOUBLESTEP, LASCUR)  # Move down to switch
                     time.sleep(.013)
                Move_l_Laser_Enable = 0
                
            if Move_r_Laser_Enable:
                print  "Moving Laser stage to the right "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                for cycle in range(1, 300):
                     target_motor.move(NEGDIR, 1, DOUBLESTEP, LASCUR)  # Move down to switch
                     time.sleep(.013)
                Move_r_Laser_Enable = 0
                
            if Move_left_Laser_Enable:
                print  "Moving Laser stage to the left "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                # Retract one step at a time until home switch active
                target_motor.move(POSDIR, 500, MICROSTEP, LASCUR)  
                Move_left_Laser_Enable = 0

            if Move_right_Laser_Enable:
                print  "Moving Laser stage to the right "
                target_motor = xyz_motor(3, 200, 100)
                atexit.register(target_motor.turn_off)
                # Retract one step at a time until home switch active
                target_motor.move(NEGDIR, 500, MICROSTEP, LASCUR)  
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
                    target_motor.move(POSDIR, 60, MICROSTEP,
                                      LASCUR)  # Moving left, away from the capillary 110
                temp = 0
                for cycle in range(1, 2):  # 1, 3
                    temp = temp + DAC.getDINbit(7, 1)
                    time.sleep(.01)
                print "Now starting Home"
                while ((temp == 0) and (LaserPos < HomeMax) and (
                            Move_Laser_Home == 1)):  # if home switch not active, move 1 step
                    temp = 0
                    for cycle in range(1, 2):
                        temp = temp + DAC.getDINbit(7, 1)
                        time.sleep(.01)
                    target_motor.move(NEGDIR, 10, MICROSTEP, LASCUR)  # Moving towards the capillary 5
                    LaserPos = LaserPos + 1

                print "Completed Laser move to Home switch"
                if ((DAC.getDINbit(7, 1) == 1)):  # if home switch is active, reset LaserPos
                    print "Input DAC(7,1) Laser Home sensor is Now Active high"
                    print  LaserPos
                    LaserPos = 0
                Move_Laser_Home = 0
                

import piplates.RELAYplate as RELAY

class Solenoid:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global Solenoid_Enable
        global Solenoid_Off

        RELAY.getID(0)

        while self._running:

            #time.sleep(30)
            time.sleep(2)

            if Solenoid_Off:
                
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
                Solenoid_Off = 0.0

            if Solenoid_Enable:
                
                #Cap_Heater_Enable = 1

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
                
                #"""
                           
                time.sleep(1)
                Solenoid_Enable = 0

class Solenoid_Sequence:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global S_Sequence_Enable     #start running sequence

        RELAY.getID(0)

        while self._running:
            #time.sleep(30)
            time.sleep(2)

            def Manifold_Off():      #turn off all solenoids in Manifold

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

            def PA_Off():         #turn off all solenoids in Pump Array
                
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
                
            def Manifold_On():      #turn on all solenoids in Manifold
                
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

            def PA_On():            #turn on all solenoids in Pump Array
                
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

            def Dispense_or_Elute_Water():

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
                
            def Mix_Sample():

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
                
            def Move_PCR():

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
                
            def PCR_Injection():

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
                
            def Injection():

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
                                
            if S_Sequence_Enable:
                
                print "Step1 \r\n"
                Manifold_On()
                PA_Off()
                time.sleep(10)
                
                print "Step2 \r\n"
                Dispense_or_Elute_Water()
                time.sleep(10)

                print "Step3 \r\n"
                Manifold_On()
                PA_Off()
                time.sleep(10)
                
                print "Step4"
                Dispense_or_Elute_Water()
                time.sleep(10)
                
                print "Step5"
                DAC.setDOUTbit(7, 0)
                Manifold_On()
                RELAY.relayOFF(0,3)   
                time.sleep(10)
            
                print "Step6"
                DAC.clrDOUTbit(7, 0)
                Manifold_On()
                RELAY.relayOFF(0,2)   # turn oN the heater on relay plate addr 0 relay number 1
                time.sleep(.22)
                RELAY.relayON(0,4)   # turn oN the heater on relay plate addr 0 relay number 1
                time.sleep(.22)
                RELAY.relayON(0,6)   # turn oN the heater on relay plate addr 0 relay number 1
                time.sleep(10)
                
                print "Step7"
                Manifold_On()
                PA_Off()
                time.sleep(10)
                
                print "Step8"
                Manifold_On()
                RELAY.relayON(0,4)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
                time.sleep(.22)
                RELAY.relayON(0,5)   # turn ON the P.A._Solenoid4 on relay plate addr 0 relay number 5
                time.sleep(.22)
                RELAY.relayON(0,6)   # turn ON the P.A._Solenoid5 on relay plate addr 0 relay number 6
                time.sleep(.22)
                RELAY.relayON(0,7)   # turn ON the P.A._Solenoid6 on relay plate addr 0 relay number 7
                time.sleep(10)
                
                print "Step9"
                Manifold_On()
                PA_Off()
                RELAY.relayON(0,2)   # turn ON the P.A._Solenoid3 on relay plate addr 0 relay number 4
                time.sleep(10)
                
                print "Step10"
                Mix_Sample()
                time.sleep(10)
                
                print "Step11"
                Move_PCR()
                time.sleep(10)
                
                print "Step12"
                Manifold_On()
                PA_Off()
                time.sleep(10)
                
                print "Step13"
                PCR_Injection()
                time.sleep(10)
                
                print "Step14"
                Manifold_On()
                RELAY.relayOFF(0,2)
                time.sleep(.22)
                RELAY.relayOFF(0,3)
                time.sleep(.22)
                RELAY.relayON(1,2)
                time.sleep(10)
                
                print "Step15"
                Manifold_On()
                PA_Off()
                time.sleep(10)
                
                print "Step16"
                Manifold_On()
                RELAY.relayON(1,2)
                time.sleep(.22)
                RELAY.relayON(1,3)
                time.sleep(10)
                
                print "Step17"
                Injection()
                PA_Off()
                time.sleep(10)
                
                print "Step18"
                Manifold_Off()
                PA_On()
                time.sleep(10)
                
                print "Step19"
                Manifold_Off()
                PA_Off()
                
                time.sleep(2)
                
                S_Sequence_Enable = 0

class CapHeat:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global Cap_Heater_Enable
        global Cap_Heater_Off

        RELAY.getID(0)

        while self._running:
            #time.sleep(30)
            time.sleep(2)

            while Cap_Heater_Enable:
                print  "Heating ON, Capillary temperature voltage is "
                RELAY.toggleLED(0)
                time.sleep(2)

                temp = DAC.getADC(7, 0)
                time.sleep(.02)
                for cycle in range(1, 10):
                    temp = DAC.getADC(7, 0)  # DAQC Board addr 7 input 0
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
                    RELAY.relayON(0,1)   # turn oN the heater on relay plate addr 0 relay number 1
                    RELAY.toggleLED(0)
                    # print  "Heating ON, Capillary temperature voltage is "
                    # print  temp
                    time.sleep(.022)
                if (temp <= 1.86):
                    RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
                    RELAY.toggleLED(0)
                    time.sleep(.022)

            if Cap_Heater_Off:

                print  "Heating OFF \r\n"
                RELAY.relayOFF(0,1)   # turn off the heater on relay plate addr 0 relay number 1
                time.sleep(.022)
                time.sleep(2)
                Cap_Heater_Off = Cap_Heater_Enable = 0.0

import DAQCplate as DAC
from threading import Thread

if __name__ == "__main__":

    global Solenoid_Enable
    global Solenoid_Off
    global S_Sequence_Enable
    global Cap_Heater_Enable
    global Cap_Heater_Off
    global Move_ReagentM_Home, Move_ReagentP_Home
    global Move_ReagentW_Home, Move_ReagentS_Home 
    global Move_ReagentE_Home, Move_ReagentB_Home
    global Move_left_Laser_Enable, Move_right_Laser_Enable
    global Move_l_Laser_Enable, Move_r_Laser_Enable, Move_Laser_Home
    global Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
    global move_gel_pump_up, move_gel_pump_down

    move_gel_pump_down = move_gel_pump_up = 0.0

    ######################################### STAGE X Z edit #############################################
    global move_stageX_left_small, move_stageX_left_big
    global move_stageX_right_small, move_stageX_right_big
    global move_stageZ_up, move_stageZ_down
    
    move_stageX_left_small = move_stageX_left_big = move_stageX_right_small = move_stageX_right_big = move_stageZ_up = move_stageZ_down = 0.0

    # absolute positions
    global move_to_sample, move_to_buffer, move_to_water, move_to_waste
    
    move_to_sample = move_to_buffer = move_to_water = move_to_waste = 0.0


    #######################################################################################################

    Move_left_Laser_Enable = Move_right_Laser_Enable = Move_l_Laser_Enable = Move_r_Laser_Enable = Move_Laser_Home = 0.0 
    Solenoid_Enable = 0.0
    Solenoid_Off = 0.0
    S_Sequence_Enable = 0.0
    Cap_Heater_Enable = 0.0
    Cap_Heater_Off = 0.0
    Move_GelPump_Home = Move_GelPump_Start = Move_GelPump_Move = 0.0    
    Move_ReagentM_Home = Move_ReagentP_Home = 0.0
    Move_ReagentW_Home = Move_ReagentS_Home = 0.0
    Move_ReagentE_Home = Move_ReagentB_Home = 0.0

    Sol = Solenoid()  # Create Class Solenoid
    SolThread = Thread(target=Sol.run)  # Create the thread to run Solenoid

    Sequence = Solenoid_Sequence()
    SeqThread = Thread(target=Sequence.run)
    SeqThread.start()

    Heat = CapHeat()  # Create Class CapHeat
    HeatThread = Thread(target=Heat.run)  # Create the thread to run Heat
    HeatThread.start()  # start runing the cap heater thread above

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
    rcv = ""

    while (rcv != "EXIT"):
        # port.write("\r\nEnter Pi Cmd:")
        rcv = readlineCR(port)
        if rcv != "":
            port.write("OK        \n")
        print "recieved serial string:" + rcv

        if (rcv == "S"):
            SolThread.start()  # start runing the Solenoid thread above
            Solenoid_Enable = 1

        if (rcv == "SF"):
            Solenoid_Off = 1

        if (rcv == "SEQ"):
            S_Sequence_Enable = 1

        if (rcv == "R"):
            Move_r_Laser_Enable = 1

        if (rcv == "L"):
            Move_l_Laser_Enable = 1

        if (rcv == "RMHOME"):
            Move_ReagentM_Home = 1
            print "Move_Reagent M Home Moving Home\r\n"

        if (rcv == "RPHOME"):
            Move_ReagentP_Home = 1
            print "Move_Reagent P Home Moving Home\r\n"

        if (rcv == "RWHOME"):
            Move_ReagentW_Home = 1
            print "Move_Reagent W Home Moving Home\r\n"
            
        if (rcv == "RSHOME"):
            Move_ReagentS_Home = 1
            print "Move_Reagent S Home Moving Home\r\n"
            
        if (rcv == "RBHOME"):
            Move_ReagentB_Home = 1
            print "Move_Reagent B Home Moving Home\r\n"

        if (rcv == "REHOME"):
            Move_ReagentE_Home = 1
            print "Move_Reagent E Home Moving Home\r\n"

        if (rcv == "CAPSETT"):
            print "Capillary Heater Set temp\r\n"

        if (rcv == "CAPGETT"):
            print "Capillary Heater Get temp\r\n"

        if (rcv == "CAPHEATON"):
            Cap_Heater_Enable = 1
            HeatThread.start()  # start runing the cap heater thread above
            print "Capillary Heater ON\r\n"

        if (rcv == "CAPHEATOFF"):
            Cap_Heater_Off = 1
            print "Capillary Heater OFF\r\n"

        if (rcv == "LASLEFT"):
            Move_left_Laser_Enable = 1

        if (rcv == "LASRIGHT"):
            Move_right_Laser_Enable = 1

        if (rcv == "RET" or rcv == "LASRET" or rcv == "LASHOME"):
            Move_Laser_Home = 1
            print "Moving Laser to home switch \r\n"

        if  "FVALVEPOS" in rcv:
            print "Sending cmd to LabSmith \r\n"
            cmd = rcv[10:]
            usb00port.write(cmd)
            print (cmd)
        ############################ Pi controls HV ##################################
        if  "SETV" in rcv:
            print "Sending SETV to HV mbed \r\n"
            usbport.write(rcv)
            usbport.write("\n")

        if  "GETVI" in rcv:
            print "GETVI from mbed \r\n"
            usbport.write("GETVI\n")
            usbrcv = readlineusbCR(usbport)
            print "response to GETVI from mbed \r\n"
            print usbrcv
            port.write( usbrcv)
            port.write("\n")
        #############################################################################
        if (rcv == "GPHOME"):
            Move_GelPump_Home = 1
            print "Moving Gel Pump to Home switch \r\n"

        if (rcv == "GPSTART"):
            print "Moving Gel Pump to Start switch \r\n"
            #GP_Mot = Thread(target=GelPump.run)
            Move_GelPump_Start = 1
            GP_Mot._running = True

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
            Solenoid_Enable = 0
            Solenoid_Off = 0
            S_Sequence_Enable = 0
            Cap_Heater_Enable = 0
            Move_ReagentM_Home = 0
            Move_ReagentP_Home = 0
            Move_ReagentW_Home = 0
            Move_ReagentS_Home = 0
            Move_ReagentE_Home = 0
            Move_ReagentB_Home = 0
            Move_GelPump_Move = 0
            Move_GelPump_Start = 0
            Move_GelPump_Home = 0
            move_gel_pump_up = 0
            move_gel_pump_down = 0
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
            target_motor = xyz_motor(7, 200, 100)
            target_motor.turn_off()
            target_motor = xyz_motor(8, 200, 100)
            target_motor.turn_off()
            target_motor = xyz_motor(9, 200, 100)
            target_motor.turn_off()
            target_motor = xyz_motor(10, 200, 100)
            target_motor.turn_off()
            target_motor = xyz_motor(11, 200, 100)
            target_motor.turn_off()
            target_motor = xyz_motor(12, 200, 100)
            target_motor.turn_off()
            print "Stopping all motors and heater\r\n"
            
        if ( rcv == "?"):
            print "All commands are shown below: \r\n"
            print "For Pump Array: REHOME RSHOME RWHOME RBHOME RMHOME RPHOME K \r\n"
            print "For Solenoids: S SF SEQ \r\n"
            print "For Capillary Heater: CAPHEATON CAPHEATOFF \r\n"
            print "For Gel Pump and Laser: LASLEFT LASRIGHT L R LASHOME GPHOME GPSTART GPRATE K Q QUIT \r\n"
            print "For XY_Stage: STAGEXRIGHT STAGEXLEFT STAGEZUP STAGEZDN\r\n"
            port.write("REHOME RSHOME RWHOME RBHOME RMHOME RPHOME K \r\n")
            port.write("CAPHEATON CAPHEATOFF LASLEFT LASRIGHT L  R  LASHOME GPHOME GPSTART GPRATE Q QUIT L R\r\n")
            port.write("SXWASTE SXWATER SXBUFFER SXSAMPLE STAGEZUP STGZDOWN  SXLFTSM SXRGHTSM SXLFTBIG SXRGHTBIG  K \r\n")

    st1.termintate()
    target_motor.turn_off()
