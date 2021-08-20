""" Rohde & Schwarz Automation for demonstration use."""
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
s.connect(('192.168.58.114', 5025))
s.settimeout(5)                             # Timeout in seconds

sWrite('FORM:DATA ASCII')
print(sQuery(f'*IDN?'))
print(sQuery(f'*OPT?'))
