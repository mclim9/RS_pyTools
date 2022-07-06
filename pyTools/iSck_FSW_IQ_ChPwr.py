""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
ChSpan = 10e6
SamplRate =122.88e6
FSW.write(':INST:SEL "IQ Analyzer"')                    # Select IQ Analyzer
FSW.write(f':LAY:REPL:WIND "1",FREQ')                   # Replace Window1 w/ Frequency
FSW.write(f':TRAC:IQ:SRAT {SamplRate}')                 # Set Sampling Rate (Span)
FSW.write(f':SENS:WIND1:DET1:FUNC RMS')                 # RMS Detector
FSW.write(f':CALC1:MARK1:FUNC:BPOW:STAT ON')            # Turn on Band Marker
FSW.write(f':CALC1:MARK1:FUNC:BPOW:SPAN {ChSpan}')      # Set Band Marker Span

MkrX = FSW.queryFloat(':CALC1:MARK1:X?')                # Get Marker Frequency
MkrY = FSW.queryFloat(':CALC1:MARK1:Y?')                # Get Marker Spot Power
MkrB = FSW.queryFloat(':CALC1:MARK1:FUNC:BPOW:RES?')    # Get Marker Band Power
print(f'{ChSpan} {MkrX} {MkrY:6.2f} {MkrB:6.2f}')
print(FSW.query('SYST:ERR?'))
