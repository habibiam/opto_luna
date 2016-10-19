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
    pid = ""
    vid = ""
    uid = ""
    devPath = ""
    portSettings = port_settings.PortSettings()
    serialPort = None
    stop = False
    thread = None
    lastMsg = ""

    subProc = xml_config_subprocess.deviceSubProcess()
    proc = None

    def Shutdown(self):
        if self.thread is not None:
            self.stop = True
            self.thread.join(2.0)
            self.thread = None

        if self.serialPort is not None:
            if self.serialPort.isOpen():
                self.serialPort.close()
            self.serialPort = None

        if self.proc is not None:
            self.proc.terminate()

        if self.name == "TECController":
            tu = tec_utils.TECUtil()
            tu.TECOff(self.devPath)

    # For this type of device, initializing means simply opening a serial
    # connection to the device.
    def InitDevice(self):
        super(USBSerialDevice, self).InitDevice()

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

        if self.name == "TECController":
            tu = tec_utils.TECUtil()
            success = tu.TECOff(self.devPath)

            self.initialized = success
            return True
        else:
            return False

    # This read currently clears the incoming data until none is available,
    # It then launches a background thread to continue reading incoming messages.
    def Read(self):
        if self.serialPort is None and self.subProc is None:
            return

        if self.subProc is not None:
            self.stop = False
            self.thread = Thread(target=self.ThreadReadSharedMemory)
            self.thread.start()
            time.sleep(0.25)
            return

        bytesToRead = self.serialPort.inWaiting()
        while bytesToRead > 0:
            self.serialPort.read(bytesToRead)
            bytesToRead = self.serialPort.inWaiting()

        self.stop = False
        self.thread = Thread(target=self.ThreadRead)
        self.thread.start()
        time.sleep(0.25)

    # This is the thread function.  Do not call directly, use Read()
    def ThreadRead(self):
        if self.serialPort is None:
            return

        self.logger.debug("Start reader thread for device: " + self.name)

        # Just read data until we're told do stop.
        while self.stop == False:
            data = ""

            while data.rfind('\n') == -1 and self.stop == False:
                bytesToRead = self.serialPort.inWaiting()
                if bytesToRead > 0:
                    data += self.serialPort.read(bytesToRead)

            if self.stop == True:
                break

            self.lastMsg = data.strip()
            self.logger.debug("Received Data: <" + self.lastMsg + ">")

        self.logger.debug("Exit reader thread for device: " + self.name)

    def ThreadReadPipe(self):
        self.logger.debug("Start pipe reader for device on " + self.name)
        while self.stop == False:

            line = self.proc.stdout.readline()
            line = line.strip()
            # self.logger.debug(line)

            if line.startswith('STP0'):
                self.logger.debug(line)

        self.logger.debug("Exit pipe reader for device on " + self.name)

    def StartTECSequence(self, cycles):
        if self.subProc is not None and len(self.subProc.cmd) > 0:
            self.serialPort = None

            cmd = [self.subProc.cmd]
            for anArg in self.subProc.args:
                cmd.append(anArg)

            # Append number of cycles at the very end.
            cmd.append(str(cycles))

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
        self.logger.debug("Start shared memory reader for device on " + self.name)
        sharedmem = posix_ipc.SharedMemory("tecControllerSM", posix_ipc.O_CREAT | posix_ipc.O_TRUNC, size=128)

        # MMap the shared memory
        mapfile = mmap.mmap(sharedmem.fd, sharedmem.size)
        sharedmem.close_fd()  # Safe to close this.

        blockTemp = -100.0
        sampleTemp = -100.0
        while self.stop == False:
            mapfile.seek(0)
            data = mapfile.readline()
            data = data.strip()
            # self.logger.debug("SM Data: <" + data + ">")

            if len(data) > 0:
                try:
                    parts = data.split()
                    blockTemp = float(parts[0])
                    sampleTemp = float(parts[1])
                    cycle = int(parts[2])
                    step = int(parts[3])
                    self.lastMsg = ("OK " + str(blockTemp) + " " + str(sampleTemp) +
                                    " " + str(cycle) + " " + str(step))

                    self.logger.debug("Block Temp: " + str(blockTemp) + "  Sample Temp: " + str(sampleTemp) +
                                      "  Cycle: " + str(cycle) + "  Step: " + str(step))


                except Exception, e:
                    self.logger.debug("Bad sm data")
                    pass

            time.sleep(0.5)

        self.logger.debug("Exit shared memory reader for device on " + self.name)

    # Write data to the serial port.
    def Write(self, data):
        if self.serialPort is None:
            return

        msg = ""
        msg += data

        self.logger.debug("Write Data: <" + msg + ">")
        self.serialPort.write(msg)
        time.sleep(0.01)  # Give a bit of delay for the data to go through.

    def GetLastResponse(self):
        return self.lastMsg
