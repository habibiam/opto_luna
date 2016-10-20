"""
Module: device_scanner.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  This module is resposible for performing a system scan (aka an inventory)
of devices that are expected to be present on the system.  These devices are defined in
the ../config/LunaSrv/LunaSrcDeviceConfig.xml file.  There are currently three types of
devices supported and are categorized by how they communicate with the OS.
  1) USB-Serial:    Devices that communicate via a serial port (e.g. /dev/ttyXXXX
  2) USB:           Devices that communicate via a vendor supplied API
  3) Ethernet:      Devices that communicate via TCP/IP
"""
import xml.etree.ElementTree as ET
import usb_serial_device
import usb_device
import ethernet_device
import subprocess
import xml_config_subprocess
import re
import socket
#import serial #sudo apt-get install python3-serial
import os
import logbase


class DeviceScanner(logbase.LogBase):
    """
    A class to scan (i.e. look for) devices on the system
    It uses an XML file as directions for what to look for.
    """
    
    configurationFile = ""
    expectedDevices = [] # List of expected devices
    foundDevices = []    # List of devices actually found on the system
    
    def __init__(self, fullPathToConfigFile):
        """
        Constructor, will scan the config file and record info found there.
        :param fullPathToConfigFile: Full path to file to read
        """

        self.configurationFile=fullPathToConfigFile

        self.logger.debug("Read XML file: " + self.configurationFile)
        
        # Read XML file
        tree = ET.parse(self.configurationFile)
        root = tree.getroot()
        
        # Parse the expected USBSerial devices
        for elemUSBSerial in root.iter('USBSerial'):
            #print(elemUSBSerial.attrib)
            aUSBSerialDevice = usb_serial_device.USBSerialDevice()
            aUSBSerialDevice.name = elemUSBSerial.attrib['Name']
            aUSBSerialDevice.pid = elemUSBSerial.attrib['Pid']
            aUSBSerialDevice.vid = elemUSBSerial.attrib['Vid']
            aUSBSerialDevice.uid = elemUSBSerial.attrib['Uid']
            
            for x in  elemUSBSerial:

                # A serial USB device should have port settings associated with it
                elemPortSettings = None
                if x.tag == 'PortSettings':
                    elemPortSettings = x
                
                if elemPortSettings is not None:
                    aUSBSerialDevice.portSettings.baud = int(elemPortSettings.attrib['Baud'])
                    aUSBSerialDevice.portSettings.parity = elemPortSettings.attrib['Parity']
                    aUSBSerialDevice.portSettings.dataBits = int(elemPortSettings.attrib['DataBits'])
                    aUSBSerialDevice.portSettings.stopBits = int(elemPortSettings.attrib['StopBits'])

                # Some of our serial USB devices have a special intermediate process that does the
                # actual communication with the device.  How to start that process is defined in the
                # subprocess element.
                elemSubProcess = None
                if x.tag == 'SubProcess':
                    elemSubProcess = x
                
                if elemSubProcess is not None:
                    aUSBSerialDevice.subProc.cmd = elemSubProcess.attrib['cmd']
                    for anArg in elemSubProcess.iter('Arg'):
                        aUSBSerialDevice.subProc.args.append(anArg.attrib['arg'])
                    
            if len(aUSBSerialDevice.subProc.cmd) == 0:
                aUSBSerialDevice.subProc = None    

            # Remember what we've read.
            self.expectedDevices.append(aUSBSerialDevice)
            
            
        # Parse the expected USB devices
        for elemUSB in root.iter('USB'):
            #print(elemUSB.attrib)
            aUSBDevice = usb_device.USBDevice() 

            aUSBDevice.name = elemUSB.attrib['Name']
            aUSBDevice.pid = elemUSB.attrib['Pid']
            aUSBDevice.vid = elemUSB.attrib['Vid']
            aUSBDevice.uid = elemUSB.attrib['Uid']
            
            self.expectedDevices.append(aUSBDevice)

        # Parse the expected Ethernet devices
        for elemEthernet in root.iter('Ethernet'):
            #print(elemEthernet.attrib)
            anEthernetDevice = ethernet_device.EthernetDevice() 

            anEthernetDevice.name = elemEthernet.attrib['Name']
            anEthernetDevice.host = elemEthernet.attrib['Host']
            anEthernetDevice.port = int(elemEthernet.attrib['Port'])
            
            
            self.expectedDevices.append(anEthernetDevice)
            
    def InventoryDevices(self):
        """
        Perform an inventory of the expected devices.  Record the results in foundDevices
        :return: None
        """
        self.logger.debug("Start Inventory...")
        
        # Find our desired usb devices.  These should be present in /dev somewhere.
        osDevices = os.listdir("/dev")
        osDevices.sort()

        # Loop through all devices in /dev asking them what they are.
        for anOSDevice in osDevices:
            
            deviceName = "/dev/" + anOSDevice
            # We're making use of the unix command "udevadm".  Read up on it!
            cmd = ["udevadm", "info", "-q", "all", "-n", deviceName]
            #print(cmd)
            pid=""
            vid=""
            uid=""
        
            # Launch udevadm for the current device name.
            FNULL = open(os.devnull, 'w')
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=FNULL)
            while True:
                line = proc.stdout.readline()
                if len(line) != 0:
                    #print(line.rstrip())
                    # Parse out the pieces of the output lines looking for the relavent information.
                    parts = re.split("[ ]", line.__str__())
                    #print(parts)
                    if len(parts) > 1:
                        kvParts = re.split("[=]", parts[1].__str__())
                        #print(kvParts)
                        # We care about procuct id, vendor id and serial number.
                        if (kvParts[0] == "ID_VENDOR_ID"):
                            vid = kvParts[1][:-1]
                        if (kvParts[0] == "ID_MODEL_ID"):
                            pid = kvParts[1][:-1]
                        if (kvParts[0] == "ID_SERIAL_SHORT"):
                            uid = kvParts[1][:-1]
                else:
                    break

            # We found a device with a Product ID and Vendor ID.  Is it one were expecting?
            if len(pid) > 0 and len(vid) > 0:
                self.logger.info( "Checking if device with ProductID: " + pid + " and VendorID: " + vid + " on " + deviceName + " is needed...") 
                foundItem = next((x for x in self.expectedDevices if isinstance(x, (usb_serial_device.USBSerialDevice, usb_device.USBDevice)) and 
                      x.pid == pid and
                      x.vid == vid and
                      x.uid == uid and
                      x.inventoried == False), None)
                
                if foundItem is not None:
                    if isinstance(foundItem, usb_serial_device.USBSerialDevice) == True:
                        if anOSDevice.startswith( 'tty') == True:
                            # Device is a Serial USB device.
                            foundItem.devPath = deviceName
                            foundItem.inventoried = True
                            foundItem.checked = True
                    else:
                        #Device is a plain USB device.
                        foundItem.devPath = deviceName
                        foundItem.inventoried = True
                        foundItem.checked = True
                    
            FNULL.close()
                    

                
        
        # Here, we probe to see if any ethernet connected devices are up and listening for connections.   
        while True:
            foundItem = next((x for x in self.expectedDevices if isinstance(x, (ethernet_device.EthernetDevice)) and 
                x.inventoried == False and x.checked == False), None)
            if foundItem is not None:
                #socket.setdefaulttimeout(10.0)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10.0)
                try:
                    s.connect((foundItem.host, foundItem.port))
                    foundItem.inventoried = True;
                except:
                    foundItem.inventoried = False;
                    # Okay to swallow!
                    pass
                finally:
                    s.close()
                foundItem.checked = True;
            else:
                break
                
        # Record what we found.
        self.logger.info("The following devices were inventoried:")
        for x in self.expectedDevices:
            if x.inventoried == True:
                if isinstance(x, (usb_serial_device.USBSerialDevice, usb_device.USBDevice)) == True:
                    self.logger.info(x.name + "  Device Node: " + x.devPath)
                else:
                    self.logger.info(x.name)
                self.foundDevices.append(x)
        
        
        
        