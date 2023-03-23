#!/usr/bin/env python3

"""base class for scpi instruments

communication backends supported:
    scpi over plain vanilla socket
    VISA for GPIB
"""

import socket
import time
import warnings

pyvisa = None
try:
    import pyvisa
except ImportError:
    pass

serial = None
try:
    import serial
except ImportError:
    pass


class InstrumentError(Exception):
    """exception during handling of Instrument"""
    pass


class Instrument():
    """a SCPI style instrument base class

    address is string IP address or string GPIB address

    raises InstrumentError
    """

    SupportedHardware = None
    Default_Port = 5025
    ScpiNewlineDelimiter = "\n"
    ScpiCommentDelimiter = ";"
    ScpiResponseMaxSize = 1 << (20 + 8)

    Supports_IDN = True
    Supports_OPC = True
    Supports_ESR = True
    Supports_RST = True

    def __init__(self, address=None, port=None, reset=True):

        self.instrument = None
        self._uses_bytes = None
        if port is None:
            port = self.Default_Port
        if address:
            if address.upper().startswith("GPIB") or address.upper().startswith('TCPIP')\
                    or address.upper().startswith("USB"):
                assert pyvisa is not None, (
                    "PyVISA (required for GPIB/VISA) not available")
                self._serial = False
                self._gpib = True
                self._socket = False
                self.instrument = pyvisa.ResourceManager().open_resource(
                    address)
                self._uses_bytes = False
                self.instrument.timeout = 10000
            elif "/dev/tty" in address or address.upper().startswith("COM"):
                assert serial is not None, (
                    "PySerial (required for serial) not available")
                self._serial = True
                self._gpib = False
                self._socket = False
                self.instrument = serial.Serial(address)
                self.instrument.timeout = 2
                self.instrument.reset_input_buffer()
                self._uses_bytes = True
            else:
                self._serial = False
                self._socket = True
                self._gpib = False
                self.instrument = socket.socket()
                self.instrument.connect((address, port))
                self._uses_bytes = True
            mfg, model = None, None
            if self.Supports_IDN:
                idn_response = self.ask("*idn?")
                if idn_response.count(",") != 3:
                    raise Exception(idn_response)
                mfg, model, _serial_number, _firmware = [
                    x.strip() for x in idn_response.split(",")]
                if self.SupportedHardware:
                    assert (mfg, model) in self.SupportedHardware, (mfg, model)
            self.manufacturer = mfg
            self.model = model
            if reset and self.Supports_RST:
                self.writeline("*RST")
                self.ask("*OPC?")

    def reset(self):
        if self.Supports_RST:
            self.writeline("*RST")
        else:
            warnings.warn('reset called but *RST not supported')

    def write_bytes(self, binary_message, add_delimiter=True):
        if self._socket:
            if add_delimiter:
                self.instrument.sendall(
                    binary_message + self.ScpiNewlineDelimiter.encode())
            else:
                self.instrument.sendall(binary_message)
        elif self._gpib:
            self.instrument.write(binary_message)
        elif self._serial:
            if add_delimiter:
                self.instrument.write(
                    binary_message + self.ScpiNewlineDelimiter.encode())
            else:
                self.instrument.write(binary_message)
        else:
            raise Exception

    def writeline(self, message):
        if self._uses_bytes:
            self.write_bytes(message.encode())
        else:
            self.write_bytes(message)

    def ask(self, message):
        self.writeline(message)
        response = self.readline()
        return response

    def read_bytes(self, strip_delimiter=True):
        response = None
        if self._socket:
            response = self.instrument.recv(self.ScpiResponseMaxSize)
        elif self._gpib:
            response = self.instrument.read_raw()
        elif self._serial:
            raise Exception()

        rval = None
        if strip_delimiter:
            delimiter = self.ScpiNewlineDelimiter
            if self._uses_bytes:
                delimiter = self.ScpiNewlineDelimiter.encode()
            rval = response[:-1 * len(delimiter)]
        else:
            rval = response
        return rval

    def readline(self):
        response = None
        if self._serial:
            response = self.instrument.readline()
        else:
            response = self.read_bytes()
        if self._uses_bytes or self._gpib:
            response = response.decode()
        return response

    def isopcomplete(self):
        rval = None
        if self.Supports_OPC and self.Supports_ESR:
            self.writeline("*OPC")
            rval = bool(0x1 & int(self.ask("*ESR?")))
        else:
            rval = True
        return rval

    def iserror(self):
        """true if command, execution, device independent or query error"""
        if self.Supports_ESR:
            esr = int(self.ask("*ESR?"))
            rval = bool(esr & ((1 << 2) | (1 << 3) | (1 << 4) | (1 << 5)))
            return rval
        else:
            return 0

    def waitforopcomplete(self, timeout=8):
        start = time.time()
        while True:
            if self.isopcomplete():
                break
            else:
                if (time.time() - start) > timeout:
                    raise InstrumentError("timed out")

    def writelines(self, lines_string, **kwargs):
        """write multiple commands in (multiline) string

        split on  newlines
        toss everything after comment delimiter
        toss leading, trailing whitespace
        """
        for origline in lines_string.split(self.ScpiNewlineDelimiter):
            line = origline[:]
            line = line.split(self.ScpiCommentDelimiter)[0]
            line = line.strip()
            if line:
                self.writeline(line)
                if self.iserror():
                    raise InstrumentError("error executing line {}".format(line))
                self.waitforopcomplete(**kwargs)
