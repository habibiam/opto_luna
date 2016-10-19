from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread

import subprocess



class LunaUI(Tk):
    def setReaderPipe(self, pipe):
        self._pipe = pipe

    def __init__(self):
        Tk.__init__(self)


# luna = LunaUI()
# luna.wm_title("Status Window")
# # input = serial.Serial()
#
# current_volts = StringVar()
# current_amps = StringVar()
# cur_temp = StringVar()
#
#
# def connectBtn():
#     data = luna._pipe.recv()
#     cur_temp.set(str(data))
#     luna.update()
#
# def display_current_volt_and_current():
#     volts, current = luna._pipe.recv()
#     current_volts.set(str(volts))
#     current_amps.set(str(current))
#     luna.update()
#
#
# voltage_label = Label(luna, text="Voltage (V):")
# current_label = Label(luna, text="Current (A):")
# temp_label = Label(luna, text="Temperature(C):")
#
# current_volts_dynamic_label = Label(luna, textvariable=current_volts)
# current_amps_dynamic_label = Label(luna, textvariable=current_amps)
# current_temp_dynamic_label = Label(luna, textvariable=cur_temp)
#
# set_voltage_label = Label(luna, text="Volts")
# set_voltage_entry = Entry(luna)
# write_button = Button(luna, text="SEND", command=display_current_volt_and_current)
#
# voltage_label.grid(row=0, column=0)
# current_label.grid(row=0, column=1)
# temp_label.grid(row=0, column=2)
#
# current_volts_dynamic_label.grid(row=1, column=0)
# current_amps_dynamic_label.grid(row=1, column=1)
# current_temp_dynamic_label.grid(row=1, column=2)
#
# set_voltage_label.grid(row=2, column=0)
# set_voltage_entry.grid(row=2, column=1)
# write_button.grid(row=2, column=2)

def on_send_button_click():
    global proc
    global cnum
    size = 94
    name = ''
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "INVTHW", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def on_getvi_button_click():
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
    # print entry.get()
    global proc
    global cnum
    size = 94 + len(input)
    name = 'HighVoltageSupply'
    args = input
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETV", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

def the_reader_thread():
    """
    A function that starts in another thread.
    Continuously runs in order to read stdout and then from there display it onto the status window
    :return:
    """
    global proc
    global current_amps
    global current_volts
    global current_status

    while(True):
        out = proc.stdout.readline()
        print "output is "+out
        cmd = out[84:93].strip()
        args = out[94:].strip()
        print "cmd is "+cmd
        print "args is "+args
        if cmd == "GETVI" and (args == "SYNTAX" or args == ""):
            on_getvi_button_click()
            print "loop"
        elif cmd == "GETVI" and args != "FAIL":
            args = out[94:]
            print args
            args_list = args.split()
            # might have to convert volt and current to floats
            volt = args_list[0]
            current = args_list[1]
            current_volts.set(volt)
            current_amps.set(current)
            list_box.insert(END, "Received current voltage and current.")
        elif cmd == "INVTHW":
            instrument_name = out[20:65].strip()
            list_box.insert(END, instrument_name+" is "+args)
        elif cmd == "SETV":
            list_box.insert(END, "Set voltage")
            # pass
            # current_status.set(out)
        print cmd

proc = None
cnum = 1
reader_thread = None

current_volts = None
current_amps = None
current_status = None
list_box = None

if __name__ == '__main__':
    cmd = [
        "python",
        "lunasrv.py"
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # start reader thread
    reader_thread = Thread(target=the_reader_thread)
    reader_thread.start()

    # start GUI
    luna = LunaUI()
    luna.wm_title("Status Window")
    title_label = Label(luna, text="OPTOKEY", fg="red", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=4)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    # current_status = StringVar()
    # status_label = Label(luna, textvariable=current_status)
    # status_label.grid(row=1, column=0, rowspan=2, columnspan=2)
    list_box = Listbox(luna, width=40)
    list_box.grid(row=2, column=0, columnspan=4)

    voltage_label = Label(luna, text="Voltage (V):")
    current_label = Label(luna, text="Current (A):")
    temp_label = Label(luna, text="Temperature(C):") # not using right now

    voltage_label.grid(row=3, column=0)
    current_label.grid(row=3, column=2)

    current_volts = StringVar()
    current_amps = StringVar()
    # cur_temp = StringVar()

    send_button = Button(luna, text="START", command = on_send_button_click)
    send_button.grid(row=5, column=0, columnspan=2)
    getvi_button = Button(luna, text="GETVI", command=on_getvi_button_click)
    getvi_button.grid(row=5, column=2, columnspan=2)
    current_volts_dynamic_label = Label(luna, textvariable=current_volts, width=10)
    current_amps_dynamic_label = Label(luna, textvariable=current_amps, width=10)
    current_volts_dynamic_label.grid(row=3, column=1)
    current_amps_dynamic_label.grid(row=3, column=3)

    set_voltage_label = Label(luna, text="set volt:")
    set_voltage_label.grid(row=4, column=0)

    set_voltage_entry = Entry(luna)
    set_voltage_entry.grid(row=4, column=1, columnspan=2)
    setv_button = Button(luna, text="SETV", command=lambda: on_setv_button_click(set_voltage_entry))
    setv_button.grid(row=4, column=3)
    luna.mainloop()

# luna.mainloop()
