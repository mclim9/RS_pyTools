"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket                                                         # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
s = iSocket().open('192.168.58.114', 5025)
# s.settimeout(1)                                                                   # Timeout in seconds
cellID = 1

s.write(':SOUR1:FREQ:CW 1e9')                                                       # Center Frequency
# s.write('*RST;*CLS;*OPC?')

# Use the Wizzard to define a FR1 reference signal (FR2 not supported)
s.write('BB:NR5G:TCW:BSCL LOC')
s.write('BB:NR5G:TCW:TC TS381411_TC72')
s.write('BB:NR5G:TCW:TRIG AAUT')
s.write('BB:NR5G:TCW:MARK FRAM')
s.write('BB:NR5G:TCW:WS:RFFR 1950e6')
s.write('BB:NR5G:TCW:WS:CBW BW100')
s.write('BB:NR5G:TCW:WS:SCSP N60')
s.write(f'BB:NR5G:TCW:WS:CELL {cellID}')
s.write('BB:NR5G:TCW:WS:UEID 0')
s.write('BB:NR5G:TCW:WS:TAP 0')
s.write('BB:NR5G:TCW:WS:RBOF 1')
s.write('BB:NR5G:TCW:APPL')

# Change the values, which are different in FR2
s.write('BB:NR5G:NODE:CELL0:CARD FR2')
s.write('SOUR:BB:NR5G:NODE:CELL0:TXBW:S120K:USE 1')
s.write('SOUR:BB:NR5G:NODE:CELL0:TXBW:S60K:USE 0')
s.write('SOUR:BB:NR5G:UBWP:USER0:USCH:CCOD:STAT 0')
s.write('SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN 66')
s.write('SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF 0')
s.write('SOUR:BB:NR5G:UBWP:USER0:USCH:CCOD:STAT 1')
