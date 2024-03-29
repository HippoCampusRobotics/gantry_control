from gantry_control.motor import BaseMotor, Result

GET_TYPE = "GTYP"
GET_SERIAL = "GSER"
GET_VERSION = "VER"
GET_OPERATING_STATUS = "OST"

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


class Motor(BaseMotor):
    def __init__(self, port, baud, timeout):
        super(Motor, self).__init__(port=port, baud=baud, timeout=timeout)

    def get_operating_status(self):
        success, ans = self._get_int(GET_OPERATING_STATUS)
        if not success:
            return Result(success=False)
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
        return Result(success=True, value=ret)

    def is_homing(self):
        success, ans = self.get_int(GET_OPERATING_STATUS)
        if not success:
            return Result(success=False)
        return Result(success=True, value=bool((1 << 0) & ans))

    def get_config_status(self):
        success, ans = self._get_int(GET_CONFIG_STATUS)
        if not success:
            return Result(success=False)
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
        return Result(success=True, value=ret)

    def get_lower_limit_switch(self):
        result = self.get_operating_status()
        if not result.success:
            return Result(success=False)
        status = result.value["status_input_1"]
        return Result(success=True, value=status)

    def get_upper_limit_switch(self):
        result = self.get_operating_status()
        if not result.success:
            return Result(success=False)
        status = result.value["status_input_2"]
        return Result(success=True, value=status)

    def is_enabled(self):
        result = self._get_int(self.CONTROL_STATUS)
        if not result.success:
            return Result(success=False)
        status = bool((1 << 10) & result.value)
        return Result(success=True, value=status)

    def is_position_reached(self):
        result = self.get_operating_status()
        if not result.success:
            return Result(success=False)
        status = result.value["position_attained"]
        return Result(success=True, value=status)
