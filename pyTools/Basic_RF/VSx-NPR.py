""" https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_application/application_notes/1ef108/1EF108_4E_FSW_NPR_p.pdf"""
# SMW-K811
# FSW-K19

from iSocket import iSocket                 # Import socket module


class VSx_NPR(object):
    """Direct Modulation Class"""
    def __init__(self):
        # self.SMW = iSocket().open('172.21.98.44', 5025)         # C4T
        # self.FSW = iSocket().open('172.21.98.120', 5025)        # C4T
        self.SMW = iSocket().open('172.24.225.100', 5025)       # RSSD
        self.FSW = iSocket().open('172.24.225.128', 5025)       # RSSD
        self.freq = 30e9
        self.RFBW = 250e6
        self.pwer = 0

    def config_VSG_arb(self):
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')           # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?')     # RMS Power Level
        # self.SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')          # Power Offset
        self.SMW.write(f':SOUR1:BB:ARB:SIGN:TYPE AWGN')
        self.SMW.write(f':SOUR1:BB:ARB:TSIG:AWGN:CRE')
        self.SMW.write(f':SOUR1:BB:ARB:STAT 1')
        self.SMW.write(f':SOUR1:BB:ARB:CLOC {self.RFBW}')       # Clock rate
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1:COUN 2')           # Notch Count
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1 1')                # Notch1 ON
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1:FREQ:OFFS 10e6')   # Notch Offset
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1:BWID:ABS 20e6')    # Notch BW
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1:STAT 1')           # Notch1 On
        self.SMW.write(f':SOUR1:BB:ARB:NOTC2:FREQ:OFFS -20e6')  # Notch Offset
        self.SMW.write(f':SOUR1:BB:ARB:NOTC2:BWID:ABS 10e6')    # Notch BW
        self.SMW.write(f':SOUR1:BB:ARB:NOTC2:STAT 1')           # Notch2 On
        self.SMW.write(f':SOUR1:BB:ARB:NOTC1:APPL')             # Apply Notch Settings

        self.SMW.write(f':SOUR1:CORR:OPT:EVM 1')                # Optimize EVM
        self.SMW.write(f':SOUR1:IQ:STAT 1')                     # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                        # RF ON
        self.SMW.clear_error()

    def config_VSG_mccw(self):
        stopCW = 501
        self.SMW.write(f':SOUR1:FREQ:CW {self.freq}')           # Center Frequency
        self.SMW.query(f':SOUR1:POW:LEV {self.pwer};*OPC?')     # RMS Power Level

        self.SMW.write(f':SOUR1:BB:MCCW:CARR:COUN {stopCW}')    # MCCW 501 points
        self.SMW.write(f':SOUR1:BB:MCCW:CARR:SPAC 500e3')       # MCCW Spacing

        # Turn on all
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAR 0')      # MCCW edit start
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STOP {stopCW-1}')  # MCCW edit stop
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAT 1')      # MCCW edit status
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:EXEC')        # MCCW edit apply

        # Notch 1
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAR 250')    # MCCW edit start
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STOP 290')    # MCCW edit stop
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAT 0')      # MCCW edit status
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:EXEC')        # MCCW edit apply

        # Notch 2
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAR 200')    # MCCW edit start
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STOP 220')    # MCCW edit stop
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:STAT 0')      # MCCW edit status
        self.SMW.write(f':SOUR1:BB:MCCW:EDIT:CARR:EXEC')        # MCCW edit apply

        self.SMW.write(f':SOUR1:BB:MCCW:CFAC:MODE SLOW')        # Crest factor Mode
        self.SMW.write(f':SOUR1:BB:MCCW:CFAC 10')               # Target Crest factor
        self.SMW.query(f':SOUR1:BB:MCCW:STAT 1;*OPC?')          # MCCW ON

        self.SMW.write(f':SOUR1:CORR:OPT:EVM 1')                # Optimize EVM
        self.SMW.write(f':SOUR1:IQ:STAT 1')                     # IQ Modulation ON
        self.SMW.write(f':OUTP1:STAT 1')                        # RF ON
        self.SMW.clear_error()

    def config_VSA(self):
        self.FSW.write(':INST:SEL "Spectrum"')                  # Select Spectrum
        self.FSW.write(':INIT:CONT ON')                         # Continious Sweep
        self.FSW.write(f':SENS:NPR:STAT ON')                    # NPR Meas On
        self.FSW.write(f':SENS:FREQ:CENT {self.freq}')          # Center Freq
        self.FSW.write(f':SENS:NPR:CHAN:BWID {self.RFBW}')      # Sampling Rate
        self.FSW.write(':SENS:WIND1:DET1:FUNC RMS')             # RMS Detector
        self.FSW.write(':SENS:SWE:TIME 1.00')                  # Sweep Time

        self.FSW.write(f':SENS:NPR:NOTC:COUN 2')                # Number of notches
        self.FSW.write(f':SENS:NPR:NOTC1:FREQ:OFFS 10e6')       # Notch Offset
        self.FSW.write(f':SENS:NPR:NOTC1:BWID:ABS 19e6')        # Notch Width
        self.FSW.write(f':SENS:NPR:NOTC2:FREQ:OFFS -20e6')      # Notch Offset
        self.FSW.write(f':SENS:NPR:NOTC2:BWID:ABS 9e6')         # Notch Width
        self.FSW.query(':SENS:ADJ:LEV;*OPC?')                   # Autolevel

        self.FSW.clear_error()

    def make_meas(self):
        self.FSW.write(':INST:SEL "VSA"')                       # Select Digital Demod
        self.FSW.query(':SENS:ADJ:LEV;*OPC?')                   # Autolevel
        self.FSW.query(':INIT:IMM;*OPC?')                       # Single Sweep
        rdStr = self.FSW.query(':CALC:NPR:RES? ALL')            # Get Results
        print(f'NPR  : {rdStr}')

if __name__ == "__main__":
    test = VSx_NPR()
    test.config_VSG_arb()
    # test.config_VSG_mccw()
    test.config_VSA()
    test.make_meas()
