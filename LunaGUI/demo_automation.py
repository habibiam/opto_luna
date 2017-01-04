from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread, Lock, RLock
import subprocess
import itertools

import logging
from tendo import singleton

FORMAT = '%(levelname)s:%(funcName)s:%(message)s'
format1 = '(%(threadName)-10s) %(message)s'
logging.basicConfig(format=format1, level=logging.DEBUG)

# This line of code will only make it so that only one instance of the gui is running.
# from tendo import singleton
me = singleton.SingleInstance()


class KevinsThreadWithArgs(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name,
                        verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        return



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

def the_reader_thread():
    """

    Need this reader thread to flush out proc.stdout
    :return:
    """
    while (True):
        out = proc.stdout.readline()
        id = out[:10].strip()
        length = out[10:20].strip()
        device_name = out[20:84].strip()
        cmd = out[84:94].strip()
        args = out[94:]
        if cmd == "INVTHW":
            logging.info("Inside back_and_forth: %s", out)
            if device_name == "FluidValve":
                return



##### SEQUENCSE OF AUTOMATION #######
def back_and_forth():

    global automation_lock

    right_thread1 = Thread(target=SXRGHTBIG_Thread)
    right_thread1.start()

    left_thread1 = Thread(target=SXLFTBIG_Thread)
    left_thread1.start()

    right_thread2 = Thread(target=SXRGHTBIG_Thread)
    right_thread2.start()

    left_thread2 = Thread(target=SXLFTBIG_Thread)
    left_thread2.start()

    right_thread1.join()
    left_thread1.join()
    right_thread2.join()
    left_thread2.join()
    logging.info("Finished start_thread_button_click")

def up_and_down():


    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    up_thread2 = Thread(target=STAGEZUP_Thread)
    up_thread2.start()

    down_thread2 = Thread(target=STAGEZDN_Thread)
    down_thread2.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    up_thread2.join()
    up_thread1.join()
    down_thread2.join()
    logging.info("Up and down function")


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
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPHOME", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()


def gp_start_button_click():
    """
    GPSTART
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPSTART", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()


def gp_rate_button_click(entry):
    """
    GPRATE_10 [microL/sec]
    :return:
    """
    #TODO still need to fix this
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

################################ Dave's Machines ########################


"""
Solution Stage X and Z
"""
def SXLFTBIG_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXLFTBIG", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def SXRGHTBIG_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXRGHTBIG", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def SXLFTSM_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXLFTSM", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def SXRGHTSM_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXRGHTSM", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def STAGEZUP_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STAGEZUP", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()


def SXSAMPLE_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXSAMPLE", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()


def SXBUFFER_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXBUFFER", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def SXWATER_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXWATER", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

def SXWASTE_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXWASTE", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()
        return

def STAGEZDN_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "STAGEZDN", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()


"""
High Voltage Power Supply
"""
def on_getvi_button_click():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'Pi'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETVI", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()

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

def on_setv_automation(set_vol=10):
    """

    :param set_vol:
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        set_vol = str(set_vol)
        size = 94 + len(set_vol)
        name = 'HighVoltageSupply'
        args = set_vol
        cmd = '%(cnum)01u0d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETV", "args": args}
        proc.stdin.write(cmd)
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = "+out)
    finally:
        automation_lock.release()


def start_thread_button_click():
    """

    :return:
    """
    """
    * In Buffer
    1) Start HV at 10kV
    """
    # HV_10_kV_on_thread.start()
    # HV_10_kV_on_thread.join()
    # logging.info("going to sleep now")
    # time.sleep(30)
    # logging.info("exiting sleep now")
    # HV_10_kV_off_thread.start()
    # HV_10_kV_off_thread.join()
    # transition()
    move_down_thread1.start()
    move_down_thread1.join()
    move_to_water_thread1.start()
    move_to_water_thread1.join()
    move_up_thread2.start()
    # move_up_thread2.join()
    # move_down_thread2.start()
    # move_down_thread2.join()
    # Injection
    # move_to_sample_thread1.start()
    # move_to_sample_thread1.join()
    # move_up_thread3.start()
    # move_up_thread3.join()
    # HV_5_kV_on_thread.start()
    # HV_5_kV_on_thread.join()
    # time.sleep(10)
    # HV_5_kV_off_thread.start()
    # HV_5_kV_off_thread.join()
    # transition()
    # move_down_thread3.start()
    # move_down_thread3.join()
    # move_to_water_thread2.start()
    # move_to_water_thread2.join()
    # move_up_thread4.start()
    # move_up_thread4.join()
    # move_down_thread4.start()
    # move_down_thread4.join()
    # Go to Buffer
    # move_to_buffer_thread1.start()
    # move_to_buffer_thread1.join()
    # move_up_thread5.start()
    logging.info("Successfully ran through the automation script")

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
    """
    Main difference here with Lock, Threads, along with the gui
    """
    global automation_lock
    automation_lock = RLock()

    # right_thread1 = Thread(name="Go RIGHT1", target=x_moveright_button_click)
    # left_thread1 = Thread(name="Go LEFT1", target=x_moveleft_button_click)
    # right_thread2 = Thread(name="Go RIGHT2", target=x_moveright_button_click)
    # left_thread2 = Thread(name="Go LEFT2", target=x_moveleft_button_click)

    # up_thread1 = Thread(target=z_moveup_button_click)
    # up_thread2 = Thread(target=z_moveup_button_click)
    # down_thread1 = Thread(target=z_movedown_button_click)
    # down_thread2 = Thread(target=z_movedown_button_click)

    HV_10_kV_on_thread = Thread(name="init gel HV on 10kV", target=on_setv_automation)
    HV_5_kV_on_thread = Thread(name="init gel HV on 5kV", target=lambda: on_setv_automation(set_vol=5))
    # HV_5_kV_on_thread = Thread(name="init gel HV on 5kV", target=on_setv_automation, args=(5, ))
    move_down_thread1 = Thread(name="go down1", target=STAGEZDN_Thread)
    move_down_thread2 = Thread(name="go down2", target=STAGEZDN_Thread)
    move_down_thread3 = Thread(name="go down3", target=STAGEZDN_Thread)
    move_down_thread4 = Thread(name="go down4", target=STAGEZDN_Thread)
    move_up_thread1 = Thread(name="go up1", target=STAGEZUP_Thread)
    move_up_thread2 = Thread(name="go up2", target=STAGEZUP_Thread)
    move_up_thread3 = Thread(name="go up3", target=STAGEZUP_Thread)
    move_up_thread4 = Thread(name="go up4", target=STAGEZUP_Thread)
    move_up_thread5 = Thread(name="go up5", target=STAGEZUP_Thread)

    move_to_water_thread1 = Thread(name="Go to water1", target=SXWATER_Thread)
    move_to_water_thread2 = Thread(name="Go to water2", target=SXWATER_Thread)
    move_to_sample_thread1 = Thread(name="Go to sample1", target=SXSAMPLE_Thread)
    move_to_buffer_thread1 = Thread(name="Go to buffer1", target=SXBUFFER_Thread)
    # HV_10_kV_off_thread = Thread(name="init gel HV off 10kV", target=on_setv_automation(set_vol=0))
    HV_10_kV_off_thread = Thread(name="init gel HV off 10kV", target=lambda: on_setv_automation(set_vol=0))
    HV_5_kV_off_thread = Thread(name="init gel HV off 5kV", target=lambda: on_setv_automation(set_vol=0))
    # reader_thread = Thread(target=the_reader_thread)
    # Set the thread as a daemon thread, aka when the gui closes down, the thread also ends.

    # reader_thread.daemon = True
    # reader_thread.start()

    """"Title ('Optokey')"""
    luna.wm_title("Status Window")
    title_label = Label(luna, text="DEMO GUI", fg="red", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=8)

    current_status_label = Label(luna, text="Current Status")
    current_status_label.grid(row=1, column=0, columnspan=4)
    # list_box =(row=2, column=0, columnspan=4)

    #### START/SHUTDOWN ####

    start_shutdown_label = Label(luna, text="0) Start/Shutdown")
    start_shutdown_label.grid(row=3, column=0, columnspan=2)
    start_button = Button(luna, text="START", command=on_send_button_click)
    start_button.grid(row=3, column=2)

    shutdown_button = Button(luna, text="Shutdown", command=shutdown_button_click)
    shutdown_button.grid(row=3, column=3)

    # start_thread_button = Button(luna, text="Start Thread", command=start_thread_button_click)
    l_and_r_thread = Button(luna, text="Back and Forth", command=back_and_forth)
    l_and_r_thread.grid(row=4, column=2)

    u_and_d_thread = Button(luna, text="Up and Down", command=up_and_down)
    u_and_d_thread.grid(row=4, column=1)

    start_automation_thread_button = Button(luna, text="Start automation", command=start_thread_button_click)
    start_automation_thread_button.grid(row=5, column=1)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()
