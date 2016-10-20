"""
Module: tec_utils.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the TECUtil class which provides some utility functions for the TEC device.
"""

import logbase
import serial


class TECUtil(logbase.LogBase):
    """
    Utility Class
    """
    bst = ['*', '1', '0', '0', '0', '0', '0', '2', '1', '\r']  # 0 output
    buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def TECOff(self, serialPortName):
        """
        Turn TEC off.  Essentially sends a command to the TEC to set a very low temp
        which we consider "off"
        :param serialPortName: Serial port name, like "/dev/ttyXXXX"
        :return: True on success, false otherwise.
        """
        try:
            self.logger.debug("Turn TEC off ....")
            #Open port
            ser = serial.Serial(serialPortName, 115200, timeout=1)
            # Write command
            for pn in range(0, 10):
                ser.write((self.bst[pn]))
            # Read response
            for pn in range(0, 8):
                self.buf[pn] = ser.read(1)
                #print(buf[pn])
            ser.close()
            # Decode response
            temp1 = self.hexc2dec(self.buf)
            self.logger.debug("TEC Temp at TECOff: " + str(temp1 / 10.0))
            return True
        except Exception, e:
            self.logger.debug("Error communicating with TEC device.")
            return False

    def hexc2dec(self, bufp):
        """
        Helper function: Hex data array to int
        :param bufp: Array containing hex digits
        :return: Integer value
        """
        newval = 0
        divvy = 4096
        for pn in range(1, 5):
            vally = ord(bufp[pn])
            if (vally < 97):
                subby = 48
            else:
                subby = 87
            newval += ((ord(bufp[pn]) - subby) * divvy)
            divvy /= 16
            if (newval > 32767):
                newval = newval - 65536
        return newval



