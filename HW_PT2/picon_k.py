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

from CapHeat import CapHeat
from threading import Thread
from Gel_Pump import Gel_Pump
from Solenoid import Solenoid
from xyz_motor import xyz_motor
from Laser_Motor import Laser_Motor
from Reagent_Pump import Reagent_Pump
from Solenoid_Sequence import Solenoid_Sequence
from Opto_MotorHAT import Opto_MotorHAT, Opto_StepperMotor


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

################################## Serial Port Communication ################################

# In GPIO, USB GPIO pins are used for serial port communication

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

#############################################################################################

####################################### Main Function #######################################

if __name__ == "__main__":

    global Solenoid_Enable
    global Solenoid_Off
    global S_Sequence_Enable
    global Cap_Heater_Enable
    global Cap_Heater_Off
    global Move_ReagentM_Home
    global Move_ReagentP_Home
    global Move_ReagentW_Home
    global Move_ReagentS_Home
    global Move_ReagentE_Home
    global Move_ReagentB_Home
    global move_gel_pump_up, move_gel_pump_down
    global Move_GelPump_Home, Move_GelPump_Start, Move_GelPump_Move
    global Move_left_Laser_Enable, Move_right_Laser_Enable, Move_Laser_Home
    global Move_l_Laser_Enable, Move_r_Laser_Enable
    

    ############################# STAGE X Z edit #############################
    
    global move_stageZ_up, move_stageZ_down
    global move_stageX_left_small, move_stageX_left_big
    global move_stageX_right_small, move_stageX_right_big
    
    move_stageX_left_small = move_stageX_left_big = 0.0
    move_stageX_right_small = move_stageX_right_big = 0.0
    move_stageZ_up = move_stageZ_down = 0.0

    # absolute positions
    global move_to_sample, move_to_buffer, move_to_water, move_to_waste
    
    move_to_sample = move_to_buffer = move_to_water = move_to_waste = 0.0

    ##########################################################################

    ############################ Initialization ##############################
 
    Solenoid_Enable = 0.0
    Solenoid_Off = 0.0
    S_Sequence_Enable = 0.0
    Cap_Heater_Enable = 0.0
    Cap_Heater_Off = 0.0
    move_gel_pump_down = move_gel_pump_up = 0.0
    Move_ReagentM_Home = Move_ReagentP_Home = 0.0
    Move_ReagentW_Home = Move_ReagentS_Home = 0.0
    Move_ReagentE_Home = Move_ReagentB_Home = 0.0
    Move_GelPump_Home = Move_GelPump_Start = Move_GelPump_Move = 0.0
    Move_left_Laser_Enable = Move_right_Laser_Enable = 0.0
    Move_l_Laser_Enable = Move_r_Laser_Enable = Move_Laser_Home = 0.0

    ##########################################################################

    ######################### Create Class Object ############################
    
    Sol = Solenoid()  

    Heat = CapHeat()
    
    GelPump = Gel_Pump()
    
    LaserMotor = Laser_Motor()
    
    Sequence = Solenoid_Sequence()  

    Reagent_Pump_Mot = Reagent_Pump()
    
    #########################################################################

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
            SolThread = Thread(target=Sol.Solenoid_Enable)
            SolThread.start()  # start runing the Solenoid thread above

        if (rcv == "SF"):
            SolThread = Thread(target=Sol.Solenoid_Off)
            SolThread.start()  # start runing the Solenoid thread above

        if (rcv == "SEQ"):
            SeqThread = Thread(target=Sequence.S_Sequence_Enable)
            SeqThread.start()

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

        if (rcv == "VC"):
            print "Valve Close \r\n"
            
        if (rcv == "VO"):
            print "Valve Open \r\n"

        if (rcv == "K") or (rcv == "KILL") or (rcv == "QUIT") or (rcv == "Q"):
            Solenoid_Off = 0
            Solenoid_Enable = 0 
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
            port.write("VC 10 VO 8REHOME RSHOME RWHOME RBHOME RMHOME RPHOME K \r\n")
            port.write("CAPHEATON CAPHEATOFF LASLEFT LASRIGHT L  R  LASHOME GPHOME GPSTART GPRATE Q QUIT L R\r\n")
            port.write("SXWASTE SXWATER SXBUFFER SXSAMPLE STAGEZUP STGZDOWN  SXLFTSM SXRGHTSM SXLFTBIG SXRGHTBIG  K \r\n")

    st1.termintate()
    target_motor.turn_off()
