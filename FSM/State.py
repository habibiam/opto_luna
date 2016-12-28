from random import randint
from time import clock

import logging
import string
from LUNA_FSM import FSM

##==================== Logging Configuration ==========================
FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

##==================== STATES ==========================

class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
        self.timer = 0
        self.startTime = 0


    def __str__(self):
        pass


    def Enter(self):
        """

        :return:
        """
        self.timer = randint(0, 5)
        self.startTime = int(clock())

    def Execute(self):
        """

        :return:
        """
        pass

    def Exit(self):
        """

        :return:
        """
        pass

##==================== ACTUAL STATES ==========================
class SystemOff(State):
    """
    2.0 SystemOff
    This state is just the start the state.
    """
    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(SystemOff, self).__init__(FSM)

    def __str__(self):
        return "SystemOff"

    def Enter(self):
        logging.info("enter SystemOff")
        super(SystemOff, self).Enter()


    def Execute(self):
        """
        State Off execution.
        When the machine turns on, transitions from poweroff --> SystemStartup
        :return:
        """
        logging.info("System is Off")
        # No matter states going form system off to system startup.
        switch = raw_input("Would you like to turn on machine? (y/n)")
        if switch == 'y':
            self.FSM.ToTransition("toSystemStartup")
        else:
            pass


    def Exit(self):
        logging.info("exit systemOff")



class SystemStartup(State):
    def __init__(self, FSM):
        """
        2.1 System Startup

        From:
        1) Systemoff (U) / turn_on_clicked()
        2) Stopped (U) / restart_clicked()
        To:
        1) Initialize Reagents (S) / system_Startup_finished()
        2) Stopped (S) / error()
        3) Shutting Down (S) / power_loss() or (U) / shutdown_clicked()
        """
        super(SystemStartup, self).__init__(FSM)

    def __str__(self):
        return "SystemStartup"

    def Enter(self):
        logging.info("SystemStartup enter")
        super(SystemStartup, self).Enter()

    def Execute(self):
        """
        Have a condition in order to check if we need to transition into another state.
        Randomly choose if the robot is going to to Vacuum or go to sleep.
        :return:
        """
        logging.info("System is in SystemStart State")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,2)
            if (rand_num) == 0:
                # system_startup_finished() / S
                logging.debug("system_startup_finished()")
                self.FSM.ToTransition("toInitializedReagents")
            elif (rand_num == 1):
                # error() / S
                logging.debug("error()")
                self.FSM.ToTransition("toStopped")
            elif (rand_num == 2):
                # user_clicked_shutdown() / U
                logging.debug("user_clicked_shutdown()")
                self.FSM.ToTransition("toShuttingDown")

    def Exit(self):
        logging.info("System Startup exit")


class InitializeReagent(State):
    """
    2.2 Initialize Reagent State

    From:
    1) System Startup (S) / system_startup_finalized()
    2) Running (S) / run_finished()
    To:
    1) Ready (S) / reagents_checked()
    2) Stopped (S) / error()
    3) Shutting Down (U) / shutdown_clicked()
    """
    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(InitializeReagent, self).__init__(FSM)

    def __str__(self):
        return "InitalizeReagent"

    def Enter(self):
        logging.info("enter")

    def Execute(self):
        logging.info("System is Initialize Reagent")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,2)
            if (rand_num) == 0:
                # reagents_checked() / S
                logging.debug("reagents_checked()")
                self.FSM.ToTransition("toReady")
            elif (rand_num == 1):
                # error() / S
                logging.debug("error()")
                self.FSM.ToTransition("toStopped")
            elif (rand_num == 2):
                # shutdown_clicked() / U
                logging.debug("shutdown_clicked()")
                self.FSM.ToTransition("toShuttingDown")

    def Exit(self):
        logging.info("exit")


class Ready(State):
    """
    2.3 Ready State

    From:
    1) Initialize Reagents (S) / reagents_checked()
    To:
    1) Running (U) / start_run_clicked()
    2) Stopped (S) / error() or (U) stop_run_clicked()
    3) Shutting Down (S) / power_loss() or (U) / shutdown_clicked()
    """

    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(Ready, self).__init__(FSM)

    def __str__(self):
        return "Ready"

    def Enter(self):
        logging.info("enter")

    def Execute(self):
        logging.info("System is Ready")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,2)
            if (rand_num) == 0:
                # start_run_clicked() / U
                logging.debug("start_run_clicked()")
                self.FSM.ToTransition("toRunning")
            elif (rand_num == 1):
                # error() / S
                logging.debug("error()")
                self.FSM.ToTransition("toStopped")
            elif (rand_num == 2):
                # shutdown_clicked() / U
                logging.debug("shutdown_clicked()")
                self.FSM.ToTransition("toShuttingDown")

    def Exit(self):
        logging.info("exiting Ready State")

class Running(State):
    """
    2.4 Running

    From:
    1) Ready (S) / start_run()
    To:
    1) Initialize Reagents (S) / run_complete()
    2) Stopped (S) / error() or (U) stop_run_clicked()
    3) Shutting Down (S) / power_loss()                 (or (U) / shutdown_clicked())
    """

    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(Running, self).__init__(FSM)

    def __str__(self):
        return "Running"

    def Enter(self):
        logging.info("enter")

    def Execute(self):
        logging.info("System is Ready")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,2)
            if (rand_num) == 0:
                # run_complete() / S
                logging.debug("run_complete()")
                self.FSM.ToTransition("toInitializedReagents")
            elif (rand_num == 1):
                # error() / S
                logging.debug("error()")
                self.FSM.ToTransition("toStopped")
            elif (rand_num == 2):
                # stop_run_clicked() / U
                logging.debug("stop_run_clicked()")
                self.FSM.ToTransition("toStopped")

    def Exit(self):
        logging.info("exit running")

class Stopped(State):
    """
    2.5 Stopped

    From:

    To:

    """

    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(Stopped, self).__init__(FSM)

    def __str__(self):
        return "Stopped"

    def Enter(self):
        logging.info("Stopped State enter")
        super(Stopped, self).Enter()

    def Execute(self):
        """
        Have a condition in order to check if we need to transition into another state.
        Randomly choose if the robot is going to to Vacuum or go to sleep.
        :return:
        """
        logging.info("System is Stopped")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,1)
            if (rand_num) == 0:
                # shutdown_clicked() / User
                logging.debug("shutdown_clicked()")
                self.FSM.ToTransition("toShuttingDown")
            elif (rand_num == 1):
                # restart_clicked() / User
                logging.debug("restart_clicked()")
                self.FSM.ToTransition("toSystemStartup")

    def Exit(self):
        logging.info("exiting from STOPPED")


class ShuttingDown(State):
    """
    2.6 Shutting Down

    From:

    To:

    """

    def __init__(self, FSM):
        """
        Going to as a FSM to be passed into the state constructor so that we can make adjustments and grab data
        from it.

        :param FSM:
        """
        super(ShuttingDown, self).__init__(FSM)

    def __str__(self):
        return "ShuttingDown"

    def Enter(self):
        logging.info("enter")

    def Execute(self):
        logging.info("System is Shutting Down")
        if self.startTime + self.timer <= clock():
            rand_num = randint(0,0)
            if (rand_num) == 0:
                # system_startup_finished() / S
                self.FSM.ToTransition("toPowerOff")
            elif (rand_num == 1):
                # restart_clicked() / S
                self.FSM.ToTransition("toStopped")

    def Exit(self):
        logging.info("exit from Shutting down")

