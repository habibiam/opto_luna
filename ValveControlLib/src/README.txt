ValveControlLib Developer Notes
Author:  Chris Lawton, DLSSolutions, Inc. (clawton@dlssolutions.com)
Date:    December 12, 2016

1) Building (Library and Python library)
The ValveControlLib project is currently an Eclipse based project.  Ultimately it will control the LabSmith AV2011-T116 fluid valve.  
IMPORTANT NOTE: IT IS ASSUMED THAT THERE IS ONE AND ONLY ONE VALVE CONNECTED TO THE SYSTEM! IF MORE ARE ADDED, THIS API WILL
NEED UPDATING.

To build, import the ValveControlLib project into your C++ eclipse environment. If you're not using eclipse,
you will need to include all the source files (both .c and .cpp) and then set the proper include and library path folders.  


1a) Building the static library
Note that the eclipse project will only build the static library, ValveControlLib.a

1b) To build the python callable module (aka a shared lib), ValveControlLib_module.so, you need to run the python setup.py script.
Note that you need to have the python development environment installed: sudo apt-get install python-dev
To build our module, run the following command: python setup.py build_ext --inplace

2) Running
See the sample script, test.py in this folder.

Run the script via: python test.py 

