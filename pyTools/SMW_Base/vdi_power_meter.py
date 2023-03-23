#!/usr/bin/env python3
"""VDI power meter interface"""
from math import log10
from instrument import Instrument, InstrumentError

def bytes_to_decimal(integer, decimal):
    return ((integer * 10) + decimal) / 10


def is_error(value):
    if len(value) == 0 or value[0] == 0x15:
        return True
    else:
        return False


def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


def pad_bytes(value):
    return value + '0' * (7 - len(value)) + '\r'


def get_calfactor(status_byte_2, status_byte_3):
    sign = (status_byte_3 >> 4) & 0x1
    tens_digit = status_byte_3 & 0xf
    ones_digit = (status_byte_2 >> 4) & 0xf
    decimal_digit = status_byte_2 & 0xf

    value = ((tens_digit * 100) + (ones_digit * 10) + decimal_digit) / 10
    if sign == 1:
        value = -1 * value
    return value


def get_range(status_byte_3):
    range_val = status_byte_3 >> 5
    if range_val == 1:
        return 200e-6
    elif range_val == 2:
        return 2e-3
    elif range_val == 3:
        return 20e-3
    elif range_val == 4:
        return 200e-3
    else:
        raise InstrumentError("Invalid range byte:", range_val)


def to_dbm(value):
    if value > 0:
        return 10 * log10(value / 1e-3)
    else:
        return None

class PowerMeter(Instrument):
    """VDI Erickson power meters
    """

    SupportedHardware = (
        ("VDI", "PM5B"),
    )

    Supports_ESR = False
    Supports_RST = False
    Supports_IDN = False

    def measure(self):
        """measure power

        returns power in Watts"""

        rval = self.ask("?D1")
        cal_factor = 10**(get_calfactor(rval[3], rval[4]) / 10)
        reading = (twos_complement(rval[2] << 8 | rval[1], 16) * 2 * get_range(rval[5]) / 59576) * cal_factor
        return reading

    def zero(self):
        """Zero the power meter"""

        self.writeline("!SZ")

    def get_firmware(self):
        """Read firmware

        returns (primary firmware, secondary firmware)
        """

        rval = self.ask("?VC")
        primary_firmware = bytes_to_decimal(rval[3], rval[2])
        secondary_firmware = bytes_to_decimal(rval[5], rval[4])
        return primary_firmware, secondary_firmware

    def writeline(self, message):
        self.write_bytes(pad_bytes(message).encode(), add_delimiter=False)
        response = self.instrument.read(1)
        if is_error(response):
            raise InstrumentError(f"Error executing line {message}")

    def ask(self, message):
        self.write_bytes(pad_bytes(message).encode(), add_delimiter=False)
        response = self.instrument.read(7)
        if is_error(response):
            raise InstrumentError(f"Error executing line {message}")
        return response[1:]

if __name__ == "__main__":
    prmtr = PowerMeter("COM8")
    print(prmtr.measure())
