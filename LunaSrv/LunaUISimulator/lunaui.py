import subprocess
import sys
import os




def printmenu():
    os.system('clear')
    print ""
    print "----------Available Commands----------"
    print " 1\tInventory Devices"
    print " 2\tGet Power Supply Voltage"
    print " 3\tSet Power Supply Voltage"
    print " 4\tStart Thermo Cycler Sequence"
    print " 5\tAbort Thermo Cycler Sequence"
    print " 6\tRead Thermo Cycler Sequence Data"
    print " 7\tRead OBIS Laser Power"
    print " 8\tTurn OBIS Laser ON"
    print " 9\tTurn OBIS Laser OFF"
    print " 10\tSet OBIS Laser Power"
    print " 11\tSet Fluid VALVE Position"
    print " 12\tSet Spectrometer Exposure time"
    print " 13\tStart Spectrometer Continuous Capture"
    print " 14\tCheck if Continuous Capture is running"
    print " 0\tQuit"
    
    sys.stdout.write("Select Command: ")
    sys.stdout.flush()
    
 
def getChoice():
    c = getUserInt()
    if c >= 0:
        return c
    else:
        print "Invalid Choice"
        printmenu()
                
def getUserInt():
    while True:
        line = sys.stdin.readline()
        line = line.strip()
        if len(line) > 0:
            c = int(line)
            return c

def getUserFloat():
    while True:
        line = sys.stdin.readline()
        line = line.strip()
        if len(line) > 0:
            c = float(line)
            return c

def getUserString():
    while True:
        line = sys.stdin.readline()
        line = line.strip()
        if len(line) > 0:
            return line


def doInventory(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": "", "cmd": "INVTHW", "args": "" }
    proc.stdin.write(cmd)
    proc.stdin.flush()
    
def doGETVI(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": "HighVoltageSupply", "cmd": "GETVI", "args": "" }
    proc.stdin.write(cmd)
    proc.stdin.flush()

def doSETV(cnum):
    sys.stdout.write("  Voltage: ")
    sys.stdout.flush()
    f = getUserFloat()
    
    size = 94 + len(str(f)) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": "HighVoltageSupply", "cmd": "SETV", "args": f }
    proc.stdin.write(cmd)
    proc.stdin.flush()
    
def doSHUTDOWN(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
        {"cnum": cnum, "size": size, "deviceName": "", "cmd": "SHUTDOWN", "args": "" }
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doSTARTSEQ(cnum):
    sys.stdout.write("  Number of Cycles:")
    sys.stdout.flush()
    i = getUserInt()

    size = 94 + len(str(i)) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "TECController", "cmd": "STARTSEQ", "args": i}
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doSTOPSEQ(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "TECController", "cmd": "STOPSEQ", "args": ""}
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doREADSEQD(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "TECController", "cmd": "READSEQD", "args": ""}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def doGETLPWR(cnum):
    size = 94
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "OBISLaser", "cmd": "GETLPWR", "args": ""}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def doSETLSTATE(cnum, state):
    size = 94 + len(state)
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "OBISLaser", "cmd": "SETLSTATE", "args": state}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def doSETLPWR(cnum):
    sys.stdout.write("  Power: ")
    sys.stdout.flush()
    f = getUserFloat()

    size = 94 + len(str(f)) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "OBISLaser", "cmd": "SETLPWR", "args": f}
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doFVALVEPOS(cnum):
    sys.stdout.write("  Position:\n")
    sys.stdout.write("  1\tA\n")
    sys.stdout.write("  2\tCLOSED\n")
    sys.stdout.write("  3\tB\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    p = getUserInt()
    pos = ""
    if p == 1:
        pos = "A"
    elif p == 2:
        pos = "CLOSED"
    elif p == 3:
        pos = "B"
    else:
        return


    size = 94 + len(str(pos)) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "FluidValve", "cmd": "FVALVEPOS", "args": pos}
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doSPCSETEXP(cnum):
    sys.stdout.write("  Exposure Time: ")
    sys.stdout.flush()
    exp = getUserInt()

    size = 94 + len(str(exp)) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "Spectrometer", "cmd": "SPCSETEXP", "args": exp}
    proc.stdin.write(cmd)
    proc.stdin.flush()


def doSPCSTARTC(cnum):
    sys.stdout.write("  Filename: ")
    sys.stdout.flush()
    filename = getUserString()

    sys.stdout.write("  Time Between Captures (ms): ")
    sys.stdout.flush()
    delayMS = getUserInt()

    sys.stdout.write("  Capture Duration (ms): ")
    sys.stdout.flush()
    durationMS = getUserInt()

    args = filename + " " + str(delayMS) + " " + str(durationMS)

    size = 94 + len(args) + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "Spectrometer", "cmd": "SPCSTARTC", "args": args}
    proc.stdin.write(cmd)
    proc.stdin.flush()

def doSPCISCRUN(cnum):
    size = 94 + 1
    cmd = '%(cnum)010d%(size)010d%(deviceName)-64s%(cmd)-10s%(args)s\n' % \
          {"cnum": cnum, "size": size, "deviceName": "Spectrometer", "cmd": "SPCISCRUN", "args": ""}
    proc.stdin.write(cmd)
    proc.stdin.flush()



if __name__ == '__main__':
    cnum = 1

    path = os.path.dirname(os.path.abspath(__file__))
    path += "/../"

    cmd = ["/usr/bin/python", "-u", path + "lunasrv.py"]
    proc = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    while (1):
        printmenu()
        choice = getChoice()
    
        if choice == 0:
            doSHUTDOWN(cnum)
            w = proc.wait()
            if w is None:
                proc.terminate()
            sys.exit(0)
            
        if choice == 1:
            doInventory(cnum)
            cnum += 1
            
        if choice == 2:
            doGETVI(cnum)
            cnum += 1

        if choice == 3:
            doSETV(cnum)
            cnum += 1

        if choice == 4:
            doSTARTSEQ(cnum)
            cnum += 1

        if choice == 5:
            doSTOPSEQ(cnum)
            cnum += 1

        if choice == 6:
            doREADSEQD(cnum)
            cnum += 1

        if choice == 7:
            doGETLPWR(cnum)
            cnum += 1

        if choice == 8:
            doSETLSTATE(cnum, "ON")
            cnum += 1

        if choice == 9:
            doSETLSTATE(cnum, "OFF")
            cnum += 1

        if choice == 10:
            doSETLPWR(cnum)
            cnum += 1

        if choice == 11:
            doFVALVEPOS(cnum)
            cnum += 1

        if choice == 12:
            doSPCSETEXP(cnum)
            cnum += 1

        if choice == 13:
            doSPCSTARTC(cnum)
            cnum += 1

        if choice == 14:
            doSPCISCRUN(cnum)
            cnum += 1