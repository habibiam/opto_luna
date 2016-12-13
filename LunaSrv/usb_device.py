"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the USBDevice class
"""


import device
import ValveControlLib_module


class USBDevice(device.Device):
    """
    Derived from device, this class represents a non-serial mode USB device.
    """
    pid=""
    vid=""
    uid=""
    devPath=""

    def InitDevice(self):
        """
        For a usb device, we typically have a vendor supplied API to control that device.
        Each one is different and will require custom code.
        :return:
        """
        super(USBDevice, self).InitDevice()

        # Try to open the serial port if we're not the TECController
        if self.name == "FluidValve":
            self.logger.debug("Start Fluid Valve...")

            try:
                ret = ValveControlLib_module.Initialize(self.devPath)
                if ret == 0:
                    self.logger.error("Fluid Valve Error: " + ValveControlLib_module.GetLastErrorMsg())
                    return False

                ret = ValveControlLib_module.SetPosition(ValveControlLib_module.STATE_CLOSED)
                if ret == 0:
                    # failed
                    self.logger.error("Fluid Valve Error: " + ValveControlLib_module.GetLastErrorMsg())
                    return False

            except Exception, e:
                self.logger.error("Fail Fluid Valve Init. "  + " Exception: " + str(e))
                return False

            self.lastMsg = "OK"
            self.initialized = True
            return True

        return False


    def Write(self, data):
        """
        Although this function is called Write, it doesn't really write to a device per se, it writes
        to an API!
        :param data: relevant to the target device
        :return: None
        """

        self.lastMsg = "OK"

        if self.name == "FluidValve":
            self.logger.debug("Fluid Valve process data: <" + data + ">")
            if data == "A":
                state = ValveControlLib_module.STATE_A
            elif data == "CLOSED":
                state = ValveControlLib_module.STATE_CLOSED
            elif data == "B":
                state = ValveControlLib_module.STATE_B
            else:
                self.lastMsg = "SYNTAX"
                return

            ret = ValveControlLib_module.SetPosition(state)
            if ret == 0:
                # failed
                self.logger.error("Fluid Valve Error: " + ValveControlLib_module.GetLastErrorMsg())
                self.lastMsg = "FAIL"
                return



    def GetLastResponse(self):
        """
        Get the last known response from this device.
        :return: Device's last message.
        """
        return self.lastMsg
