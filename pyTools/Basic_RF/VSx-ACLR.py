""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


class VSx_ACLR(object):
    """ACLR Class"""
    def __init__(self):
        # self.SMW = iSocket().open('172.21.98.44', 5025)       # C4T
        # self.FSW = iSocket().open('172.21.98.120', 5025)      # C4T
        self.SMW = iSocket().open('172.24.225.100', 5025)       # RSSD
        self.FSW = iSocket().open('172.24.225.128', 5025)       # RSSD
        self.freq = 30e9
        self.RFBW = 250e6
        self.pwer = -10

    def config_VSG(self):
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')           # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?')     # RMS Power Level
        # self.SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')          # Power Offset
        self.SMW.write(f':SOUR1:BB:DM:SRAT {self.RFBW}')        # Sampling Rate
        self.SMW.write(f':SOUR1:BB:DM:PRBS:LENG 23')            # PRBS length
        self.SMW.write(f':SOUR1:BB:DM:FORM QAM256')             # Modulation
        self.SMW.write(f':SOUR1:BB:DM:FILT:TYPE RCOS')          # Filter Type
        self.SMW.write(f':SOUR1:BB:DM:FILT:PAR:RCOS 0.11')      # Filter Coefficient
        self.SMW.write(f':SOUR1:BB:DM:STAT 1')                  # Direct Modulation On
        self.SMW.write(f':SOUR1:IQ:STAT 1')                     # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                        # RF ON
        self.SMW.clear_error()                                  # Clear Errors

    def config_VSA(self):
        VSA_BW = self.RFBW * 0.7
        self.FSW.write(':INST:SEL "Spectrum"')                  # Select Spectrum
        self.FSW.write(':INIT:CONT OFF')                        # Single Sweep
        self.FSW.write(f':SENS:FREQ:CENT {self.freq}')          # Center Freq
        self.FSW.write(f':SENS:BAND:RES 1e6')                   # Res BW
        self.FSW.write(f':SENS:BAND:RES:AUTO OFF')              # Res BW
        self.FSW.write(f':SENS:WIND:DET1:FUNC RMS')             # RMS Detector

        self.FSW.write(f':CALC:MARK:FUNC:POW:SEL ACP')          # Measure ACLR
        self.FSW.write(f':SENS:POW:ACH:ACP 2')                  # Adj Channels
        self.FSW.write(f':SENS:POW:ACH:BWID:CHAN1 {VSA_BW}')    # Tx Ch Bandwidth
        self.FSW.write(f':SENS:POW:ACH:BWID:ACH {VSA_BW}')      # Adj Ch Bandwidth
        self.FSW.write(f':SENS:POW:ACH:SPAC:CHAN1 {self.RFBW}') # Tx Ch Spacing
        self.FSW.write(f':SENS:POW:ACH:SPAC:ACH {self.RFBW}')   # Adj Ch Spacing
        self.FSW.clear_error()                                  # Clear Errors

    def make_meas(self):
        self.FSW.write(':INST:SEL "Spectrum"')                  # Select Spectrum

        self.FSW.query(':SENS:ADJ:LEV;*OPC?')                   # Autolevel
        self.FSW.query(':INIT:IMM;*OPC?')                       # Single Sweep

        # data = self.FSW.query(':CALC:MARK1:FUNC:POW:RES? CPOW') # Get Ch Power
        data = self.FSW.query(':CALC:MARK1:FUNC:POW:RES? ACP')  # Get ACPR Values
        print(data)
        self.FSW.clear_error()                                  # Clear Errors

if __name__ == "__main__":
    test = VSx_ACLR()
    test.config_VSG()
    test.config_VSA()
    test.make_meas()
