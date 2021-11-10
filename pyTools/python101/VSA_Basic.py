""" Spectrum Analyzer Demo"""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode().strip()  # Read socket
    return sOut

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds

sWrite('FORM:DATA ASCII')
sWrite(':SENS:FREQ:CENT 24.0e9')
sWrite(':SENS:FREQ:SPAN 1.0e9')
sWrite(':DISP:TRAC:Y:RLEV 0')
sWrite(':INP:ATT:AUTO ON')
sWrite(':INP:ATT 10')
print(sQuery(f'*IDN?'))
