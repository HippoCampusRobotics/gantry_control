import serial
import time

GET_TYPE = "GTYP"
GET_SERIAL = "GSER"
GET_VERSION = "VER"
GET_POSITION = "POS"
GET_TARGET_POSITION = "TPOS"
GET_VELOCITY = "GV"
GET_TARGET_VELOCITY = "GN"
GET_TEMPERATURE = "TEM"
GET_OPERATING_STATUS = "OST"

GET_STATUS = "GST"
GET_ACTUAL_STATE = "GAST"
GET_EXTENDED_STATE = "GES"
GET_FAILURE_STATE = "GFS"
GET_HARD_STATE = "HS"

GET_CONFIG_STATUS = "CST"
GET_MODE = "GMOD"
GET_ENCODE_RESOLUTION = "GENCRES"
GET_SPEED_CONSTANT = "GKN"
GET_MOTOR_RESISTANCE = "GRM"
GET_MAGNETIC_PITCH = "GTM"
GET_STEP_WIDTH = "GSTW"
GET_STEP_NUMBER = "GSTN"
GET_MINIMUM_VELOCITY = "GMV"
GET_POSITIVE_LIMIT = "GPL"
GET_NEGATIVE_LIMIT = "GNL"
GET_MAXIMUM_SPEED = "GSP"
GET_ACCELERATION = "GAC"
GET_DECELERATION = "GDEC"
GET_SAMPLING_RATE = "GSR"
GET_VELOCITY_P_GAIN = "GPOR"
GET_VELOCITY_I_GAIN = "GI"
GET_POSITION_P_GAIN = "GPP"
GET_POSITION_D_GAIN = "GPD"
GET_CURRENT_I_GAIN = "GCI"
GET_PEAK_CURRENT = "GPC"
GET_CONTINUOUS_CURRENT = "GCC"
GET_DEVIATION = "GDEV"
GET_CORRIDOR = "GCORRIDOR"

START_HOMING = "GOHOSEQ"

CST_AUTOMATIC_REPONSE_BITMASK = 0b11
CST_AUTOMATIC_RESPONSE_BITSHIFT = 1
CST_VELOCITY_PRESETTING_BITMASK = 0b111
CST_VELOCITY_PRESETTING_BITSHIFT = 3
CST_MODE_BITMASK = 0b111
CST_MODE_BITSHIFT = 7
CST_POWER_AMPLIFIER_BITMASK = 0b1
CST_POWER_AMPLIFIER_BITSHIFT = 10
CST_POSITION_CONTROLLER_BITMASK = 0b1
CST_POSITION_CONTROLLER_BITSHIFT = 11
CST_ANALOGUE_DIRECTION_BITMASK = 0b1
CST_ANALOGUE_DIRECTION_BITSHIFT = 12
CST_POSITION_LIMITS_BITMASK = 0b1
CST_POSITION_LIMITS_BITSHIFT = 13
CST_SIN_COMMUTATION_BITMASK = 0b1
CST_SIN_COMMUTATION_BITSHIFT = 14

AVAILABLE_BAUD = (1200, 2400, 4800, 9600, 19200, 57600, 115200)


class Motor(object):
    def __init__(self, port, baud, timeout):
        self.port = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    def _send_command(self, command, arg=""):
        self.port.write(b"{}{}\r".format(command, arg))

    def _read_answer(self):
        return self.port.readline().rstrip()

    def read_motor_info(self):
        motor_type = self.read_type()
        motor_serial = self.read_serial()
        motor_version = self.read_version()
        return dict(type=motor_type, serial=motor_serial, version=motor_version)

    def read_type(self):
        self._send_command(GET_TYPE)
        return self._read_answer()

    def read_temperature(self):
        self._send_command(GET_TEMPERATURE)
        return self._read_answer()

    def read_serial(self):
        self._send_command(GET_SERIAL)
        return self._read_answer()

    def read_version(self):
        self._send_command(GET_VERSION)
        return self._read_answer()

    def read_position(self):
        self._send_command(GET_POSITION)
        return int(self._read_answer())

    def read_target_position(self):
        self._send_command(GET_TARGET_POSITION)
        return int(self._read_answer)

    def read_velocity(self):
        self._send_command(GET_VELOCITY)
        return float(self._read_answer)

    def read_target_velocity(self):
        self._send_command(GET_TARGET_VELOCITY)
        return float(self._read_answer)

    def read_operating_status(self):
        self._send_command(GET_OPERATING_STATUS)
        ans = int(self._read_answer())
        ret = {}
        ret["homing_running"] = bool((1 << 0) & ans)
        ret["program_running"] = bool((1 << 1) & ans)
        ret["program_stopped_delay"] = bool((1 << 2) & ans)
        ret["program_stopped_notify"] = bool((1 << 3) & ans)
        ret["current_limit_active"] = bool((1 << 4) & ans)
        ret["devication_error"] = bool((1 << 5) & ans)
        ret["overvoltage"] = bool((1 << 6) & ans)
        ret["overtemperature"] = bool((1 << 7) & ans)
        ret["status_input_1"] = bool((1 << 8) & ans)
        ret["status_input_2"] = bool((1 << 9) & ans)
        ret["status_input_3"] = bool((1 << 10) & ans)
        ret["position_attained"] = bool((1 << 16) & ans)
        ret["continuous_current_limit"] = bool((1 << 17) & ans)
        return ret

    def is_homing(self):
        self._send_command(GET_OPERATING_STATUS)
        ans = int(self._read_answer())
        return bool((1 << 0) & ans)

    def start_homing(self, wait_until_finished=True):
        self._send_command(START_HOMING)
        if wait_until_finished:
            while (self.is_homing()):
                time.sleep(1.0)

    def read_mode(self):
        self._send_command(GET_MODE)
        ans = self._read_answer()
        if ans == b"c":
            return "CONTMOD"
        elif ans == b"s":
            return "STEPMOD"
        elif ans == b"a":
            return "APCMOD"
        elif ans == b"h":
            return "ENCMOD"
        elif ans == b"e":
            return "ENCSPEED"
        elif ans == b"g":
            return "GEARMOD"
        elif ans == b"v":
            return "VOLTMOD"
        else:
            return "Unknown: '{}'".format(ans)

    def read_config_status(self):
        self._send_command(GET_CONFIG_STATUS)
        ans = int(self._read_answer())
        ret = {}
        ret["automatic_response"] = ((ans >> CST_AUTOMATIC_RESPONSE_BITSHIFT)
                                     & CST_AUTOMATIC_REPONSE_BITMASK)
        ret["velocity_presetting"] = ((ans >> CST_VELOCITY_PRESETTING_BITSHIFT)
                                      & CST_VELOCITY_PRESETTING_BITMASK)
        ret["mode"] = ((ans >> CST_MODE_BITSHIFT) & CST_MODE_BITMASK)
        ret["power_amplifier"] = ((ans >> CST_POWER_AMPLIFIER_BITSHIFT)
                                  & CST_POWER_AMPLIFIER_BITMASK)
        ret["position_controller"] = ((ans >> CST_POSITION_CONTROLLER_BITSHIFT)
                                      & CST_POSITION_CONTROLLER_BITMASK)
        ret["analogue_direction"] = ((ans >> CST_ANALOGUE_DIRECTION_BITSHIFT)
                                     & CST_ANALOGUE_DIRECTION_BITMASK)
        ret["position_limits"] = ((ans >> CST_POSITION_LIMITS_BITSHIFT)
                                  & CST_POSITION_LIMITS_BITMASK)
        ret["sin_commutation"] = ((ans >> CST_SIN_COMMUTATION_BITSHIFT)
                                  & CST_SIN_COMMUTATION_BITMASK)
        return ret
