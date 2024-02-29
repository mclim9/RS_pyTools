""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)

FSW.write(':INST:CRE:NEW IQ, "IQ Analyzer"')                # Create channel
FSW.write(':LAY:REPL:WIND "1",FREQ')                        # Spectrum window
FSW.write(':INP:ATT 0')                                     # Zero attenuation
FSW.write('INIT:CONT OFF')                                  # Single sweep
FSW.write(':TRAC:IQ:BWID 100e6')                            # Analysis BW
FSW.write(':SENS:SWE:TIME 1e-3')                            # Sweep Time
FSW.write(':SENS:IQ:BWID:RES 120e3')                        # RBW
FSW.write(':SENS:WIND1:DET1:FUNC RMS')                      # Detector
FSW.write(':DISP:WIND1:SUBW:TRAC1:MODE AVER')               # Trace Mode

FSW.tick()
for i in range(10):
    freq = 7e9 + 100e6 * i
    FSW.write(f':SENS:FREQ:CENT {freq}')                    
    FSW.query(':INIT:IMM;*OPC?')
    FSW.write(':CALC1:MARK1:MAX:PEAK')
    MkrX = FSW.queryFloat(':CALC1:MARK1:X?')                # Get Marker Frequency
    MkrY = FSW.queryFloat(':CALC1:MARK1:Y?')                # Get Marker Spot Power
    print(f'{freq:.0f}: {MkrX:.0f}Hz {MkrY:6.2f} dBm')
FSW.tock('Total test')
