""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module
import struct

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    return s.recv(10000)                    # Read socket

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(10)                            # Timeout in seconds

chunk = 1000
sWrite('FORM:DATA REAL,32')                 # 4 bytes per I or Q
sWrite('TRAC:IQ:DATA:FORM IQP')             # IQ Pairs
recLent = int(sQuery(f':TRAC:IQ:RLEN?').decode())
IQBytes = b''
for i in range(recLent // chunk):
    rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
    rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
    if len(rdChunk) < chunk * 8:
        rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
        rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
        print(f'reread chunk{i}')
    numBytes = int(chr(rdChunk[1]))         # Number of Bytes
    numIQ    = int(rdChunk[2:2 + numBytes])
    IQBytes  += rdChunk[(numBytes + 2):-1]  # Remove Header

IQAscii  = struct.unpack("<" + 'f' * int(len(IQBytes) / 4), IQBytes)
IQPoints = len(IQBytes) / 8                 # 4 bytes I + 4 bytes Q
print(f'{IQPoints} IQ Points')
