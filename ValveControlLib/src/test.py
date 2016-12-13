from ValveControlLib_module import *

Initialize("/dev/ttyUSB0")
print GetLastErrorMsg()

print GetStatus()

ret = SetPosition(STATE_A)
if ret == 0:
    #failed
    print GetLastErrorMsg()
    
print GetStatus()

SetPosition(STATE_CLOSED)
print GetStatus()

SetPosition(STATE_B)
print GetStatus()

