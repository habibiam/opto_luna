from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread
import subprocess

import logging

FORMAT = '%(levelname)s:%(funcName)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# This line of code will only make it so that only one instance of the gui is running.
# from tendo import singleton
# me = singleton.SingleInstance()

def on_send_button_click():
    """
    INVTHW
    :return:
    """
    global proc
    global cnum
    size = 94
    name = ''
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "INVTHW", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def shutdown_button_click():
    """
    Button click to stop/abort the thermo cycler's currently running sequence
    :return:
    """
    global proc
    global cnum
    size = 94
    name = ''
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SHUTDOWN", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    luna.quit()
    cnum+=1
"""
Capillary Heater
"""
def turn_on_cap_heater_button_click():
    """
    Button click to turn on capillary heater
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPHEATON", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum+=1

def turn_off_cap_heater_button_click():
    """
    Button click to turn on capillary heater
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPHEATOFF", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum+=1

def gett_cap_heater_button_click():
    """
    Button click to turn on capillary heater
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPGETT", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum+=1


"""
Gel Pump
"""

def gp_home_button_click():
    """
    GPHOME
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPHOME", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def gp_start_button_click():
    """
    GPSTART
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPSTART", "args": args}
    proc.stdin.write(cmd)
    cnum+=1


def gp_rate_button_click(entry):
    """
    GPRATE_10 [microL/sec]
    :return:
    """
    input = entry.get()
    global proc
    global cnum
    size = 94+len(input)
    name = 'Pi'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPRATE", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

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

"""
READER Thread

start reader thread
Separate thread to display the message/status of the Devices
"""

def the_reader_thread():
    """
    A function that starts in another thread.
    Continuously runs in order to read stdout and then from there display it onto the status window
    :return:
    """

    # List of commands and devices just to keep track which ones are connected to the reader thread.
    list_of_commands = ["GETVI", "SETV",
                        "STARTSEQ", "STOPSEQ", "READSEQD",
                        "GETLPWR", "SETLPWR", "SETLSTATE",
                        "MOVELEFT", "MOVERIGHT", "RETRACT", "CAPREADY",
                        "CAPHEATON", "CAPHEATOFF", "CAPGETT", "CAPSETT",
                        "GELMV", "GELRET", "GELSTART"]

    list_of_devices = ['HighVoltageSupply',
                       'TECController',
                       'OBISLaser',
                       'LaserMotor',
                       'CapillaryHeater',
                       'GelPump']

    while(True):
        out = proc.stdout.readline()
        print(out)
        id = out[:10].strip()
        length = out[10:19].strip()
        device_name = out[20:83].strip()
        cmd = out[84:93].strip()
        args = out[94:]
        # print (id, length, device_name, cmd, args)
        # try:
        #     pass
        # except IOError:
        #     logging.info('CMD now part of the dictionary')
        #
        #
        if cmd=="INVTHW":
            list_box.insert(END, device_name+" is "+args)
        elif cmd=="SHUTDOWN":
            list_box.insert(END, "Luna is Shutting down")
            time.sleep(1.0)
            luna.quit()
        # elif (dict_of_devices_and_commands[device_name]):
        #     pass
        #     # if cmd=="GETVI":
        #     #     if args !="FAIL":
        #     #         args_list = args.split()
        #     #         volt = args_list[0]
        #     #         current = args_list[1]
        #     #         current_volts.set(volt)
        #     #         current_amps.set(current)
        #     #         list_box.insert(END, "Received current voltage and current.")
        #     # elif cmd=="SETV":
        #     #     list_box.insert(END, "Set voltage")
        #     # # TEC Controller
        #     # elif cmd == "STARTSEQ":
        #     #     pass
        #     # elif cmd=="STOPSEQ":
        #     #     pass
        #     # elif cmd=="READSEQD":
        #     #     message_status = args.split()
        #     #     if message_status[0] == "OK":
        #     #         block_temp = message_status[1]
        #     #         sample_temp = message_status[2]
        #     #         cycle = message_status[3]
        #     #         step = message_status[4]
        #     #         current_block_temp.set(block_temp)
        #     #         current_sample_temp.set(sample_temp)
        #     #         current_cycle.set(cycle)
        #     #         current_number_of_steps.set(step)
        #     #
        #     #
        #     #
        #     # # OBIS Laser
        #     # elif cmd == "GETLPWR":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "SETLPWR":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "SETLSTATE":
        #     #     list_box.insert(END, out)
        #     #
        #     #
        #     #
        #     # # Laser's Motor
        #     # elif cmd == "MOVLEFT":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "MOVERIGHT":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "RETRACT":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "CAPREADY":
        #     #     list_box.insert(END, out)
        #     # # Cap Heater
        #     # elif cmd == "CAPHEATON":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "CAPHEATOFF":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "CAPGETT":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "CAPSETT":
        #     #     list_box.insert(END, out)
        #     # # Gel Pump
        #     # elif cmd == "GELMV":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "GELRET":
        #     #     list_box.insert(END, out)
        #     # elif cmd == "GELSTART":
        #     #     list_box.insert(END, out)




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
    1) Start reader_thread
    """
    reader_thread = Thread(target=the_reader_thread)
    # Set the thread as a daemon thread, aka when the gui closes down, the thread also ends.
    reader_thread.daemon = True
    reader_thread.start()

    """"Title ('Optokey')"""
    luna.wm_title("Status Window")
    title_label = Label(luna, text="Pi Controller", fg="blue", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    list_box = Listbox(luna, width=40)
    list_box.grid(row=2, column=0, columnspan=4)

    #### START ####

    #### START ####

    start_shutdown_label = Label(luna, text="0) Start/Shutdown")
    start_shutdown_label.grid(row=3, column=0, columnspan=2)
    start_button = Button(luna, text="START", command = on_send_button_click)
    start_button.grid(row=3, column=2)

    shutdown_button = Button(luna, text="Shutdown", command=shutdown_button_click)
    shutdown_button.grid(row=3, column=3)

    """##### Capillary Heater #####"""

    capillary_heater_label = Label(luna, text="1) Capillary Heater: ")
    capillary_heater_label.grid(row=4, column=0, columnspan=4)

    turn_on_cap_heater_button = Button(luna, text="Turn On Heater", command=turn_on_cap_heater_button_click)
    turn_on_cap_heater_button.grid(row=5, column=0, columnspan=2)
    turn_off_cap_heater_button = Button(luna, text="Turn Off Heater", command=turn_off_cap_heater_button_click)
    turn_off_cap_heater_button.grid(row=5, column=2, columnspan=2)

    cap_heater_current_temp_label = Label(luna, text="Current Temp (C):")
    cap_heater_current_temp_label.grid(row=6, column=0)
    cap_heater_current_temp = StringVar()
    cap_heater_current_temp_dynamic_label = Label(luna, textvariable=cap_heater_current_temp, width=10)
    cap_heater_current_temp_dynamic_label.grid(row=6, column=1, columnspan=2)
    gett_cap_heater_button = Button(luna, text="CAPGETT", command=gett_cap_heater_button_click)
    gett_cap_heater_button.grid(row=7, column=3)

    cap_heater_set_temp_label = Label(luna, text="Set Temp (C):")
    cap_heater_set_temp_label.grid(row=6, column=0)
    cap_heater_set_temp_entry = Entry(luna)
    cap_heater_set_temp_entry.grid(row=6, column=1, columnspan=2)

    sett_cap_heater_button = Button(luna, text="CAPSETT", command=None)
    sett_cap_heater_button.grid(row=6, column=3)

    """##### Laser Motor #####"""
    laser_motor_label = Label(luna, text="2) Laser Motor")
    laser_motor_label.grid(row=7, column=0, columnspan=4)

    lm_moveleft_button = Button(luna, text="MOVELEFT", command=None)
    lm_moveleft_button.grid(row=8, column=1)
    lm_moveright_button = Button(luna, text="MOVERIGHT", command=None)
    lm_moveright_button.grid(row=8, column=2)

    lm_lmhome_button = Button(luna, text="LMHOME", command=None)
    lm_lmhome_button.grid(row=9, column=1)
    lm_capready_button = Button(luna, text="CAPREADY", command=None)
    lm_capready_button.grid(row=9, column=2)

    """##### Gel Pump #####"""
    gel_pump_label = Label(luna, text="3) gel_pump")
    gel_pump_label.grid(row=10, column=0, columnspan=4)

    gp_home_button = Button(luna, text="GPHOME", command=gp_home_button_click)
    gp_home_button.grid(row=11, column=1)

    gp_start_button = Button(luna, text="GPSTART", command=gp_start_button_click)
    gp_start_button.grid(row=11, column=2)

    set_gprate_label = Label(luna, text="set rate [microL/sec]:")
    set_gprate_label.grid(row=12, column=0)
    set_gprate_entry = Entry(luna)
    set_gprate_entry.grid(row=12, column=1, columnspan=2)
    gp_rate_button = Button(luna, text="GPRATE", command=lambda:gp_rate_button_click(set_gprate_entry))
    gp_rate_button.grid(row=12, column=3)

    """##### Reagent W, P, B, M #####"""
    reagent_pump_label = Label(luna, text="4) Reagent Pumps (W, P, B, M): ")
    reagent_pump_label.grid(row=13, column=0, columnspan=4)

    valve_options = [
        ("A", 0),
        ("HOME", 1),
        ("RATE", 2)
    ]

    row_counter = 14
    for reagent in ['W', 'P', 'B', 'K']:
        reagent_label = Label(luna, text=reagent)
        reagent_label.grid(row=row_counter, column=0, columnspan=4)
        row_counter+=1

        home_button_text = "R" + str(reagent) + "HOME"
        reagent_home_button = Button(luna, text=home_button_text, command=lambda: None)
        reagent_home_button.grid(row=row_counter, column=0)
        reagent_rate_entry = Entry(luna)
        reagent_rate_entry.grid(row=row_counter, column=1, columnspan=2)
        rate_button_text = "R" + str(reagent) + "RATE"
        reagent_home_button = Button(luna, text=rate_button_text, command=None)
        reagent_home_button.grid(row=row_counter, column=3)
        row_counter+=1

    """##### Chip Station Z Y #####"""
    chip_station_label = Label(luna, text="5) Chip Station (Z and Y): ")
    chip_station_label.grid(row=22, column=0, columnspan=4)
    chip_Z_home_button = Button(luna, text="CHIPZHOME", command=None)
    chip_Z_home_button.grid(row=23, column=0)
    chip_Z_up_button = Button(luna, text="CHIPZUP", command=None)
    chip_Z_up_button.grid(row=23, column=1)

    chip_Y_home_button = Button(luna, text="CHIPYHOME", command=None)
    chip_Y_home_button.grid(row=23, column=0)
    chip_Y_up_button = Button(luna, text="CHIPZUP", command=None)
    chip_Y_up_button.grid(row=23, column=1)
    """ Valve v1-v20"""
    valve_nums = []
    num = 1
    for row in range(24,29):
        for col in range(4):
            valve_text = 'v' + str(num)
            num += 1
            # valve_label = Label(luna, text=valve_text)
            valve_num = IntVar()
            chk = Checkbutton(luna, text=valve_text, variable=valve_num)
            chk.grid(row=row, column=col)

            valve_nums.append(valve_num)

    valve_open_button = Button(luna, text="OPEN valves", command=None)
    valve_open_button.grid(row=30, column=1)

    valve_close_button = Button(luna, text="CLOSED valves", command=None)
    valve_close_button.grid(row=30, column=2)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()