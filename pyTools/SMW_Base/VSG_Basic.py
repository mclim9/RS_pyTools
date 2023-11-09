""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

SMW = iSocket().open('192.168.58.115', 5025)

SMW.write(f':SOUR1:FREQ:CW 12e9')           # Center Frequency
SMW.query(f':SOUR1:POW:LEV -10;*OPC?')      # RMS Power Level
SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')     # Power Offset
SMW.write(f':SOUR1:IQ:STAT 0')              # IQ Modulation OFF
SMW.write(f':OUTP1:STAT 1')                 # RF ON
