"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the USBDevice class
"""


import device
import ValveControlLib_module
import SpectroLib_module
import os


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

        # Try to initialize the device via its API
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

        if self.name == "Spectrometer":
            self.logger.debug("Start Spectrometer...")

            try:
                ret = SpectroLib_module.Initialize()
                if ret == 0:
                    self.logger.error("Spectrometer Error: " + SpectroLib_module.GetLastErrorMsg())
                    return False

            except Exception, e:
                self.logger.error("Fail Spectrometer Init. "  + " Exception: " + str(e))
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


        if self.name == "Spectrometer":
            self.logger.debug("Spectrometer process data: <" + data + ">")

            if data.startswith("EXP:"):
                parts = data.split(":")
                exp = 0;
                try:
                    exp = int(parts[1])
                except Exception, e:
                    self.logger.error("Spectrometer data conversion error: " + str(e))
                    self.lastMsg = "FAIL"
                    return

                ret = SpectroLib_module.SetExposureMS(exp)
                if ret == 0:
                    self.logger.error("Spectrometer Error: " + SpectroLib_module.GetLastErrorMsg())
                    self.lastMsg = "FAIL"
                    return

            if data.startswith("ISC:"):
                ret = SpectroLib_module.IsCaptureContinuousSpectrumDone()
                if ret == 0:
                    self.lastMsg = "TRUE"
                else:
                    self.lastMsg = "FALSE"
                    return

            if data.startswith("STARTC:"):
                parts = data.split(":")
                args = parts[1]
                argParts = args.split()
                filename = argParts[0];
                delayMS = 0;
                durationMS = 0;
                try:
                    delayMS = int(argParts[1])
                    durationMS = int(argParts[2])
                except Exception, e:
                    self.logger.error("Spectrometer data conversion error: " + str(e))
                    self.lastMsg = "FAIL"
                    return

                path = os.path.dirname(os.path.abspath(__file__))
                # ...and set our current directory to that same location so
                # that we know where we are and where to look for other files.
                path = os.getcwd()
                path += "/../data/"
                destFilename = path + filename

                self.logger.debug("Spectrometer start continuous: <" + destFilename + "> <" + str(delayMS) + "> <" + str(durationMS) + ">")

                ret = SpectroLib_module.CaptureContinuousSpectrum(destFilename, delayMS, durationMS)
                if ret == 0:
                    self.logger.error("Spectrometer Error: " + SpectroLib_module.GetLastErrorMsg())
                    self.lastMsg = "FAIL"
                    return




    def GetLastResponse(self):
        """
        Get the last known response from this device.
        :return: Device's last message.
        """
        return self.lastMsg
