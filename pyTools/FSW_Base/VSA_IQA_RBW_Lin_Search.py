""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

Desr_RBW = 120e3
Curr_Wind = 48000

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)

FSW.write(':INP:ATT 0')                                     # Zero attenuation
FSW.write('INIT:CONT OFF')                                  # Single sweep
FSW.write(':TRAC:IQ:BWID 1000e6')                           # Analysis BW
FSW.write(':SENS:SWE:TIME 1e-3')                            # Sweep Time
FSW.write(':SENS:WIND1:DET1:FUNC RMS')                      # Detector
FSW.write(':DISP:WIND1:SUBW:TRAC1:MODE AVER')               # Trace Mode
FSW.write(':SENS:IQ:BWID:MODE FFT')                         # Advanced FFT Mode
FSW.write(':SENS:IQ:FFT:LENG 65536')                        # FFT Length

def searcher(delta):
    SRat = FSW.query(':TRAC:IQ:SRAT?')                      # Sampling Rate
    Wind = FSW.queryInt(':SENS:IQ:FFT:WIND:LENG?')          # Window Length
    for i in range(10):
        Curr_RBW  = FSW.queryFloat(':SENS:IQ:BWID:RES?')    # RBW
        if Curr_RBW < Desr_RBW:
            Curr_Wind = Wind - delta
        else:
            Curr_Wind = Wind + delta
        FSW.write(f':SENS:IQ:FFT:WIND:LENG {Curr_Wind}')    # Window Length
        # FSW.query(':INIT:IMM;*OPC?')                      # Update Screen
        RBW  = FSW.queryFloat(':SENS:IQ:BWID:RES?')         # RBW
        Wind = FSW.queryInt(':SENS:IQ:FFT:WIND:LENG?')      # Window Length
        print(f'{SRat}: Desr_RBW:{Desr_RBW} Curr_RBW:{RBW:.2f} {Wind}')

FSW.tick()
searcher(5000)
searcher(1000)
searcher(100)
searcher(10)
searcher(1)
FSW.tock('asdf')