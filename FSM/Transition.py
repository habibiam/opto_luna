##==================== TRANSITION ==========================

import logging

FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

## Base Transition Class
class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        # print "Transitioning..."
        logging.info("Transitioning to... %s", self.toState)

## Base Transition Class
class Restart_Clicked(Transition):
    def __init__(self, FSM):
        super(Restart_Clicked, self).__init__(FSM)

    def Execute(self):
        pass