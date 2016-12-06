from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread
import subprocess

cnum = 1

# current_volts = None
# current_amps = None
# list_box = None

"""
Luna Server Process
"""
cmd = [
    "python",
    "../LunaSrv/lunasrv.py"
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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

    while(True):
        out = proc.stdout.readline()
        print "output is "+out
        cmd = out[84:93].strip()
        args = out[94:].strip()
        # print "cmd is "+cmd
        # print "args is "+args

        if cmd=="INVTHW":
            instrument_name = out[20:65].strip()
            list_box.insert(END, instrument_name+" is "+args)
        elif cmd=="SHUTDOWN": #Won't output Shutdown because there's no response.
            luna.quit()
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

reader_thread = Thread(target=the_reader_thread)
# Set the thread as a daemon thread, aka when the gui closes down, the thread also ends.
reader_thread.daemon = True
reader_thread.start()

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

if __name__ == '__main__':
    """
    1) Start reader_thread
    """
    """"Title ('Optokey')"""
    luna.wm_title("Status Window")
    title_label = Label(luna, text="OPTOKEY", fg="red", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    list_box = Listbox(luna, width=40)
    list_box.grid(row=2, column=0, columnspan=4)

    voltage_label = Label(luna, text="Voltage (V):")
    current_label = Label(luna, text="Current (A):")

    sample_temp_label = Label(luna, text="Sample Temp(C):") # not using right now
    block_temp_label = Label(luna, text="Block Temp(C):")  # not using right now
    current_cycle_label = Label(luna, text="Current Cycle:")  # not using right now
    number_of_steps_label = Label(luna, text="Steps:")  # not using right now

    voltage_label.grid(row=3, column=0)
    current_label.grid(row=3, column=2)
    sample_temp_label.grid(row=6, column=0)
    block_temp_label.grid(row=6, column=2)
    current_cycle_label.grid(row=7, column=0)
    number_of_steps_label.grid(row=7, column=2)

    current_volts = StringVar()
    current_amps = StringVar()
    current_sample_temp = StringVar()
    current_block_temp = StringVar()
    current_cycle = StringVar()
    current_number_of_steps = StringVar()

    getvi_button = Button(luna, text="GETVI", command=on_getvi_button_click)
    getvi_button.grid(row=5, column=2, columnspan=2)
    current_volts_dynamic_label = Label(luna, textvariable=current_volts, width=10)
    current_amps_dynamic_label = Label(luna, textvariable=current_amps, width=10)
    current_volts_dynamic_label.grid(row=3, column=1)
    current_amps_dynamic_label.grid(row=3, column=3)
    sample_temp_dynamic_label = Label(luna, textvariable=current_sample_temp, width=10)
    block_temp_dynamic_label = Label(luna, textvariable=current_block_temp, width=10)
    current_cycle_dynamic_label = Label(luna, textvariable=current_cycle, width=10)
    number_of_steps_dynamic_label = Label(luna, textvariable=current_number_of_steps, width=10)
    sample_temp_dynamic_label.grid(row=6, column=1)
    block_temp_dynamic_label.grid(row=6, column=3)
    current_cycle_dynamic_label.grid(row=7, column=1)
    number_of_steps_dynamic_label.grid(row=7, column=3)

    send_button = Button(luna, text="START", command = on_send_button_click)
    send_button.grid(row=5, column=0, columnspan=2)

    # Set voltage row on GUI
    set_voltage_label = Label(luna, text="set volt:")
    set_voltage_label.grid(row=4, column=0)
    set_voltage_entry = Entry(luna)
    set_voltage_entry.grid(row=4, column=1, columnspan=2)
    setv_button = Button(luna, text="SETV", command=lambda: on_setv_button_click(set_voltage_entry))
    setv_button.grid(row=4, column=3)

    # Set cycle number row on GUI
    set_cycle_number_label = Label(luna, text="Cycle Number:")
    set_cycle_number_label.grid(row=8, column=0)
    set_cycle_number_entry = Entry(luna)
    set_cycle_number_entry.grid(row=8, column=1, columnspan=2)
    start_TEC_Seq_button = Button(luna, text="Start TEC", command=lambda:start_TEC_Seq_button_click(set_cycle_number_entry))
    start_TEC_Seq_button.grid(row=8, column=3)

    read_TEC_Seq_button = Button(luna, text="Read TEC status", command=read_TEC_Seq_button_click)
    read_TEC_Seq_button.grid(row=9, column=0)
    stop_TEC_Seq_button = Button(luna, text="Stop TEC", command=stop_TEC_Seq_button_click)
    stop_TEC_Seq_button.grid(row=9, column=1)
    shutdown_button = Button(luna, text="Shutdown", command=shutdown_button_click)
    shutdown_button.grid(row=9, column=3)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()
# luna.mainloop()
