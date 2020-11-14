"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name

import socket                                           #Import socket module
host = '192.168.58.114'                                 #Instrument IP address

###############################################################################
### Code Begin
###############################################################################
def sQuery(SCPI):
    '''socket query'''
    out = SCPI + "\n"
    s.sendall(out.encode())                                                         #Write 'cmd'
    sOut = s.recv(2048).strip()                                                     #read socket
    return sOut.decode()

def sWrite(SCPI):
    '''socket write'''
    out = SCPI + "\n"
    s.sendall(out.encode())                                                         #Write 'cmd'

###############################################################################
### Main Code
###############################################################################
s = socket.socket()                                                                 # Create a socket object
s.connect((host, 5025))
s.settimeout(1)                                                                     # Timeout in seconds

AntPort = 1000
sWrite(':SOUR1:FREQ:CW 1e9')                                                        # Center Frequency
sWrite(':SOUR1:BB:NR5G:STAT 0')                                                     # Baseband off
sWrite(':SOUR1:BB:NR5G:SETTing:LOAD "/var/user/FR2_Demo/DL-100MHz-120kHz-256QAM"')
sWrite(':SOUR1:BB:NR5G:NODE:RFPH:MODE 0')                                           # Phase Compensation OFF
sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSC:TXSC:NLAY 2')           # PDSCH Layers 2/1
if AntPort == 1000:
    sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL0:ROW0:REAL 1')   # PDSCH AntPorts 1000
    sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL1:ROW0:REAL 0')   # PDSCH AntPorts 1000
else:
    sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL0:ROW0:REAL 0')   # PDSCH AntPort 1001
    sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL1:ROW0:REAL 1')   # PDSCH AntPort 1001
sWrite(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSC:TXSC:CDMD 1')           # CDM Group
sWrite(':SOUR1:BB:NR5G:STAT 1')                                                     # Baseband On
