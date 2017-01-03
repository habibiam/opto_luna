from Tkinter import *
# import Tkinter as tk
from time import sleep
from serial import *

from threading import Thread
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

def back_and_forth():

    right_thread1.start()
    right_thread1.join()
    left_thread1.start()
    left_thread1.join()
    right_thread2.start()
    right_thread2.join()
    left_thread2.start()

    # rnge = 6
    # for i in range(rnge):
    #     if i%2==0:
    #
    #     else:
    #         left_thread.start()
    #         if i!=(rnge-1):
    #
    # right_thread2.join()
    print "Finished start_thread_button_click"

def up_and_down():

    down_thread1.start()
    down_thread1.join()
    up_thread2.start()
    up_thread2.join()
    down_thread2.start()
    down_thread2.join()
    up_thread1.start()

###############################################################333
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
1) INVTHW
2) SXRGHTBIG
3) SXLFTBIG
"""

def thread_1():
    """
    Move right
    :return:
    """
    global proc
    global cnum

    size = 94
    name = 'Pi'
    args = ''
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SXRGHTBIG", "args": args}
    logging.debug("in thread 1 before write")
    proc.stdin.write(cmd)
    cnum += 1
    # # Print if it got the message successfully
    # out = proc.stdout.readline()
    # print(out)
    # id = out[:10].strip()
    # length = out[10:20].strip()
    # device_name = out[20:84].strip()
    # cmd = out[84:94].strip()
    # args = out[94:]
    logging.debug("in thread 1")
    return


def left_big_thread():
    """
    Move Left
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
    logging.debug("in thread 1")
    return
################################ Dave's Machines ########################


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

# dict_of_devices_and_commands \
#     = {'HighVoltageSupply': ["GETVI", "SETV"],
#        'TECController': ["STARTSEQ", "STOPSEQ", "READSEQD"],
#        'OBISLaser': ["GETLPWR", "SETLPWR", "SETLSTATE"],
#        'Spectrometer': ["SPCSETEXP", "SPCSTARTC", "SPCISCRUN"],
#        'FluidValve': ['FVALVEPOS'],
#        # Dave's Instruments
#        'Pi': ['CAPHEATON', 'CAPHEATOFF', 'CAPGETT', 'CAPSETT',
#               'MOVELEFT', 'MOVERIGHT', 'LMHOME', 'CAPREADY',
#               'GPHOME', 'GPRATE', 'GPSTART',
#               'RWHOME', 'RWRATE',
#               'RPHOME', 'RPRATE',
#               'RBHOME', 'RBRATE',
#               'RMHOME', 'RMRATE',
#               'CHIPZHOME', 'CHIPZUP',
#               'CHIPYHOME', 'CHIPYOUT']
#              + ['v' + str(i) for i in range(1, 21)]
#        }

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

def on_setv_automation(set_vol=10):
    global proc
    global cnum
    set_vol = str(set_vol)
    size = 94 + len(set_vol)
    name = 'HighVoltageSupply'
    args = set_vol
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": name, "cmd": "SETV", "args": args}
    proc.stdin.write(cmd)
    cnum+=1

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
    while(True):
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

    right_thread1 = Thread(name="Go RIGHT1", target=x_moveright_button_click)
    left_thread1 = Thread(name="Go LEFT1", target=x_moveleft_button_click)
    right_thread2 = Thread(name="Go RIGHT2", target=x_moveright_button_click)
    left_thread2 = Thread(name="Go LEFT2", target=x_moveleft_button_click)

    up_thread1 = Thread(target=z_moveup_button_click)
    up_thread2 = Thread(target=z_moveup_button_click)
    down_thread1 = Thread(target=z_movedown_button_click)
    down_thread2 = Thread(target=z_movedown_button_click)

    HV_10_kV_on_thread = Thread(name="init gel HV on 10kV", target=on_setv_automation)
    HV_5_kV_on_thread = Thread(name="init gel HV on 5kV", target=lambda: on_setv_automation(set_vol=5))
    # HV_5_kV_on_thread = Thread(name="init gel HV on 5kV", target=on_setv_automation, args=(5, ))
    move_down_thread1 = Thread(name="go down1", target=z_movedown_button_click)
    move_down_thread2 = Thread(name="go down2", target=z_movedown_button_click)
    move_down_thread3 = Thread(name="go down3", target=z_movedown_button_click)
    move_down_thread4 = Thread(name="go down4", target=z_movedown_button_click)
    move_up_thread1 = Thread(name="go up1", target=z_moveup_button_click)
    move_up_thread2 = Thread(name="go up2", target=z_moveup_button_click)
    move_up_thread3 = Thread(name="go up3", target=z_moveup_button_click)
    move_up_thread4 = Thread(name="go up4", target=z_moveup_button_click)
    move_up_thread5 = Thread(name="go up5", target=z_moveup_button_click)

    move_to_water_thread1 = Thread(name="Go to water1", target=x_move_to_water_button_click)
    move_to_water_thread2 = Thread(name="Go to water2", target=x_move_to_water_button_click)
    move_to_sample_thread1 = Thread(name="Go to sample1", target=x_move_to_sample_button_click)
    move_to_buffer_thread1 = Thread(name="Go to buffer1", target=x_move_to_buffer_button_click)
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
