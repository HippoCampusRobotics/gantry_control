import serial


class Result(object):
    def __init__(self, success=False, value=None, message=None):
        self.success = success
        self.value = value
        if message is not None:
            self.message = message
        else:
            self.message = ""


class BaseMotor(object):
    """A base class providing an API for the Faulhaber motors of the gantry.

    Args:
        port (str): Name of the motor's serial port.
        baud (int): Baud of the motor's serial interface.
        timeout (float): Timeout for the serial interface.
    """
    ENABLE = "EN"
    DISABLE = "DI"
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
    SET_DECELERATION = "DEC"
    GET_DECELERATION = "GDEC"

    GET_TYPE = "GTYP"
    GET_SERIAL = "GSER"

    GET_IO_CONFIG = "IOC"

    SET_VELOCITY = "V"
    GET_TARGET_VELOCITY = "GV"
    GET_VELOCITY = "GN"

    def __init__(self, port, baud, timeout):
        self.port = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    def _send_command(self, command, arg=""):
        s = f"{command}{arg}\r"
        self.port.write(s.encode())

    def _read_answer(self):
        return self.port.readline().rstrip().decode()

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

    def get_type(self):
        self._send_command(self.GET_TYPE)
        return self._read_answer()

    def get_serial(self):
        self._send_command(self.GET_SERIAL)
        return self._read_answer()

    def enable(self):
        self._send_command(self.ENABLE)

    def disable(self):
        self._send_command(self.DISABLE)

    def get_position(self):
        """Reads the current position of the motor.

        Returns:
            (Result): Success flag and position in motor increments.
        """
        (success, position) = self._get_int(self.GET_POSITION)
        result = Result(success=success, value=position)
        return result

    def set_position_target(self, position, relative=False):
        """Sets a new target position either as absolute or relative value.

        Args:
            position (int): Position in increments.
            relative (bool, optional): Flag that indicates, if target position
                is relative. Defaults to False.
        """
        if relative:
            self._send_command(self.SET_POSITION_RELATIVE, position)
        else:
            self._send_command(self.SET_POSITION_ABSOLUTE, position)

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
            (Result): Returns success flag and current velocity in RPM.
        """
        (success, velocity) = self._get_int(self.GET_VELOCITY)
        return Result(success=success, value=velocity)

    def get_target_velocity(self):
        """Gets the target velocity.

        Returns:
            (Result): Returns success flag and target velocity in RPM.
        """
        (success, velocity) = self._get_int(self.GET_TARGET_VELOCITY)
        return Result(success=success, value=velocity)

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

    def set_velocity_limit(self, value):
        """Sets the maximal velocity for all modes.

        Args:
            value (int): Maxmimal velocity in RPM of the motor.
        """
        self._send_command(self.SET_MAX_VELOCITY, int(value))

    def get_velocity_limit(self):
        """Gets the maximal velocity for all modes.

        Returns:
            (Result): Success flag and maximal velocity in RPM of the motor.
        """
        (success, velocity) = self._get_int(self.GET_MAX_VELOCITY)
        return Result(success=success, value=velocity)

    def set_acceleration_limit(self, value):
        """Sets the acceleration.

        Args:
            value (int): Acceleration in Rev/s^2.
        """
        self._send_command(self.SET_ACCELERATION, int(value))

    def get_acceleration_limit(self):
        """Gets the acceleration.

        Returns:
            (Result): Success flag and acceleration in Rev/s^2.
        """
        (success, acceleration) = self._get_int(self.GET_ACCELERATION)
        return Result(success=success, value=acceleration)

    def set_deceleration_limit(self, value):
        self._send_command(self.SET_DECELERATION, int(value))

    def get_deceleration_limit(self):
        (success, deceleration) = self._get_int(self.GET_DECELERATION)
        return Result(success=success, value=deceleration)

    def is_homing(self):
        raise NotImplementedError

    def get_lower_limit_switch(self):
        raise NotImplementedError

    def get_upper_limit_switch(self):
        raise NotImplementedError

    def is_enabled(self):
        raise NotImplementedError

    def is_position_reached(self):
        raise NotImplementedError
