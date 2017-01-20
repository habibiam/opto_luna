import spidev
import time
import string
import site
import sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

#Initialize
if (sys.version_info < (2,7,0)):
    sys.stderr.write("You need at least python 2.7.0 to use the ISStreamer")
    exit(1)
    
GPIO.setmode(GPIO.BCM)
GPIObaseADDR=8
ppFRAME = 25
ppINT = 22
GPIO.setup(ppFRAME,GPIO.OUT)
GPIO.setup(ppINT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
spi = spidev.SpiDev()
spi.open(0,1)	
localPath=site.getsitepackages()[0]
helpPath=localPath+'/piplates/DAQChelp.txt'


MAXADDR=8
	
def CLOSE():
	spi.close()
	GPIO.cleanup()

def Help():
	help()

def HELP():
	help()	
	
def help():
    valid=True
    try:    
        f=open(helpPath,'r')
        while(valid):
            Count=0
            while (Count<20):
                s=f.readline()
                if (len(s)!=0):
                    print s[:len(s)-1]
                    Count = Count + 1
                    if (Count==20):
                        Input=raw_input('press \"Enter\" for more...')                        
                else:
                    Count=100
                    valid=False
        f.close()
    except IOError:
        print ("Can't open help file. Did you copy it to the same folder as DAQCplate.py?")

def version():
    print 'DAQCplate Python Module Version 1.01'

#===============================================================================#	
# ADC Functions	     	                                              			#
#===============================================================================#	
def getADC(addr,channel):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (channel>8):
		return "ERROR: channel argument out of range - must be less than 9"	
	resp=ppCMD(addr,0x30,channel,0,2)
	value=(256*resp[0]+resp[1])
	#print value
	value=round(value*4.096/1024,3)
	#print value
	if (channel==8):
		value=value*2.0
	return value

def getADCall(addr):
    value=range(8)
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1
    resp=ppCMD(addr,0x31,0,0,16)
    for i in range (0,8):
        value[i]=(256*resp[2*i]+resp[2*i+1])
        value[i]=round(value[i]*4.096/1024,3)
    return value    
    
#===============================================================================#	
# Digital Input Functions	                                                   	#
#===============================================================================#
def getDINbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"
	resp=ppCMD(addr,0x20,bit,0,1)
	if resp[0] > 0:
		return 1
	else:
		return 0
		
def getDINall(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x25,0,0,1)
	return resp[0]

def enableDINint(addr, bit, edge):	# enable DIN interrupt
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"	
	if ((edge=='f') or (edge=='F')):
		resp=ppCMD(addr,0x21,bit,0,0)		
	if ((edge=='r') or (edge=='R')):
		resp=ppCMD(addr,0x22,bit,0,0)
	if ((edge=='b') or (edge=='B')):
		resp=ppCMD(addr,0x23,bit,0,0)		
		
def disableDINint(addr,bit):	# disable DIN interrupt
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"
	resp=ppCMD(addr,0x24,bit,0,0)
	
def getTEMP(addr,channel,scale):
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1
    if (channel>7):
        return "ERROR: channel value out of range"
    scal=scale.lower()
    if ((scal!='c') and (scal!='f') and (scal!='k')):
        return "ERROR: incorrect scale parameter"
    resp=ppCMD(addr,0x70,channel,0,0)   #initiate measurement
    time.sleep(1)
    resp=ppCMD(addr,0x71,channel,0,2)   #get data
    Temp=resp[0]*256+resp[1]
    if (Temp>0x8000):
        Temp = Temp^0xFFFF
        Temp = -(Temp+1)
    Temp = round((Temp/16.0),4)
    if (scal=='k'):
        Temp = Temp + 273
    if (scal=='f'):
        Temp = round((Temp*1.8+32.2),4)
    return Temp
    
    
#===============================================================================#	
# Hybrid Functions	                                                   	#
#===============================================================================#    
def getRANGE(addr,channel,units):
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1
    if (channel>6):
        return "ERROR: channel value out of range"
    uni=units.lower()
    if ((uni!='c') and (uni!='i')):
        return "ERROR: incorrect units parameter"
    resp=ppCMD(addr,0x80,channel,0,0)   #initiate measurement
    time.sleep(.07)
    resp=ppCMD(addr,0x81,channel,0,2)   #get data
    Range=resp[0]*256+resp[1]
    if (Range==0):
        return "ERROR: sensor failure"
    if (uni=='c'):
        Range = Range/58.326
    if (uni=='i'):
        Range = Range/148.148
    Range=round(Range,2)
    return Range
    
#===============================================================================#	
# LED Functions	                                                   		   		#
#===============================================================================#			
def setLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x60,led,0,0)

def clrLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x61,led,0,0)

def toggleLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x62,led,0,0)	

def getLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x63,led,0,1)
	return resp[0]	


#==============================================================================#	
# Switch Functions	                                                   #
#==============================================================================#		
def getSWstate(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x50,0,0,1)
	return resp[0]

def enableSWint(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x51,0,0,0)

def disableSWint(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x52,0,0,0)		
	
def enableSWpower(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x53,0,0,0)

def disableSWpower(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x54,0,0,0)
		
		
#==============================================================================#	
# Digital Output Functions	                                                   #
#==============================================================================#	
def setDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x10,bit,0,0)

	
def clrDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x11,bit,0,0)		

def toggleDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x12,bit,0,0)		
	
def setDOUTall(addr,byte):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (byte>127):
		return "ERROR: byte argument out of range - must be less than 128"
	resp=ppCMD(addr,0x13,byte,0,0)			

def getDOUTbyte(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x14,0,0,1)
	return resp


#==============================================================================#	
# PWM and DAC Output Functions	                                                   #
#==============================================================================#	
def setPWM(addr,channel,value):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (value>1023):
		return "ERROR: PWM argument out of range - must be less than 1024"
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	hibyte = value>>8
	lobyte = value - (hibyte<<8)
	resp=ppCMD(addr,0x40+channel,hibyte,lobyte,0)

def getPWM(addr,channel):
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1
    if (channel>2):
        return "Error: PWM channel must be 0 or 1"
    ## Return PWM set value
    resp=ppCMD(addr,0x40+channel+2,0,0,2)
    value=(256*resp[0]+resp[1])
    return value	
	
def setDAC(addr,channel,value):
	global Vcc
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (value>4.097):
		return "ERROR: PWM argument out of range - must be less than 4.097 volts"
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	value = int(value/Vcc[addr]*1024)
	hibyte = value>>8
	lobyte = value - (hibyte<<8)
	resp=ppCMD(addr,0x40+channel,hibyte,lobyte,0)

	
def getDAC(addr,channel):
    global Vcc
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1
    if (channel>2):
        return "Error: PWM channel must be 0 or 1"
    ## Return DAC value
    resp=ppCMD(addr,0x40+channel+2,0,0,2)
    value=(256*resp[0]+resp[1])
    value=value*Vcc[addr]/1023
    return value

def calDAC(addr):
    global Vcc
    if (addr>MAXADDR):
        return "ERROR: address out of range - must be less than", MAXADDR-1    
    rtn = getADDR(addr)
    if ((rtn-8)==addr):
        Vcc[addr] = getADC(addr,8)
    else:
        Vcc[i]=10000        
        
#==============================================================================#	
# Interrupt Control Functions	                                               #
#==============================================================================#	
def intEnable(addr):	#DAQC will pull down on INT pin if an enabled event occurs
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x04,0,0,0)
	
def intDisable(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x05,0,0,0)
	
def getINTflags(addr):	#read INT flag registers in DAQC
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x06,0,0,2)
	value=(256*resp[0]+resp[1])
	return value
		
#==============================================================================#	
# System Functions	                                                   		   #
#==============================================================================#	
def getFWrev(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x03,0,0,1)
	rev = resp[0]
	whole=float(rev>>4)
	point = float(rev&0x0F)
	return whole+point/10.0
	
def getHWrev(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x02,0,0,1)
	rev = resp[0]
	whole=float(rev>>4)
	point = float(rev&0x0F)
	return whole+point/10.0	

def getADDR(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x00,0,0,1)
	return resp[0]
	
def getID(addr):
	global GPIObaseADDR
	addr=addr+GPIObaseADDR
	if (addr>255):
		return "ERROR: address out of range - must be less than 255"
	id=""
	arg = range(4)
	resp = []
	arg[0]=addr;
	arg[1]=0x1;
	arg[2]=0;
	arg[3]=0;

	ppFRAME = 25
	GPIO.output(ppFRAME,True)
	null = spi.writebytes(arg)
	count=0
	time.sleep(.0001)
	while (count<20): 
		dummy=spi.readbytes(1)
		if (dummy[0] != 0):
			num = dummy[0]
			id = id + chr(num)
			count = count + 1
		else:
			count=20
	GPIO.output(ppFRAME,False)
	return id	
	
def getPROGdata(addr,paddr):	#read a byte of data from program memory
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0xF0,paddr>>8,paddr&0xFF,2)
	value=(256*resp[0]+resp[1])
	return hex(value)	

def Poll():
    ppFoundCount=0
    for i in range (0,8):
        rtn = getADDR(i)
        if ((rtn-8)==i):
            print "DAQCplate found at address",rtn-8
            ppFoundCount += 1
    if (ppFoundCount == 0):
        print "No DAQCplates found"

	
def ppCMD(addr,cmd,param1,param2,bytes2return):
    global GPIObaseADDR
    arg = range(4)
    resp = []
    arg[0]=addr+GPIObaseADDR;
    arg[1]=cmd;
    arg[2]=param1;
    arg[3]=param2;
    GPIO.output(ppFRAME,True)
    null = spi.writebytes(arg)
    if bytes2return>0:
        time.sleep(.0001)
        for i in range(0,bytes2return):	
            dummy=spi.readbytes(1)
            resp.append(dummy[0])
    GPIO.output(ppFRAME,False)
    return resp	
	

	
Vcc=range(8)
ppFoundCount=0
#getID(0)
for i in range (0,8):
	rtn = getADDR(i)
	if ((rtn-8)==i):
		Vcc[i] = getADC(i,8)
		setDOUTall(i,0)
		setPWM(i,0,0)
		setPWM(i,1,0)
		ppFoundCount += 1
	else:
		Vcc[i]=10000
if (ppFoundCount==0):
    print "No DAQCplates found!"