"""
Module: logbase.py
Author: Chris Lawton, DLS Solutions, Inc.
Description:  Contains the class that other classes my derive from that will provide
logging to that derived class.
"""

import logging

class LogBase(object):
    """
    Class to provide logging facilities.  Based on the python logging module.
    """
    @property
    def logger(self):
        """
        Get the current logger but with the its name set to the using class.
        :return: logger
        """
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)