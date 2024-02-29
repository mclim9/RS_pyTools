""" Rohde & Schwarz Automation for demonstration use."""
import socket

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')                 # Print SCPI to screen
    s.sendall(f'{SCPI}\n'.encode())         # Send SCPI to socket

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)                            # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read SCPI from socket
    print(f'Query: {sOut}')                 # Print Read to screen
    return sOut                             # Return value

s = socket.socket()                         # Create Socket
s.connect(('192.168.58.115', 5025))         # IP Address of socket
s.settimeout(5)                             # Timeout

sQuery('*IDN?')                             # Instrument Identification String
sQuery('*OPT?')                             # Query options
sQuery('SYST:DFPR?')                        # Instrument XML description
