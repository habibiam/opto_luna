"""
Example of a state machine for a light bulb
"""
from random import randint
from time import clock

State = type("State", (object,), {})

##==================== STATES ==========================
class LightOn(State):
    def Execute(self):
        print "Light is On!"


class LightOff(State):
    def Execute(self):
        print "Light is Off!"

##==================== TRANSITION ==========================

class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print "Transitioning..."

##==================== State Machine ==========================
class SimpleFSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {} # Store all of the states here
        self.transitions = {} # Store all of the transition here.
        self.curState = None # Current State
        self.trans = None # Trnasition

    def SetState(self, stateName):
        """
        Function will look
        :param stateName:
        :return:
        """
        self.curState = self.states[stateName]

    def Transition(self, transName):
        self.trans = self.transitions[transName]

    def Execute(self):
        """
        If there is a transition stored in self.trans, then
        :return:
        """
        if (self.trans):
            self.trans.Execute() # going to execute the transition
            self.SetState(self.trans.toState) # set the current state to whatever that transition is to
            self.trans = None # Then reset self.trans to None
        self.curState.Execute() # Finally, going to execute the current state.

##==================== Character Class ==========================
class Char(object):
    def __init__(self):
        """
        Hold all the character attributes and properties (i.e. Lightbulb)
        Also need to put the FSM in this class
        """
        self.FSM = SimpleFSM(self)
        self.LightOn = True

##==================== Create and run this program ==========================

if __name__=="__main__":
    light = Char() # Create an instance of the character
    # Created an instance of the light on state, that we declared up above,
    light.FSM.states["On"] = LightOn()
    light.FSM.states["Off"] = LightOff()
    # Create transitions
    # This "On" matches with the state that we declared for state two lines above
    light.FSM.transitions["toOn"] = Transition("On")
    light.FSM.transitions["toOff"] = Transition("Off")
    # Set the initial state of the FSM
    light.FSM.SetState("On")
    # Main program that's going to run this
    for i in range(20):
        """
        Run through this program/simulation 20 times, record the starting time and the time Interval
        """
        startTime = clock()
        timeInterval = 1
        while(startTime + timeInterval > clock()):
            # While clock has not passed one second, we are gonna loop around it, otherwise continue.
            pass
        # This random integer, 0 or 1. If it's 0, then going to skip over the if statement, if it's one, then it's
        # true so will execute the if statement
        if randint(0,2):
            if light.LightOn:
                # If light is currently on, we are going to transition to off, and the
                light.FSM.Transition("toOff")
                light.LightOn = False
            else:
                light.FSM.Transition("toOn")
                light.LightOn = True
        light.FSM.Execute()






