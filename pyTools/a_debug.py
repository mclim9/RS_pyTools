""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module
import time


def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode()          # Read socket
    # print(f'Query: {sOut}')
    return sOut.strip()


def sWrite(SCPI):                           # Socket Write
    # print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI


# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.114', 5025))
s.settimeout(5)                             # Timeout in seconds

# sWrite('FORM:DATA ASCII')
sWrite('FORM:DATA REAL,32')
sWrite('TRAC:IQ:DATA:FORM IQP')
# rdStr = sQuery(f':STAT:QUES:POW:COND?')
# sWrite(':STAT:QUES:INT:ENAB 4')
# rdStr = sQuery(f':STAT:QUES:INT:COND?')
rdStr = sQuery(f'*IDN?')

print(rdStr)
