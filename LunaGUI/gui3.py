from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread
import subprocess

# This line of code will only make it so that only one instance of the gui is running.
from tendo import singleton
me = singleton.SingleInstance()

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
        args = out[94:].strip()
        # print (id, length, device_name, cmd, args)

        if cmd=="INVTHW":
            list_box.insert(END, device_name+" is "+args)
        elif cmd=="SHUTDOWN":
            luna.quit()

        # High Voltage Supply
        elif cmd=="GETVI":
            if args == "SYNTAX" or args == "":
                # Error Checking, sometimes hardware issues. Not connected properly.
                # on_getvi_button_click()
                pass
            elif args !="FAIL":
                args = out[94:]
                args_list = args.split()
                volt = args_list[0]
                current = args_list[1]
                current_volts.set(volt)
                current_amps.set(current)
                list_box.insert(END, "Received current voltage and current.")
        elif cmd=="SETV":
            list_box.insert(END, "Set voltage")
        # TEC Controller
        elif cmd == "STARTSEQ":
            pass
        elif cmd=="STOPSEQ":
            pass
        elif cmd=="READSEQD":
            message_status = args.split()
            if message_status[0] == "OK":
                block_temp = message_status[1]
                sample_temp = message_status[2]
                cycle = message_status[3]
                step = message_status[4]
                current_block_temp.set(block_temp)
                current_sample_temp.set(sample_temp)
                current_cycle.set(cycle)
                current_number_of_steps.set(step)



        # OBIS Laser
        elif cmd == "GETLPWR":
            list_box.insert(END, out)
        elif cmd == "SETLPWR":
            list_box.insert(END, out)
        elif cmd == "SETLSTATE":
            list_box.insert(END, out)



        # Laser's Motor
        elif cmd == "MOVLEFT":
            list_box.insert(END, out)
        elif cmd == "MOVERIGHT":
            list_box.insert(END, out)
        elif cmd == "RETRACT":
            list_box.insert(END, out)
        elif cmd == "CAPREADY":
            list_box.insert(END, out)
        # Cap Heater
        elif cmd == "CAPHEATON":
            list_box.insert(END, out)
        elif cmd == "CAPHEATOFF":
            list_box.insert(END, out)
        elif cmd == "CAPGETT":
            list_box.insert(END, out)
        elif cmd == "CAPSETT":
            list_box.insert(END, out)
        # Gel Pump
        elif cmd == "GELMV":
            list_box.insert(END, out)
        elif cmd == "GELRET":
            list_box.insert(END, out)
        elif cmd == "GELSTART":
            list_box.insert(END, out)



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
"""
High Voltage Power Supply
"""
def on_getvi_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'HighVoltageSupply'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETVI", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def on_setv_button_click(entry):
    input = entry.get()
    global proc
    global cnum
    size = 94 + len(input)
    name = 'HighVoltageSupply'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETV", "args": args}
    proc.stdin.write(cmd)
    cnum+=1
"""
TEC Controller
"""
def start_TEC_Seq_button_click(entry):
    """
    Start the thermo cycler's predefined steps for the given number of cycles
    :param entry: int/float - number of cycles for the TEC
    :return:
    """
    input = entry.get()
    global proc
    global cnum
    size = 94 + len(input)
    name = 'TECController'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STARTSEQ", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def stop_TEC_Seq_button_click():
    """
    Button click to stop/abort the thermo cycler's currently running sequence
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'TECController'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STOPSEQ", "args": args}
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

def read_TEC_Seq_button_click():
    """
    Button click to read data about the currently running sequence.
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'TECController'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "READSEQD", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

""" OBIS Laser Command """
def turn_on_laser_clicked():
    """
    Button click to read data about the currently running sequence.
    :return:
    """
    global proc
    global cnum
    args = 'ON'
    size = 94+len(args)
    name = 'OBISLaser'
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETLSTATE", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def turn_off_laser_clicked():
    """
    Button click to read data about the currently running sequence.
    :return:
    """
    global proc
    global cnum
    args = 'OFF'
    size = 94+len(args)
    name = 'OBISLaser'
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETLSTATE", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def get_current_laser_power_clicked():
    """
    Button click to read data about the currently running sequence.
    :return:
    """
    global proc
    global cnum
    args = ''
    size = 94
    name = 'OBISLaser'
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETLPWR", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def set_laser_power_clicked(entry):
    """
    Button click to read data about the currently running sequence.
    :return:
    """
    input = entry.get()
    global proc
    global cnum
    args = input
    size = 94 + len(input)
    name = 'OBISLaser'
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETLPWR", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

""" Fluidic Valve Commands """
def set_fluidic_valve_clicked():
    input = valve_set.get()
    global proc
    global cnum
    name = 'FluidValve'
    if input==1:
        args = 'A'
    elif input==2:
        args = 'B'
    elif input==3:
        args = 'CLOSED'
    size = 94 + len(args)
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "FVALVEPOS", "args": args}
    proc.stdin.write(cmd)
    cnum += 1


""" Spectrometer Commands """
def spectrometer_set_exposure_time_clicked(entry):
    """
    function call to send set exposure time for the spectrometer
    :param entry:
    :return:
    """
    exp_time = entry.get()
    args = exp_time
    global proc
    global cnum
    name = "Spectrometer"
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SPCSETEXP ", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def start_spectrometer_continuous_capture(filename_entry, timeBetween_entry, duration_entry):
    """

    :param filename_entry:
    :param timeBetween_entry:
    :param duration_entry:
    :return:
    """
    filename = filename_entry.get()
    delayMS = timeBetween_entry.get()
    durationMS = duration_entry.get()
    args = filename + " " + str(delayMS) + " " + str(durationMS)
    global proc
    global cnum
    name = "Spectrometer"
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SPCSTARTC", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def check_continous_capture():
    global proc
    global cnum
    args = ''
    size = 94
    name = "Spectrometer"
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SPCISCRUN", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

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
    title_label = Label(luna, text="OPTOKEY", fg="red", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    list_box = Listbox(luna, width=40)
    list_box.grid(row=2, column=0, columnspan=4)

    #### START ####

    start_shutdown_label = Label(luna, text="1) Start/Shutdown")
    start_shutdown_label.grid(row=3, column=0, columnspan=2)
    start_button = Button(luna, text="START", command = on_send_button_click)
    start_button.grid(row=3, column=2)

    shutdown_button = Button(luna, text="Shutdown", command=shutdown_button_click)
    shutdown_button.grid(row=3, column=3)

    high_voltage_label = Label(luna, text="2) High Voltage Supply")
    high_voltage_label.grid(row=4, column=0, columnspan=4)


    voltage_label = Label(luna, text="Voltage (V):")
    current_label = Label(luna, text="Current (A):")

    voltage_label.grid(row=5, column=0)
    current_label.grid(row=5, column=2)

    current_volts = StringVar()
    current_amps = StringVar()

    current_volts_dynamic_label = Label(luna, textvariable=current_volts, width=10)
    current_amps_dynamic_label = Label(luna, textvariable=current_amps, width=10)
    current_volts_dynamic_label.grid(row=5, column=1)
    current_amps_dynamic_label.grid(row=5, column=3)

    getvi_button = Button(luna, text="GETVI", command=on_getvi_button_click)
    getvi_button.grid(row=6, column=3)

    # Set voltage row on GUI
    set_voltage_label = Label(luna, text="set volt:")
    set_voltage_label.grid(row=6, column=0)
    set_voltage_entry = Entry(luna)
    set_voltage_entry.grid(row=6, column=1)
    setv_button = Button(luna, text="SETV", command=lambda: on_setv_button_click(set_voltage_entry))
    setv_button.grid(row=6, column=2)


    """##### TEC Controller #####"""

    TEC_control_label = Label(luna, text="3) TEC Controller")
    TEC_control_label.grid(row=7, column=0, columnspan=4)

    sample_temp_label = Label(luna, text="Sample Temp(C):")
    block_temp_label = Label(luna, text="Block Temp(C):")
    current_cycle_label = Label(luna, text="Current Cycle:")
    number_of_steps_label = Label(luna, text="Steps:")

    sample_temp_label.grid(row=8, column=0)
    block_temp_label.grid(row=8, column=2)
    current_cycle_label.grid(row=9, column=0)
    number_of_steps_label.grid(row=9, column=2)

    current_sample_temp = StringVar()
    current_block_temp = StringVar()
    current_cycle = StringVar()
    current_number_of_steps = StringVar()

    sample_temp_dynamic_label = Label(luna, textvariable=current_sample_temp, width=10)
    block_temp_dynamic_label = Label(luna, textvariable=current_block_temp, width=10)
    current_cycle_dynamic_label = Label(luna, textvariable=current_cycle, width=10)
    number_of_steps_dynamic_label = Label(luna, textvariable=current_number_of_steps, width=10)
    sample_temp_dynamic_label.grid(row=8, column=1)
    block_temp_dynamic_label.grid(row=8, column=3)
    current_cycle_dynamic_label.grid(row=9, column=1)
    number_of_steps_dynamic_label.grid(row=9, column=3)

    set_cycle_number_label = Label(luna, text="Cycle Number:")
    set_cycle_number_label.grid(row=10, column=0, columnspan=2)
    set_cycle_number_entry = Entry(luna)
    set_cycle_number_entry.grid(row=10, column=2, columnspan=2)
    start_TEC_Seq_button = Button(luna, text="Start TEC", command=lambda:start_TEC_Seq_button_click(set_cycle_number_entry))
    start_TEC_Seq_button.grid(row=11, column=1)

    read_TEC_Seq_button = Button(luna, text="Read TEC status", command=read_TEC_Seq_button_click)
    read_TEC_Seq_button.grid(row=11, column=2)
    stop_TEC_Seq_button = Button(luna, text="Stop TEC", command=stop_TEC_Seq_button_click)
    stop_TEC_Seq_button.grid(row=11, column=3)

    """##### OBIS Laser #####"""

    OBIS_Laser_label = Label(luna, text="4) OBIS Laser: ")
    OBIS_Laser_label.grid(row=12, column=0, columnspan=2)

    turn_on_OBIS_Laser_button = Button(luna, text="Turn on Laser", command=turn_on_laser_clicked)
    turn_on_OBIS_Laser_button.grid(row=12, column=2)
    turn_off_OBIS_Laser_button = Button(luna, text="Turn off Laser", command=turn_off_laser_clicked)
    turn_off_OBIS_Laser_button.grid(row=12, column=3)

    laser_power_label = Label(luna, text="Power (W):")
    laser_power_label.grid(row=13, column=0)
    current_power = StringVar()
    current_power_dynamic_label = Label(luna, textvariable=current_volts, width=10)
    current_power_dynamic_label.grid(row=13, column=1, columnspan=2)
    getp_button = Button(luna, text="GETLPWR", command=get_current_laser_power_clicked)
    getp_button.grid(row=13, column=3)

    set_power_label = Label(luna, text="set power:")
    set_power_label.grid(row=14, column=0)
    set_power_entry = Entry(luna)
    set_power_entry.grid(row=14, column=1, columnspan=2)
    setp_button = Button(luna, text="SETLPWR", command=lambda:set_laser_power_clicked(set_power_entry))
    setp_button.grid(row=14, column=3)

    """##### Laser Motor #####"""

    laser_motor_label = Label(luna, text="5) Laser Motor: ")
    laser_motor_label.grid(row=15, column=0, columnspan=4)

    go_left_laser_motor_button = Button(luna, text="MOVELEFT", command=None)
    go_left_laser_motor_button.grid(row=16, column=0, columnspan=2)
    go_right_laser_motor_button = Button(luna, text="MOVERIGHT", command=None)
    go_right_laser_motor_button.grid(row=16, column=2, columnspan=2)
    go_left_laser_motor_button = Button(luna, text="RETRACT", command=None)
    go_left_laser_motor_button.grid(row=17, column=0, columnspan=2)
    go_right_laser_motor_button = Button(luna, text="CAPREADY", command=None)
    go_right_laser_motor_button.grid(row=17, column=2, columnspan=2)

    """##### Capillary Heater #####"""

    capillary_heater_label = Label(luna, text="6) Capillary Heater: ")
    capillary_heater_label.grid(row=18, column=0, columnspan=4)

    turn_on_cap_heater_button = Button(luna, text="Turn On Heater", command=None)
    turn_on_cap_heater_button.grid(row=19, column=0, columnspan=2)
    turn_off_cap_heater_button = Button(luna, text="Turn Off Heater", command=None)
    turn_off_cap_heater_button.grid(row=19, column=2, columnspan=2)

    cap_heater_current_temp_label = Label(luna, text="Current Temp (C):")
    cap_heater_current_temp_label.grid(row=20, column=0)
    cap_heater_current_temp = StringVar()
    cap_heater_current_temp_dynamic_label = Label(luna, textvariable=cap_heater_current_temp, width=10)
    cap_heater_current_temp_dynamic_label.grid(row=20, column=1, columnspan=2)
    gett_cap_heater_button = Button(luna, text="GETT", command=None)
    gett_cap_heater_button.grid(row=20, column=3)

    cap_heater_set_temp_label = Label(luna, text="Set Temp (C):")
    cap_heater_set_temp_label.grid(row=21, column=0)
    cap_heater_set_temp_entry = Entry(luna)
    cap_heater_set_temp_entry.grid(row=21, column=1, columnspan=2)

    sett_cap_heater_button = Button(luna, text="SETT", command=None)
    sett_cap_heater_button.grid(row=21, column=3, command=None)

    """##### Fluidic Valve #####"""
    fluidic_valve_label = Label(luna, text="7) Fluid Valve: ")
    fluidic_valve_label.grid(row=23, column=0, columnspan=4)

    valve_set = IntVar()
    valve_set.set(3)
    valve_options = [
        ("A", 1),
        ("B", 2),
        ("CLOSED", 3)
    ]
    for txt, val in valve_options:
        radio_button = Radiobutton(luna, text=txt, variable=valve_set, command=set_fluidic_valve_clicked, value=val)
        radio_button.grid(row=24, column=val)

    """##### Spectrometer #####"""
    spectrometer_label = Label(luna, text="8) Spectrometer: ")
    spectrometer_label.grid(row=26, column=0, columnspan=4)

    set_exposure_time_label = Label(luna, text="set exposure time:")
    set_exposure_time_label.grid(row=27, column=0)
    set_exposure_time_entry = Entry(luna)
    set_exposure_time_entry.grid(row=27, column=1, columnspan=2)
    set_exposure_time_button = Button(luna, text="SPCSETEXP", command=lambda:spectrometer_set_exposure_time_clicked(set_exposure_time_entry))
    set_exposure_time_button.grid(row=27, column=3)

    set_spectrometer_filename_label = Label(luna, text="filename:")
    set_spectrometer_filename_label.grid(row=28, column=0)
    set_spectrometer_filename_entry = Entry(luna)
    set_spectrometer_filename_entry.grid(row=28, column=1)

    set_spectrometer_time_between_label = Label(luna, text="time between reads (ms):")
    set_spectrometer_time_between_label.grid(row=28, column=2)
    set_spectrometer_time_between_entry = Entry(luna)
    set_spectrometer_time_between_entry.grid(row=28, column=3)

    set_spectrometer_duration_label = Label(luna, text="duration (ms):")
    set_spectrometer_duration_label.grid(row=29, column=0)
    set_spectrometer_duration_entry = Entry(luna)
    set_spectrometer_duration_entry.grid(row=29, column=1)

    start_continuous_spectrometer_button = Button(luna,
                                    text="SPCSTARTC",
                                    command=lambda:start_spectrometer_continuous_capture(set_spectrometer_filename_entry,
                                                                                         set_spectrometer_time_between_entry,
                                                                                         set_spectrometer_duration_entry))
    start_continuous_spectrometer_button.grid(row=29, column=2)
    start_continuous_spectrometer_button = Button(luna, text="SPCISCRUN", command=check_continous_capture)
    start_continuous_spectrometer_button.grid(row=29, column=3)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()
# luna.mainloop()
