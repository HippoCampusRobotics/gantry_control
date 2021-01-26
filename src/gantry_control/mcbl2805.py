import serial
from gantry_control.motor import BaseMotor


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
            return False, None
        except ValueError:
            return False, None
        return True, status

    def is_enabled(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        try:
            status = bool(int(ans[3]))
        except IndexError:
            return False, None
        except ValueError:
            return False, None
        return True, status

    def get_lower_limit_switch(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        try:
            lls_status = bool(int(ans[6]))
        except IndexError:
            return False, None
        except ValueError:
            return False, None
        return True, lls_status

    def get_upper_limit_switch(self):
        self._send_command(self.GET_ACTUAL_STATUS)
        ans = self._read_answer()
        try:
            uls_status = bool(int(ans[0]))
        except IndexError:
            return False, None
        except ValueError:
            return False, None
        return True, uls_status
