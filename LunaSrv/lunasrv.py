import device_scanner
import logging
from logging.config import fileConfig
import sys
import select
import signal
import os



scanner = None
cnum = 0



def processINVTHW(receivedDeviceName, recievedArgs):
    global scanner
    global cnum
    
    logger.info("Handle INVTHW command")
    
    # Get full path to our xml device configuration file
    path = os.path.dirname(os.path.abspath(__file__))
    configFile = path + "/DeviceConfig.xml"
    
    if scanner != None:
        for aDevice in scanner.foundDevices:
            aDevice.Shutdown()
            
        del scanner.expectedDevices[:]
        del scanner.foundDevices[:]
        scanner = None

    # Get a device scanner.  This will also read and parse the xml file.
    if scanner == None: 
        scanner = device_scanner.DeviceScanner(configFile)
    
    # Perform an inventory of devices using the xml as a guide as to what to look for.
    scanner.InventoryDevices()
    
    # for every device we found, try to start it.
    for aDevice in scanner.foundDevices:
        aDevice.initialized = aDevice.InitDevice()

        # Start readers for most devices now.  Except the TEC Controller.
        if aDevice.initialized == True and aDevice.name != "TECController":
            aDevice.Read()
            
    # Send back our results
    for aDevice in scanner.expectedDevices:
        size = 94
        name = aDevice.name
        args = ""
        if (aDevice.checked == True and aDevice.initialized == True):
            args = "READY"
        elif (aDevice.checked == True and aDevice.initialized == True):
            args = "NOT READY"
        else:
            args = "NOT FOUND"
           

        size += (len(args) + 1)            
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
            {"cnum": cnum, "size": size, "deviceName": name, "cmd": "INVTHW", "args": args }
            
        logger.debug("Sending command: <"+cmd+">")
            
        sys.stdout.write(cmd)
        sys.stdout.flush()
        
        
        
def processGETVI(receivedDeviceName, recievedArgs):
    global scanner
    global cnum
    
    logger.info("Handle GETVI command")
    
    if scanner == None:
        sendFAILResponse("GETVI", receivedDeviceName)
        return

    
    aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
    aDevice.Write("GETVI\n")
    data = aDevice.GetLastResponse()
    
    if "SYNTAX" in data:
        #retry once
        aDevice.Write("GETVI\n")
        data = aDevice.GetLastResponse()

    args = ""        
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = data[16:]
    else:
        args = "SYNTAX"
        

    size = 94 + len(args) + 1           
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "GETVI", "args": args }
    
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()

        
def processSETV(receivedDeviceName, recievedArgs):
    global scanner
    global cnum
    
    logger.info("Handle SETV command")
    
    if scanner == None:
        sendFAILResponse("SETV", receivedDeviceName)
        return
    
    aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
    aDevice.Write("SETV " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()
    
    if "SYNTAX" in data:
        #retry once
        aDevice.Write("SETV " + str(recievedArgs) + "\n")
        data = aDevice.GetLastResponse()

    args = ""        
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = data[16:]
    else:
        args = "SYNTAX"
        

    size = 94 + len(args) + 1           
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "SETV", "args": args }
    
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSHUTDOWN(receivedDeviceName, recievedArgs):
    logger.info("Handle SHUTDOWN command")
    do_exit()


def processSTARTSEQ(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle STARTSEQ command")

    if scanner == None:
        sendFAILResponse("STARTSEQ", receivedDeviceName)
        return

    aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
    if aDevice is None:
        sendFAILResponse("STARTSEQ", receivedDeviceName)
        return

    cycles = int(recievedArgs)

    #Start the TEC Sequence.  This launches a speparate python process to control the sequence.
    success = aDevice.StartTECSequence(cycles)

    args = ""
    if success == True:
        #Now it's okay to start listening for data from the TEC.
        aDevice.Read()
        args = "OK"
    else:
        args = "FAIL"

    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STARTSEQ", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSTOPSEQ(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle STOPSEQ command")

    if scanner == None:
        sendFAILResponse("STOPSEQ", receivedDeviceName)
        return

    aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
    if aDevice is None:
        sendFAILResponse("STOPSEQ", receivedDeviceName)
        return

    aDevice.Shutdown()

    args = "OK"


    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STOPSEQ", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processREADSEQD(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle READSEQD command")

    if scanner == None:
        sendFAILResponse("READSEQD", receivedDeviceName)
        return

    aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
    aDevice.Write("READSEQD\n")
    args = aDevice.GetLastResponse()




    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "READSEQD", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def sendFAILResponse(recievedCmd, receivedDeviceName):
    global cnum

    args = "FAIL"
    size = 94 + len(args) + 1           
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": recievedCmd, "args": args }
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()


def waitForCommands():
    global cnum
    
    while (1):
        #Wait for data to arrive on stdin(==0)
        if select.select([sys.stdin,],[],[])[0]:
            line = sys.stdin.readline()
            line = line.strip()
            if len(line) > 0:
                logger.debug(line)
                
                cnum = int (line[0:10].strip())
                cmdLen =int (line[10:20].strip())
                cmd = line[84:93].strip()
                devName=line[20:83].strip()
                args = line[94:cmdLen].strip()
                logger.debug("Command Number: " + str(cnum) + " Device Name" + devName + "  Parsed command: <"+cmd+">  Args: <" + args + ">" )
                cmdmap[cmd](devName,args)
                

def do_exit():
    global scanner
    logger.info('Stopping devices...')

    if scanner is not None:
        for aDevice in scanner.foundDevices:
            aDevice.Shutdown()

    logger.info('--------------Exit--------------')
    # Raises SystemExit(0):
    sys.exit(0)


def sigterm_handler(_signo, _stack_frame):
    do_exit()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    cmdmap = {"INVTHW": processINVTHW,
               "GETVI": processGETVI,
               "SETV": processSETV,
               "SHUTDOWN": processSHUTDOWN,
               "STARTSEQ": processSTARTSEQ,
               "STOPSEQ": processSTOPSEQ,
               "READSEQD": processREADSEQD}

    path = os.path.dirname(os.path.abspath(__file__))
    loggerIniFile = path + "/logger.ini"
    
    fileConfig(loggerIniFile)
    logger = logging.getLogger()
    logger.info('--------------Start--------------')
    
    waitForCommands()
    
