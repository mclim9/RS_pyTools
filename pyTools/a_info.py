""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read socket
    print(sOut)
    return sOut

s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.114', 5025))
s.settimeout(5)                             # Timeout in seconds
sQuery(f'*IDN?')

s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds
sQuery(f'*IDN?')