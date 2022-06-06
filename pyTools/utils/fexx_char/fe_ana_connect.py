""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)

centerFreq = 41e9
FSW.write(f':SENS:EFR:STAT ON')
FSW.write(f':SENS:EFR1:CONN:CONF "FE170SR","192.168.58.171",""')
FSW.write(f':SENS:EFR1:CONN:STAT ON')
print(FSW.query(f':SENS:EFR1:CONN:CST?'))
