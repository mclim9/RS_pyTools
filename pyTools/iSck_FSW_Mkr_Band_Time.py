""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
import timeit

def main():
    FSW = iSocket().open('192.168.58.109', 5025)
    ChSpan = 100e6
    freq   = 1e9

    FSW.write(':INST:SEL "Spectrum"')                       # Select Spectrum
    FSW.write(f':SENS:WIND1:DET1:FUNC RMS')                 # RMS Detector
    FSW.write(f':SENS:FREQ:CENT {freq}')                    # Center Freq
    FSW.write('INIT:CONT OFF')                              # Single Sweep
    FSW.write(f':CALC1:MARK1:FUNC:BPOW:STAT ON')            # Turn on Band Marker
    FSW.write(f':CALC1:MARK1:FUNC:BPOW:SPAN {ChSpan}')      # Set Band Marker Span
    FSW.write(f':CALC1:MARK1:X {freq}')                     # Set Marker Frequency

    tick = timeit.default_timer()
    FSW.query('INIT:IMM:*OPC?')
    MkrX = FSW.queryFloat(':CALC1:MARK1:X?')                # Get Marker Frequency
    MkrY = FSW.queryFloat(':CALC1:MARK1:Y?')                # Get Marker Spot Power
    MkrB = FSW.queryFloat(':CALC1:MARK1:FUNC:BPOW:RES?')    # Get Marker Band Power
    timeDelta = timeit.default_timer() - tick
    print(f'TTime: {timeDelta:.6f} sec')

    print(f'{ChSpan} {MkrX} {MkrY:6.2f} {MkrB:6.2f}')
    print(FSW.query('SYST:ERR?'))

main()
