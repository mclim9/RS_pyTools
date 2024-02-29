""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)

FSW.write(':CALC1:MARK1:MAX:PEAK')
MkrX = FSW.queryFloat(':CALC1:MARK1:X?')                # Get Marker Frequency
MkrY = FSW.queryFloat(':CALC1:MARK1:Y?')                # Get Marker Spot Power
print(f'{MkrX:.0f} Hz {MkrY:6.2f} dBm')
