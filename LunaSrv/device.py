import logbase

# Base class for all devices
# It is expected that derived classes will override the functions.
class Device(logbase.LogBase):
    name = ""
    inventoried=False  # set to true when a device is found
    initialized=False  # set to true when a device is successfully initialized
    checked=False      # set to true when a device was found 
    stop=False

    def InitDevice(self):
        self.logger.debug("Initialize Device...")
        
    def Read(self):
        pass
        
    def Write(self, data):
        pass
    
    def Shutdown(self):
        pass
    
    def GetLastResponse(self):
        pass
     
        