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
FSW.write(':SENS:IQ:BWID:MODE FFT')                         # Adv FFT Mode
FSW.write(':SENS:IQ:FFT:ALG AVER')                          # Adv FFT Transform Algo
FSW.write(':SENS:IQ:FFT:LENG 65536')                        # FFT Length
FSW.write(f':SENS:IQ:FFT:WIND:LENG {Curr_Wind}')            # Window Length

def searcher():
    delta = FSW.queryInt(':SENS:IQ:FFT:WIND:LENG?') / 2     # Window Length
    SRat  = FSW.query(':TRAC:IQ:SRAT?')                     # Sampling Rate
    Wind  = FSW.queryInt(':SENS:IQ:FFT:WIND:LENG?')         # Window Length
    RBW   = FSW.queryFloat(':SENS:IQ:BWID:RES?')            # RBW
    while delta > 1:
        if RBW < Desr_RBW:
            Curr_Wind = Wind - delta
        else:
            Curr_Wind = Wind + delta
        FSW.write(f':SENS:IQ:FFT:WIND:LENG {Curr_Wind}')    # Window Length
        # FSW.query(':INIT:IMM;*OPC?')                      # Update Screen
        RBW  = FSW.queryFloat(':SENS:IQ:BWID:RES?')         # RBW
        Wind = FSW.queryInt(':SENS:IQ:FFT:WIND:LENG?')      # Window Length
        print(f'{SRat}: Desr_RBW:{Desr_RBW/1e3:7.2f}kHz Curr_RBW:{RBW/1e3:7.3f}kHz {Wind} {delta}')
        delta = delta / 2

FSW.tick()
searcher()
FSW.tock('asdf')
