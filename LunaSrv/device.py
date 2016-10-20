"""
Module: device_scanner.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the base class for all device types,
"""

import logbase

class Device(logbase.LogBase):
    """
    Base class for all devices
    It is expected that derived classes will override the functions.
    We also inherit our system logger so we have the same logger in our device classes
    """
    name = "" # Name of device.  From XML file
    inventoried=False  # set to true when a device is found
    initialized=False  # set to true when a device is successfully initialized
    checked=False      # set to true when a device was found 
    stop=False # Flag used when shutting down a device

    # For the base class, we're really just defining the interface.
    # It is expected that derived classes will override these functions as needed.
    def InitDevice(self):
        self.logger.debug("Initialize Device...")
        
    def Read(self):
        pass
        
    def Write(self, data):
        pass
    
    def Shutdown(self):
        pass
    
    def GetLastResponse(self):
        pass
     
        