from __future__ import print_function
import logging
import subprocess
import time
from Tkinter import *
from serial import *
from threading import Thread, RLock

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

def cont_run_Thread(min):
    """

    :return:
    """
    t_end = time.time() + (60 * min)
    while time.time() < t_end:
        time.sleep(1)
        getvi_THREAD1 = Thread(target=GETVI_Thread)
        getvi_THREAD1.start()
        time.sleep(1)
        capgett_thread1 = Thread(target=CAPGETT_Thread)
        capgett_thread1.start()
        capgett_thread1.join()




##### SEQUENCSE OF AUTOMATION #######
def pt1_run_state_sequence():
    """
    Have the heater on...

    automation function
    for LUNA prototype 1
    :return:
    """
    """
    Initilaize Gel
    """
    # Start at buffer to initialize gel
    # down_thread1 = Thread(target=STAGEZDN_Thread)
    # down_thread1.start() # Probably dont need this thread since the buffer thread will check to see if it's at the buffer or not
    # buffer_thread1 = Thread(target=SXBUFFER_Thread)
    # buffer_thread1.start()
    # up_thread1 = Thread(target=STAGEZUP_Thread)
    # up_thread1.start()

    # Turn on the High Voltage 10kV
    # setv_thread1 = Thread(target=SETV_Thread, kwargs={"set_vol": "10"})
    # setv_thread1.start()
    # # Loops for 3 minutes
    # min = 3
    # t_end = time.time() + (60 * min)
    # while time.time() < t_end:
    #     time.sleep(1)
    #     getvi_THREAD1 = Thread(target=GETVI_Thread)
    #     getvi_THREAD1.start()
    # # Turn off HV
    # setv_thread_off = Thread(target=SETV_Thread, kwargs={"set_vol": "0"})
    # setv_thread_off.start()
    # getvi_thread_off = Thread(target=GETVI_Thread)
    # getvi_thread_off.start()

    # Transition to water
    # transition_down_thread1 = Thread(target=STAGEZDN_Thread)
    # transition_down_thread1.start()
    # transition_water_thread1 = Thread(target=SXWATER_Thread)
    # transition_water_thread1.start()
    # transition_up_thread1 = Thread(target=STAGEZUP_Thread)
    # transition_up_thread1.start()

    """
    Injection
    """
    # down_thread1 = Thread(target=STAGEZDN_Thread)
    # down_thread1.start()
    # sample_thread = Thread(target=SXSAMPLE_Thread)
    # sample_thread.start()
    # up_thread1 = Thread(target=STAGEZUP_Thread)
    # up_thread1.start()
    #
    # # Turn on the High Voltage 5kV
    # setv_thread2 = Thread(target=SETV_Thread, kwargs={"set_vol": "5"})
    # setv_thread2.start()
    # # Loops for 10 seconds
    # sec = 10
    # t_end = time.time() + sec
    # while time.time() < t_end:
    #     time.sleep(1)
    #     getvi_THREAD1 = Thread(target=GETVI_Thread)
    #     getvi_THREAD1.start()
    # # Turn off HV
    # setv_thread_off = Thread(target=SETV_Thread, kwargs={"set_vol": "0"})
    # setv_thread_off.start()
    # getvi_thread_off = Thread(target=GETVI_Thread)
    # getvi_thread_off.start()
    #
    # # Transition to water
    # transition_down_thread2 = Thread(target=STAGEZDN_Thread)
    # transition_down_thread2.start()
    # transition_water_thread2 = Thread(target=SXWATER_Thread)
    # transition_water_thread2.start()
    # transition_up_thread2 = Thread(target=STAGEZUP_Thread)
    # transition_up_thread2.start()
    #
    #
    # """
    # Run
    # """
    # down_thread4 = Thread(target=STAGEZDN_Thread)
    # down_thread4.start() # Probably dont need this thread since the buffer thread will check to see if it's at the buffer or not
    # buffer_thread4 = Thread(target=SXBUFFER_Thread)
    # buffer_thread4.start()
    # up_thread4 = Thread(target=STAGEZUP_Thread)
    # up_thread4.start()
    #
    # # Turn on HV
    # setv_thread_on = Thread(target=SETV_Thread, kwargs={"set_vol": "10"})
    # setv_thread_on.start()
    # getvi_thread_on = Thread(target=GETVI_Thread)
    # getvi_thread_on.start()
    #
    # # Set and turn on Laser
    setlstate_thread_on = Thread(target=SETLSTATE_Thread, kwargs={"state": "ON"})
    setlstate_thread_on.start()
    time.sleep(3)
    getlspower_thread1 = Thread(target=GETLPWR_Thread)
    getlspower_thread1.start()
    time.sleep(3)
    setlpower_thread = Thread(target=SETLPOWER_Thread, kwargs={"watts": 10})
    setlpower_thread.start()
    time.sleep(3)
    getlspower_thread2 = Thread(target=GETLPWR_Thread)
    getlspower_thread2.start()
    time.sleep(3)
    setlstate_thread_off = Thread(target=SETLSTATE_Thread, kwargs={"state": "OFF"})
    setlstate_thread_off.start()
    #
    # # Turn on spectrometer, do this after I test out all the rest.
    #
    # # Start a reader thread
    # running_for_however_long_thread = Thread(target=cont_run_Thread, kwargs={"min": 45})
    # running_for_however_long_thread.start()

def back_and_forth():

    # global automation_lock

    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    right_thread1 = Thread(target=SXRGHTBIG_Thread)
    right_thread1.start()

    left_thread1 = Thread(target=SXLFTBIG_Thread)
    left_thread1.start()

    right_thread2 = Thread(target=SXRGHTBIG_Thread)
    right_thread2.start()

    left_thread2 = Thread(target=SXLFTBIG_Thread)
    left_thread2.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    right_thread1.join()
    left_thread1.join()
    right_thread2.join()
    left_thread2.join()
    up_thread1.join()
    logging.info("Finished start_thread_button_click")

def go_to_sample():
    """

    :return:
    """
    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    command_thread = Thread(target=SXSAMPLE_Thread)
    command_thread.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    command_thread.join()
    up_thread1.join()
    logging.info("Finished going to sample")

def go_to_buffer():
    """
    1) STAGEZDN
    2) SXBUFFER
    3) STAGEZUP
    :return:
    """
    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    command_thread = Thread(target=SXBUFFER_Thread)
    command_thread.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    command_thread.join()
    up_thread1.join()
    logging.info("Finished going to buffer")

def go_to_water():
    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    command_thread = Thread(target=SXWATER_Thread)
    command_thread.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    command_thread.join()
    up_thread1.join()
    logging.info("Finished going to water")

def go_to_waste():
    down_thread1 = Thread(target=STAGEZDN_Thread)
    down_thread1.start()

    command_thread = Thread(target=SXWASTE_Thread)
    command_thread.start()

    up_thread1 = Thread(target=STAGEZUP_Thread)
    up_thread1.start()

    down_thread1.join()
    command_thread.join()
    up_thread1.join()
    logging.info("Finished going to waste")

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
def CAPHEATON_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPHEATON", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        # TODO Need a feedback from the pi
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


def CAPHEATOFF_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPHEATOFF", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        # TODO Need a feedback from the pi
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


def gett_cap_heater_button_click():
    #TODO To make this into a thread and have it in pimain.py
    """

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

def CAPGETT_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPGETT", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


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
    proc.stdin.flush()
    cnum += 1


"""
Laser Motor
"""
def LASLEFT_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LASLEFT", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()

def LASRIGHT_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LASRIGHT", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


def LMHOME_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "LMHOME", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()

def CAPREADY_Thread():
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
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "CAPREADY", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


""" Fluidic Valve Commands """
def FVALVEPOS_Thread(valve_pos = "CLOSED"):
    """
    Thread function that set's the Fluidic Valve to whatever position is passed as the
    parameter
    :param valve_pos: string "A"|"B"|"CLOSED"
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        name = 'FluidValve'
        size = 94 + len(valve_pos)
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "FVALVEPOS", "args": valve_pos}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
    finally:
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

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
    proc.stdin.flush()
    cnum += 1
    out = proc.stdout.readline()
    logging.debug("out = " + out)

"""
Gel Pump
"""
def GPHOME_Thread():
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


def GPSTART_Thread():
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
        proc.stdin.flush()
        cnum += 1
    finally:
        # logging.info("releasing lock from")
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        automation_lock.release()

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
    proc.stdin.flush()
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
    proc.stdin.flush()
    cnum += 1

# def gp_rate_button_click(entry):
#     """
#     GPRATE_10 [microL/sec]
#     :return:
#     """
#     #TODO still need to fix this
#     input = entry.get()
#     global proc
#     global cnum
#     size = 94 + len(input)
#     name = 'Pi'
#     args = input
#     cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
#           {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GPRATE", "args": args}
#     proc.stdin.write(cmd)
#     cnum += 1

################################ Dave's Machines ########################
def kill_pi_clicked():
    """

    :return:
    """
    global proc
    global cnum
    size = 94
    name = 'pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "KILL", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()
    cnum+=1

"""
OBIS Laser
"""

def GETLPWR_Thread():
    """
    Get Laser Power
    CMD: 			GETLPWR
    Device Name: 	OBISLaser
    Response:  		OK________[power in watts]\n
    Example: 		GETLPWR___\n
    Description: 		Will return the current output power (in watts).

    Still need to test
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'OBISLaser'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETLPWR", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()

def SETLPOWER_Thread(watts=1):
    """
    Set Laser Power
    CMD: 			SETLPWR [watts]
    Device Name: 	OBISLaser
    Response: 		OK________\n
    Example: 		SETLPWR___0.01600\n
    Description: 		Will set the current output power (in watts).

    Still need to test
    :param watts:
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        watts = str(watts)
        size = 94 + len(watts)
        name = 'OBISLaser'
        args = watts
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETLPWR", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = "+out)
    finally:
        automation_lock.release()

def SETLSTATE_Thread(state="OFF"):
    """
    Turn Laser ON or OFF
    CMD: 			SETLSTATE [ON|OFF]
    Device Name: 	OBISLaser
    Response: 		OK________\n
    Example:		SETLSTATE_OFF\n
    Description:		Will turn on or off the laser.

    Still need to test
    Command to turn on the OBIS Laser on/off
    :param state: "ON" or "OFF" (default)
    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94 + len(state)
        name = 'OBISLaser'
        args = state
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETLSTATE", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = "+out)
    finally:
        automation_lock.release()



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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        # logging.info("releasing lock from")
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
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
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()


"""
High Voltage Power Supply
"""
def GETVI_Thread2():
    """
    I don't think I need this thread but just keep it as a reference...
    :return:
    """
    counter = 0

    global proc
    global cnum
    size = 94
    name = 'HighVoltageSupply'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETVI", "args": args}
    while(counter<5):
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum+=1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
        time.sleep(5)
        counter+=1

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
    proc.stdin.flush()
    out = proc.stdout.readline()
    logging.debug("out = "+out)
    cnum+=1

def GETVI_Thread():
    """

    :return:
    """
    global proc, cnum, automation_lock
    automation_lock.acquire()
    try:
        size = 94
        name = 'HighVoltageSupply'
        args = ''
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "GETVI", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = " + out)
    finally:
        automation_lock.release()

def SETV_Thread(set_vol="10"):
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
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
              {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETV", "args": args}
        proc.stdin.write(cmd)
        proc.stdin.flush()
        cnum += 1
        out = proc.stdout.readline()
        logging.debug("out = "+out)
    finally:
        automation_lock.release()

def continuouse_GETVI():
    # global automation_lock

    setv_thread1 = Thread(target=SETV_Thread, kwargs={"set_vol": "10"})
    setv_thread1.start()
    min = 3
    t_end = time.time()+(60*min)
    # Loops for 3 minutes   ^
    while time.time() < t_end:
        getvi_THREAD1 = Thread(target=GETVI_Thread)
        getvi_THREAD1.start()
    setv_thread0 = Thread(target=SETV_Thread, kwargs={"set_vol": "0"})
    setv_thread0.start()
    getvi_THREAD = Thread(target=GETVI_Thread)
    getvi_THREAD.start()

    getvi_THREAD1.join()
    setv_thread1.join()
    setv_thread0.join()
    getvi_THREAD.join()
    logging.info("Finished start_thread_button_click")

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
    # Check if proc returned anything...
    if proc is None or proc.returncode is not None:
        if proc.returncode is not None:
            print ("LunaSrv exited immediately with a return code" + (str(proc.returncode)))
        else:
            print (" Failed to start LunaSrv")
        sys.exit(-1)
    """
    Main difference here with Lock, Threads, along with the gui
    """
    global automation_lock
    automation_lock = RLock()
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

    turn_on_cap_heater_button = Button(luna, text="Turn On Heater", command=CAPHEATON_Thread)
    turn_on_cap_heater_button.grid(row=5, column=0, columnspan=2)
    turn_off_cap_heater_button = Button(luna, text="Turn Off Heater", command=CAPHEATOFF_Thread)
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

    getvi_button = Button(luna, text="GETVI", command=GETVI_Thread)
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

    lm_moveleft_button = Button(luna, text="LASLEFT", command=continuouse_GETVI)
    lm_moveleft_button.grid(row=13, column=1)
    lm_moveright_button = Button(luna, text="LASRIGHT", command=LASRIGHT_Thread)
    lm_moveright_button.grid(row=13, column=2)

    lm_lmhome_button = Button(luna, text="LMHOME", command=LMHOME_Thread)
    lm_lmhome_button.grid(row=14, column=1)
    lm_capready_button = Button(luna, text="CAPREADY", command=CAPREADY_Thread)
    lm_capready_button.grid(row=14, column=2)

    """##### Gel Pump #####"""
    gel_pump_label = Label(luna, text="4) gel_pump")
    gel_pump_label.grid(row=15, column=0, columnspan=4)

    gp_home_button = Button(luna, text="GPHOME", command=GPHOME_Thread)
    gp_home_button.grid(row=16, column=1)

    gp_start_button = Button(luna, text="GPSTART", command=GPSTART_Thread)
    gp_start_button.grid(row=16, column=2)

    gp_up_button = Button(luna, text="GPUP", command=gp_up_button_click)
    gp_up_button.grid(row=18, column=1)

    gp_down_button = Button(luna, text="GPDOWN", command=gp_down_button_click)
    gp_down_button.grid(row=18, column=2)

    """ Stage X and Z"""
    stage_x_and_z_label = Label(luna, text="5) Solution Stage X and Z")
    stage_x_and_z_label.grid(row=20, column=0, columnspan=4)

    z_moveup_button = Button(luna, text="ZUP", command=STAGEZUP_Thread)
    z_moveup_button.grid(row=21, column=2)
    z_movedown_button = Button(luna, text="ZDOWN", command=STAGEZDN_Thread)
    z_movedown_button.grid(row=22, column=2)

    x_sample_button1 = Button(luna, text="LEFT", command=go_to_sample)
    x_sample_button1.grid(row=24, column=0)

    x_sample_button = Button(luna, text="SXSAMPLE", command=go_to_sample)
    x_sample_button.grid(row=24, column=0)
    x_buffer_button = Button(luna, text="SXBUFFER", command=go_to_buffer)
    x_buffer_button.grid(row=24, column=1)
    x_water_button = Button(luna, text="SXWATER", command=go_to_water)
    x_water_button.grid(row=24, column=2)
    x_waste_button = Button(luna, text="SXWASTE", command=go_to_waste)
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
    # spectrometer_label = Label(luna, text="8) Spectrometer: ")
    # spectrometer_label.grid(row=27, column=0, columnspan=4)
    #
    # set_exposure_time_label = Label(luna, text="set exposure time:")
    # set_exposure_time_label.grid(row=28, column=0)
    # set_exposure_time_entry = Entry(luna)
    # set_exposure_time_entry.grid(row=28, column=1, columnspan=2)
    # set_exposure_time_button = Button(luna, text="SPCSETEXP",
    #                                   command=lambda: spectrometer_set_exposure_time_clicked(set_exposure_time_entry))
    # set_exposure_time_button.grid(row=28, column=3)
    #
    # set_spectrometer_filename_label = Label(luna, text="filename:")
    # set_spectrometer_filename_label.grid(row=29, column=0)
    # set_spectrometer_filename_entry = Entry(luna)
    # set_spectrometer_filename_entry.grid(row=29, column=1)
    #
    # set_spectrometer_time_between_label = Label(luna, text="time between reads (ms):")
    # set_spectrometer_time_between_label.grid(row=29, column=2)
    # set_spectrometer_time_between_entry = Entry(luna)
    # set_spectrometer_time_between_entry.grid(row=29, column=3)
    #
    # set_spectrometer_duration_label = Label(luna, text="duration (ms):")
    # set_spectrometer_duration_label.grid(row=30, column=0)
    # set_spectrometer_duration_entry = Entry(luna)
    # set_spectrometer_duration_entry.grid(row=30, column=1)
    #
    # start_continuous_spectrometer_button = Button(luna,
    #                                               text="SPCSTARTC",
    #                                               command=lambda: start_spectrometer_continuous_capture(
    #                                                   set_spectrometer_filename_entry,
    #                                                   set_spectrometer_time_between_entry,
    #                                                   set_spectrometer_duration_entry))
    # start_continuous_spectrometer_button.grid(row=30, column=2)
    # start_continuous_spectrometer_button = Button(luna, text="SPCISCRUN", command=check_continous_capture)
    # start_continuous_spectrometer_button.grid(row=30, column=3)

    kill_pi_button = Button(luna, text="kill pi", command=kill_pi_clicked)
    kill_pi_button.grid(row=31, column=1)

    start_automation_button = Button(luna, text="START AUTO", command=pt1_run_state_sequence)
    start_automation_button.grid(row=31, column=2)

    """
    Turn off gui, then terminate the subproccess
    """
    luna.mainloop()
    proc.terminate()