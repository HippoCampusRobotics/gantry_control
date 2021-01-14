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
        status = bool(int(ans[3]))
        return status

    def is_enabled(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer()
        status = bool(int(ans[3]))
        return status

    def get_lower_limit_switch(self):
        self._send_command(self.GET_STATUS)
        ans = self._read_answer(self)
        lls_status = bool(int(ans[6]))
        return lls_status

    def get_upper_limit_switch(self):
        self._send_command(self.GET_ACTUAL_STATUS)
        ans = self._read_answer(self)
        uls_status = bool(int(ans[0]))
        return uls_status
