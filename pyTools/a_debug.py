""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode().strip()  # Read socket
    print(f'Query: {sOut}')
    return sOut


def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

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
