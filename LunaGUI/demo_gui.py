import logging
import subprocess
from Tkinter import *
from serial import *
from threading import Thread

from tendo import singleton

FORMAT = '%(levelname)s:%(funcName)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# This line of code will only make it so that only one instance of the gui is running.
# from tendo import singleton
me = singleton.SingleInstance()


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
    cnum += 1


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
    cnum += 1

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


################################ Dave's Machines ########################
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
    cnum += 1


def turn_off_cap_heater_button_click():
    """
    Button click to turn off capillary heater
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
    cnum += 1


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
    cnum += 1


def sett_cap_heater_button_click(entry):
    """
    Button click to set the capillary heater temperature [degrees C]
    :param entry: Tkinter entry
    :return:
    """
    input = entry.get()
    global proc
    global cnum
    size = 94 + len(input)
    name = 'Pi'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPSETT", "args": args}
    proc.stdin.write(cmd)
    cnum += 1


"""
Laser Motor
"""


def move_left_button_click():
    """
    Button click to move the Laser Motor counter-clockwise by one increment
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LASLEFT", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum += 1


def move_right_button_click():
    """
    Button click to move the Laser Motor counter-clockwise by one increment
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LASRIGHT", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum += 1


def LMHOME_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LMHOME", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum += 1


def CAPREADY_button_click():
    """
    Sends a "CAPREADY" command to LunaSrv
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPREADY", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum += 1


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
    cnum += 1


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
    cnum += 1

def gp_up_button_click():
    """
    GPUP
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPUP", "args": args}
    proc.stdin.write(cmd)
    cnum += 1


def gp_down_button_click():
    """
    GPDOWN
    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPDOWN", "args": args}
    proc.stdin.write(cmd)
    cnum += 1


def gp_rate_button_click(entry):
    """
    GPRATE_10 [microL/sec]
    :return:
    """
    input = entry.get()
    global proc
    global cnum
    size = 94 + len(input)
    name = 'Pi'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPRATE", "args": args}
    proc.stdin.write(cmd)
    cnum += 1


"""
Solution Stage X and Z
"""
def x_moveleft_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXLFTBIG", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def x_moveright_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXRGHTBIG", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def small_x_moveleft_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXLFTSM", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def small_x_moveright_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXRGHTSM", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def z_moveup_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STAGEZUP", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def x_move_to_sample_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXSAMPLE", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def x_move_to_buffer_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXBUFFER", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def x_move_to_water_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXWATER", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def x_move_to_waste_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXWASTE", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

def z_movedown_button_click():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STAGEZDN", "args": args}
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
    """

    :return:
    """
    global proc
    global cnum
    args = ''
    size = 94
    name = "Spectrometer"
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SPCISCRUN", "args": args}
    proc.stdin.write(cmd)
    cnum += 1

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

    while (True):
        out = proc.stdout.readline()
        print(out)
        id = out[:10].strip()
        length = out[10:20].strip()
        device_name = out[20:84].strip()
        cmd = out[84:94].strip()
        args = out[94:]
        # print (id, length, device_name, cmd, args)
        # try:
        #     pass
        # except IOError:
        #     logging.info('CMD now part of the dictionary')
        #
        #
        if cmd == "INVTHW":
            list_box.insert(END, device_name + " is " + args)
        elif cmd == "SHUTDOWN":
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
    # proc.wait(1)
    # if proc is None or proc.returncode is not None:
    #     if proc.returncode is not None:
    #         print "LunaSrv exited immediately with a return code" + (str(proc.returncode))
    #     else:
    #         print " Failed to start LunaSrv"
    #     sys.exit(-1)
    """
    1) Start reader_thread
    """
    reader_thread = Thread(target=the_reader_thread)
    # Set the thread as a daemon thread, aka when the gui closes down, the thread also ends.
    reader_thread.daemon = True
    reader_thread.start()

    """"Title ('Optokey')"""
    luna.wm_title("Status Window")
    title_label = Label(luna, text="DEMO GUI", fg="green", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    list_box = Listbox(luna, width=40)
    list_box.grid(row=2, column=0, columnspan=4)

    #### START/SHUTDOWN ####

    start_shutdown_label = Label(luna, text="0) Start/Shutdown")
    start_shutdown_label.grid(row=3, column=0, columnspan=2)
    start_button = Button(luna, text="START", command=on_send_button_click)
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
    gett_cap_heater_button.grid(row=6, column=3)

    cap_heater_set_temp_label = Label(luna, text="Set Temp (C):")
    cap_heater_set_temp_label.grid(row=7, column=0)
    cap_heater_set_temp_entry = Entry(luna)
    cap_heater_set_temp_entry.grid(row=7, column=1, columnspan=2)

    sett_cap_heater_button = Button(luna, text="CAPSETT",
                                    command=lambda: sett_cap_heater_button_click(cap_heater_set_temp_entry))
    sett_cap_heater_button.grid(row=7, column=3)

    """High Voltage Supply"""
    high_voltage_label = Label(luna, text="2) High Voltage Supply")
    high_voltage_label.grid(row=8, column=0, columnspan=4)


    voltage_label = Label(luna, text="Voltage (V):")
    current_label = Label(luna, text="Current (A):")

    voltage_label.grid(row=9, column=0)
    current_label.grid(row=9, column=2)

    current_volts = StringVar()
    current_amps = StringVar()

    current_volts_dynamic_label = Label(luna, textvariable=current_volts, width=10)
    current_amps_dynamic_label = Label(luna, textvariable=current_amps, width=10)
    current_volts_dynamic_label.grid(row=10, column=1)
    current_amps_dynamic_label.grid(row=10, column=3)

    getvi_button = Button(luna, text="GETVI", command=on_getvi_button_click)
    getvi_button.grid(row=11, column=3)

    # Set voltage row on GUI
    set_voltage_label = Label(luna, text="set volt:")
    set_voltage_label.grid(row=11, column=0)
    set_voltage_entry = Entry(luna)
    set_voltage_entry.grid(row=11, column=1)
    setv_button = Button(luna, text="SETV", command=lambda: on_setv_button_click(set_voltage_entry))
    setv_button.grid(row=11, column=2)
    """##### Laser Motor #####"""
    laser_motor_label = Label(luna, text="3) Laser Motor")
    laser_motor_label.grid(row=12, column=0, columnspan=4)

    lm_moveleft_button = Button(luna, text="LASLEFT", command=move_left_button_click)
    lm_moveleft_button.grid(row=13, column=1)
    lm_moveright_button = Button(luna, text="LASRIGHT", command=move_right_button_click)
    lm_moveright_button.grid(row=13, column=2)

    lm_lmhome_button = Button(luna, text="LMHOME", command=LMHOME_button_click)
    lm_lmhome_button.grid(row=14, column=1)
    lm_capready_button = Button(luna, text="CAPREADY", command=CAPREADY_button_click)
    lm_capready_button.grid(row=14, column=2)

    """##### Gel Pump #####"""
    gel_pump_label = Label(luna, text="4) gel_pump")
    gel_pump_label.grid(row=15, column=0, columnspan=4)

    gp_home_button = Button(luna, text="GPHOME", command=gp_home_button_click)
    gp_home_button.grid(row=16, column=1)

    gp_start_button = Button(luna, text="GPSTART", command=gp_start_button_click)
    gp_start_button.grid(row=16, column=2)

    gp_up_button = Button(luna, text="GPUP", command=gp_up_button_click)
    gp_up_button.grid(row=18, column=1)

    gp_down_button = Button(luna, text="GPDOWN", command=gp_down_button_click)
    gp_down_button.grid(row=18, column=2)

    set_gprate_label = Label(luna, text="set rate [microL/sec]:")
    set_gprate_label.grid(row=17, column=0)
    set_gprate_entry = Entry(luna)
    set_gprate_entry.grid(row=17, column=1, columnspan=2)
    gp_rate_button = Button(luna, text="GPRATE", command=lambda: gp_rate_button_click(set_gprate_entry))
    gp_rate_button.grid(row=17, column=3)

    """ Stage X and Z"""
    stage_x_and_z_label = Label(luna, text="5) Solution Stage X and Z")
    stage_x_and_z_label.grid(row=20, column=0, columnspan=4)

    x_moveleft_button = Button(luna, text="SXLFTBIG", command=x_moveleft_button_click)
    x_moveleft_button.grid(row=22, column=1)
    x_moveright_button = Button(luna, text="SXRGHTBIG", command=x_moveright_button_click)
    x_moveright_button.grid(row=22, column=3)

    small_x_moveleft_button = Button(luna, text="SXLFTSM", command=small_x_moveleft_button_click)
    small_x_moveleft_button.grid(row=23, column=1)
    small_x_moveright_button = Button(luna, text="SXRGHTSM", command=small_x_moveright_button_click)
    small_x_moveright_button.grid(row=23, column=3)

    z_moveup_button = Button(luna, text="ZUP", command=z_moveup_button_click)
    z_moveup_button.grid(row=21, column=2)
    z_movedown_button = Button(luna, text="ZDOWN", command=z_movedown_button_click)
    z_movedown_button.grid(row=22, column=2)


    x_sample_button = Button(luna, text="SXSAMPLE", command=x_move_to_sample_button_click)
    x_sample_button.grid(row=24, column=0)
    x_buffer_button = Button(luna, text="SXBUFFER", command=x_move_to_buffer_button_click)
    x_buffer_button.grid(row=24, column=1)
    x_water_button = Button(luna, text="SXWATER", command=x_move_to_water_button_click)
    x_water_button.grid(row=24, column=2)
    x_waste_button = Button(luna, text="SXWASTE", command=x_move_to_waste_button_click)
    x_waste_button.grid(row=24, column=3)
    """##### Fluidic Valve #####"""
    fluidic_valve_label = Label(luna, text="6) LAB SMITH Fluid Valve: ")
    fluidic_valve_label.grid(row=25, column=0, columnspan=4)

    valve_set = IntVar()
    valve_set.set(3)
    valve_options = [
        ("A", 1),
        ("B", 2),
        ("CLOSED", 3)
    ]
    for txt, val in valve_options:
        radio_button = Radiobutton(luna, text=txt, variable=valve_set, command=set_fluidic_valve_clicked, value=val)
        radio_button.grid(row=26, column=val)

    """##### Spectrometer #####"""
    spectrometer_label = Label(luna, text="8) Spectrometer: ")
    spectrometer_label.grid(row=27, column=0, columnspan=4)

    set_exposure_time_label = Label(luna, text="set exposure time:")
    set_exposure_time_label.grid(row=28, column=0)
    set_exposure_time_entry = Entry(luna)
    set_exposure_time_entry.grid(row=28, column=1, columnspan=2)
    set_exposure_time_button = Button(luna, text="SPCSETEXP", command=lambda:spectrometer_set_exposure_time_clicked(set_exposure_time_entry))
    set_exposure_time_button.grid(row=28, column=3)

    set_spectrometer_filename_label = Label(luna, text="filename:")
    set_spectrometer_filename_label.grid(row=29, column=0)
    set_spectrometer_filename_entry = Entry(luna)
    set_spectrometer_filename_entry.grid(row=29, column=1)

    set_spectrometer_time_between_label = Label(luna, text="time between reads (ms):")
    set_spectrometer_time_between_label.grid(row=29, column=2)
    set_spectrometer_time_between_entry = Entry(luna)
    set_spectrometer_time_between_entry.grid(row=29, column=3)

    set_spectrometer_duration_label = Label(luna, text="duration (ms):")
    set_spectrometer_duration_label.grid(row=30, column=0)
    set_spectrometer_duration_entry = Entry(luna)
    set_spectrometer_duration_entry.grid(row=30, column=1)

    start_continuous_spectrometer_button = Button(luna,
                                    text="SPCSTARTC",
                                    command=lambda:start_spectrometer_continuous_capture(set_spectrometer_filename_entry,
                                                                                         set_spectrometer_time_between_entry,
                                                                                         set_spectrometer_duration_entry))
    start_continuous_spectrometer_button.grid(row=30, column=2)
    start_continuous_spectrometer_button = Button(luna, text="SPCISCRUN", command=check_continous_capture)
    start_continuous_spectrometer_button.grid(row=30, column=3)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()