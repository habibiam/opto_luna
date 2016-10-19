import logbase
import serial


# Base class for all devices
# It is expected that derived classes will override the functions.
class TECUtil(logbase.LogBase):
    bst = ['*', '1', '0', '0', '0', '0', '0', '2', '1', '\r']  # 0 output
    buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def TECOff(self, serialPortName):
        try:
            self.logger.debug("Turn TEC off ....")
            ser = serial.Serial(serialPortName, 115200, timeout=1)
            for pn in range(0, 10):
                ser.write((self.bst[pn]))
            for pn in range(0, 8):
                self.buf[pn] = ser.read(1)
                #print(buf[pn])
            ser.close()
            temp1 = self.hexc2dec(self.buf)
            self.logger.debug("TEC Temp at TECOff: " + str(temp1 / 10.0))
            return True
        except Exception, e:
            self.logger.debug("Error communicating with TEC device.")
            return False

    def hexc2dec(self, bufp):
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



