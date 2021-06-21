""" Rohde & Schwarz Automation for demonstration use."""
# ##############################################################################
# ## User Entry
# ##############################################################################
import socket                               # Import socket module

def sQuery(SCPI):
    """Socket Query"""
    sWrite(SCPI)
    sOut = s.recv(1000)                     # Read socket
    # print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):
    """Socket Write"""
    # print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds

chunk = 100
sWrite('FORM:DATA REAL,32')                 # 4 bytes per I or Q
sWrite('TRAC:IQ:DATA:FORM IQP')
recLent = int(sQuery(f':TRAC:IQ:RLEN?').decode())
IQBytes = b''
for i in range(recLent // chunk):
    rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
    numBytes = int(chr(rdChunk[1]))         # Number of Bytes
    numIQ    = int(rdChunk[2:2 + numBytes])
    IQBytes  += rdChunk[(numBytes + 2):-1]  # Remove Header

IQPoints = len(IQBytes) / 8                 # 4 bytes I + 4 bytes Q
print(f'{IQPoints} IQ Points')
