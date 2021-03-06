""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    return s.recv(1000)                     # Read socket

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds

# sWrite('FORM:DATA ASCII')
sWrite('FORM:DATA REAL,32')
sWrite('TRAC:IQ:DATA:FORM IQP')
rdStr = sQuery(f'TRAC:IQ:DATA:MEM?')

numBytes = int(chr(rdStr[1]))               # Number of Bytes
numIQ    = int(rdStr[2:2 + numBytes])
IQBytes  = rdStr[(numBytes + 2):-1]         # Remove Header
IQPoints = len(IQBytes) / 8                 # 4 bytes I + 4 bytes Q
print(f'{IQPoints} IQ Points')
