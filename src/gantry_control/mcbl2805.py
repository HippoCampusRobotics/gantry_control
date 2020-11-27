import serial

POSITION_ERROR = -999

MOVE = "M"

START_HOMING = "GOHOSEQ"

GET_POSITION = "POS"
GET_VELOCITY = "GV"
GET_TARGET_VELOCITY = "GN"
GET_CURRENT_LIMIT = "GCL"
GET_ACTUAL_CURRENT = "GRC"
GET_VERSION = "VER"
GET_STATUS = "GST"
GET_FAULT_STATUS = "GFS"
GET_ACTUAL_STATUS = "GAST"
GET_SPECIAL_CONFIGURATION = "GSCS"
GET_ENHANCED_STATUS = "GES"

GET_POSITION_MAX_VELOCITY = "GSP"
GET_POSITION_ACCELERATION = "GAC"

SET_POSITION = "LA"
SET_POSITION_RELATIVE = "LR"
SET_HOME = "HO"
SET_POSTION_MAX_VELOCITY = "SP"
SET_POSITION_ACCELERATION = "AC"

SET_VELOCITY = "V"

STATUS_POSITION_CONTROLLER_ACTIVE_BITMASK = 0x01
STATUS_POSITION_CONTROLLER_ACTIVE_SHIFT = 0x00
STATUS_DRIVE_ENABLED_BITMASK = 0x01
STATUS_DRIVE_ENABLED_SHIFT = 0x03
STATUS_POSITION_REACHED_BITMASK = 0x01
STATUS_POSITION_REACHED_SHIFT = 0x04
STATUS_LIMIT_SWITCH_EDGE_BITMASK = 0x01
STATUS_LIMIT_SWITCH_EDGE_SHIFT = 0x05
STATUS_LIMIT_SWITCH_LEVEL_BITMASK = 0x01
STATUS_LIMIT_SWITCH_LEVEL_SHIFT = 0x0

AST_LIMIT_SWITCH_2_BITMASK = 0x01
AST_LIMIT_SWITCH_2_SHIFT = 0x00
AST_LIMIT_SWITCH_3_BITMASK = 0x01
AST_LIMIT_SWITCH_3_SHIFT = 0x01
AST_DIRECTION_BITMASK = 0x01
AST_DIRECTION_SHIFT = 0x02
AST_POWER_ON_HOMING_ACTIVE_BITMASK = 0x01
AST_POWER_ON_HOMING_ACTIVE_SHIFT = 0x03

SCS_HOMING_ACTIVE_BITMASK = 0x01
SCS_HOMING_ACTIVE_SHIFT = 0x00
SCS_FAULT_PIN_IO_BITMASK = 0x01
SCS_FAULT_PIN_IO_SHIFT = 0x01
SCS_FAULT_PIN_PULSE_ERROR_BITMASK = 0x01
SCS_FAULT_PIN_PULSE_ERROR_SHIFT = 0x02
SCS_FAULT_PIN_CONFIG_BITMASK = 0x01
SCS_FAULT_PIN_CONFIG_SHIFT = 0x03
SCS_LIMIT_SWITCH2_EDGE_BITMASK = 0x01
SCS_LIMIT_SWITCH2_EDGE_SHIFT = 0x04
SCS_LIMIT_SWITCH3_EDGE_BITMASK = 0x01
SCS_LIMIT_SWITCH3_EDGE_SHIFT = 0x05
SCS_PROGRAM_SEQUENCE_ACTIVE_BITMASK = 0x01
SCS_PROGRAM_SEQUENCE_ACTIVE_SHIFT = 0x06
SCS_AUTO_ANSWER_BITMASK = 0x01
SCS_AUTO_ANSWER_SHIFT = 0x07

ES_ANALOG_CURRENT_BITMASK = 0x01
ES_ANALOG_CURRENT_SHIFT = 0x02
ES_POSITION_LIMIT_MODE_BITMASK = 0x01
ES_POSITION_LIMIT_MODE_SHIFT = 0x03
ES_DEVIATION_ERROR_BITMASK = 0x01
ES_DEVIATION_ERROR_SHIFT = 0x04


class Motor():
    def __init__(self, port, baud, timeout):
        self.port = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    def _send_command(self, command, arg=""):
        self.port.write(b"{}{}\r".format(command, arg))

    def _read_answer(self):
        return self.port.readline().rstrip()

    def set_home(self):
        self._send_command(SET_HOME)
        return

    def read_position(self):
        self._send_command(GET_POSITION)
        ans = self._read_answer()
        try:
            position = int(ans)
        except ValueError:
            position = POSITION_ERROR
        return position

    def set_velocity(self, value):
        self._send_command(SET_VELOCITY, int(value))

    def read_target_velocity(self):
        self._send_command(GET_TARGET_VELOCITY)
        ans = self._read_answer()
        try:
            target = int(ans)
        except ValueError:
            target = 0
        return target

    def start_homing(self):
        self._send_command(START_HOMING)

    def read_velocity(self):
        self._send_command(GET_VELOCITY)
        ans = self._read_answer()
        try:
            velocity = int(ans)
        except ValueError:
            velocity = 0
        return velocity

    def set_position(self, value, relative=False):
        if relative:
            self._send_command(SET_POSITION_RELATIVE, value)
        else:
            self._send_command(SET_POSITION, value)

    def move_to_position(self):
        self._send_command(MOVE)

    def set_position_max_velocity(self, value):
        self._send_command(SET_POSTION_MAX_VELOCITY, value)

    def read_position_max_velocity(self):
        self._send_command(GET_POSITION_MAX_VELOCITY)
        ans = self._read_answer()
        try:
            max_velocity = int(ans)
        except ValueError:
            max_velocity = -1
        return max_velocity
    
    def set_position_acceleration(self, value):
        self._send_command(SET_POSITION_ACCELERATION, value)
    
    def read_position_acceleration(self):
        self._send_command(GET_POSITION_ACCELERATION)
        ans = self._read_answer()
        try:
            acceleration = int(ans)
        except ValueError:
            acceleration = 0
        return acceleration

    def read_special_configuration(self):
        self._send_command(GET_SPECIAL_CONFIGURATION)
        ans = int(self._read_answer())
        ret = {}
        ret["homing_active"] = ((ans >> SCS_HOMING_ACTIVE_SHIFT)
                                & SCS_HOMING_ACTIVE_BITMASK)
        ret["fault_pin_io"] = ((ans >> SCS_FAULT_PIN_IO_SHIFT)
                               & SCS_FAULT_PIN_IO_BITMASK)
        ret["fault_pin_pulse"] = ((ans >> SCS_FAULT_PIN_PULSE_ERROR_SHIFT)
                                  & SCS_FAULT_PIN_PULSE_ERROR_BITMASK)
        ret["limit_switch_2_edge"] = ((ans >> SCS_LIMIT_SWITCH2_EDGE_SHIFT)
                                      & SCS_LIMIT_SWITCH2_EDGE_BITMASK)
        ret["limit_switch_3_edge"] = ((ans >> SCS_LIMIT_SWITCH3_EDGE_SHIFT)
                                      & SCS_LIMIT_SWITCH3_EDGE_BITMASK)
        ret["program_sequence_active"] = (
            (ans >> SCS_PROGRAM_SEQUENCE_ACTIVE_SHIFT)
            & SCS_PROGRAM_SEQUENCE_ACTIVE_BITMASK)
        ret["auto_answer"] = ((ans >> SCS_AUTO_ANSWER_SHIFT)
                              & SCS_AUTO_ANSWER_BITMASK)
        return ret

    def is_homing(self):
        self._send_command(GET_SPECIAL_CONFIGURATION)
        ans = int(self._read_answer())
        return bool((ans >> SCS_HOMING_ACTIVE_SHIFT)
                    & SCS_HOMING_ACTIVE_BITMASK)
