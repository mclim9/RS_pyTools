"""Rohde & Schwarz Automation for demonstration use. """

from iSocket import iSocket                                                         # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
s = iSocket.sOpen('192.168.58.114', 5025)
# s.settimeout(1)                                                                   # Timeout in seconds

AntPort = 1000
s.sWrite(':SOUR1:FREQ:CW 1e9')                                                      # Center Frequency
s.sWrite(':SOUR1:BB:NR5G:STAT 0')                                                   # Baseband off
s.sWrite(':SOUR1:BB:NR5G:SETTing:LOAD "/var/user/FR2_Demo/DL-100MHz-120kHz-256QAM"')
s.sWrite(':SOUR1:BB:NR5G:NODE:RFPH:MODE 0')                                         # Phase Compensation OFF
s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSC:TXSC:NLAY 2')         # PDSCH Layers 2/1
if AntPort == 1000:
    s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL0:ROW0:REAL 1') # PDSCH AntPorts 1000
    s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL1:ROW0:REAL 0') # PDSCH AntPorts 1000
else:
    s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL0:ROW0:REAL 0') # PDSCH AntPort 1001
    s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL1:ROW0:REAL 1') # PDSCH AntPort 1001
s.sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSC:TXSC:CDMD 1')         # CDM Group
s.sWrite(':SOUR1:BB:NR5G:STAT 1')                                                   # Baseband On
