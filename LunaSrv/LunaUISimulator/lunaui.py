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