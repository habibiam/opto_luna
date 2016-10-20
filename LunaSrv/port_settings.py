"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the PortSettings class
"""

class PortSettings:
    """
    Provides common serial port settings and defaults.
    """
    baud = 115200
    parity = "N"
    dataBits = 8
    stopBits = 1
    