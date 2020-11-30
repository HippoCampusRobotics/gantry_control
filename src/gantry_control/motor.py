import serial
import abc


class BaseMotor(object):
    GET_POSITION = "POS"
    GET_TARGET_VELOCITY = "GN"
    SET_POSITION_ABSOLUTE = "LA"
    SET_POSITION_RELATIVE = "LR"
    MOVE_POSITION = "M"

    START_HOMING = "GOHOSEQ"
    SET_HOME = "HO"
    SET_MAX_VELOCITY = "SP"
    GET_MAX_VELOCITY = "GSP"
    SET_ACCELERATION = "AC"
    GET_ACCELERATION = "GAC"

    SET_VELOCITY = "V"
    GET_TARGET_VELOCITY = "GV"
    GET_VELOCITY = "GN"
    __metaclass__ = abc.ABCMeta

    def __init__(self, port, baud, timeout):
        self.port = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    def _send_command(self, command, arg=""):
        self.port.write(b"{}{}\r".format(command, arg))

    def _read_answer(self):
        return self.port.readline().rstrip()

    def _get_int(self, command, arg=""):
        self._send_command(command, arg)
        ans = self._read_answer()
        success = True
        try:
            value = int(ans)
        except ValueError:
            value = 0
            success = False
        return success, value

    def get_position(self):
        """Reads the current position of the motor.

        Returns:
            (bool, int): Returns success flag and position of motor in
                increments.
        """
        (success, position) = self._get_int(self.GET_POSITION)
        return success, position

    def set_position_target(self, position, relative=False):
        """Sets a new target position either as absolute or relative value.

        Args:
            position (int): Position in increments.
            relative (bool, optional): Flag that indicates, if target position
                is relative. Defaults to False.
        """
        if relative:
            self._send_command(self.SET_POSITION_RELATIVE)
        else:
            self._send_command(self.SET_POSITION_ABSOLUTE)

    def start_homing(self):
        self._send_command(self.START_HOMING)

    def set_home(self, position=0):
        """Sets the actual position to the given value.

        Args:
            position (int, optional): Position in increments. Defaults to 0.
        """
        self._send_command(self.SET_HOME, int(position))

    def set_velocity(self, velocity):
        """Moves the motor with the given velocity.

        Args:
            velocity (int): Velocity in RPM.
        """
        self._send_command(self.SET_VELOCITY, int(velocity))

    def get_velocity(self):
        """Gets the current velocity.

        Returns:
            (bool, int): Returns success flag and current velocity in RPM.
        """
        (success, velocity) = self._get_int(self.GET_VELOCITY)
        return success, velocity

    def get_target_velocity(self):
        """Gets the target velocity.

        Returns:
            (bool, int): Returns success flag and target velocity in RPM.
        """
        (success, velocity) = self._get_int(self.GET_TARGET_VELOCITY)
        return success, velocity

    def move_to_target_position(self, position=None, relative=False):
        """Moves to the specified position.

        Args:
            position (int, optional): Sets a new target position if not None.
                Defaults to None.
            relative (bool, optional): Indicates if position is relative or
                absolute. Defaults to False.
        """
        if position is not None:
            if relative:
                self._send_command(self.SET_POSITION_RELATIVE, position)
            else:
                self._send_command(self.SET_POSITION_ABSOLUTE, position)
        self._send_command(self.MOVE_POSITION)

    def set_max_velocity(self, value):
        """Sets the maximal velocity for position control mode.

        Args:
            value (int): Maxmimal velocity in RPM of the motor.
        """
        self._send_command(self.SET_MAX_VELOCITY, int(value))

    def get_max_velocity(self):
        """Gets the maximal velocity for position control mode.

        Returns:
            (bool, int): Success flag and maximal velocity in RPM of the motor.
        """
        (success, velocity) = self._get_int(self.GET_MAX_VELOCITY)
        return success, velocity

    def set_acceleration(self, value):
        """Sets the acceleration.

        Args:
            value (int): Acceleration in Rev/s^2.
        """
        self._send_command(self.SET_ACCELERATION, int(value))

    def get_acceleration(self):
        """Gets the acceleration.

        Returns:
            (bool, int): Success flag and acceleration in Rev/s^2.
        """
        (success, acceleration) = self._get_int(self.GET_ACCELERATION)
        return success, acceleration

    @abc.abstractmethod
    def is_homing(self):
        """Checks if the motor is currently homing.

        Returns:
            bool: Returns True if homing. Otherwise False will be returned.
        """
        pass
