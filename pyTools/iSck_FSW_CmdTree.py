""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):
    sWrite(SCPI)
    return s.recv(2048).decode('ascii', 'replace')

def sQuery_sync(SCPI):
    sWrite(SCPI)
    s.recv(6)                               # Read Header
    numByte = int(s.recv(1))                # Read Data Size Bytes
    datSize = int(s.recv(numByte))          # Read Data Size
    bindata = s.recv(datSize)               # Read Data
    bindata.replace(b'\\x00', b'')
    return bindata.decode('ascii', 'replace')

def sWrite(SCPI):
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

def getSCPIPersonality():
    rdStr = sQuery(f'SYST:COMM:INT:COMM:TABL? "*"').split(';')
    for opt in rdStr:
        print(opt)

def getSCPITree():
    rdStr = sQuery_sync(f'SYST:COMM:INT:COMM:TABL? "NR5G"')
    rdStr.replace('\x00', ' ')
    print(rdStr)

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds

getSCPITree()
