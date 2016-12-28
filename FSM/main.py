
from State import *
from Character import LunaSrv

##==================== Main ==========================
if __name__=="__main__":
    l = LunaSrv() # Create an instance of the RobotMaid
    for i in range(20):
        startTime = clock()
        timeInterval = 1
        while(startTime+timeInterval > clock()): # MAKES SURE TO WAIT ONE SECOND so that it executes literally every second
            pass
        # print i
        l.Execute()
