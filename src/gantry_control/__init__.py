from . import faulhaber_rs232
from . import mcbl2805
from . import motor


def create(port, baud, timeout) -> motor.BaseMotor:
    m = motor.BaseMotor(port=port, baud=baud, timeout=timeout)
    t = m.get_type()
    if t == 'CS':
        return mcbl2805.Motor(port=port, baud=baud, timeout=timeout)
    elif t == 'CS-BX4':
        return faulhaber_rs232.Motor(port=port, baud=baud, timeout=timeout)
    elif t == '':
        raise IOError(
            'Motor not responding.\nIs it switched on?\nAre all '
            'wires connected?\nHave you tried turning it off and on again?')
    else:
        raise RuntimeError(f'Unknown motor type: {t}')
