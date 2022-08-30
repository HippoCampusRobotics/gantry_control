from gantry_control.motor import BaseMotor, Result


class Motor(BaseMotor):
    GET_STATUS = "GST"
    GET_ACTUAL_STATUS = "GAST"

    def __init__(self, port, baud, timeout):
        super(Motor, self).__init__(port=port, baud=baud, timeout=timeout)

    def is_homing(self):
        self._send_command(self.GET_ACTUAL_STATUS)
        ans = self._read_answer()
        try:
            status = bool(int(ans[3]))
        except IndexError:
            return Result(success=False)
        except ValueError:
            return Result(success=False)
        return Result(success=True, value=status)

    def is_enabled(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        try:
            status = bool(int(ans[3]))
        except IndexError:
            return Result(success=False)
        except ValueError:
            return Result(success=False)
        return Result(success=True, value=status)

    def get_lower_limit_switch(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        try:
            status = bool(int(ans[6]))
        except IndexError:
            return Result(success=False)
        except ValueError:
            return Result(success=False)
        return Result(success=True, value=status)

    def get_upper_limit_switch(self):
        self._send_command(self.GET_ACTUAL_STATUS)
        ans = self._read_answer()
        try:
            status = bool(int(ans[0]))
        except IndexError:
            return Result(success=False)
        except ValueError:
            return Result(success=False)
        return Result(success=True, value=status)

    def is_position_reached(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        if len(ans) == 7:
            return Result(success=True, value=bool(int(ans[4])))
        return Result(success=False)
