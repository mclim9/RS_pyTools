""" Rohde & Schwarz Automation for demonstration use."""
#pylint: disable=E0611,E0401
#pylint: disable=invalid-name
##########################################################
### User Entry
##########################################################
import socket                       #Import socket module
host = '192.168.1.109'             #Instrument IP address
port = 5025                         #Instrument control port

##########################################################
### Code Begin
##########################################################

def sQuery(SCPI):
    """Socket Query"""
    out = SCPI + "\n"
    s.sendall(out.encode())             #Write 'cmd'
    sOut = s.recv(2048).strip()         #read socket
    return sOut.decode()

def sWrite(SCPI):
    """Socket Write"""
    out = SCPI + "\n"
    s.sendall(out.encode())             #Write 'cmd'

##########################################################
### Main Code
##########################################################
s = socket.socket()                     #Create a socket object
s.connect((host, port))
s.settimeout(1)                         #Timeout in seconds

sWrite(':INST:SEL "Analog Demod"')      # Select Analog Demod
sWrite(':INIT:CONT OFF')                # Single Sweep
sWrite(':DISP:WIND1:SUBW:TRAC:Y:SCAL:PDIV 200e6')
sWrite(':SENS:BWID:DEM 200e6')
sWrite(':CALC1:MARK1:STAT ON')          # Window1 Marker1 ON
sWrite(':CALC1:MARK2:STAT ON')          # Window1 Marker2 ON
for i in range(10000):
    sWrite(':INIT:IMM;*OPC?')
    mkr1 = sQuery(':CALC1:MARK1:Y?')
    mkr2 = sQuery(':CALC1:MARK2:Y?')
    print(f'Marker1:{mkr1} Marker2:{mkr2}')
