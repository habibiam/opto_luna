"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the USBDevice class
"""

import device

class USBDevice(device.Device):
    """
    Derived from device, this class represents a non-serial mode USB device.
    """
    pid=""
    vid=""
    uid=""
    devPath=""