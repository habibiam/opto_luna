SpectroLib Developer Notes
Author:  Chris Lawton, DLSSolutions, Inc. (clawton@dlssolutions.com)
Date:    December 9, 2016

1) Building (Library and Python library)
The SpectroLib project is currently and Eclipse based project.  ultimately it will control the Ibesn Spectrometer via the Digital
Input Sensor Board (DISB).  To build, import the SpectroLib project into your C++ eclipse environment. If you're not using eclipse,
you will need to include all the source files (both .c and .cpp) and then set the proper include and library path folders.  
The "DLNXXX()" functions can be found under the DLNWare folder.  In addition to linking with the libdln.a, you also need to link
with QtCore as the DLN people used it for their threading model.

1a) Building the static library
Note that the eclipse project will only build the static library, SpectroLib.a

1b) To build the python callable module (aka a shared lib), SpectroLib_module.so, you need to run the python setup.py script.
Note that you need to have the python development environment installed: sudo apt-get install python-dev
To build our module, run the following command: python setup.py build_ext --inplace

2) Running
See the sample script, test.py in this folder.
Note that in order to run successfully, you need to have started the dln_srv process prior to connecting the spectrometer!

Run the script via: python test.py 

