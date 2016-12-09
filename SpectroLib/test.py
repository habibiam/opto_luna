from SpectroLib_module import *
import time


Initialize()
print GetLastErrorMsg()

print ReadSerialNumber()
print GetLastErrorMsg()

SetExposureMS(250)
print GetLastErrorMsg()

spectrum = CaptureSingleSpectrum()
print spectrum

CaptureContinuousSpectrum("chris.csv", 0, 5000)
done = IsCaptureContinuousSpectrumDone()
while done != 1:
    time.sleep(0.5)
    done = IsCaptureContinuousSpectrumDone()

print GetLastErrorMsg()
