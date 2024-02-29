""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    return s.recv(10000000)                 # Read socket

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(10)                            # Timeout in seconds

sWrite('FORM:DATA REAL,32')                 # Binary Data
sWrite('TRAC:IQ:DATA:FORM IQP')             # IQ Pairs
rdStr = sQuery(f'TRAC:IQ:DATA:MEM?')        # Retrieve Data

HeaderBytes = int(chr(rdStr[1]))            # Number of Bytes
NumBytes    = int(rdStr[2:2 + HeaderBytes])
IQBytes  = rdStr[(HeaderBytes + 2):-1]      # Remove Header
IQPoints = len(IQBytes) / 8                 # 4 bytes I + 4 bytes Q
IQAscii  = struct.unpack("<" + 'f' * int(numIQ / 4), IQBytes)

print(f'Expected IQ: {NumBytes/8}')
print(f'Received IQ: {IQPoints}')
