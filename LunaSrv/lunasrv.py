"""
Module: lunasrv.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  This module is the entry point for the Luna system's instrument controller software,
known as LunaSrv.  Communication to LunaSrv is via pipes where this processes' stdin is monitored
for commands and responses are sent out on stdout.  There are two supporting classes: device_scanner and
device (and its derived types).  They are responsible for handling system setup discovery and communication
with an individual device in the system,
"""
import device_scanner
import logging
from logging.config import fileConfig
import sys
import select
import signal
import os
import json
import time


scanner = None
cnum = 0


def processRUNSAMPLE(receivedDeviceName, recievedArgs):
    """
    Started on processRUNSAMPLE in order to add the run_config.json
    file in to the LunaSrv.
    Need to built this once all the devices are hooked up and sample runs are ready to be automated
    as of now, can load and have access to json config file.
    """
    global scanner
    global cnum

    logger.info("Handle RUNSAMPLE command")

    # Get full path to our json run configuration file

    path = os.path.dirname(os.path.abspath(__file__))
    path += "/../config"
    configFile = path + "/run_config.json"

    with open(configFile, 'r') as f:
        run_config = json.load(f)
    print run_config


def processINVTHW(receivedDeviceName, recievedArgs):
    """
    Process the INVenTory HardWare command.  Will initiate a scan of the system
    looking for expected devices. Expected devices are defined in the config file
    ..\config\LunaSrvDeviceConfig.xml.  Found devices are initialized as per their
    type.  Finally, for each expected device a status message is sent to the pipe
    containing the name of a specific device and its status.
    :param receivedDeviceName: Target device, in this case should be empty
    :param recievedArgs: Expected command arguments, None for this command
    :return: None
    """
    global scanner
    global cnum
    
    logger.info("Handle INVTHW command")
    
    # Get full path to our xml device configuration file
    path = os.path.dirname(os.path.abspath(__file__))
    path += "/../config"
    configFile = path + "/LunaSrvDeviceConfig.xml"

    # Clean up old status so we can go again if needed.
    if scanner != None:
        for aDevice in scanner.foundDevices:
            aDevice.Shutdown()
            
        del scanner.expectedDevices[:]
        del scanner.foundDevices[:]
        scanner = None

    # Get a device scanner.  This will also read and parse the xml file.
    if scanner is None:
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
        elif (aDevice.checked == True and aDevice.initialized == False):
            args = "NOT READY"
        else:
            args = "NOT FOUND"


        size += (len(args) + 1)
        cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
            {"cnum": cnum, "size": size, "deviceName": name, "cmd": "INVTHW", "args": args }

        logger.debug("Sending command: <"+cmd+">")

        sys.stdout.write(cmd)
        sys.stdout.flush()

"""
High voltage Supply
"""
def processHVSON(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle HVSON command")

    if scanner is None:
        sendFAILResponse("HVSON", receivedDeviceName)
    return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("HVSON", receivedDeviceName)
        return

    aDevice.Write("HVSON\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("HVSON\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "HVSON", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processHVSOFF(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle HVSOFF command")

    if scanner is None:
        sendFAILResponse("HVSOFF", receivedDeviceName)
    return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("HVSOFF", receivedDeviceName)
        return

    aDevice.Write("HVSOFF\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("HVSOFF\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "HVSOFF", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processGETVI(receivedDeviceName, recievedArgs):
    """
    Process the GET Voltage and Current(I) command.
    Queries the High Voltage Power Supply device for Voltage and Current.
    Sends back data to caller.
    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle GETVI command")

    if scanner is None:
        sendFAILResponse("GETVI", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("GETVI", receivedDeviceName)
        return

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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "GETVI", "args": args }
    
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()

def processSETV(receivedDeviceName, recievedArgs):
    """
    Process the SET Voltage command.  Sends a set voltage command to the named device
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Voltage to set.
    :return: None
    """
    global scanner
    global cnum
    
    logger.info("Handle SETV command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("SETV", receivedDeviceName)
        return

    #Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("SETV", receivedDeviceName)
        return

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
        
    # Send results back to caller
    size = 94 + len(args) + 1           
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "SETV", "args": args }
    
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Shutdown
"""
def processSHUTDOWN(receivedDeviceName, recievedArgs):
    """
    Process SHUTDOWN command.  Will shutdown all devices and exit.
    No response is sent.
    :param receivedDeviceName: None
    :param recievedArgs: None
    :return: None
    """
    logger.info("Handle SHUTDOWN command")
    do_exit()

"""
TEC CONTROLLER
"""
def processSTARTSEQ(receivedDeviceName, recievedArgs):
    """
    Process the START SEQuence command.  The sequence is a thermocycler sequence.
    :param receivedDeviceName: The target device.
    :param recievedArgs: Number of cycles
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STARTSEQ command")

    if scanner is None:
        sendFAILResponse("STARTSEQ", receivedDeviceName)
        return

    aDevice = get_device_by_name(receivedDeviceName)
    if aDevice is None:
        sendFAILResponse("STARTSEQ", receivedDeviceName)
        return

    cycles = int(recievedArgs)

    # Start the TEC Sequence.  This launches a speparate python process to control the sequence.
    success = aDevice.StartTECSequence(cycles)

    args = ""
    if success == True:
        # Now it's okay to start listening for data from the TEC.
        aDevice.Read() # Non-blocking
        args = "OK"
    else:
        args = "FAIL"

    # Send caller response
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STARTSEQ", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSTOPSEQ(receivedDeviceName, recievedArgs):
    """
    Process the STOP SEQuence command. Will stop a running thermocycler sequence.
    :param receivedDeviceName: The target device.
    :param recievedArgs: None.
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STOPSEQ command")

    if scanner is None:
        sendFAILResponse("STOPSEQ", receivedDeviceName)
        return

    # Find the device and perform a shutdown.
    aDevice = get_device_by_name(receivedDeviceName)
    if aDevice is None:
        sendFAILResponse("STOPSEQ", receivedDeviceName)
        return

    aDevice.Shutdown()

    args = "OK"

    # Send caller response
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STOPSEQ", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processREADSEQD(receivedDeviceName, recievedArgs):
    """
    Process the READ SEQuence Data command.  Will read current date from the thermocycler device.
    This includes block temp, sample temp, current cycle and current step/
    :param receivedDeviceName: The target device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle READSEQD command")

    if scanner is None:
        sendFAILResponse("READSEQD", receivedDeviceName)
        return

    # Find device, read last data, and send response.
    aDevice = get_device_by_name(receivedDeviceName)
    if aDevice is None:
        sendFAILResponse("READSEQD", receivedDeviceName)
        return

    # Get last bit of data from device
    aDevice.Write("READSEQD\n")
    args = aDevice.GetLastResponse()

    # Send our response
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "READSEQD", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
OBIS Laser
"""
def processGETLPWR(receivedDeviceName, recievedArgs):
    """
    Process the GET Laser PoWeR command.
    Queries the laser device for its current power.
    Sends back data to caller.
    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle LPWR command")

    if scanner is None:
        sendFAILResponse("LPWR", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("LPWR", receivedDeviceName)
        return

    tries = 0
    max_tries = 6

    while tries < max_tries:
        sendData = "SOUR:POW:LEV?\r\n"
        aDevice.Write(sendData)
        time.sleep(0.02)
        data = aDevice.GetLastResponse()
        data = data.strip()

        if "ERR" in data or "SYNTAX" in data or "FAIL" in data or len(data) == 0:
            tries = tries + 1
            time.sleep(0.1)
        else:
            break

    args = ""
    if "ERR" in data:
        args = "FAIL"
    elif "OK" in data:
        # Parse the returned data.
        # Expected X.XXXXX\r\nOK
        parts = data.split()
        args = parts[0]
    else:
        args = "SYNTAX"

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "LPWR", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSETLSTATE(receivedDeviceName, recievedArgs):
    """
    Process the GET Laser PoWeR command.
    Queries the laser device for its current power.
    Sends back data to caller.
    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum
    cmdName = "SETLSTATE"

    logger.info("Handle SETLSTATE command")

    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    if recievedArgs != "ON" and recievedArgs != "OFF":
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    tries = 0
    max_tries = 6

    while tries < max_tries:
        sendData = "SOUR:AM:STAT " + recievedArgs + "\r\n"
        aDevice.Write(sendData)
        time.sleep(0.02)
        data = aDevice.GetLastResponse()
        data = data.strip()

        if "ERR" in data or "SYNTAX" in data or "FAIL" in data or len(data) == 0:
            tries = tries + 1
            time.sleep(0.1)
        else:
            break

    args = ""
    if "ERR" in data:
        args = "FAIL"
    elif "OK" in data:
        args = "OK"
    else:
        args = "SYNTAX"

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": cmdName, "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSETLPWR(receivedDeviceName, recievedArgs):
    """
    Process the SET Laser PoWeR command.  Sends a set power command to the named device
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Power to set.
    :return: None
    """
    global scanner
    global cnum
    cmdName = "SETLPWR"


    logger.info("Handle SETLPWR command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    if len(recievedArgs) == 0:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    tries = 0
    max_tries = 6

    while tries < max_tries:
        sendData = "SOUR:POW:LEV:IMM:AMPL " + recievedArgs + "\r\n"
        aDevice.Write(sendData)
        time.sleep(0.02)
        data = aDevice.GetLastResponse()
        data = data.strip()

        if "ERR" in data or "SYNTAX" in data or "FAIL" in data or len(data) == 0:
            tries = tries + 1
            time.sleep(0.1)
        else:
            break


    args = ""
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = "OK"
    else:
        args = "SYNTAX"

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "SETLPWR", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


"""
Fluid Valve (LabSmith Valve)
"""
def processFVALVEPOS(receivedDeviceName, recievedArgs):
    """
    Process the Fluid VALVE POSition command.  Send a command to position the fluidic valve
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Position to set A, CLOSED or B
    :return: None
    """
    global scanner
    global cnum
    cmdName = "FVALVEPOS"


    logger.info("Handle FVALVEPOS command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return


    aDevice.Write(recievedArgs)
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write(recievedArgs)
        data = aDevice.GetLastResponse()

    args = ""
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = data
    else:
        args = "SYNTAX"

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": cmdName, "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


"""
Spectrometer
"""
def processSPCSETEXP(receivedDeviceName, recievedArgs):
    """
    Process the SPeCtrometer SET EXPosure command.  Will set exposure for the spectrometer
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Exposure time, in milliseconds
    :return: None
    """
    global scanner
    global cnum
    cmdName = "SPCSETEXP"


    logger.info("Handle SPCSETEXP command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return


    aDevice.Write("EXP:" + recievedArgs)
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write(recievedArgs)
        data = aDevice.GetLastResponse()

    args = ""
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = data
    else:
        args = "SYNTAX"

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": cmdName, "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSPCSTARTC(receivedDeviceName, recievedArgs):
    """
    Process the SPeCtrometer START Continuous capture command.
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Filename, time between scans, duration time
    :return: None
    """
    global scanner
    global cnum
    cmdName = "SPCSTARTC"


    logger.info("Handle SPCSTARTC command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return


    aDevice.Write("STARTC:" + recievedArgs)
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write(recievedArgs)
        data = aDevice.GetLastResponse()

    args = ""
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "FAIL" in data:
        args = "FAIL"
    elif "OK" in data:
        args = data
    else:
        args = "SYNTAX"

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": cmdName, "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processSPCISCRUN(receivedDeviceName, recievedArgs):

    """
    Process the SPeCtrometer IS Continuous RUNning
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum
    cmdName = "SPCISCRUN"


    logger.info("Handle SPCISCRUN command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse(cmdName, receivedDeviceName)
        return


    aDevice.Write("ISC:")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write(recievedArgs)
        data = aDevice.GetLastResponse()

    args = ""
    if "SYNTAX" in data:
        args = "SYNTAX"
    elif "TRUE" in data or "FALSE" in data:
        args = data
    else:
        args = "SYNTAX"

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": cmdName, "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Laser Motor
"""
def processLASLEFT(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle LASLEFT command")

    if scanner is None:
        sendFAILResponse("LASLEFT", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("LASLEFT", receivedDeviceName)
        return

    aDevice.Write("LASLEFT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("LASLEFT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "LASLEFT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processLASRIGHT(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle LASRIGHT command")

    if scanner is None:
        sendFAILResponse("LASRIGHT", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("LASRIGHT", receivedDeviceName)
        return

    aDevice.Write("LASRIGHT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("LASRIGHT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "LASRIGHT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processLMHOME(receivedDeviceName, recievedArgs):
    """
    process Laser Motor HOME

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle LMHOME command")

    if scanner is None:
        sendFAILResponse("LMHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("LMHOME", receivedDeviceName)
        return

    aDevice.Write("LMHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("LMHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "LMHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCAPREADY(receivedDeviceName, recievedArgs):
    """
    process Laser Motor CAPREADY

    Laser Motor moves back to it's original position relative to capillary being installed

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle CAPREADY command")

    if scanner is None:
        sendFAILResponse("CAPREADY", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CAPREADY", receivedDeviceName)
        return

    aDevice.Write("CAPREADY\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("LMHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CAPREADY", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Gel pump
"""
def processGPHOME(receivedDeviceName, recievedArgs):
    """
        Process the SPeCtrometer IS Continuous RUNning
        :param receivedDeviceName: The name of the device.
        :param recievedArgs: None
        :return: None
        """
    global scanner
    global cnum

    logger.info("Handle GPHOME command")

    if scanner is None:
        sendFAILResponse("GPHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("GPHOME", receivedDeviceName)
        return

    aDevice.Write("GPHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("GPHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "GPHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processGPSTART(receivedDeviceName, recievedArgs):
    """
    Process the SPeCtrometer IS Continuous RUNning
    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle GPSTART command")

    if scanner is None:
        sendFAILResponse("GPSTART", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("GPSTART", receivedDeviceName)
        return

    aDevice.Write("GPSTART\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("GPSTART\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "GPSTART", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processGPRATE(receivedDeviceName, recievedArgs):
    return

"""
Capillary Heater
"""
def processCAPHEATON(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle CAPHEATON command")

    if scanner is None:
        sendFAILResponse("CAPHEATON", receivedDeviceName)
    return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CAPHEATON", receivedDeviceName)
        return

    aDevice.Write("CAPHEATON\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CAPHEATON\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CAPHEATON", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCAPHEATOFF(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle CAPHEATOFF command")

    if scanner is None:
        sendFAILResponse("CAPHEATOFF", receivedDeviceName)
    return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CAPHEATOFF", receivedDeviceName)
        return

    aDevice.Write("CAPHEATOFF\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CAPHEATOFF\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CAPHEATOFF", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCAPGETT(receivedDeviceName, recievedArgs):
    global scanner
    global cnum

    logger.info("Handle CAPGETT command")

    if scanner is None:
        sendFAILResponse("CAPGETT", receivedDeviceName)
    return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CAPGETT", receivedDeviceName)
        return

    aDevice.Write("CAPGETT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CAPGETT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CAPGETT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCAPSETT(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName:
    :param recievedArgs:
    :return:
    """
    global scanner
    global cnum

    logger.info("Handle CAPSETT command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("CAPSETT", receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CAPSETT", receivedDeviceName)
        return

    aDevice.Write("CAPSETT " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()

    if "CAPSETT" in data:
        # retry once
        aDevice.Write("CAPSETT " + str(recievedArgs) + "\n")
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

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CAPSETT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Reagents W, P, B, and M
"""
def processRWHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent W HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RWHOME command")

    if scanner is None:
        sendFAILResponse("RWHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RWHOME", receivedDeviceName)
        return

    aDevice.Write("RWHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RWHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RWHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processRWRATE(receivedDeviceName, recievedArgs):
    """
    Process the Reagent W RATE command.
    Sends a set rate [microL/sec] command to the named device [pi]

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Voltage to set.
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RWRATE command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("RWRATE", receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RWRATE", receivedDeviceName)
        return

    aDevice.Write("RWRATE " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RWRATE " + str(recievedArgs) + "\n")
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

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RWRATE", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processRPHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent P HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RPHOME command")

    if scanner is None:
        sendFAILResponse("RPHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RPHOME", receivedDeviceName)
        return

    aDevice.Write("RPHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RPHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RPHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processRPRATE(receivedDeviceName, recievedArgs):
    """
    Process the Reagent P RATE command.
    Sends a set rate [microL/sec] command to the named device [pi]

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Voltage to set.
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RPRATE command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("RPRATE", receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RPRATE", receivedDeviceName)
        return

    aDevice.Write("RPRATE " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RPRATE " + str(recievedArgs) + "\n")
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

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RPRATE", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processRBHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent B HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RBHOME command")

    if scanner is None:
        sendFAILResponse("RBHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RBHOME", receivedDeviceName)
        return

    aDevice.Write("RBHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RBHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RBHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processRBRATE(receivedDeviceName, recievedArgs):
    """
    Process the Reagent B RATE command.
    Sends a set rate [microL/sec] command to the named device [pi]

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Voltage to set.
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RBRATE command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("RBRATE", receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RBRATE", receivedDeviceName)
        return

    aDevice.Write("RBRATE " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RBRATE " + str(recievedArgs) + "\n")
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

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RBRATE", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processRMHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent M HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RMHOME command")

    if scanner is None:
        sendFAILResponse("RMHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RMHOME", receivedDeviceName)
        return

    aDevice.Write("RMHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RMHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RMHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def processRMRATE(receivedDeviceName, recievedArgs):
    """
    Process the Reagent M RATE command.
    Sends a set rate [microL/sec] command to the named device [pi]

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: Voltage to set.
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle RMRATE command")

    # Fail if inventory has not been done yet.
    if scanner is None:
        sendFAILResponse("RMRATE", receivedDeviceName)
        return

    # Find device by name, send the command to it, and read response.
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("RMRATE", receivedDeviceName)
        return

    aDevice.Write("RMRATE " + str(recievedArgs) + "\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("RMRATE " + str(recievedArgs) + "\n")
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

    # Send results back to caller
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RMRATE", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Chip Station Z
"""
def processCHIPZHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent M HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle CHIPZHOME command")

    if scanner is None:
        sendFAILResponse("CHIPZHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CHIPZHOME", receivedDeviceName)
        return

    aDevice.Write("CHIPZHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CHIPZHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CHIPZHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCHIPZUP(receivedDeviceName, recievedArgs):
    """
    Process the CHIP Z UP command.
    Move Chip Station Z up

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle CHIPZUP command")

    if scanner is None:
        sendFAILResponse("CHIPZUP", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CHIPZUP", receivedDeviceName)
        return

    aDevice.Write("CHIPZUP\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CHIPZUP\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CHIPZUP", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Chip Station Y
"""
def processCHIPYHOME(receivedDeviceName, recievedArgs):
    """
    Process the Reagent M HOME command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle CHIPYHOME command")

    if scanner is None:
        sendFAILResponse("CHIPYHOME", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CHIPYHOME", receivedDeviceName)
        return

    aDevice.Write("CHIPYHOME\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CHIPYHOME\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CHIPYHOME", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processCHIPYOUT(receivedDeviceName, recievedArgs):
    """
    Process the CHIP Y OUT command.

    :param receivedDeviceName: The name of the device
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle CHIPYOUT command")

    if scanner is None:
        sendFAILResponse("CHIPYOUT", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("CHIPYOUT", receivedDeviceName)
        return

    aDevice.Write("CHIPYOUT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("CHIPYOUT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "CHIPYOUT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

# """
# Valve V1-V20
# """
# def processValve(receivedDeviceName, recievedArgs):
#     """
#
#     :param receivedDeviceName: The name of the device.
#         In this case, it should 'Pi'
#     :param recievedArgs: OPEN | CLOSED.
#     :return: None
#     """
#     global scanner
#     global cnum
#
#     logger.info("Handle RMRATE command")
#
#     # Fail if inventory has not been done yet.
#     if scanner is None:
#         sendFAILResponse("RMRATE", receivedDeviceName)
#         return
#
#     # Find device by name, send the command to it, and read response.
#     aDevice = get_device_by_name(receivedDeviceName)
#
#     if aDevice is None:
#         sendFAILResponse("RMRATE", receivedDeviceName)
#         return
#
#     aDevice.Write("RMRATE " + str(recievedArgs) + "\n")
#     data = aDevice.GetLastResponse()
#
#     if "SYNTAX" in data:
#         # retry once
#         aDevice.Write("RMRATE " + str(recievedArgs) + "\n")
#         data = aDevice.GetLastResponse()
#
#     args = ""
#     if "SYNTAX" in data:
#         args = "SYNTAX"
#     elif "FAIL" in data:
#         args = "FAIL"
#     elif "OK" in data:
#         args = data[16:]
#     else:
#         args = "SYNTAX"
#
#     # Send results back to caller
#     size = 94 + len(args) + 1
#     cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
#           {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "RMRATE", "args": args}
#
#     logger.debug("Sending command: <" + cmd + ">")
#
#     sys.stdout.write(cmd)
#     sys.stdout.flush()

"""
Stage X
"""
def processSTAGEXLEFT(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STAGEXLEFT command")

    if scanner is None:
        sendFAILResponse("STAGEXLEFT", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("STAGEXLEFT", receivedDeviceName)
        return

    aDevice.Write("STAGEXLEFT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("STAGEXLEFT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STAGEXLEFT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processSTAGEXRIGHT(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STAGEXRIGHT command")

    if scanner is None:
        sendFAILResponse("STAGEXRIGHT", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("STAGEXRIGHT", receivedDeviceName)
        return

    aDevice.Write("STAGEXRIGHT\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("STAGEXRIGHT\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STAGEXRIGHT", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

"""
Stage Z
"""
def processSTAGEZUP(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STAGEZUP command")

    if scanner is None:
        sendFAILResponse("STAGEZUP", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("STAGEZUP", receivedDeviceName)
        return

    aDevice.Write("STAGEZUP\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("STAGEZUP\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STAGEZUP", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()

def processSTAGEZDN(receivedDeviceName, recievedArgs):
    """

    :param receivedDeviceName: The name of the device.
    :param recievedArgs: None
    :return: None
    """
    global scanner
    global cnum

    logger.info("Handle STAGEZDN command")

    if scanner is None:
        sendFAILResponse("STAGEZDN", receivedDeviceName)
        return

    # Find the correct device by name (as defined in the xml file).
    aDevice = get_device_by_name(receivedDeviceName)

    if aDevice is None:
        sendFAILResponse("STAGEZDN", receivedDeviceName)
        return

    aDevice.Write("STAGEZDN\n")
    data = aDevice.GetLastResponse()

    if "SYNTAX" in data:
        # retry once
        aDevice.Write("STAGEZDN\n")
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

    # Send back results
    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": "STAGEZDN", "args": args}

    logger.debug("Sending command: <" + cmd + ">")

    sys.stdout.write(cmd)
    sys.stdout.flush()


def get_device_by_name(receivedDeviceName):
    """
    Get a device by its name from the scanners found devices/
    :param receivedDeviceName: Device to look for.
    :return: a device on success, None otherwise
    """
    global scanner
    try:
        aDevice = next(x for x in scanner.foundDevices if x.name == receivedDeviceName)
        return aDevice
    except Exception, e:
        return None


def sendFAILResponse(recievedCmd, receivedDeviceName):
    """
    Send a general FAIL response for a given command and device
    :param recievedCmd: Failed command.
    :param receivedDeviceName: Device Name
    :return: None
    """
    global cnum

    # Send the FAIL status
    args = "FAIL"
    size = 94 + len(args) + 1           
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": receivedDeviceName, "cmd": recievedCmd, "args": args }
    
    logger.debug("Sending command: <"+cmd+">")
            
    sys.stdout.write(cmd)
    sys.stdout.flush()


def waitForCommands():
    """
    Poll for commands on stdin.  Commands are expected to be line-feed terminated.
    See the document: "Instrument Control Command Set" for details on command layout
    and supported commands.
    :return:
    """
    global cnum
    
    while (1):
        # Wait for data to arrive on stdin(==0)
        if select.select([sys.stdin,],[],[])[0]:
            line = sys.stdin.readline()
            line = line.strip()
            if len(line) > 0:
                logger.debug(line)

                # Parse out individual fields
                cnum = int (line[0:10].strip())
                cmdLen =int (line[10:20].strip())
                devName = line[20:84].strip()
                cmd = line[84:94].strip()
                args = line[94:cmdLen].strip()
                logger.debug("Command Number: " + str(cnum) + " Device Name" + devName + "  Parsed command: <"+cmd+">  Args: <" + args + ">" )
                # Call the appropriate handler function.
                cmdmap[cmd](devName,args)
                

def do_exit():
    """
    Gracefully shutdown the system and exit.
    :return: None
    """
    global scanner
    logger.info('Stopping devices...')

    # Stop every device.
    if scanner is not None:
        for aDevice in scanner.foundDevices:
            aDevice.Shutdown()

    logger.info('--------------Exit--------------')
    # Raises SystemExit(0):
    sys.exit(0)


def sigterm_handler(_signo, _stack_frame):
    """
    Handle a unix style signal.  In this case, handle SIGTERM.
    Will call our shutdown routine.
    :param _signo: Unix Signal Number, e.g. SIGTERM
    :param _stack_frame: Current stack
    :return: None
    """
    do_exit()


if __name__ == '__main__':
    # Set up a signal handler to handle most common reasons for stopping.
    signal.signal(signal.SIGTERM, sigterm_handler) # kill
    signal.signal(signal.SIGINT, sigterm_handler) # Ctrl-C

    # Setup all function calling vector for each supported command.
    cmdmap = { "RUNSAMPLE": processRUNSAMPLE,
               "INVTHW": processINVTHW,
               "HVSON": None, #Haven't implemented on the instrument side
               "HVSOFF": None, # Have to talk with kevin dong about this.
               "GETVI": processGETVI,
               "SETV": processSETV,
               "SHUTDOWN": processSHUTDOWN,
               "STARTSEQ": processSTARTSEQ,
               "STOPSEQ": processSTOPSEQ,
               "READSEQD": processREADSEQD,
               "SETLSTATE": processSETLSTATE,
               "SETLPWR": processSETLPWR,
               "GETLPWR": processGETLPWR,
               "FVALVEPOS": processFVALVEPOS,
               "SPCSETEXP": processSPCSETEXP,
               "SPCSTARTC": processSPCSTARTC,
               "SPCISCRUN": processSPCISCRUN,
               # Dave's pi process functions
               "CAPHEATON": processCAPHEATON,
               "CAPHEATOFF": processCAPHEATOFF,
               "CAPGETT": processCAPGETT,
               "CAPSETT": processCAPSETT,
               "LASLEFT": processLASLEFT,
               "LASRIGHT": processLASRIGHT,
               "LMHOME": processLMHOME,
               "CAPREADY": processCAPREADY,
               "GPHOME": processGPHOME,
               "GPRATE": processGPRATE,
               "GPSTART": processGPSTART,
               "RWHOME": processRWHOME,
               "RWRATE": processRWRATE,
               "RPHOME": processRPHOME,
               "RPRATE": processRPRATE,
               "RBHOME": processRBHOME,
               "RBRATE": processRBRATE,
               "RMHOME": processRMHOME,
               "RMRATE": processRMRATE,
               "CHIPZHOME": processCHIPZHOME,
               "CHIPZUP": processCHIPZUP,
               "CHIPYHOME": processCHIPYHOME,
               "CHIPYOUT": processCHIPYOUT,
               # Need to add valve controls... v1-v20
               "STAGEXRIGHT": None,
               "STAGEXLEFT": None,
               "STAGEZUP": None,
               "STAGEZDN": None
            }

    # Get path to this file...
    path = os.path.dirname(os.path.abspath(__file__))
    # ...and set our current directory to that same location so
    # that we know where we are and where to look for other files.
    os.chdir(path)

    path += "/../config"
    loggerIniFile = path + "/LunaSrvLogger.ini"

    # Start our logger
    fileConfig(loggerIniFile)
    logger = logging.getLogger()
    logger.info('--------------Start--------------')

    #processINVTHW("", "")
    #do_exit()

    # loop forever
    waitForCommands()
    
