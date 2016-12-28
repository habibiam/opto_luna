"""
Author: Kevin Kim
FSM in python, specifically used for Luna M

"""

class FSM(object):
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None # or self.curState = initalState, and initalize the FSM to 'off' state.
        self.prevState = None # USE TO PREVENT LOOPING 2 STATE, didn't implement here but should implement for more complex FSM
        self.trans = None

    """ """
    def AddTransition(self, transName, transition):
        """
        Cleaner way to add objects to dictionaries
        :param transName:
        :param transition:
        :return:
        """
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        """
        Cleaner way to add objects to dictionaries

        Can put states and transitions in, but cannot modify them.
        :param stateName:
        :param state:
        :return:
        """
        self.states[stateName] = state

    def SetState(self, stateName):
        """
        This time store prevState as curState and then pass in curState
        :param stateName:
        :return:
        """
        self.prevState = self.curState
        self.curState = self.states[stateName]

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def Execute(self):
        """
        Checks to see if self.trans is set. If it is set, then
        :return:
        """
        if self.trans:
            self.curState.Exit()                    # Call the Exit function of the current state
            self.trans.Execute()                    # Get the current transition function
            self.SetState(self.trans.toState)       # set the state to the transition's target state
            self.curState.Enter()                   # Call the enter function of the current state because it's been switched over to the new state
            self.trans = None                       # finally set the trans to None
        self.curState.Execute()                     # Lastly, execute the current function.

