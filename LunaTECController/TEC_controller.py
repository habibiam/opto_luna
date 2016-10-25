#===============================================================================
# Luna TEC controller 
# Using OvenIndustry controller board
#
# Oct. 13:
# Adding check for sample tmpr reaching x degree of setpoint
#===============================================================================

import serial
import numpy
import drawnow
import matplotlib.pyplot as plt 
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
from Function import *
from CheckSerial import *
#from test.test_zlib import ChecksumTestCase
import time
import os
from sys import argv
import posix_ipc # sudo pip install posix_ipc
import mmap
import signal
import process_lock



IDLE_TMPR = 30  # 12% duty cycle set block tmpr to about 30C
graph_points = 100
global gSerial_port
global gTmpr
#mapfile is a descriptor to a memory mapped file
mapfile = None
shared_mem_lock = None

# initial setup for manual control = 1, output = 2
CMD_TYPE_CFG    = 1
CMD_TYPE_OUTPUT = 2
gdbg_file_h    = 0
LOG = 1     # log to file 
prntflg = 1 # print out to console

# gPID_gains_h = 0
gdbg_file_h  = 0

Tmpr_arr = []
Tblock_arr  = []
Tsample_arr = []
plot_data_ctr = 0 # reset data plot 
default_num_cycles = 1
current_cycle = 0
gTsample = Tblock = 0

# controller gains
step0_Kp_ramp    = 0 
step0_Kp_ss      = 0
step0_Kp_ss_hold = 0
step0_Ti_ramp    = 0 
step0_Ti_ss      = 0
step0_Kd_ramp    = 0 
step0_Kd_ss      = 0
step0_U_ss       = 0
step0_st1st2trans_blk = 0
step0_st2st3trans_smp = 0

step1_Kp_ramp    = 0 
step1_Kp_ss      = 0
step1_Kp_ss_hold = 0
step1_Ti_ramp    = 0 
step1_Ti_ss      = 0
step1_Kd_ramp    = 0 
step1_Kd_ss      = 0
step1_U_ss       = 0
step1_st1st2trans_blk = 0
step1_st2st3trans_smp = 0

step2_Kp_ramp    = 0 
step2_Kp_ss      = 0
step2_Kp_ss_hold = 0
step2_Ti_ramp    = 0 
step2_Ti_ss      = 0
step2_Kd_ramp    = 0 
step2_Kd_ss      = 0
step2_U_ss       = 0
step2_st1st2trans_blk = 0
step2_st2st3trans_smp = 0

step3_Kp_ramp    = 0 
step3_Kp_ss      = 0
step3_Kp_ss_hold = 0
step3_Ti_ramp    = 0 
step3_Ti_ss      = 0
step3_Kd_ramp    = 0 
step3_Kd_ss      = 0
step3_U_ss       = 0
step3_st1st2trans_blk = 0
step3_st2st3trans_smp = 0

step4_Kp_ramp    = 0 
step4_Kp_ss      = 0
step4_Kp_ss_hold = 0
step4_Ti_ramp    = 0 
step4_Ti_ss      = 0
step4_Kd_ramp    = 0 
step4_Kd_ss      = 0
step4_U_ss       = 0
step4_st1st2trans_blk = 0
step4_st2st3trans_smp = 0


# Sample control params
gStpoint_step0              = 0
gOvershoot_step0            = 0
gOvershoot_hold_time_step0  = 0
gHold_time_step1            = 0

gStpoint_step1              = 0
gOvershoot_step1            = 0
gOvershoot_hold_time_step1  = 0
gHold_time_step1            = 0

gStpoint_step2              = 0
gUndershoot_step2           = 0 
gUndershoot_hold_time_step2 = 0
gHold_time_step2            = 0 

gStpoint_step3              = 0
gOvershoot_step3            = 0 
gOvershoot_hold_time_step3  = 0
gHold_time_step3            = 0 

gStpoint_step4              = 0
gOvershoot_step4            = 0 
gOvershoot_hold_time_step4  = 0
gHold_time_step4            = 0  
 
gCoef0 = 0
gCoef1 = 0
gCoef1 = 0
Sample_time_constant = 0

#  Calibration for all thermisters  ** should be in config file change to config_file
# Thermister 1: [  5.80065359   4.3872549   47.77777778]
# Thermister 2: [  5.80065359   4.3872549   47.77777778]
# Iulius: [-534.54545455  901.27272727 -262.        ]
# Thermister 3: [ -4.18660287  40.93700159   6.87240829]
# y = ax^2 + bx + c
Sample_time_constant = 5.0 # secs


def write_to_shared_memory(a_map_file, s):
    global shared_mem_lock

    try:
        shared_mem_lock.acquire()
        a_map_file.seek(0)
        a_map_file.write(s)
        shared_mem_lock.release()
    except Exception, e:
        log_dbg(e.message)

#===============================================================================
# Create figure window
#===============================================================================
def plot_blk_smp(): 
    global gTmpr
    
    plt.ylim(30,110)                                 # y axis limits
    plt.title('Block Data (thermister')             
    plt.grid(True)                                  # grid on
    plt.ylabel('Tmpr deg C')                            
    plt.plot(Tblock_arr, 'r-', label='Tblock')       #plot the temperature
    plt.legend(loc='upper left')                    
    plt2=plt.twinx()
    plt.ylim(30, 110)
    major_ytick = numpy.arange(0, 110, 5)
    minor_ytick = numpy.arange(0, 110, 2)
#     plt.set_yticks( major_ytick )
#     plt.set_yticks( minor_ytick, minor = True)      
    plt2.plot(Tsample_arr, 'g-', label='Tsample') 
    plt2.set_ylabel('Tsmp deg C')                    
    plt2.ticklabel_format(useOffset=False)           
    plt2.legend(loc='upper right')                                                  
    
#===============================================================================
# display block and sample tempraure
#===============================================================================
def disp_blk_smp(blk, smp):
    global graph_points
    Tblock_arr.append(blk)
    Tsample_arr.append(smp)
    drawnow(plot_blk_smp)
    plt.pause(.000001)
    graph_points += 1
    if(graph_points > 500): #If you have 50 or more points, delete the first one from the array
        Tblock_arr.pop(0)   #This allows us to just see the last 50 data points
        Tsample_arr.pop(0)
#     print "********<%3.2f, %3.2f>*******" % (blk, smp)

#===============================================================================
# 
#===============================================================================
# Calculate sample temperature...                                 
# Sample T[new] = Sample T + (Block T - Sample T) * SamplePeriod) 
#                            ----------------------------------
#                                (Tube Time Constant - Sensor Lag)
#---------------------------------------------------------------
def rcFilter(Tin, Tout, samplePeriod, timeConstant):
    return (Tout + (Tin - Tout) * samplePeriod / timeConstant)
#===============================================================================
def load_cntrl_k(prntflag):
    global step0_Kp_ramp,step0_Kp_ss,step0_Kp_ss_hold,\
           step0_Ti_ramp,step0_Ti_ss,step0_Kd_ramp,step0_Kd_ss,\
           step0_U_ss, step0_st1st2trans_blk, step0_st2st3trans_smp,\
           step1_Kp_ramp,step1_Kp_ss,step1_Kp_ss_hold,\
           step1_Ti_ramp,step1_Ti_ss,step1_Kd_ramp,step1_Kd_ss,\
           step1_U_ss, step1_st1st2trans_blk, step1_st2st3trans_smp,\
           step2_Kp_ramp,step2_Kp_ss,step2_Kp_ss_hold,\
           step2_Ti_ramp,step2_Ti_ss,step2_Kd_ramp,step2_Kd_ss,\
           step2_U_ss, step2_st1st2trans_blk, step2_st2st3trans_smp,\
           step3_Kp_ramp,step3_Kp_ss,step3_Kp_ss_hold,\
           step3_Ti_ramp,step3_Ti_ss,step3_Kd_ramp,step3_Kd_ss,\
           step3_U_ss, step3_st1st2trans_blk, step3_st2st3trans_smp,\
           step4_Kp_ramp,step4_Kp_ss,step4_Kp_ss_hold,\
           step4_Ti_ramp,step4_Ti_ss,step4_Kd_ramp,step4_Kd_ss,\
           step4_U_ss, step4_st1st2trans_blk, step4_st2st3trans_smp
                      
    fname_h = open('../config/PID_gains.txt', 'r+')
    for line in fname_h.readlines():
        gains = line.split(',')
        if gains[0] == 'step0':
            step0_Kp_ramp    = float(gains[1]) 
            step0_Kp_ss      = float (gains[2])
            step0_Kp_ss_hold = float (gains[3])
            step0_Ti_ramp    = float (gains[4])
            step0_Ti_ss      = float (gains[5])
            step0_Kd_ramp    = float (gains[6]) 
            step0_Kd_ss      = float (gains[7])
            step0_U_ss       = float (gains[8])
            step0_st1st2trans_blk = float (gains[9])
            step0_st2st3trans_smp = float (gains[10])
        
        
        if gains[0] == 'step1':
            step1_Kp_ramp    = float(gains[1]) 
            step1_Kp_ss      = float (gains[2])
            step1_Kp_ss_hold = float (gains[3])
            step1_Ti_ramp    = float (gains[4])
            step1_Ti_ss      = float (gains[5])
            step1_Kd_ramp    = float (gains[6]) 
            step1_Kd_ss      = float (gains[7])
            step1_U_ss       = float (gains[8])
            step1_st1st2trans_blk = float (gains[9])
            step1_st2st3trans_smp = float (gains[10])
 
        elif gains[0] == 'step2':
            step2_Kp_ramp    = float (gains[1]) 
            step2_Kp_ss      = float (gains[2])
            step2_Kp_ss_hold = float (gains[3])
            step2_Ti_ramp    = float (gains[4]) 
            step2_Ti_ss      = float (gains[5])
            step2_Kd_ramp    = float (gains[6]) 
            step2_Kd_ss      = float (gains[7])
            step2_U_ss       = float (gains[8])
            step2_st1st2trans_blk = float (gains[9])
            step2_st2st3trans_smp = float (gains[10])
            
        elif gains[0] == 'step3':
            step3_Kp_ramp    = float (gains[1]) 
            step3_Kp_ss      = float (gains[2])
            step3_Kp_ss_hold = float (gains[3])
            step3_Ti_ramp    = float (gains[4]) 
            step3_Ti_ss      = float (gains[5])
            step3_Kd_ramp    = float (gains[6]) 
            step3_Kd_ss      = float (gains[7])
            step3_U_ss       = float (gains[8])
            step3_st1st2trans_blk = float (gains[9])
            step3_st2st3trans_smp = float (gains[10])

        elif gains[0] == 'step4':
            step4_Kp_ramp    = float (gains[1]) 
            step4_Kp_ss      = float (gains[2])
            step4_Kp_ss_hold = float (gains[3])
            step4_Ti_ramp    = float (gains[4]) 
            step4_Ti_ss      = float (gains[5])
            step4_Kd_ramp    = float (gains[6]) 
            step4_Kd_ss      = float (gains[7])
            step4_U_ss       = float (gains[8])
            step4_st1st2trans_blk = float (gains[9])
            step4_st2st3trans_smp = float (gains[10])  
                     
            if prntflag:
                print "%3.2f %3.2f %3.2f %3.2f %3.2f %3.2f %3.2f" %\
                       (step3_Kp_ramp, step3_Kp_ss, step3_Kp_ss_hold,\
                       step3_Ti_ramp, step3_Ti_ss,\
                       step3_Kd_ramp, step3_Kd_ss)
    fname_h.close()
#    add range checking on gains here
#         else:
#             msg = "PID_gain file corrupted!"
#             log_dbg(msg)
#             if prntflg:
#                 print msg
 
#===============================================================================
# Open tec parameter file 
# Read onvershoot, undershoot and hold times for 3 step PCR and sample time const
#===============================================================================
def read_cofig_file():
    global gStpoint_step0,gOvershoot_step0,gOvershoot_hold_time_step0,gHold_time_step0,\
           gStpoint_step1,gOvershoot_step1,gOvershoot_hold_time_step1,gHold_time_step1,\
           gStpoint_step2,gUndershoot_step2,gUndershoot_hold_time_step2,gHold_time_step2,\
           gStpoint_step3,gOvershoot_step3,gOvershoot_hold_time_step3,gHold_time_step3,\
           gStpoint_step4,gOvershoot_step4,gOvershoot_hold_time_step4,gHold_time_step4,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant
   
    Tec_config_h   = open('../config/TEC_config.txt', 'r+')
    
    for line in Tec_config_h.readlines():
        param_list = line.split(',')
        if param_list[0] == 'step0':
            gStpoint_step0              = float (param_list[1])
            gOvershoot_step0            = float (param_list[2])
            gOvershoot_hold_time_step0  = float (param_list[3])
            gHold_time_step0            = float (param_list[4])    
        if param_list[0] == 'step1':
            gStpoint_step1              = float (param_list[1])
            gOvershoot_step1            = float (param_list[2])
            gOvershoot_hold_time_step1  = float (param_list[3])
            gHold_time_step1            = float (param_list[4])
        elif param_list[0] == 'step2':
            gStpoint_step2              = float (param_list[1])
            gUndershoot_step2           = float (param_list[2]) 
            gUndershoot_hold_time_step2 = float (param_list[3])
            gHold_time_step2            = float (param_list[4]) 
        elif param_list[0] == 'step3':
            gStpoint_step3              = float (param_list[1])
            gOvershoot_step3            = float (param_list[2]) 
            gOvershoot_hold_time_step3  = float (param_list[3])
            gHold_time_step3            = float (param_list[4]) 
        elif param_list[0] == 'step4':
            gStpoint_step4              = float (param_list[1])
            gOvershoot_step4            = float (param_list[2]) 
            gOvershoot_hold_time_step4  = float (param_list[3])
            gHold_time_step4            = float (param_list[4])  
        elif param_list[0] == 'Coefficients':
            gCoef0 = float (param_list[1])
            gCoef1 = float (param_list[2])
            gCoef1 = float (param_list[3])
        elif param_list[0] == 'Sample_time_constant':
            Sample_time_constant = float (param_list[1])
         
    # gOvershoot range must be 0-6, no reason overhsoot to be > 6
    if gOvershoot_step1 < 0 or gOvershoot_step1 > 6:  # set initial Overshoot to -1
        msg = "parmeter file corropted!"
        log_dbg(msg)
        if prntflg:
            print msg

    Tec_config_h.close() 
           
    
# ***************************************************************************************    
#     log dbg data 
# ****************************************************
# Log dbg info
# ****************************************************
def log_dbg(msg):   
    global gdbg_file_h
    
    gdbg_file_h.write (msg)
    if LOG == True:
        gdbg_file_h.write ('\n')
        gdbg_file_h.flush()
    if prntflg == 1:
        print (msg)

# ****************************************************
# Log dbg info
# ****************************************************
def log_tmpr(msg):   
    global gtmpr_logfile_h
    
    gtmpr_logfile_h.write (msg)
    if LOG == True:
        gtmpr_logfile_h.write ('\n')
    if prntflg == 1:
        print (msg)

# ****************************************************
# Log dbg info
# ****************************************************
def log_param(msg):   # obsolete, not used any more
    global gTec_config_h
    
    gTec_config_h.write (msg)
    if LOG == True:
        gdbg_file_h.write ('\n')
    if prntflg == 1:
        print (msg)
        
# ****************************************************
def close_log_tmpr_file():
    global gtmpr_logfile_h
    gtmpr_logfile_h.close()
# ****************************************************
def close_log_dbg():
    global gdbg_file_h
    gdbg_file_h.close()
    # ****************************************************
def close_config_file():
    global gTec_config_h
    gTec_config_h.close()
# ****************************************************
def close_all():
    close_log_tmpr_file()
    close_log_dbg()

# ==================================================================
def twoscomp(number, nBits):
    return (-number) & (2**nBits - 1)

# ==================================================================
def open_serial_port ():
    global gSerial_port
    
    gSerial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  
    print gSerial_port  

# ==================================================================
def hexc2dec(bufp):
    newval=0
    divvy=4096
    for pn in range (1,5):
        vally=ord(bufp[pn])
        if(vally < 97):
            subby=48
        else:
            subby=87
        newval+=((ord(bufp[pn])-subby)*divvy)
        divvy/=16
        if(newval > 32767):
            newval=newval-65536
    return newval


# ==================================================================
# input: decimal value for PWM
# 1. convert to hex
# 2. insert to output buf
# 3. if negative value, convert to two's complement and do steps 1-2
# command format:
# byte[1]-byte[2]: command 2 bytes
# byte[3]-byte[6]: outpute value, 4 bytes
# byte[7]-byte[8]: checksum of bytes 1-6, command + data
# 
# bst  = ['*','1','0','0','0','c','8','5','c','\r']  # 200
# bst  = ['*','1','0','f','f','3','8','9','8','\r'] # -200  78.4%
# ==================================================================
def write_control_output(cmd, cntl):
    global gSerial_port, gTmpr, manual_output_enble
    buf=[0,0,0,0,0,0,0,0,0,0,0,0,0]  # read buffer
    
    checksum_str = '*100000'
    # initial command to set up the board for manual contrl
    if cmd == 1 and manual_output_enble == 0:
        #if not manual_output_enble:
        # configure for manual output command run one time if necessary
        bst = ['*','2','d','0','0','0','3','5','9','\r']  # manual config 
        manual_output_enble = 1 
        print ("TEC config for manual output...")
   
    # write output command
    else:
        bst = ['*','1','0','0','0','0','0','0','0','\r']
        # convert control out put 
        if cntl < 0 :
            neg_output = twoscomp (abs(cntl), 8)
            # sign extend MSB
            bst[3] = 'f'
            bst[4] = 'f'
            cntl_value = hex(neg_output)
        else:
            cntl_value = hex(cntl)  # sign extend for pos number
            bst[3] = '0'  # don't need it - bst is already set to 00
            bst[4] = '0'
        
        # output value 4 bytes, only write LSB 2 bytes
        # max output is 255 or FF
        # if values are 0 or less than 15 (0xf or less) need to pad the string   
        #bst[5] = cntl_value[2] # ?
        if cntl_value == '0x0':  # 0x0 index[3] is out of bond, force a '0'
            cntl_value += '0'
        elif len(cntl_value) < 4:  # values less than 0xf
            cntl_value2 = cntl_value
            cntl_value = cntl_value2[:2] + '0' + cntl_value2[2:]
            bst[5] = cntl_value[2]
            bst[6] = cntl_value[3]
        else:
            bst[5] = cntl_value[2]
            bst[6] = cntl_value[3]
        
        # add checksum, find checksum for checksum_str
        checksum_str = '*10' + bst[3] +bst[4] + cntl_value[2] + cntl_value[3] 
        cs = get_checksum (checksum_str)  # 5C, 200
        # add checksum to the buffer
        bst[7] = cs[0]
        bst[8] = cs[1] 
          
    for pn in range(0,10):
        gSerial_port.write((bst[pn])) 
        
    for pn in range(0,8):
        buf[pn] = gSerial_port.read(1)
        
    tmpr = hexc2dec(buf)
    return tmpr/10.0 
    
# ==================================================================
# Set TEC output to 0, this will set PWM to 0 duty cyle
# ==================================================================
def turn_off_tec():
    write_control_output (CMD_TYPE_OUTPUT, 0)

# ==================================================================
# Check output power level 
# ==================================================================
def check_output_power_levl():
    bst=['*','0','3','0','0','0','0','2','3','\r']
    buf=[0,0,0,0,0,0,0,0,0,0,0,0,0]
 
#     print "Check output power level...."
    for pn in range(0,10):
        gSerial_port.write((bst[pn]))
    for pn in range(0,8):
        buf[pn]=gSerial_port.read(1)
        #print(buf[pn])
        
    return hexc2dec(buf)

# ==================================================================
# TEC board has to be in manual config before calling this function
# ==================================================================
def read_cur_temp():
    global gSerial_port
    
    bst=['*','0','1','0','0','0','0','2','1','\r']
    buf = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    
#     for pn in range(0,8):
#         buf[pn]=gSerial_port.write()
    for pn in range(0,10):
        gSerial_port.write((bst[pn]))
        
    for pn in range(0,8):
        buf[pn]=gSerial_port.read(1)
        
    temp1=hexc2dec(buf)
    return temp1/10.0


# ==================================================================
# Activation Step 
# Will go to denaturation temperature and hold the temperature
# input: none, this is a fixed step and only performs the DNA melt
# will change this to accept Ks, set-point and hold time
# Returns once the hold time is expired but will not chage the
# TEC out put. The following step will control to next temperature
# ==================================================================
def step0 ():
    global gTmpr, gTsample,\
           step0_Kp_ramp, step0_Kp_ss,step0_Kp_ss_hold,\
           step0_Ti_ramp,step0_Ti_ss,step0_Kd_ramp,step0_Kd_ss,\
           gStpoint_step0,gOvershoot_step0,gOvershoot_hold_time_step0,gHold_time_step0,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant
    global mapfile,current_cycle
    
    # any updates for the control loop should be in this block
    # update gains
    Kp_ramp    = step0_Kp_ramp
    Kp_ss      = step0_Kp_ss
    Kp_ss_hold = step0_Kp_ss_hold
    Ti_ramp    = step0_Ti_ramp
    Ti_ss      = step0_Ti_ss
    Kd_ramp    = step0_Kd_ramp
    Kd_ss      = step0_Kd_ss
   
    U_ss = step0_U_ss
    st1st2trans_blk = step0_st1st2trans_blk
    st2st3trans_smp = step0_st2st3trans_smp
    
    setpoint   = gStpoint_step0
    overshoot  = gOvershoot_step0
    denature_setpoint   = gStpoint_step0 #80
    overshoot_hold_time = gOvershoot_hold_time_step0
    hold_time  = gHold_time_step0

#     Kd = 0.0
    U  = 0
#     Ts = 0.5 # loop sample time in seconds, reset time
    Ts = 0.25
    setpoint = gStpoint_step0 #80 
    denature_setpoint = gStpoint_step0 #80
    ss_clock  = 0
    Ui_k_1 = 0
    max_saturation = 70
    upper_saturation = 30
    lower_saturation = -30
    runaway_tmpr  = setpoint + 10
    
    Ui_k   = 0.0
    Ui_k_1 = 0.0       # use for feed-forward
    Ud     = 0.0
    e_k = e_k_1 = 0.0
    ma_e   = 0.0         # moving average of error signal
    ma_buf = [0,0,0,0] # 4 tap FIR
    ma_ctr = 0         # index in the circular buffer 
    
    PB = 100
    ss_flag = 0
    in_steadystate = 0
    
    start_integration_tmpr = st1st2trans_blk #5  # integrate once with in 5C of the setpoint
    ss_clock = 0
    int_flag = 0
    stage_1 = 1
    stage_2 = 2
    stage_3 = 3      # state ramp dn to denature setpoint
    state =  stage_1 # ramping 
    
    Kp = Kp_ramp
    Ti = Ti_ramp 
    Kd = Kd_ramp  
    tmpr = read_cur_temp()
    sp = setpoint + overshoot
        
    while (1):
              
        if tmpr >= runaway_tmpr:
           turn_off_tec()
           tmp_runaway_flag = 1
           print ">>>>>>>>>> TEC thremal runaway >>>>>> **"
           return
       
        tmpr = Tblock = read_cur_temp()
#         tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)
        gTsample = rcFilter(Tblock, gTsample, 0.5, Sample_time_constant)
        disp_blk_smp(Tblock, gTsample)
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, gTsample) 
        log_tmpr (tmpr_msg)
        
        e_k_1 = e_k      
        e = e_k = sp - tmpr

        ma_ctr += 1   # buffer index
        if ma_ctr > 3: ma_ctr = 0
        ma_buf[ma_ctr] = e_k        
        ma_e = (ma_buf[0]+ma_buf[1]+ma_buf[2]+ma_buf[3])/4.0
        if abs(ma_e) <= 0.5: ss_flag = 1 

        Up = Kp * e  # for debug
        Ui_k = (Ui_k_1 + (1/Ti_ramp * Ts*e))  # first stage integration

        if e <= start_integration_tmpr and state == stage_1: # change to state_2
            state =  stage_2
            Kp = Kp_ss
            Ti = Ti_ss
            Kd = Kd_ss
#             if abs(Ui_k) > max_saturation:
#                 if Ui_k >= upper_saturation:  Ui_k = upper_saturation
#                 if Ui_k <= lower_saturation: Ui_k = lower_saturation 
            Ui_k = U_ss #60 # holding output = 48
            print "***********  reset ************"
        if abs(Ui_k) > 100:
            Ui_k = 100
 
        Ud = Kd * (e - e_k_1)/Ts  # Ud = 1/Td * (e - e_k_1)/Ts

        e_k_1 = e
        Ui_k_1 = Ui_k
    
        if state == stage_2: Kp = Kp_ss  # U = Kp * (e + Ui_k + Ud)
        else:                Kp = Kp_ramp

        U = Kp*e + Ui_k + Ud    #  U = Kp*e + Kp*Ui_k + Kp*Ud
        if U > 100:  
            U = 100
        tec_output = (int)((U/PB) * 255)
        
        tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)
        
        dbg_msg = "STP0<st%2d><sp%5.2f><BlkT %5.2f><SmpT %5.2f><Err %5.2f> <U %5.2f>   <Up %5.2f> <Ui_k %5.2f>  <Ud %5.2f>  <tec_out %4d> \
        <Kp =%5.2f><Ti =%5.2f><Kd =%5.2f>"  % (state, sp, Tblock, gTsample, e,    U,    Up,  Ui_k, Ud, tec_output, Kp, Ti, Kd)
        log_dbg(dbg_msg)
        #print dbg_msg

        #Write to shared memory
        sm = "%5.6f  %5.6f %-04d %-04d\n" % (Tblock, gTsample, current_cycle, 0)
        write_to_shared_memory(mapfile, sm)


        if (ss_flag):  # Start hold time clock
            if abs(ma_e) < 0.5:
                ss_clock += Ts # increment by Ts seconds
            else: 
                ss_clock = 0   # start a new counter 
        print ss_clock 
        print overshoot_hold_time   
        
#         if state == stage_2 and ss_clock >= overshoot_hold_time:
# #         if (state == stage_2 and ss_clock >= overshoot_hold_time) or (gTsample > denature_setpoint - 0.5):
# #         print " smp  den", gTsample, denature_setpoint
# #         if (gTsample > denature_setpoint - 0.5):
# #             print " in the loop smp  den", gTsample, denature_setpoint
#             ss_flag = 1
#             setpoint = denature_setpoint  # ramp dn to new setpoint
#             state = stage_3
#             Kp = Kp_ss_hold
#             ss_clock = 0   # reset ss clock for stage_3 
#             sp = setpoint  # denature setpoint            
# #             Ui_k = 70 # pre-load Ui for stage_3 

        if state == stage_2: 
            print "step1 abs ", abs(gTsample-denature_setpoint)
            if ss_clock >= overshoot_hold_time or abs(gTsample-denature_setpoint) <= 1.0:
                ss_flag = 1
                setpoint = denature_setpoint  # ramp dn to new setpoint
                state = stage_3
                Kp = Kp_ss_hold
                ss_clock = 0   # reset ss clock for stage_3 
                sp = setpoint  # denature setpoint            
#               Ui_k = 70 # pre-load Ui for stage_3 
        else: 
            if ss_clock >= hold_time and state == stage_3:
                print "ss_clock = ", ss_clock
                return 

        time.sleep(Ts) # loop delay, this is fastest possible without serial overrun
        # if error stays with in 0.5C of the setpoint for 10*Ts start hold timer


#   step1   *************************************************************
def Step1 ():
    global gTmpr, gTsample,\
           step1_Kp_ramp,step1_Kp_ss,step1_Kp_ss_hold,\
           step1_Ti_ramp,step1_Ti_ss,step1_Kd_ramp,step1_Kd_ss,\
           gStpoint_step1,gOvershoot_step1,gOvershoot_hold_time_step1,gHold_time_step1,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant 
    global mapfile,current_cycle

    # any updates for the control loop should be in this block
    # update gains
    Kp_ramp    = step1_Kp_ramp
    Kp_ss      = step1_Kp_ss
    Kp_ss_hold = step1_Kp_ss_hold
    Ti_ramp    = step1_Ti_ramp
    Ti_ss      = step1_Ti_ss
    Kd_ramp    = step1_Kd_ramp
    Kd_ss      = step1_Kd_ss
   
    U_ss = step1_U_ss
    st1st2trans_blk = step1_st1st2trans_blk
    st2st3trans_smp = step1_st2st3trans_smp
    
    setpoint   = gStpoint_step1
    overshoot  = gOvershoot_step1
    denature_setpoint   = gStpoint_step1 #80
    overshoot_hold_time = gOvershoot_hold_time_step1
    hold_time  = gHold_time_step1

#     Kd = 0.0
    U  = 0
    Ts = 0.5 # loop sample time in seconds, reset time
    setpoint = gStpoint_step1 #80 
    denature_setpoint = gStpoint_step1 #80
    ss_clock  = 0
    Ui_k_1 = 0
    max_saturation = 70
    upper_saturation = 30
    lower_saturation = -30
    runaway_tmpr  = setpoint + 10
    
    Ui_k   = 0.0
    Ui_k_1 = 0.0       # use for feed-forward
    Ud     = 0.0
    e_k = e_k_1 = 0.0
    ma_e   = 0.0         # moving average of error signal
    ma_buf = [0,0,0,0] # 4 tap FIR
    ma_ctr = 0         # index in the circular buffer 
    
    PB = 100
    ss_flag = 0
    in_steadystate = 0
    
    start_integration_tmpr = st1st2trans_blk #5  # integrate once with in 5C of the setpoint
    ss_clock = 0
    int_flag = 0
    stage_1 = 1
    stage_2 = 2
    stage_3 = 3      # state ramp dn to denature setpoint
    state =  stage_1 # ramping 
    
    Kp = Kp_ramp
    Ti = Ti_ramp 
    Kd = Kd_ramp  
    tmpr = read_cur_temp()
    sp = setpoint + overshoot
        
    while (1):
              
        if tmpr >= runaway_tmpr:
           turn_off_tec()
           tmp_runaway_flag = 1
           print ">>>>>>>>>> TEC thremal runaway >>>>>> **"
           return
       
        tmpr = Tblock = read_cur_temp()
        gTsample = rcFilter(Tblock, gTsample, 0.5, Sample_time_constant)
        disp_blk_smp(Tblock, gTsample)
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, gTsample) 
        log_tmpr (tmpr_msg)
                
        e_k_1 = e_k      
        e = e_k = sp - tmpr

        ma_ctr += 1   # buffer index
        if ma_ctr > 3: ma_ctr = 0
        ma_buf[ma_ctr] = e_k        
        ma_e = (ma_buf[0]+ma_buf[1]+ma_buf[2]+ma_buf[3])/4.0
        if abs(ma_e) <= 0.5: ss_flag = 1 

        Up = Kp * e  # for debug
        Ui_k = (Ui_k_1 + (1/Ti_ramp * Ts*e))  # first stage integration

        if e <= start_integration_tmpr and state == stage_1: # change to state_2
            state =  stage_2
            Kp = Kp_ss
            Ti = Ti_ss
            Kd = Kd_ss
#             if abs(Ui_k) > max_saturation:
#                 if Ui_k >= upper_saturation:  Ui_k = upper_saturation
#                 if Ui_k <= lower_saturation: Ui_k = lower_saturation 
            Ui_k = U_ss #60 # holding output = 48
            print "***********  reset ************"
        if abs(Ui_k) > 100:
            Ui_k = 100
 
        Ud = Kd * (e - e_k_1)/Ts  # Ud = 1/Td * (e - e_k_1)/Ts

        e_k_1 = e
        Ui_k_1 = Ui_k
    
        if state == stage_2: Kp = Kp_ss  # U = Kp * (e + Ui_k + Ud)
        else:                Kp = Kp_ramp

        U = Kp*e + Ui_k + Ud    #  U = Kp*e + Kp*Ui_k + Kp*Ud
        if U > 100:  
            U = 100
        tec_output = (int)((U/PB) * 255)
        
#         tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)
        tmpr = write_control_output (CMD_TYPE_OUTPUT, tec_output)
        
        dbg_msg = "STP1<st%2d><sp%5.2f><BlkT %5.2f><SmpT %5.2f><Err %5.2f> <U %5.2f>   <Up %5.2f> <Ui_k %5.2f>  <Ud %5.2f>  <tec_out %4d> \
        <Kp =%5.2f><Ti =%5.2f><Kd =%5.2f>"  % (state, sp, Tblock, gTsample, e,    U,    Up,  Ui_k, Ud, tec_output, Kp, Ti, Kd)
        log_dbg(dbg_msg)

        #Write to shared memory
        sm = "%5.6f  %5.6f %-04d %-04d\n" % (Tblock, gTsample, current_cycle, 1)
        write_to_shared_memory(mapfile, sm)


        if (ss_flag):  # Start hold time clock
            if abs(ma_e) < 0.5:
                ss_clock += Ts # increment by Ts seconds
            else: 
                ss_clock = 0   # start a new counter 
            
#         if state == stage_2 and ss_clock >= overshoot_hold_time:
#             ss_flag = 1
#             setpoint = denature_setpoint  # ramp dn to new setpoint
#             state = stage_3
#             Kp = Kp_ss_hold
#             ss_clock = 0   # reset ss clock for stage_3 
#             sp = setpoint  # denature setpoint 
        if state == stage_2: 
            print "step1 abs ", abs(gTsample-denature_setpoint)
            if ss_clock >= overshoot_hold_time or abs(gTsample-denature_setpoint) <= 1.0:
                ss_flag = 1
                setpoint = denature_setpoint  # ramp dn to new setpoint
                state = stage_3
                Kp = Kp_ss_hold
                ss_clock = 0   # reset ss clock for stage_3 
                sp = setpoint  # denature setpoint            
#               Ui_k = 70 # pre-load Ui for stage_3 
        else: 
            if ss_clock >= hold_time and state == stage_3:
                print "ss_clock = ", ss_clock
                return 

        time.sleep(Ts) # loop delay, this is fastest possible without serial overrun
        # if error stays with in 0.5C of the setpoint for 10*Ts start hold timer


# ==================================================================
# Will go to annealing temperature and hold the temperature
# input: none, this is a fixed step and only performs the DNA melt
# This function may change to accept Ks and hold time
# 
# Returns once the hold time is expired but will not change the
# TEC out put. The following step will control to next temperature

# ==================================================================
def Step2():
# ==================================================================
    global gTmpr, gTsample,\
           step2_Kp_ramp,step2_Kp_ss,step2_Kp_ss_hold,\
           step2_Ti_ramp,step2_Ti_ss,step2_Kd_ramp,step2_Kd_ss,\
           gStpoint_step2,gUndershoot_step2,gUndershoot_hold_time_step2,gHold_time_step2,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant
    global mapfile, current_cycle

    Kp_ramp    = step2_Kp_ramp
    Kp_ss      = step2_Kp_ss
    Kp_ss_hold = step2_Kp_ss_hold
    Ti_ramp    = step2_Ti_ramp
    Ti_ss      = step2_Ti_ss
    Kd_ramp    = step2_Kd_ramp
    Kd_ss      = step2_Kd_ss    
    
    U_ss = step2_U_ss
    st1st2trans_blk = step2_st1st2trans_blk
    st2st3trans_smp = step2_st2st3trans_smp
    
    setpoint   = gStpoint_step2
    undershoot  = gUndershoot_step2
    extension_setpoint   = gStpoint_step2 #80
    undershoot_hold_time = gUndershoot_hold_time_step2
    hold_time  = gHold_time_step2 
            
#    Kd = 0.0
    U  = 0
    Ts = 0.5 # loop sample time in seconds, reset time
    setpoint = gStpoint_step2
    anealing_setpoint = gStpoint_step2   
    ss_clock  = 0
    Ui_k_1 = 0
    max_saturation = 40 #70
    upper_saturation = 30
    lower_saturation = -30
    runaway_tmpr  = setpoint - 10
 
    Ui_k   = 0
    Ui_k_1 = 0.0  # use for feed forward
    Ud     = 0.0
    e_k = e_k_1 = 0.0
    ma_e = 0      # moving average of error signal
    ma_buf = [0,0,0,0]  # 4 tap FIR
    ma_ctr = 0    # index in the circular buffer 
    
    PB = 100
    ss_flag = 0
    in_steadystate = 0
    
    start_integration_tmpr = st1st2trans_blk #2.0 # 2.0 # 3.0 #5  
    ss_clock = 0
    int_flag = 0
    stage_1  = 1
    stage_2  = 2  # int starts 
    stage_3  = 3  # state ramp dn to denature setpoint
    state =  stage_1 # ramping 
    
    Kp = Kp_ramp
    Ti = Ti_ramp
    Kd = Kd_ramp  
    tmpr = read_cur_temp()
    sp = setpoint - undershoot
        
    while (1):
        if tmpr <= runaway_tmpr:
           turn_off_tec()
           tmp_runaway_flag = 1
           print ">>>>>>>>>> TEC thremal runaway >>>>>> **"
           return -1

        tmpr = Tblock = read_cur_temp()
        gTsample = rcFilter(Tblock, gTsample, 0.5, Sample_time_constant)
        disp_blk_smp(Tblock, gTsample) 
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, gTsample) 
        log_tmpr (tmpr_msg)
        
        e_k_1 = e_k      
        e = e_k = sp - tmpr
        
        ma_ctr += 1   # index in the circular buffer 
        if ma_ctr > 3: ma_ctr = 0
        ma_buf[ma_ctr] = e_k        
        ma_e = (ma_buf[0]+ma_buf[1]+ma_buf[2]+ma_buf[3])/4.0
        if abs(ma_e) <= 0.5: ss_flag = 1 
        
        Up = Kp_ramp * e  # debug
        Ui_k = (Ui_k_1 + (1/Ti * Ts*e))  

        if abs(e) <= start_integration_tmpr and state == stage_1: # change to state_2
            state =  stage_2
            Kp = Kp_ss
            Ti = Ti_ss
            Kd = Kd_ss
            Ui_k = U_ss # 10.0 #-20.0 #-40 # holding output = 48
            print "***********  reset ************ %3.2f " % Ui_k
        if abs(Ui_k) > 100:
            Ui_k = -100
 
        Ud = Kd * (e - e_k_1)/Ts  # Ud = 1/Td * (e - e_k_1)/Ts

        e_k_1 = e
        Ui_k_1 = Ui_k
    
        if state == stage_2: Kp = Kp_ss  # U = Kp * (e + Ui_k + Ud)
        else:                Kp = Kp_ss

        U = Kp*e + Ui_k + Ud    #  U = Kp*e + Kp*Ui_k + Kp*Ud
        if U < -100:  
            U = -100
        tec_output = (int)((U/PB) * 255)
        tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)

        dbg_msg = "STP2<st%2d><sp%5.2f><BlkT %5.2f><SmpT %5.2f><Err %5.2f> <U %5.2f>   <Up %5.2f> <Ui_k %5.2f>  <Ud %5.2f>  <tec_out %4d> \
        <Kp =%5.2f><Ti =%5.2f><Kd =%5.2f>"  % (state, sp, Tblock, gTsample, e,    U,    Up,  Ui_k, Ud, tec_output, Kp, Ti, Kd)
        log_dbg(dbg_msg)

        #Write to shared memory
        sm = "%5.6f  %5.6f %-04d %-04d\n" % (Tblock, gTsample, current_cycle, 2)
        write_to_shared_memory(mapfile, sm)

                       
        if (ss_flag):  # Start hold time clock
            if abs(ma_e) < 0.5:
                ss_clock += Ts # increment by Ts seconds
            else: 
                ss_clock = 0   # start a new counter 
            
#         if state == stage_2 and ss_clock >= undershoot_hold_time:  # change to stage_3 ss
#             ss_flag = 1
#             setpoint = anealing_setpoint  # ramp dn to new setpoint
#             state = stage_3
#             Kp = Kp_ss_hold
#             ss_clock = 0 # reset ss clock for stage_3 
#             sp = setpoint  # denature setpoint 
#             
#             Ui_k = 50.0  # pre-load for steady state 
#                        #  make this a parameter for set to steady state holding output

        if state == stage_2: 
            print "step1 abs ", abs(gTsample-anealing_setpoint)
            if ss_clock >= undershoot_hold_time or abs(gTsample-anealing_setpoint) <= 1.0:
                ss_flag = 1
                setpoint = anealing_setpoint  # ramp dn to new setpoint
                state = stage_3
                Kp = Kp_ss_hold
                ss_clock = 0   # reset ss clock for stage_3 
                sp = setpoint  # denature setpoint            
#                 Ui_k = 50 # pre-load Ui for stage_3         
        
        
        else: 
            if ss_clock >= hold_time and state == stage_3:
                print "ss_clock = ", ss_clock
                return    

        time.sleep(Ts) # loop delay, this is fastest possible without serial overrun
        # if error stays with in 0.5C of the setpoint for 10*Ts start hold timer



# ==================================================================
# Step3 extension step
# Will go to denaturation temperature and hold the temperature
# input: none, this is a fixed step and only performs the DNA melt
# will change this to accept Ks, set-point and hold time
# Returns once the hold time is expired but will not chage the
# TEC out put. The following step will control to next temperature
# ==================================================================
def Step3():
    global gTmpr, gTsample,\
           step3_Kp_ramp,step3_Kp_ss,step3_Kp_ss_hold,\
           step3_Ti_ramp,step3_Ti_ss,step3_Kd_ramp,step3_Kd_ss,\
           gStpoint_step3,gOvershoot_step3,gOvershoot_hold_time_step3,gHold_time_step3,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant
    global mapfile,current_cycle

    Kp_ramp    = step3_Kp_ramp
    Kp_ss      = step3_Kp_ss
    Kp_ss_hold = step3_Kp_ss_hold
    Ti_ramp    = step3_Ti_ramp
    Ti_ss      = step3_Ti_ss
    Kd_ramp    = step3_Kd_ramp
    Kd_ss      = step3_Kd_ss

    U_ss = step3_U_ss
    st1st2trans_blk = step3_st1st2trans_blk
    st2st3trans_smp = step3_st2st3trans_smp
    
    overshoot  = gOvershoot_step3
    anealing_setpoint = gStpoint_step3 #80
    overshoot_hold_time = gOvershoot_hold_time_step3
    hold_time  = gHold_time_step3

    U  = 0
    Ts = 0.5 # loop sample time in seconds, reset time
    setpoint = gStpoint_step3
    extension_setpoint = gStpoint_step3
    ss_clock  = 0
    Ui_k_1 = 0
    max_saturation = 70
    upper_saturation = 30
    lower_saturation = -30
    runaway_tmpr  = setpoint + 10
    
    Ui_k = 0
    Ui_k_1 = 0.0  # use for feed forward
    Ud     = 0.0
    e_k = e_k_1 = 0.0
    ma_e = 0      # moving average of error signal
    ma_buf = [0,0,0,0]  # 4 tap FIR
    ma_ctr = 0    # index in the circular buffer 
    
    PB = 100
    ss_flag = 0
    in_steadystate = 0
    
    start_integration_tmpr = st1st2trans_blk # 4.0 #3.0 #5  # integrate once with in 5C of the setpoint
    ss_clock = 0
    int_flag = 0
    stage_1 = 1
    stage_2 = 2
    stage_3 = 3  # state ramp dn to extension setpoint
    state =  stage_1 # ramping 
    
    Kp = Kp_ramp
    Ti = Ti_ramp  
    Kd = Kd_ramp 
    tmpr = read_cur_temp()
    sp = setpoint + overshoot
        
    while (1):
        if tmpr >= runaway_tmpr:
           turn_off_tec()
           tmp_runaway_flag = 1
           print ">>>>>>>>>> TEC thremal runaway >>>>>> **", runaway_tmpr
           return -1

        tmpr = Tblock = read_cur_temp()
        gTsample = rcFilter(Tblock, gTsample, 0.5, Sample_time_constant)
        disp_blk_smp(Tblock, gTsample) 
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, gTsample) 
        log_tmpr (tmpr_msg)
                      
        e_k_1 = e_k      
        e = e_k = sp - tmpr
        
        ma_ctr += 1   # buffer index
        if ma_ctr > 3: ma_ctr = 0
        ma_buf[ma_ctr] = e_k        
        ma_e = (ma_buf[0]+ma_buf[1]+ma_buf[2]+ma_buf[3])/4.0
        if abs(ma_e) <= 0.5: ss_flag = 1 
        
        Up = Kp * e  # debug
        Ui_k = Ui_k_1 + (1/Ti * Ts*e)  # first stage integration

        if e <= start_integration_tmpr and state == stage_1: # change to state_2
            state =  stage_2
            Kp = Kp_ss
            Ti = Ti_ss
#             if abs(Ui_k) > max_saturation:
#                 if Ui_k >= upper_saturation:  Ui_k = upper_saturation
#                 if Ui_k<= lower_saturation: Ui_k = lower_saturation 
            Ui_k = U_ss # 45 # holding output = 80
            print "***********  reset ************"
 
            
        if abs(Ui_k) > 100:
            Ui_k = 100
 
        Ud = Kd * (e - e_k_1)/Ts  # Ud = 1/Td * (e - e_k_1)/Ts

        e_k_1 = e
        Ui_k_1 = Ui_k
    
        if state == stage_2: Kp = Kp_ss  # U = Kp * (e + Ui_k + Ud)
        else:                Kp = Kp_ramp

        U = Kp*e + Ui_k + Ud    #  U = Kp*e + Kp*Ui_k + Kp*Ud
        if U > 100:  
            U = 100
        tec_output = (int)((U/PB) * 255)
        
        tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)

        dbg_msg = "STP3<st%2d><sp%5.2f><BlkT %5.2f><SmpT %5.2f><Err %5.2f> <U %5.2f>   <Up %5.2f> <Ui_k %5.2f>  <Ud %5.2f>  <tec_out %4d> \
        <Kp =%5.2f><Ti =%5.2f><Kd =%5.2f>"  % (state, sp, Tblock, gTsample, e,    U,    Up,  Ui_k, Ud, tec_output, Kp, Ti, Kd)
        log_dbg(dbg_msg)

        #Write to shared memory
        sm = "%5.6f  %5.6f %-04d %-04d\n" % (Tblock, gTsample, current_cycle, 3)
        write_to_shared_memory(mapfile, sm)

        if (ss_flag):  # Start hold time clock
            if abs(ma_e) < 0.5:
                ss_clock += Ts # increment by Ts seconds
            else: 
                ss_clock = 0   # start a new counter 
            
#         if state == stage_2 and ss_clock >= overshoot_hold_time:
#             ss_flag = 1
#             setpoint = extension_setpoint  # ramp dn to new setpoint
#             state = stage_3
#             Kp = Kp_ss_hold
#             ss_clock = 0   # reset ss clock for stage_3 
#             sp = setpoint  # extension setpoint 
#             Ui_k = 80 # pre-load Ui for stage_3 
#             #print "<Kp = %5.2f> <Ti = %5.2f>" % (Kp, Ti)
            
        if state == stage_2: 
#             if ss_clock >= overshoot_hold_time or gTsample > extension_setpoint - 0.5:
            if ss_clock >= overshoot_hold_time or abs(gTsample-extension_setpoint) <= 0.5:
                ss_flag = 1
                setpoint = extension_setpoint  # ramp dn to new setpoint
                state = stage_3
                Kp = Kp_ss_hold
                ss_clock = 0   # reset ss clock for stage_3 
                sp = setpoint  # denature setpoint            
                Ui_k = 80 # pre-load Ui for stage_3
        else: 
            if ss_clock >= hold_time and state == stage_3:
                print "ss_clock = ", ss_clock
                return 

        time.sleep(Ts) # loop delay, this is fastest possible without serial overrun
        # if error stays with in 0.5C of the setpoint for 10*Ts start hold timer





# ==================================================================
# Step3 extension step-- last extension
# Will go to denaturation temperature and hold the temperature
# input: none, this is a fixed step and only performs the DNA melt
# will change this to accept Ks, set-point and hold time
# Returns once the hold time is expired but will not chage the
# TEC out put. The following step will control to next temperature
# ==================================================================
def step4():
    global gTmpr, gTsample,\
           step4_Kp_ramp,step4_Kp_ss,step4_Kp_ss_hold,\
           step4_Ti_ramp,step4_Ti_ss,step4_Kd_ramp,step4_Kd_ss,\
           gStpoint_step4,gOvershoot_step4,gOvershoot_hold_time_step4,gHold_time_step4,\
           gCoef0,gCoef1,gCoef1,Sample_time_constant
    global mapfile,current_cycle

    Kp_ramp    = step4_Kp_ramp
    Kp_ss      = step4_Kp_ss
    Kp_ss_hold = step4_Kp_ss_hold
    Ti_ramp    = step4_Ti_ramp
    Ti_ss      = step4_Ti_ss
    Kd_ramp    = step4_Kd_ramp
    Kd_ss      = step4_Kd_ss

    U_ss = step4_U_ss
    st1st2trans_blk = step4_st1st2trans_blk
    st2st3trans_smp = step4_st2st3trans_smp
    
    overshoot  = gOvershoot_step4
    anealing_setpoint = gStpoint_step4 #80
    overshoot_hold_time = gOvershoot_hold_time_step4
    hold_time  = gHold_time_step4

    U  = 0
    Ts = 0.5 # loop sample time in seconds, reset time
    setpoint = gStpoint_step4
    extension_setpoint = gStpoint_step4
    ss_clock  = 0
    Ui_k_1 = 0
    max_saturation = 70
    upper_saturation = 30
    lower_saturation = -30
    runaway_tmpr  = setpoint + 10
    
    Ui_k = 0
    Ui_k_1 = 0.0  # use for feed forward
    Ud     = 0.0
    e_k = e_k_1 = 0.0
    ma_e = 0      # moving average of error signal
    ma_buf = [0,0,0,0]  # 4 tap FIR
    ma_ctr = 0    # index in the circular buffer 
    
    PB = 100
    ss_flag = 0
    in_steadystate = 0
    
    start_integration_tmpr = st1st2trans_blk # 4.0 #3.0 #5  # integrate once with in 5C of the setpoint
    ss_clock = 0
    int_flag = 0
    stage_1 = 1
    stage_2 = 2
    stage_3 = 3  # state ramp dn to extension setpoint
    state =  stage_1 # ramping 
    
    Kp = Kp_ramp
    Ti = Ti_ramp  
    Kd = Kd_ramp 
    tmpr = read_cur_temp()
    sp = setpoint + overshoot
    dbg_msg = 'Starting step4 ....'  
    log_dbg(dbg_msg)

    print "step 4 start tmpr and overshoot setpoint", tmpr, overshoot, setpoint
    
    while (1):
        if tmpr >= runaway_tmpr:
           turn_off_tec()
           tmp_runaway_flag = 1
           print ">>>>>>>>>> TEC thremal runaway >>>>>> **", runaway_tmpr
           return -1

        tmpr = Tblock = read_cur_temp()
        gTsample = rcFilter(Tblock, gTsample, 0.5, Sample_time_constant)
        disp_blk_smp(Tblock, gTsample) 
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, gTsample) 
        log_tmpr (tmpr_msg)
              
        e_k_1 = e_k      
        e = e_k = sp - tmpr
        
        ma_ctr += 1   # buffer index
        if ma_ctr > 3: ma_ctr = 0
        ma_buf[ma_ctr] = e_k        
        ma_e = (ma_buf[0]+ma_buf[1]+ma_buf[2]+ma_buf[3])/4.0
        if abs(ma_e) <= 0.5: ss_flag = 1 
        
        Up = Kp * e  # debug
        Ui_k = Ui_k_1 + (1/Ti * Ts*e)  # first stage integration

        if e <= start_integration_tmpr and state == stage_1: # change to state_2
            state =  stage_2
            Kp = Kp_ss
            Ti = Ti_ss
#             if abs(Ui_k) > max_saturation:
#                 if Ui_k >= upper_saturation:  Ui_k = upper_saturation
#                 if Ui_k<= lower_saturation: Ui_k = lower_saturation 
            Ui_k = U_ss # 45 # holding output = 80
            print "***********  reset ************"
            
        if abs(Ui_k) > 100:
            Ui_k = 100
 
        Ud = Kd * (e - e_k_1)/Ts  # Ud = 1/Td * (e - e_k_1)/Ts

        e_k_1 = e
        Ui_k_1 = Ui_k
    
        if state == stage_2: Kp = Kp_ss  # U = Kp * (e + Ui_k + Ud)
        else:                Kp = Kp_ramp

        U = Kp*e + Ui_k + Ud    #  U = Kp*e + Kp*Ui_k + Kp*Ud
        if U > 100:  
            U = 100
        tec_output = (int)((U/PB) * 255)
        
        tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, tec_output)

        dbg_msg = "STP4<st%2d><sp%5.2f><BlkT %5.2f><SmpT %5.2f><Err %5.2f> <U %5.2f>   <Up %5.2f> <Ui_k %5.2f>  <Ud %5.2f>  <tec_out %4d> \
        <Kp =%5.2f><Ti =%5.2f><Kd =%5.2f>"  % (state, sp, Tblock, gTsample, e,    U,    Up,  Ui_k, Ud, tec_output, Kp, Ti, Kd)
        log_dbg(dbg_msg)

        # Write to shared memory
        sm = "%5.6f  %5.6f %-04d %-04d\n" % (Tblock, gTsample, current_cycle, 4)
        write_to_shared_memory(mapfile, sm)

        if (ss_flag):  # Start hold time clock
            if abs(ma_e) < 0.5:
                ss_clock += Ts # increment by Ts seconds
            else: 
                ss_clock = 0   # start a new counter 
            
#         if state == stage_2 and ss_clock >= overshoot_hold_time:
#             ss_flag = 1
#             setpoint = extension_setpoint  # ramp dn to new setpoint
#             state = stage_3
#             Kp = Kp_ss_hold
#             ss_clock = 0   # reset ss clock for stage_3 
#             sp = setpoint  # extension setpoint 
#             Ui_k = 80 # pre-load Ui for stage_3 
#             #print "<Kp = %5.2f> <Ti = %5.2f>" % (Kp, Ti)

        if state == stage_2: 
            if ss_clock >= overshoot_hold_time or abs(gTsample-extension_setpoint) <= 0.5:
                ss_flag = 1
                setpoint = extension_setpoint  # ramp dn to new setpoint
                state = stage_3
                Kp = Kp_ss_hold
                ss_clock = 0   # reset ss clock for stage_3 
                sp = setpoint  # denature setpoint            
                Ui_k = 80 # pre-load Ui for stage_3               
        else: 
            if ss_clock >= hold_time and state == stage_3:
                print "STEP4 *****   ss_clock  and hold_time = ", ss_clock, hold_time
                return 

        time.sleep(Ts) # loop delay, this is fastest possible without serial overrun
        # if error stays with in 0.5C of the setpoint for 10*Ts start hold timer


# ==============================================
# ==============================================
def main(*argv):
    global manual_output_enble
    global gdbg_file_h, gtmpr_logfile_h #, gTec_config_h, gPID_gains_h
    global gTmpr, gTsample
    global mapfile, shared_mem_lock
    global current_cycle


    if len(sys.argv) > 1:
        num_cycles = int (sys.argv[1])
    else: 
        num_cycles = default_num_cycles

    dbg_file_n = "TEC_logfile-" + time.strftime("%Y%m%d-%H%M%S") +'.txt'
    tmpr_log_n = "TEC_tmprlog-" + time.strftime("%Y%m%d-%H%M%S") +'.txt'    
    gdbg_file_h     = open ("../logs/tec_logs/" + dbg_file_n,'w')
    gtmpr_logfile_h = open ("../logs/tmpr_log/" + tmpr_log_n,'w')
    
    dbg_msg = " <TEC_cntrl version 26>"
    log_dbg(dbg_msg)
    dbg_msg = " ** Starting Luna logfile ** %s " % file
    log_dbg(dbg_msg)


    try:
        shared_mem_lock = process_lock.ProcessLock("/tmp/TECControllerSMLock.tmp")
        sharedmem = posix_ipc.SharedMemory("tecControllerSM", posix_ipc.O_CREAT|posix_ipc.O_TRUNC, size=128)

        # MMap the shared memory
        mapfile = mmap.mmap(sharedmem.fd, sharedmem.size)
        sharedmem.close_fd()  # Safe to close this.
    except Exception, e:
        log_dbg(e.message)



    #------------------------------------------------------------------------------
#     print " <TEC_cntrl version 26>"
    # open serial port
    open_serial_port()
    manual_output_enble = 1 # set to manual control
    # configure board for manual output
    # **** NOTE: don't send configuration command more than once *****
    ret = write_control_output (CMD_TYPE_CFG, 0) # second param is not used with CFG type
    
    gTmpr = Tblock = Tsample = read_cur_temp()
    tmpr_msg = "%3.2f, %3.2f" % (gTmpr, gTsample)
    log_tmpr (tmpr_msg)    
    # plot tmpr data 
    plt.ion()
    plt.grid()
#     major_ytick = numpy.arange(0, 110, 5)
#     minor_ytick = numpy.arange(0, 110, 2)
#     plt.set_yticks( major_ytick )
#     plt.set_yticks( minor_ytick, minor = True)
#     
    #turn off controller
    turn_off_tec()
    # set to idle tmpr
    tmpr = write_control_output (CMD_TYPE_OUTPUT, IDLE_TMPR) # change from IDLE to 2 cmd
            # load controller gains
    load_cntrl_k(1)
    read_cofig_file()
    
    # Activeation Step
    ret = step0()
    dbg_msg = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Step0 start ...'
    log_dbg(dbg_msg)

    # start cycles 
    for cycle in range (1, num_cycles):
        current_cycle = cycle
        tmpr = Tblock = write_control_output (CMD_TYPE_OUTPUT, IDLE_TMPR)
#         Tsample = rcFilter(Tblock, Tsample, Ts, Sample_time_constant)    
        Tsample = rcFilter(Tblock, Tsample, 0.5, Sample_time_constant)
#         print "---------------------->  %3.2f %3.2f" % (Tblock, Tsample)   
        tmpr_msg = "%3.2f, %3.2f" % (Tblock, Tsample)
        log_tmpr (tmpr_msg)

        print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Step1 start ...')
        ret = Step1()
        if ret == -1: 
            break
        print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Step2 start ...')
        ret = Step2()
        if ret == -1: 
            break
        print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Step3 start ...')
        ret = Step3()
        if ret == -1: 
            break
        read_cofig_file()
        load_cntrl_k(0) # no print
        
    ret = step4()

    tmpr = write_control_output (CMD_TYPE_OUTPUT, 30)  # idle tmpr
    
    dbg_msg = 'End .... '
    log_dbg(dbg_msg)
    print dbg_msg

    mapfile.close()
    posix_ipc.unlink_shared_memory("tecControllerSM")
    
    gSerial_port.close()
    close_log_tmpr_file()
    close_log_dbg()


def sigterm_handler(_signo, _stack_frame):
    do_exit()


def do_exit():
    global mapfile
    global shared_mem_sema

    mapfile.close()
    posix_ipc.unlink_shared_memory("tecControllerSM")
    shared_mem_sema.close()
    TECOff('/dev/ttyUSB0')

def TECOff(serialPortName):
    try:
        bst = ['*', '1', '0', '0', '0', '0', '0', '2', '1', '\r']  # 0 output
        buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        print ("Turn TEC off ....")
        ser = serial.Serial(serialPortName, 115200, timeout=1)
        for pn in range(0, 10):
            ser.write(bst[pn])
        for pn in range(0, 8):
            buf[pn] = ser.read(1)
            # print(buf[pn])
        ser.close()
        temp1 = hexc2dec(buf)
        print ("TEC Temp at TECOff: " + str(temp1 / 10.0))
        return True
    except Exception, e:
        print ("Failed to communicate with TEC.")
        return False




#===============================================================================
# main()
#===============================================================================
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)




    main()
