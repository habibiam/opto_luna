from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread
import subprocess
import itertools

import logging
import json
from tendo import singleton

FORMAT = '%(levelname)s:%(funcName)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# This line of code will only make it so that only one instance of the gui is running.
# from tendo import singleton
me = singleton.SingleInstance()

def send_command_to_LunaSrv(device_name, CMD, args):
    global proc
    global cnum
    arguement = str(args)
    size = 94 + len(arguement)
    name = device_name
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": CMD, "args": arguement}
    proc.stdin.write(cmd)
    cnum+=1
    return

dict_of_devices_and_commands \
    = {'HighVoltageSupply': ["GETVI", "SETV"],
       'TECController': ["STARTSEQ", "STOPSEQ", "READSEQD"],
       'OBISLaser': ["GETLPWR", "SETLPWR", "SETLSTATE"],
       'Spectrometer': ["SPCSETEXP", "SPCSTARTC", "SPCISCRUN"],
       'FluidValve': ['FVALVEPOS'],
       # Dave's Instruments
       'Pi': ['CAPHEATON', 'CAPHEATOFF', 'CAPGETT', 'CAPSETT',
              'MOVELEFT', 'MOVERIGHT', 'LMHOME', 'CAPREADY',
              'GPHOME', 'GPRATE', 'GPSTART',
              'RWHOME', 'RWRATE',
              'RPHOME', 'RPRATE',
              'RBHOME', 'RBRATE',
              'RMHOME', 'RMRATE',
              'CHIPZHOME', 'CHIPZUP',
              'CHIPYHOME', 'CHIPYOUT']
             + ['v' + str(i) for i in range(1, 21)]
       }

cnum = 1

"""
Luna Server Process
"""
cmd = [
    "python",
    "../LunaSrv/lunasrv.py"
]
global proc


# def the_reader_thread():
#     """
#     A function that starts in another thread.
#     Continuously runs in order to read stdout and then from there display it onto the status window
#     :return:
#     """
#
#     # List of commands and devices just to keep track which ones are connected to the reader thread.
#     list_of_commands = ["GETVI", "SETV",
#                         "STARTSEQ", "STOPSEQ", "READSEQD",
#                         "GETLPWR", "SETLPWR", "SETLSTATE",
#                         "MOVELEFT", "MOVERIGHT", "RETRACT", "CAPREADY",
#                         "CAPHEATON", "CAPHEATOFF", "CAPGETT", "CAPSETT",
#                         "GELMV", "GELRET", "GELSTART"]
#
#     list_of_devices = ['HighVoltageSupply',
#                        'TECController',
#                        'OBISLaser',
#                        'LaserMotor',
#                        'CapillaryHeater',
#                        'GelPump']
#
#     while(True):
#         out = proc.stdout.readline()
#         print(out)
#         id = out[:10].strip()
#         length = out[10:20].strip()
#         device_name = out[20:84].strip()
#         cmd = out[84:94].strip()
#         args = out[94:]
#         # print (id, length, device_name, cmd, args)
#         # try:
#         #     pass
#         # except IOError:
#         #     logging.info('CMD now part of the dictionary')
#         #
#         #
#         if cmd=="INVTHW":
#             list_box.insert(END, device_name+" is "+args)
#         elif cmd=="SHUTDOWN":
#             list_box.insert(END, "Luna is Shutting down")
#             time.sleep(1.0)
#             luna.quit()
#         # elif (dict_of_devices_and_commands[device_name]):
#         #     pass
#         #     # if cmd=="GETVI":
#         #     #     if args !="FAIL":
#         #     #         args_list = args.split()
#         #     #         volt = args_list[0]
#         #     #         current = args_list[1]
#         #     #         current_volts.set(volt)
#         #     #         current_amps.set(current)
#         #     #         list_box.insert(END, "Received current voltage and current.")
#         #     # elif cmd=="SETV":
#         #     #     list_box.insert(END, "Set voltage")
#         #     # # TEC Controller
#         #     # elif cmd == "STARTSEQ":
#         #     #     pass
#         #     # elif cmd=="STOPSEQ":
#         #     #     pass
#         #     # elif cmd=="READSEQD":
#         #     #     message_status = args.split()
#         #     #     if message_status[0] == "OK":
#         #     #         block_temp = message_status[1]
#         #     #         sample_temp = message_status[2]
#         #     #         cycle = message_status[3]
#         #     #         step = message_status[4]
#         #     #         current_block_temp.set(block_temp)
#         #     #         current_sample_temp.set(sample_temp)
#         #     #         current_cycle.set(cycle)
#         #     #         current_number_of_steps.set(step)
#         #     #
#         #     #
#         #     #
#         #     # # OBIS Laser
#         #     # elif cmd == "GETLPWR":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "SETLPWR":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "SETLSTATE":
#         #     #     list_box.insert(END, out)
#         #     #
#         #     #
#         #     #
#         #     # # Laser's Motor
#         #     # elif cmd == "MOVLEFT":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "MOVERIGHT":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "RETRACT":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "CAPREADY":
#         #     #     list_box.insert(END, out)
#         #     # # Cap Heater
#         #     # elif cmd == "CAPHEATON":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "CAPHEATOFF":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "CAPGETT":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "CAPSETT":
#         #     #     list_box.insert(END, out)
#         #     # # Gel Pump
#         #     # elif cmd == "GELMV":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "GELRET":
#         #     #     list_box.insert(END, out)
#         #     # elif cmd == "GELSTART":
#         #     #     list_box.insert(END, out)



def processRUNSAMPLE(receivedDeviceName, recievedArgs):
    """
    Started on processRUNSAMPLE in order to add the run_config.json
    file in to the LunaSrv.
    Need to built this once all the devices are hooked up and sample runs are ready to be automated
    as of now, can load and have access to json config file.
    """
    # global scanner
    # global cnum
    #
    # logger.info("Handle RUNSAMPLE command")
    #
    # # Get full path to our json run configuration file
    #
    # path = os.path.dirname(os.path.abspath(__file__))
    # path += "/../config"
    # configFile = path + "/run_config.json"
    #
    # with open(configFile, 'r') as f:
    #     run_config = json.load(f)
    # print run_config
    #
    # # 1.0) Initialize Reagent State
    #
    # # 2.0) Ready State
    #
    # # 3.0) Run State


    """
    3.3.1) Time 0
        Voltage: 10 kV
        Current: n/a
        Spectrum: dark
        solution station: buffer
    """

    """
    3.1) Initailze Gel
        Time: 3 minutes
        * Voltage: 10 kV
        * Current: n/a
        * Spectrum: OFF
        * solution station: buffer
        TRANSITION (Rinse in water)
    """
    # 1) Move to water and then to buffer


    """
    3.2) Injection
        Time: 10 sec
        * Voltage: 5 kV
        * Current: n/a
        * Spectrum: OFF
        * solution station: buffer
        TRANSITION (Rinse in water)
    """
    """
    3.3.0 Run State
        look at ../config/run_config.json
        Spectrum Parameters
        Exposure time: 250 ms
        Integration Time: 250 ms
        Log time: 250 ms
        Duration: 50 minutes
        Filename: whatever

    :return:
    """
    """
    3.3.2) Time 1 minutes (turn on reference)
        voltage: 10 kV
        Current: n/a
        Spectrum: reference
        Solution Station: buffer


    """

    """
    3.3.3) Time 1 minutes (turn on reference)
        voltage: 0 kV
        Current: 0
        Spectrum: off
        Solution Station: waste
        Valve Position: CLOSED
    """

    """
    3.3) Time 2 minutes (end)
    """
    return

"""
start GUI
"""
class LunaUI(Tk):
    def setReaderPipe(self, pipe):
        self._pipe = pipe

    def __init__(self):
        Tk.__init__(self)

    def quit(self):
        self.destroy()

luna = LunaUI()

if __name__ == '__main__':
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(1)
    if proc is None or proc.returncode is not None:
        if proc.returncode is not None:
            print "LunaSrv exited immediately with a return code" + (str(proc.returncode))
        else:
            print " Failed to start LunaSrv"
        sys.exit(-1)


    """
    Start the Luna Srv
    """
    send_command_to_LunaSrv('', 'INVTHW', '')

    # Get full path to our json run configuration file

    path = os.path.dirname(os.path.abspath(__file__))
    path += "/../config"
    configFile = path + "/run_config.json"

    with open(configFile, 'r') as f:
        run_config = json.load(f)
    print run_config

    """
    3.1) Initailze Gel
        Time: 3 minutes / 10 seconds
        * Voltage: 10 kV
        * Current: n/a
        * Spectrum: OFF
        * solution station: buffer
        TRANSITION (Rinse in water)
    """
    # 1) Move to water and then to buffer
    send_command_to_LunaSrv('pi', 'SXWATER', '')
    send_command_to_LunaSrv('pi', 'STAGEZUP', '')
    send_command_to_LunaSrv('pi', 'STAGEZDN', '')
    send_command_to_LunaSrv('pi', 'SXBUFFER', '')

    # 2) Start the High Voltage Supply
    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', run_config["High Voltage Supply"]["init gel voltage"])
    time.sleep(3*60)
    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', 0) # Turn off
    send_command_to_LunaSrv('pi', 'STAGEZDN', '')

    send_command_to_LunaSrv('pi', 'SXWASTE', '')

    send_command_to_LunaSrv('pi', 'STAGEZUP', '')
    send_command_to_LunaSrv('pi', 'STAGEZDN', '')
    """
    3.2) Injection
        Time: 10 sec
        * Voltage: 5 kV
        * Current: n/a
        * Spectrum: OFF
        * solution station: sample
        TRANSITION (Rinse in water)
    """
    send_command_to_LunaSrv('pi', 'SXSAMPLE', '')
    send_command_to_LunaSrv('pi', 'STAGEZUP', '')

    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', run_config["High Voltage Supply"]["injection voltage"])
    time.sleep(10)
    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', 0)  # Turn off
    send_command_to_LunaSrv('pi', 'STAGEZDN', '')

    send_command_to_LunaSrv('pi', 'SXWATER', '')
    send_command_to_LunaSrv('pi', 'STAGEZUP', '')
    send_command_to_LunaSrv('pi', 'STAGEZDN', '')

    """
    3.3.0 Run State
        look at ../config/run_config.json
        Spectrum Parameters
        Exposure time: 250 ms
        Integration Time: 250 ms
        Log time: 250 ms
        Duration: 50 minutes
        Filename: whatever

    """

    """
    3.3.1) Time 0
        Voltage: 10 kV
        Current: n/a
        Spectrum: dark
        solution station: buffer
    """
    send_command_to_LunaSrv('pi', 'SXBUFFER', '')
    send_command_to_LunaSrv('pi', 'STAGEZUP', '')
    # Turn on High Voltage Supply
    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', run_config["High Voltage Supply"]["run voltage"])
    # Set laser power
    send_command_to_LunaSrv('OBISLaser', 'SETLPWR', run_config["OBIS Laser"]["laser power"]) #10 mW
    # Turn laser on
    send_command_to_LunaSrv('OBISLaser', 'SETLSTATE', "ON")
    """
    3.3.2) Time 1 minutes (turn on reference)
        voltage: 10 kV
        Current: n/a
        Spectrum: reference
        Solution Station: buffer
    """
    # Turn on Spectrometer
    send_command_to_LunaSrv('Spectrometer', 'SPCSETEXP', 250)
    send_command_to_LunaSrv('Spectrometer', 'SPCSTARTC', None)

    """
    3.3.3) Time 2 minutes (end)
        voltage: 0 kV
        Current: 0
        Spectrum: off
        Solution Station: waste
        Valve Position: CLOSED
    """
    time.sleep(50 * 60)
    send_command_to_LunaSrv('HighVoltageSupply', 'SETV', 0)  # Turn off
    send_command_to_LunaSrv('OBISLaser', 'SETLSTATE', "OFF")

    send_command_to_LunaSrv('pi', 'STAGEZDN', '')
    send_command_to_LunaSrv('pi', 'SXWATER', '')


    proc.terminate()