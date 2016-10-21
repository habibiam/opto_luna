"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the USBSerialDevice class.  This class is responsible for communicating with all
known types of serial based USB devices on the Luna system/
"""

import device
import port_settings
import xml_config_subprocess
import serial
from threading import Thread
import time
import os
import subprocess
import tec_utils
import mmap
import posix_ipc


class USBSerialDevice(device.Device):
    """
    Derived from Device, this class contains functionality to deal with known USB Serial mode devices.
    Generally, a USB serial device just reads via a serial port on some /dev/ttyXXX device.  However,
    we have also categorized a special type of USB serial device that has an intermediate process in
    between this process and the device.  For that type we may have a unique way of communication with that'
    subprocess.  Currently, only the TECController device uses this method and for that device, communication
    is via shared memory.
    """
    pid = ""
    vid = ""
    uid = ""
    devPath = "" # Device path, like "/dev/ttyXXXX"
    portSettings = port_settings.PortSettings() # serail port settings
    serialPort = None
    stop = False # Flag: stop communication with device?
    thread = None # Background reader thread.
    lastMsg = "" # Last message read from the device.

    subProc = xml_config_subprocess.deviceSubProcess()
    proc = None

    def Shutdown(self):
        """
        Gracefully shutdown this device.
        :return: None
        """

        # If we have a reader thread, shut it down.
        # Wait up to 2 seconds for it to die.
        if self.thread is not None:
            self.stop = True
            self.thread.join(2.0)
            self.thread = None

        # If the serial port is open, close it.
        if self.serialPort is not None:
            if self.serialPort.isOpen():
                self.serialPort.close()
            self.serialPort = None

        # If a subprocess is still running, forcefully kill it.
        if self.proc is not None and self.proc.returncode is None:
            self.proc.kill()
            self.proc = None

        # If were the special device TECController, turn off.
        if self.name == "TECController":
            tu = tec_utils.TECUtil()
            tu.TECOff(self.devPath)

    def InitDevice(self):
        """
        For this type of device, initializing generally means simply opening a serial
        connection to the device. If were the TECController, just make sure we're off for now.
        :return: True on success, false otherwise
        """
        super(USBSerialDevice, self).InitDevice()

        # Try to open the serial port if we're not the TECController
        if self.name != "TECController":
            self.logger.debug("Connecting to port: " + self.devPath)

            try:
                self.serialPort = serial.Serial(
                    port=self.devPath,
                    baudrate=int(self.portSettings.baud),
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=int(self.portSettings.dataBits),
                    timeout=0)

            except serial.SerialException, e:
                self.logger.error("Could not connect to port: " + self.devPath + " Exception: " + str(e))
                return False

            self.initialized = True
            return True

        # If we are the TECController, make sure we're off for now.
        if self.name == "TECController":
            tu = tec_utils.TECUtil()
            success = tu.TECOff(self.devPath)

            self.initialized = success
            return True
        else:
            return False

    def Read(self):
        """
        Override: This read currently clears amy incoming data until none is available,
        It then launches a background thread to continue reading incoming messages.
        :return: None
        """

        # Make sure we know what to do.
        if self.serialPort is None and self.subProc is None:
            return

        # If we're the TECController, start a thread reading shared memory.
        if self.name == "TECController":
            self.stop = False
            self.thread = Thread(target=self.ThreadReadSharedMemory)
            self.thread.start()
            time.sleep(0.25)
            return

        # We're a regular serial device.
        # Clear any old data.
        bytesToRead = self.serialPort.inWaiting()
        while bytesToRead > 0:
            self.serialPort.read(bytesToRead)
            bytesToRead = self.serialPort.inWaiting()

        # Start a thread reading the serial port.
        self.stop = False
        self.thread = Thread(target=self.ThreadRead)
        self.thread.start()
        time.sleep(0.25)

    def ThreadRead(self):
        """
        This is the serial read thread function.  Do not call directly, use Read()
        :return: None
        """
        if self.serialPort is None:
            return

        self.logger.debug("Start reader thread for device: " + self.name)

        # Just read data until we're told to stop.
        while self.stop == False:
            data = ""

            while data.rfind('\n') == -1 and self.stop == False:
                bytesToRead = self.serialPort.inWaiting()
                if bytesToRead > 0:
                    data += self.serialPort.read(bytesToRead)

            if self.stop == True:
                break

            # Remember the last thing read.
            self.lastMsg = data.strip()
            self.logger.debug("Received Data: <" + self.lastMsg + ">")

        self.logger.debug("Exit reader thread for device: " + self.name)

    def ThreadReadPipe(self):
        """
        A pipe read thread function.  Currently not used and not debugged.
        :return: None
        """
        self.logger.debug("Start pipe reader for device on " + self.name)
        while self.stop == False:

            line = self.proc.stdout.readline()
            line = line.strip()
            # self.logger.debug(line)

            if line.startswith('STP0'):
                self.logger.debug(line)

        self.logger.debug("Exit pipe reader for device on " + self.name)

    def StartTECSequence(self, cycles):
        """
        Helper function to start the TEC ThermoCycler Sequence. Essentially starts the
        defined subprocess with the correct arguments.
        :param cycles:
        :return: True on success, false otherwise.
        """
        if self.subProc is not None and len(self.subProc.cmd) > 0:
            self.serialPort = None

            cmd = [self.subProc.cmd]
            for anArg in self.subProc.args:
                cmd.append(anArg)

            # Append number of cycles at the very end.
            cmd.append(str(cycles))

            # Get a /dev/null to send stderr to.
            FNULL = open(os.devnull, 'w')
            self.logger.debug("Starting subprocess:" + str(cmd))
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=FNULL)

            if self.proc is None:
                self.logger.debug("Failed to start process.")
                return False
            # Give the process time to start up before continuing
            time.sleep(5)
            return True

    def ThreadReadSharedMemory(self):
        """
        This is the background thread to read from shared memory.  It is used exclusively by the
        TECController device.
        :return:
        """
        self.logger.debug("Start shared memory reader for device on " + self.name)

        # Get our shared memorm protection semaphore. The name should be the same as used
        # in the TEC Controller subprocess.
        shared_mem_sema = posix_ipc.Semaphore("/tecSMProtection", posix_ipc.O_CREAT)
        # Open our known shared memory.  The name should be the same as used in the TEC Controller subprocess.
        sharedmem = posix_ipc.SharedMemory("tecControllerSM", posix_ipc.O_CREAT | posix_ipc.O_TRUNC, size=128)

        # MMap the shared memory
        mapfile = mmap.mmap(sharedmem.fd, sharedmem.size)
        sharedmem.close_fd()  # Safe to close this.

        # Start with some invalid values.
        blockTemp = -100.0
        sampleTemp = -100.0
        cycle = -1
        step = -1

        # Keep reading until we're told to stop or the subprocess is finished.
        while self.stop == False and self.proc is not None and self.proc.returncode is None:

            # Read from the beginning of shared memory to a new line.
            shared_mem_sema.acquire()
            # with posix_ipc.Semaphore("/tecSMProtection"):
            mapfile.seek(0)
            data = mapfile.readline()
            shared_mem_sema.release()
            data = data.strip()
            # self.logger.debug("SM Data: <" + data + ">")

            # The format of the shared memory is four numbers separated by spaces.
            # They are <block temp> <sample temp> <current cycle number> <current step within cycle>
            if len(data) > 0:
                try:
                    # Parse the shared mem line.
                    parts = data.split()
                    blockTemp = float(parts[0])
                    sampleTemp = float(parts[1])
                    cycle = int(parts[2])
                    step = int(parts[3])

                    # Build an appropriate response to send back to a client.
                    self.lastMsg = ("OK " + str(blockTemp) + " " + str(sampleTemp) +
                                    " " + str(cycle) + " " + str(step))

                    self.logger.debug("Block Temp: " + str(blockTemp) + "  Sample Temp: " + str(sampleTemp) +
                                      "  Cycle: " + str(cycle) + "  Step: " + str(step))


                except Exception, e:
                    self.logger.debug("Bad sm data")
                    pass

            time.sleep(0.5)

            # Check if subprocess is still alive.
            self.proc.poll()

        # All done.  Reset our last message so that requesters don't get stale data.
        self.lastMsg = "FAIL"
        self.logger.debug("Exit shared memory reader for device on " + self.name)

    # Write data to the serial port.
    def Write(self, data):
        """
        Write string data to the serial port for this device.
        :param data:
        :return: None
        """
        if self.serialPort is None:
            return

        msg = ""
        msg += data

        self.logger.debug("Write Data: <" + msg + ">")
        self.serialPort.write(msg)
        time.sleep(0.01)  # Give a bit of delay for the data to go through.

    def GetLastResponse(self):
        """
        Get the last known response from this device.
        :return: Device's last message.
        """

        if self.name == "TECController" and self.proc is None:
            return "FAIL"

        if self.serialPort is None and self.name != "TECController":
            return "FAIL"

        return self.lastMsg
