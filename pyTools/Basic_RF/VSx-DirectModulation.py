""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


class VSx_DirectMod(object):
    """Direct Modulation Class"""
    def __init__(self):
        self.SMW = iSocket().open('10.0.0.60', 5025)
        # self.FSW = iSocket().open('192.168.58.115', 5025)
        self.freq = 28e9
        self.RFBW = 250e6
        self.pwer = -10

    def config_VSG(self):
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')       # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?') # RMS Power Level
        # self.SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')      # Power Offset
        self.SMW.write(f':SOUR1:BB:DM:SRAT {self.RFBW}')    # Sampling Rate
        self.SMW.write(f':SOUR1:BB:DM:PRBS:LENG 23')        # PRBS length
        self.SMW.write(f':SOUR1:BB:DM:FORM QAM256')         # Modulation
        self.SMW.write(f':SOUR1:BB:DM:FILT:TYPE RCOS')      # Filter Type
        self.SMW.write(f':SOUR1:BB:DM:FILT:PAR:RCOS 0.22')  # Filter Coefficient
        self.SMW.write(f':SOUR1:BB:DM:STAT 1')              # Direct Modulation On
        self.SMW.write(f':SOUR1:IQ:STAT 1')                 # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                    # RF ON

    def config_VSA(self):
        self.FSW.write(':INST:SEL "Analog Demod"')          # Select Analog Demod
        self.FSW.write(':INIT:CONT OFF')                    # Single Sweep
        self.FSW.write(f':SENS:FREQ:CENT {self.freq}')      # Center Freq
        self.FSW.write(f':SENS:DDEM:SRAT {self.RFBW}')      # Sampling Rate
        self.FSW.write(f':SOUR1:BB:DM:PRBS:LENG 23')        # PRBS length
        self.FSW.write(f':SENS:DDEM:FORM QAM')              # Modulation
        self.FSW.write(f':SENS:DDEM:QAM:NST 256QAM')        # Modulation
        self.FSW.write(f':SENS:DDEM:TFIL:NAME RRC')         # Filter Type
        self.FSW.write(f':SENS:DDEM:TFIL:NAME 0.22')        # Filter Coefficient

    def take_Meas(self):
        self.FSW.write(':INST:SEL "Analog Demod"')          # Select Analog Demod
        self.FSW.write(':CALC1:MARK1:STAT ON')              # Window1 Marker1 ON
        self.FSW.write(':CALC1:MARK2:STAT ON')              # Window1 Marker2 ON
        for i in range(100):
            self.FSW.write(':INIT:IMM;*OPC?')
            mkr1 = self.FSW.query(':CALC1:MARK1:Y?')
            mkr2 = self.FSW.query(':CALC1:MARK2:Y?')
            print(f'Marker1:{mkr1} Marker2:{mkr2}')

if __name__ == "__main__":
    test = VSx_DirectMod()
    test.config_VSG()
    # test.config_VSA()
    # test.take_Meas()
