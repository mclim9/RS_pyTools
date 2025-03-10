""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


class VSx_IMD(object):
    """Direct Modulation Class"""
    def __init__(self):
        # self.SMW = iSocket().open('172.21.98.44', 5025)         # C4T
        # self.FSW = iSocket().open('172.21.98.120', 5025)        # C4T
        # self.SMW = iSocket().open('172.24.225.114', 5025)       # RSSD
        # self.FSW = iSocket().open('172.24.225.128', 5025)       # RSSD
        self.SMW = iSocket().open('SMW200A-111623', 5025)       # RSSD
        self.FSW = iSocket().open('FSW50-101877', 5025)         # RSSD
        self.freq = 30e9
        self.RFBW = 11e6
        self.pwer = -10

    def config_VSG(self):
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')           # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?')     # RMS Power Level
        # self.SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')          # Power Offset

        self.SMW.write(f':SOUR1:BB:MCCW:CARR:COUN 2')           # Multi-CW Count
        self.SMW.write(f':SOUR1:BB:MCCW:CARR:SPAC {self.RFBW}') # Carrier Spacing
        self.SMW.write(f':SOUR1:BB:MCCW:STAT 1')                # Multi-Carrier CW

        self.SMW.write(f':SOUR1:CORR:OPT:EVM 1')                # Optimize EVM
        self.SMW.write(f':SOUR1:IQ:STAT 1')                     # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                        # RF ON
        self.SMW.clear_error()                                  # Clear Errors

    def config_VSA(self):
        self.FSW.write(':SYST:DISP ON')                         # Display On
        self.FSW.write(':INST:SEL "Spectrum"')                  # Select Spectrum
        self.FSW.write(':INIT:CONT ON')                         # Continious Sweep
        self.FSW.write(':CALC:MARK:FUNC:TOI:STAT ON')           # IMD Meas On
        self.FSW.write(f':SENS:FREQ:CENT {self.freq}')          # Center Freq
        self.FSW.write(f':SENS:FREQ:SPAN {4 * self.RFBW}')      # Span
        self.FSW.write(':SENS:WIND1:DET1:FUNC RMS')             # RMS Detector
        self.FSW.write(':SENS:SWE:TIME 0.1')                   # Sweep Time
        self.FSW.write(':CALC1:MARK2:FUNC:TOI:SEAR ONCE')       # Find IMD
        self.FSW.query(':INIT:IMM;*OPC?')                       # Take Sweep

        self.FSW.clear_error()                                  # Clear Errors

    def make_meas(self):
        self.FSW.write(':INST:SEL "Spectrum"')                  # Select Spectrum
        self.FSW.write(':INIT:CONT OFF')                        # Continious Sweep
        self.FSW.query(':INIT:IMM;*OPC?')                       # Take Sweep
        rdStr = self.FSW.query(':CALC:MARK:FUNC:TOI:RES?')      # Make Measurement
        print(f'IMD Results: {rdStr}')

    def meas_IMD_PhaseSweep(self):
        for i in range(180):
            self.SMW.query(f':SOUR1:BB:MCCW:CARR:LIST:PHAS 1,{i};*OPC?')
            # self.SMW.write(f':SOUR1:BB:MCCW:CARR:LIST:PHAS 1,{i}')
            self.make_meas()
        self.SMW.clear_error()                                  # Clear Errors

if __name__ == "__main__":
    test = VSx_IMD()
    test.config_VSG()
    test.config_VSA()
    # test.make_meas()
    test.meas_IMD_PhaseSweep()
