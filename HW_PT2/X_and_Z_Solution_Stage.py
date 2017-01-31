"""
X anx Z Solution Stage class

"""
from pimain import *
class Motor:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def done_response(self):
        """
        Sends a response back to port
        :return:
        """

class X_and_Z_Solution_Stage:

    def __init__(self):
        self._running = True
        with open('stage_x_z_absolute_position.json') as f:
            self.stage_x_and_z_pos = json.load(f)
        # Need to check z first, then x
        """
        if (self.stage_x_and_z_pos["z_pos"] !=0):
            print "Moving Stage Z Home"
            target_motor = xyz_motor(2, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(POSDIR, self.stage_x_and_z_pos["z_pos"], MICROSTEP, HIGHCUR)  # POSDIR makes Stage Z go down
            self.stage_x_and_z_pos["z_pos"] -= self.stage_x_and_z_pos["z_pos"]
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
        if (self.stage_x_and_z_pos["x_pos"] != 0):
            print "Moving Stage X HOME"
            target_motor = xyz_motor(6, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(NEGDIR, self.stage_x_and_z_pos["x_pos"], MICROSTEP,
                              HIGHCUR)  # To move from big to big vial, increment is 4500
            self.stage_x_and_z_pos["x_pos"] -= self.stage_x_and_z_pos["x_pos"]
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
        """
        self.z_stage_move_step = 6600  # 6000
        self.x_stage_move_step_big = 4500  # 4500
        self.x_stage_move_step_small = 4000  # 4000

        self.sample_abs_pos = 3100  # 3100
        self.buffer_abs_pos = self.sample_abs_pos + self.x_stage_move_step_small  # 7100
        self.water_abs_pos = self.buffer_abs_pos + self.x_stage_move_step_big  # 11600
        self.waste_abs_pos = self.water_abs_pos + self.x_stage_move_step_big  # 16100

    def terminate(self):
        self._running = False

    def check_stage_z_is_down(self):
        """
        check to see if stage z is down.
        If it's not down, then stage z will move down.
        Use this function to check stage z is down whenever moving stage x (Either relative or absolute)
        :return:
        """
        if self.stage_x_and_z_pos["z_pos"] > 0:
            print "Moving Stage Z DOWN FIRST"
            target_motor = xyz_motor(2, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(POSDIR, self.z_stage_move_step, DOUBLECOILMICROSTEP,
                              XZSTATIONCUR)  # POSDIR makes Stage Z go down
            self.stage_x_and_z_pos["z_pos"] -= self.z_stage_move_step
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)

    """
    Relative Positions
    """
    def move_stageX_left_small(self):
        """

        :return:
        """
        self.check_stage_z_is_down()
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        target_motor.move(NEGDIR, self.x_stage_move_step_small, DOUBLECOILMICROSTEP,
                          XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
        self.stage_x_and_z_pos["x_pos"] -= self.x_stage_move_step_small
        with open('stage_x_z_absolute_position.json', 'w') as wf:
            json.dump(self.stage_x_and_z_pos, wf)
        port.write("done  \n")

    def move_stageX_right_small(self):
        """

        :return:
        """
        self.check_stage_z_is_down()
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        target_motor.move(POSDIR, self.x_stage_move_step_small, DOUBLECOILMICROSTEP,
                          XZSTATIONCUR)  # To move from big to small vial or vice versa, increment is 4000
        self.stage_x_and_z_pos["x_pos"] += self.x_stage_move_step_small
        with open('stage_x_z_absolute_position.json', 'w') as wf:
            json.dump(self.stage_x_and_z_pos, wf)
        port.write("done   \n")

    def move_stageX_left_big(self):
        """

        :return:
        """
        self.check_stage_z_is_down()
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        target_motor.move(NEGDIR, self.x_stage_move_step_big, DOUBLECOILMICROSTEP,
                          XZSTATIONCUR)  # To move from big to big vial, increment is 4500
        self.stage_x_and_z_pos["x_pos"] -= self.x_stage_move_step_big
        with open('stage_x_z_absolute_position.json', 'w') as wf:
            json.dump(self.stage_x_and_z_pos, wf)
        port.write("done   \n")


    def move_stageX_right_big(self):
        """

        :return:
        """
        self.check_stage_z_is_down()
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        target_motor.move(POSDIR, self.x_stage_move_step_big, DOUBLECOILMICROSTEP,
                          XZSTATIONCUR)  # To move from big to big vial, increment is 4500
        self.stage_x_and_z_pos["x_pos"] += self.x_stage_move_step_big
        with open('stage_x_z_absolute_position.json', 'w') as wf:
            json.dump(self.stage_x_and_z_pos, wf)
        port.write("done   \n")

    def move_stageZ_up(self):
        """
        Moves stage z up by self.z_stage_move_step
        :return:
        """
        if self.stage_x_and_z_pos["z_pos"] >= self.z_stage_move_step:
            print "Stage z is already at the top"
            port.write("done   \n")
            print "sent done to port"
        else:
            print "Moving Stage Z UP"
            target_motor = xyz_motor(2, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(NEGDIR, self.z_stage_move_step, DOUBLECOILMICROSTEP,
                              XZSTATIONCUR)  # NEGDIR makes Stage Z go up
            self.stage_x_and_z_pos["z_pos"] += self.z_stage_move_step
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
            port.write("done   \n")
            print "sent done to port"

    def move_stageZ_down(self):
        """
        Moves stage z down by self.z_stage_move_step
        :return:
        """
        if self.stage_x_and_z_pos["z_pos"] <= 0:
            print "Stage z is already at the very bottom"
            port.write("done   \n")
            print "sent done to port"
        else:
            print "Moving Stage Z DOWN"
            target_motor = xyz_motor(2, 200, 100)
            atexit.register(target_motor.turn_off)
            target_motor.move(POSDIR, self.z_stage_move_step, DOUBLECOILMICROSTEP,
                              XZSTATIONCUR)  # POSDIR makes Stage Z go down
            self.stage_x_and_z_pos["z_pos"] -= self.z_stage_move_step
            with open('stage_x_z_absolute_position.json', 'w') as wf:
                json.dump(self.stage_x_and_z_pos, wf)
            port.write("done   \n")
            print "sent done to port"


    """
    Absolute Positions
    """
    def move_absolute(self, move_to):
        """
        Moves X stage to the absolute position and updates the json file once moved.
        :param move_to: int - Should be a self.*_abs_pos local variable.
        :return:
        """
        target_motor = xyz_motor(6, 200, 100)
        atexit.register(target_motor.turn_off)
        current_x_pos = self.stage_x_and_z_pos["x_pos"]
        relative_steps = abs(move_to - current_x_pos)
        # Check current position relative to move_to position
        if current_x_pos < move_to:  # if current_x_pos == 0, 3500
            target_motor.move(POSDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
        elif current_x_pos > move_to:  # if current_x_pos == 12000, 16500
            target_motor.move(NEGDIR, relative_steps, DOUBLECOILMICROSTEP, XZSTATIONCUR)
        # update the json file
        self.stage_x_and_z_pos["x_pos"] = move_to
        with open('stage_x_z_absolute_position.json', 'w') as wf:
            json.dump(self.stage_x_and_z_pos, wf)

    def move_to_sample(self):
        self.check_stage_z_is_down()
        self.move_absolute(move_to=self.sample_abs_pos)
        port.write("done   \n")
        print "sent done to port"

    def move_to_buffer(self):
        self.check_stage_z_is_down()
        self.move_absolute(move_to=self.buffer_abs_pos)
        port.write("done   \n")
        print "sent done to port"

    def move_to_water(self):
        self.check_stage_z_is_down()
        self.move_absolute(move_to=self.water_abs_pos)
        port.write("done   \n")
        print "sent done to port"

    def move_to_waste(self):
        self.check_stage_z_is_down()
        self.move_absolute(move_to=self.waste_abs_pos)
        port.write("done   \n")
        print "sent done to port"



