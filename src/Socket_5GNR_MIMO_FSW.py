"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name

import socket                                                           #Import socket module
host = '192.168.58.109'                                                 #Instrument IP address

###############################################################################
### Code Begin
###############################################################################
def sQuery(SCPI):
    '''socket query'''
    out = SCPI + "\n"
    s.sendall(out.encode())                                             #Write 'cmd'
    sOut = s.recv(2048).strip()                                         #read socket
    return sOut.decode()

def sWrite(SCPI):
    '''socket write'''
    out = SCPI + "\n"
    s.sendall(out.encode())

###############################################################################
### Main Code
###############################################################################
s = socket.socket()                                                     # Create a socket object
s.connect((host, 5025))
s.settimeout(1)                                                         # Timeout in seconds

AntPort = 1000
sWrite(':SENS:FREQ:CENT 1e9')                                           # Center Frequency
sWrite(':INST:CRE:NEW NR5G, "5G NR"')                                   # Start 5GNR
sWrite(':INIT:CONT ON')                                                 # Continuous Sweep
sWrite(':MMEM:LOAD:DEM:CC1 "C:\\R_S\\Instr\\user\\Demo\\5GNR-FR2-Demo\\DL-100MHz-120kHz-256QAM.allocation"')
if AntPort == 1000:
    sWrite(':CONF:NR5G:DL:CC1:PAM1:STAT ON')                            # PDSCH AntPort 1000
else:
    sWrite(':CONF:NR5G:DL:CC1:PAM2:STAT ON')                            # PDSCH AntPort 1001
sWrite(':CONF:NR5G:DL:CC1:IDC ON')                                      # Ignore DC
sWrite(':CONF:NR5G:DL:CC1:RFUC:STAT OFF')                               # Phase Compensation OFF
sWrite(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:CLM LC21')              # PDSCH Layers 2/1
sWrite(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:AP 1000, 1001')    # PDSCH Antenna ports 0,1