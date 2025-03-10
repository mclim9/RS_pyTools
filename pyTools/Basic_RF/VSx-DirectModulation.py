""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


class VSx_DirectMod(object):
    """Direct Modulation Class"""
    def __init__(self):
        # self.SMW = iSocket().open('172.21.98.44', 5025)         # C4T
        # self.FSW = iSocket().open('172.21.98.120', 5025)        # C4T
        self.SMW = iSocket().open('172.24.225.130', 5025)       # RSSD
        self.FSW = iSocket().open('172.24.225.128', 5025)       # RSSD
        self.freq = 30e9
        self.RFBW = 250e6
        self.pwer = 0

    def config_VSG(self):
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')       # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?') # RMS Power Level
        # self.SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')      # Power Offset
        self.SMW.write(f':SOUR1:BB:DM:SRAT {self.RFBW}')    # Sampling Rate
        self.SMW.write(f':SOUR1:BB:DM:PRBS:LENG 23')        # PRBS length
        self.SMW.write(f':SOUR1:BB:DM:FORM QAM256')         # Modulation
        self.SMW.write(f':SOUR1:BB:DM:FILT:TYPE RCOS')      # Filter Type
        self.SMW.write(f':SOUR1:BB:DM:FILT:PAR:RCOS 0.11')  # Filter Coefficient
        self.SMW.write(f':SOUR1:BB:DM:STAT 1')              # Direct Modulation On
        self.SMW.write(f':SOUR1:IQ:STAT 1')                 # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                    # RF ON
        self.SMW.clear_error()

    def config_VSA(self):
        self.FSW.write(':INST:CRE:NEW DDEM, "VSA"')         # Create Channel
        self.FSW.write(':INST:SEL "VSA"')                   # Select Digital Demod
        self.FSW.write(':INIT:CONT OFF')                    # Single Sweep
        self.FSW.write(f':SENS:FREQ:CENT {self.freq}')      # Center Freq
        self.FSW.write(f':SENS:DDEM:SRAT {self.RFBW}')      # Sampling Rate
        self.FSW.write(f':SENS:DDEM:FORM QAM')              # Modulation
        self.FSW.write(f':SENS:DDEM:QAM:NST 256')           # Modulation
        self.FSW.write(f':SENS:DDEM:TFIL:NAME "RRC"')       # Filter Type
        self.FSW.write(f':SENS:DDEM:TFIL:ALPH 0.11')        # Filter Coefficient
        self.FSW.write(f':SENS:DDEM:EQU:STAT ON')           # Equalizer ON
        self.FSW.write(f':SENS:DDEM:EQU:LENG 20')           # Equalizer Length

        self.FSW.clear_error()

    def make_meas(self):
        self.FSW.write(':INST:SEL "VSA"')                   # Select Digital Demod
        # self.FSW.write(':CALC1:MARK1:STAT ON')              # Window1 Marker1 ON
        # self.FSW.write(':CALC1:MARK2:STAT ON')              # Window1 Marker2 ON

        self.FSW.query(':SENS:ADJ:LEV;*OPC?')
        self.FSW.write(':INIT:IMM;*OPC?')
        # mkr1 = self.FSW.query(':CALC1:MARK1:Y?')
        # mkr2 = self.FSW.query(':CALC1:MARK2:Y?')

if __name__ == "__main__":
    test = VSx_DirectMod()
    test.config_VSG()
    test.config_VSA()
    test.make_meas()
